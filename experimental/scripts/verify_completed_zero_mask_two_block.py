#!/usr/bin/env python3
"""Exact checks for completed_zero_mask_two_block.md.

Usage:
    python3 verify_completed_zero_mask_two_block.py --check
    python3 verify_completed_zero_mask_two_block.py --tamper-selftest

The checker is deterministic and standard-library only. It performs no file,
network, or subprocess operations.
"""

import random
import sys
from collections import defaultdict
from itertools import chain, combinations, product


EXPECTED_MASK_CASES = 43
EXPECTED_MASK_ATTAINED = 1
EXPECTED_EXACT_WEIGHTS = 5_762_500
EXPECTED_W1_WEIGHTS = 2_818_750
EXPECTED_W2_WEIGHTS = 2_943_750
EXPECTED_XI_ZERO = 1_000
RANDOM_SEED = 20260712


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def vector_add(first, second, modulus):
    return tuple((x + y) % modulus for x, y in zip(first, second))


def vector_subtract(first, second, modulus):
    return tuple((x - y) % modulus for x, y in zip(first, second))


def vector_scale(scalar, vector, modulus):
    return tuple(scalar * value % modulus for value in vector)


def weight(vector):
    return sum(value != 0 for value in vector)


def support_mask(vector):
    mask = 0
    for index, value in enumerate(vector):
        if value:
            mask |= 1 << index
    return mask


def masks_of_size(length, size):
    for selected in combinations(range(length), size):
        mask = 0
        for index in selected:
            mask |= 1 << index
        yield mask


def xi_value(m_length, direction_weight, exact_weight, height):
    return (
        direction_weight * (m_length - exact_weight) ** 2
        + m_length * height**2
        - direction_weight * m_length**2
    )


def theorem_bound(m_length, direction_weight, xi):
    ambient_length = m_length + direction_weight
    if xi > 0:
        return ambient_length - 1
    if xi == 0:
        return 2 * (ambient_length - 2)
    return None


def endpoint_bound(m_length, direction_weight, exact_weight, height, xi):
    if exact_weight == 0:
        return direction_weight // height
    if exact_weight == m_length and xi >= 0:
        return 2 * direction_weight - 1
    return None


def maximum_clique_size(adjacency):
    """Exact bitset branch-and-bound with greedy coloring."""

    best = 0

    def color_sort(candidates):
        order = []
        colors = []
        color = 0
        remaining = candidates
        while remaining:
            color += 1
            available = remaining
            while available:
                bit = available & -available
                vertex = bit.bit_length() - 1
                remaining &= ~bit
                available &= ~bit
                available &= ~adjacency[vertex]
                order.append(vertex)
                colors.append(color)
        return order, colors

    def expand(candidates, size):
        nonlocal best
        if not candidates:
            best = max(best, size)
            return

        order, colors = color_sort(candidates)
        for index in range(len(order) - 1, -1, -1):
            if size + colors[index] <= best:
                return
            vertex = order[index]
            bit = 1 << vertex
            expand(candidates & adjacency[vertex], size + 1)
            candidates &= ~bit

    expand((1 << len(adjacency)) - 1, 0)
    return best


def two_block_case(m_length, direction_weight, exact_weight, height):
    outside_size = m_length - exact_weight
    candidates = [
        (outside, inside)
        for outside in masks_of_size(m_length, outside_size)
        for inside_size in range(height, direction_weight + 1)
        for inside in masks_of_size(direction_weight, inside_size)
    ]

    adjacency = [0] * len(candidates)
    for first_index, (first_x, first_y) in enumerate(candidates):
        for second_index in range(first_index):
            second_x, second_y = candidates[second_index]
            common = (first_x & second_x).bit_count()
            common += (first_y & second_y).bit_count()
            if common <= m_length:
                adjacency[first_index] |= 1 << second_index
                adjacency[second_index] |= 1 << first_index

    xi = xi_value(m_length, direction_weight, exact_weight, height)
    bound = theorem_bound(m_length, direction_weight, xi)
    observed = maximum_clique_size(adjacency)
    return {
        "M": m_length,
        "d": direction_weight,
        "e": exact_weight,
        "h": height,
        "Xi": xi,
        "vertices": len(candidates),
        "maximum": observed,
        "bound": bound,
    }


def exhaustive_two_block_checks():
    cases = 0
    equality_cases = 0
    attained = 0
    maximum_vertices = 0

    for m_length in range(2, 6):
        for direction_weight in range(2, 6):
            for exact_weight in range(1, m_length):
                for height in range(1, direction_weight + 1):
                    xi = xi_value(
                        m_length, direction_weight, exact_weight, height
                    )
                    if xi < 0:
                        continue
                    row = two_block_case(
                        m_length, direction_weight, exact_weight, height
                    )
                    require(row["bound"] is not None, "paid case lost its bound")
                    require(
                        row["maximum"] <= row["bound"],
                        f"two-block bound failed: {row}",
                    )
                    cases += 1
                    equality_cases += xi == 0
                    attained += row["maximum"] == row["bound"]
                    maximum_vertices = max(maximum_vertices, row["vertices"])

    require(cases == EXPECTED_MASK_CASES, "two-block case count changed")
    require(attained == EXPECTED_MASK_ATTAINED, "attained-case count changed")
    return {
        "cases": cases,
        "Xi=0": equality_cases,
        "attained": attained,
        "max_vertices": maximum_vertices,
    }


def exhaustive_endpoint_checks():
    cases = 0
    attained = 0
    maximum_vertices = 0
    for m_length in range(1, 6):
        for direction_weight in range(1, 6):
            for exact_weight in (0, m_length):
                for height in range(1, direction_weight + 1):
                    xi = xi_value(
                        m_length, direction_weight, exact_weight, height
                    )
                    bound = endpoint_bound(
                        m_length,
                        direction_weight,
                        exact_weight,
                        height,
                        xi,
                    )
                    if bound is None:
                        continue
                    row = two_block_case(
                        m_length, direction_weight, exact_weight, height
                    )
                    require(
                        row["maximum"] <= bound,
                        f"endpoint bound failed: {row}, endpoint={bound}",
                    )
                    cases += 1
                    attained += row["maximum"] == bound
                    maximum_vertices = max(maximum_vertices, row["vertices"])
    require(cases > 0, "endpoint suite found no paid cases")
    require(attained > 0, "endpoint suite found no sharp case")
    return {
        "cases": cases,
        "attained": attained,
        "max_vertices": maximum_vertices,
    }


def explicit_family_row(r_value, exact_weight):
    length = 500 * r_value
    redundancy = 275 * r_value
    kappa = 225 * r_value
    radius = 150 * r_value
    direction_weight = 250 * r_value
    m_length = 250 * r_value
    punctured_distance = 25 * r_value + 1
    q_value = 2 * exact_weight - 50 * r_value
    height = 100 * r_value + exact_weight

    require(length == redundancy + kappa, "family dimension mismatch")
    require(m_length == length - direction_weight, "family puncture mismatch")
    require(
        punctured_distance == redundancy + 1 - direction_weight,
        "family punctured distance mismatch",
    )

    if q_value <= punctured_distance:
        branch = "W1-"
        old_denominator = (
            exact_weight**2
            - 2 * m_length * exact_weight
            + m_length * punctured_distance
        )
    else:
        require(q_value < m_length, "selected family weight entered W3+")
        branch = "W2-"
        old_denominator = (
            exact_weight**2
            - m_length * (2 * radius - direction_weight)
        )

    xi = xi_value(m_length, direction_weight, exact_weight, height)
    factorized = (
        500
        * r_value
        * (exact_weight - 50 * r_value)
        * (exact_weight - 100 * r_value)
    )
    require(xi == factorized, "Xi factorization failed")
    return {
        "branch": branch,
        "old_denominator": old_denominator,
        "Xi": xi,
        "q": q_value,
        "Delta": punctured_distance,
    }


def explicit_family_checks(maximum_r=500):
    checked = 0
    branch_counts = {"W1-": 0, "W2-": 0}
    equality_count = 0

    for r_value in range(1, maximum_r + 1):
        require(
            (500 * r_value - 150 * r_value) ** 2
            < 500 * r_value * 250 * r_value,
            "high-direction route unexpectedly paid",
        )
        require(
            (25 * r_value + 1) * 250 * r_value
            - 2 * 150 * r_value * 250 * r_value
            + (150 * r_value) ** 2
            < 0,
            "punctured-Johnson route unexpectedly paid",
        )
        require(3 * 150 * r_value > 275 * r_value, "deep route unexpectedly paid")

        weights = chain(
            range(15 * r_value, 50 * r_value + 1),
            range(100 * r_value, 111 * r_value + 1),
        )
        for exact_weight in weights:
            row = explicit_family_row(r_value, exact_weight)
            require(row["old_denominator"] < 0, "selected stratum is not strict")
            require(row["Xi"] >= 0, "selected stratum is not two-block paid")
            branch_counts[row["branch"]] += 1
            equality_count += row["Xi"] == 0
            checked += 1

            if exact_weight <= 25 * r_value:
                require(
                    250 * r_value >= 2 * (100 * r_value + exact_weight),
                    "Cramer prefactor lower bound failed",
                )
                require(
                    250 * r_value - (exact_weight - 1)
                    >= 10 * (25 * r_value - (exact_weight - 1)),
                    "Cramer product lower bound failed",
                )
            else:
                require(
                    250 * r_value > 2 * exact_weight,
                    "Cramer binomial lower bound failed",
                )

        direct_budget = (
            46 * r_value * (500 * r_value - 1)
            + 2 * (1000 * r_value - 4)
        )
        require(
            direct_budget == 23000 * r_value**2 + 1954 * r_value - 8,
            "explicit direct budget identity failed",
        )

    require(checked == EXPECTED_EXACT_WEIGHTS, "exact-weight count changed")
    require(
        branch_counts["W1-"] == EXPECTED_W1_WEIGHTS,
        "W1- count changed",
    )
    require(
        branch_counts["W2-"] == EXPECTED_W2_WEIGHTS,
        "W2- count changed",
    )
    require(equality_count == EXPECTED_XI_ZERO, "Xi equality count changed")
    return {
        "exact_weight_checks": checked,
        "W1-": branch_counts["W1-"],
        "W2-": branch_counts["W2-"],
        "Xi=0": equality_count,
    }


def boundary_falsifier_checks():
    checked = 0
    for r_value in (1, 2, 10, 100, 500):
        low = explicit_family_row(r_value, 50 * r_value + 1)
        high = explicit_family_row(r_value, 100 * r_value - 1)
        require(low["Xi"] < 0, "lower equality-limit falsifier was paid")
        require(high["Xi"] < 0, "upper equality-limit falsifier was paid")
        checked += 2

    false_case = two_block_case(2, 2, 1, 1)
    require(false_case["maximum"] == 6, "weakened-threshold witness changed")
    false_bound = 2 * ((2 + 2) - 2)
    require(
        false_case["maximum"] > false_bound,
        "weakened common-zero threshold was not falsified",
    )
    return {
        "equality_limit_sequences_rejected": checked,
        "weakened_threshold_observed": false_case["maximum"],
        "weakened_threshold_false_bound": false_bound,
    }


def matrix_rank(rows, modulus):
    if not rows:
        return 0
    work = [list(row) for row in rows]
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column] % modulus
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, modulus)
        work[pivot_row] = [value * inverse % modulus for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (value - factor * pivot_value) % modulus
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def weighted_rs_columns(modulus, points, redundancy, weights):
    require(len(points) == len(set(points)), "evaluation points are not distinct")
    require(all(weight_value % modulus for weight_value in weights), "zero weight")
    columns = [
        tuple(
            weights[index] * pow(point, degree, modulus) % modulus
            for degree in range(redundancy)
        )
        for index, point in enumerate(points)
    ]
    require(matrix_rank(columns, modulus) == redundancy, "parity map lost rank")
    return columns


def syndrome(word, columns, modulus):
    return tuple(
        sum(word[index] * columns[index][degree] for index in range(len(word)))
        % modulus
        for degree in range(len(columns[0]))
    )


def support_span(mask, columns, modulus):
    selected = [index for index in range(len(columns)) if mask & (1 << index)]
    values = set()
    for coefficients in product(range(modulus), repeat=len(selected)):
        word = [0] * len(columns)
        for index, coefficient in zip(selected, coefficients):
            word[index] = coefficient
        values.add(syndrome(tuple(word), columns, modulus))
    return values


def build_chart(modulus, points, redundancy, radius, weights):
    length = len(points)
    columns = weighted_rs_columns(modulus, points, redundancy, weights)
    zero = (0,) * redundancy
    minimum_lifts = {}
    low_witnesses = defaultdict(dict)
    kernel_distance = None

    for word in product(range(modulus), repeat=length):
        target = syndrome(word, columns, modulus)
        word_weight = weight(word)
        key = (word_weight, word)
        if target not in minimum_lifts or key < minimum_lifts[target]:
            minimum_lifts[target] = key
        if target == zero and word_weight:
            kernel_distance = (
                word_weight
                if kernel_distance is None
                else min(kernel_distance, word_weight)
            )
        if word_weight <= radius:
            mask = support_mask(word)
            old = low_witnesses[target].get(mask)
            if old is None or word < old:
                low_witnesses[target][mask] = word

    require(
        len(minimum_lifts) == modulus**redundancy,
        "parity map did not cover its syndrome space",
    )
    require(kernel_distance == redundancy + 1, "weighted-RS kernel lost MDS distance")

    spans = {
        mask: support_span(mask, columns, modulus)
        for mask in range(1 << length)
    }
    syndromes = list(product(range(modulus), repeat=redundancy))
    return {
        "p": modulus,
        "N": length,
        "R": redundancy,
        "t": radius,
        "columns": columns,
        "minimum_lifts": minimum_lifts,
        "low_witnesses": low_witnesses,
        "spans": spans,
        "syndromes": syndromes,
    }


def select_completed_records(chart, y_0, y_1):
    modulus = chart["p"]
    records = []
    for gamma in range(modulus):
        target = vector_add(y_0, vector_scale(gamma, y_1, modulus), modulus)
        candidates = chart["low_witnesses"].get(target, {})
        for mask in sorted(candidates, key=lambda item: (item.bit_count(), item)):
            if y_0 in chart["spans"][mask] and y_1 in chart["spans"][mask]:
                continue
            witness = candidates[mask]
            require(
                syndrome(witness, chart["columns"], modulus) == target,
                "selected witness has wrong syndrome",
            )
            records.append(
                {"gamma": gamma, "witness": witness, "support": mask}
            )
            break
    return records


def validate_record_group(chart, y_1, direction_lift, records, exact_weight):
    modulus = chart["p"]
    length = chart["N"]
    radius = chart["t"]
    direction_weight = weight(direction_lift)
    j_mask = support_mask(direction_lift)
    full_mask = (1 << length) - 1
    outside_mask = full_mask ^ j_mask
    m_length = length - direction_weight
    height = max(1, direction_weight + exact_weight - radius)
    decorated = []

    for record in records:
        witness = record["witness"]
        support = record["support"]
        require(weight(witness) <= radius, "selected witness exceeds radius")
        require(
            (support & outside_mask).bit_count() == exact_weight,
            "selected witness has wrong punctured weight",
        )
        zero_mask = full_mask ^ support
        x_mask = zero_mask & outside_mask
        y_mask = zero_mask & j_mask
        require(x_mask.bit_count() == m_length - exact_weight, "wrong X size")
        require(y_mask.bit_count() >= height, "transversality zero height failed")
        decorated.append((record, x_mask, y_mask))

    for first_index, (first, first_x, first_y) in enumerate(decorated):
        for second, second_x, second_y in decorated[:first_index]:
            slope_delta = (first["gamma"] - second["gamma"]) % modulus
            require(slope_delta, "duplicate slope in completed stratum")
            normalized = vector_scale(
                pow(slope_delta, -1, modulus),
                vector_subtract(first["witness"], second["witness"], modulus),
                modulus,
            )
            require(
                syndrome(normalized, chart["columns"], modulus) == y_1,
                "normalized witness difference is not a direction lift",
            )
            require(
                weight(normalized) >= direction_weight,
                "minimum direction distance was violated",
            )
            common = (first_x & second_x).bit_count()
            common += (first_y & second_y).bit_count()
            require(common <= m_length, "two-block common-zero cap failed")

    xi = xi_value(m_length, direction_weight, exact_weight, height)
    if exact_weight in (0, m_length):
        bound = endpoint_bound(
            m_length, direction_weight, exact_weight, height, xi
        )
        if exact_weight == m_length:
            full_inside = [
                record
                for record, _x_mask, y_mask in decorated
                if y_mask == j_mask
            ]
            require(
                len(full_inside) <= 1,
                "two full-J endpoint masks violate transversality",
            )
    else:
        bound = theorem_bound(m_length, direction_weight, xi)
    if bound is not None:
        require(len(records) <= bound, "completed-witness theorem bound failed")
    return xi, bound


def audit_line(chart, y_0, y_1):
    require(any(y_1), "direction syndrome must be nonzero")
    direction_lift = chart["minimum_lifts"][y_1][1]
    direction_weight = weight(direction_lift)
    m_length = chart["N"] - direction_weight
    records = select_completed_records(chart, y_0, y_1)
    groups = defaultdict(list)

    j_mask = support_mask(direction_lift)
    outside_mask = ((1 << chart["N"]) - 1) ^ j_mask
    for record in records:
        exact_weight = (record["support"] & outside_mask).bit_count()
        if 0 <= exact_weight <= m_length:
            groups[exact_weight].append(record)

    stats = {
        "retained_slopes": len(records),
        "interior_strata": 0,
        "paid_strata": 0,
        "endpoint_strata": 0,
        "paid_endpoint_strata": 0,
        "Xi=0_strata": 0,
        "deletion_checks": 0,
    }
    for exact_weight, group in groups.items():
        xi, bound = validate_record_group(
            chart, y_1, direction_lift, group, exact_weight
        )
        stats["interior_strata"] += 1
        stats["paid_strata"] += bound is not None
        stats["endpoint_strata"] += exact_weight in (0, m_length)
        stats["paid_endpoint_strata"] += (
            exact_weight in (0, m_length) and bound is not None
        )
        stats["Xi=0_strata"] += xi == 0

        for subset in (group[::2], group[1::2]):
            if subset and len(subset) < len(group):
                validate_record_group(
                    chart, y_1, direction_lift, subset, exact_weight
                )
                stats["deletion_checks"] += 1
    return stats


def add_stats(total, update):
    for key, value in update.items():
        total[key] = total.get(key, 0) + value


def finite_geometry_checks():
    totals = {
        "exhaustive_lines": 0,
        "random_lines": 0,
        "retained_slopes": 0,
        "interior_strata": 0,
        "paid_strata": 0,
        "endpoint_strata": 0,
        "paid_endpoint_strata": 0,
        "Xi=0_strata": 0,
        "deletion_checks": 0,
    }

    exhaustive_chart = build_chart(
        modulus=5,
        points=(0, 1, 2, 3, 4),
        redundancy=3,
        radius=2,
        weights=(1, 2, 3, 4, 1),
    )
    zero = (0,) * exhaustive_chart["R"]
    for y_1 in exhaustive_chart["syndromes"]:
        if y_1 == zero:
            continue
        for y_0 in exhaustive_chart["syndromes"]:
            add_stats(totals, audit_line(exhaustive_chart, y_0, y_1))
            totals["exhaustive_lines"] += 1

    rng = random.Random(RANDOM_SEED)
    for chart_index, radius in enumerate((2, 3, 2)):
        points = tuple(rng.sample(range(7), 6))
        weights = tuple(rng.randrange(1, 7) for _ in range(6))
        chart = build_chart(
            modulus=7,
            points=points,
            redundancy=4,
            radius=radius,
            weights=weights,
        )
        for _ in range(400):
            y_0 = tuple(rng.randrange(7) for _ in range(4))
            y_1 = (0, 0, 0, 0)
            while not any(y_1):
                y_1 = tuple(rng.randrange(7) for _ in range(4))
            add_stats(totals, audit_line(chart, y_0, y_1))
            totals["random_lines"] += 1

        require(chart_index < 3, "random chart index drifted")

    require(totals["exhaustive_lines"] == 15_500, "exhaustive line count changed")
    require(totals["random_lines"] == 1_200, "random line count changed")
    require(totals["paid_strata"] > 0, "finite geometry hit no paid stratum")
    require(totals["deletion_checks"] > 0, "first-match deletion was not exercised")
    return totals


def expect_failure(label, action):
    try:
        action()
    except AssertionError:
        return label
    raise AssertionError(f"tamper was accepted: {label}")


def validate_family_claim(r_value, exact_weight, claimed_xi, claimed_branch):
    row = explicit_family_row(r_value, exact_weight)
    require(row["Xi"] == claimed_xi, "claimed Xi does not match exact Xi")
    require(row["branch"] == claimed_branch, "claimed strict branch is wrong")


def require_paid_family_weight(r_value, exact_weight):
    row = explicit_family_row(r_value, exact_weight)
    require(row["Xi"] >= 0, "weight is outside the exact Xi-paid region")


def validate_mask_threshold(family, threshold):
    for first_index, (first_x, first_y) in enumerate(family):
        for second_x, second_y in family[:first_index]:
            common = (first_x & second_x).bit_count()
            common += (first_y & second_y).bit_count()
            require(common <= threshold, "claimed common-zero threshold is false")


def tamper_selftest():
    caught = []
    base = explicit_family_row(10, 150)
    caught.append(
        expect_failure(
            "Xi mutation",
            lambda: validate_family_claim(10, 150, base["Xi"] + 1, base["branch"]),
        )
    )
    caught.append(
        expect_failure(
            "strict-branch mutation",
            lambda: validate_family_claim(10, 150, base["Xi"], "W2-"),
        )
    )
    caught.append(
        expect_failure(
            "lower equality-limit promoted",
            lambda: require_paid_family_weight(10, 501),
        )
    )
    caught.append(
        expect_failure(
            "upper equality-limit promoted",
            lambda: require_paid_family_weight(10, 999),
        )
    )

    false_family = [
        (outside, inside)
        for outside in masks_of_size(2, 1)
        for inside_size in (1, 2)
        for inside in masks_of_size(2, inside_size)
    ]
    caught.append(
        expect_failure(
            "M-1 common-zero threshold",
            lambda: validate_mask_threshold(false_family, 1),
        )
    )

    attained = two_block_case(4, 5, 1, 3)
    caught.append(
        expect_failure(
            "sharp bound reduced by one",
            lambda: require(
                attained["maximum"] <= attained["bound"] - 1,
                "mutated sharp bound rejected",
            ),
        )
    )

    endpoint = two_block_case(2, 4, 0, 2)
    endpoint_bound_value = endpoint_bound(2, 4, 0, 2, endpoint["Xi"])
    require(endpoint["maximum"] == endpoint_bound_value, "endpoint witness drifted")
    caught.append(
        expect_failure(
            "e=0 endpoint bound reduced by one",
            lambda: require(
                endpoint["maximum"] <= endpoint_bound_value - 1,
                "mutated endpoint bound rejected",
            ),
        )
    )

    require(len(caught) == 7, "tamper suite size changed")
    print(f"tamper-selftest: PASS ({len(caught)}/{len(caught)} mutations rejected)")
    return 0


def run_check():
    mask_stats = exhaustive_two_block_checks()
    endpoint_stats = exhaustive_endpoint_checks()
    family_stats = explicit_family_checks()
    geometry_stats = finite_geometry_checks()
    falsifier_stats = boundary_falsifier_checks()

    print(f"two-block set-system exhaustive: PASS {mask_stats}")
    print(f"endpoint set-system exhaustive: PASS {endpoint_stats}")
    print(f"strict linear family: PASS {family_stats}")
    print(f"weighted-RS completed geometry: PASS {geometry_stats}")
    print(f"deliberate falsifiers: REJECTED {falsifier_stats}")
    print("RESULT: PASS")
    return 0


def main(argv):
    if argv == ["--tamper-selftest"]:
        return tamper_selftest()
    if argv in ([], ["--check"]):
        return run_check()
    print("usage: verify_completed_zero_mask_two_block.py [--check|--tamper-selftest]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
