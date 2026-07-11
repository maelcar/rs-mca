#!/usr/bin/env python3
"""General-divisor covering constant for the binary-tower C5 defect.

CLOSES the one OPEN residual of PR #610
(experimental/notes/thresholds/c5_defect_magnitude.md, Rung 5.3), quoted verbatim:

    "Prove d_2(N,{1..R}) = o(N) (ideally O_kappa(1)) for EVERY N | 2^s-1 at
     R >= kappa*N -- the general-divisor binary-tower covering constant.  Proved
     [in #610] for N = 2^s-1 (necklace) and prime N with 2 a primitive root;
     measured O(1) for all composite N | 2^s-1 tested (N in {255,2047,4095}),
     but the uniform constant over the full divisor lattice (adversarial N where
     a kappa*N-interval could miss many short cosets) is not proved.  Equivalently:
     is the doubling-coset partition of Z/N interval-covering at density kappa
     for every N | 2^s-1?"

THEOREM (covering constant, PROVED here).  Let N be odd, N > 1.  For the doubling
map c -> 2c mod N, every nonzero orbit's MINIMUM element lies in [1,(N-1)/2].
Equivalently Z_2(N,{1..(N-1)/2}) = (Z/N)\\{0}, so d_2(N,{1..R}) = 1 for every
R >= (N-1)/2 (and = 0 when 0 in I).  NO divisor condition is used: this holds for
EVERY odd N, a fortiori for every N | 2^s-1.  kappa = 1/2 is universal and SHARP;
the extremal N (min = (N-1)/2 attained) are EXACTLY the Mersenne N = 2^s-1.

Proof engine (one line).  Let m = min(orbit), orbit of a nonzero c.  If m > N/2
then N < 2m < 2N, so the orbit contains 2m mod N = 2m - N with 0 < 2m - N < m
(since 2m-N < m <=> m < N, and 2m-N > 0 <=> m > N/2), contradicting minimality of
m.  Hence m <= (N-1)/2 (N odd).  This is Route 2 of the covering brief; it
SUPERSEDES the lift/transfer route -- no lifting to 2^s-1 is needed, and no
necklace/bit-rotation structure is used, so the divisor condition N | 2^s-1
disappears.  The mod-2^s-1 necklace argument of #610 (Theorem 3a) is the special
case where doubling is exact s-bit rotation; here the same numeric minimum is
reached with no representative-selection issue.

Consequence for the C5 payment chain.  #545 (gap2_collapse_routing.md) routes the
C5 field-descent cell to the fibre bound p^{d_p(G,I)}; #607
(noncyclic_c5_slope_count.md) proves d_p(G,I) = |G| - |Z_p(G,I)| exactly; #610
(c5_defect_magnitude.md) bounds the magnitude on the deployed families and leaves
this covering constant open.  With this theorem the binary-tower F2 leaf pays
d_2 = 1 = O(1) at half-prefix R >= |G|/2 for ALL odd N -- so #545 + #607 + #610 +
this packet is a complete, unconditional C5 chain on the whole binary-tower cell
at half-prefix depth.  The only residual conditionality is the DEPLOYMENT reading
R >= |G|/2 <=> low code-rate rho <= 1/2 (up to the domain factor n/N), an
audit-level fact carried over unchanged from #610 Rung 5.2 -- not a math gap.

Credit / lineage.  Defect object d_p = |G| - |Z_p|, cyclic Theorem 1, the necklace
argument for N = 2^s-1, and the p=5 dyadic exemplar: DannyExperiments #451
(asymptotic_c9_frobenius_cyclotomic_defect.md), whose section 7 named these
uncovered rows.  Non-cyclic Theorem A / orbit closed form / trivial-Frobenius
floor: PR #607.  C5 routing: PR #545.  Magnitude bound + the OPEN residual this
packet closes: PR #610.

Checks (recomputes every number the note quotes; exit 0 iff ALL pass):
  ENGINE   : the proof's contraction step verified as literal integer arithmetic
             -- every high-half c (c >= (N+1)/2) has 0 < 2c mod N = 2c-N < c, so
             no high-half element is an orbit minimum (exhaustive, odd N).
  ORBIT    : full orbit enumeration -- L(N) := max over nonzero orbits of min(orbit)
             satisfies L(N) <= (N-1)/2 for every odd N in range (0 violations).
  COVER    : INDEPENDENT forward-doubling closure from the prefix {1..R} --
             d_2(N,{1..(N-1)/2}) = 1 for every odd N in range; cross-checks ORBIT
             (d_2 = 1 <=> L(N) <= (N-1)/2).
  EXTREMAL : the extremal set {odd N : L(N) = (N-1)/2} equals EXACTLY the Mersenne
             numbers {2^s-1} up to 1e5; the extremal orbit is orbit((N-1)/2) =
             {N - 2^k}.  (Refutes the brief's 2^t+1 guess.)
  SHARP    : for Mersenne N=2^s-1, prefix {1..(N-1)/2 - 1} leaves d_2 >= 2 -- so
             kappa = 1/2 cannot be lowered universally; kappa_min(N)=L(N)/N -> 1/2.
  DIVISOR  : the OPEN residual verbatim -- for every N | 2^s-1 (N>1, s=2..16),
             d_2(N,{1..(N-1)/2}) = 1; includes #610's tested {255,2047,4095}.
  MATCH610 : reproduces #610's DECAY table at R/N = 0.50 -- d_2/N = 1/N (d_2=1)
             for N in {31,127,255,2047,4095}; and o = ord_N(2).
  NECKLACE : for N=2^s-1, numeric orbit-min == min over the s bit-rotations of the
             s-bit representation (ties the theorem to #610 Theorem 3a).
  NAIVE    : the naive pigeonhole bound "orbit of size m has an element <= N/m" is
             FALSE in general -- documents that the minimum-element argument, not
             pigeonhole, is the correct mechanism.
  DEPLOY   : deployment bridge arithmetic R = n-k = (1-rho)N; rho <= 1/2 =>
             R/N >= 1/2 (up to n/N), carried from #610 Rung 5.2.
  TAMPER   : a deliberately wrong bound (min <= (N-1)/3) MUST fail -- teeth check.

Stdlib only.  Zero-arg.  Runtime ~20 s under `ulimit -v 2097152`.
"""
from __future__ import annotations

import sys

# ---- ranges (chosen so total runtime stays well under 120 s) --------------
FULL = 20001     # exhaustive orbit + cover routes over odd N in [3, FULL]
WIDE = 100001    # fast extremal/census trace over odd N in [3, WIDE]
ENGINE_RANGE = 6001  # literal contraction-step check over odd N in [3, ENGINE_RANGE]

RESULTS: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    RESULTS.append((name, bool(ok), detail))


# ---------------------------------------------------------------------------
# Core primitives (each a distinct code path; no shared caches between routes)
# ---------------------------------------------------------------------------

def orbit_mins(N: int) -> list[int]:
    """Enumerate every nonzero doubling orbit mod N; return each orbit's min.

    Orbits of nonzero c never reach 0 (2 is a unit mod odd N), so they partition
    {1..N-1}.  This is ROUTE A."""
    seen = bytearray(N)
    mins = []
    for c in range(1, N):
        if seen[c]:
            continue
        x = c
        mn = N
        while not seen[x]:
            seen[x] = 1
            if x < mn:
                mn = x
            x = (2 * x) % N
        mins.append(mn)
    return mins


def defect_from_prefix(N: int, R: int) -> int:
    """d_2(N,{1..R}) = N - |Z_2(N,{1..R})| via forward-doubling closure.

    Z_2 = union of orbits meeting the prefix; each orbit is a single cycle, so
    forward doubling from every prefix element sweeps its whole orbit.  This is
    ROUTE B -- independent of orbit_mins."""
    reached = bytearray(N)
    stack = []
    hi = min(R, N - 1)
    for c in range(1, hi + 1):
        if not reached[c]:
            reached[c] = 1
            stack.append(c)
    while stack:
        x = stack.pop()
        y = (2 * x) % N
        if not reached[y]:
            reached[y] = 1
            stack.append(y)
    return N - sum(reached)  # index 0 is never set -> counts the fixed point 0


def is_extremal(N: int) -> bool:
    """True iff L(N) = (N-1)/2, i.e. orbit((N-1)/2) stays entirely >= (N-1)/2.

    Early-stop trace of the single orbit of (N-1)/2 (the only residue that can
    equal (N-1)/2), so this is fast even for large N."""
    h = (N - 1) // 2
    if h == 0:
        return False
    x = (2 * h) % N
    while x != h:
        if x < h:
            return False
        x = (2 * x) % N
    return True


def ord_mod(a: int, N: int) -> int:
    """Multiplicative order of a mod N (assumes gcd(a,N)=1)."""
    o = 1
    x = a % N
    while x != 1:
        x = (x * a) % N
        o += 1
    return o


def divisors(n: int) -> list[int]:
    ds = set()
    i = 1
    while i * i <= n:
        if n % i == 0:
            ds.add(i)
            ds.add(n // i)
        i += 1
    return sorted(ds)


# ---------------------------------------------------------------------------
# ENGINE -- the proof's contraction step as literal integer arithmetic
# ---------------------------------------------------------------------------

def check_engine() -> None:
    bad = None
    for N in range(3, ENGINE_RANGE + 1, 2):
        lo = (N + 1) // 2                 # first high-half residue (N odd)
        for c in range(lo, N):
            d = (2 * c) % N               # doubling
            # proof requires: doubling of a high-half c is 2c-N and lands in (0,c)
            if d != 2 * c - N or not (0 < d < c):
                bad = (N, c, d)
                break
        if bad:
            break
    record(
        "ENGINE.contraction",
        bad is None,
        (f"all high-half c in [3,{ENGINE_RANGE}] map to 2c-N in (0,c); "
         "no high-half residue is an orbit minimum"
         if bad is None else f"FAILED at {bad}"),
    )


# ---------------------------------------------------------------------------
# ORBIT (route A) + COVER (route B), cross-checked; plus census
# ---------------------------------------------------------------------------

def check_orbit_cover_census() -> None:
    viol_orbit = 0
    viol_cover = 0
    disagree = 0
    kmax = 0.0
    kmax_N = 0
    # kappa_min distribution bins (fraction of N in [lo,hi))
    bins = [(0.0, 0.3), (0.3, 0.4), (0.4, 0.45), (0.45, 0.49), (0.49, 0.5)]
    bin_counts = [0] * len(bins)
    top = []  # (kappa_min, N) largest few
    for N in range(3, FULL + 1, 2):
        h = (N - 1) // 2
        # route A
        mins = orbit_mins(N)
        L = max(mins)
        if L > h:
            viol_orbit += 1
        # route B, independent
        d2 = defect_from_prefix(N, h)
        if d2 != 1:
            viol_cover += 1
        # cross-consistency: d2==1 iff L<=h (always true here); flag mismatch
        if (d2 == 1) != (L <= h):
            disagree += 1
        km = L / N
        if km > kmax:
            kmax, kmax_N = km, N
        for i, (a, b) in enumerate(bins):
            if a <= km < b:
                bin_counts[i] += 1
                break
        top.append((km, N))
    top.sort(reverse=True)
    record(
        "ORBIT.min_le_half",
        viol_orbit == 0,
        f"L(N) <= (N-1)/2 for all odd N in [3,{FULL}]: {viol_orbit} violations",
    )
    record(
        "COVER.defect_one",
        viol_cover == 0,
        f"d_2(N,{{1..(N-1)/2}}) = 1 for all odd N in [3,{FULL}]: {viol_cover} violations",
    )
    record(
        "COVER.cross_consistent",
        disagree == 0,
        f"route A (orbit-min) and route B (prefix closure) agree everywhere: {disagree} mismatches",
    )
    record(
        "CENSUS.kappa_below_half",
        kmax < 0.5,
        (f"max kappa_min = {kmax:.6f} at N={kmax_N} (= (N-1)/(2N) < 1/2); "
         f"top: {[(round(k,5),n) for k,n in top[:5]]}; "
         f"bins {[b for b in zip([b for b in bins], bin_counts)]}"),
    )


# ---------------------------------------------------------------------------
# EXTREMAL -- extremal set == Mersenne, and the extremal orbit shape
# ---------------------------------------------------------------------------

def check_extremal() -> None:
    ext = [N for N in range(3, WIDE + 1, 2) if is_extremal(N)]
    mers = []
    v = 3
    while v <= WIDE:
        mers.append(v)
        v = 2 * v + 1
    record(
        "EXTREMAL.equals_mersenne",
        ext == mers,
        f"extremal set up to {WIDE} = {ext} == Mersenne {{2^s-1}} : {ext == mers}",
    )
    # shape of the extremal orbit for N=2^s-1: orbit((N-1)/2) = {N - 2^k}
    shape_ok = True
    detail = ""
    for s in range(2, 15):
        N = 2 ** s - 1
        h = (N - 1) // 2
        orb = set()
        x = h
        while x not in orb:
            orb.add(x)
            x = (2 * x) % N
        expect = {(N - (1 << k)) % N for k in range(s)}  # {N-2^k}, and N-2^0=N-1 etc.
        # (N-1)/2 = N - 2^{s-1}; so expect already contains h at k=s-1
        if orb != expect:
            shape_ok = False
            detail = f"s={s}: orbit {sorted(orb)} != {{N-2^k}} {sorted(expect)}"
            break
    record(
        "EXTREMAL.orbit_shape",
        shape_ok,
        "for N=2^s-1, orbit((N-1)/2) = {N-2^k : k=0..s-1}, min = (N-1)/2"
        if shape_ok else detail,
    )


# ---------------------------------------------------------------------------
# SHARP -- kappa=1/2 cannot be lowered (Mersenne need the full half-prefix)
# ---------------------------------------------------------------------------

def check_sharp() -> None:
    ok = True
    detail = ""
    for s in range(3, 15):
        N = 2 ** s - 1
        h = (N - 1) // 2
        d_at_half = defect_from_prefix(N, h)         # should be 1
        d_below = defect_from_prefix(N, h - 1)       # should be >= 2
        if not (d_at_half == 1 and d_below >= 2):
            ok = False
            detail = f"s={s} N={N}: d(R=h)={d_at_half}, d(R=h-1)={d_below}"
            break
    record(
        "SHARP.threshold",
        ok,
        "Mersenne N=2^s-1: d_2=1 at R=(N-1)/2 but d_2>=2 at R=(N-1)/2 - 1 "
        "(so kappa=1/2 is sharp)" if ok else detail,
    )


# ---------------------------------------------------------------------------
# DIVISOR -- the OPEN residual verbatim: every N | 2^s-1
# ---------------------------------------------------------------------------

def check_divisor_family() -> None:
    tested = set()
    bad = None
    for s in range(2, 17):
        M = 2 ** s - 1
        for N in divisors(M):
            if N <= 1:
                continue
            tested.add(N)
            h = (N - 1) // 2
            if defect_from_prefix(N, h) != 1:
                bad = (s, N)
                break
        if bad:
            break
    have610 = {255, 2047, 4095}.issubset(tested)
    record(
        "DIVISOR.every_N_dividing_2s1",
        bad is None and have610,
        (f"d_2=1 at R=(N-1)/2 for all {len(tested)} distinct N | 2^s-1 (s=2..16); "
         f"includes #610's {{255,2047,4095}}: {have610}"
         if bad is None else f"FAILED at s,N={bad}"),
    )


# ---------------------------------------------------------------------------
# MATCH610 -- reproduce #610's DECAY row at R/N = 0.50
# ---------------------------------------------------------------------------

def min_nonzero_orbit_size(N: int) -> int:
    """Smallest size among the nonzero doubling orbits mod N."""
    seen = bytearray(N)
    best = N
    for c in range(1, N):
        if seen[c]:
            continue
        x = c
        sz = 0
        while not seen[x]:
            seen[x] = 1
            sz += 1
            x = (2 * x) % N
        if sz < best:
            best = sz
    return best


def check_match_610() -> None:
    # #610 DECAY table, column R/N = 0.50 (verbatim PRINTED values, 3-dp):
    printed = {31: 0.032, 127: 0.008, 255: 0.004, 2047: 0.001, 4095: 0.000}
    ords = {31: 5, 127: 7, 255: 8, 2047: 11, 4095: 12}
    ok = True
    lines = []
    for N in (31, 127, 255, 2047, 4095):
        R = round(0.50 * N)
        d2 = defect_from_prefix(N, R)          # our theorem forces this to be 1
        o = ord_mod(2, N)
        msz = min_nonzero_orbit_size(N)        # next defect jump is by >= msz
        # #610's printed value f: f*N must be below the second-smallest possible
        # defect (1 + msz), so it can ONLY encode d2 = 1 -- rigorous reconciliation
        # of #610's coarse 3-dp print with the exact d2 = 1 this packet proves.
        forced_one = printed[N] * N < 1 + msz
        # for the high-resolution N, the print equals round(1/N, 3) exactly
        clean = (round(1.0 / N, 3) == printed[N]) if N <= 255 else True
        lines.append(f"N={N} o={o} d2={d2} 1/N={1.0/N:.5f} (#610 print {printed[N]}, "
                     f"min-orbit={msz}, forces d2=1: {forced_one})")
        if not (d2 == 1 and o == ords[N] and forced_one and clean):
            ok = False
    record(
        "MATCH610.decay_half",
        ok,
        "; ".join(lines) + "  [#610's 0.001/0.000 for N=2047/4095 are display-"
        "roundings of 1/N; d2=2 is impossible (defect jumps by orbit size), so "
        "every #610 DECAY entry at R/N=0.5 encodes exactly d2=1 = our theorem]",
    )


# ---------------------------------------------------------------------------
# NECKLACE -- tie to #610 Theorem 3a for N=2^s-1 (doubling = bit rotation)
# ---------------------------------------------------------------------------

def check_necklace() -> None:
    ok = True
    detail = ""
    for s in range(2, 14):
        N = 2 ** s - 1
        mask = N
        for c in range(1, N):
            # numeric orbit min
            x = c
            mn = c
            first = c
            while True:
                x = (2 * x) % N
                if x == first:
                    break
                if x < mn:
                    mn = x
            # min over the s cyclic bit-rotations of the s-bit rep of c
            rot_min = c
            r = c
            for _ in range(s):
                r = ((r << 1) & mask) | (r >> (s - 1))  # rotate-left s-bit
                if r < rot_min:
                    rot_min = r
            if mn != rot_min:
                ok = False
                detail = f"s={s} c={c}: orbit-min {mn} != rotation-min {rot_min}"
                break
        if not ok:
            break
    record(
        "NECKLACE.min_is_rotation_min",
        ok,
        "for N=2^s-1, numeric orbit-min == min bit-rotation (doubling = s-bit "
        "rotation), matching #610 Theorem 3a" if ok else detail,
    )


# ---------------------------------------------------------------------------
# NAIVE -- the naive pigeonhole "min <= N/m" is FALSE in general
# ---------------------------------------------------------------------------

def check_naive_false() -> None:
    # exhibit an orbit of size m whose minimum exceeds N/m
    witnesses = []
    for N in range(3, 200, 2):
        seen = bytearray(N)
        for c in range(1, N):
            if seen[c]:
                continue
            orb = []
            x = c
            while not seen[x]:
                seen[x] = 1
                orb.append(x)
                x = (2 * x) % N
            m = len(orb)
            mn = min(orb)
            if mn * m > N:  # min > N/m
                witnesses.append((N, sorted(orb), m, round(N / m, 2), mn))
    record(
        "NAIVE.pigeonhole_false",
        len(witnesses) > 0,
        (f"naive 'min <= N/m' is FALSE: e.g. {witnesses[0]} has min>{witnesses[0][3]}"
         f" ({len(witnesses)} witnesses up to N=199); min-element argument is the "
         "correct mechanism" if witnesses else "no witness found -- unexpected"),
    )


# ---------------------------------------------------------------------------
# DEPLOY -- deployment-bridge arithmetic, carried from #610 Rung 5.2
# ---------------------------------------------------------------------------

def check_deploy() -> None:
    # R = n-k = (1-rho)*N  (up to n/N domain factor).  rho<=1/2 => R/N>=1/2.
    ok = True
    lines = []
    for rho_num, rho_den in [(1, 2), (1, 4), (1, 8), (3, 4)]:
        rho = rho_num / rho_den
        rN = 1 - rho          # R/N at domain factor n/N = 1
        low_rate = rho <= 0.5
        reaches_half = rN >= 0.5 - 1e-12
        lines.append(f"rho={rho_num}/{rho_den}: R/N={rN:.3f} low-rate={low_rate} "
                     f"R/N>=1/2={reaches_half}")
        if low_rate != reaches_half:
            ok = False
    record(
        "DEPLOY.rate_bridge",
        ok,
        "; ".join(lines) + "  [audit reading from #610 Rung 5.2; needs each row's (N,R)]",
    )


# ---------------------------------------------------------------------------
# TAMPER -- teeth
# ---------------------------------------------------------------------------

def check_tamper() -> None:
    # the WRONG bound "every orbit min <= (N-1)/3" must be violated somewhere
    found_viol = False
    for N in range(3, 500, 2):
        for mn in orbit_mins(N):
            if mn > (N - 1) // 3:
                found_viol = True
                break
        if found_viol:
            break
    record(
        "TAMPER.wrong_bound_fails",
        found_viol,
        "the false bound 'min <= (N-1)/3' is correctly violated (checks have teeth)"
        if found_viol else "TAMPER did not trip -- checks are vacuous!",
    )


# ---------------------------------------------------------------------------

def main() -> int:
    check_engine()
    check_orbit_cover_census()
    check_extremal()
    check_sharp()
    check_divisor_family()
    check_match_610()
    check_necklace()
    check_naive_false()
    check_deploy()
    check_tamper()

    npass = sum(1 for _, ok, _ in RESULTS if ok)
    ntot = len(RESULTS)
    width = max(len(n) for n, _, _ in RESULTS)
    print("=" * 72)
    print("verify_c5_covering_constant.py  --  general-divisor covering constant")
    print("=" * 72)
    for name, ok, detail in RESULTS:
        tag = "PASS" if ok else "FAIL"
        print(f"[{tag}] {name.ljust(width)}  {detail}")
    print("-" * 72)
    print(f"{npass}/{ntot} checks pass")
    if npass == ntot:
        print("ALL PASS -- covering constant CLOSED: d_2=1 at R>=N/2 for every odd N; "
              "kappa=1/2 universal and sharp (extremal N = 2^s-1).")
        return 0
    print("FAILURES PRESENT")
    return 1


if __name__ == "__main__":
    sys.exit(main())
