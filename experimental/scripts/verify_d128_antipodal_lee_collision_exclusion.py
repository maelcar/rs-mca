#!/usr/bin/env python3
"""Independent exact audit of the D128 antipodal/Lee exclusion."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import sympy as sp


P = 2_147_483_647
DIMENSION = 64
REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = (
    REPO_ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "d128-blockfree-seven-moment-injectivity"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def fp2_mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (
        (left[0] * right[0] - left[1] * right[1]) % P,
        (left[0] * right[1] + left[1] * right[0]) % P,
    )


def fp2_pow(base: tuple[int, int], exponent: int) -> tuple[int, int]:
    answer = (1, 0)
    while exponent:
        if exponent & 1:
            answer = fp2_mul(answer, base)
        base = fp2_mul(base, base)
        exponent >>= 1
    return answer


def cayley(parameter: int) -> tuple[int, int]:
    inverse = pow(parameter * parameter + 1, P - 2, P)
    return (
        (parameter * parameter - 1) * inverse % P,
        2 * parameter * inverse % P,
    )


def active_domain() -> list[int]:
    # The primary generator uses parameter 2.  This audit uses parameter 3.
    eta = fp2_pow(cayley(3), 1 << 22)
    require(fp2_pow(eta, 512) == (1, 0), "eta does not have order dividing 512")
    require(fp2_pow(eta, 256) != (1, 0), "eta does not have exact order 512")
    point = eta
    step = fp2_mul(eta, eta)
    roots = []
    for _ in range(128):
        roots.append(point[0])
        point = fp2_mul(point, step)
    require(len(set(roots)) == 128, "active domain has repeated roots")
    return sorted(roots)


def chebyshev4(value: int) -> int:
    square = (2 * value * value - 1) % P
    return (2 * square * square - 1) % P


def independent_sector_coordinates() -> tuple[list[int], list[int], list[list[int]]]:
    fibers: dict[int, list[int]] = defaultdict(list)
    for root in active_domain():
        fibers[chebyshev4(root)].append(root)
    blocks = [sorted(fibers[key]) for key in sorted(fibers)]
    require(len(blocks) == 32, "wrong number of T4 blocks")
    require(all(len(block) == 4 for block in blocks), "a T4 block is not four-point")

    representatives: list[int] = []
    deltas: list[int] = []
    for block in blocks:
        reps = sorted({min(root, (-root) % P) for root in block})
        require(len(reps) == 2, "a block is not two antipodal pairs")
        u, v = reps
        require({u, -u % P, v, -v % P} == set(block), "bad antipodal block")
        require((u * u + v * v) % P == 1, "u^2+v^2 != 1")
        representatives.extend((u, v))
        deltas.append((2 * u * u - 1) % P)
        for degree, expected in enumerate((4, 0, 2, 0)):
            observed = sum(pow(root, degree, P) for root in block) % P
            require(observed == expected, f"bad block power sum in degree {degree}")
    return representatives, deltas, blocks


def read_certificate() -> dict[str, object]:
    lines = (ARTIFACTS / "antipodal_sector_lattice_certificate.txt").read_text(
        encoding="ascii"
    ).splitlines()
    require(lines[0] == "D128_ANTIPODAL_SECTOR_CERT_V1", "bad certificate magic")
    metadata = list(map(int, lines[1].split()))
    require(metadata == [P, 32, 32, 64, 9, 16], "bad certificate metadata")
    representatives = list(map(int, lines[2].split()))
    deltas = list(map(int, lines[3].split()))
    even_witness = list(map(int, lines[4].split()))
    odd_witness = list(map(int, lines[5].split()))
    cursor = 6
    even_basis = [list(map(int, lines[cursor + row].split())) for row in range(32)]
    cursor += 32 + 32 + math.comb(32, 2)
    odd_basis = [list(map(int, lines[cursor + row].split())) for row in range(64)]
    cursor += 64 + 64 + math.comb(64, 2)
    require(cursor == len(lines), "certificate section lengths do not exhaust file")
    return {
        "representatives": representatives,
        "deltas": deltas,
        "even_witness": even_witness,
        "odd_witness": odd_witness,
        "even_basis": even_basis,
        "odd_basis": odd_basis,
    }


def read_matrix(path: Path, dimension: int) -> list[list[int]]:
    rows = [
        list(map(int, re.findall(r"-?\d+", line)))
        for line in path.read_text(encoding="ascii").splitlines()
        if re.search(r"-?\d+", line)
    ]
    require(len(rows) == dimension, f"{path.name}: wrong row count")
    require(all(len(row) == dimension for row in rows), f"{path.name}: wrong column count")
    return rows


def modular_moments(vector: list[int], representatives: list[int]) -> tuple[int, int]:
    first = sum(value * root for value, root in zip(vector, representatives)) % P
    third = sum(value * pow(root, 3, P) for value, root in zip(vector, representatives)) % P
    return first, third


def assignments(twos: int, ones: int) -> int:
    support = twos + ones
    return math.comb(DIMENSION, support) * math.comb(support, twos) * (1 << support)


def load_json(name: str) -> dict[str, object]:
    return json.loads((ARTIFACTS / name).read_text(encoding="ascii"))


def parse_fixed_radius_output(name: str) -> dict[str, object]:
    output: dict[str, object] = {}
    profiles: list[tuple[int, int, int, int]] = []
    for line in (ARTIFACTS / name).read_text(encoding="ascii").splitlines()[1:]:
        if line.startswith("profile "):
            values = dict(part.split("=") for part in line.split()[1:])
            profiles.append(tuple(int(values[key]) for key in ("norm", "twos", "ones", "count")))
            continue
        key, _, value = line.partition(" ")
        if key in {"first_enumeration_coordinates", "first_lattice_vector"}:
            output[key] = list(map(int, value.split()))
        elif value and re.fullmatch(r"-?\d+", value):
            output[key] = int(value)
        else:
            output[key] = value
    output["profiles"] = profiles
    return output


def verify_basis_and_witnesses(certificate: dict[str, object]) -> dict[str, object]:
    representatives, deltas, _ = independent_sector_coordinates()
    require(certificate["representatives"] == representatives, "independent representatives differ")
    require(certificate["deltas"] == deltas, "independent deltas differ")

    even_witness = certificate["even_witness"]
    odd_witness = certificate["odd_witness"]
    require(sum(value * value for value in even_witness) == 10, "bad even witness norm")
    require(sum(value * delta for value, delta in zip(even_witness, deltas)) % P == 0,
            "even witness misses its modular equation")
    require(sum(value * value for value in odd_witness) == 17, "bad odd witness norm")
    require(modular_moments(odd_witness, representatives) == (0, 0),
            "odd norm-17 witness misses a moment")

    even_basis = certificate["even_basis"]
    odd_basis = certificate["odd_basis"]
    require(abs(int(sp.Matrix(even_basis).det(method="domain-ge"))) == P,
            "certificate even basis has wrong index")
    require(abs(int(sp.Matrix(odd_basis).det(method="domain-ge"))) == P**2,
            "certificate odd basis has wrong index")
    require(all(sum(value * delta for value, delta in zip(row, deltas)) % P == 0
                for row in even_basis), "an even basis row misses its equation")
    require(all(modular_moments(row, representatives) == (0, 0) for row in odd_basis),
            "an odd certificate basis row misses a moment")

    enumeration_basis = read_matrix(ARTIFACTS / "odd_sector_sdb40_basis.txt", 64)
    require(abs(int(sp.Matrix(enumeration_basis).det(method="domain-ge"))) == P**2,
            "enumeration basis has wrong index")
    require(all(modular_moments(row, representatives) == (0, 0) for row in enumeration_basis),
            "an enumeration basis row misses a moment")
    return {"representatives": representatives, "deltas": deltas}


def verify_ball(representatives: list[int]) -> None:
    radius15 = parse_fixed_radius_output("odd_radius15_output.txt")
    require(radius15["radius_squared"] == 15, "wrong radius-15 output")
    require(radius15["nonzero_hits"] == 0, "radius-15 enumeration found a vector")
    require(radius15["enumeration_nodes"] == 1_334_988_488, "unexpected radius-15 node count")

    ball16 = parse_fixed_radius_output("odd_ball16_output.txt")
    require(ball16["radius_squared"] == 16, "wrong radius-16 output")
    require(ball16["enumeration_mode"] == "collect_all", "radius-16 run was not exhaustive")
    require(ball16["nonzero_hits"] == 1, "unexpected number of sign-normalized ball vectors")
    require(ball16["enumeration_nodes"] == 1_491_620_685, "unexpected radius-16 node count")
    require(ball16["minimum_lee_weight"] == 16, "collision-relevant vector in the radius-16 ball")
    require(ball16["profiles"] == [(16, 0, 16, 1)], "unexpected radius-16 profile census")
    vector = ball16["first_lattice_vector"]
    require(len(vector) == 64, "bad reconstructed ball vector length")
    require(sum(value * value for value in vector) == 16, "bad reconstructed ball norm")
    require(sum(abs(value) for value in vector) == 16, "bad reconstructed ball Lee weight")
    require(modular_moments(vector, representatives) == (0, 0), "ball vector misses a moment")

    replay_basis = read_matrix(ARTIFACTS / "odd_sector_lll_replay_basis.txt", 64)
    coefficients = ball16["first_enumeration_coordinates"]
    replay_vector = [
        sum(coefficients[row] * replay_basis[row][column] for row in range(64))
        for column in range(64)
    ]
    require(replay_vector == vector, "enumeration coordinates do not reconstruct the ball vector")


def verify_profile_census() -> list[tuple[int, int]]:
    derived = {
        (twos, ones)
        for twos in range(8)
        for ones in range(0, 15, 2)
        if 2 * twos + ones <= 14 and 4 * twos + ones >= 17
    }
    expected = {
        (2, 10), (3, 6), (3, 8), (4, 2), (4, 4), (4, 6),
        (5, 0), (5, 2), (5, 4), (6, 0), (6, 2), (7, 0),
    }
    require(derived == expected, "the twelve Lee profiles were not derived exhaustively")

    generic = {
        "profile_4_2_output.json": (4, 2),
        "profile_5_0_output.json": (5, 0),
        "profile_5_2_output.json": (5, 2),
        "profile_6_0_output.json": (6, 0),
        "profile_4_4_output.json": (4, 4),
        "profile_6_2_output.json": (6, 2),
        "profile_5_4_output.json": (5, 4),
        "profile_3_6_output.json": (3, 6),
    }
    covered: set[tuple[int, int]] = set()
    for name, profile in generic.items():
        data = load_json(name)
        require(data["verdict"] == "PASS_EXCLUDE_LEE_PROFILE", f"{name}: bad verdict")
        require((data["total_twos"], data["total_ones"]) == profile, f"{name}: bad profile")
        left = (data["left_twos"], data["left_ones"])
        right = (profile[0] - left[0], profile[1] - left[1])
        require(data["left_records"] == assignments(*left), f"{name}: incomplete left census")
        require(data["right_records"] == assignments(*right), f"{name}: incomplete right census")
        require(data["disjoint_relation_found"] is False, f"{name}: collision found")
        covered.add(profile)

    profile70 = load_json("profile_7_0_output.json")
    require(profile70["verdict"] == "PASS_EXCLUDE_PROFILE_7_0", "bad (7,0) verdict")
    require(profile70["triple_records"] == assignments(3, 0), "incomplete signed triples")
    require(profile70["quadruple_records"] == assignments(4, 0), "incomplete signed quadruples")
    require(profile70["disjoint_relation_found"] is False, "(7,0) collision found")
    covered.add((7, 0))

    profile46 = load_json("profile_4_6_output.json")
    require(profile46["verdict"] == "PASS_EXCLUDE_PROFILE_4_6_BY_RAW_SYNDROME",
            "bad (4,6) verdict")
    require(profile46["left_records"] == assignments(0, 5), "incomplete (4,6) left census")
    require(profile46["right_supports"] == math.comb(64, 4) * 60,
            "incomplete (4,6) right supports")
    require(profile46["right_assignments"] == profile46["right_supports"] * 32,
            "incomplete (4,6) right assignments")
    require(profile46["raw_syndrome_match_found"] is False, "(4,6) syndrome match found")
    covered.add((4, 6))

    for name, profile in (
        ("profile_3_8_output.json", (3, 8)),
        ("profile_2_10_output.json", (2, 10)),
    ):
        data = load_json(name)
        twos, singletons = profile
        half = 7 - twos
        require(data["verdict"] == "PASS_EXCLUDE_EVEN_FIRST_PROFILE", f"{name}: bad verdict")
        require((data["twos"], data["singletons"]) == profile, f"{name}: bad profile")
        require(data["even_half_subset_records"] == math.comb(64, half),
                f"{name}: incomplete even half census")
        require(data["doubled_odd_records"] == math.comb(64, twos) * (1 << twos),
                f"{name}: incomplete doubled census")
        require(data["singleton_sign_patterns"] ==
                data["even_disjoint_relations"] * (1 << singletons),
                f"{name}: incomplete singleton signs")
        require(data["raw_odd_syndrome_matches"] == 0, f"{name}: odd match found")
        require(data["collision_found"] is False, f"{name}: collision found")
        covered.add(profile)

    independent46 = load_json("profile_4_6_even_first_crosscheck.json")
    require(independent46["even_half_subset_records"] == math.comb(64, 3),
            "independent (4,6) even census incomplete")
    require(independent46["even_disjoint_relations"] == 0,
            "independent (4,6) check found an even relation")
    require(independent46["collision_found"] is False,
            "independent (4,6) check found a collision")

    require(covered == expected, "profile output family does not cover all twelve profiles")
    return sorted(covered)


def main() -> None:
    certificate = read_certificate()
    domain_data = verify_basis_and_witnesses(certificate)
    verify_ball(domain_data["representatives"])
    profiles = verify_profile_census()

    derived_outputs = {
        "antipodal_lee_audit_output.json",
        "global_injectivity_output.json",
        "SHA256SUMS.txt",
    }
    files = sorted(
        path
        for path in ARTIFACTS.iterdir()
        if path.is_file()
        and path.suffix in {".json", ".txt"}
        and path.name not in derived_outputs
    )
    output = {
        "verdict": "PASS_D128_ANTIPODAL_LEE_COLLISION_EXCLUSION",
        "field": P,
        "domain_points": 128,
        "T4_blocks": 32,
        "independent_cayley_parameter": 3,
        "odd_lattice_rank": 64,
        "odd_lattice_index": str(P**2),
        "proved_empty_radius_squared": 15,
        "radius16_sign_normalized_classes": 1,
        "radius16_minimum_lee_weight": 16,
        "collision_profiles_excluded": [list(profile) for profile in profiles],
        "collision_profiles_excluded_count": len(profiles),
        "profile_4_6_independent_even_first_check": True,
        "audited_artifact_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
