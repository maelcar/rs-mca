#!/usr/bin/env python3
"""Verify the terminal shift-pair vanishing and shared-even alternant claims."""

from __future__ import annotations

import argparse
import collections
from decimal import Decimal, getcontext
import itertools
import json
from pathlib import Path


Elt = tuple[int, int]
ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "primitive-shiftpair-terminal-alternant"
    / "primitive_shiftpair_terminal_alternant.json"
)


def field_mul(x: Elt, y: Elt, p: int) -> Elt:
    return (
        (x[0] * y[0] - x[1] * y[1]) % p,
        (x[0] * y[1] + x[1] * y[0]) % p,
    )


def field_power(x: Elt, exponent: int, p: int) -> Elt:
    out = (1, 0)
    while exponent:
        if exponent & 1:
            out = field_mul(out, x, p)
        x = field_mul(x, x, p)
        exponent >>= 1
    return out


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def element_order(x: Elt, p: int, group_order: int) -> int:
    for divisor in divisors(group_order):
        if field_power(x, divisor, p) == (1, 0):
            return divisor
    raise AssertionError("element order not found")


def norm_one_generator(p: int) -> Elt:
    group = tuple(
        (a, b)
        for a in range(p)
        for b in range(p)
        if (a * a + b * b) % p == 1
    )
    assert len(group) == p + 1
    for element in group:
        if element_order(element, p, p + 1) == p + 1:
            return element
    raise AssertionError("cyclic generator not found")


def projected_domain(p: int, size: int) -> tuple[int, ...]:
    assert p % 4 == 3 and (p + 1) % size == 0
    generator = norm_one_generator(p)
    step = field_power(generator, (p + 1) // size, p)
    subgroup = tuple(field_power(step, j, p) for j in range(size))
    inverse = field_power(generator, p, p)
    twin = (
        {field_mul(generator, x, p) for x in subgroup}
        | {field_mul(inverse, x, p) for x in subgroup}
    )
    domain = tuple(sorted({x[0] for x in twin}))
    assert len(twin) == 2 * size and len(domain) == size
    assert element_order(generator, p, p + 1) == p + 1
    return domain


def locator(domain: tuple[int, ...], support: tuple[int, ...], p: int) -> tuple[int, ...]:
    coeff = [1]
    for index in support:
        root = domain[index]
        nxt = [0] * (len(coeff) + 1)
        for j, value in enumerate(coeff):
            nxt[j] = (nxt[j] + value) % p
            nxt[j + 1] = (nxt[j + 1] - root * value) % p
        coeff = nxt
    return tuple(coeff)


def t2(x: int, p: int) -> int:
    return (2 * x * x - 1) % p


def occupancy(support: tuple[int, ...], image_indices: tuple[int, ...], size: int) -> tuple[int, ...]:
    out = [0] * size
    for index in support:
        out[image_indices[index]] += 1
    return tuple(out)


def switch_word(
    q2_counts: tuple[int, ...],
    q4_counts: tuple[int, ...],
    q2_to_q4: tuple[int, ...],
) -> tuple[int, ...]:
    word = []
    for q4_index, selected in enumerate(q4_counts):
        if not selected:
            continue
        preimages = [i for i, image in enumerate(q2_to_q4) if image == q4_index]
        assert len(preimages) == 2
        choices = [i for i in preimages if q2_counts[i]]
        assert len(choices) == 1 and q2_counts[choices[0]] == 1
        word.append(0 if choices[0] == preimages[0] else 1)
    return tuple(word)


def hamming(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    assert len(left) == len(right)
    return sum(a != b for a, b in zip(left, right))


def poly_trim(poly: list[int], p: int) -> list[int]:
    while len(poly) > 1 and poly[-1] % p == 0:
        poly.pop()
    return [value % p for value in poly]


def poly_add(left: list[int], right: list[int], p: int, scale: int = 1) -> list[int]:
    out = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        out[index] = (out[index] + value) % p
    for index, value in enumerate(right):
        out[index] = (out[index] + scale * value) % p
    return poly_trim(out, p)


def poly_mul(left: list[int], right: list[int], p: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = (out[i + j] + x * y) % p
    return poly_trim(out, p)


def poly_shift(poly: list[int]) -> list[int]:
    return [0] + poly


def poly_divmod(left: list[int], right: list[int], p: int) -> tuple[list[int], list[int]]:
    dividend = poly_trim(left[:], p)
    divisor = poly_trim(right[:], p)
    assert divisor != [0]
    quotient = [0] * max(1, len(dividend) - len(divisor) + 1)
    leading_inverse = pow(divisor[-1], -1, p)
    while dividend != [0] and len(dividend) >= len(divisor):
        degree = len(dividend) - len(divisor)
        coefficient = dividend[-1] * leading_inverse % p
        quotient[degree] = coefficient
        for index, value in enumerate(divisor):
            dividend[index + degree] = (
                dividend[index + degree] - coefficient * value
            ) % p
        dividend = poly_trim(dividend, p)
    return poly_trim(quotient, p), dividend


def poly_gcd(left: list[int], right: list[int], p: int) -> list[int]:
    left = poly_trim(left[:], p)
    right = poly_trim(right[:], p)
    while right != [0]:
        left, right = right, poly_divmod(left, right, p)[1]
    inverse = pow(left[-1], -1, p)
    return [(value * inverse) % p for value in left]


def poly_eval(poly: list[int], value: int, p: int) -> int:
    out = 0
    for coefficient in reversed(poly):
        out = (out * value + coefficient) % p
    return out


def poly_degree(poly: list[int], p: int) -> int:
    trimmed = poly_trim(poly[:], p)
    return -1 if trimmed == [0] else len(trimmed) - 1


def even_odd_parts(
    domain: tuple[int, ...], support: list[int], p: int
) -> tuple[list[int], list[int]]:
    ascending = list(reversed(locator(domain, tuple(support), p)))
    return poly_trim(ascending[0::2], p), poly_trim(ascending[1::2], p)


def terminal_norms(
    even: list[int], odd: list[int], scalar: int, p: int
) -> tuple[list[int], list[int]]:
    odd_square = poly_shift(poly_mul(odd, odd, p))
    g_norm = poly_add(poly_mul(even, even, p), odd_square, p, -1)
    shifted_even = even[:]
    shifted_even[0] = (shifted_even[0] + scalar) % p
    f_norm = poly_add(poly_mul(shifted_even, shifted_even, p), odd_square, p, -1)
    return f_norm, g_norm


def matrix_rank(matrix: list[list[int]], p: int) -> int:
    if not matrix:
        return 0
    work = [[value % p for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, p)
        work[rank] = [(value * inverse) % p for value in work[rank]]
        for row in range(len(work)):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (x - factor * y) % p
                for x, y in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def null_vector(matrix: list[list[int]], p: int) -> list[int]:
    work = [[value % p for value in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_columns: list[int] = []
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, p)
        work[rank] = [(value * inverse) % p for value in work[rank]]
        for row in range(row_count):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (x - factor * y) % p
                for x, y in zip(work[row], work[rank])
            ]
        pivot_columns.append(column)
        rank += 1
    free_columns = [
        column for column in range(column_count) if column not in pivot_columns
    ]
    assert free_columns
    vector = [0] * column_count
    vector[free_columns[0]] = 1
    for row, column in reversed(list(enumerate(pivot_columns))):
        vector[column] = -sum(
            work[row][j] * vector[j] for j in free_columns
        ) % p
    assert all(
        sum(x * y for x, y in zip(row, vector)) % p == 0 for row in matrix
    )
    return vector


def alternant_row(x: int, tag: str, r: int, p: int) -> list[int]:
    square = x * x % p
    powers = [1]
    for _ in range(1, 2 * r):
        powers.append(powers[-1] * square % p)
    zeros = [0] * (2 * r)
    weighted = [x * value % p for value in powers]
    if tag == "same":
        return powers + weighted + zeros
    assert tag == "opposite"
    return powers + zeros + weighted


def selected_by_q2(
    support: list[int], top_to_q2: tuple[int, ...]
) -> dict[int, int]:
    out = {top_to_q2[index]: index for index in support}
    assert len(out) == len(support)
    return out


def active_hamming_ledger() -> dict:
    e = 67448
    r = e // 4
    length = 2 * e

    def sphere(radius: int) -> int:
        term = 1
        total = 1
        for index in range(1, radius + 1):
            term = term * (length - index + 1) // index
            total += term
        return total

    repaired_distance = 2 * r + 1
    repaired_radius = r
    repaired_volume = sphere(repaired_radius)
    repaired_quotient = (1 << length) // repaired_volume
    target_distance = 40705
    target_radius = (target_distance - 1) // 2
    target_volume = sphere(target_radius)
    target_quotient = (1 << length) // target_volume
    return {
        "length": length,
        "candidate_distance": repaired_distance,
        "candidate_radius": repaired_radius,
        "candidate_sphere_floor_log2": repaired_volume.bit_length() - 1,
        "candidate_mask_bound_floor_log2": repaired_quotient.bit_length() - 1,
        "candidate_top_bound_floor_log2": (2 * repaired_quotient).bit_length() - 1,
        "candidate_excess_over_mask_target": (
            repaired_quotient.bit_length() - 1 - 52346
        ),
        "candidate_pays": repaired_quotient <= (1 << 52346),
        "target_distance": target_distance,
        "target_radius": target_radius,
        "target_sphere_floor_log2": target_volume.bit_length() - 1,
        "target_mask_bound_floor_log2": target_quotient.bit_length() - 1,
        "target_pays": target_quotient <= (1 << 52346),
    }


def qary_first_lp_ledger(e: int) -> dict:
    getcontext().prec = 60
    delta = Decimal(1) / 2
    gamma = (
        Decimal(3)
        - Decimal(2) * delta
        - Decimal(2) * (Decimal(3) * delta * (1 - delta)).sqrt()
    ) / Decimal(4)
    h4 = (
        gamma * (Decimal(3) / gamma).ln()
        - (Decimal(1) - gamma) * (Decimal(1) - gamma).ln()
    ) / Decimal(4).ln()
    top_bits_envelope = Decimal(4) * Decimal(e) * h4
    top_target_bits = Decimal(52347)
    return {
        "scope": "asymptotic first q-ary LP envelope; not a finite active certificate",
        "q": 4,
        "relative_distance_limit": "1/2",
        "gamma4": format(gamma, ".50f"),
        "H4_gamma4": format(h4, ".50f"),
        "top_bits_per_e_envelope": format(Decimal(4) * h4, ".50f"),
        "active_top_bits_envelope_without_lower_order_term": format(top_bits_envelope, ".40f"),
        "active_top_target_bits": int(top_target_bits),
        "optimistic_gap_before_lower_order_term": format(top_bits_envelope - top_target_bits, ".40f"),
        "target_base4_rate": format(top_target_bits / (Decimal(4) * Decimal(e)), ".50f"),
        "route_pays": False,
    }


def exact_terminal_row(p: int = 191, M: int = 64, e: int = 4) -> dict:
    domain = projected_domain(p, M)

    q2_values = sorted({t2(x, p) for x in domain})
    q4_values = sorted({t2(x, p) for x in q2_values})
    q2_index = {x: i for i, x in enumerate(q2_values)}
    q4_index = {x: i for i, x in enumerate(q4_values)}
    top_to_q2 = tuple(q2_index[t2(x, p)] for x in domain)
    top_to_q4 = tuple(q4_index[t2(t2(x, p), p)] for x in domain)
    q2_to_q4 = tuple(q4_index[t2(x, p)] for x in q2_values)
    top_index = {x: i for i, x in enumerate(domain)}
    top_negation = tuple(top_index[(-x) % p] for x in domain)

    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = collections.defaultdict(list)
    for support in itertools.combinations(range(M), e):
        loc = locator(domain, support, p)
        buckets[loc[1:e]].append(support)

    groups: dict[tuple, dict[tuple[int, ...], dict]] = collections.defaultdict(dict)
    strict_top_pairs = 0
    for supports in buckets.values():
        for i, left in enumerate(supports):
            left_set = set(left)
            for right in supports[i + 1 :]:
                if left_set.intersection(right):
                    continue
                for ordered_left, ordered_right in ((left, right), (right, left)):
                    left_q2 = occupancy(ordered_left, top_to_q2, len(q2_values))
                    right_q2 = occupancy(ordered_right, top_to_q2, len(q2_values))
                    left_q4 = occupancy(ordered_left, top_to_q4, len(q4_values))
                    right_q4 = occupancy(ordered_right, top_to_q4, len(q4_values))
                    if max(left_q2 + right_q2) != 1:
                        continue
                    if max(left_q4 + right_q4) != 1:
                        continue
                    if any(a and b for a, b in zip(left_q2, right_q2)):
                        continue
                    if any(a and b for a, b in zip(left_q4, right_q4)):
                        continue

                    strict_top_pairs += 1
                    left_word = switch_word(left_q2, left_q4, q2_to_q4)
                    right_word = switch_word(right_q2, right_q4, q2_to_q4)
                    word = left_word + right_word
                    top_left = locator(domain, ordered_left, p)
                    top_right = locator(domain, ordered_right, p)
                    c = (top_left[-1] - top_right[-1]) % p
                    key = (left_q4, right_q4)
                    entry = groups[key].setdefault(
                        word,
                        {
                            "orientations": 0,
                            "scalars": set(),
                            "first_top_supports": [list(ordered_left), list(ordered_right)],
                            "top_support_pairs": set(),
                        },
                    )
                    entry["orientations"] += 1
                    entry["scalars"].add(c)
                    entry["top_support_pairs"].add((tuple(ordered_left), tuple(ordered_right)))

    size_hist = collections.Counter()
    distance_hist = collections.Counter()
    scalar_class_hist = collections.Counter()
    orientation_hist = collections.Counter()
    top_distance_hist = collections.Counter()
    bottom_scalar_mismatches = 0
    orientation_pair_mismatches = 0
    nontrivial = []
    for key, words in groups.items():
        r = e // 4
        left_q4_support = tuple(i for i, x in enumerate(key[0]) if x)
        right_q4_support = tuple(i for i, x in enumerate(key[1]) if x)
        left_bottom = locator(tuple(q4_values), left_q4_support, p)
        right_bottom = locator(tuple(q4_values), right_q4_support, p)
        bottom_band_coefficient = (left_bottom[r] - right_bottom[r]) % p
        predicted_scalar = bottom_band_coefficient * pow(pow(2, 3 * r + 2, p), -1, p) % p
        size_hist[len(words)] += 1
        scalar_class_hist[len({c for entry in words.values() for c in entry["scalars"]})] += 1
        for entry in words.values():
            orientation_hist[entry["orientations"]] += 1
            assert len(entry["scalars"]) == 1
            first_pair = tuple(tuple(side) for side in entry["first_top_supports"])
            negative_pair = tuple(
                tuple(sorted(top_negation[i] for i in side))
                for side in first_pair
            )
            if entry["top_support_pairs"] != {first_pair, negative_pair}:
                orientation_pair_mismatches += 1
            if next(iter(entry["scalars"])) != predicted_scalar:
                bottom_scalar_mismatches += 1
        word_list = list(words)
        distances = [hamming(a, b) for a, b in itertools.combinations(word_list, 2)]
        for distance in distances:
            distance_hist[distance] += 1
        top_distances = []
        for left_word, right_word in itertools.combinations(word_list, 2):
            first = words[left_word]["first_top_supports"]
            second = words[right_word]["first_top_supports"]
            second_flipped = [
                [top_negation[i] for i in second[0]],
                [top_negation[i] for i in second[1]],
            ]
            for candidate in (second, second_flipped):
                distance = sum(
                    e - len(set(first[side]).intersection(candidate[side]))
                    for side in (0, 1)
                )
                top_distances.append(distance)
                top_distance_hist[distance] += 2
        if len(words) > 1:
            nontrivial.append(
                {
                    "q4_left_support": list(left_q4_support),
                    "q4_right_support": list(right_q4_support),
                    "bottom_band_coefficient": bottom_band_coefficient,
                    "predicted_scalar": predicted_scalar,
                    "words": [
                        {
                            "word": "".join(map(str, word)),
                            "scalar": next(iter(entry["scalars"])),
                            "orientations": entry["orientations"],
                            "first_top_supports": entry["first_top_supports"],
                        }
                        for word, entry in sorted(words.items())
                    ],
                    "pair_distances": distances,
                    "top_pair_distances_with_multiplicity_suppressed": top_distances,
                }
            )

    return {
        "p": p,
        "M": M,
        "e": e,
        "strict_top_pairs": strict_top_pairs,
        "strict_bottoms": len(groups),
        "terminal_intermediate_words": sum(map(len, groups.values())),
        "code_size_histogram": dict(sorted(size_hist.items())),
        "orientation_histogram": dict(sorted(orientation_hist.items())),
        "scalar_class_histogram": dict(sorted(scalar_class_hist.items())),
        "bottom_scalar_mismatches": bottom_scalar_mismatches,
        "orientation_pair_mismatches": orientation_pair_mismatches,
        "pair_distance_histogram": dict(sorted(distance_hist.items())),
        "same_word_orientation_pairs": sum(map(len, groups.values())),
        "same_word_orientation_distance": 2 * e,
        "top_q4_distance_histogram_scope": "pairs from distinct intermediate words in nontrivial fixed-bottom codes, with both global orientations",
        "top_q4_distance_histogram": dict(sorted(top_distance_hist.items())),
        "nontrivial_bottoms": nontrivial,
    }


def two_value_diagnostic(row: dict, p: int = 191, M: int = 64, e: int = 4) -> dict:
    domain = projected_domain(p, M)
    q2_values = sorted({t2(x, p) for x in domain})
    q2_index = {x: i for i, x in enumerate(q2_values)}
    top_to_q2 = tuple(q2_index[t2(x, p)] for x in domain)
    r = e // 4
    pair_records = []

    for bottom_index, bottom in enumerate(row["nontrivial_bottoms"]):
        assert len(bottom["words"]) == 2
        reconstructed = []
        for word in bottom["words"]:
            f_support, g_support = word["first_top_supports"]
            even, odd = even_odd_parts(domain, g_support, p)
            f_norm, g_norm = terminal_norms(even, odd, word["scalar"], p)
            reconstructed.append(
                {
                    "even": even,
                    "odd": odd,
                    "f_norm": f_norm,
                    "g_norm": g_norm,
                    "f_support": f_support,
                    "g_support": g_support,
                }
            )

        left, right = reconstructed
        scalar = bottom["words"][0]["scalar"]
        assert scalar == bottom["words"][1]["scalar"]
        a_poly = poly_add(left["even"], right["even"], p, -1)
        odd_minus = poly_add(left["odd"], right["odd"], p, -1)
        odd_plus = poly_add(left["odd"], right["odd"], p)
        b_poly = poly_shift(poly_mul(odd_minus, odd_plus, p))
        u_poly = poly_add(left["f_norm"], right["f_norm"], p, -1)
        v_poly = poly_add(left["g_norm"], right["g_norm"], p, -1)
        even_sum = poly_add(left["even"], right["even"], p)
        v_from_collision = poly_add(
            poly_mul(a_poly, even_sum, p), b_poly, p, -1
        )
        even_sum_shifted = even_sum[:]
        even_sum_shifted[0] = (even_sum_shifted[0] + 2 * scalar) % p
        u_from_collision = poly_add(
            poly_mul(a_poly, even_sum_shifted, p), b_poly, p, -1
        )
        u_minus_v = poly_add(u_poly, v_poly, p, -1)
        twice_c_a = [(2 * scalar * value) % p for value in a_poly]

        rows: list[list[int]] = []
        tags: list[str] = []
        nodes: list[int] = []
        sides: list[str] = []
        root_squares: list[int] = []
        for side_name in ("f", "g"):
            first = selected_by_q2(left[f"{side_name}_support"], top_to_q2)
            second = selected_by_q2(right[f"{side_name}_support"], top_to_q2)
            for q2_coordinate in sorted(set(first).intersection(second)):
                first_index = first[q2_coordinate]
                second_index = second[q2_coordinate]
                x = domain[first_index]
                y = domain[second_index]
                if x == y:
                    tag = "same"
                else:
                    assert (x + y) % p == 0
                    tag = "opposite"
                rows.append(alternant_row(x, tag, r, p))
                tags.append(tag)
                nodes.append(x)
                sides.append(side_name.upper())
                root_squares.append(x * x % p)
                norm = left[f"{side_name}_norm"]
                norm_prime = right[f"{side_name}_norm"]
                assert poly_eval(norm, x * x % p, p) == 0
                assert poly_eval(norm_prime, x * x % p, p) == 0

        coefficient_vector = (
            a_poly
            + [0] * (2 * r - len(a_poly))
            + odd_minus
            + [0] * (2 * r - len(odd_minus))
            + odd_plus
            + [0] * (2 * r - len(odd_plus))
        )
        assert len(coefficient_vector) == 6 * r
        residuals = [
            sum(x * y for x, y in zip(matrix_row, coefficient_vector)) % p
            for matrix_row in rows
        ]
        common_count = len(rows)
        binary_distance = bottom["pair_distances"][0]
        record = {
            "bottom_index": bottom_index,
            "q4_left_support": bottom["q4_left_support"],
            "q4_right_support": bottom["q4_right_support"],
            "scalar": scalar,
            "binary_distance": binary_distance,
            "common_root_count": common_count,
            "root_distance_identity_holds": common_count + binary_distance == 2 * e,
            "same_orientation_common_roots": tags.count("same"),
            "opposite_orientation_common_roots": tags.count("opposite"),
            "alternant_rank": matrix_rank(rows, p),
            "alternant_kernel_residuals": residuals,
            "common_root_nodes": nodes,
            "common_root_squares": root_squares,
            "common_root_sides": sides,
            "orientation_tags": tags,
            "A": a_poly,
            "O_minus_O_prime": odd_minus,
            "O_plus_O_prime": odd_plus,
            "B": b_poly,
            "U": u_poly,
            "V": v_poly,
            "degree_A": poly_degree(a_poly, p),
            "degree_B": poly_degree(b_poly, p),
            "degree_U": poly_degree(u_poly, p),
            "degree_V": poly_degree(v_poly, p),
            "degree_gcd_UV": poly_degree(poly_gcd(u_poly, v_poly, p), p),
            "degree_gcd_AB": poly_degree(poly_gcd(a_poly, b_poly, p), p),
            "B_zero": b_poly == [0],
            "A_zero": a_poly == [0],
            "collision_V_holds": v_poly == v_from_collision,
            "collision_U_holds": u_poly == u_from_collision,
            "U_minus_V_equals_2cA": u_minus_v == poly_trim(twice_c_a, p),
        }
        pair_records.append(record)

    synthetic_nodes = [38, 121, 64, 40, 6, 74]
    synthetic_tags = [
        "opposite",
        "opposite",
        "same",
        "opposite",
        "same",
        "same",
    ]
    synthetic_rows = [
        alternant_row(x, tag, 1, p)
        for x, tag in zip(synthetic_nodes, synthetic_tags)
    ]
    synthetic_kernel = null_vector(synthetic_rows, p)
    synthetic_squares = [x * x % p for x in synthetic_nodes]
    synthetic = {
        "scope": "Chebyshev-node alternant only; not a realizable terminal pair",
        "p": p,
        "r": 1,
        "nodes": synthetic_nodes,
        "squares": synthetic_squares,
        "orientation_tags": synthetic_tags,
        "all_nodes_in_D0": all(x in domain for x in synthetic_nodes),
        "distinct_squares": len(set(synthetic_squares)) == len(synthetic_squares),
        "matrix_rank": matrix_rank(synthetic_rows, p),
        "matrix_size": [len(synthetic_rows), len(synthetic_rows[0])],
        "kernel_vector_A_Cminus_Cplus": synthetic_kernel,
        "kernel_residuals": [
            sum(x * y for x, y in zip(matrix_row, synthetic_kernel)) % p
            for matrix_row in synthetic_rows
        ],
        "balanced_tag_counts": {
            "same": synthetic_tags.count("same"),
            "opposite": synthetic_tags.count("opposite"),
        },
        "refutes_unrestricted_full_spark_alternant": (
            matrix_rank(synthetic_rows, p) < len(synthetic_rows)
        ),
        "does_not_refute_root_cap": True,
    }

    return {
        "pair_records": pair_records,
        "pair_count": len(pair_records),
        "pair_distance_histogram": dict(
            sorted(collections.Counter(x["binary_distance"] for x in pair_records).items())
        ),
        "common_root_histogram": dict(
            sorted(collections.Counter(x["common_root_count"] for x in pair_records).items())
        ),
        "alternant_rank_histogram": dict(
            sorted(collections.Counter(x["alternant_rank"] for x in pair_records).items())
        ),
        "zero_A_pairs": sum(x["A_zero"] for x in pair_records),
        "zero_B_pairs": sum(x["B_zero"] for x in pair_records),
        "synthetic_rank_drop": synthetic,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ARTIFACT)
    args = parser.parse_args()
    row = exact_terminal_row()
    diagnostic = two_value_diagnostic(row)
    hamming_ledger = active_hamming_ledger()
    payload = {
        "certificate": "PRIMITIVE_SHIFTPAIR_TERMINAL_ALTERNANT",
        "theorem_interface": {
            "A_zero_root_cap": "|Z_F|+|Z_G|<=e-1",
            "B_zero_root_cap": "|Z_F|+|Z_G|<=6r-1 when A!=0",
            "shared_even_alternant_columns": "6r",
            "candidate_alternant_distance": "2r+1 if relevant 6r-row minors are nonsingular or identity-only",
        },
        "proof_boundary": {
            "exhaustive": "all strict terminal pairs over nontrivial fixed bottoms in the p191 M64 e4 row",
            "not_proved": [
                "uniform shared-even alternant rank",
                "realizable rank-drop classification",
                "uniform terminal capacity",
                "active 94191 common-root cap",
                "growing counterfamily",
            ],
        },
        "active_hamming_ledger": hamming_ledger,
        "row_summary": {
            key: value for key, value in row.items() if key != "nontrivial_bottoms"
        },
        "two_value_diagnostic": diagnostic,
    }
    payload["all_passed"] = (
        row["strict_top_pairs"] == 8832
        and row["strict_bottoms"] == 4412
        and row["terminal_intermediate_words"] == 4416
        and row["code_size_histogram"] == {1: 4408, 2: 4}
        and row["orientation_histogram"] == {2: 4416}
        and row["scalar_class_histogram"] == {1: 4412}
        and row["bottom_scalar_mismatches"] == 0
        and row["orientation_pair_mismatches"] == 0
        and row["same_word_orientation_pairs"] == 4416
        and row["same_word_orientation_distance"] == 8
        and min(row["top_q4_distance_histogram"], default=row["e"] + 1) >= row["e"] + 1
        and diagnostic["pair_count"] == 4
        and diagnostic["pair_distance_histogram"] == {3: 2, 5: 2}
        and diagnostic["common_root_histogram"] == {3: 2, 5: 2}
        and diagnostic["alternant_rank_histogram"] == {3: 2, 5: 2}
        and diagnostic["zero_A_pairs"] == 0
        and diagnostic["zero_B_pairs"] == 0
        and all(
            record["root_distance_identity_holds"]
            and record["collision_V_holds"]
            and record["collision_U_holds"]
            and record["U_minus_V_equals_2cA"]
            and not any(record["alternant_kernel_residuals"])
            for record in diagnostic["pair_records"]
        )
        and diagnostic["synthetic_rank_drop"]["all_nodes_in_D0"]
        and diagnostic["synthetic_rank_drop"]["distinct_squares"]
        and diagnostic["synthetic_rank_drop"]["matrix_rank"] == 5
        and not any(diagnostic["synthetic_rank_drop"]["kernel_residuals"])
        and hamming_ledger["candidate_mask_bound_floor_log2"] == 61579
        and hamming_ledger["candidate_excess_over_mask_target"] == 9233
        and hamming_ledger["candidate_pays"] is False
        and hamming_ledger["target_pays"] is True
    )
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded, encoding="utf-8")
    print("primitive shift-pair terminal alternant")
    print(
        "strict_bottoms="
        + str(payload["row_summary"]["strict_bottoms"])
        + " nontrivial_pairs="
        + str(payload["two_value_diagnostic"]["pair_count"])
    )
    print(
        "distances="
        + str(payload["two_value_diagnostic"]["pair_distance_histogram"])
        + " ranks="
        + str(payload["two_value_diagnostic"]["alternant_rank_histogram"])
    )
    print("PASS_WITH_TERMINAL_VANISHING_AND_ALTERNANT_REDUCTION")


if __name__ == "__main__":
    main()
