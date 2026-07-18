#!/usr/bin/env python3
from itertools import combinations
from math import isqrt
p=2_130_706_433
omega=1_548_376_985
# deterministic primality by trial division (sqrt(p)<50k)
assert p%2
for d in range(3,isqrt(p)+1,2):
    assert p%d, f'composite factor {d}'
assert p-1==127*2**24
assert pow(omega,64,p)==1 and pow(omega,32,p)!=1
roots=[pow(omega,i,p) for i in range(64)]
assert len(set(roots))==64
# Synthetic complete quadrilateral with target root profile.
Q=[
    frozenset((0,1,4,7)),   # AB
    frozenset((0,2,5,8)),   # AC
    frozenset((0,3,6,9)),   # AD
    frozenset((1,2,6,10)),  # BC
    frozenset((1,3,5,11)),  # BD
    frozenset((2,3,4,12)),  # CD
]
edges=[(0,1,2),(0,3,4),(1,3,5),(2,4,5)]
# Check Pasch incidence and target multiplicities.
assert all(len(set(e))==3 for e in edges)
assert sorted(sum(([i for i in e] for e in edges),[])).count(0)==2
for q in range(6): assert sum(q in e for e in edges)==2
for i,j in combinations(range(4),2): assert len(set(edges[i])&set(edges[j]))==1
mult=[sum(r in q for q in Q) for r in range(64)]
assert (mult.count(1),mult.count(2),mult.count(3),sum(m>=4 for m in mult))==(6,3,4,0)
# Reproduce the pair-incidence completion count: six ordered choices of the
# first shared quartic/vertex-pairing represent one unique Pasch.
paths=0; configs=set()
incident={q:[] for q in range(6)}
for ei,e in enumerate(edges):
    for q in e: incident[q].append(ei)
pair_to_thirds={}
for e in edges:
    for a,b in combinations(e,2):
        third=next(x for x in e if x not in (a,b))
        pair_to_thirds.setdefault(tuple(sorted((a,b))),set()).add(third)
for shared in range(6):
    for e0i,e1i in combinations(incident[shared],2):
        e0,e1=edges[e0i],edges[e1i]
        if len(set(e0)&set(e1))!=1: continue
        ab=[x for x in e0 if x!=shared]
        de=[x for x in e1 if x!=shared]
        for pairing in (0,1):
            b,c=ab; d,e=de[pairing],de[1-pairing]
            common=pair_to_thirds.get(tuple(sorted((b,d))),set()) & pair_to_thirds.get(tuple(sorted((c,e))),set())
            for f in common:
                if len({shared,b,c,d,e,f})==6:
                    paths+=1; configs.add(tuple(sorted((shared,b,c,d,e,f))))
assert paths==6 and len(configs)==1
print(f'FIELD_AND_PASCH_SELFTEST: PASS p={p} omega_order=64 synthetic_paths={paths} synthetic_unique={len(configs)} target_profile=6,3,4')
