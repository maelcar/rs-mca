#!/usr/bin/env python3
"""Verify the Route-D F23 fixed-target marked-core key-addback floor.

The census is a raw algebraic Rule-2 obstruction.  It does not execute the
named first-match deletions and it never treats a raw Vandermonde pivot as the
actual marked-incidence matrix consumed by the rank-drop owner.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence


P = 23
RANK = 2
BETA1 = 10
SHIFT = 17
DOMAIN = tuple(range(1, P))

SOURCE_PINS = {
    "base_commit": "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e",
    "singleton_commit": "84b393ec1bc52fa662756bd117a45537007d086a",
    "singleton_note_blob": "dda538a9a36cd0c8e267c11600a49cdc5bf054d1",
    "prefix_commit": "e83962ae5ad7bacb391b691ffd37f0abef977b83",
    "prefix_note_blob": "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
    "admission_gap_commit": "8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67",
    "admission_gap_note_blob": "fdeabf0708cb8806feefae9322ed9002339332cf",
    "all_minors_owner_commit": "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0",
    "all_minors_owner_note_blob": "f24ce928df7e7170c1b4f3228d5fe9b184be50b4",
}

EXPECTED_ROWS_DIGEST = "de477753d921638e65fdbd346e6f4a7359afb51760ce32c82861bb3173ad0ce2"


class CertificateError(RuntimeError):
    """Raised when any fail-closed certificate check fails."""


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
    require(len(roots) == 2, "degree-two locator requires two roots")
    left, right = sorted(roots)
    return ((left * right) % P, (-(left + right)) % P, 1)


def polynomial_roots(poly: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        point
        for point in DOMAIN
        if sum(coefficient * pow(point, degree, P) for degree, coefficient in enumerate(poly)) % P == 0
    )


def moment(weight: Mapping[int, int], degree: int) -> int:
    return sum(coefficient * pow(root, degree, P) for root, coefficient in weight.items()) % P


def projectively_primitive(weight: Mapping[int, int]) -> bool:
    """No nontrivial scalar/sign pair stabilizes the literal signed weight."""
    for scalar in DOMAIN:
        for sign in (1, -1):
            if (scalar, sign) == (1, 1):
                continue
            transformed: dict[int, int] = {}
            for root, coefficient in weight.items():
                add_weight(transformed, (scalar * root) % P, sign * coefficient)
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
        source = tuple(sorted((core, *side_a)))
        target = tuple(sorted((core, *side_r)))
        require(set(side_a).isdisjoint(side_r), "shifted sides unexpectedly meet")
        require((sum(source) - BETA1) % P == 0, "fixed parent target drift")
        packets.append(
            {
                "S": source,
                "S_prime": target,
                "G": (core,),
                "A": tuple(sorted(side_a)),
                "R": side_r,
                "U": locator_u,
            }
        )
    packets.sort(key=lambda packet: (packet["S"], packet["S_prime"]))
    return packets


def h_roots(representative: Mapping[str, object], packet: Mapping[str, object]) -> tuple[int, ...]:
    a0 = set(representative["A"])
    r0 = set(representative["R"])
    side_a = set(packet["A"])
    side_r = set(packet["R"])
    return tuple(sorted((a0 & side_a) | (r0 & side_r)))


def comparison_record(
    representative: Mapping[str, object], packet: Mapping[str, object]
) -> dict[str, object]:
    a0 = set(representative["A"])
    r0 = set(representative["R"])
    core = set(packet["G"])
    side_a = set(packet["A"])
    side_r = set(packet["R"])

    mu = signed_weight((a0, 1), (side_r, 1), (r0, -1), (side_a, -1))
    contact_plus = a0 & core
    contact_minus = r0 & core
    kappa = signed_weight((contact_plus, 1), (contact_minus, -1))
    off_core = dict(mu)
    for root, coefficient in kappa.items():
        add_weight(off_core, root, -coefficient)

    require(all(moment(mu, degree) == 0 for degree in range(RANK + 1)), "Rule-2 moment drift")
    require(set(off_core).isdisjoint(core), "off-core weight meets literal common core")
    require(
        {root: coefficient for root, coefficient in mu.items() if root in core} == kappa,
        "contact restriction drift",
    )

    return {
        "G": packet["G"],
        "A": packet["A"],
        "R": packet["R"],
        "U": packet["U"],
        "lambda_weight": tuple(sorted(off_core.items())),
        "mu3": moment(mu, RANK + 1),
        "support": len(off_core),
        "profile": (len(contact_plus), len(contact_minus)),
        "primitive": projectively_primitive(off_core),
    }


def h_label(roots: tuple[int, ...]) -> str:
    if not roots:
        return "1"
    require(len(roots) == 1, "unexpected gcd degree in the F23 fixture")
    return f"X-{roots[0]}"


def rows_digest(rows: Sequence[Mapping[str, object]]) -> str:
    serializable = [
        {
            "G": row["G"],
            "A": row["A"],
            "R": row["R"],
            "U": row["U"],
            "lambda_weight": row["lambda_weight"],
            "mu3": row["mu3"],
            "support": row["support"],
            "profile": row["profile"],
        }
        for row in rows
    ]
    payload = json.dumps(serializable, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def summarize() -> dict[str, object]:
    packets = enumerate_packets()
    require(bool(packets), "empty packet family")
    representative = packets[0]
    require(
        representative
        == {
            "S": (1, 2, 7),
            "S_prime": (1, 4, 5),
            "G": (1,),
            "A": (2, 7),
            "R": (4, 5),
            "U": (14, 14, 1),
        },
        "canonical representative drift",
    )

    h_histogram = Counter(h_label(h_roots(representative, packet)) for packet in packets[1:])
    h_one_rows = [
        comparison_record(representative, packet)
        for packet in packets[1:]
        if not h_roots(representative, packet)
    ]
    extension_count = sum(row["mu3"] == 0 for row in h_one_rows)
    survivors = [row for row in h_one_rows if row["mu3"] != 0]

    require(len({packet["U"] for packet in packets}) == len(packets), "Rule-1 key collision appeared")
    require(all(row["support"] >= RANK + 3 for row in survivors), "BC/support-collapse row survived")
    require(all(row["primitive"] for row in survivors), "nonprimitive row survived")
    require(
        len({row["lambda_weight"] for row in survivors}) == len(survivors),
        "off-core lambda collision appeared",
    )
    require(rows_digest(survivors) == EXPECTED_ROWS_DIGEST, "kept-row digest drift")

    core_histogram = Counter(row["G"][0] for row in survivors)
    support_histogram = Counter(row["support"] for row in survivors)
    profile_histogram = Counter(str(row["profile"]) for row in survivors)

    return {
        "status": "COUNTEREXAMPLE",
        "claim_class": "RAW_ALGEBRAIC_COUNTEREXAMPLE_NEW_FLOOR",
        "theorem_id": "FIXED_TARGET_MARKED_CORE_KEY_ADDBACK_FLOOR",
        "provenance": SOURCE_PINS,
        "parameters": {
            "field": "F_23",
            "domain": "F_23^*",
            "r": RANK,
            "beta1": BETA1,
            "c": SHIFT,
            "printed_fixed_key": "(r,c,U0,H,beta)",
        },
        "canonical_representative": {
            "G0": list(representative["G"]),
            "A0": list(representative["A"]),
            "R0": list(representative["R"]),
            "U0_ascending_coefficients": list(representative["U"]),
        },
        "census": {
            "packets": len(packets),
            "distinct_U": len({packet["U"] for packet in packets}),
            "rule1_deletions": 0,
            "H_histogram": dict(sorted(h_histogram.items())),
            "H_equals_1": len(h_one_rows),
            "extension_deletions": extension_count,
            "kept_distinct_lambda": len(survivors),
            "distinct_literal_G": len(core_histogram),
            "maximum_fixed_G_fiber": max(core_histogram.values()),
            "support_histogram": {str(key): value for key, value in sorted(support_histogram.items())},
            "contact_profile_histogram": dict(sorted(profile_histogram.items())),
            "kept_rows_sha256": rows_digest(survivors),
        },
        "cardinality_no_go": {
            "field_labels": P,
            "profile_field_labels": RANK * P,
            "complete_bases": len(survivors),
            "exceeds_field": len(survivors) > P,
            "exceeds_profile_times_field": len(survivors) > RANK * P,
        },
        "ownership": {
            "literal_common_core_preserved": True,
            "all_survivors_projectively_primitive": True,
            "raw_vandermonde_is_actual_incidence": False,
            "actual_incidence_matrix_constructed": False,
            "only_actual_all_maximal_minors_vanishing_may_route": True,
            "any_fixture_packet_routed_to_rank_drop": False,
            "named_first_match_deletions_executed": False,
            "post_first_match_counterexample_claimed": False,
            "deployed_bound_refuted": False,
        },
    }


EXPECTED = {
    "status": "COUNTEREXAMPLE",
    "claim_class": "RAW_ALGEBRAIC_COUNTEREXAMPLE_NEW_FLOOR",
    "theorem_id": "FIXED_TARGET_MARKED_CORE_KEY_ADDBACK_FLOOR",
    "provenance": SOURCE_PINS,
    "parameters": {
        "field": "F_23",
        "domain": "F_23^*",
        "r": 2,
        "beta1": 10,
        "c": 17,
        "printed_fixed_key": "(r,c,U0,H,beta)",
    },
    "canonical_representative": {
        "G0": [1],
        "A0": [2, 7],
        "R0": [4, 5],
        "U0_ascending_coefficients": [14, 14, 1],
    },
    "census": {
        "packets": 75,
        "distinct_U": 75,
        "rule1_deletions": 0,
        "H_histogram": {"1": 56, "X-2": 5, "X-4": 5, "X-5": 4, "X-7": 4},
        "H_equals_1": 56,
        "extension_deletions": 1,
        "kept_distinct_lambda": 55,
        "distinct_literal_G": 21,
        "maximum_fixed_G_fiber": 5,
        "support_histogram": {"5": 1, "6": 5, "7": 21, "8": 28},
        "contact_profile_histogram": {"(0, 0)": 43, "(0, 1)": 6, "(1, 0)": 6},
        "kept_rows_sha256": EXPECTED_ROWS_DIGEST,
    },
    "cardinality_no_go": {
        "field_labels": 23,
        "profile_field_labels": 46,
        "complete_bases": 55,
        "exceeds_field": True,
        "exceeds_profile_times_field": True,
    },
    "ownership": {
        "literal_common_core_preserved": True,
        "all_survivors_projectively_primitive": True,
        "raw_vandermonde_is_actual_incidence": False,
        "actual_incidence_matrix_constructed": False,
        "only_actual_all_maximal_minors_vanishing_may_route": True,
        "any_fixture_packet_routed_to_rank_drop": False,
        "named_first_match_deletions_executed": False,
        "post_first_match_counterexample_claimed": False,
        "deployed_bound_refuted": False,
    },
}


def validate(certificate: Mapping[str, object]) -> None:
    require(certificate == EXPECTED, "certificate does not match the fail-closed expected object")


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
    raise CertificateError(f"unsupported tamper leaf type: {type(value).__name__}")


def tamper_selftest(certificate: dict[str, object]) -> int:
    paths = tuple(leaf_paths(certificate))
    caught = 0
    for path in paths:
        broken = copy.deepcopy(certificate)
        cursor: object = broken
        for key in path[:-1]:
            cursor = cursor[key]  # type: ignore[index]
        key = path[-1]
        cursor[key] = mutate_leaf(cursor[key])  # type: ignore[index]
        try:
            validate(broken)
        except CertificateError:
            caught += 1

    extra = copy.deepcopy(certificate)
    extra["unexpected"] = True
    try:
        validate(extra)
    except CertificateError:
        caught += 1

    missing = copy.deepcopy(certificate)
    del missing["ownership"]
    try:
        validate(missing)
    except CertificateError:
        caught += 1

    require(caught == len(paths) + 2, "tamper self-test failed open")
    return caught


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper", action="store_true", help="run exhaustive fail-closed leaf mutation tests")
    args = parser.parse_args()

    certificate = summarize()
    validate(certificate)
    if args.tamper:
        caught = tamper_selftest(certificate)
        print(f"TAMPER: PASS ({caught} mutations rejected)")
    else:
        print(json.dumps(certificate, indent=2, sort_keys=True))
        print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
