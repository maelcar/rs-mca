#!/usr/bin/env python3
"""Exact stdlib verifier for the Role-03 d=4828 route cut.

It proves the finite part of the theorem by exhaustive enumeration:
  (i) the inherited v=10 determinant-square obstruction;
  (ii) every residual weighted-clique skeleton of cost chi=6;
  (iii) the 6 K7 skeleton's 675 determinant-square survivors, all of which
        fail the 7-adic Hasse invariant forced by B B^T.
It then replays the sharpened parameter/pencil arithmetic.

No third-party package and no assert statement is used.  Normal and -O runs
therefore have identical semantics.
"""

from fractions import Fraction
from itertools import combinations, permutations, product
from math import isqrt

M = 218
D = 4828
N = 1_053_556
A_REQ = 72_451
BUDGET = 1_658
R_MAX = 151


def fail(message):
    raise SystemExit("FAIL: " + message)


def bareiss_det(matrix):
    a = [list(map(int, row)) for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = None
            for i in range(k + 1, n):
                if a[i][k] != 0:
                    pivot = i
                    break
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        pivot_value = a[k][k]
        for i in range(k + 1, n):
            aik = a[i][k]
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot_value - aik * a[k][j]
                if numerator % previous != 0:
                    fail("nonexact Bareiss division")
                a[i][j] = numerator // previous
        previous = pivot_value
        for i in range(k + 1, n):
            a[i][k] = 0
        for j in range(k + 1, n):
            a[k][j] = 0
    return sign * a[-1][-1]


def is_square(value):
    if value < 0:
        return False
    root = isqrt(value)
    return root * root == value


def factor_integer(value):
    n = abs(value)
    factors = {}
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            n //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def format_factorization(factors):
    pieces = []
    for prime in sorted(factors):
        exponent = factors[prime]
        pieces.append(str(prime) if exponent == 1 else f"{prime}^{exponent}")
    return " * ".join(pieces) if pieces else "1"


def zero_matrix(n):
    return [[0] * n for _ in range(n)]


def add_edge(adjacency, u, v):
    if u == v or adjacency[u][v] != 0:
        fail(f"invalid edge {u},{v}")
    adjacency[u][v] = 1
    adjacency[v][u] = 1


def add_clique(adjacency, vertices):
    for u, v in combinations(vertices, 2):
        add_edge(adjacency, u, v)


def check_regular(adjacency, degree=7):
    degrees = [sum(row) for row in adjacency]
    if degrees != [degree] * len(adjacency):
        fail(f"degree sequence mismatch: {degrees}")


def shifted_matrix(adjacency, shift=14):
    n = len(adjacency)
    return [
        [(shift if i == j else 0) - adjacency[i][j] for j in range(n)]
        for i in range(n)
    ]


def cycle_adjacency(partition):
    n = sum(partition)
    adjacency = zero_matrix(n)
    start = 0
    for length in partition:
        vertices = list(range(start, start + length))
        for i, u in enumerate(vertices):
            v = vertices[(i + 1) % length]
            add_edge(adjacency, u, v)
        start += length
    return adjacency


def graph_complement(adjacency):
    n = len(adjacency)
    return [
        [0 if i == j else 1 - adjacency[i][j] for j in range(n)]
        for i in range(n)
    ]


def verify_v10_obstruction():
    partitions = [(10,), (7, 3), (6, 4), (5, 5), (4, 3, 3)]
    expected = [
        {7: 1, 11: 2, 13: 1, 19: 2, 239: 2},
        {2: 2, 7: 3, 17: 1, 3121: 2},
        {2: 10, 3: 2, 5: 2, 7: 3, 13: 2, 17: 1},
        {7: 1, 11: 4, 17: 1, 19: 4},
        {2: 4, 3: 2, 5: 2, 7: 5, 13: 1, 17: 2},
    ]
    prefactor = 225 * (7 ** 25) * (15 ** 182)
    output = []
    for partition, wanted in zip(partitions, expected):
        residual = graph_complement(cycle_adjacency(partition))
        check_regular(residual)
        determinant = bareiss_det(shifted_matrix(residual))
        factors = factor_integer(determinant)
        if factors != wanted:
            fail(f"v=10 factor mismatch at {partition}: {factors}")
        if is_square(prefactor * determinant):
            fail(f"v=10 square survived at {partition}")
        output.append((partition, format_factorization(factors)))
    return output


def clique_cost_skeletons(cost):
    rows = []
    for c in range(28):
        v = M - 8 * c
        if v < 18:
            continue
        for k7 in range(v // 7 + 1):
            for k6 in range((v - 7 * k7) // 6 + 1):
                for k5 in range((v - 7 * k7 - 6 * k6) // 5 + 1):
                    u = v - 7 * k7 - 6 * k6 - 5 * k5
                    chi = k7 + 2 * k6 + 3 * k5 + u
                    if chi == cost:
                        rows.append((v, c, k7, k6, k5, u))
    rows.sort()
    return rows


def canonical_cycle_word(word):
    word = tuple(word)
    n = len(word)
    candidates = []
    for base in (word, tuple(reversed(word))):
        for shift in range(n):
            candidates.append(base[shift:] + base[:shift])
    return min(candidates)


def enumerate_A1():
    # Three K6 blocks.  The external graph is a 2-regular properly 3-colored
    # graph, hence a multiset of colored cycles.
    cycle_types = []
    for length in range(3, 19):
        seen = set()

        def extend(prefix):
            if len(prefix) == length:
                if prefix[-1] != prefix[0]:
                    seen.add(canonical_cycle_word(prefix))
                return
            for color in range(3):
                if prefix and color == prefix[-1]:
                    continue
                extend(prefix + [color])

        extend([])
        for word in sorted(seen):
            counts = tuple(word.count(color) for color in range(3))
            if all(value <= 6 for value in counts):
                cycle_types.append((length, word, counts))
    cycle_types.sort(key=lambda item: (item[0], item[1]))

    solutions = []

    def choose(start, remaining_counts, remaining_length, chosen):
        if remaining_length == 0:
            if remaining_counts == (0, 0, 0):
                solutions.append(tuple(chosen))
            return
        for index in range(start, len(cycle_types)):
            length, _, counts = cycle_types[index]
            if length > remaining_length:
                break
            if all(counts[i] <= remaining_counts[i] for i in range(3)):
                choose(
                    index,
                    tuple(remaining_counts[i] - counts[i] for i in range(3)),
                    remaining_length - length,
                    chosen + [index],
                )

    choose(0, (6, 6, 6), 18, [])
    if len(solutions) != 3311:
        fail(f"A1 type count {len(solutions)} != 3311")

    prefactor = 225 * (7 ** 24) * (15 ** 175)
    square_survivors = 0
    for chosen in solutions:
        adjacency = zero_matrix(18)
        groups = [list(range(0, 6)), list(range(6, 12)), list(range(12, 18))]
        for group in groups:
            add_clique(adjacency, group)
        next_vertex = [0, 0, 0]
        for index in chosen:
            word = cycle_types[index][1]
            vertices = []
            for color in word:
                vertex = groups[color][next_vertex[color]]
                next_vertex[color] += 1
                vertices.append(vertex)
            for i, u in enumerate(vertices):
                add_edge(adjacency, u, vertices[(i + 1) % len(vertices)])
        if next_vertex != [6, 6, 6]:
            fail("A1 color use mismatch")
        check_regular(adjacency)
        determinant = bareiss_det(shifted_matrix(adjacency))
        if is_square(prefactor * determinant):
            square_survivors += 1
    if square_survivors != 0:
        fail(f"A1 has {square_survivors} square survivors")
    return len(solutions), square_survivors


def weak_compositions(total, length, maximum):
    values = [0] * length

    def generate(index, remaining):
        if index == length:
            if remaining == 0:
                yield tuple(values)
            return
        for value in range(min(maximum, remaining) + 1):
            values[index] = value
            yield from generate(index + 1, remaining - value)

    yield from generate(0, total)


def binary_matrices(row_sums, column_sums):
    rows = [0] * len(row_sums)
    remaining = list(column_sums)

    def generate(index):
        if index == len(row_sums):
            if all(value == 0 for value in remaining):
                yield tuple(rows)
            return
        needed = row_sums[index]
        available = [j for j, value in enumerate(remaining) if value > 0]
        if len(available) < needed:
            return
        for columns in combinations(available, needed):
            for j in columns:
                remaining[j] -= 1
            if all(0 <= remaining[j] <= len(row_sums) - index - 1 for j in range(len(remaining))):
                rows[index] = sum(1 << j for j in columns)
                yield from generate(index + 1)
            for j in columns:
                remaining[j] += 1

    yield from generate(0)


def value_preserving_permutations(labels):
    classes = {}
    for index, label in enumerate(labels):
        classes.setdefault(label, []).append(index)
    positions = list(classes.values())
    choices = [list(permutations(group)) for group in positions]
    output = []
    for selected in product(*choices):
        permutation = list(range(len(labels)))
        for slots, old_indices in zip(positions, selected):
            for slot, old_index in zip(slots, old_indices):
                permutation[slot] = old_index
        output.append(tuple(permutation))
    return output


def canonical_bipartite(rows, row_labels, column_labels):
    column_permutations = value_preserving_permutations(column_labels)
    label_values = sorted(set(row_labels), reverse=True)
    best = None
    for column_permutation in column_permutations:
        transformed = []
        for index, mask in enumerate(rows):
            new_mask = 0
            for new_column, old_column in enumerate(column_permutation):
                if (mask >> old_column) & 1:
                    new_mask |= 1 << new_column
            transformed.append((row_labels[index], new_mask))
        ordered = []
        for label in label_values:
            ordered.extend((label, mask) for mask in sorted(mask for value, mask in transformed if value == label))
        code = tuple(ordered)
        if best is None or code < best:
            best = code
    return best


def enumerate_A2():
    # K7, K6, K5.  Edge counts between the three groups are 2,5,10.
    ab_types = sorted(set(tuple(sorted(values, reverse=True)) for values in weak_compositions(2, 6, 2)))
    ac_types = sorted(set(tuple(sorted(values, reverse=True)) for values in weak_compositions(5, 5, 3)))
    representatives = []
    for ab in ab_types:
        row_sums = tuple(2 - value for value in ab)
        for ac in ac_types:
            column_sums = tuple(3 - value for value in ac)
            canonical = {}
            for matrix in binary_matrices(row_sums, column_sums):
                key = canonical_bipartite(matrix, ab, ac)
                canonical.setdefault(key, matrix)
            representatives.extend((ab, ac, matrix) for matrix in canonical.values())
    if len(representatives) != 78:
        fail(f"A2 type count {len(representatives)} != 78")

    prefactor = 225 * (7 ** 24) * (15 ** 175)
    square_survivors = 0
    for ab, ac, matrix in representatives:
        adjacency = zero_matrix(18)
        groups = [list(range(0, 7)), list(range(7, 13)), list(range(13, 18))]
        for group in groups:
            add_clique(adjacency, group)
        next_a = 0
        for b_index, count in enumerate(ab):
            for _ in range(count):
                add_edge(adjacency, groups[0][next_a], groups[1][b_index])
                next_a += 1
        for c_index, count in enumerate(ac):
            for _ in range(count):
                add_edge(adjacency, groups[0][next_a], groups[2][c_index])
                next_a += 1
        if next_a != 7:
            fail("A2 K7 leaf count mismatch")
        for b_index, mask in enumerate(matrix):
            for c_index in range(5):
                if (mask >> c_index) & 1:
                    add_edge(adjacency, groups[1][b_index], groups[2][c_index])
        check_regular(adjacency)
        determinant = bareiss_det(shifted_matrix(adjacency))
        if is_square(prefactor * determinant):
            square_survivors += 1
    if square_survivors != 0:
        fail(f"A2 has {square_survivors} square survivors")
    return len(representatives), square_survivors


def canonical_path_word(word):
    word = tuple(word)
    return min(word, tuple(reversed(word)))


def bounded_partitions(total, minimum=2, maximum=6, start=None):
    if start is None:
        start = minimum
    if total == 0:
        yield ()
        return
    for value in range(start, min(maximum, total) + 1):
        for rest in bounded_partitions(total - value, minimum, maximum, value):
            yield (value,) + rest


def enumerate_B1():
    # Two K7 and two K6 blocks.  The external graph has degrees 1 and 2,
    # hence paths with K7 endpoints and alternating K6 interiors, plus even
    # alternating K6 cycles.
    path_words = {canonical_path_word((0, 1))}
    for internal_count in range(1, 13):
        for start_color in (2, 3):
            internal = tuple(start_color if i % 2 == 0 else 5 - start_color for i in range(internal_count))
            for left in (0, 1):
                for right in (0, 1):
                    path_words.add(canonical_path_word((left,) + internal + (right,)))
    paths = sorted(path_words, key=lambda word: (len(word), word))
    path_counts = [tuple(word.count(color) for color in range(4)) for word in paths]

    path_solutions = []

    def choose_paths(start, number, remaining, chosen):
        if number == 7:
            if remaining[0] == 0 and remaining[1] == 0:
                path_solutions.append((tuple(chosen), remaining))
            return
        for index in range(start, len(paths)):
            counts = path_counts[index]
            if all(counts[i] <= remaining[i] for i in range(4)):
                choose_paths(
                    index,
                    number + 1,
                    tuple(remaining[i] - counts[i] for i in range(4)),
                    chosen + [index],
                )

    choose_paths(0, 0, (7, 7, 6, 6), [])
    solutions = []
    for selected_paths, remaining in path_solutions:
        if remaining[2] != remaining[3]:
            continue
        for cycle_halves in bounded_partitions(remaining[2]):
            solutions.append((selected_paths, cycle_halves))
    if len(solutions) != 6204:
        fail(f"B1 type count {len(solutions)} != 6204")

    prefactor = 225 * (7 ** 23) * (15 ** 168)
    square_survivors = 0
    for selected_paths, cycle_halves in solutions:
        adjacency = zero_matrix(26)
        groups = [list(range(0, 7)), list(range(7, 14)), list(range(14, 20)), list(range(20, 26))]
        for group in groups:
            add_clique(adjacency, group)
        next_vertex = [0, 0, 0, 0]
        for index in selected_paths:
            word = paths[index]
            vertices = []
            for color in word:
                vertex = groups[color][next_vertex[color]]
                next_vertex[color] += 1
                vertices.append(vertex)
            for i in range(len(vertices) - 1):
                add_edge(adjacency, vertices[i], vertices[i + 1])
        for half in cycle_halves:
            word = tuple([2, 3] * half)
            vertices = []
            for color in word:
                vertex = groups[color][next_vertex[color]]
                next_vertex[color] += 1
                vertices.append(vertex)
            for i, u in enumerate(vertices):
                add_edge(adjacency, u, vertices[(i + 1) % len(vertices)])
        if next_vertex != [7, 7, 6, 6]:
            fail("B1 color use mismatch")
        check_regular(adjacency)
        determinant = bareiss_det(shifted_matrix(adjacency))
        if is_square(prefactor * determinant):
            square_survivors += 1
    if square_survivors != 0:
        fail(f"B1 has {square_survivors} square survivors")
    return len(solutions), square_survivors


def multiset_indices(type_count, length, start=0, prefix=()):
    if length == 0:
        yield prefix
        return
    for index in range(start, type_count):
        yield from multiset_indices(type_count, length - 1, index, prefix + (index,))


def enumerate_B2():
    # Three K7 blocks and one K5 block.
    triple_types = [values for values in product(range(4), repeat=3) if sum(values) == 3]
    solutions = []
    for selected in multiset_indices(len(triple_types), 5):
        used = [sum(triple_types[index][group] for index in selected) for group in range(3)]
        if any(value > 7 for value in used):
            continue
        leftover = [7 - value for value in used]
        numerators = [
            leftover[0] + leftover[1] - leftover[2],
            leftover[0] + leftover[2] - leftover[1],
            leftover[1] + leftover[2] - leftover[0],
        ]
        if min(numerators) < 0 or any(value % 2 for value in numerators):
            continue
        edge_counts = tuple(value // 2 for value in numerators)
        if sum(edge_counts) != 3:
            fail("B2 matching count mismatch")
        solutions.append((selected, edge_counts))
    if len(solutions) != 454:
        fail(f"B2 type count {len(solutions)} != 454")

    prefactor = 225 * (7 ** 23) * (15 ** 168)
    square_survivors = 0
    for selected, edge_counts in solutions:
        adjacency = zero_matrix(26)
        groups = [list(range(0, 7)), list(range(7, 14)), list(range(14, 21))]
        k5 = list(range(21, 26))
        for group in groups + [k5]:
            add_clique(adjacency, group)
        next_vertex = [0, 0, 0]
        for center, type_index in zip(k5, selected):
            counts = triple_types[type_index]
            for group, count in enumerate(counts):
                for _ in range(count):
                    add_edge(adjacency, center, groups[group][next_vertex[group]])
                    next_vertex[group] += 1
        remaining = [groups[group][next_vertex[group]:] for group in range(3)]
        positions = [0, 0, 0]
        for count, (left, right) in zip(edge_counts, ((0, 1), (0, 2), (1, 2))):
            for _ in range(count):
                add_edge(adjacency, remaining[left][positions[left]], remaining[right][positions[right]])
                positions[left] += 1
                positions[right] += 1
        if any(positions[group] != len(remaining[group]) for group in range(3)):
            fail("B2 leftover matching mismatch")
        check_regular(adjacency)
        determinant = bareiss_det(shifted_matrix(adjacency))
        if is_square(prefactor * determinant):
            square_survivors += 1
    if square_survivors != 0:
        fail(f"B2 has {square_survivors} square survivors")
    return len(solutions), square_survivors


def matching_solutions_four(leftover):
    l0, l1, l2, l3 = leftover
    for x01 in range(min(l0, l1) + 1):
        for x02 in range(min(l0 - x01, l2) + 1):
            x03 = l0 - x01 - x02
            if x03 < 0 or x03 > l3:
                continue
            a = l1 - x01
            b = l2 - x02
            c = l3 - x03
            numerators = (a + b - c, a + c - b, b + c - a)
            if min(numerators) < 0 or any(value % 2 for value in numerators):
                continue
            yield (x01, x02, x03, numerators[0] // 2, numerators[1] // 2, numerators[2] // 2)


def canonical_C_solution(pair_types, selected, edge_counts):
    compositions = [pair_types[index] for index in selected]
    edge_matrix = [[0] * 4 for _ in range(4)]
    for count, (left, right) in zip(edge_counts, ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))):
        edge_matrix[left][right] = count
        edge_matrix[right][left] = count
    best = None
    for permutation in permutations(range(4)):
        transformed_compositions = tuple(sorted(tuple(comp[permutation[i]] for i in range(4)) for comp in compositions))
        transformed_edges = tuple(
            edge_matrix[permutation[left]][permutation[right]]
            for left, right in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
        )
        code = (transformed_compositions, transformed_edges)
        if best is None or code < best:
            best = code
    return best


def enumerate_C():
    # Four K7 blocks and one K6 block.
    pair_types = [values for values in product(range(3), repeat=4) if sum(values) == 2]
    representatives = {}
    for selected in multiset_indices(len(pair_types), 6):
        used = [sum(pair_types[index][group] for index in selected) for group in range(4)]
        if any(value > 7 for value in used):
            continue
        leftover = tuple(7 - value for value in used)
        for edge_counts in matching_solutions_four(leftover):
            key = canonical_C_solution(pair_types, selected, edge_counts)
            representatives.setdefault(key, (selected, edge_counts))
    if len(representatives) != 1125:
        fail(f"C type count {len(representatives)} != 1125")

    prefactor = 225 * (7 ** 22) * (15 ** 161)
    square_survivors = 0
    for selected, edge_counts in representatives.values():
        adjacency = zero_matrix(34)
        groups = [list(range(0, 7)), list(range(7, 14)), list(range(14, 21)), list(range(21, 28))]
        k6 = list(range(28, 34))
        for group in groups + [k6]:
            add_clique(adjacency, group)
        next_vertex = [0, 0, 0, 0]
        for center, type_index in zip(k6, selected):
            counts = pair_types[type_index]
            for group, count in enumerate(counts):
                for _ in range(count):
                    add_edge(adjacency, center, groups[group][next_vertex[group]])
                    next_vertex[group] += 1
        remaining = [groups[group][next_vertex[group]:] for group in range(4)]
        positions = [0, 0, 0, 0]
        for count, (left, right) in zip(edge_counts, ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))):
            for _ in range(count):
                add_edge(adjacency, remaining[left][positions[left]], remaining[right][positions[right]])
                positions[left] += 1
                positions[right] += 1
        if any(positions[group] != len(remaining[group]) for group in range(4)):
            fail("C leftover matching mismatch")
        check_regular(adjacency)
        determinant = bareiss_det(shifted_matrix(adjacency))
        if is_square(prefactor * determinant):
            square_survivors += 1
    if square_survivors != 0:
        fail(f"C has {square_survivors} square survivors")
    return len(representatives), square_survivors


def regular_multigraph_matrices(size, degree):
    matrix = [[0] * size for _ in range(size)]
    remaining = [degree] * size

    def generate(i, j):
        if i >= size - 1:
            if all(value == 0 for value in remaining):
                yield tuple(tuple(row) for row in matrix)
            return
        if j >= size:
            if remaining[i] == 0:
                yield from generate(i + 1, i + 2)
            return
        maximum = min(remaining[i], remaining[j])
        for value in range(maximum + 1):
            matrix[i][j] = value
            matrix[j][i] = value
            remaining[i] -= value
            remaining[j] -= value
            if remaining[i] <= sum(remaining[index] for index in range(j + 1, size)):
                yield from generate(i, j + 1)
            remaining[i] += value
            remaining[j] += value
        matrix[i][j] = 0
        matrix[j][i] = 0

    yield from generate(0, 1)


def canonical_six_k7_graph(multigraph):
    groups = [list(range(7 * group, 7 * (group + 1))) for group in range(6)]
    allocations = [[[] for _ in range(6)] for _ in range(6)]
    for i in range(6):
        position = 0
        for j in range(6):
            if i == j:
                continue
            count = multigraph[i][j]
            allocations[i][j] = groups[i][position:position + count]
            position += count
        if position != 7:
            fail("D allocation row mismatch")
    adjacency = zero_matrix(42)
    for group in groups:
        add_clique(adjacency, group)
    for i in range(6):
        for j in range(i + 1, 6):
            left = allocations[i][j]
            right = allocations[j][i]
            if len(left) != len(right):
                fail("D allocation symmetry mismatch")
            for u, v in zip(left, right):
                add_edge(adjacency, u, v)
    check_regular(adjacency)
    return adjacency


def ldl_diagonal(matrix):
    n = len(matrix)
    lower = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    diagonal = [Fraction(0)] * n
    for i in range(n):
        lower[i][i] = Fraction(1)
        pivot = Fraction(matrix[i][i])
        for k in range(i):
            pivot -= lower[i][k] * lower[i][k] * diagonal[k]
        if pivot == 0:
            fail("zero LDL pivot")
        diagonal[i] = pivot
        for j in range(i + 1, n):
            value = Fraction(matrix[j][i])
            for k in range(i):
                value -= lower[j][k] * lower[i][k] * diagonal[k]
            lower[j][i] = value / pivot
    return diagonal


def valuation_fraction(value, prime):
    numerator = value.numerator
    denominator = value.denominator
    valuation = 0
    while numerator % prime == 0:
        valuation += 1
        numerator //= prime
    while denominator % prime == 0:
        valuation -= 1
        denominator //= prime
    return valuation


def unit_mod_prime(value, prime):
    valuation = valuation_fraction(value, prime)
    numerator = value.numerator
    denominator = value.denominator
    if valuation >= 0:
        numerator //= prime ** valuation
    else:
        denominator //= prime ** (-valuation)
    return (numerator % prime) * pow(denominator % prime, -1, prime) % prime


def legendre(value, prime):
    residue = pow(value % prime, (prime - 1) // 2, prime)
    if residue == 1:
        return 1
    if residue == prime - 1:
        return -1
    fail("Legendre symbol received zero")


def hilbert_odd(a, b, prime):
    alpha = valuation_fraction(a, prime)
    beta = valuation_fraction(b, prime)
    u = unit_mod_prime(a, prime)
    v = unit_mod_prime(b, prime)
    result = -1 if (alpha * beta * ((prime - 1) // 2)) % 2 else 1
    if beta % 2:
        result *= legendre(u, prime)
    if alpha % 2:
        result *= legendre(v, prime)
    return result


def hasse_invariant_odd(diagonal, prime):
    invariant = 1
    product_so_far = Fraction(1)
    for coefficient in diagonal:
        invariant *= hilbert_odd(product_so_far, coefficient, prime)
        product_so_far *= coefficient
    return invariant


def enumerate_D_and_hasse():
    # Six K7 blocks.  The external graph is a perfect matching.  Its
    # color-count matrix H is a loopless symmetric 7-regular multigraph on six
    # colors.  The determinant reduction is
    # det(C_R)=224^15 det(119 I_6-H).
    multigraph_count = 0
    determinant_survivors = []
    prefactor = 225 * (7 ** 21) * (15 ** 154) * (224 ** 15)
    for multigraph in regular_multigraph_matrices(6, 7):
        multigraph_count += 1
        reduced = [
            [(119 if i == j else 0) - multigraph[i][j] for j in range(6)]
            for i in range(6)
        ]
        determinant = bareiss_det(reduced)
        if is_square(prefactor * determinant):
            determinant_survivors.append(multigraph)
    if multigraph_count != 100_135:
        fail(f"D multigraph count {multigraph_count} != 100135")
    if len(determinant_survivors) != 675:
        fail(f"D determinant survivors {len(determinant_survivors)} != 675")

    d8 = [[15 * (i == j) - 1 for j in range(8)] for i in range(8)]
    fixed_diagonal = ldl_diagonal(d8) * 22
    hasse_failures = 0
    for multigraph in determinant_survivors:
        residual = canonical_six_k7_graph(multigraph)
        residual_diagonal = ldl_diagonal(shifted_matrix(residual))
        stable_diagonal = fixed_diagonal + residual_diagonal + [Fraction(-225, 7)]
        invariant = hasse_invariant_odd(stable_diagonal, 7)
        if invariant == -1:
            hasse_failures += 1
        else:
            fail("D determinant survivor passed the 7-adic Hasse test")
    return multigraph_count, len(determinant_survivors), hasse_failures


def parameter_counts(eta_minimum):
    old_pairs = 0
    new_pairs = 0
    old_triples = 0
    new_triples = 0
    for r in range(R_MAX + 1):
        old_delta_max = (BUDGET - 8 * r) // 7
        new_delta_max = (BUDGET - eta_minimum - 8 * r) // 7
        old_pairs += old_delta_max + 1
        new_pairs += max(0, new_delta_max + 1)
        for delta in range(old_delta_max + 1):
            eta_max = BUDGET - 8 * r - 7 * delta
            old_triples += eta_max + 1
            if eta_max >= eta_minimum:
                new_triples += eta_max - eta_minimum + 1
    return old_pairs, new_pairs, old_triples, new_triples


def main():
    if M * D != 1_052_504 or N - M * D != 1_052:
        fail("base arithmetic mismatch")
    if 15 * D != 72_420 or A_REQ - 15 * D != 31:
        fail("per-point demand mismatch")

    v10_rows = verify_v10_obstruction()
    cost6 = clique_cost_skeletons(6)
    expected_cost6 = [
        (18, 25, 0, 3, 0, 0),
        (18, 25, 1, 1, 1, 0),
        (18, 25, 2, 0, 0, 4),
        (26, 24, 2, 2, 0, 0),
        (26, 24, 3, 0, 1, 0),
        (34, 23, 4, 1, 0, 0),
        (42, 22, 6, 0, 0, 0),
    ]
    if cost6 != expected_cost6:
        fail(f"cost-6 skeleton mismatch: {cost6}")

    a1 = enumerate_A1()
    a2 = enumerate_A2()
    # The third v=18 skeleton (2 K7 plus four remaining vertices) is impossible:
    # 14 clique-external stubs plus at most 12 internal stubs on four vertices
    # cannot supply the required residual degree sum 28.
    if 14 + 12 >= 28:
        fail("A3 degree contradiction arithmetic was altered")
    a3 = (1, 0)
    b1 = enumerate_B1()
    b2 = enumerate_B2()
    c_result = enumerate_C()
    d_result = enumerate_D_and_hasse()

    # chi is even.  The v>=18 argument rules out chi<6; the exhaustive block
    # above rules out chi=6.  Therefore chi>=8 and eta>=31*8=248.
    eta_minimum = 248
    delta_global = (BUDGET - eta_minimum) // 7
    delta_at_rmax = (BUDGET - eta_minimum - 8 * R_MAX) // 7
    if (delta_global, delta_at_rmax) != (201, 28):
        fail("sharpened delta maxima mismatch")
    c_global = 1_052 + delta_global
    c_at_rmax = 1_052 + delta_at_rmax
    perfect_global = M - delta_global
    perfect_at_rmax = M - delta_at_rmax
    if (c_global, c_at_rmax, perfect_global, perfect_at_rmax) != (1_253, 1_080, 17, 190):
        fail("pencil compression arithmetic mismatch")

    old_pairs, new_pairs, old_triples, new_triples = parameter_counts(eta_minimum)
    if (old_pairs, new_pairs, old_triples, new_triples) != (22_973, 17_589, 13_502_312, 8_469_896):
        fail("finite parameter count mismatch")

    print("V10_DETERMINANTS")
    for partition, factorization in v10_rows:
        print(f"  {'+'.join(map(str, partition))}: {factorization}; square_after_prefactor=False")
    print("COST6_SKELETON_ENUMERATION")
    print(f"  A1_3K6_types={a1[0]}; determinant_square_survivors={a1[1]}")
    print(f"  A2_K7_K6_K5_types={a2[0]}; determinant_square_survivors={a2[1]}")
    print("  A3_2K7_U4_types=1; graph_degree_survivors=0")
    print(f"  B1_2K7_2K6_types={b1[0]}; determinant_square_survivors={b1[1]}")
    print(f"  B2_3K7_K5_types={b2[0]}; determinant_square_survivors={b2[1]}")
    print(f"  C_4K7_K6_types={c_result[0]}; determinant_square_survivors={c_result[1]}")
    print(f"  D_6K7_multigraphs={d_result[0]}; determinant_square_survivors={d_result[1]}; hasse7_failures={d_result[2]}")
    print("SHARPENED_CLIQUE_AND_PENCIL_LEDGER")
    print(f"  eta_min={eta_minimum}")
    print(f"  delta_max_global={delta_global}")
    print(f"  delta_max_at_r151={delta_at_rmax}")
    print(f"  degE_max_global={delta_global}")
    print(f"  degE_max_at_r151={delta_at_rmax}")
    print(f"  C_max_global={c_global}")
    print(f"  C_max_at_r151={c_at_rmax}")
    print(f"  perfect_fibers_min_global={perfect_global}")
    print(f"  perfect_fibers_min_at_r151={perfect_at_rmax}")
    print("FINITE_PARAMETER_COUNTS")
    print(f"  old_r_delta_pairs={old_pairs}")
    print(f"  new_r_delta_pairs={new_pairs}")
    print(f"  removed_r_delta_pairs={old_pairs-new_pairs}")
    print(f"  old_r_delta_eta_triples={old_triples}")
    print(f"  new_r_delta_eta_triples={new_triples}")
    print(f"  removed_r_delta_eta_triples={old_triples-new_triples}")
    print("PASS")


if __name__ == "__main__":
    main()
