# Lower reserve, deep-remainder wall: atlas preserved, domination theorem retired

**Hard input:** 5 (lower reserve / unsafe-side comparison).

**Status:** `PROVED / FIXED / COUNTEREXAMPLE`. The occupancy-atlas exhaustion,
constant complete-support count, degree-`c` interlace identity, and absence of
a clean quotient-coordinate slot in the strict-deep regime remain proved. The
former **Theorem DR** and its conclusion that the field-drop route is dead are
**RETIRED**.

**Audit disposition.** PR #699 attempted to localize the strict-deep case
`w<r` to a partial-occupancy atlas. This note built that atlas, but then made an
invalid inference:

```text
no clean quotient-coordinate slot
    does not imply
the joint prefix image is the Cartesian space B^w.
```

DannyExperiments #714 supplies the exact obstruction. For each fixed remainder
label, multiplication by the reciprocal remainder locator is a unit in the
truncated prefix ring, so it preserves the descended quotient image. Summing
over labels cancels the label count in the image-normalized average. The strict-
deep `F_169` cell has a guaranteed list `6` while the ambient identity
pigeonhole floor is `1`. This refutes the finite domination claim and the
load-bearing implication used by the purported asymptotic theorem. The atlas
survives; the domination theorem does not.

Target: `experimental/asymptotic_rs_mca_frontiers.tex` (read at `ea4eb07`).
Attacks the deep-remainder residual of route **O5c** of hard input 5, scoped by
the coverage audit **#693** (`lower_reserve_unsafe_side_coverage_audit.md`,
sections 3--4) and the wall localisation of **#699**
(`lower_reserve_o5c_profile_lists.md`, section 5).

**Sources audited and consumed:**
- **#699** — `lower_reserve_o5c_profile_lists.md`: the O5c payment for the
  quotient / Euclidean-remainder / Chebyshev classes, the QR4 varying-summand
  observation in its stated `r<c` range, and the wall statement audited here.
- **#693** — lower-reserve / unsafe-side route audit: the O5c/O7 decomposition
  and the "any larger ... remainder-profile list" open statement.
- **#714** — `deep_remainder_partial_occupancy_counterexample.md`: the
  label-factored joint-image theorem, strict-deep `F_169` counterexample, and
  square-tower profile-floor exponent used to retire Theorem DR.

Also consumes the in-paper theorems `prop:simple-pole-lower` (L6180),
`thm:collision-aware-pole` (4.2, L1997), `prop:exact-prefix-list` (4.1, L1965),
`prop:prefix-rigidity-full` (4.4, L2044),
`thm:exact-quotient-remainder-normal-form` (QR2/QR4, L3456),
`prop:complete-support-factorization` (L3577), and
`thm:exact-partial-occupancy` (PO1/PO2, L3608).

**Verifier:** `experimental/scripts/verify_lower_reserve_deep_remainder.py`
-> `RESULT: PASS 44/44` (`--check`), `RESULT: PASS 10/10`
(`--tamper-selftest`), plus `certificate check: PASS`, under normal and
optimized Python, stdlib only. It exhaustively recomputes the occupancy atlas
over `F_25` (square fold, `c=2`) and `F_13` (cube fold, `c=3`), the degree-`c`
interlace and field-drop alphabet contrast over `F_25`, and the #714
contradiction arithmetic over `F_169`. Mode `--check` byte-compares that result
with the deterministic frozen JSON certificate without writing; only explicit
`--write` regenerates
`experimental/data/certificates/lower-reserve-deep-remainder/deep_remainder_atlas.json`.

---

## 1. The obligation, and what a partial-occupancy atlas must provide

`prop:simple-pole-lower` ("Exact unsafe test", L6180) certifies `a_n` unsafe from
any list of `L` distinct dimension-`(k_n+1)` codewords agreeing on `>= a_n`
points, via the collision-aware pole `M(L)` (4.2) and the challenge average
`P = ceil((|Gamma_n|/q_n) M(L))` (L6201--6208). Its last sentence (L6196--6198)
allows `L_n` "replaced by any larger identity, quotient, Chebyshev, or
remainder-profile list proved for the dimension-`(k_n+1)` code."

**The list is a prefix fiber** (`prop:exact-prefix-list`, 4.1): for a prefix value
`z in B_n^w` (`w = a_n - k_n - 1`), the codewords agreeing with `U_z` on `>= a_n`
points are **exactly** `{U_z - Q_S : pref_w(Q_S) = z}`. So a profile-list of proved
size `>= L` is a pigeonhole `max_z #{S in profile : pref_w(Q_S) = z} >= L`. To beat
the identity floor `L_id = ceil(binom(n,a) |B|^{-w})` the pigeonhole must run over
a **smaller alphabet than `B^w`** — this is the **field drop**: the quotient
profile pigeonholes the depth-`d` quotient coefficients `v_1(E),...,v_d(E) in
eta^j B_phi` (a proper subfield coset), giving `L_quot = ceil(binom(N-|phi(R)|,m)
|B_phi|^{-d})`, `N = n/c`, `m = (a-r)/c`, `d = floor(w/c)`.

**The regimes the old wall conflated.** QR2/QR4 assumes `0<=r<c`. In its
`w<r` case one necessarily has `w<c`, so `E` is invisible and the exact
prefix fiber is the remainder-prefix sum
`sum_R binom(N-|phi(R)|,m)`. Its summands can vary with `|phi(R)|`, but no
degree-`c` quotient coordinate is visible.

The arbitrary partial-occupancy decomposition separately permits `r>=c`.
There QR5 remains valid and the degree-`c` interlace begins: `p_c(R)` and
`v_1(E)` collide. QR4's fixed-prefix formula does **not** extend to this
regime. Thus #699's identification of `w<r` with `r>=c`, and the old atlas
note's use of both QR4 factorization and visible interlace in one strict-deep
cell, were invalid. What survives across the regimes is the occupancy
disintegration, the constant admissible-`E` count per partial label, and the
QR5 identity.

**Stated exactly, a partial-occupancy atlas for this obligation must supply:**
1. **Cells.** A finite decomposition of the deep-remainder `a_n`-supports indexed
   by an occupancy pattern (which `phi`-fibers are complete, which are partially
   hit, by how much).
2. **Index set.** A reorganisation of the complete-support count
   `sum_R binom(N-|phi(R)|,m)` in which the summand is **constant** on each
   cell, so the cell cardinality factors by partial label.
3. **Per-cell inequality.** For each cell, a lower bound on the largest depth-`w`
   prefix fiber inside the cell that **runs over a subfield alphabet** (carries a
   field drop), so that it converts through the collision-aware pole the way
   `#699`'s single-pigeonhole quotient list did.
4. **Exhaustion.** A proof the cells tile `binom(D_n, a_n)`.

Requirements 1, 2, 4 are met by the atlas below. The original note claimed
requirement 3 was impossible because no single quotient-coordinate slot stays
clean. Section 3 preserves that coordinate statement but explains why it does
not decide the joint image; #714 supplies requirement 3 by label factoring.

---

## 2. The atlas, BUILT: occupancy cells and constant support count

The cell index is exactly `thm:exact-partial-occupancy` (PO1/PO2, L3608--3644).
With `D = D_0 sqcup X`, `|X| = b`, `phi : D_0 ->> Q` of complete fibers of size
`c`, `N = |Q|`, the occupancy of `S subseteq D` is
`lambda_phi(S) = (t, m, p, r)`: `t = |S cap X|` exceptional points, `m` complete
fibers, `p` partially-hit fibers, `r` selected points in those partial fibers.

**Proposition A (exhaustion; PROVED, verbatim PO1/PO2).** The cells
`Omega_{t,m,p,r}` partition `binom(D, a)`, with exact count
`|Omega_{t,m,p,r}| = binom(b,t) binom(N,p) binom(N-p,m) [x^r]((1+x)^c - 1 - x^c)^p`
and add-back `sum_{t+cm+r=a} |Omega_{t,m,p,r}| = binom(b+cN, a)`.

*Verified exhaustively* (verifier group A): over `F_25` (square fold, `c=2`,
`b=0`, `N=4`, so `(1+x)^2-1-x^2 = 2x`) PO1 is exact on every cell and PO2 holds
for `a = 0..8`; the `a=4` partition is `(0,0,4,4)->16`, `(0,1,2,2)->48`,
`(0,2,0,0)->6`, summing to `70 = binom(8,4)`. Over `F_13` (cube fold, `c=3`,
`N=4`, `(1+x)^3-1-x^3 = 3x(1+x)`) PO1/PO2 hold for `a = 0..7`, exercising the
`p < r` cells (a partial fiber may hold `2` of `3` points) that `c=2` never
produces.

**Proposition B (constant support count; PROVED).** For every
`S in Omega_{t,m,p,r}`, the partial part `R(S)` has
`|phi(R(S))|=p`, a cell constant. For each fixed partial label `(T,R)`, the
number of admissible complete-fiber sets is therefore

```text
#{E subseteq Q setminus phi(R): |E|=m}=binom(N-p,m).
```

*Proof.* A fiber lies in `E(S)` iff all `c` of its points are in `S`; the partial
fibers are exactly the `p` fibers meeting `R(S)`, so `|phi(R(S))| = p` by
definition of the cell. Fixing the partial-fiber set fixes `phi(R)`, hence
`E in binom(Q setminus phi(R), m)` ranges over `binom(N-p, m)` sets independently
of the label. This proves the cell-size factorization in Proposition A. It
does **not** factor a fixed-prefix fiber when `r>=c` and `w>=c`, because then
the visible quotient coefficient `v_1(E)` varies with `E`. `QED`

This **stratifies the varying support count** `#699` flagged: its three values
`binom(12-|phi(R)|,4) in {495, 330, 210}` correspond to three different
occupancy types (`p in {0,1,2}`), not a varying complete-support factor within
one cell.  The corrected fixed-`r=2,c=3` QR4 example uses only the realizable
`p in {1,2}` weights `330,210`; `p=0` is impossible there.  Verifier group B
reproduces the cross-type counts and confirms
`|phi(R)| = p = 2` is constant across all 48 supports of the `F_25` cell
`(0,1,2,2)`.)

So the atlas assembles: cells and exhaustion (Proposition A), plus a constant
admissible-`E` count per partial label (Proposition B). The per-cell prefix
inequality is a separate image question, supplied by #714 below.

---

## 3. The interlace is a coordinate route cut, not an image theorem

Take reciprocal polynomials (`A^vee(Z)=Z^{deg A}A(Z^{-1})`) and
`Phi(Z)=Z^c phi(Z^{-1})`. The exact QR5 identity is

```text
Q_S^vee(Z) = P_R^vee(Z)
  (Phi(Z)^m + sum_{j=1}^m v_j(E) Z^{cj} Phi(Z)^{m-j}).
```

A quotient-coordinate slot at degree `jc` is *clean* when `r<jc<=w`; then the
remainder polynomial cannot contribute at that degree and the quotient
coefficient can be read triangularly in its descended `B_phi` coset. Hence

```text
w<r  =>  there is no clean quotient-coordinate slot.
```

This clean-slot lemma is correct and remains useful: it rules out the naive
coordinate-by-coordinate extraction used in the Euclidean-remainder case.
The coefficient at degree `jc<=w<r` is interlaced with a remainder coefficient.
The `F_25` toy calculation confirms that the clean quotient slot takes `5`
values while the interlaced slot takes `21` values.

The old proof then made an invalid jump. Coordinatewise variation, even outside
all proper subfield cosets, does not determine the size of the **joint** prefix
image and does not make that image the Cartesian space `B^w`. Proposition
`prop:prefix-rigidity-full` supplies an upper bound on fiber size; it does not
supply the missing lower bound `|image|=|B|^w(1-o(1))`.

For a fixed remainder label `u=(T,R)`, put

```text
U_u(X)=Q_T(X)P_R(X).
```

The reciprocal `U_u^vee` has constant coefficient one, so multiplication by it
is an automorphism of `B[Z]/(Z^{w+1})`. Modulo `Z^{w+1}`, the bracket in QR5
depends only on

```text
v_1(E),...,v_d(E),   d=min(m,floor(w/c)),
```

which have at most `|B_phi|^d` values. Thus every fixed label contributes at
most `|B_phi|^d` prefixes even when no individual coordinate is clean. With

```text
J_{t,p,r}=binom(b,t) binom(N,p)
            [x^r]((1+x)^c-1-x^c)^p,
```

the corrected joint-image bound is

```text
|Phi_w(Omega_{t,m,p,r})| <= J_{t,p,r}|B_phi|^d,
max_z |Omega intersect Phi_w^{-1}(z)|
  >= ceil(binom(N-p,m)/|B_phi|^d).
```

The label count cancels in the image-normalized average. This is a genuine
field-drop list bound in the strict-deep regime; it does not require a clean
coordinate slot.

---

## 4. Exact counterexample to the retired domination theorem

Use the square fold over

```text
B=F_169=F_13[T]/(T^2-2),
theta=2+T, H=<theta^7>, D=theta H, phi(x)=x^2.
```

Here `n=24`, `N=12`, `c=2`, and `B_phi=F_13`. Take

```text
(n,a,k,w,c,m,p,r)=(24,12,8,3,2,4,4,4).
```

This is strict-deep because `w=3<r=4`. Exact arithmetic gives

```text
J=binom(12,4)2^4=7920,
|Omega|=7920 binom(8,4)=554400,
d=1,
|Phi_3(Omega)| <= 7920*13=102960,
guaranteed list >= ceil(binom(8,4)/13)=6,
identity floor = ceil(binom(24,12)/169^3)=1.
```

The exhaustive verifier strengthens the image bound to

```text
realized image = 86320,
maximum prefix fiber = 20,
average fiber = 6930/1079.
```

Therefore a strict-deep canonical cell has a proved field-drop list six times
the identity pigeonhole floor. This refutes all of the old Theorem DR's
load-bearing conclusions:

- absence of a clean slot does not make the effective prefix image `B^w`;
- the strict-deep field-drop route is not dead;
- deep profile lists need not be identity-dominated; and
- prefix rigidity does not repair the implication.

The finite row's tangent floor is `13`, so this correction does not move that
row's final lower reserve or any deployed threshold.

---

## 5. Corrected status of O5c

| component | corrected status |
|---|---|
| occupancy cells and PO1/PO2 exhaustion | **PROVED** |
| constant admissible-`E` count and cell-size factorization | **PROVED** |
| degree-`c` interlace identity | **PROVED** |
| no clean quotient-coordinate slot when `w<r` | **PROVED route cut** |
| no clean slot implies full joint image | **COUNTEREXAMPLE / RETIRED** |
| Theorem DR: strict-deep field-drop route dead | **COUNTEREXAMPLE / RETIRED** |
| label-factored image bound and list floor | **PROVED** (#714) |
| strict-deep `F_169` list `6` vs identity floor `1` | **PROVED finite** |
| general natural-scale upper payment / distinct-ray compiler | **OPEN** |

The square-tower construction in #714 also gives positive profile-floor
exponents for explicit strict-deep families. This is lower-side list progress,
not a primitive-residual upper payment. Canonical partial-occupancy profiles
are removed before the primitive residual, and a sufficient PEU comparison
that drops their natural cell scale is invalid.

The remaining useful question is not whether label-factored field drop exists;
it does. It is whether the resulting natural-scale cells receive the required
upper/profile-envelope and distinct-slope payments in every relevant row.

---

## 6. Per-claim labels and nonclaims

**Preserved:** atlas exhaustion, constant support count and cell-size
factorization, QR5 interlace, and the clean-coordinate route cut are `PROVED`.

**Fixed:** the joint-image inference, Theorem DR, the field-drop-dead verdict,
and the identity-domination corollary are `COUNTEREXAMPLE` and retired. The
correct label-factored theorem and its strict-deep witness are `PROVED`.

This note does not claim:

- a primitive-PEU counterexample;
- a source-valid distinct-ray or residual-ray compiler;
- catalogue exhaustivity or line uniformity;
- a deployed KoalaBear or M31 threshold crossing;
- Grand MCA, Grand List, or either prize question; or
- any edit or promotion to the paper TeX.

Credit for the theorem and counterexample that force this retirement belongs
to DannyExperiments, PR #714. This correction changes the status bookkeeping,
not that result's authorship.

---

## 7. Replay

```bash
python3 experimental/scripts/verify_lower_reserve_deep_remainder.py --check
python3 -O experimental/scripts/verify_lower_reserve_deep_remainder.py --check
python3 experimental/scripts/verify_lower_reserve_deep_remainder.py --tamper-selftest
python3 -O experimental/scripts/verify_lower_reserve_deep_remainder.py --tamper-selftest
python3 experimental/scripts/verify_deep_remainder_partial_occupancy_counterexample.py --check
python3 -O experimental/scripts/verify_deep_remainder_partial_occupancy_counterexample.py --check
python3 experimental/scripts/verify_deep_remainder_partial_occupancy_counterexample.py --tamper-selftest
python3 -O experimental/scripts/verify_deep_remainder_partial_occupancy_counterexample.py --tamper-selftest
```

Both verifiers are stdlib-only and fail closed under optimized mode. The first
checks the deterministic frozen certificate byte-for-byte without writing it.
Its explicit `--write` mode is reserved for reviewed regeneration under
`experimental/data/certificates/lower-reserve-deep-remainder/`.
