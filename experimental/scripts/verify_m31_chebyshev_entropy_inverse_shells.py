#!/usr/bin/env python3
"""Zero-argument, stdlib-only verifier for the M31 Chebyshev few-shell packet.

It recomputes:
  * the exact M31-list constants and one-shell affine cap;
  * the finite Turan higher-shell obligation;
  * two exhaustive small Chebyshev shell censuses;
  * the faithful p=127,n=32,m=15,w=2 prefix distribution;
  * the integer-only primitive-participation counterexample;
  * every numeric certificate field in the shipped JSON; and
  * ten corruption self-tests, each of which must be rejected.

Run with no arguments.  The script applies a 2 GiB address-space cap itself;
the packet's canonical command also runs it under ``ulimit -v 2097152``.
"""

import copy
import hashlib
import json
import math
import os
import sys
from collections import Counter, defaultdict
from itertools import combinations


def _apply_address_space_cap():
    try:
        import resource

        cap = 2 * 1024 ** 3
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        new_hard = cap if hard == resource.RLIM_INFINITY else min(hard, cap)
        if soft == resource.RLIM_INFINITY or soft > cap:
            resource.setrlimit(resource.RLIMIT_AS, (cap, new_hard))
    except Exception:
        pass


_apply_address_space_cap()

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_PATH = os.path.join(
    REPO_ROOT,
    "experimental",
    "data",
    "cap25_v13_m31_chebyshev_entropy_inverse_shells.json",
)

CHECKS = []


def check(name, condition, detail=""):
    ok = bool(condition)
    CHECKS.append((name, ok))
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{suffix}")


def ceil_div(a, b):
    return -((-a) // b)


# --------------------------------------------------------------------- torus domain
def cmul(u, v, p):
    a, b = u
    c, d = v
    return ((a * c - b * d) % p, (a * d + b * c) % p)


def cpow(u, exponent, p):
    out = (1, 0)
    while exponent:
        if exponent & 1:
            out = cmul(out, u, p)
        u = cmul(u, u, p)
        exponent >>= 1
    return out


def element_order(u, p):
    value = (1, 0)
    for order in range(1, p + 2):
        value = cmul(value, u, p)
        if value == (1, 0):
            return order
    raise AssertionError("order exceeds p+1")


def circle_generator(p):
    assert p % 4 == 3
    for a in range(p):
        for b in range(p):
            u = (a, b)
            if (a * a + b * b) % p == 1 and element_order(u, p) == p + 1:
                return u
    raise AssertionError("no norm-one generator")


def cheb_twin_domain(p, n, goff=1):
    omega = circle_generator(p)
    order = p + 1
    assert order % n == 0 and 2 * n <= order
    hgen = cpow(omega, order // n, p)
    H = [cpow(hgen, j, p) for j in range(n)]
    g = cpow(omega, goff, p)
    ginv = cpow(omega, order - goff, p)
    lifted = {cmul(g, h, p) for h in H} | {cmul(ginv, h, p) for h in H}
    by_x = defaultdict(list)
    for u in lifted:
        by_x[u[0]].append(u)
    D = sorted(by_x)
    two_to_one = len(lifted) == 2 * n and all(len(fiber) == 2 for fiber in by_x.values())
    return D, omega, two_to_one


def cheb_T(degree, x, p):
    if degree == 0:
        return 1
    if degree == 1:
        return x % p
    t0, t1 = 1, x % p
    for _ in range(2, degree + 1):
        t0, t1 = t1, (2 * x * t1 - t0) % p
    return t1


def rank_mod(matrix, p):
    a = [row[:] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col] % p), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col] % p, -1, p)
        a[rank] = [(v * inv) % p for v in a[rank]]
        for r in range(rows):
            if r != rank and a[r][col] % p:
                factor = a[r][col] % p
                a[r] = [(x - factor * y) % p for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


# --------------------------------------------------------------- exhaustive shell gates
def prefix_families(D, p, m, w):
    fibers = defaultdict(list)
    for subset in combinations(D, m):
        key = tuple(sum(pow(x, j, p) for x in subset) % p for j in range(1, w + 1))
        fibers[key].append(frozenset(subset))
    return fibers


def shells(family, m):
    return sorted(
        {
            m - len(a & b)
            for i, a in enumerate(family)
            for b in family[i + 1 :]
        }
    )


def shell_gate(p, n, m, w):
    D, omega, two_to_one = cheb_twin_domain(p, n)
    fibers = prefix_families(D, p, m, w)
    kernel_dim = n - w - 1
    bounded = True
    for family in fibers.values():
        s = len(shells(family, m))
        bounded &= len(family) <= math.comb(kernel_dim + s, s)
    eval_matrix = [[cheb_T(j, x, p) for x in D] for j in range(w + 1)]
    return D, omega, two_to_one, fibers, bounded, rank_mod(eval_matrix, p)


# --------------------------------------------------------------- subset-sum dynamic programs
def subset_hist_1d(values, m, p):
    dp = [[0] * p for _ in range(m + 1)]
    dp[0][0] = 1
    seen = 0
    for value in values:
        seen += 1
        for j in range(min(seen, m), 0, -1):
            prev = dp[j - 1]
            cur = dp[j]
            for u, count in enumerate(prev):
                if count:
                    cur[(u + value) % p] += count
    return dp[m]


def subset_hist_2d(D, m, p):
    size = p * p
    dp = [[0] * size for _ in range(m + 1)]
    dp[0][0] = 1
    seen = 0
    for x in D:
        seen += 1
        x2 = x * x % p
        for j in range(min(seen, m), 0, -1):
            prev = dp[j - 1]
            cur = dp[j]
            for index, count in enumerate(prev):
                if count:
                    u, v = divmod(index, p)
                    target = ((u + x) % p) * p + (v + x2) % p
                    cur[target] += count
    return dp[m]


def nonzero_fourier_energy(histogram, p, total):
    return p * sum(value * value for value in histogram) - total * total


print("== Inputs and theorem target ==")
with open(JSON_PATH, encoding="utf-8") as handle:
    SHIPPED = json.load(handle)

# --------------------------------------------------------------- exact deployed arithmetic
p = 2 ** 31 - 1
n = 2 ** 21
k = 2 ** 20
a_plus = 1_116_023
w = a_plus - k
m = n - a_plus
Bstar = (p ** 4) // (2 ** 100)
kernel_dim = n - w - 1
one_shell_cap = kernel_dim + 1
headroom = Bstar - one_shell_cap

check("M31 constants", (p, n, k, a_plus, w, m) == (2147483647, 2097152, 1048576, 1116023, 67447, 981129))
check("signed-profile characteristic gate p > 2n", p > 2 * n)
check("B* = 2^24-1", Bstar == 16_777_215)
check("Chebyshev affine-kernel dimension N=n-w-1", kernel_dim == 2_029_704)
check("one-shell cap n-w", one_shell_cap == 2_029_705)
check("one-shell exact headroom", headroom == 14_747_510)

print("\n== Exact M31-list average ceiling (large integers) ==")
ambient_count = math.comb(n, m)
pw = p ** w
avg_ceil = ceil_div(ambient_count, pw)
check("ceil(C(n,m)/p^w)=1993678", avg_ceil == 1_993_678, str(avg_ceil))
check("K-1 numerator", Bstar - avg_ceil == 14_783_537)

print("\n== Finite multishell obligation ==")
L = Bstar + 1
r = one_shell_cap
q, remainder = divmod(L, r)
nonminimal_pairs = remainder * math.comb(q + 1, 2) + (r - remainder) * math.comb(q, 2)
anchor_min = ceil_div(2 * nonminimal_pairs, L)
check("first violating subfamily L=B*+1=8n", L == 16_777_216 == 8 * n)
check("balanced Turan division", (q, remainder) == (8, 539_576))
check("higher-shell pair floor", nonminimal_pairs == 61_148_348)
check("some anchor has at least 8 higher-shell neighbors", anchor_min == 8)
check("minimum/higher exchange sizes", (w + 1, w + 2) == (67_448, 67_449))

print("\n== Exhaustive shell gate: p=31,n=8,m=4,w=2 ==")
D31, omega31, two31, fibers31, bounded31, rank31 = shell_gate(31, 8, 4, 2)
collisions31 = [(key, family) for key, family in fibers31.items() if len(family) > 1]
shells31 = shells(collisions31[0][1], 4)
check("faithful p31 twin domain", D31 == [2, 5, 10, 11, 20, 21, 26, 29] and two31)
check("Chebyshev rows T0..T2 have rank 3", rank31 == 3)
check("69 occupied fibers", len(fibers31) == 69)
check("sole collision fiber (p1,p2)=(0,2), equivalently (T1,T2)=(0,0)",
      len(collisions31) == 1 and collisions31[0][0] == (0, 2)
      and len(collisions31[0][1]) == 2 and shells31 == [4])
check("affine few-shell cap holds on every p31 fiber", bounded31)
check("p31 collision affine cap is 6", math.comb((8 - 2 - 1) + 1, 1) == 6)

print("\n== Exhaustive shell gate: p=127,n=16,m=8,w=1 ==")
D16, omega127, two16, fibers16, bounded16, rank16 = shell_gate(127, 16, 8, 1)
zero16 = fibers16[(0,)]
shells16 = shells(zero16, 8)
check("faithful p127,n16 twin domain", len(D16) == 16 and two16 and omega127 == (2, 39))
check("Chebyshev rows T0..T1 have rank 2", rank16 == 2)
check("z=0 fiber size 132", len(zero16) == 132)
check("z=0 shell set", shells16 == [2, 3, 4, 5, 6, 8])
check("affine few-shell cap holds on every p127,n16 fiber", bounded16)
check("z=0 affine cap C(20,6)=38760", math.comb((16 - 1 - 1) + 6, 6) == 38_760)

print("\n== Faithful primitive-PR counterexample: p=127,n=32,m=15,w=2 ==")
pt, nt, mt, wt = 127, 32, 15, 2
D32, omega32, two32 = cheb_twin_domain(pt, nt)
expected_D32 = [
    2, 5, 9, 19, 22, 23, 26, 27, 32, 38, 39, 42, 45, 50, 53, 62,
    65, 74, 77, 82, 85, 88, 89, 95, 100, 101, 104, 105, 108, 118, 122, 125,
]
check("p127,n32 standard twin domain", D32 == expected_D32 and two32 and omega32 == (2, 39))
check("D=-D and 0 is absent", set(D32) == {(-x) % pt for x in D32} and 0 not in D32)
t2_fibers = defaultdict(list)
for x in D32:
    t2_fibers[cheb_T(2, x, pt)].append(x)
check("T2 is exactly two-to-one with fibers {x,-x}",
      len(t2_fibers) == 16
      and all(len(xs) == 2 and (xs[0] + xs[1]) % pt == 0 for xs in t2_fibers.values()))

# Exhaustively gate the statement: f=t1*x+t2*x^2 is T2-fiber-constant iff t1=0.
quotient_iff = True
for t1 in range(pt):
    for t2 in range(pt):
        constant = all(
            len({(t1 * x + t2 * x * x) % pt for x in xs}) == 1
            for xs in t2_fibers.values()
        )
        quotient_iff &= constant == (t1 == 0)
check("quadratic quotient directions are exactly t1=0", quotient_iff)
check("primitive direction count", pt * (pt - 1) == 16_002)

total = math.comb(nt, mt)
fiber2 = subset_hist_2d(D32, mt, pt)
sum_fibers = sum(fiber2)
sum_fiber_squares = sum(value * value for value in fiber2)
nonempty = sum(value > 0 for value in fiber2)
min_fiber = min(fiber2)
max_fiber = max(fiber2)
max_syndromes = [list(divmod(i, pt)) for i, value in enumerate(fiber2) if value == max_fiber]
Qraw = pt * pt * sum_fiber_squares - total * total
check("C(32,15)=565722720", total == 565_722_720)
check("all p^2=16129 fibers nonempty", nonempty == 16_129 and min_fiber > 0)
check("fiber range 34139..36079", (min_fiber, max_fiber) == (34_139, 36_079))
check("maximum syndromes", max_syndromes == [[38, 0], [89, 0]])
check("fiber mass and square sum", sum_fibers == total and sum_fiber_squares == 19_846_266_349_238)
check("average floor is 35074", total // (pt * pt) == 35_074)
R_num = pt * pt * max_fiber
R_den = total
gcd_R = math.gcd(R_num, R_den)
R_num //= gcd_R
R_den //= gcd_R
check("normalized max exact and <1.03", (R_num, R_den) == (581_918_191, 565_722_720)
      and 100 * R_num < 103 * R_den)

Qs = []
roots = []
for slope in range(pt):
    values = [(x + slope * x * x) % pt for x in D32]
    histogram = subset_hist_1d(values, mt, pt)
    check_mass = sum(histogram) == total
    if not check_mass:
        raise AssertionError(f"line histogram mass failed at slope {slope}")
    energy = nonzero_fourier_energy(histogram, pt, total)
    root = math.isqrt(energy)
    if not (root * root <= energy < (root + 1) * (root + 1)):
        raise AssertionError("isqrt certificate failed")
    Qs.append(energy)
    roots.append(root)

Qprimitive = sum(Qs)
A = sum(roots)
A2 = A * A
quot_hist = subset_hist_1d([x * x % pt for x in D32], mt, pt)
Qquotient = nonzero_fourier_energy(quot_hist, pt, total)
check("primitive/quotient Parseval split", Qprimitive + Qquotient == Qraw)
check("primitive energy Q", Qprimitive == 649_241_132_046)
check("quotient and raw energies", (Qquotient, Qraw) == (57_584_781_529_256, 58_234_022_661_302))
check("integer L1 lower certificate A", A == 6_615_676 and A2 == 43_767_168_936_976)

gcd_pr = math.gcd(A2, Qprimitive)
pr_lower_num = A2 // gcd_pr
pr_lower_den = Qprimitive // gcd_pr
excess_55 = A2 - 55 * Qprimitive
check("PR_primitive lower fraction", (pr_lower_num, pr_lower_den) == (21_883_584_468_488, 324_620_566_023))
check("integer lower bound exceeds 55", excess_55 == 8_058_906_674_446 and excess_55 > 0)

nu_num = (Bstar - avg_ceil) ** 2
nu_den = avg_ceil ** 2
cross_nu = A2 * nu_den - Qprimitive * nu_num
check("nu*_ref exact fraction", (nu_num, nu_den) == (218_552_966_230_369, 3_974_751_967_684))
check("primitive lower bound exceeds nu*_ref exactly", cross_nu == 32_070_065_644_787_419_800_378_610 and cross_nu > 0)

gcd_energy = math.gcd(Qquotient, Qraw)
energy_num = Qquotient // gcd_energy
energy_den = Qraw // gcd_energy
check("quotient energy fraction exact", (energy_num, energy_den) == (28_792_390_764_628, 29_117_011_330_651))
check("quotient carries >98% of nonzero L2 energy", 100 * energy_num > 98 * energy_den)

qs_bytes = ",".join(str(value) for value in Qs).encode("ascii")
qs_sha256 = hashlib.sha256(qs_bytes).hexdigest()
sum_qs_squared = sum(value * value for value in Qs)
weighted_qs = sum((index + 1) * value for index, value in enumerate(Qs))
check("127-line Q_s certificate hash", qs_sha256 == "fa7d7d93f0f812e2094b6b546c8ec28661d3d2c8e32cc1a95223507db74503c1")
check("Q_s secondary checksums", len(qs_bytes) == 1347
      and sum_qs_squared == 16_155_812_469_253_054_999_196
      and weighted_qs == 41_844_768_125_384)

# --------------------------------------------------------------- JSON exact replay
certificate = {
    "deployed_m31": {
        "p": p,
        "n": n,
        "k": k,
        "a_plus": a_plus,
        "m": m,
        "w": w,
        "Bstar": Bstar,
        "avg_ceil": avg_ceil,
        "kernel_dimension": kernel_dim,
        "one_shell_cap": one_shell_cap,
        "one_shell_headroom": headroom,
        "K_minus_1_numerator": Bstar - avg_ceil,
        "K_denominator": avg_ceil,
    },
    "finite_multishell_obligation": {
        "selected_size": L,
        "clique_cap": r,
        "quotient": q,
        "remainder": remainder,
        "nonminimal_pair_floor": nonminimal_pairs,
        "anchor_neighbor_floor": anchor_min,
        "minimum_exchange": w + 1,
        "higher_exchange": w + 2,
    },
    "shell_toy_p31": {
        "domain": D31,
        "occupied_fibers": len(fibers31),
        "collision_key": list(collisions31[0][0]),
        "collision_size": len(collisions31[0][1]),
        "collision_shells": shells31,
        "affine_cap": 6,
    },
    "shell_toy_p127_n16": {
        "zero_fiber_size": len(zero16),
        "zero_fiber_shells": shells16,
        "affine_cap": 38_760,
    },
    "primitive_pr_counterexample": {
        "p": pt,
        "n": nt,
        "m": mt,
        "w": wt,
        "domain": D32,
        "subset_count": total,
        "syndrome_count": pt * pt,
        "average_floor": total // (pt * pt),
        "nonempty_fibers": nonempty,
        "min_fiber": min_fiber,
        "max_fiber": max_fiber,
        "max_syndromes": max_syndromes,
        "sum_fiber_squares": sum_fiber_squares,
        "normalized_max_numerator": R_num,
        "normalized_max_denominator": R_den,
        "primitive_direction_count": pt * (pt - 1),
        "Q_primitive": Qprimitive,
        "Q_quotient": Qquotient,
        "Q_raw": Qraw,
        "A": A,
        "A_squared": A2,
        "PR_lower_numerator": pr_lower_num,
        "PR_lower_denominator": pr_lower_den,
        "excess_over_55_cross_product": excess_55,
        "nu_ref_numerator": nu_num,
        "nu_ref_denominator": nu_den,
        "excess_over_nu_ref_cross_product": cross_nu,
        "quotient_energy_numerator": energy_num,
        "quotient_energy_denominator": energy_den,
        "Q_s_count": len(Qs),
        "Q_s_ascii_bytes": len(qs_bytes),
        "Q_s_sha256": qs_sha256,
        "Q_s_sum_squares": sum_qs_squared,
        "Q_s_weighted_sum": weighted_qs,
        "Q_s_first8": Qs[:8],
        "Q_s_last8": Qs[-8:],
    },
}

EXPECTED_PACKET = {
    "schema": "cap25-v13-m31-chebyshev-entropy-inverse-shells-v1",
    "status": "PROVED few-shell Chebyshev entropy-inverse subregime; PROVED-AT-TOYS + COUNTEREXAMPLE primitive-PR witness; CONJECTURAL unrestricted deployed bound",
    "rung": 1,
    "certificate": certificate,
}


def packet_valid(packet):
    return packet == EXPECTED_PACKET


print("\n== Shipped JSON exact replay ==")
check("JSON equals the fully recomputed certificate", packet_valid(SHIPPED))

print("\n== Corruption self-tests (every mutation must be rejected) ==")


def tamper(name, mutate):
    bad = copy.deepcopy(SHIPPED)
    mutate(bad)
    check(f"tamper::{name}", not packet_valid(bad), "corruption rejected")


tamper("wrong_rung", lambda x: x.__setitem__("rung", 2))
tamper("M31_p_plus_one", lambda x: x["certificate"]["deployed_m31"].__setitem__("p", p + 1))
tamper("kernel_dimension_off_by_one", lambda x: x["certificate"]["deployed_m31"].__setitem__("kernel_dimension", kernel_dim + 1))
tamper("one_shell_cap_equals_Bstar", lambda x: x["certificate"]["deployed_m31"].__setitem__("one_shell_cap", Bstar))
tamper("Turan_pair_floor_minus_one", lambda x: x["certificate"]["finite_multishell_obligation"].__setitem__("nonminimal_pair_floor", nonminimal_pairs - 1))
tamper("p31_domain_point", lambda x: x["certificate"]["shell_toy_p31"]["domain"].__setitem__(0, 3))
tamper("toy_max_fiber_plus_one", lambda x: x["certificate"]["primitive_pr_counterexample"].__setitem__("max_fiber", max_fiber + 1))
tamper("primitive_energy_plus_one", lambda x: x["certificate"]["primitive_pr_counterexample"].__setitem__("Q_primitive", Qprimitive + 1))
tamper("A_minus_one", lambda x: x["certificate"]["primitive_pr_counterexample"].__setitem__("A", A - 1))
tamper("Q_s_hash_bitflip", lambda x: x["certificate"]["primitive_pr_counterexample"].__setitem__("Q_s_sha256", "0" + qs_sha256[1:]))

npass = sum(ok for _, ok in CHECKS)
ntotal = len(CHECKS)
print("\n== Result ==")
print("Object: M31 Chebyshev entropy-inverse few-shell subregime + primitive-PR falsifier")
print("Theorem/problem: PR #434; rem:entropy-inverse-skeleton; prob:entropy-inverse-q")
print("Status: PROVED (general/few-shell) + PROVED-AT-TOYS/COUNTEREXAMPLE (faithful toy) + CONJECTURAL (unrestricted bound)")
print(f"RESULT: {'PASS' if npass == ntotal else 'FAIL'} ({npass}/{ntotal} checks)")
sys.exit(0 if npass == ntotal else 1)
