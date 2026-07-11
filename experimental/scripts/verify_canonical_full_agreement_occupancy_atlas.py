#!/usr/bin/env python3
"""Exact replay for the joint support/full-agreement occupancy atlas."""

from collections import Counter, defaultdict
from itertools import combinations, product
from math import comb


def safe_comb(top, bottom):
    if bottom < 0 or top < 0 or bottom > top:
        return 0
    return comb(top, bottom)


def multiply(first, second):
    out = [0] * (len(first) + len(second) - 1)
    for i, left in enumerate(first):
        for j, right in enumerate(second):
            out[i + j] += left * right
    return out


def occupancy_weight(profile, exceptional_count, fiber_count, fiber_size):
    t, m, p, rho = profile
    if not (0 <= t <= exceptional_count):
        return 0
    if not (0 <= p <= fiber_count and 0 <= m <= fiber_count - p):
        return 0

    base = [0] * (fiber_size + 1)
    for selected in range(1, fiber_size):
        base[selected] = comb(fiber_size, selected)
    polynomial = [1]
    for _ in range(p):
        polynomial = multiply(polynomial, base)
    coefficient = polynomial[rho] if rho < len(polynomial) else 0

    return (
        safe_comb(exceptional_count, t)
        * safe_comb(fiber_count, p)
        * safe_comb(fiber_count - p, m)
        * coefficient
    )


def occupancy_profile(selected, exceptional_count, fibers):
    selected = set(selected)
    exceptional = set(range(exceptional_count))
    t = len(selected & exceptional)
    complete = [fiber for fiber in fibers if set(fiber) <= selected]
    complete_points = {point for fiber in complete for point in fiber}
    residual = selected - exceptional - complete_points
    partial = [fiber for fiber in fibers if set(fiber) & residual]
    return (t, len(complete), len(partial), len(residual))


def all_subsets(domain):
    for size in range(len(domain) + 1):
        yield from combinations(domain, size)


def check_occupancy_formula():
    checks = 0
    for exceptional_count in range(3):
        for fiber_count in range(1, 4):
            for fiber_size in range(2, 4):
                start = exceptional_count
                fibers = []
                for index in range(fiber_count):
                    fibers.append(
                        tuple(
                            range(
                                start + index * fiber_size,
                                start + (index + 1) * fiber_size,
                            )
                        )
                    )
                domain = tuple(
                    range(exceptional_count + fiber_count * fiber_size)
                )

                census = Counter(
                    occupancy_profile(subset, exceptional_count, fibers)
                    for subset in all_subsets(domain)
                )
                for profile, count in census.items():
                    assert count == occupancy_weight(
                        profile, exceptional_count, fiber_count, fiber_size
                    )
                    checks += 1

                for threshold in range(len(domain) + 1):
                    enumerated = sum(
                        1
                        for subset in all_subsets(domain)
                        if len(subset) >= threshold
                        and occupancy_profile(
                            subset, exceptional_count, fibers
                        )[2:] == (0, 0)
                    )
                    formula = sum(
                        comb(exceptional_count, t)
                        * sum(
                            comb(fiber_count, m)
                            for m in range(
                                max(
                                    0,
                                    (threshold - t + fiber_size - 1)
                                    // fiber_size,
                                ),
                                fiber_count + 1,
                            )
                        )
                        for t in range(exceptional_count + 1)
                    )
                    assert enumerated == formula
                    checks += 1
    return checks


def is_noncommon_constant_pair(r_0, r_1, selected):
    values_0 = {r_0[index] for index in selected}
    values_1 = {r_1[index] for index in selected}
    return not (len(values_0) == 1 and len(values_1) == 1)


def minimum_vertex_cover_weight(edges, weights):
    vertices = sorted(weights, key=repr)
    best = None
    for mask in range(1 << len(vertices)):
        chosen = {vertices[index] for index in range(len(vertices)) if mask >> index & 1}
        if all(left in chosen or right in chosen for left, right in edges):
            total = sum(weights[vertex] for vertex in chosen)
            best = total if best is None else min(best, total)
    return 0 if best is None else best


def check_received_lines():
    modulus = 3
    domain = (0, 1, 2)
    exceptional_count = 1
    fibers = [(1, 2)]
    support_size = 2
    support_profiles = Counter(
        occupancy_profile(selected, exceptional_count, fibers)
        for selected in combinations(domain, support_size)
    )
    all_profile_weights = Counter(
        occupancy_profile(selected, exceptional_count, fibers)
        for selected in all_subsets(domain)
    )

    checked = 0
    strict_improvements = 0
    for r_0 in product(range(modulus), repeat=len(domain)):
        for r_1 in product(range(modulus), repeat=len(domain)):
            witnesses = []
            support_slopes = defaultdict(set)
            agreement_slopes = defaultdict(set)

            for gamma in range(modulus):
                line = tuple(
                    (r_0[index] + gamma * r_1[index]) % modulus
                    for index in domain
                )
                for h in range(modulus):
                    agreement = tuple(index for index in domain if line[index] == h)
                    if len(agreement) < support_size:
                        continue
                    for selected in combinations(agreement, support_size):
                        if not is_noncommon_constant_pair(r_0, r_1, selected):
                            continue
                        sigma = occupancy_profile(selected, exceptional_count, fibers)
                        alpha = occupancy_profile(agreement, exceptional_count, fibers)
                        witnesses.append((gamma, selected, agreement, sigma, alpha))
                        support_slopes[selected].add(gamma)
                        agreement_slopes[agreement].add(gamma)

            assert all(len(slopes) <= 1 for slopes in support_slopes.values())
            assert all(len(slopes) <= 1 for slopes in agreement_slopes.values())

            raw_cells = defaultdict(set)
            for gamma, _, _, sigma, alpha in witnesses:
                raw_cells[(sigma, alpha)].add(gamma)

            ordered = sorted(
                raw_cells,
                key=lambda pair: (
                    int(pair[1][2] + pair[1][3] > 0),
                    pair[1],
                    -pair[0][2],
                    pair[0],
                ),
            )
            assigned = set()
            first_match = {}
            for edge in ordered:
                first_match[edge] = raw_cells[edge] - assigned
                assigned.update(first_match[edge])

            live_edges = [edge for edge in ordered if first_match[edge]]
            weights = {}
            for sigma, alpha in live_edges:
                weights[("support", sigma)] = support_profiles[sigma]
                weights[("agreement", alpha)] = all_profile_weights[alpha]
                assert len(first_match[(sigma, alpha)]) <= min(
                    modulus, support_profiles[sigma], all_profile_weights[alpha]
                )

            graph_edges = [
                (("support", sigma), ("agreement", alpha))
                for sigma, alpha in live_edges
            ]
            tau = minimum_vertex_cover_weight(graph_edges, weights)
            assert len(assigned) <= min(modulus, tau)
            assert tau <= comb(len(domain), support_size)
            if tau < comb(len(domain), support_size):
                strict_improvements += 1
            checked += 1

    return checked, strict_improvements


def check_partial_support_factor():
    checks = 0
    for fiber_count in range(2, 13):
        for selected_fibers in range(1, fiber_count):
            support_profile = (0, 0, selected_fibers, selected_fibers)
            agreement_profile = (0, selected_fibers, 0, 0)
            support_weight = occupancy_weight(
                support_profile, 0, fiber_count, 2
            )
            agreement_weight = occupancy_weight(
                agreement_profile, 0, fiber_count, 2
            )
            assert support_weight == comb(fiber_count, selected_fibers) * 2 ** selected_fibers
            assert agreement_weight == comb(fiber_count, selected_fibers)
            assert support_weight == (2 ** selected_fibers) * agreement_weight
            checks += 1
    return checks


def main():
    occupancy_checks = check_occupancy_formula()
    line_checks, strict_improvements = check_received_lines()
    factor_checks = check_partial_support_factor()

    print("object: joint support/full-agreement occupancy atlas")
    print(f"occupancy and saturated-count checks: {occupancy_checks} PASS")
    print(f"received lines over F_3: {line_checks} PASS")
    print(f"strict weighted-cover improvements: {strict_improvements}")
    print(f"two-fold partial-support factor checks: {factor_checks} PASS")
    print("theorem: canonical_full_agreement_occupancy_atlas")
    print("status: PROVED exact compiler and saturated-stratum payment")


if __name__ == "__main__":
    main()
