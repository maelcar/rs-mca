# Ray-compiler balanced-core input: a field-independent higher-dimensional transverse-secant bound

**Lane:** hard input #3 of `AGENTS.md` -- the residual ray compiler for
higher-dimensional balanced cores. Direct attack (not an audit).
**Target file:** `experimental/asymptotic_rs_mca_frontiers.tex` (worktree tip
`4e3c4ee`). **No `.tex`/`.pdf` edited.**
**Verifier:** `experimental/scripts/verify_ray_compiler_core.py` (stdlib-only,
zero-arg, `RESULT: PASS (173 checks)`; recomputes every gated number below).

**Highest rung reached: 3 (a general infinite subclass with explicit
constants). Verdict: `PROVED`** for the per-chart higher-dimensional
transverse-secant bound, plus a `PROVED` conditional discharge of `(RC)` on
bounded-kernel balanced cores, plus a `NULL` falsifier (no violation; bound
found sharp).

Credit: this lane builds on the audits of the same gap by **LegaSage**
(`#523`, `#514`). #523 modelled the higher-dim core by a linear form
`gamma = c . p` on an abstract grid `F_q^d` and verdicted `NO ISSUE` while
explicitly flagging that "the higher-dim balanced-core ray map may be nonlinear;
needs proved RC not linear rank only"; #514 checked the abstract bipartite
double-count `|Z| H <= J |P|`. Both are statement/proxy-level audits. This lane
differs in scope: it is a **direct proof in the actual RS witness geometry**
(the weighted rational-normal-curve secant configuration), which yields a
field-independent count the linear-form proxy (image size exactly `q`) cannot
express.

---

## 1. Anatomy (rung 1) -- exact extraction

### 1.1 The `(RC)` hypothesis (`hyp:ray-compiler`, L6033-6057; `eq:ray-compiler`, L6051)

For every received line and primitive residual profile `lambda`, with
`Z^o_lambda` the actual first-match set of unpaid bad slopes,
`P_lambda = {(A,B) in (Omega^o_lambda)^2 : Phi_lambda(A) = Phi_lambda(B)}`,
and `m_lambda = |Omega^o_lambda| = sum_s Q_lambda(s)`, the row satisfies `(RC)`
on the profile if **either** the direct bound

```
        |Z^o_lambda|  <=  e^{o(n)} (1 + Nbar_lambda)                      (RC-direct)
```

holds, **or** there are an incidence `I_lambda subset Z^o_lambda x P_lambda`
and numbers `H_lambda, J_lambda >= 1` with

```
   deg_{I}(gamma) >= H_lambda,   deg_{I}(A,B) <= J_lambda,
   J_lambda * m_lambda / H_lambda  =  e^{o(n)}.                            (RC-incidence)
```

`(RC)` is the paper's **sole** `\begin{hypothesis}` environment (verified in the
#524 delta-audit and re-gated here).

**Double-count anatomy (checked).** `(RC-incidence)` implies `(RC-direct)`
because `Nbar_lambda = |Omega^o_lambda| / L_lambda` is the average fiber size
(`def` at L855; `L_lambda = |Phi_lambda(Omega^o_lambda)|`). For equal fibers
`|P_lambda| = sum_y f_y^2 ~ L_lambda * Nbar^2 = m_lambda * Nbar_lambda`, so the
bipartite double count `|Z^o| H <= |I| <= J |P|` gives
`|Z^o| <= J |P|/H = (J m/H) Nbar = e^{o(n)} Nbar_lambda`. So the
`J m / H = e^{o(n)}` display is exactly the condition that turns the collision
mass into the direct slope bound. (This is the sharp inequality the task names.)

### 1.2 The concrete open object (`rem:balanced-core-exhaustion`, L4762; `def` L4526)

A **balanced-core chart** (L4526) is a parameter family of equal-degree monic
residual locator pairs with a common prefix, after all common factors, quotient
pullbacks, planted blocks, and certified rank degeneracies are removed, "whose
remaining moving coefficient space has projective dimension greater than one."
`rem:balanced-core-exhaustion` says the one-pencil moving-root bound
(`prop:split-pencil-payment`, L4741, `|Z| <= floor((n-g)/h)`) "neither covers a
higher-dimensional coefficient family nor proves that such a family decomposes
into subexponentially many pencils. That structural statement is part of `(RC)`
or must be established by a direct ray count." L1088-1090 names the missing
object precisely: **"a higher-dimensional transverse-secant bound beyond the
bounded-kernel, single-circuit, curve, pencil, and deep-quotient cases proved
here."** This lane supplies exactly that bound.

### 1.3 The exact-transverse-secant model and the proved base case

`thm:syndrome-secant-exact` (L1606, `eq:transverse-secant-count` L1615) makes the
bad-slope problem **exactly** a transverse line-secant incidence:
`B_C^{MCA}(a) = max_{y_0,y_1} Theta_t(y_0,y_1)` where `t = n-a` and

```
 Theta_t(y0,y1) = #{ gamma in F : exists E subset D, |E| <= t,
                     y0 + gamma y1 in V_E,  {y0,y1} not subset V_E }.
```

Here `V_E = span{ h_x : x in E }`, `h_x = (1, x, ..., x^{R-1})` are the `R = n-k`
parity columns (points of the weighted rational normal curve), `R = ` redundancy.
For a **fixed chart** `U subset D`, write `Theta_t^U` for the same count with
`E subset U`. The paper's proved per-chart cases:

| chart type | label | bound | field |
|---|---|---|---|
| independent union `\|U\|<=R` | `lem:independent-union-rays` L1646 | `t+1` | indep. |
| single circuit `\|U\|=R+1` (`kappa=1`) | `thm:single-mds-circuit-ray` L1734 | `C(R+1,2)` | **independent** |
| bounded residual kernel, general `kappa` | `thm:bounded-residual-kernel-ray` L1679 | `(t+1) \|F\|^{kappa(U)}` | **DEPENDENT** |

with `kappa(U) = dim ker H_U = max{0, |U|-R}`.

### 1.4 What the single-circuit proof uses that fails at `kappa >= 2` (checked)

The `kappa=1` proof (L1747-1774): the circuit kernel is generated by **one**
vector `z` with **full support**; each error is `e_gamma = b0 + gamma b1 + c_gamma z`
with `c_gamma` a **scalar**; a coordinate `x` vanishes iff `c_gamma = f_x(gamma)`
with `f_x` **affine in gamma**; transversality forces `>= 2` vanishing
coordinates, so two affine functions `f_x = f_{x'}` agree at `<= 1` slope; charge
each slope to an unordered **pair** => `|Z| <= C(R+1,2)`.

At `kappa >= 2` the kernel `ker H_U` has dimension `kappa`, `c_gamma in F^kappa`,
and a single vanishing coordinate is **one linear equation in `kappa` unknowns**,
not a determination of `c_gamma`. The naive kernel sum then loses a factor
`|F|` per extra kernel dimension -- this is exactly why
`thm:bounded-residual-kernel-ray` carries `(t+1)|F|^{kappa}`, which is useless
in the asymptotic regime where `|F| = q` is exponentially large in `n`. The open
problem is to remove the field factor for `kappa >= 2`.

---

## 2. Main result (rungs 2 + 3): a field-independent transverse-secant bound

**Theorem (higher-dimensional transverse-secant bound).** `[PROVED]`
Let `H` be a Reed-Solomon (Vandermonde/MDS) parity check of redundancy `R` over
any field `F`. Let `U subset D` with `|U| = R + kappa`, so
`kappa = dim ker H_U >= 1`. Let `0 <= t <= R-1`, and fix a syndrome line
`y0 + gamma y1`. Then the number of finite transverse slopes admitting a witness
`E_gamma subset U` with `|E_gamma| <= t` satisfies

```
        |Z|  <=  C(R + kappa, kappa + 1)             (field-INDEPENDENT).
```

- `kappa=1` recovers `thm:single-mds-circuit-ray` exactly: `C(R+1,2)`.
- The `|F|^kappa` of `thm:bounded-residual-kernel-ray` is **eliminated**: the
  chart pays a field-free polynomial in `R+kappa`.

**Proof.** `[PROVED -- re-derive at PI review; computationally validated end to
end, group E of the verifier]`

If `|Z| <= 1` the bound is trivial. Otherwise two line points lie in `V_U`, so
`y0, y1 in V_U`; fix lifts `b0, b1 in F^U` with `H_U b_i = y_i`. Fix a basis
`z_1, ..., z_kappa` of `ker H_U`. Because `H` is MDS, any `R` columns are
independent, so `H_U` has rank `R` and `ker H_U` is an `[R+kappa, kappa, R+1]`
MDS code: every nonzero kernel vector has weight `>= R+1` (vanishes on `<= kappa-1`
coordinates), and any `kappa` columns of the generator `Z = [z_1;...;z_kappa]`
are independent.

For each `gamma in Z`, some `e_gamma in F^U` supported on `E_gamma` has
`H_U e_gamma = y0 + gamma y1`, hence
`e_gamma = b0 + gamma b1 + sum_i c_gamma^{(i)} z_i` for some `c_gamma in F^kappa`.
Its zero set `S_gamma = { x in U : e_gamma(x)=0 } ` has
`|S_gamma| >= |U| - t = R + kappa - t >= kappa + 1`.

Define for each `x` the linear form
`L_x(gamma, c) = b0(x) + gamma b1(x) + sum_i c^{(i)} z_i(x)`. For any
`(kappa+1)`-subset `T = {x_0,...,x_kappa} subset S_gamma`, the point `c_gamma`
lies on all `kappa+1` hyperplanes `L_{x_i}(gamma, .) = 0`, so the augmented
`(kappa+1) x (kappa+1)` system is consistent and its determinant vanishes:

```
 Delta_T(gamma) = det[ Z_T | b0_T + gamma b1_T ] = 0,
```

where `Z_T` has rows `(z_1(x_i),...,z_kappa(x_i))` and the last column is
`(b0(x_i) + gamma b1(x_i))_i`. Expanding the last column, `Delta_T` is **affine
in gamma**: `Delta_T = det[Z_T|b0_T] + gamma det[Z_T|b1_T]`.

*Transversality => some `T` is non-degenerate.* Suppose every
`(kappa+1)`-subset `T subset S_gamma` had `Delta_T = 0` identically, i.e. both
`det[Z_T|b0_T] = 0` and `det[Z_T|b1_T] = 0`. Then the `|S_gamma| x (kappa+1)`
matrix `[Z_{S_gamma} | b0_{S_gamma}]` has all `(kappa+1)`-minors zero, so rank
`<= kappa`; but its first `kappa` columns are independent (any `kappa` rows give
a nonsingular MDS minor, and `|S_gamma| >= kappa+1`), so
`b0|_{S_gamma} in span(z_1|_{S_gamma},...,z_kappa|_{S_gamma})`; likewise
`b1|_{S_gamma}`. Subtracting the matching kernel combinations from `b0, b1`
produces lifts `b0', b1'` with the same syndromes `y0, y1` supported on
`U \ S_gamma = supp(e_gamma) subset E_gamma`. Then `y0, y1 in V_{E_gamma}`,
contradicting transversality. Hence some `T_gamma subset S_gamma` has
`Delta_{T_gamma}` affine and **not identically zero**, so `Delta_{T_gamma}` has
a unique root; `gamma` is that root.

*Injective charge.* If `gamma != gamma'` mapped to the same `T`, both would be
roots of the nonzero affine `Delta_T`, impossible. So `gamma |-> T_gamma`
injects `Z` into the `(kappa+1)`-subsets of `U`, giving
`|Z| <= C(|U|, kappa+1) = C(R+kappa, kappa+1)`. QED.

**Why this is the named "transverse-secant" object.** In `mathbb P(F^R)` the
columns `h_x` are `R+kappa` points of the rational normal curve in **general
position** (any `R` independent -- the MDS/uniform-matroid fact). `Delta_T = 0`
is precisely the condition that the `kappa+1` curve points of `T` and the moving
syndrome point `b0 + gamma b1` are linearly dependent -- a moving-secant
incidence -- and "affine in gamma" is why each secant is hit once. The bound
counts secant `(kappa+1)`-flats, field-independently.

### 2.1 Falsifier (rung 4) -- outcome `NULL`, and the bound is `sharp`

Design (stated so a null is informative): exact arithmetic over prime `F_q`,
Vandermonde parity checks, charts `U` of size `R+kappa`. For each case compute
`max_{y0,y1} Theta_t^U` **without baking in the bound** -- full `(y0,y1)`
enumeration for small `q`, and the projective-line reduction
`max_W min(projcount(W), q)` (cross-validated equal to full enumeration, group D)
for larger `q`. Family swept:
`q in {5,7,11,13,17,19}`, `R in {2,3,4}`, `kappa in {1,2,3}`, `t in {1,...,R-1}`.

- **No violation** of `|Z| <= C(R+kappa,kappa+1)` in any case. `[NULL]`
- The interesting regime is `C(R+kappa,kappa+1) < q` (bound, not `q`, binding).
  There the bound is **attained** (`max = C(R+kappa,kappa+1)`) for `kappa=1`
  (`C(R+1,2) = 6` at `R=3,q in {7,11,13,17,19}`; `C(5,2)=10` at `R=4,q in{11,13}`)
  and for `kappa=2` (`C(5,3)=10` at `R=3,q in {11,13}`). At `kappa=3, q=17` the
  max is `14 <= 15 = C(6,4)` (valid, near-sharp, not `q`-limited since `14<17`).
- So the bound is not merely valid but **exactly sharp for `kappa <= 2`**, i.e.
  it cannot be lowered as a universal `C(R+kappa,kappa+1)` bound. `[COMPUTED]`

A counterexample here would have refuted the theorem; the null therefore
corroborates the proof, and the attained maxima corroborate that the constant is
correct (not merely safe).

### 2.2 Consequence for `(RC)` -- conditional discharge `[PROVED]`

On a balanced-core chart confined to a fixed `U` with `|U| = R + kappa`, the
theorem gives the **direct** bound `|Z^o_lambda| <= C(R+kappa,kappa+1)`. Whenever
`kappa = o(n / log n)` (in particular any **bounded** kappa),
`C(R+kappa,kappa+1) <= C(n,kappa+1) = e^{o(n)}`, so `(RC-direct)` holds
**unconditionally and field-independently**. Thus `(RC)` is a **theorem, not a
hypothesis**, on the bounded-kernel higher-dimensional balanced cores -- the
"higher-dimensional coefficient family" half of `rem:balanced-core-exhaustion`.
This strictly enlarges the regime of `thm:bounded-residual-kernel-ray` from
`(|U|-R) log|F| = o(n)` (field-dependent, vacuous for exponentially large `q`) to
`(|U|-R) log(R+|U|) = o(n)` (field-free).

---

## 3. What remains open (rung 5) -- named walls, checked

1. **Unbounded kernel dimension.** If `kappa = Theta(n)`, then
   `C(R+kappa,kappa+1)` is itself exponential; the theorem no longer gives
   `e^{o(n)}`. WALL: *is the residual balanced-core kernel dimension `o(n/log n)`
   for admissible sequences?* This is a property of the atlas, not of a single
   chart. Cheap route checked-dead: one cannot beat `C(R+kappa,kappa+1)` by the
   affine-determinant charge alone -- the falsifier shows it is already **sharp**
   at `kappa<=2`, so no better field-independent per-chart constant of this shape
   exists; reducing the exponent needs extra structure on which `U` occur.
2. **Chart exhaustion / atlas count.** The number of charts `U` (= profiles) must
   be `e^{o(n)}` to sum the per-chart bounds; that is condition (A2)
   (`lem:profile-atlas`, L4772), the "decomposes into subexponentially many
   pencils" half of `rem:balanced-core-exhaustion`. Not addressed here; it is a
   *separate* input (hard input #1). This lane bounds the per-chart count, not the
   number of charts.
3. **Off-chart witnesses.** The theorem assumes witnesses confined to one fixed
   `U`. Bad slopes whose witness supports are not all inside a single size-`(R+kappa)`
   chart are handled by the first-match atlas decomposition, not here.

These three are the honest residual; none is silently consumed.

---

## 4. Proposed ledger entries (proposed; NOT applied to `.tex`/`.pdf`)

Format per `experimental/asymptotic_rs_mca.md` (Source / Status / Paper impact /
Next action).

### L-RC-1 (new theorem available to replace part of the hypothesis)
- **Source:** this lane; `verify_ray_compiler_core.py`.
- **Status:** `PROVED` (per-chart), field-independent; computationally sharp for
  `kappa<=2`.
- **Paper impact:** `thm:bounded-residual-kernel-ray` (L1679) can be sharpened
  from `(t+1)|F|^{kappa(U)}` to the field-independent `C(R+kappa,kappa+1)`
  (`kappa = |U|-R`), recovering `thm:single-mds-circuit-ray` at `kappa=1`. The
  higher-dimensional case of `rem:balanced-core-exhaustion` (L4762) and the open
  "higher-dimensional transverse-secant bound" (L1088-1090) are then supplied for
  bounded / `o(n/log n)` kernel dimension.
- **Next action:** insert as a corollary of `thm:syndrome-secant-exact` using the
  affine `(kappa+1)`-minor charge; re-derive the transversality step at review.

### L-RC-2 (scope tightening for the remark)
- **Source:** this lane.
- **Status:** `AUDIT`.
- **Paper impact:** `rem:balanced-core-exhaustion` bundles two claims (higher-dim
  coefficient family; decomposition into subexponentially many pencils). Only the
  second is genuinely open once L-RC-1 is inserted; the first is discharged for
  `kappa = o(n/log n)`.
- **Next action:** split the remark so the residual open statement is the
  atlas/exhaustion (A2) claim and the per-chart count is cited as proved; state
  the explicit `kappa = o(n/log n)` regime.

---

## 5. Files, credit, per-claim labels

- Note: `experimental/notes/thresholds/ray_compiler_balanced_core.md` (this).
- Verifier: `experimental/scripts/verify_ray_compiler_core.py`
  (`RESULT: PASS (173 checks)`; groups A combinatorics, B MDS structure,
  C exact inequality, D cross-check + tightness, E charging-certificate,
  F LegaSage cross-check, G tex anchors).
- Read-only inputs: `experimental/asymptotic_rs_mca_frontiers.tex@4e3c4ee`;
  #524 delta-audit (`thresholds-frontiers-delta-audit`); LegaSage `#523`
  (`pr-523-legasage`), `#514` (`pr-514-legasage`).

**Per-claim status.** anatomy 1.1-1.4 = `EXTRACTED` (checked against tex, gated
lines); Theorem 2 = `PROVED` (full proof; end-to-end computational validation of
the charging mechanism, group E); tightness 2.1 = `COMPUTED` (exact, gated,
`kappa<=2` sharp); `(RC)` discharge 2.2 = `PROVED` conditional on bounded/
`o(n/log n)` kernel dimension and single-chart confinement; walls 3 = `WALL`
(cheap routes checked). Ledger entries = proposed, not applied.

**Credit.** LegaSage `#523` isolated this as hard input (c) and disclosed the
"nonlinear ray map" gap; `#514` gated the abstract double-count. The proof and
the field-independent constant here are the direct-attack complement to those
audits: same gap, different scope (proof in RS geometry vs proxy/statement
audit).

**Distinction (exact vs heuristic).** All computations are exact finite-field
arithmetic (Gaussian elimination over prime `F_q`); no floating point, no
sampling in the gated checks. The projective-line reduction used for large `q` is
proved equal to definition-level full enumeration on overlapping cases
(group D). The asymptotic reading `C(R+kappa,kappa+1) = e^{o(n)}` for
`kappa = o(n/log n)` is an elementary bound, flagged for the PI as the single
non-finite step.
