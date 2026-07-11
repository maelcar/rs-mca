#!/usr/bin/env python3
"""Certify the characteristic-three carry coordinates of orientation prefixes.

This checker is intentionally stdlib-only.  It imports the already shipped
orientation phase verifier for its finite-field and locator-polynomial
conventions, exhausts F_9 and F_27, and constructs exact affine-F_3 root-set
witnesses in F_27 and F_81.  It does not claim that carry fibers are affine.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import itertools
import json
import os
import resource
import sys
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "orientation_witt_carry_obstruction.v1"
STATUS = (
    "PROVED_SPECIAL_EXACT_COORDINATES_BOUNDED_PRECISION_OBSTRUCTION_"
    "AND_SHALLOW_MIXING"
)
CAP_BYTES = 1024**3
DEFAULT_ARTIFACT = Path(
    "experimental/data/certificates/orientation-witt-carry-obstruction/"
    "orientation_witt_carry_obstruction.json"
)
VERIFIER_PATH = Path(
    "experimental/scripts/verify_orientation_witt_carry_obstruction.py"
)
PHASE_SCRIPT = Path(
    "experimental/scripts/verify_orientation_prefix_phase_transition.py"
)
NOTE_PATH = Path(
    "experimental/notes/thresholds/orientation_witt_carry_obstruction.md"
)
SOURCE_PATHS = (
    VERIFIER_PATH,
    PHASE_SCRIPT,
    NOTE_PATH,
    Path(
        "experimental/notes/thresholds/"
        "orientation_prefix_phase_transition.md"
    ),
    Path(
        "experimental/notes/thresholds/"
        "full_agreement_orientation_saturation.md"
    ),
    Path("experimental/notes/thresholds/fi_field_discharge.md"),
)
FIELD_MODULI = {
    2: (1, 0, 1),       # X^2+1
    3: (1, 2, 0, 1),    # X^3-X+1
    4: (2, 1, 0, 0, 1), # X^4+X+2
}


class CheckFailure(AssertionError):
    """Raised when a replay invariant fails."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CheckFailure(label)


def impose_cap() -> int:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = CAP_BYTES if hard == resource.RLIM_INFINITY else min(CAP_BYTES, hard)
    if soft == resource.RLIM_INFINITY or soft > cap:
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
        soft = cap
    require(soft != resource.RLIM_INFINITY and soft <= CAP_BYTES, "one GiB cap")
    return int(soft)


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def without_hash(obj: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(obj)
    result.pop("payload_sha256", None)
    return result


def payload_hash(obj: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(without_hash(obj))).hexdigest()


def ceil_div(left: int, right: int) -> int:
    return (left + right - 1) // right


def locate_repo(explicit: Path | None) -> Path:
    if explicit is not None:
        root = explicit.expanduser().resolve()
        require((root / PHASE_SCRIPT).is_file(), "explicit repo has phase verifier")
        return root
    if os.environ.get("OWC_REPO"):
        return locate_repo(Path(os.environ["OWC_REPO"]))
    candidates = [Path.cwd().resolve(), *Path(__file__).resolve().parents]
    for candidate in candidates:
        if (candidate / PHASE_SCRIPT).is_file():
            return candidate
    raise CheckFailure("pass --repo or set OWC_REPO")


def load_phase(root: Path) -> Any:
    path = root / PHASE_SCRIPT
    spec = importlib.util.spec_from_file_location("orientation_phase_verifier", path)
    require(spec is not None and spec.loader is not None, "phase import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_many(field: Any, values: Iterable[int]) -> int:
    total = 0
    for value in values:
        total = field.add(total, value)
    return total


def field_context(module: Any, r: int) -> tuple[Any, int, tuple[int, ...]]:
    field = module.GF3Extension(FIELD_MODULI[r])
    generator = field.primitive_element()
    a = (field.q - 1) // 2
    representatives = tuple(field.pow(generator, index) for index in range(a))
    require(field.pow(generator, a) == field.neg(1), "antipodal generator")
    return field, generator, representatives


def oriented_roots(
    field: Any, representatives: tuple[int, ...], mask: int
) -> tuple[int, ...]:
    return tuple(
        value if not (mask >> index) & 1 else field.neg(value)
        for index, value in enumerate(representatives)
    )


def truncated_prefix(
    field: Any,
    representatives: tuple[int, ...],
    mask: int,
    depth: int,
) -> tuple[int, ...]:
    """Return c_1,...,c_depth for prod_i(1-root_i T)."""
    coefficients = [1] + [0] * depth
    for root in oriented_roots(field, representatives, mask):
        negative_root = field.neg(root)
        for degree in range(depth, 0, -1):
            coefficients[degree] = field.add(
                coefficients[degree],
                field.mul(negative_root, coefficients[degree - 1]),
            )
    return tuple(coefficients[1:])


def power_sum(
    field: Any, representatives: tuple[int, ...], mask: int, exponent: int
) -> int:
    return add_many(
        field,
        (
            field.pow(root, exponent)
            for root in oriented_roots(field, representatives, mask)
        ),
    )


def primitive_indices(u: int) -> tuple[int, ...]:
    return tuple(index for index in range(1, u + 1, 2) if index % 3)


def carry_indices(u: int) -> tuple[int, ...]:
    return tuple(index for index in range(3, u + 1, 6))


def build_records(module: Any, r: int) -> tuple[Any, int, tuple[int, ...], list[Any]]:
    field, generator, representatives = field_context(module, r)
    a = len(representatives)
    legal_max = a - 2
    indices = primitive_indices(legal_max)
    weights = {
        exponent: tuple(
            field.pow(generator, position * exponent) for position in range(a)
        )
        for exponent in indices
    }
    records = []
    for mask in range(2**a):
        roots = oriented_roots(field, representatives, mask)
        locator = module.locator_polynomial(field, roots)
        prefix = tuple(locator[a - index] for index in range(1, a - 1))
        moments = []
        for exponent in indices:
            moments.append(
                add_many(
                    field,
                    (
                        weight if not (mask >> position) & 1
                        else field.neg(weight)
                        for position, weight in enumerate(weights[exponent])
                    ),
                )
            )
        records.append((mask, prefix, tuple(moments)))
    require(len(records) == 2**a, f"F_{field.q} orientation count")
    return field, generator, indices, records


def map_partitions_equal(
    pairs: Iterable[tuple[tuple[int, ...], tuple[int, ...]]]
) -> bool:
    left_to_right: dict[tuple[int, ...], tuple[int, ...]] = {}
    right_to_left: dict[tuple[int, ...], tuple[int, ...]] = {}
    for left, right in pairs:
        if left_to_right.setdefault(left, right) != right:
            return False
        if right_to_left.setdefault(right, left) != left:
            return False
    return True


def smallest_new_carry_split(
    records: list[Any],
    moment_indices: tuple[int, ...],
    h: int,
    width: int,
) -> dict[str, Any]:
    active = tuple(i for i, exponent in enumerate(moment_indices) if exponent <= h)
    groups: dict[tuple[Any, ...], list[Any]] = defaultdict(list)
    for mask, prefix, moments in records:
        moment_key = tuple(moments[index] for index in active)
        groups[(moment_key, prefix[: h - 1])].append((mask, prefix))
    best: tuple[Any, ...] | None = None
    for (moment_key, prior), rows in groups.items():
        for left_index, (left_mask, left_prefix) in enumerate(rows):
            for right_mask, right_prefix in rows[left_index + 1 :]:
                if left_prefix[h - 1] == right_prefix[h - 1]:
                    continue
                if left_mask < right_mask:
                    low, high = left_mask, right_mask
                    low_c, high_c = left_prefix[h - 1], right_prefix[h - 1]
                else:
                    low, high = right_mask, left_mask
                    low_c, high_c = right_prefix[h - 1], left_prefix[h - 1]
                candidate = (
                    (low ^ high).bit_count(), low, high, low_c, high_c,
                    moment_key, prior,
                )
                if best is None or candidate[:3] < best[:3]:
                    best = candidate
    require(best is not None, f"c_{h} split exists")
    distance, left, right, left_c, right_c, moments, prior = best
    return {
        "coefficient": h,
        "left_mask": left,
        "right_mask": right,
        "left_sign_bits": [(left >> i) & 1 for i in range(width)],
        "right_sign_bits": [(right >> i) & 1 for i in range(width)],
        "hamming_distance": distance,
        "common_primitive_moments": list(moments),
        "common_locator_prefix_before_cut": list(prior),
        "left_c_h": left_c,
        "right_c_h": right_c,
        "checks": {
            "same_prior_locator": True,
            "same_active_primitive_moments": True,
            "c_h_splits": left_c != right_c,
            "minimum_pair_selected_exhaustively": True,
        },
    }


def finite_census(module: Any, r: int) -> dict[str, Any]:
    field, generator, moment_indices, records = build_records(module, r)
    q = field.q
    a = (q - 1) // 2
    orbits = module.odd_frobenius_orbits(r)
    rows = []
    for u in range(a - 1):
        active_positions = tuple(
            index for index, exponent in enumerate(moment_indices) if exponent <= u
        )
        carries = carry_indices(u)
        locator_groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
        moment_groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
        locator_values_by_moment: dict[tuple[int, ...], set[tuple[int, ...]]] = (
            defaultdict(set)
        )
        partition_pairs = []
        for mask, prefix, moments in records:
            locator_key = prefix[:u]
            moment_key = tuple(moments[index] for index in active_positions)
            enhanced_key = moment_key + tuple(prefix[index - 1] for index in carries)
            locator_groups[locator_key].append(mask)
            moment_groups[moment_key].append(mask)
            locator_values_by_moment[moment_key].add(locator_key)
            partition_pairs.append((locator_key, enhanced_key))
        locator_sizes = Counter(map(len, locator_groups.values()))
        moment_sizes = Counter(map(len, moment_groups.values()))
        locator_max = max(locator_sizes)
        moment_max = max(moment_sizes)
        odd_count = (u + 1) // 2
        carry_count = (u + 3) // 6
        primitive_count = odd_count - carry_count
        avoidance = module.avoidance_from_orbits(r, u, orbits)
        exact_partition = map_partitions_equal(partition_pairs)
        bounded_carry_lower = ceil_div(moment_max, q**carry_count)
        global_lower = ceil_div(2**a, q**odd_count)
        checks = {
            "all_orientations_partitioned": sum(locator_sizes.elements()) == len(records),
            "primitive_plus_odd_carries_equals_locator_partition": exact_partition,
            "printed_primitive_count": primitive_count == len(primitive_indices(u)),
            "printed_carry_count": carry_count == len(carries),
            "coordinate_count_is_ceil_u_over_2": (
                primitive_count + carry_count == odd_count
            ),
            "bounded_carry_pigeonhole_lower_holds": locator_max >= bounded_carry_lower,
            "global_prefix_pigeonhole_lower_holds": locator_max >= global_lower,
        }
        require(all(checks.values()), f"F_{q} exact depth-{u} carry partition")
        rows.append(
            {
                "u": u,
                "primitive_odd_moment_indices": list(primitive_indices(u)),
                "odd_carry_coefficient_indices": list(carries),
                "primitive_coordinate_count_b_u": primitive_count,
                "carry_coordinate_count": carry_count,
                "total_coordinate_count": odd_count,
                "moment_image_size": len(moment_groups),
                "locator_image_size": len(locator_groups),
                "maximum_primitive_moment_fiber": moment_max,
                "maximum_locator_prefix_fiber": locator_max,
                "maximum_locator_subfibers_in_one_moment_fiber": max(
                    map(len, locator_values_by_moment.values())
                ),
                "moment_information_set_bound_2_to_E": 2 ** avoidance["E_r_u"],
                "E_r_u": avoidance["E_r_u"],
                "bounded_carry_lower_ceil_moment_max_over_q_to_carries": (
                    bounded_carry_lower
                ),
                "global_lower_ceil_2_to_a_over_q_to_ceil_u_over_2": global_lower,
                "checks": checks,
                "all_pass": all(checks.values()),
            }
        )
    split_witnesses = []
    if q == 27:
        split_witnesses = [
            smallest_new_carry_split(records, moment_indices, h, a) for h in (3, 9)
        ]
        expected = {3: (0, 49, 3), 9: (72, 1845, 9)}
        require(
            all(
                (row["left_mask"], row["right_mask"], row["hamming_distance"])
                == expected[row["coefficient"]]
                for row in split_witnesses
            ),
            "pinned exact c3/c9 split witnesses",
        )
    checks = {
        "all_legal_depths_present": [row["u"] for row in rows] == list(range(a - 1)),
        "all_depths_pass": all(row["all_pass"] for row in rows),
        "q27_has_exact_c3_c9_splits": q != 27 or len(split_witnesses) == 2,
    }
    require(all(checks.values()), f"F_{q} finite census")
    return {
        "r": r,
        "q": q,
        "a": a,
        "orientation_count": 2**a,
        "field_modulus_ascending": list(field.modulus),
        "primitive_generator_encoded": generator,
        "depth_rows": rows,
        "exact_first_new_carry_split_witnesses": split_witnesses,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def affine_subspace(field: Any, s: int) -> set[int]:
    basis = tuple(3**index for index in range(s))
    return {
        add_many(
            field,
            (
                field.mul(coefficient, basis[index])
                for index, coefficient in enumerate(coefficients)
            ),
        )
        for coefficients in itertools.product(range(3), repeat=s)
    }


def affine_coset_witness(module: Any, r: int, s: int) -> dict[str, Any]:
    field, generator, representatives = field_context(module, r)
    q = field.q
    n = q - 1
    a = n // 2
    h = 3**s
    subspace = affine_subspace(field, s)
    alpha = 3**s
    coset = {field.add(alpha, value) for value in subspace}
    exponent_by_element = {
        field.pow(generator, exponent): exponent for exponent in range(n)
    }
    base_mask = 0
    positions = []
    exponents = []
    for value in sorted(coset):
        exponent = exponent_by_element[value]
        exponents.append(exponent)
        if exponent < a:
            position, bit = exponent, 0
        else:
            position, bit = exponent - a, 1
        require(position not in positions, "one point per antipodal pair")
        positions.append(position)
        if bit:
            base_mask |= 1 << position
    flip_mask = sum(1 << position for position in positions)
    other_mask = base_mask ^ flip_mask
    base_prefix = truncated_prefix(field, representatives, base_mask, h)
    other_prefix = truncated_prefix(field, representatives, other_mask, h)
    base_moments = tuple(
        power_sum(field, representatives, base_mask, exponent)
        for exponent in range(1, h + 1, 2)
    )
    other_moments = tuple(
        power_sum(field, representatives, other_mask, exponent)
        for exponent in range(1, h + 1, 2)
    )
    locator = module.locator_polynomial(field, tuple(sorted(coset)))
    nonzero_degrees = [
        degree for degree, coefficient in enumerate(locator) if coefficient
    ]
    expected_degrees = [0] + [3**index for index in range(s + 1)]
    checks = {
        "subspace_has_dimension_s": len(subspace) == h,
        "alpha_not_in_subspace": alpha not in subspace,
        "coset_has_h_points": len(coset) == h,
        "coset_avoids_zero": 0 not in coset,
        "coset_is_orientation_compatible": all(
            field.neg(value) not in coset for value in coset
        ),
        "translated_locator_is_affine_linearized": (
            nonzero_degrees == expected_degrees
        ),
        "all_odd_moments_through_h_equal": base_moments == other_moments,
        "locator_equal_through_h_minus_1": base_prefix[:-1] == other_prefix[:-1],
        "locator_c_h_splits": base_prefix[-1] != other_prefix[-1],
        "hamming_distance_is_h": (base_mask ^ other_mask).bit_count() == h,
        "cut_is_inside_legal_window": h <= a - 2,
    }
    require(all(checks.values()), f"F_{q} affine-coset c_{h} witness")
    return {
        "r": r,
        "q": q,
        "a": a,
        "s": s,
        "h": h,
        "subspace": "span_F3(1,t,...,t^(s-1))",
        "alpha_encoded": alpha,
        "subspace_elements_encoded": sorted(subspace),
        "affine_coset_elements_encoded": sorted(coset),
        "affine_coset_exponents_mod_q_minus_1": sorted(exponents),
        "affine_coset_locator_nonzero_degrees": nonzero_degrees,
        "base_mask": base_mask,
        "other_mask": other_mask,
        "flipped_positions": sorted(positions),
        "base_prefix_through_h": list(base_prefix),
        "other_prefix_through_h": list(other_prefix),
        "common_odd_moments_through_h": list(base_moments),
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def affine_coset_towers(module: Any) -> dict[str, Any]:
    fields = []
    for r, levels in ((3, (1, 2)), (4, (1, 2, 3))):
        rows = [affine_coset_witness(module, r, s) for s in levels]
        nested = all(
            set(rows[index]["subspace_elements_encoded"]).issubset(
                rows[index + 1]["subspace_elements_encoded"]
            )
            for index in range(len(rows) - 1)
        )
        require(nested, f"F_{3**r} nested F3 subspaces")
        fields.append(
            {
                "r": r,
                "q": 3**r,
                "levels": rows,
                "subspaces_are_nested": nested,
                "all_pass": nested and all(row["all_pass"] for row in rows),
            }
        )
    return {
        "scope_guard": (
            "the root sets are affine F3 cosets; locator/Witt fibers above "
            "the first digit are nonlinear and are not claimed affine"
        ),
        "fields": fields,
        "all_pass": all(field["all_pass"] for field in fields),
    }


def b_count(v: int) -> int:
    return (v + 1) // 2 - (v + 3) // 6


def component_length(u: int, k: int) -> int:
    require(k <= u and k % 2 == 1 and k % 3, "primitive component index")
    length = 0
    value = k
    while value <= u:
        length += 1
        value *= 3
    return length


def collective_precision(u: int, limit: int) -> tuple[int, int]:
    left = sum(b_count(u // (3**j)) for j in range(limit))
    right = sum(
        min(component_length(u, k), limit) for k in primitive_indices(u)
    )
    return left, right


def symbolic_precision_payload() -> dict[str, Any]:
    range_checks = []
    for u in range(244):
        explicit_b = len(primitive_indices(u))
        odd_count = (u + 1) // 2
        carries = len(carry_indices(u))
        lengths = [component_length(u, k) for k in primitive_indices(u)]
        range_checks.append(
            b_count(u) == explicit_b
            and carries == (u + 3) // 6
            and explicit_b + carries == odd_count
            and sum(lengths) == odd_count
            and all(
                collective_precision(u, limit)[0]
                == collective_precision(u, limit)[1]
                for limit in (1, 2, 3)
            )
        )
    require(all(range_checks), "symbolic precision identities through u=243")
    samples = []
    for u in (0, 1, 2, 3, 5, 8, 9, 11, 26, 27, 38):
        row = {"u": u, "component_lengths": {}}
        for k in primitive_indices(u):
            row["component_lengths"][str(k)] = component_length(u, k)
        row["precision_rows"] = []
        for limit in (1, 2, 3):
            left, right = collective_precision(u, limit)
            row["precision_rows"].append(
                {
                    "L": limit,
                    "D_L": left,
                    "sum_j_b_floor_u_over_3j": left,
                    "sum_k_min_s_k_L": right,
                    "pigeonhole_image_targets_q_to_D_L": {
                        "q27": 27**left,
                        "q81": 81**left,
                    },
                    "identity_holds": left == right,
                }
            )
        samples.append(row)
    return {
        "definitions": {
            "b(v)": "ceil(v/2)-floor((v+3)/6)",
            "s_k": "1+floor(log_3(u/k)) for odd k with 3 not dividing k",
            "D_L(u)": "sum_(j=0)^(L-1) b(floor(u/3^j))",
        },
        "count_identity": (
            "b(u)+#{odd n<=u:3|n}=ceil(u/2), and sum_k s_k=ceil(u/2)"
        ),
        "bounded_carry_lower": (
            "a primitive-moment fiber split by C carry coordinates has a "
            "locator subfiber of size at least ceil(moment_fiber/q^C)"
        ),
        "collective_precision_identity": (
            "D_L(u)=sum_(primitive odd k<=u) min(s_k,L)"
        ),
        "critical_samples": samples,
        "checked_u_range": [0, 243],
        "checked_precision_limits": [1, 2, 3],
        "all_pass": all(range_checks),
    }


def cos_pi_over_9_bracket() -> tuple[Decimal, Decimal]:
    """Directed bracket for the root in (0.9,1) of 8x^3-6x-1."""
    with localcontext() as context:
        context.prec = 120
        polynomial = lambda x: 8 * x**3 - 6 * x - 1
        value = Decimal("0.94")
        for _ in range(30):
            value -= polynomial(value) / (24 * value**2 - 6)
        require(Decimal("0.9") < value < 1, "cos(pi/9) root interval")
        require(abs(polynomial(value)) < Decimal("1e-110"), "cos root")
        radius = Decimal("1e-90")
        lower = value - radius
        upper = value + radius
        require(
            polynomial(lower) < 0 < polynomial(upper),
            "directed cos(pi/9) bracket",
        )
        return +lower, +upper


def decimal_string(value: Decimal, digits: int = 70) -> str:
    return format(value, f".{digits}E")


def depth_three_fourier_payload(actual_q27_max: int) -> dict[str, Any]:
    with localcontext() as context:
        context.prec = 105
        cosine_lower, cosine_upper = cos_pi_over_9_bracket()
        cosine = +cosine_upper
        rows = []
        for q in (9, 27, 81, 243, 729, 2187):
            a = (q - 1) // 2
            first = Decimal(q - 1) * (Decimal(2) ** (-(q // 3)))
            second = Decimal(q * q - q) * (cosine ** (q // 3))
            delta = first + second
            base = Decimal(2**a) / Decimal(q * q)
            upper = base * (1 + delta)
            row = {
                "q": q,
                "a": a,
                "depth_3_inside_packet_legal_window": 3 <= a - 2,
                "nontrivial_order_dividing_3_character_count": q - 1,
                "order_9_character_count": q * q - q,
                "character_count_with_trivial": 1 + (q - 1) + (q * q - q),
                "term_(q-1)2^(-q/3)": decimal_string(first),
                "term_(q^2-q)cos(pi/9)^(q/3)": decimal_string(second),
                "Delta_2": decimal_string(delta),
                "base_2^a_over_q^2": decimal_string(base),
                "upper_2^a_over_q^2_times_(1+Delta_2)": decimal_string(upper),
                "character_counts_sum_to_q_squared": (
                    1 + (q - 1) + (q * q - q) == q * q
                ),
            }
            if q == 27:
                row["exact_census_maximum_depth_3_locator_fiber"] = actual_q27_max
                row["exact_max_is_below_fourier_upper"] = (
                    Decimal(actual_q27_max) <= upper
                )
            rows.append(row)
        checks = {
            "cosine_bracket_inside_zero_one": (
                0 < cosine_lower < cosine_upper < 1
            ),
            "cosine_bracket_is_directed": (
                8 * cosine_lower**3 - 6 * cosine_lower - 1 < 0
                < 8 * cosine_upper**3 - 6 * cosine_upper - 1
            ),
            "all_character_counts_exact": all(
                row["character_counts_sum_to_q_squared"] for row in rows
            ),
            "q27_exact_max_below_bound": rows[1]["exact_max_is_below_fourier_upper"],
        }
        require(all(checks.values()), "depth-three W2 finite Fourier formula")
        return {
            "formula": (
                "Delta_2=(q-1)2^(-q/3)+(q^2-q)cos(pi/9)^(q/3); "
                "M_3<=2^a/q^2*(1+Delta_2)"
            ),
            "cos_pi_over_9_directed_bracket": {
                "lower": decimal_string(cosine_lower, 100),
                "upper_used_for_all_bounds": decimal_string(
                    cosine_upper, 100
                ),
            },
            "character_classes": (
                "1 trivial, q-1 nontrivial characters killed by 3, and "
                "q^2-q characters of exact additive order 9"
            ),
            "scope_guard": (
                "the formula gives Delta_2=o(1) as q grows; no finite-q "
                "sharpness is claimed, and q=9 depth 3 is outside the legal window"
            ),
            "rows": rows,
            "checks": checks,
            "all_pass": all(checks.values()),
        }


def build_payload(root: Path, module: Any, effective_cap: int) -> dict[str, Any]:
    finite = [finite_census(module, r) for r in (2, 3)]
    q27_depth3 = next(
        row["maximum_locator_prefix_fiber"]
        for field in finite if field["q"] == 27
        for row in field["depth_rows"] if row["u"] == 3
    )
    affine = affine_coset_towers(module)
    symbolic = symbolic_precision_payload()
    fourier = depth_three_fourier_payload(q27_depth3)
    source_pins = {}
    for path in SOURCE_PATHS:
        require((root / path).is_file(), f"source pin exists: {path}")
        source_pins[str(path)] = hashlib.sha256(
            (root / path).read_bytes()
        ).hexdigest()
    checks = {
        "finite_censuses_pass": all(field["all_pass"] for field in finite),
        "affine_coset_towers_pass": affine["all_pass"],
        "symbolic_precision_passes": symbolic["all_pass"],
        "depth_three_fourier_passes": fourier["all_pass"],
        "address_space_at_most_one_GiB": effective_cap <= CAP_BYTES,
    }
    require(all(checks.values()), "top-level checks")
    payload = {
        "schema": SCHEMA,
        "status": STATUS,
        "role": (
            "exact Witt-coordinate replay, bounded-precision obstruction, "
            "and shallow W2 mixing calibration; no frontiers-tex "
            "promotion, prize-line conclusion, or affine-fiber claim"
        ),
        "source_pins_sha256": source_pins,
        "address_space_cap_bytes": CAP_BYTES,
        "finite_exact_censuses": finite,
        "affine_F3_root_set_towers": affine,
        "symbolic_collective_precision": symbolic,
        "depth_three_W2_fourier_bound": fourier,
        "checks": checks,
        "verification": {
            "zero_argument_mode": "--check",
            "write": (
                "python3 experimental/scripts/"
                "verify_orientation_witt_carry_obstruction.py --write"
            ),
            "check": (
                "python3 experimental/scripts/"
                "verify_orientation_witt_carry_obstruction.py --check"
            ),
            "tamper_selftest": (
                "python3 experimental/scripts/"
                "verify_orientation_witt_carry_obstruction.py "
                "--tamper-selftest"
            ),
            "semantic_tamper_mutations": 8,
        },
        "nonclaims": [
            "No full fixed-c locator-prefix upper improvement is claimed.",
            "No locator or Witt fiber is claimed affine.",
            "The shallow mixing theorem is not simultaneous over all k.",
            "No prize-relevant received line or C7/FI-field payment is supplied.",
            "No statement is promoted to the frontiers TeX.",
        ],
        "all_pass": all(checks.values()),
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def validate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    require(candidate.get("schema") == SCHEMA, "artifact schema")
    require(candidate.get("status") == STATUS, "artifact status")
    require(candidate.get("payload_sha256") == payload_hash(candidate), "artifact hash")
    require(canonical(candidate) == canonical(expected), "artifact exact replay")


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations = []
    first = copy.deepcopy(expected)
    first["all_pass"] = False
    mutations.append(first)
    second = copy.deepcopy(expected)
    second["finite_exact_censuses"][1]["depth_rows"][3][
        "maximum_locator_prefix_fiber"
    ] += 1
    second["payload_sha256"] = payload_hash(second)
    mutations.append(second)
    third = copy.deepcopy(expected)
    third["affine_F3_root_set_towers"]["fields"][1]["levels"][2][
        "other_mask"
    ] ^= 1
    third["payload_sha256"] = payload_hash(third)
    mutations.append(third)
    fourth = copy.deepcopy(expected)
    fourth["symbolic_collective_precision"]["critical_samples"].pop()
    fourth["payload_sha256"] = payload_hash(fourth)
    mutations.append(fourth)
    fifth = copy.deepcopy(expected)
    fifth["depth_three_W2_fourier_bound"]["rows"][1]["Delta_2"] = "0"
    fifth["payload_sha256"] = payload_hash(fifth)
    mutations.append(fifth)
    sixth = copy.deepcopy(expected)
    sixth["source_pins_sha256"][str(NOTE_PATH)] = "0" * 64
    sixth["payload_sha256"] = payload_hash(sixth)
    mutations.append(sixth)
    seventh = copy.deepcopy(expected)
    seventh["affine_F3_root_set_towers"]["scope_guard"] = (
        "all carry fibers are affine"
    )
    seventh["payload_sha256"] = payload_hash(seventh)
    mutations.append(seventh)
    eighth = copy.deepcopy(expected)
    eighth["nonclaims"].pop()
    eighth["payload_sha256"] = payload_hash(eighth)
    mutations.append(eighth)
    caught = 0
    for mutation in mutations:
        try:
            validate(mutation, expected)
        except CheckFailure:
            caught += 1
    require(caught == len(mutations), "all tamper mutations rejected")
    return caught


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    args = parser.parse_args(argv)
    effective_cap = impose_cap()
    root = locate_repo(args.repo)
    module = load_phase(root)
    expected = build_payload(root, module, effective_cap)
    artifact = args.artifact.expanduser()
    if not artifact.is_absolute():
        artifact = root / artifact
    if args.write:
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(
            json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"WROTE {artifact} {expected['payload_sha256']}")
        print(f"RLIMIT_AS {effective_cap} bytes")
        return 0
    if args.tamper_selftest:
        count = tamper_selftest(expected)
        print(f"PASS tamper-selftest ({count} mutations)")
        return 0
    require(artifact.is_file(), f"artifact exists: {artifact}")
    candidate = json.loads(artifact.read_text(encoding="utf-8"))
    validate(candidate, expected)
    print(f"PASS {artifact} {candidate['payload_sha256']}")
    print(f"RLIMIT_AS {effective_cap} bytes")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckFailure as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
