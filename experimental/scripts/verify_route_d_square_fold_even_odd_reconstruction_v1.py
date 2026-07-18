#!/usr/bin/env python3
"""Verify the Route-D square-fold even/odd reconstruction packet.

The verifier rebuilds the SHA-pinned raw F23 Rule-2 family, folds every
off-core signed weight through x |-> x^2, checks exact even/odd recovery, and
exhibits a three-member failure of odd-data-plus-pivot recovery.  It does not
execute unavailable first-match projectors or construct an actual RIM matrix.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence


P = 23
RANK = 2
BETA1 = 10
SHIFT = 17
DOMAIN = tuple(range(1, P))

SOURCE_PINS = {
    "base_commit": "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e",
    "prefix_commit": "e83962ae5ad7bacb391b691ffd37f0abef977b83",
    "prefix_note_blob": "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
    "singleton_commit": "84b393ec1bc52fa662756bd117a45537007d086a",
    "singleton_note_blob": "dda538a9a36cd0c8e267c11600a49cdc5bf054d1",
    "f23_precursor_commit": "f23a3b78a6bbe1d50a81b3976f92aa7c135ab300",
    "f23_precursor_note_blob": "5214d5d7fc91dab3f5ba12aabf5fef0c26922e9b",
    "f23_precursor_verifier_blob": "678463a3a188ecdb07c7bd7cd6f66401895d0eeb",
    "marked_transfer_commit": "332153d6e74403e3ad20f367ff4a3df8406a30bf",
    "marked_transfer_note_blob": "6ce5a571ca05f774a6569a9c78d9cb69e8fc896a",
    "marked_fold_commit": "3d9e4c01ac8dce2e6d9f73b3ab124977f8e18835",
    "marked_fold_note_blob": "13479a4b8de5f495508375a16366b62efe39acab",
    "admission_gap_commit": "8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67",
    "admission_gap_note_blob": "fdeabf0708cb8806feefae9322ed9002339332cf",
    "all_minors_owner_commit": "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0",
    "all_minors_owner_note_blob": "f24ce928df7e7170c1b4f3228d5fe9b184be50b4",
}

PRECURSOR_ROWS_DIGEST = "de477753d921638e65fdbd346e6f4a7359afb51760ce32c82861bb3173ad0ce2"
ALL_FOLD_ROWS_DIGEST = "f6ac27af0adff1a4e864c0b565c9e3b3e524c08ab7bfac9ac940e7f1583b8877"
COLLISION_FAMILY_DIGEST = "0b95b519f541e314a5809cea782afaad97126c2a9f44ca1de21ec5c5c2da52b7"


class CertificateError(RuntimeError):
    """Raised when a fail-closed check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def add_weight(weight: dict[int, int], root: int, coefficient: int) -> None:
    value = weight.get(root, 0) + coefficient
    if value:
        weight[root] = value
    else:
        weight.pop(root, None)


def signed_weight(*terms: tuple[Iterable[int], int]) -> dict[int, int]:
    weight: dict[int, int] = {}
    for roots, coefficient in terms:
        for root in roots:
            add_weight(weight, root, coefficient)
    return weight


def locator_pair(roots: Sequence[int]) -> tuple[int, int, int]:
    left, right = sorted(roots)
    return ((left * right) % P, (-(left + right)) % P, 1)


def polynomial_roots(poly: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        point for point in DOMAIN
        if sum(coefficient * pow(point, degree, P)
               for degree, coefficient in enumerate(poly)) % P == 0
    )


def moment(weight: Mapping[int, int], degree: int) -> int:
    return sum(
        coefficient * pow(root, degree, P)
        for root, coefficient in weight.items()
    ) % P


def projectively_primitive(weight: Mapping[int, int]) -> bool:
    for scalar in DOMAIN:
        for sign in (1, -1):
            if (scalar, sign) == (1, 1):
                continue
            transformed: dict[int, int] = {}
            for root, coefficient in weight.items():
                add_weight(transformed, scalar * root % P, sign * coefficient)
            if transformed == weight:
                return False
    return True


def enumerate_packets() -> list[dict[str, object]]:
    packets: list[dict[str, object]] = []
    for side_a in itertools.combinations(DOMAIN, RANK):
        core = (BETA1 - sum(side_a)) % P
        if core == 0 or core in side_a:
            continue
        locator_u = locator_pair(side_a)
        locator_v = ((locator_u[0] - SHIFT) % P, locator_u[1], 1)
        side_r = polynomial_roots(locator_v)
        if len(side_r) != RANK or core in side_r:
            continue
        require(set(side_a).isdisjoint(side_r), "packet sides meet")
        packets.append({
            "S": tuple(sorted((core, *side_a))),
            "S_prime": tuple(sorted((core, *side_r))),
            "G": (core,),
            "A": tuple(sorted(side_a)),
            "R": side_r,
            "U": locator_u,
        })
    packets.sort(key=lambda packet: (packet["S"], packet["S_prime"]))
    require(len(packets) == 75, "F23 packet census drift")
    require(len({packet["U"] for packet in packets}) == 75,
            "Rule-1 key collision appeared")
    return packets


def h_roots(representative: Mapping[str, object], packet: Mapping[str, object]) -> tuple[int, ...]:
    return tuple(sorted(
        (set(representative["A"]) & set(packet["A"]))
        | (set(representative["R"]) & set(packet["R"]))
    ))


def square_fibers() -> tuple[tuple[int, int, int], ...]:
    seen = set()
    fibers = []
    for root in DOMAIN:
        image = root * root % P
        if image in seen:
            continue
        seen.add(image)
        chosen = min(root, (-root) % P)
        fibers.append((image, chosen, (-chosen) % P))
    fibers.sort()
    require(len(fibers) == (P - 1) // 2, "square-fiber census drift")
    return tuple(fibers)


def fold_weight(weight: Mapping[int, int]) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (image, weight.get(root, 0) + weight.get(negative, 0),
         weight.get(root, 0) - weight.get(negative, 0))
        for image, root, negative in square_fibers()
    )


def reconstruct_weight(folded: Sequence[tuple[int, int, int]]) -> dict[int, int]:
    fiber_by_image = {image: (root, negative) for image, root, negative in square_fibers()}
    recovered: dict[int, int] = {}
    for image, occupancy, signed in folded:
        require((occupancy + signed) % 2 == 0 and (occupancy - signed) % 2 == 0,
                "fold parity drift")
        root, negative = fiber_by_image[image]
        add_weight(recovered, root, (occupancy + signed) // 2)
        add_weight(recovered, negative, (occupancy - signed) // 2)
    return recovered


def lex_weighted_pivot(weight: Mapping[int, int]) -> int:
    support = sorted(weight)
    require(len(support) >= 3, "pivot support too small")
    columns = [
        (weight[root] % P, weight[root] * root % P,
         weight[root] * root * root % P)
        for root in support[:3]
    ]
    matrix = [[columns[column][row] for column in range(3)] for row in range(3)]
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    ) % P


def sha256_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def precursor_rows_digest(rows: Sequence[Mapping[str, object]]) -> str:
    serializable = [{
        "G": row["G"], "A": row["A"], "R": row["R"], "U": row["U"],
        "lambda_weight": row["lambda"], "mu3": row["mu3"],
        "support": row["support"], "profile": row["profile"],
    } for row in rows]
    return sha256_json(serializable)


def build_rows() -> list[dict[str, object]]:
    packets = enumerate_packets()
    representative = packets[0]
    require(representative == {
        "S": (1, 2, 7), "S_prime": (1, 4, 5), "G": (1,),
        "A": (2, 7), "R": (4, 5), "U": (14, 14, 1),
    }, "canonical representative drift")
    a0, r0 = set(representative["A"]), set(representative["R"])
    rows = []
    h_one_count = 0
    extension_count = 0
    for packet_index, packet in enumerate(packets[1:], start=1):
        if h_roots(representative, packet):
            continue
        h_one_count += 1
        core, side_a, side_r = set(packet["G"]), set(packet["A"]), set(packet["R"])
        mu = signed_weight((a0, 1), (side_r, 1), (r0, -1), (side_a, -1))
        require(all(moment(mu, degree) == 0 for degree in range(3)),
                "Rule-2 moment drift")
        mu3 = moment(mu, 3)
        if mu3 == 0:
            extension_count += 1
            continue
        contact = signed_weight((a0 & core, 1), (r0 & core, -1))
        off_core = dict(mu)
        for root, coefficient in contact.items():
            add_weight(off_core, root, -coefficient)
        require(set(off_core).isdisjoint(core), "literal common core lost")
        require(len(off_core) >= RANK + 3, "non-full support survived")
        require(projectively_primitive(mu) and projectively_primitive(off_core),
                "primitive filter drift")
        folded = fold_weight(off_core)
        require(reconstruct_weight(folded) == off_core, "even/odd reconstruction failed")
        for exponent in range(3):
            even = sum(occupancy * pow(image, exponent, P)
                       for image, occupancy, _ in folded) % P
            odd = sum(signed * root * pow(image, exponent, P)
                      for (image, _, signed), (_, root, _) in zip(folded, square_fibers())) % P
            require(even == moment(off_core, 2 * exponent), "even moment fold drift")
            require(odd == moment(off_core, 2 * exponent + 1), "odd moment fold drift")
        even_sparse = tuple((image, occupancy) for image, occupancy, _ in folded if occupancy)
        odd_sparse = tuple((image, signed) for image, _, signed in folded if signed)
        rows.append({
            "packet_index": packet_index,
            "G": packet["G"], "A": packet["A"], "R": packet["R"], "U": packet["U"],
            "profile": (len(a0 & core), len(r0 & core)),
            "mu": tuple(sorted(mu.items())), "lambda": tuple(sorted(off_core.items())),
            "even": even_sparse, "odd": odd_sparse,
            "pivot": lex_weighted_pivot(off_core),
            "support": len(off_core), "mu3": mu3,
        })
    require(h_one_count == 56 and extension_count == 1 and len(rows) == 55,
            "75/56/55 census drift")
    require(precursor_rows_digest(rows) == PRECURSOR_ROWS_DIGEST,
            "F23 precursor digest drift")
    require(sha256_json(rows) == ALL_FOLD_ROWS_DIGEST, "fold-row digest drift")
    return rows


def summarize() -> dict[str, object]:
    rows = build_rows()
    groups: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[(row["G"], row["odd"], row["pivot"])].append(row)
    collision_families = [family for family in groups.values() if len(family) > 1]
    require(len(collision_families) == 1 and len(collision_families[0]) == 3,
            "odd/pivot collision family drift")
    family = collision_families[0]
    require(sha256_json(family) == COLLISION_FAMILY_DIGEST,
            "collision-family digest drift")
    require(all(row["G"] == (10,) and row["profile"] == (0, 0) for row in family),
            "collision literal-core mark drift")
    require(all(row["support"] == 8 and row["mu3"] == 1 for row in family),
            "collision full/nonextension drift")
    require(len({row["mu"] for row in family}) == 3
            and len({row["lambda"] for row in family}) == 3
            and len({row["even"] for row in family}) == 3,
            "collision members not distinct")
    require(all(row["mu"] == row["lambda"] for row in family),
            "zero-contact collision changed full defect")
    require(all(row["pivot"] != 0 for row in rows), "toy pivot vanished")
    size_histogram = Counter(len(family_rows) for family_rows in groups.values())
    return {
        "status": "COUNTEREXAMPLE",
        "theorems": [
            "SQUARE_FOLD_ODD_DATA_RECOVERY_NO_GO",
            "MARKED_SQUARE_FOLD_EVEN_ODD_RECONSTRUCTION",
        ],
        "provenance": SOURCE_PINS,
        "parameters": {"field": "F_23", "r": 2, "beta1": 10, "c": 17, "H": "1"},
        "fold_equations": {
            "positive_coordinate": "mu(x)=(u_y+sigma_y)/2",
            "negative_coordinate": "mu(-x)=(u_y-sigma_y)/2",
            "even_moment": "mu_(2a)=sum_y u_y*y^a",
            "odd_moment": "mu_(2a+1)=sum_y sigma_y*x_y*y^a",
        },
        "census": {
            "precursor_packets": 75,
            "fixed_H_comparisons": 56,
            "extension_deletions": 1,
            "retained_full_raw_rows": len(rows),
            "distinct_odd_data": len({row["odd"] for row in rows}),
            "distinct_G_odd_data": len({(row["G"], row["odd"]) for row in rows}),
            "distinct_G_odd_pivot": len(groups),
            "distinct_G_even_odd": len({(row["G"], row["even"], row["odd"]) for row in rows}),
            "G_odd_pivot_fiber_histogram": {str(key): value for key, value in sorted(size_histogram.items())},
            "vanishing_toy_pivots": sum(row["pivot"] == 0 for row in rows),
            "all_fold_rows_sha256": sha256_json(rows),
        },
        "collision": {
            "family_size": len(family),
            "G": list(family[0]["G"]),
            "odd": [list(pair) for pair in family[0]["odd"]],
            "pivot": family[0]["pivot"],
            "packet_indices": [row["packet_index"] for row in family],
            "supports": [row["support"] for row in family],
            "mu3": [row["mu3"] for row in family],
            "family_sha256": sha256_json(family),
        },
        "ownership": {
            "literal_common_core_preserved": True,
            "odd_data_nonzero": bool(family[0]["odd"]),
            "support8_is_full_raw_stratum": True,
            "support8_called_deployed_scale_large": False,
            "named_first_match_executor_available": False,
            "toy_pivot_is_actual_RIM": False,
            "vanishing_family_routed": False,
            "only_future_actual_all_minors_vanishing_routes_to_owner": True,
            "deployed_bound_refuted": False,
        },
    }


EXPECTED = {
    "status": "COUNTEREXAMPLE",
    "theorems": ["SQUARE_FOLD_ODD_DATA_RECOVERY_NO_GO", "MARKED_SQUARE_FOLD_EVEN_ODD_RECONSTRUCTION"],
    "provenance": SOURCE_PINS,
    "parameters": {"field": "F_23", "r": 2, "beta1": 10, "c": 17, "H": "1"},
    "fold_equations": {
        "positive_coordinate": "mu(x)=(u_y+sigma_y)/2",
        "negative_coordinate": "mu(-x)=(u_y-sigma_y)/2",
        "even_moment": "mu_(2a)=sum_y u_y*y^a",
        "odd_moment": "mu_(2a+1)=sum_y sigma_y*x_y*y^a",
    },
    "census": {
        "precursor_packets": 75, "fixed_H_comparisons": 56,
        "extension_deletions": 1, "retained_full_raw_rows": 55,
        "distinct_odd_data": 52, "distinct_G_odd_data": 52,
        "distinct_G_odd_pivot": 53, "distinct_G_even_odd": 55,
        "G_odd_pivot_fiber_histogram": {"1": 52, "3": 1},
        "vanishing_toy_pivots": 0,
        "all_fold_rows_sha256": ALL_FOLD_ROWS_DIGEST,
    },
    "collision": {
        "family_size": 3, "G": [10],
        "odd": [[2, -1], [3, 1], [4, 1], [16, -1]], "pivot": 6,
        "packet_indices": [5, 53, 58], "supports": [8, 8, 8],
        "mu3": [1, 1, 1], "family_sha256": COLLISION_FAMILY_DIGEST,
    },
    "ownership": {
        "literal_common_core_preserved": True, "odd_data_nonzero": True,
        "support8_is_full_raw_stratum": True,
        "support8_called_deployed_scale_large": False,
        "named_first_match_executor_available": False,
        "toy_pivot_is_actual_RIM": False, "vanishing_family_routed": False,
        "only_future_actual_all_minors_vanishing_routes_to_owner": True,
        "deployed_bound_refuted": False,
    },
}


def validate(certificate: Mapping[str, object]) -> None:
    require(certificate == EXPECTED, "certificate differs from fail-closed expected object")


def leaf_paths(value: object, path: tuple[object, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from leaf_paths(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from leaf_paths(child, (*path, index))
    else:
        yield path


def mutate_leaf(value: object) -> object:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "!"
    raise CertificateError(f"unsupported leaf type {type(value).__name__}")


def tamper_selftest(certificate: dict[str, object]) -> int:
    paths = tuple(leaf_paths(certificate))
    caught = 0
    for path in paths:
        broken = copy.deepcopy(certificate)
        cursor: object = broken
        for key in path[:-1]:
            cursor = cursor[key]  # type: ignore[index]
        cursor[path[-1]] = mutate_leaf(cursor[path[-1]])  # type: ignore[index]
        try:
            validate(broken)
        except CertificateError:
            caught += 1
    for operation in ("extra", "missing"):
        broken = copy.deepcopy(certificate)
        if operation == "extra":
            broken["unexpected"] = True
        else:
            del broken["ownership"]
        try:
            validate(broken)
        except CertificateError:
            caught += 1
    require(caught == len(paths) + 2, "tamper suite failed open")
    return caught


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper", action="store_true")
    args = parser.parse_args()
    certificate = summarize()
    validate(certificate)
    if args.tamper:
        print(f"TAMPER: PASS ({tamper_selftest(certificate)} mutations rejected)")
    else:
        print(json.dumps(certificate, indent=2, sort_keys=True))
        print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
