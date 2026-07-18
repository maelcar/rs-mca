#!/usr/bin/env python3
"""Finite structural audit for the weighted triple-line bound used in R31 role 06.

Labels are 0..6. A line is a 3-subset. A family is linear if no label pair
occurs in two lines. This checks the complete labelled census through six lines
and verifies the short certificates yielding total weight W <= 2r whenever
line weights are <= lambda <= r/2 and vertex loads are <= r.
"""
from itertools import combinations
from collections import Counter

V = range(7)
EDGES = tuple(combinations(V, 3))

def linear(fam):
    used = set()
    for e in fam:
        for p in combinations(e, 2):
            if p in used:
                return False
            used.add(p)
    return True

def degrees(fam):
    return tuple(sum(v in e for e in fam) for v in V)

counts = Counter()
five_degree_sequences = Counter()
six_degree_sequences = Counter()
cert_A = cert_B = cert_six = 0
examples = {}

for m in range(0, 7):
    for fam in combinations(EDGES, m):
        if not linear(fam):
            continue
        counts[m] += 1
        deg = degrees(fam)
        seq = tuple(sorted(deg, reverse=True))
        examples.setdefault((m, seq), fam)
        if m <= 4:
            # W <= m lambda <= 4 lambda <= 2r.
            continue
        if m == 5:
            five_degree_sequences[seq] += 1
            if seq == (3, 2, 2, 2, 2, 2, 2):
                v = deg.index(3)
                incident = [i for i,e in enumerate(fam) if v in e]
                assert len(incident) == 3
                # Vertex-v load <= r; the two uncovered line weights are each <= lambda.
                assert len(set(range(5)) - set(incident)) == 2
                cert_A += 1
            elif seq == (3, 3, 2, 2, 2, 2, 1):
                hubs = [v for v,d in enumerate(deg) if d == 3]
                assert len(hubs) == 2
                I = [{i for i,e in enumerate(fam) if v in e} for v in hubs]
                # The two hub constraints cover every line, with their common line counted twice.
                assert len(I[0] & I[1]) == 1
                assert I[0] | I[1] == set(range(5))
                cert_B += 1
            else:
                raise AssertionError((seq, fam))
        elif m == 6:
            six_degree_sequences[seq] += 1
            assert seq == (3, 3, 3, 3, 2, 2, 2)
            hubs = [v for v,d in enumerate(deg) if d == 3]
            assert len(hubs) == 4
            # Each line contains exactly two degree-3 labels, so summing their
            # vertex-load constraints gives 2W <= 4r.
            assert all(sum(v in e for v in hubs) == 2 for e in fam)
            # The three unused label pairs are a triangle: Fano-minus-one.
            used_pairs = {p for e in fam for p in combinations(e,2)}
            missing = [p for p in combinations(V,2) if p not in used_pairs]
            assert len(missing) == 3
            miss_deg = Counter(v for p in missing for v in p)
            assert sorted(miss_deg.values()) == [2,2,2]
            cert_six += 1

# Seven lines would be an STS(7)/Fano plane. We census it combinatorially but
# the source excludes it by odd-characteristic nonrepresentability.
seven = 0
for fam in combinations(EDGES, 7):
    if linear(fam):
        seven += 1
assert seven == 30

print('linear_family_counts_m0_to_m6', ' '.join(f'{m}:{counts[m]}' for m in range(7)))
print('five_line_degree_sequences', dict(sorted(five_degree_sequences.items())))
print('five_line_certificates', f'A={cert_A}', f'B={cert_B}', f'total={cert_A+cert_B}')
print('six_line_degree_sequences', dict(sorted(six_degree_sequences.items())))
print('six_line_fano_minus_one_certificates', cert_six)
print('seven_line_labelled_fano_systems', seven)
print('bound', 'm<=4: W<=4lambda<=2r; m=5: certificates A/B; m=6: 2W<=4r')
print('INDEPENDENT_TRIPLE_LINE_BOUND: PASS')
