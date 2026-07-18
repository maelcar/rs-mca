# Dense-shell PROP-TAIL: DISCHARGED (certified-census, CONDITIONAL) via the deep-base equilibrium chain

Stacked on the predecessor packet (`experimental/notes/thresholds/dense_shell_inv_tail_closure.md`,
PR #885), which reduced #880's |K| = 1 class-sum dichotomy (unconditional persistence
of three certified floors for all levels j >= 49) to a single named scalar residual,
(PROP-TAIL): the cross-index spread of the sibling entrywise ratio profile,
`rho_prop@i<17(n) <= 1.02560749`, persisting for all n beyond the level-60 grid the
predecessor certified. This packet reduces that scalar from an opaque numeric
persistence claim to a **certified contraction frame** — an exact reduction lemma, an
exact spectral gap, a certified one-step recursion, and a joint induction — and then
**closes it**: the deep-base equilibrium route (base `J0* = 500`, floor pad
`f* = 99/100`, contraction gate `theta* = theta_band`, a certified band-uniform constant
from gate V15-IA, not a fixed number) clears the arithmetic slot on **finite checks**,
certified by an exact-Fraction, lam-minced interval-arithmetic census of the tangent
seminorm (gate V15-IA) feeding an exact-Fraction minced interval-arithmetic forcing
census (gate V17-IA), plus a re-certified floor family at the deep base (gate F3) plus
full base coverage to `n = 500` (gate V18). **The discharge holds as a certified-census
theorem MODULO the enumerated computed clauses** (Section 8.4: (FOLD),
(FLOOR-PERSIST)) — its two load-bearing gates certify a **forced-proportional surrogate**
(`c^+ = lam c^-`) of the real cascade, so the STATUS is **CONDITIONAL**, not PROVED. The
contraction gate `theta* = theta_band` is a certified band-uniform constant from gate
V15-IA, not an asserted number. **Upgrade (this revision):** the fourth clause,
(SIB-BAND) — whether the forced-proportional surrogate's coverage extends to the real,
non-proportional cascade — is now **DISCHARGED**: gate SIB-CERT re-runs the same
wobble census at a much deeper anchor (`J0 = 800`, floor pad `999/1000`) using the
tighter, geometric-center wobble band (its own boundary slot, `i=17`, one past the IH's
window, covered by a separately-monitored deep box — Section 8.4's BOUNDARY ANNEX), and
it clears (`+7.4%` margin), covering the real cascade with no assumption beyond
(LAM-BOX) itself (Section 8.4). The deep grid (gate V18) is extended to `n = 800` to
match. **Upgrade (this revision, LAM-INV):** (LAM-BOX) itself — the sibling-
proportionality magnitude box `[lam, Lambda^+, Lambda^-]` both load-bearing gates
box-max over — is now **DISCHARGED-conditional**: gate LAM-INV (full mode only) proves
`lam`, `Lambda^+`, `Lambda^-` are *invariant intervals*, valid for **every** `n`, not
merely a measured-and-padded range monitored on a finite grid. The proof rests on an
exact windowed-mass-recursion identity, a Birkhoff mass-field enclosure, and a coupled
Lambda-field enclosure (DERIV_LAMBOX.md), conditional on the existing floor box, the
existing finite base-case census (MAG-BOX/V18), an a-posteriori Lipschitz self-check, and
one remaining generous monitored constant (the `(C'-CAP)` clause). The `Lambda^+` floor
is widened `-1.16 -> -1.17` (R1 mitigation (b)) to give the proved interval comfortable
headroom; every consumer census is re-run over the wider box (Section 8.4). **Upgrade
(this revision, round 4):** (C'-CAP) itself is **DISCHARGED-conditional** — R1
mitigation (a), the exact floor-box bound on the correction derivative, is carried out:
gate LAM-INV now PROVES `C' <= CPRIME = 3/500` at every node of its own NG grid (the
only places the recursion consumes the cap), via an exact identity for the dropped term
(`Lambda_true - Lambda_pure = [gbar*Lambda_pure - C'/P]/(1-gbar)`) and per-branch
floor-box data, with the a-posteriori monitor retained as the empirical cross-check
(Section 8.4). And (FLOOR-PERSIST) — until now IMPORTED reasoning with no gate of its
own — becomes a **first-class monitored clause**: new core gate FLOOR-DRIFT checks the
drift mechanism directly (123 parameters, deep-grid pairs) plus the exact as-consumed
floor margins at both anchors, and the natural discharge route is **CLOSED as a
route-cut** (Section 9(v): a V12-style pointwise corner census box-worst misses the
floors by ~42% — the box has no mechanism coupling input-floor slack to output-floor
slack). Two computed clauses remain open: **(FOLD)** and **(FLOOR-PERSIST)** — both
named, gated, and tamperable; no monitored-only literal remains.

## 0. Status (S0)

**(PROP-TAIL) DISCHARGED as a certified-census theorem MODULO the enumerated computed
clauses (Section 8.4) — STATUS: CONDITIONAL.** House form: **PROVED (equilibrium chain,
sufficiency) + census-closed (gates F3 / MAG-BOX / V15-IA / V17-IA / V18 / LAM-INV /
FLOOR-DRIFT), conditional on exactly two computed clauses (FOLD), (FLOOR-PERSIST) —
(LAM-BOX) is DISCHARGED-conditional by gate LAM-INV, (SIB-BAND) is DISCHARGED at a deep
anchor by gate SIB-CERT, and (C'-CAP) is DISCHARGED-conditional by LAM-INV's floor-box
node census (this revision; the a-posteriori monitor is retained as a cross-check)
(Section 8.4)**. The composed
theorem (Section 7) is PROVED-given-gates; every core gate it depends on is green at the
shipped triple `(J0*, f*, theta*) = (500, 99/100, theta_band)`, where **`theta_band` is
itself a certified band-uniform output of gate V15-IA** (Section 5), not an asserted
constant. The two load-bearing gates (V15-IA, V17-IA) certify the **forced-proportional
surrogate** `c^+ = lam c^-` of the cascade at that shallower anchor; the residual
computed content (the magnitude box the gates box-max over, the window fold, and floor
persistence for `n > 500`) is enumerated explicitly in Section 8.4, together with the
now-discharged (SIB-BAND) clause and the SIB-CERT deep-anchor census that discharges it.
Certified equilibrium arithmetic (exact values; final gate comparisons are exact
Fraction; gates V15-IA / V17-IA / V18):

```
    theta_band                  = 0.6020244   (certified band-uniform sup, gate V15-IA,
                                                exact Fraction 1505061/2500000, lam-minced
                                                rigorous enclosure, folded by the certified
                                                Window Lemma factor <=57/50)
    F_box(500, 99/100)          = 0.02690175  (certified sup, width-2 minced-IA, Fraction, gate V17-IA)
    tau*                        = 0.07585533  (exact-Fraction lower bound TAU_STAR_FR
                                                = 0.075855330599169 <= 3 log(1.02560749))
    threshold (1-theta*)*tau*   = 0.03018857  (theta*=theta_band; final comparison exact Fraction)
    margin                      = 10.9%       (F_box 0.02690175 <= 0.03018857 clears the threshold)

    equilibrium chain (gate-printed):
      F_box/(1-theta_band)      = 0.06759647  <= tau* = 0.07585533   [OK]
      (1/3)*0.06759647          = 0.02253216  <= log(TARGET) = 0.02528511
      exp(0.02253216)           = 1.022788    <= TARGET = 1.02560749  [OK]

    sup_{n>=500} V_17(n) <= max(V_17(500), F_box/(1-theta_band))
                          = max(0.00111699, 0.06759647)
                          = 0.06759647                         (the forcing dominates)

    log rho_prop@i<17(n) <= (1/3) * 0.06759647 = 0.02253216    (for all n >= 500, Lemma 1)
    ln(1.02560749)                             = 0.02528511
                            0.02253216 < 0.02528511            margin 10.9%
```

for all `n >= 500`; the deep grid (gate V18) covers `48 <= n <= 500` directly (every
tested level `rho_prop@i<17(n) <= 1.02560749`, monotone non-increasing), so **the
target holds for every `n >= 48`**, discharging (PROP-TAIL) modulo the Section 8.4
computed clauses.

**The contraction gate, precisely.** The discharge-determining contraction gate is
`theta* = theta_band`, a certified band-uniform output of gate V15-IA (Section 5): an
exact-Fraction, lam-minced rigorous enclosure of the Lemma A1 tangent seminorm over the
*entire* certified LC ratio box, not merely a tested grid or the realized profile.
Certified `theta_band = 0.6020244`; at the shipped anchor `(500, 99/100)` the forcing
census clears with a 10.9% margin. The grid census (`theta_tot`, `theta_win`, `N_free`)
is retained as an **informational robustness cross-check** (gate `V15-GRID`) — it is
comfortably consistent with the certified band (`theta_tot`'s worst grid value `0.3766`
sits well inside `theta_band = 0.602`), but is not part of the certified chain.

**PROVED** (elementary; no finite check needed beyond exact rational/interval
arithmetic):
- the **reduction lemma** (Section 2, Lemma 1): `log rho_prop@i<17(n) <= (1/3) V_17(n)`,
  where `V_17(n)` is a *single-level* windowed tangent spread — proved by the
  fundamental theorem of calculus plus a triangle inequality, removing the two-branch
  coupling from the target;
- `theta~(t) <= 1/5` (Section 4, Lemma 3) via the **exact polynomial identity**
  `75(1-x^2) - (6+3x)^2 = -3(2x-1)(14x+13)`, `x = cos(2 pi t/3) in [1/2, cos(pi/9)]`,
  verified coefficient-by-coefficient over the rationals; equality only at `x = 1/2`
  (the domain's edge, `t = 1/2`);
- the **exact 3-term cascade** `L = T1 (share-variation) + T2 (smoothed deviation) +
  T3 (a'-source)`, imported from the predecessor's differential-cascade machinery
  (Section 3);
- the **tangent-half corner-sufficiency closed form** (Lemma A1, Section 5): for fixed
  profiles, the map from child log-derivative deviations to the deviation term `T2` is
  linear, and its induced oscillation-seminorm has an exact closed form (an LP-vertex
  identity — no sampling loss in the tangent direction);
- the **band-uniform tangent census** (Section 5, gate V15-IA, one of the two
  load-bearing certificates): an exact-Fraction, lam-minced rigorous enclosure of Lemma
  A1's seminorm over the *entire* certified LC ratio box (not the realized profile, not a
  tested grid) — `theta_band = 0.6020244`, certified for every `n >= J0*`, feeding
  gate V17-IA's threshold directly;
- the **window lemma's asymptotic fact** `289/256 <= 57/50` (Section 6, Lemma W1) —
  an exact rational inequality;
- the **triangle steps** (Section 6, Lemma W3, and the second inequality of Lemma 1):
  subadditivity of `max - min`, no hypotheses;
- the **deep-base forcing census** (Section 8.1, gate V17-IA, one of the two
  load-bearing certificates): `F_box(500, 99/100) <= (1-theta_band) tau*` via an
  exact-Fraction, minced interval-arithmetic enclosure of the box-certified forcing at
  width-2 locality (every index `i`'s marginal range, not merely the two endpoints) — a
  rigorous upper bound, not a corner-sample estimate;
- the **re-certified floor family at the deep base** (Section 8.1, gate F3):
  positivity, LC-compatibility, and the `i = 0` halving-convention cross-check hold at
  `J0* = 500`, pad `f* = 99/100`, over the full 41-parent grid.

**COMPUTED — informational grid views** (a finite, reproducible measurement, not a
proof; these specific items are robustness cross-checks, not gates the discharge rests
on — the computed inputs that DO feed the certified chain are enumerated separately in
Section 8.4):
- `theta_tot in [0.3662, 0.3766]` over `n in {60,...,500}` — **flat**, and **binding at
  the parent `t = 1/6`, not the edge** (a correction to a naive edge-only reading, see
  Section 10); comfortably inside the certified `theta_band = 0.602` at every level
  tested — a robustness cross-check, not the gate the discharge rests on (gate
  `V15-GRID`, informational);
- `theta_win in [0.1971, 0.2032]` over the same grid — flat, binding at the edge `t ->
  1/2`;
- forcing tables `F_ext(n)*n^2 in [182.4, 187.8]` and `Curv(n)*n^2 in [100.4, 109.1]`,
  both flat/decaying, with a **hairline non-monotonicity in `Curv*n^2` at n = 300**
  (an uptick of +0.002, ~0.002% relative) flagged as most likely finite-difference
  noise at that small a raw value, not a real turn;
- the bridge weight `w(n) ~ 0.61` (range `[0.6084, 0.6115]`, informational/alpha-only —
  not used by the shipped equilibrium chain, Section 2);
- the deep grid to `n = 500`: `rho_prop@i<17(n) <= 1.02560749` at every gated level,
  monotone non-increasing, margin growing from `+1.7e-5` at `n=48` to `+0.0254` at
  `n=500`;
- the crossover `V_17(n) <= tau* := 3 log(1.02560749) = 0.075855...` at **exactly**
  `n = 62` (`V_17(61) = 0.0761 > tau*`, `V_17(62) = 0.0737 <= tau*`, full-integer scan) —
  informational (the deep grid to `n=500` already covers the base directly; the
  equilibrium route does not need this crossover, only the sharp/R-c strengthening
  would);
- the mu-sign / monotone-cone tightener `theta~0.376` for the *sharp* `C/n^2` law stays
  COMPUTED/informational only — checked and found **NOT** to carry as a clean
  finite corner certificate (Section 8.3); **not needed** for this discharge, which
  uses only the certified band-uniform `theta_band` gate.

## 1. Objects and conventions (self-contained)

Level vectors `G_n(t)`, `t in [1/6, 1/2]`. Flipped-positive half-weight coordinates
`c_0 = b_0`, `c_i = b_i/2`, even-extended (`c_{-1-k} := c_k`). One branch step is exact
`Z`-convolution with the tridiagonal kernel `K_d = (1/4, d, 1/4)`, `d(t) = -cos(2 pi
t)/2`; children `t_pm = (1 pm t)/3`; the aggregated step

```
    c(G_n(t)) = K_{d(t_+)} * c(G_{n-1}(t_+)) + K_{d(t_-)} * c(G_{n-1}(t_-)).      (STEP)
```

Mass factor `a(t) = sin^2(pi t) = 1/2 + d(t)`; `a'(t) = pi sin(2 pi t)`. Write
`rc_i := c_{i+1}/c_i` (band ratio), `L_i(n,t) := d/dt log c_i(G_n(t))` (the *tangent*
object this packet's frame is built on), and the *sibling* ratio and its cross-index
spread (the predecessor's S7 object, V13's convention):

```
    g_i(n,t) := c_i(G_n(t_-)) / c_i(G_n(t_+)),
    rho_prop@i<W(n) := sup_t  max_{i<W} g_i / min_{i<W} g_i.
```

**Operative window**: `i < 17` (indices 0..16, `OPWIN = 17`), the corner-vector length
the predecessor's census (V12) consumes. **Honest child-read window**: `i < 18`
(indices 0..17, `CWIN = 18`) — the tridiagonal step reads one index beyond the output
window (Section 6). The windowed single-level tangent spread and its threshold:

```
    V_W(n) := sup_t [ max_{i<W} L_i(n,t) - min_{i<W} L_i(n,t) ],
    TARGET := 1.02560749,   tau* := 3 * log(TARGET) = 0.07585533...
```

**Imported facts** (established in the predecessor packet, re-used here without
re-proof): the c-vector is nonincreasing (`rc_i <= 1` for every `j >= 5`, PROVED);
level-48-anchored floors `rc_i(n,t) >= (49/50) rc_i(48,t)` persist for all `n >= 48`
(certified, since `rc_i` drifts upward in `n`); the output c-ratios stay non-increasing
under the predecessor's corner census (output log-concavity, "output-LC" — see the
precision note in Section 10 for an honest caveat on this specific clause); the
degenerate CLT limit `c_i(n,t) ~ c_0 exp(-beta i^2/n)`, `beta = 0.6191` (COMPUTED, a
fitted asymptotic, not proved); and the differential cascade `Dc(G_n) = (1/3)[K_{d+} *
Dc^+ + a'(t_+) c^+] - (1/3)[K_{d-} * Dc^- + a'(t_-) c^-]` (PROVED, chain rule), which
Section 3's cascade below re-derives for the tangent object `L`.

## 2. Lemma 1 — the reduction. PROVED.

> **Lemma 1.** For every level `n` with `c_i(G_n(t)) > 0` on `i < 17`, `t in [1/6,1/2]`
> (guaranteed by the caps/floors above):
> ```
>     log rho_prop@i<17(n)  <=  sup_t (2t/3) * sup_{tau in [t_-,t_+]} spread_{i<17} L(n,tau)
>                            <=  (1/3) * V_17(n).
> ```

*Proof.* Fix `t`. For each `i`, `log g_i(n,t) = log c_i(G_n(t_-)) - log c_i(G_n(t_+)) =
-integral_{t_-}^{t_+} L_i(n,tau) dtau` (fundamental theorem of calculus). For any two
indices `i, i' < 17`, `log g_i - log g_{i'} = -integral(L_i - L_{i'}) dtau <=
integral spread_{i<17} L(n,tau) dtau`. Taking `max_i, min_{i'}`, then `sup_t`:
`spread_{i<17} log g_i(n,t) <= (t_+ - t_-) sup_{tau in [t_-,t_+]} spread_{i<17}
L(n,tau)`. Since `t_+ - t_- = 2t/3 <= 1/3` and `[t_-,t_+] subset [1/6,1/2]`, the RHS is
`<= (1/3) V_17(n)`. QED.

**What this buys.** `rho_prop` is a *two-branch* object (it compares the two
children); Lemma 1 bounds it by a *single-profile* object `V_17(n)` — the coupling
survives only in the *recursion* for `V_17` (Sections 3-5), never in the target itself.
This is the entire reduction: everything after this lemma is about bounding one
single-level tangent spread, not a sibling pair.

**Tightness (informational).** The ratio of the loose bound `(1/3)V_17(n)` to the
sharp integral form is a *bridge weight* `w(n)`, COMPUTED flat at `~0.61` (gate V19,
Section 11) — the `(1/3)`-form alone overstates by a nearly-constant `1/0.611 = 1.637x`
factor. The certified spine below (Section 7) uses the loose `(1/3)` form plus decay,
never the tight integral, so `w` plays no role in the beta-spine discharge; it is kept
only as an alpha-route, informational cross-check (Section 9(iii), Section 11's V19).

## 3. Lemma 2 — the exact 3-term cascade. PROVED structure, COMPUTED reconstruction.

Write `c^pm := c(G_{n-1}(t_pm))`, `W^pm := K_{d(t_pm)} * c^pm` (so `c(G_n) = W^+ +
W^-` by (STEP)), branch shares `sigma^pm_i := W^pm_i / c_i(G_n)`
(`sigma^+_i + sigma^-_i = 1`), child log-derivatives `L^pm_k := L_k(n-1, t_pm)`, split
`L^pm_k = Lambda^pm + delta^pm_k` about the **window-mean reference scalar**
`Lambda^pm := mean_{k<18} L^pm_k` (the choice is not free: the Lemma A1 seminorm
`(1/2) sum_k |Delta_k - mu|` is the operator norm over ZERO-SUM deviations, and only the
window-mean makes `delta^pm` zero-sum; with a non-zero-sum `delta` the row-sum mass
differs and `osc(T2)/osc(delta)` is unbounded — adding a constant to `delta` leaves
`osc(delta)=0` but `osc(T2)!=0`. The choice is sound and costs nothing:
`osc(delta) = spread(L) = V_17(n-1)` is shift-invariant, unchanged by the reference).
Then, from the chain rule applied to (STEP) (the predecessor's differential-cascade
machinery, re-derived here for `L` rather than `Dc`), **exactly**:

```
  L_i(n,t) = (1/3)[ Lambda^+ sigma^+_i - Lambda^- sigma^-_i ]                       (T1, share-variation)
           + (1/3)[ (K_{d+}*(delta^+ (x) c^+))_i - (K_{d-}*(delta^- (x) c^-))_i ] / c_i(G_n)   (T2, smoothed deviation)
           + (1/3)[ a'(t_+)(c^+_i - c^-_i) - a'(t/3) c^-_i ] / c_i(G_n).            (T3, a'-source)
```

**COMPUTED**: reconstruction `max_i |T1+T2+T3 - L_i| <= 4e-11` at every tested `(n,t)`.
`T2` alone carries the recursion (it is the only term reading the *child deviations*
`delta^pm`, whose spread is `V_17(n-1)`); `T1, T3` are forcing terms driven by the
child *profiles*, not their tangent deviations.

## 4. Lemma 3 — the leading contraction, closed form. PROVED.

> **Lemma 3.** In the identical-sibling limit (`c^+ = c^- =: c`, `delta^+ = delta^- =:
> delta`), `T2` reduces to `T2_i = theta~(t) delta_i (1 + O(1/n))` with
> ```
>     theta~(t) = (d_+ - d_-) / (3(a_+ + a_-)) = sqrt(3) sin(2 pi t/3) / (6 + 3 cos(2 pi t/3)),
> ```
> increasing on `[1/6, 1/2]`, `theta~(1/6) = 0.0672`, `theta~(1/2) = 1/5`. Hence
> `theta~(t) <= 1/5` on the whole domain, with the **maximum at the binding edge**
> `t = 1/2` (equality there).

*Proof.* The two kernels differ only in the center weight, `K_{d+} - K_{d-} = (d_+ -
d_-) delta_0`, so the `T2` numerator collapses to `(1/3)(d_+ - d_-) delta_i c_i`; the
denominator `c_i(G_n) = (a_+ + a_-) c_i (1 + O(1/n))` by the trace identity `a_+ + a_-
= 1 - d(t/3)`. Dividing gives the closed form; `d_+ - d_- = (sqrt(3)/2) sin(2 pi t/3)`
and `a_+ + a_- = 1 + (1/2) cos(2 pi t/3)` by product-to-sum on `d(s) = -cos(2 pi s)/2`.
For the bound: set `x = cos(2 pi t/3)`. Squaring (both sides nonnegative on the
domain), `theta~(t) <= 1/5` is equivalent to `75(1-x^2) <= (6+3x)^2`, i.e.
```
    75(1-x^2) - (6+3x)^2  <=  0.
```
**Exact polynomial identity** (Fraction-verified, coefficient-by-coefficient in `x`):
```
    75(1-x^2) - (6+3x)^2  =  -3(2x-1)(14x+13).
```
On the domain `t in [1/6,1/2] => x = cos(2 pi t/3) in [1/2, cos(pi/9)]` (cos decreasing):
`(2x-1) >= 0` (equality only at `x = 1/2`, i.e. `t = 1/2`) and `(14x+13) >= 20 > 0`, so
`-3(2x-1)(14x+13) <= 0` throughout, equality only at the edge. QED.

This is **the spectral gap the predecessor's shape-analysis could not see**: it lives
in the *tangent* (log-derivative) direction, not in the profile itself — the
predecessor's own refutation of a uniform full-profile contraction (`theta_j -> 1` as
`n` grows, no geometric contraction on the *shape*) is a fact about a different object.

## 5. The tangent corner-sufficiency certificate (Lemma A1)

`T2_i` is, for **fixed** child profiles `(c^+,c^-)`, a **linear** map of the deviation
vectors `(delta^+, delta^-)`:
```
   T2_i = sum_k M^+_{ik} delta^+_k + sum_k M^-_{ik} delta^-_k,
   M^pm_{ik} = (1/3) (K_{d(t_pm)})_{ik} c^pm_k / o_i,     o := K_{d+}c^+ + K_{d-}c^- = c(G_n(t)).
```
`osc_{i<17}(T2) = max_{i,i'} (T2_i - T2_{i'})` is then a max of linear functionals of
`(delta^+, delta^-)` — convex and positively homogeneous, hence a **seminorm**; its
extreme over the polytope `{osc(delta^pm) <= 1}` sits at vertices.

> **Lemma A1 (tangent seminorm, PROVED).** Take the deviations `delta^pm` about the
> **window-mean reference** `Lambda^pm = mean_{k<18} L^pm_k` (so `delta^pm` is zero-sum,
> Section 3 — the seminorm below is the operator norm over ZERO-SUM deviations, and the
> window-mean is the choice that realizes it). With `Delta^pm_k := M^pm_{ik} -
> M^pm_{i'k}`, `mu^pm := mean_k Delta^pm`,
> ```
>   ||delta -> T2||_{osc<-osc}  =  max_{0<=i<i'<17}  (1/2)[ sum_k |Delta^+_k - mu^+| + sum_k |Delta^-_k - mu^-| ],
> ```
> an exact LP-vertex identity — **no sampling loss in the tangent direction**.

`K_d` is tridiagonal (`(K_d)_{ik}` nonzero only for `|i-k| <= 1`, plus the
even-extension doubling at `i=0`), so each row of `M^pm` has at most 3 nonzero entries
and the sum above is cheap and exact (rational, given rational inputs).

**What is (and is not) rigorously certified here.** Lemma A1 makes the *tangent*
direction exact: for any FIXED profile pair `(c^+,c^-)`, the seminorm formula above is
the true operator norm, not an estimate. The grid gate `V15-GRID` (informational,
Section 11) evaluates that exact formula only at the *realized* profiles on a 41-parent
grid at each tested level `n` (**COMPUTED** — a grid measurement at the actual cascade,
not a box census). The **profile** direction does *not* enjoy the predecessor's V12
Möbius corner-sufficiency (the seminorm, as an `osc`/max-min object, is a difference of
terms with *different denominators* `o_i, o_{i'}`, hence a degree-`(2,2)` rational in
each profile ratio, not a Möbius function — the same structural boundary the precision
note of Section 10 documents for V12's own out-LC clause).

**The band-uniform enclosure (gate V15-IA).** Under the SAME forced
sibling-proportionality reduction gate V17-IA already uses (`c^+ = lam c^-`, `lam` in
the certified magnitude box), `M^pm_{ik}` reduces to `(1/3) w_ik lam^{[pm=+]}
(c^-_k/c^-_i)/(A+B P_i)` (`A = lam d_+ + d_-`, `B = lam+1`, `P_i` as in Lemma C0). For
**fixed** `lam`, the diagonal entry depends on `(rc_{i-1},rc_i)` only via the scalar
`P_i` (reuse its own tight closed-form box), and the off-diagonal entries are — by direct
partial-derivative computation, no assumption — strictly coordinatewise monotone in
**both** `(rc_{i-1},rc_i)` simultaneously, with a sign independent of `lam`, so their
extremes sit at exactly two `(rc_{i-1},rc_i)` points (a monotone-path argument). Each
entry is Möbius in `lam` — but the **seminorm** is a sum of `|differences of
Möbius-in-lam entries with different denominators|`, so it is **not** itself Möbius in
`lam` and can attain its maximum at an interior `lam`; an endpoint-in-`lam` sufficiency
argument would therefore be **unsound**. The rigorous fix is to **mince `lam` into
panels** (`LAM_MINCE = 24`), hull each Möbius-in-`lam` entry over each panel, and take
the outer max over panels — a genuine rigorous enclosure over the shared-`lam` box (all
entries in a given panel evaluation share one `lam` sub-interval, respecting the
shared-`lam` constraint; a per-entry-independent-`lam` bound would be strictly looser,
Section 9(iv)). Cross-validated against 36,000 random LC-feasible profile draws (0
violations). **Certified**: `theta_band = 0.6020244` (exact Fraction `1505061/2500000`,
window-folded, `J0*=500, f*=99/100`) — comfortably inside the gate's own unconditional
sanity ceiling `0.9`, and consistent with the realized `theta_tot approx 0.35-0.38` (the
realized deviation is far from the seminorm's own worst-case vertex). This forced-
proportional surrogate is what the load-bearing gates certify; the real cascade is
non-proportional, and that gap is enumerated as computed clause (SIB-BAND) in Section
8.4 — now DISCHARGED there at a deep anchor (gate SIB-CERT), given (LAM-BOX) alone.
`theta_band` feeds gate V17-IA's threshold as `theta*` (Section 8.1) — the
discharge's contraction gate is a **certified band-uniform constant**, not a grid
measurement.

## 6. Window lemmas (W1-W3)

The tridiagonal step means the output index `i = 16` (the top of the operative window)
reads child index `k = 17` — one beyond the operative window. Three lemmas unify this
bookkeeping.

> **Lemma W1 (child-window factor).** The one-step contraction census on the operative
> output window `i < 17` reads child `L`-deviations on `i < 18`, and
> ```
>     spread_{i<18}(L)  <=  (V_18/V_17) * spread_{i<17}(L),   V_18/V_17 -> 289/256 = 1.128906...  (n -> infinity),
> ```
> certified by the finite check `sup_{n,t} spread_{i<18}(L)/spread_{i<17}(L) <= 57/50 =
> 1.14` (measured max `1.1322` at `n = 48`, decreasing thereafter).

The asymptotic ratio comes from the degenerate CLT tangent profile `L_i propto -i^2`,
giving `mu_k := L_{k+1} - L_k propto (2k+1)`, hence `V_W propto (W-1)^2`
(`V_18/V_17 -> 17^2/16^2` exactly, an elementary consequence of the quadratic profile).
**Label**: the arithmetic fact `289/256 <= 57/50` is PROVED (exact rational
comparison); but the fold factor `57/50` actually used by the gates is a **COMPUTED
(grid-measured) bound** — it is `sup_{n,t}` over the FINITE grid (measured max `1.1322`
at `n = 48`, decreasing thereafter) resting on a COMPUTED CLT quadratic-profile ansatz
(`L_i propto -i^2`), gated by V16b, **not proved for all `n`**. It is enumerated as
computed clause **(FOLD)** in Section 8.4.

> **Lemma W2 (census window for curvature objects, PROVED read-set).** Any gate
> certifying `Curv_{i<17} := sup_t spread_{i<17}[(K_d * c)_i/c_i]` (or `F_ext`'s
> `T3`-ratio) must sample `c_0, ..., c_17` — the operative corner vector (`c_0..c_16`,
> 17 values) extended by **one** index. A census truncated at `c_16` undercounts
> `Curv_{i<17}` by a measured factor of `1.14`-`1.15` (gate V16b's structural check).

*Why*: the top row's curvature term is `P_16 = (1/4)(rc_16 + 1/rc_15)`, and `rc_16 =
c_17/c_16` needs the 18th c-value. This is not a numerical coincidence; it is the
tridiagonal read-set, confirmed by V16b's direct comparison of the correctly-computed
spread against the one-index-short proxy.

> **Lemma W3 (triangle, PROVED, no hypotheses).**
> `V_17(n) = sup_t spread_{i<17}(T1+T2+T3) <= sup_t [spread(T1) + spread(T2) +
> spread(T3)]`, by subadditivity of `max - min`.

The COMPUTED "alignment" of `T1,T2,T3` (all three monotone in `i`, near-equal to the
sum to `<1%`) is a tightness remark only; the discharge chain (Section 7) never needs
the near-equality, only the `<=` direction.

## 7. THE THEOREM — the composed discharge, parametric in the forcing input

Notation: `B(n)` = the predecessor's step-closed bundle at level `n` (`{caps, LC,
floors >= 0.98 r_i(48,t), sigma <= sigma_max(t), rho_prop@i<17 <= TARGET}`, certified
step-closed there by its own corner census); `V_17(n)` as above; `tau* = 3
log(TARGET) = 0.075855...`.

> **IH `H(m)`:** `B(m)` holds **and** `V_17(m) <= v_m`, `{v_m}` a tracked ceiling (base:
> measured on the grid; step: the recursion below).

> **Composed Theorem (parametric).** Assume: **(G-theta)** the contraction gate
> `theta_tot <= theta*` with `theta* < 1` certified (Section 4's exact `theta~ <= 1/5`
> plus Section 5's band-uniform tangent seminorm plus Lemma W1's window fold; gate
> V15-IA/V16/V16b — `theta*` is itself `theta_band`, V15-IA's certified output);
> **(G-F)** the forcing gate `F(m) <= Phi(m)` certified (gate V17); **(Base)** the deep
> grid establishes `H(m)` for `48 <= m <= J*` (gates V13-style census + V18). Then, for
> the arithmetic recursion `v_m := theta* v_{m-1} + Phi(m-1)`, **if `v_m <= tau*` for
> all `m > J*`**, `H(n)` holds for all `n >= 48` — i.e. `rho_prop@i<17(n) <= TARGET` for
> all `n`, and **(PROP-TAIL) is DISCHARGED**.

**The step `H(n-1) => H(n)`, labeled:**
- **(i) V-recursion.** By the exact cascade (Lemma 2, PROVED structure) and `osc(sum)
  <= sum osc` (Lemma W3, PROVED), `V_17(n) <= osc(T2) + osc(T1+T3)`. Gate (G-theta)
  bounds the `T2` + sibling multiplier by `theta* V_17(n-1)` (Sections 4-6: `theta~ <=
  1/5` exact + the tangent seminorm + the window fold); gate (G-F) bounds the
  curvature-only residual `osc(T1+T3)|_{g equiv const} = F(n-1) <= Phi(n-1)`. Hence
  `V_17(n) <= theta* V_17(n-1) + Phi(n-1) <= theta* v_{n-1} + Phi(n-1) =: v_n`.
  **PROVED-given-gates.**
- **(ii) Reduction.** Lemma 1 (PROVED): `log rho_prop@i<17(n) <= (1/3) V_17(n) <= (1/3)
  v_n`. If `v_n <= tau*`, `rho_prop@i<17(n) <= TARGET` — the `rho_prop` clause of
  `B(n)`. **PROVED-given (i) + the arithmetic slot.**
- **(iii) Box closure.** With `rho_prop@i<17(n) <= TARGET` established, the
  predecessor's own step machinery (its corner census + assembly) closes the remaining
  clauses of `B(n)` (`{caps, LC, floors, sigma}`) exactly as it already does in the
  predecessor packet. **PROVED (sufficiency)-given-gates** (that packet's own label for
  this step). `H(n)` holds. **Floor persistence for `n > 500` specifically** is not
  re-derived here: it composes from the predecessor packet's monotone-drift machinery
  re-anchored at the `(500, 99/100)` floors (`rc_i` drifts upward in `n`, so the
  level-500 floors persist upward). That machinery is **COMPUTED in the predecessor and
  imported** here — enumerated as computed clause **(FLOOR-PERSIST)** in Section 8.4.

Base = the deep grid (`48 <= n <= J*`), well-founded (single intra-level edge,
acyclic, matching the predecessor's own joint-induction argument). **Joint clauses
(this revision's bookkeeping):** the induction's `H(m)` also carries LAM-INV's
field-membership clause, and the (C'-CAP) node-census bound consumed by the field's
step at level `n` reads `H(n-1)`'s V-ceiling — acyclic per level, same shape as gate
SIB-CERT's lemma consuming the IH's `rho_prop` clause (Section 8.4's (C'-CAP) entry
spells out the step order).

### 7.1 The arithmetic slot — INSTANTIATED (R-a, the deep-base equilibrium)

Iterating `v_n = theta* v_{n-1} + Phi(n-1)` (`theta* < 1`, elementary geometric-sum,
PROVED):

| route | forcing `Phi(m)` | closed bound `v_n` | slot condition | grid `J*` |
|---|---|---|---|---|
| **R-a** (deep-base, constant) — **INSTANTIATED** | `F_box(500,99/100) = 0.02690175` (certified constant, gate V17-IA) | `max(v_500, F_box/(1-theta_band)) = 0.06759647` | `F_box/(1-theta_band) = 0.06759647 <= tau* = 0.07585533` — **CLEARS, 10.9% margin** | `J* = 500` (gates F3/MAG-BOX/V15-IA/V17-IA/V18) |
| R-b (sandwich, `O(1/n)`) — strengthening, not needed | `c_1/m`, `c_1 = 3/8` (leading, at `kappa=3/2`) | `[c_1/(1-theta*)]/n * (1+o(1))` | crosses `tau*` at `n* approx c_1/((1-theta*)tau*)` | `~250-300` |
| R-c (sharp, `O(1/n^2)`) — strengthening, not needed | `B_crv/m^2`, `B_crv/(1-theta*) = 282` (explained, `= 185/0.657`) | `[B_crv/(1-theta*)]/n^2 * (1+o(1))` | `<= tau*` for `n >= 62` | `~62-80` |

**R-a closes the slot.** With the certified `theta_band = 0.6020244` (gate V15-IA,
Section 5) and the certified `F_box(500, 99/100) = 0.02690175` (gate V17-IA, Section
8.1), `F_box/(1-theta_band) = 0.06759647 <= tau* = 0.07585533` — a 10.9% margin — so
`v_n <= 0.06759647` for all `n > 500`, and by (ii), `log rho_prop@i<17(n) <=
(1/3)(0.06759647) = 0.02253216 < ln(1.02560749) = 0.02528511` for all `n >= 500`. The
deep grid (gate V18) directly covers `48 <= n <= 500`. **Every hypothesis of the
Composed Theorem is discharged on finite checks, with `theta*` itself a certified
band-uniform constant, not an asserted one** — no decay-rate input, no Edgeworth content,
Edgeworth-free and mu-sign-free throughout. This closes the slot for the
**forced-proportional surrogate**; Section 8.4's SIB-CERT deep anchor separately closes
it for the real cascade (DISCHARGING (SIB-BAND)). The remaining computed inputs to this
certified chain (the magnitude box the gates box-max over, the window fold, floor
persistence) are enumerated as computed clauses in Section 8.4, which is why the STATUS
is CONDITIONAL. R-b/R-c remain open as
**strengthenings** toward the sharp `C/n^2` law (Section 8.2-8.3) — genuinely
interesting, but **not needed** for this discharge.

### 7.2 The firewall (what this theorem does NOT give)

- **Magnitude `kappa_c` is untouched.** The whole chain is **spread-only** (Lemma 1
  bounds a spread; `V_17` is a spread; `T1/T2/T3`'s common reference scalar `Lambda` is
  invariant and never appears in the bound). It is structurally incapable of proving
  `kappa_c -> 1` — consistent with the flat-at-`~1.29` measured magnitude. Any claim
  about the magnitude would be a category error against this frame.
- **Window-specific.** The theorem is for the **operative window `i < 17`** at the
  target `1.02560749`. `i < 10` decays faster and is informational only (as in the
  predecessor); nothing is claimed for `i >= 17` or window-free.
- **The sharp `C/n^2` law** still requires the **R-c** row specifically (Section 8.3,
  CONJECTURAL) — the discharged R-a route gives a constant-forcing equilibrium
  sufficient for (PROP-TAIL), not the sharp rate.
- **General `K` / other windows** remain outside this packet's scope (unchanged from
  the predecessor).
- **The binding scope pin** (repository experimental-ledger track only) is stated once,
  in full, in Section 12 — it applies here without repetition.

## 8. THE RESIDUAL LADDER — R-a INSTANTIATED (this packet); R-b/R-c open strengthenings

Section 7.1's arithmetic slot needs exactly one of three statements. **R-a is
INSTANTIATED**, discharging (PROP-TAIL) modulo the Section 8.4 computed clauses; R-b and
R-c remain open **strengthenings** toward the sharp `C/n^2` law — genuinely interesting
future work, but not needed for the discharge itself.

### 8.1 (R-a) Deep-base box feasibility — INSTANTIATED

The certified box (caps `rc_i <= 1`; floors `rc_i >= f* rc_i(J0,t)`; output-LC)
certifies, via the curvature normal form `Curv(n) = sup_t spread_{i<17}[(K_d*c)_i/c_i]
= sup_t spread_{i<17}(P_i)` (`P_i` as in Lemma W2), only a **CONSTANT** bound in `n` —
the floors are level-`J0` constants, and nothing in caps/floors/LC shrinks with `n`.
At the **shipped-then** base `J0 = 48` this constant missed the requirement by `~3.9x`
(`box F_const(48) = 0.196` vs required `(1-theta_tot)tau* = 0.657 * 0.075855 = 0.0498`,
using the edge-only `theta_tot=0.343` reading; the corrected sup-over-`t` reading up to
`0.376` worsens the miss slightly further, to `~4.1x`). **Re-basing closes it.** Raising
the certified base to `J0* = 500` — re-running the corner census with floors anchored
there (gate F3: positivity, LC-compatibility, and the `i=0` halving convention all
verified over the 41-parent grid) and certifying the forcing at that base via an exact,
non-sampled interval-arithmetic enclosure (gate V17-IA) — gives, at the anchor
`f* = 99/100`:

```
    F_box(500, 99/100)          = 0.02690175  (certified sup, width-2 minced-IA, exact Fraction)
    required (1-theta_band)*tau* = 0.03018857 (theta_band = 0.6020244, gate V15-IA's certified band-uniform output)
    margin                      = 10.9%       (CLEARS)
```

**Method, honestly.** A naive "corner-sample the two window endpoints `i=0,16` and rely
on the child ratio profile being monotone across the whole box" gives a numerically
close but *unrigorous* estimate (it rests on a monotonicity fact that is true on the
measured/realized cascade but not proved to hold at every point of the certified box).
Gate V17-IA instead computes a marginal interval for **every** index `i = 0..16`
(mincing each ratio's range and enclosing every LC-feasible adjacent panel pair,
in exact Fraction arithmetic, no sampling), which is provably a valid upper bound
regardless of that monotonicity question. Deriving the threshold: Lemma 1 gives
`log rho_prop <= (1/3)V_17(n)`; the V-recursion at constant forcing gives the
equilibrium ceiling `F_box/(1-theta_band)`, which must sit `<= tau*` — exactly this
gate's check (`tau*` enters as the exact-Fraction lower bound `TAU_STAR_FR =
0.075855330599169`, and the final comparison is exact Fraction). **Status: R-a CLEARED
at `(500, 99/100)` with a 10.9% margin, conditional on the Section 8.4 computed
clauses.** The contraction gate `theta*` is a certified band-uniform constant (gate
V15-IA), not an asserted one resting on a grid measurement; the grid census `theta_tot`
is retained purely as an informational robustness cross-check (Section 0), comfortably
inside `theta_band` at every level tested to `n=500`.

### 8.2 (R-b) The two-sided sandwich — open strengthening, not needed

> **Sandwich hypothesis.** On the operative window, uniformly in `t` and for `n >=
> J0`: `l_0 := log(rc_0) >= -c_0/n` with `c_0 = 5/8` (a rational `>= beta = 0.6191`);
> and `D2_i := l_i - l_{i-1} >= -kappa/n` for `1 <= i <= 16`, `kappa = 3/2` (a rational
> `>= kappa_hat`, the measured worst-case constant). The upper sides (`l_i <= 0`,
> `D2_i <= 0`) are log-concavity, already available (proved on one branch, computed in
> general).

> **Lemma C2 (sandwich => `O(1/n)`, PROVED given the hypothesis).** Under the
> sandwich, `|l_i| <= (c_0 + 16 kappa)/n` on the window, giving
> `Curv(n) <= (kappa/4)(1/n) + O(1/n^2) = O(1/n)` with **leading rational constant
> `c_1 = kappa/4 = 3/8`**.

**Honest status of the hypothesis.** Neither one-sided bound is proved. Both are
*drift-type* (`1/n`) statements, and they inherit exactly the difficulty (R-a)
identified: the certified box gives only constant lower bounds on log-ratios, not
`1/n` ones — the sandwich's content is genuinely new, not a repackaging of the box. The
**natural proof handle is a quantitative no-spike tower**: the predecessor's no-spike
hierarchy (`ns(Delta), ns^2(Delta), ...`, entrywise nonnegative at every level tested)
is a *sign* statement; a **quantitative** bound on its second application would pin
`D2_i >= -kappa/n` directly. This quantification is not carried out here — it is the
single most promising open sub-problem this packet identifies, since it would close
(R-b) non-circularly and without any Edgeworth-type input. **Label**: the two
constants `c_0 = 5/8`, `kappa = 3/2` are COMPUTED (measured `kappa_hat approx 1.442`,
`c_0 approx beta approx 0.619`, both comfortably inside the stated rationals); Lemma
C2 is PROVED *given* the sandwich; the sandwich itself is CONJECTURAL (unproved, no
counterexample found either).

### 8.3 (R-c) The single-branch Edgeworth-1 curvature lemma — open strengthening, not needed

> **Residual Lemma (curvature-uniformity).** `Curv(n) = O(1/n^2)` — the kernel-smoothing
> factor `(K_d * c)_i / c_i` is index-uniform over the operative window to *second*
> order, not merely bounded.

This is the sharp form: with `l_i = log rc_i`, the exact-Gaussian profile has `l_i -
l_{i-1}` constant in `i`, so `Curv`'s leading term vanishes identically and only the
`O(1/n^2)` deviation from Gaussian survives — this is genuine Edgeworth content, but a
**single-branch, single-level** statement about one convolution, not the coupled
two-branch remainder a naive approach to (PROP-TAIL) would otherwise require. If
proved, it gives the **explained constant** `B_crv/(1-theta*) = 185/0.657 = 282`,
matching the independently-measured `V_17(n)*n^2` almost exactly (Section 7.1) — i.e.
the `C/n^2` law with a constant that is a fixed-point balance, not a fit. **Label**:
CONDITIONAL / CONJECTURAL — not attempted beyond the identification of its exact scope
(a relative-`O(1/n^2)` Edgeworth expansion of a single convolution, uniform in `i` over
a fixed window) in this packet.

### 8.4 Computed clauses (the remaining computed inputs to the certified chain)

The discharge is a certified-census theorem **modulo** the following two computed
inputs — **(FOLD)** and **(FLOOR-PERSIST)** — plus three further clauses, (LAM-BOX),
(SIB-BAND), and (C'-CAP), that are **DISCHARGED** below (not open — recorded in this
section because their discharge is itself a computed-census fact resting on a named
gate, not an unconditional proof). Each open item is monitored by a named gate; as of
this revision no monitored-only literal remains (the (C'-CAP) constant, the last one,
is now a PROVED floor-box bound with its monitor retained as a cross-check). The two
open clauses' existence is exactly why the STATUS is **CONDITIONAL** rather than PROVED
(PROVED would require zero computed clauses).

**(LAM-BOX) — the sibling-proportionality magnitude box. DISCHARGED-conditional
(gate LAM-INV, full mode only).**

*What the clause was about.* Both load-bearing gates box-max the seminorm/forcing over a
fixed magnitude box — `lam`, `Lambda^+`, `Lambda^-` — that was, before this revision, a
**measured + padded** range (six silent literals: two endpoints each), monitored by gate
MAG-BOX but not proved to hold for all `n`. `DERIV_LAMBOX.md` (derivation lane) upgrades
this to **PROVED invariant intervals**, conditional on the existing floor box, the
existing finite base-case census, an a-posteriori Lipschitz self-check, and one
remaining generous monitored constant.

**Two identities (compressed from `DERIV_LAMBOX.md` Sections 1 and 3.2).**

> **(I1) Exact windowed mass recursion.** Write `M_w(c) := sum_{i<W} c_i`, `W = OPWIN =
> 17`. Telescoping the tridiagonal kernel `K_d = (1/4,d,1/4)`'s own definition
> (even-extended at `i=0`) over the window `i < W`:
> ```
>    sum_{i<W} (K_d * c)_i  =  a(t) M_w(c)  -  (1/4)(c_0 - c_1)  -  (1/4)(c_{W-1} - c_W).
>                                    bulk        i=0 halving term    window-edge leak
> ```
> *Proof.* `(1/4) sum_{i<W} c_{|i-1|} = (1/4)(M_w + c_1 - c_{W-1})` (the `i=0` tap folds
> to `c_1` by even extension); `d sum_{i<W} c_i = d M_w`; `(1/4) sum_{i<W} c_{i+1} =
> (1/4)(M_w - c_0 + c_W)` (`c_W` is one index PAST the window). Summing and using
> `a = 1/2+d` gives the identity. **PROVED** — verified EXACTLY in Fraction arithmetic
> (residual algebraically `0`, not merely float-small) by gate LAM-INV's own live
> spot-check and, independently, by the concurrent lab lane (`LAB_LAMBOX.md` Q2: residual
> `0` over 40 checks, converting the verifier's own float `c`/`d` to `Fraction` before
> convolving, so `a(t)` is reconstructed as `1/2+Fr(d(t))`, the exact value `conv_even`
> itself computes with). The `E_W = c_{16}-c_{17}` term reads `c_17`, **one past** the
> operative `i<17` window — but only via `rc_16 = c_17/c_16 in [f_16,1]`, and gate F3
> already certifies the floor family over `i<18` (`FLOOR_WIN=CWIN=18`), so `rc_16` sits
> **inside** the certified floor window: no new hypothesis.

> **(I2) The Lambda log-derivative identity.** `Lambda^pm_mass = (log S^W)'(t_pm)`,
> `S^W(s) := sum_{i<W} c_i(G(s))` — window-generic; **the field instantiates `W = 17 =
> OPWIN`**, matching (I1) and the `gamma`/`C'` floor-box covers (window-coherence fix,
> this revision — see Section 10; an earlier revision cited `W = 18` here while (I1)
> and `gamma` were at `W = 17`, one edge term of slippage between the field and its
> realized comparisons; the monitors now compare against the `W = 17` object). *Proof.* `L_i := d/dt log c_i` by definition, so
> `L_i c_i = c_i'`; summing, `sum_i L_i c_i = sum_i c_i' = d/dt sum_i c_i`; dividing by
> `sum_i c_i` gives `d/dt log(sum_i c_i)`, i.e. the mass-weighted mean of `L` over the
> window equals the log-derivative of the windowed mass. **PROVED** (elementary algebra;
> confirmed to `1e-11` by finite-difference cross-check in the derivation lane).

**The enclosure (`DERIV_LAMBOX.md` Sections 2-3, gate LAM-INV Section 11).** The pure
`a`-weighted mass operator `(TS)(t) := a(t_+)S(t_+) + a(t_-)S(t_-)` is exactly positive,
hence Birkhoff-contracting to a fixed *ray* (projective direction) — not a fixed point:
`a(t_+)+a(t_-) = 1 + (1/2)cos(2 pi t/3) in [1.25, 1.47]`, strictly `> 1`, so `T` grows any
starting field by a dominant-eigenvalue-like factor every pass. Since `lam`/`Lambda` are
ratio / log-derivative objects, invariant to any `t`-independent rescaling of `S`, gate
LAM-INV represents `S`/`Lambda` as interval fields on a fine grid (`NG = 3841` points on
`[1/6,1/2]`), pre-converges a candidate field once in float (Birkhoff power iteration,
rescaled every pass by its own max — the standard projective-power-iteration
normalization — for `S`; the coupled `Lambda` recursion of (I2)'s differentiated form
against the resulting `lam` envelope, `400` passes, matching `DERIV_LAMBOX.md`'s own
validated proto5/6 setting), then **certifies** that candidate with **one rigorous
exact-Fraction forward pass**: `T(S)/sc_exact subset S` (`sc_exact := max_t T(S)_hi(t)`,
derived from that same pass, not an independent input — the ray-normalization), and the
analogous one-pass check for the coupled `Lambda` field. The comparison tolerance is
`GMAX` (mass) / `CPRIME` (Lambda), applied **only at this final comparison**, not by
perturbing the field itself — additive field-padding was tried and found
counterproductive (`sc_exact`'s own self-referential dependence on the widened field
amplifies hi-side widening into the lo-side gap; see the verifier's module comment above
`gate_lam_inv`). Both one-pass checks are **rigorous** (house V17-IA style: float error
is dwarfed by the documented outward slops; the final comparisons are exact Fraction).
A-posteriori self-checks confirm the Lipschitz constants used to build the between-grid
brackets are valid: `sup|Lambda| = 1.1595 <= LIP_S = 1.20`, `sup|Lambda'| = 2.4897 <=
LIP_L = 2.60`.

**Proved intervals vs the shipped boxes** (gate LAM-INV, `(J0*,f*) = (500, 99/100)`,
`NG = 3841`, `GMAX = 0.005`, `CPRIME = 0.006`):

| object | proved interval (LAM-INV) | shipped box (post-widening) | inside? | headroom |
|---|---|---|---|---|
| `lam` | `[0.767193, 0.929926]` | `[0.72, 0.95]` | **yes** | `+0.047` / `+0.020` |
| `Lambda^+` | `[-1.159560, -0.868700]` | `[-1.17, -0.82]` | **yes** | `+0.0104` (was `+0.0004` pre-widening) |
| `Lambda^-` | `[-0.650454, -0.360426]` | `[-0.66, -0.35]` | **yes** | `+0.0095` / `+0.0104` |

**Provenance table** (which check proves which endpoint; valid for every `n >= 48`
composing with the existing base-case grid; consumed where):

| endpoint | proved by | inputs | consumed by |
|---|---|---|---|
| `lam` lo/hi | LAM-INV mass-field one-pass invariance + `sc_exact` ray-normalization, `GMAX`-tolerance comparison | F3 floors (i<17) via `a(t_pm)` brackets; `LIP_S` a-posteriori | V15-IA, V17-IA (box-max lam, MINCE); MAG-BOX (empirical cross-check) |
| `Lambda^+` lo/hi | LAM-INV coupled Lambda-field one-pass invariance, `t_+ in [0.389,0.5]`, `CPRIME`-tolerance comparison | mass-field envelope + `(log a)'(t_pm)` + `LIP_L` a-posteriori | V17-IA (nc,nl), SIB-CERT, SIB-BAND (informational); MAG-BOX |
| `Lambda^-` lo/hi | LAM-INV coupled Lambda-field one-pass invariance, `t_- in [0.167,0.278]` | same at `t_-` | V17-IA, SIB-CERT, SIB-BAND; MAG-BOX |

**Conditional basis** — the *same* conditional basis the other load-bearing gates already
stand on: the existing F3 floor box; the existing finite base-case census (gates
MAG-BOX/V18, `n in {48..800}`, cited not re-derived by LAM-INV); this gate's own
a-posteriori Lipschitz self-check; and the `(C'-CAP)` clause (below — a generous
monitored constant when this upgrade first landed, and **itself DISCHARGED-conditional
as of this revision** by the floor-box node census in its own entry). `gamma <= GMAX` (the branch-mass correction fraction) is
itself **PROVED** here, in exact Fraction, from the F3 floor box alone (not merely
monitored): `Delta_0 = c_0(1-rc_0) <= c_0(1-f_0)`, `E_W = c_16(1-rc_16) <= c_0(1-f_16)`
(`c_16<=c_0` by monotonicity), and `M_w/c_0 >= Q := sum_{k=0}^{16} prod_{i<k} f_i` (each
`rc_i >= f_i`, the floor box itself), giving `gamma <= (1/4)[(1-f_0)+(1-f_16)]/(a_lo Q)`
— computed exact bound `0.004318 <= GMAX = 0.005` at the shipped anchor, `13.6%` margin.

**Risk register R1 (the load-bearing `Lambda^+` floor) — both mitigations.**
- *The risk.* At the *original* box floor `-1.16`, the proved `Lambda^+` interval's
  headroom is razor-thin (`+0.0004`) and **fails outright at `2x` the measured
  correction-derivative bound** (`CPRIME = 0.008 -> Lambda^+_lo ~ -1.163 < -1.16`,
  confirmed live by the verifier's `laminv-floor` tamper). The enclosure overhead
  (grid + Lipschitz + the `CPRIME` slop) eats nearly all of the realized headroom, and
  `CPRIME` dominates.
- **Mitigation (b) — low-risk ship, TAKEN.** Widen the `Lambda^+` floor `-1.16 -> -1.17`
  (a `0.86%` widening). Every consumer that box-maxes over `LAP_LO_F` is re-run over the
  wider box: V15-IA is **structurally unaffected** (`theta_band` depends only on `lam`
  and the LC ratio box, never on `Lambda^+`/`Lambda^-` — confirmed bit-identical
  before/after); V17-IA, SIB-CERT, and the SIB-BAND exhibit all shrink by **well under
  1%** (see the verifier's own printed margins, and the builder round's run log for the
  exact before/after numbers). The proved `Lambda^+` headroom against the *widened* floor
  is `+0.0104` — comfortable, no longer razor-thin.
- **Mitigation (a) — full rigor, TAKEN (this revision).** The exact floor-box bound on
  the correction derivative's drop is derived and gated: see the (C'-CAP) entry below
  (DISCHARGED-conditional; certified node census, worst bound well under `CPRIME`,
  the identity + the three outward ingredients spelled out there). The monitored
  constant `CPRIME = 0.006` remains in the recursion as the applied slop, but it is now
  a **proved** cover, not merely a generous one; the a-posteriori monitor (measured
  `~0.001-0.003`) is retained as the empirical cross-check.

**Honest labels.** Net effect of the LAM-INV revision: **"six silent computed literals,
grid-monitored, unproved for all `n`"** became **"invariant intervals on the same
conditional basis as the load-bearing censuses, plus one generous monitored cap"** — the
`(C'-CAP)` constant was the *only* new computed content (and is itself
DISCHARGED-conditional as of this revision, see its entry); `gamma<=GMAX` moved from
monitored to proved; the base case and floor box were already-named, already-monitored
inputs the rest of the chain depends on regardless. `lam` and `Lambda^-` are solidly
comfortable; `Lambda^+`'s floor was thin and is now widened to match.

- *Gate*: **LAM-INV** [core, FULL MODE ONLY] proves the invariant intervals (above).
  **MAG-BOX** [core] continues to verify that the realized `lam`, `Lambda^+`,
  `Lambda^-`, and the per-entry ratios `rho_i = c^+_i/c^-_i` lie inside the (now proved)
  box at every grid level — now the **empirical cross-check** of LAM-INV's proved
  intervals, not the sole evidence for them.
- *Evidence*: realized `lam in [0.7759, 0.9190]`, `Lambda^+ in [-1.1429, -0.8883]`,
  `Lambda^- in [-0.6334, -0.3788]`, per-entry `rho_i in [0.7734, 0.9259]` — all inside
  the proved boxes; `Lambda^+_mass`'s own headroom against the widened floor is `0.0271`
  (was `0.0172` pre-widening); the worst headroom over the WHOLE proved-conditional
  category (`lam`, mass-weighted `Lambda^+/-`, every `rho_i`) is `0.0241`, at `rho_16`,
  `n=48`. The arithmetic-mean `Lambda^+/-` variants (COMPUTED-monitored only — NOT
  covered by the LAM-INV enclosure, and per LAB_LAMBOX's Q1 finding they WIDEN with
  depth) are the overall tightest, `0.0196` at `n=48`. Gate MAG-BOX also now cross-checks
  the realized-vs-field correction-derivative `C'` at its own 6 grid levels x 41
  parents (broader than gate LAM-INV's own sparser one-anchor sample; W=17 field object
  per the round-4 window-coherence fix, Section 10): worst `0.0027`
  vs `CPRIME = 0.006`, comfortable.
- *Remaining open item*: **NONE as of this revision** — mitigation (a), the exact
  floor-box bound on `C'`, is carried out below ((C'-CAP), DISCHARGED-conditional),
  removing the last monitored-only content from this clause. (LAM-BOX)'s conditional
  basis is now: the floor box, the finite base-case census, the a-posteriori Lipschitz
  self-check, and — via the (C'-CAP) bound's own inputs — (FOLD) and the joint IH.

**(SIB-BAND) — the forced-proportional surrogate vs the real cascade. DISCHARGED
(anchored census, gate SIB-CERT).**
- *Asserts (what the clause is about)*: the load-bearing gates V15-IA/V17-IA, at the
  shallow anchor `(J0*, f*) = (500, 99/100)`, certify only the **forced-proportional
  surrogate** `c^+ = lam c^-`; the real cascade is non-proportional
  (`c^+_i = lam w_i c^-_i` by the IH `rho_prop <= R*`, per-entry sibling wobble
  `w_i in [1/R*, R*]`). Whether that surrogate's coverage extends to the real cascade is
  exactly this clause.
- **The GEOMETRIC-CENTER LEMMA (discharges the clause, 3 lines, no assumption beyond
  (LAM-BOX)).** Fix a level `n` and parent `t`. Let `rho_i := c^+_i/c^-_i` (the realized
  per-entry sibling ratio at that level/parent) and suppose (LAM-BOX) holds: every
  `rho_i in [LAM_LO, LAM_HI] = [0.72, 0.95]` (gate MAG-BOX's own hypothesis). Set
  `lam_gc := sqrt(min_i rho_i * max_i rho_i)`. Then:
  1. `min_i rho_i <= lam_gc <= max_i rho_i` (the geometric mean of two positive numbers
     lies between them), and both `min_i rho_i, max_i rho_i in [LAM_LO, LAM_HI]` by
     (LAM-BOX) — so `lam_gc` is *itself* a legal point of the **same, already-monitored**
     lam box. No new box, no new assumption.
  2. `w_i := rho_i / lam_gc` satisfies `max_i w_i = sqrt(max_i rho_i / min_i rho_i) =
     sqrt(rho_prop@i<17(n)) <= sqrt(R*)` by the governing IH `rho_prop@i<17 <= R*`, and
     symmetrically `min_i w_i >= 1/sqrt(R*)` — so `w_i` lies in the **geometric-center
     half-band** `WOB_HALF := [1/sqrt(R*), sqrt(R*)]` for every `i < 17` (**the IH's own
     window — boundary slot: see the BOUNDARY ANNEX immediately below**), from the IH
     alone.
  3. Hence the *real* one-step pair `c^+_i = lam_gc * w_i * c^-_i` — with `lam_gc` in the
     lam box and `w_i` in `WOB_HALF` per-entry, for `i < 17` — is exactly the object the
     wobble censuses (`theta_band_wobble_certified`/`F_box_wobble_certified`) already
     box-max over on their `i<17`-indexed slots: lam ranges over the full lam box
     (`lam_gc` qualifies, by 1), and each in-window `w_i` ranges *independently* over
     `WOB_HALF` (a safe superset of the `lam_gc`-linked real `w_i`, by 2). A census
     clearing the equilibrium threshold, WITH the boundary slot's own hypothesis in place
     (annex below), therefore covers the **real, non-proportional cascade** — not merely
     the `lam_gc == const, w_i == 1` forced-proportional slice V15-IA/V17-IA certify. No
     assumption is used beyond (LAM-BOX) (already a named, monitored clause) and the IH
     (already the induction hypothesis every gate in this chain assumes) — **for the
     in-window slots**; the boundary slot needs one further, separately-monitored
     hypothesis, below.

  **BOUNDARY ANNEX (round-2 correction; PI review caught this).** (a) The IH
  `rho_prop@i<17(n-1) <= R*` bounds `rho_i`, hence `w_i`, only for `i < 17` — it says
  nothing about `rho_17`. (b) The two wobble censuses range three coordinates `(u,v,x)`
  per row `i` — `u = w_{i-1}`, `v = w_i`, `x = w_{i+1}` (the tridiagonal kernel's three
  neighbors) — over every row `i = 0,...,16`. At row `i = 16` (the *top* of the window),
  `x = w_{17}`: **one index past the IH's window**. This is the *only* out-of-window
  slot in the whole census: the row coefficients `(a,b) = (rc_{i-1}, rc_i)` come from
  gate F3's re-certified floor family, itself valid to `i < 18` (`FLOOR_WIN = CWIN = 18`,
  Section 6), so `a,b` are covered; `u,v` at every row satisfy `i-1 <= 15` and `i <= 16`,
  both `< 17`, so always in-window; `lam, Lambda^+, Lambda^-` are the *shared* magnitude
  scalars gate MAG-BOX already monitors directly (not per-entry), unaffected by this
  question. Only `x` at `i=16` reaches `w_{17}`. (c) **The naive "same band as the
  window" claim is FALSE at shallow levels.** Measured directly (`w_17(n) :=
  (c^+_{17}/c^-_{17}) / lam_gc`, `lam_gc` as above, over `i<17`): at `n=48`,
  `w_17 in [1.005459, 1.016780]` — the upper end, `1.016780`, EXCEEDS `WOB_HALF`'s own
  outward bracket `1.012723`. So before this correction, the top-row census silently
  used a band `w_{17}` does not actually satisfy at shallow `n`; the boundary slot
  genuinely needed its own hypothesis, not a rhetorical one. (d) **SIB-CERT's operative
  domain is `n > 800`** (the deep grid, gate V18, covers `48 <= n <= 800` directly on
  the grid — Section 11); at that depth the measured `w_17` is far tighter:
  `w_17(800) in [1.000018, 1.000056]`, decaying like `C/n^2` (`C ~ 36`, matching the
  window's own `Curv = O(1/n^2)` shape, Section 8.3) — comfortably inside a much smaller
  box, `W17 := [999/1000, 1001/1000] = [0.999, 1.001]` (`>= 6x` headroom against the
  realized range on the monitored grid below). Gate **MAG-BOX** now monitors `w_17`
  against exactly this box, over `n in {500,550,600,650,700,750,800}` (`W17_GRID`,
  SIB-CERT's own operative domain — the check is not attempted, and not claimed, at
  shallow `n` where (c) shows it would be false) — the *same epistemic status the*
  `lam`/`Lambda^pm` *boxes had before gate LAM-INV*: a **(LAM-BOX)-class COMPUTED
  hypothesis**, monitored not proved, honest where before there was silence. `w_17`
  itself is NOT covered by LAM-INV's enclosure (which proves the i<17/i<18-window
  `lam`/`Lambda^+`/`Lambda^-` boxes only) and remains open at this status. (e) The
  full-band shallow-anchor
  **exhibit** gate (`gate_sibling_band`, informational, unchanged by this correction —
  it passes no `boundary_band` and its printed numbers are byte-identical to before) is
  unaffected in spirit: it is already marked FAIL, and its "the extension does NOT
  close" message is, if anything, *reinforced* by (a)–(c) — an out-of-window `w_17` with
  no band at all only makes that shallow-anchor non-closure more clearly expected, not
  less. Gate **SIB-CERT** (below) is the one that changes: it now passes
  `boundary_band = (W17_LO_F, W17_HI_F)`, routing *only* the `i=16` row's `x`-slot to the
  `W17` box instead of `WOB_HALF`, leaving every other slot (`u,v` everywhere; `x` at
  `i<16`) untouched.
- *Gate*: **SIB-CERT** [core, full mode only] re-runs the geometric-center half-band
  censuses at a **deep anchor**: `J0_SIB = 800`, floor pad `PAD_SIB = 999/1000`, band
  `WOB_HALF = [1/sqrt(R*), sqrt(R*)]` for the in-window slots (the *outward* rational
  bracket on `sqrt(R*)`, `_SQ_HI`, already used by the shipped `gate_sibling_band`
  exhibit — SIB-CERT additionally self-checks `_SQ_HI * _SQ_HI >= R_STAR_FR` every run,
  so an inward (unsound) bracket cannot silently pass), PLUS `boundary_band =
  W17 = [999/1000, 1001/1000]` for the single boundary slot (annex above). Both
  censuses are exact-Fraction interval arithmetic, identical in kind to
  V15-IA/V17-IA/SIB-BAND, just re-anchored deeper, re-banded tighter, and — this
  revision — honest about the one slot that needs a separate box.
- *Evidence (certified numbers, gate SIB-CERT at the shipped deep anchor, round-2
  boundary-corrected)*:
  ```
      theta_band_wob(800, 999/1000)  = 0.6020655   (exact Fraction 1204131/2000000)
      F_box_wob(800, 999/1000)       = 0.0279431   (exact Fraction, width-2 minced-IA,
                                                      geometric-center half-band for i<17
                                                      PLUS the W17 boundary box at i=16)
      threshold (1-theta_wob)*tau*   = 0.0301855   (exact Fraction
                                                      60370906108630032861/2*10^21)
      margin                         = +7.4%       (F_box_wob <= threshold —
                                                      CLEARS, exact-Fraction compare)
  ```
  (Exact Fraction numerator/denominator strings for all three are recorded by the gate
  into `_SIBCERT_CERT` and transcribed verbatim into the packet's cert JSON.) The
  boundary-slot fix (annex above) TIGHTENS this value relative to round 1's (pre-fix)
  `F_box_wob = 0.0287228`, margin `+4.6%` — restricting one census slot's range from
  `WOB_HALF` to the narrower `W17` box never increases a box-max, and the round-2 value
  confirms it: `F_box_wob` drops to `0.0279431`, margin improves to `+7.4%`.

  The **sounding trend** with anchor depth below is retained from round 1's sounding
  (pre-boundary-fix: the `x`-slot at `i=16` used `WOB_HALF`, not `W17`, at every anchor
  tested) as a qualitative illustration of *why* a deep anchor is needed at all — the
  MISS-MISS-CLEAR shape is not expected to flip from the (small, one-slot, tightening-
  only) boundary correction, but re-sounding `J0=600/700` under the corrected code was
  out of scope for this round (only the shipped anchor, `J0=800`, was re-verified
  exactly): at the same pad `999/1000`, `J0=600`: `F_box_wob = 0.0331175` vs threshold
  `0.0298019`, margin **-11.1% (MISS)**; `J0=700`: `F_box_wob = 0.0305601` vs
  `0.0299836`, margin **-1.9% (MISS)**; `J0=800`: **CLEARS** — monotone improvement with
  depth (deeper anchor -> looser floors -> smaller `F_box`, while `theta_band_wob` stays
  comparatively flat). The **full** (non-geometric-center) band `[1/R*, R*]` still
  misses even at the deep anchor (same pre-fix sounding): `F_box_wob(800, 999/1000)
  = 0.0445412` vs threshold `0.0290492`, margin **-53.3% (MISS)** — the tightening from
  full band to geometric-center half-band is what makes the deep anchor sufficient; the
  full band was already shown (earlier in this section, historically) to miss at *every*
  depth. See gate SIB-CERT's report line and the note's verifier map (Section 11) for
  the full gate text, and `experimental/scripts/verify_dense_shell_prop_tail_reduction.py`
  tampers `sibcert-sqrt`/`sibcert-pad`/`sibcert-band`/`w17-shrink` for the isolated
  negative controls (the last catches gate MAG-BOX's own boundary-slot monitor, not
  SIB-CERT itself).
- *Honest dependence (what the discharge still rests on)*: the SIB-CERT discharge adds
  **no new open clause** — it is a corollary of (LAM-BOX) plus the IH, both already
  named — but it does **inherit** the existing computed clauses at the deep anchor
  specifically: (LAM-BOX) itself (the per-entry `rho_i` boxes must contain the realized
  ratios for all `n`, not merely the `MAG_GRID` levels gate MAG-BOX actually samples —
  unchanged in kind from the shallow anchor, just relied on more directly here, since the
  lemma's soundness is conditional on it holding pointwise) — **now including the
  boundary slot's own `W17` box** (the annex's `(LAM-BOX)`-class hypothesis, monitored
  by MAG-BOX over `W17_GRID = {500,...,800}` only, i.e. exactly SIB-CERT's own operative
  domain — this is a new *instance* of the (LAM-BOX) clause's kind, not a new named
  clause); (FOLD) (the `<=57/50` child-window fold enters `theta_band_wob` exactly as it
  enters `theta_band`, via the same `theta_band_wobble_certified` machinery); and
  (FLOOR-PERSIST), now specifically **at pad `999/1000`** for `n > 800` (rather than at
  pad `99/100` for `n > 500`) — the V18 deep-grid extension to `n = 800` (Section 11)
  empirically confirms monotone drift through the new anchor, but persistence *beyond*
  `800` at this tighter pad is imported reasoning, not re-derived from scratch. These
  three are exactly the three clauses this section still lists as open; SIB-CERT does
  not add a fourth.

**(FOLD) — the 57/50 child-window fold.**
- *Asserts*: the Window Lemma (W1) fold factor `spread_{i<18}/spread_{i<17} <= 57/50`.
- *Gate*: V16b (grid-measured; measured max `1.1322` at `n=48`, decreasing).
- *Evidence*: `sup_{n,t}` over the finite grid plus a COMPUTED CLT quadratic-profile
  ansatz; not proved for all `n`.
- *Upgrade*: a proved uniform bound on `spread_{i<18}/spread_{i<17}`.

**(FLOOR-PERSIST) — floor persistence for `n > 500`. STILL COMPUTED — but now
first-class: named, gated, tamperable (gate FLOOR-DRIFT, this revision), with its
natural discharge route CLOSED as a route-cut (Section 9(v)).**
- *Asserts (made precise this revision — the exact as-consumed form)*: for every parent
  `t` (41-grid) and every `n >= 500`, the CHILD ratio profiles at the branch parameters
  satisfy `rc_i(n, t_pm) >= (99/100) rc_i(500, t)` for `i < 18` (the census gates box
  child profiles by the parent-`t` anchor family); and the same at the SIB-CERT anchor,
  `rc_i(n, t_pm) >= (999/1000) rc_i(800, t)` for `n >= 800`. Both a parameter-transfer
  (child-vs-parent parameter, measured to consume `~0.003%` of the pad) and a
  level-transfer (the drift) are inside this statement.
- *Gate*: **FLOOR-DRIFT** [core, full mode only, this revision] — monitoring, NOT a
  proof: (1) the drift mechanism directly, `rc_i(n2, s) >= rc_i(n1, s)` over
  consecutive deep-grid pairs `n1 >= 500`, all 123 monitored parameters (41 parents +
  82 branch values), `i < 18` — worst step ratio `~1.00005`, decaying but strictly
  above 1; (2) the as-consumed margins at both anchors — worst `1.0101` at
  `(500, 99/100)` (the pad is what carries it; the raw margin over the pad is `~1.0%`)
  and `1.0010` at `(800, 999/1000)`. Tamper `floordrift-margin` (isolated).
- *Evidence*: the drift (`rc_i` upward in `n`, the CLT flattening) was COMPUTED in the
  predecessor and previously *imported silently*; it is now checked directly at every
  monitored parameter and level pair in THIS packet's own verifier.
- *Route-cut (this revision)*: the natural discharge — re-run a V12-style pointwise
  corner census of the one-step output ratios over the floor box at the deep anchor —
  is **REFUTED**: box-worst `r'_i`/floor `= 0.58` at `(500, 99/100)` (94% of rows
  fail; 100% at `(800, 999/1000)`). See Section 9(v). Any future discharge must be a
  trajectory/drift argument (e.g. a quantitative no-spike-tower bound, the same open
  handle as R-b), not a box census.
- *Upgrade*: a self-contained drift proof (quantitative monotone-comparison /
  no-spike-tower argument) — now sharply separated from the dead census route.

**(C'-CAP) — the Lambda correction-derivative cap. DISCHARGED-conditional (gate
LAM-INV, floor-box node census, this revision — R1 mitigation (a) carried out).**

*What the clause was about.* The coupled Lambda-field recursion drops the derivative of
the branch-mass correction as an outward slop `CPRIME = 3/500` per pass; before this
revision that cap was MONITORED (measured `~0.001-0.003`), not proved — the one
monitored-only literal in the packet.

**The exact identity (the drop, in closed form).** Sum (I1) over the two branches:
`S_n(t) = P(t) - C(t)` with `P := a_+ S^+ + a_- S^-` (the pure operator) and
`C := (1/4) sum_pm (Delta_0 + E_W)^pm >= 0`. Then, elementarily
(`(P'-C')/(P-C) - P'/P`):

```
    Lambda_true(t) - Lambda_pure(t) = [ gbar*Lambda_pure - C'/P ] / (1 - gbar),
    gbar := C/P = sum_pm w_pm gamma^pm,      w_pm := a_pm S^pm / P  (mass weights),
```

so `|drop| <= [gbar*|Lambda_pure| + |C'|/P]/(1-gbar)`. **Three ingredients, all outward
(gate LAM-INV's node census, exact Fraction):**
1. `gamma^pm <= G^pm(t_pm)` — the *same* per-branch floor-box derivation as the PROVED
   `gamma <= GMAX` bound (`Delta_0 <= c_0(1-f_0)`, `E_W <= c_0(1-f_16)`,
   `M_w/c_0 >= Q`), evaluated at the node's two child parameters from the anchor
   level's own head vectors; `gbar` maximized over the lam-enclosure's `w`-corners
   (every expression below is affine in `w` — corner-sufficient; each occurrence is
   maximized separately, a sound marginal bound). The mass-weight split is what makes
   the bound clear: the worst per-branch `gamma` (the `t_- ~ 1/6` branch, `0.0043`)
   carries only `~0.2` mass weight at the binding parent `t ~ 1/2`.
2. `|Lambda_pure|` — enclosed by the *same* 8-corner candidate enumeration the
   invariance check runs (bilinear in `(w, gp, gm)` — corner-sufficient), re-derived
   per node with identical brackets.
3. `|C'|/P` — from `Delta_0' = L_0 Delta_0 + c_1(L_0 - L_1)` and `E_W' = L_16 E_W +
   c_17(L_16 - L_17)` (product rule + FTC on `c_i' = L_i c_i`):
   ```
   |C'|/P <= (1/3)[ w G^+ L^+ + (1-w) G^- L^- ]
           + (1/12) V18c [ (w/a^+_lo)(2/Q^+) + ((1-w)/a^-_lo)(2/Q^-) ],
   ```
   with `|L_i| <= |Lambda^pm_child| + V18c =: L^pm` (window-mean split, zero-sum
   deviations), `|L_0-L_1|, |L_16-L_17| <= V18c`, `(c_1+c_17)/S^pm <= 2/Q^pm`,
   `(Delta_0+E_W)^pm/P = 4 gamma^pm w_pm`, chain rule `|dt_pm/dt| = 1/3`
   (whence `(1/4)(1/3) = 1/12`), and
   `V18c := (57/50) * max(V_17(J0), F_box/(1-theta_band))` — the **(FOLD)-folded
   equilibrium ceiling**, consumed as an exact Fraction from the UNTAMPERED V15-IA /
   V17-IA chain (memoized; a tampered load-bearing census never feeds this bound).

**Where the cap is needed — node census suffices.** The Lambda recursion consumes
`CPRIME` only **at the NG grid nodes** (the between-grid coverage rides the existing
`LIP_S`/`LIP_L` brackets), so certifying the bound at every node is certifying it
everywhere it is used. **The joint-induction step is acyclic per level**: the pass
`n-1 -> n` consumes `H(n-1)`'s V-ceiling (the IH tracks `V_17 <= v_m`) and `H(n-1)`'s
field membership (lam in its box); the base `n-1 in [48, J0)` rides the existing
base-case grid, so the cap is only ever invoked at child levels `>= J0` where the
equilibrium ceiling holds. This is the same joint-IH structure gate SIB-CERT's lemma
already uses (its wobble band consumes the IH's `rho_prop` clause).
- *Gate*: **LAM-INV** [core, full mode only] — the node census over all NG grid points;
  worst bound, locus, and the per-ingredient split (`gbar`, `|Lambda_pure|`, the two
  `C'/P` terms) are printed on the gate line and recorded in the cert JSON. The
  a-posteriori realized-vs-field monitor is **RETAINED as the empirical cross-check**
  (the same demotion MAG-BOX received when LAM-INV landed). Tamper `cprime-bound-graze`
  doubles the final bound (isolated: nothing upstream of the comparison changes).
- *Honest dependence*: floors at the node's branch parameters (gate F3 at the parent
  grid + the (FLOOR-PERSIST) clause, gate FLOOR-DRIFT), **(FOLD)** (the `57/50` fold
  enters `V18c`), the joint IH (V-ceiling + field membership), and the finite base-case
  census — all already-named inputs; **no new clause and no monitored-only literal**.
- *Sounding vs certificate*: the float per-`t` sounding sups at `~0.0046` vs
  `CPRIME = 0.006`; the exact census's worst (with all outward slops) is the certified
  number on the gate line.

## 9. ROUTE-CUT RESULTS (valuable negatives)

Four routes were tested and are now closed with quantified margins — recording them
prevents re-litigating dead ends.

**(i) The rate-free equilibrium bound at a base `<= 100`, on the certified corner
family, is REFUTED.** The natural "no decay needed" route bounds the source term
`s(t)` (share-variation + a'-source) by its value over the *whole* certified band,
rather than at the realized trajectory. That band-wide census — filtered by the
`rho_prop <= TARGET` constraint (the load-bearing restriction: without it the source
inflates further) — realizes `BAND s_sup approx 0.2886`, against a `0.10` ceiling: a
route-breaking miss. Because the band is **level-independent** (its value does not
depend on `n`) while the *realized* trajectory keeps shrinking, the **inflation factor
grows with `n`**: `4.76x` at `n = 60`, worsening to `13.34x` at `n = 100`. This is
reproduced as an explicit negative control by gate V17's informational sub-check
(Section 11).

**(ii) The whole-map empirical contraction ratio is CIRCULAR for an equilibrium
argument.** Fitting `spread(n+1) approx theta_emp(n) spread(n) + s_emp(n)` directly
to the raw sibling spread sequence gives a clean law `theta_emp(n) approx 1 -
2.98/n` — drifting to 1, the *same functional shape* as the (separately, already-known)
refuted full-profile contraction. Since `spread(n) -> 0` regardless of which fixed
`theta < 1` one substitutes, "find a fixed `theta_win` with the residual `s(n)`
bounded" is numerically easy for *essentially any* `theta_win < 1` sampled against this
drifting empirical fit — it demonstrates nothing about the true one-step map. The
content has to come from a **structural** contraction argument on a *fixed-size*
channel (Sections 4-5's `theta~`/`theta_tot`, genuinely flat, not curve-fit), not from
fitting the raw drifting recursion.

**(iii) The naive `(1/3)`-bridge form of Lemma 1 misses the discharge target by
`3.8%`, and the "certifiable-without-integral" sharp variant is a dead end.** Using
`(1/3) V_17(60)` directly as the equilibrium ceiling gives `0.0262`, against the target
`log(1.02560749) = 0.02528` — a miss. A natural attempt to tighten this *without*
computing an integral — replacing `sup_tau` over the full domain by the local sup over
just `[t_-, t_+]`, paired with the sharp gap `(2t/3)` rather than the loose `1/3` — is
numerically **IDENTICAL** to the loose `(1/3) V_17(n)` bound (ratio `1.0000` at every
tested level): at the binding locus `t = 1/2`, `[t_-,t_+]` *is* the full domain, so the
"sharp, no-integral" variant provides no tightening at all. Only the **true weighted
integral** (the `w(n) approx 0.61` bridge weight, gate V19) recovers the tighter bound
— and it is informational/alpha-only here (Section 7.2), since the beta spine
(Section 7) closes via decay, not via this tighter constant.

**(iv) A shared box parameter must be held fixed across a composite object's
sub-terms.** `lam` (the sibling-proportionality scalar, Section 5) is *one shared* box
variable, not a per-matrix-entry one. Extremizing `lam` separately for each entry of
each row (a valid marginal bound, in the same style V17-IA's own per-index marginal
bounding uses) and combining the results can combine entries at `lam` values no single
box point realizes *simultaneously*, inflating the certified `theta_band`. The lam-minced
census (Section 5) instead respects the shared-`lam` constraint — every entry in a given
panel evaluation shares one `lam` sub-interval, and each Möbius-in-`lam` entry is hulled
over that panel — so a single-panel, per-entry-independent-`lam` bound is strictly
looser. Recorded because the "independently extremize a shared parameter per sub-object"
pattern is easy to reach for by default in this style of certificate and is not
automatically wrong (V17-IA's own per-index `P_i` marginal bounding is a legitimate use
of the same pattern) — it is specifically wrong to do it with a variable, like `lam`,
that a single composite object (the seminorm over a *pair* of rows) must hold fixed
across all of its own sub-terms.

**(v) The pointwise corner-census route to (FLOOR-PERSIST) is CLOSED (this revision).**
The natural discharge of (FLOOR-PERSIST) — prove the floor family *step-closed* by a
V12-style corner census (per parent `t`, per row `i < 18`: box-minimize the one-step
output ratio `r'_i = o_{i+1}/o_i` over the minus-child ratio box `[F_j(t_-), 1]`
(LC vertices), the sibling magnitude `lam` in the (LAM-BOX) box, and per-entry wobble
in the geometric-center half-band, and compare against the output floor `F_i(t)`) —
**misses catastrophically, and structurally**: box-worst `r'_i/floor = 0.579` at
`(500, 99/100)` (697/738 rows fail), `0.568` at `(800, 999/1000)` (**all** 738 rows
fail). The failure is not marginal and no deeper anchor or pad tuning can fix it: the
box-worst adversarial profile puts numerator-adjacent ratios at their floors and
denominator-adjacent ratios at their caps, producing an output-ratio swing of order
`(1 - f_i) ~ 4-5%` per index against a pad slack of `1%` (resp. `0.1%`) — the box has
**no mechanism coupling input-floor slack to output-floor slack**, exactly the same
structural boundary as Section 10's "no free `O(1/n)` sits in the caps/floors box"
correction. Persistence is a property of the *realized trajectory* (the upward CLT
drift, gate FLOOR-DRIFT's check (1)), not of the certified box. Reproduced as an
INFORMATIONAL negative control on gate FLOOR-DRIFT's own line
(`_floor_census_routecut`), so the dead end stays visible and un-relitigated.

Plain statements of drift/error found and fixed against earlier material that
fed into this packet.

- The child log-derivative profile is `mu_k propto (2k+1)`, **not** `(k+1)` — an
  earlier window-growth constant used the wrong profile exponent (Section 6,
  Lemma W1).
- The honest child-read window for the one-step contraction census is `i < 18`, **not**
  `i < 19` — an earlier window was one index wider than the tridiagonal
  read-set requires (safe, but loose; corrected in Lemma W1/W2).
- The `C(I0)/j^2` law's "stable to 3 digits" characterization holds **only for `j <=
  64`**: extended to `j = 200` on a deep grid, all four tested window constants
  (`I0 = 4,8,12,17`) drift **down** by `1.4%-3.6%`, stable to only ~1-2 digits over
  that range — a real, if benign (decay if anything slightly faster than a fixed-`C`
  law predicts), scoping correction to an earlier "stable to 3 digits" claim.
- A claim that "`Curv = O(1/n)` from caps/floors/LC alone (no Gaussian cancellation),
  constant `~16 beta`" is **INCORRECT as stated**. That derivation silently imports the
  drift formula `rc_i approx 1 - (2i+1)beta/n` (itself only COMPUTED, a fitted CLT
  law) to get the `1/n` spread of `rc_i` across the window. **From caps/floors/LC
  alone, the certified bound is a CONSTANT** (Section 8.1's Lemma C1/normal form), not
  `O(1/n)` — the box has no mechanism to shrink with `n` on its own. This correction is
  the substance of Section 8.1's honest miss-by-3.9x finding: there is no free `O(1/n)`
  bound sitting in the caps/floors box waiting to be extracted.
- The `--fallback` flag switches the whole triple atomically to a **legacy,
  informational** alternative chain `(J0 = 430, f = 49/50, theta* = 1/2 fixed)`; it is
  not part of the certified primary claim.
- **Window coherence of the LAM-INV field (found and fixed this revision).** The
  round-3 text cited identity (I2) at `W = 18` (`Lambda^pm_mass = (log S^18)'`) while
  identity (I1), the `gamma <= GMAX` floor-box bound, and the live Fraction spot-check
  all use `W = 17 = OPWIN` — and the field's reality-side comparisons (the `C'`
  monitor, MAG-BOX's realized-vs-field consistency check) compared against the
  **18-window** mass-weighted `Lambda`. The field pair `(S, Lambda)` is
  self-consistent for exactly one window, and its drop covers (`gamma`, `C'`) are
  derived at `W = 17` — so the mismatch was one edge term (`(1/4)(c_17 - c_18)` vs
  `(1/4)(c_16 - c_17)`) of slippage between the certified invariance argument and the
  monitored realized object. **Fix**: (I2) is restated window-generic and instantiated
  at `W = 17`; `onestep_compose` now emits the `W = 17` mass-weighted references
  (`Lamp17`/`Lamm17`); the `C'` monitor and MAG-BOX's field consistency check compare
  against those; MAG-BOX additionally monitors the `W = 17` variants in-box alongside
  the (retained) `W = 18` mass and arithmetic-mean variants. Numerically the shift is
  small (all boxes/headrooms re-verified green; see the re-run gate lines) — the fix
  is bookkeeping coherence, not a value correction; the (C'-CAP) node census (this
  revision) is derived at `W = 17` throughout and is unaffected. Same finding class as
  this section's existing V12 out-LC precision note: a latent statement-vs-check
  mismatch surfaced by adversarial re-derivation, fixed before it could bite.

**Precision note on the predecessor's V12 (#885)**: the predecessor's corner census
certifies its **cap** and **floor** clauses by a genuine corner-sufficiency theorem
(each is a single output ratio, or its offset by a constant, hence a Möbius function of
each input ratio, extremal at box corners — a proved reduction). Its **output-LC**
clause (`r'_i - r'_{i+1} >= 0`, a *difference* of two output ratios with *different
denominators*) is **not** covered by that theorem: as a function of a single input
ratio it is a degree-`(2,2)` rational, not Möbius, and need not be monotone on the box.
The predecessor's output-LC check is therefore **corner-sampled, empirically clean —
not corner-proved**. This is exactly the same structural boundary Section 5 documents
for the tangent seminorm's profile direction. **Impact, stated honestly**: this does
not touch the predecessor's cap/floor clauses (still corner-proved) or any of its
gated numeric outcomes — this reading is consistent with the predecessor's `-1e-6`
output-LC tolerance, which never binds (its measured margin `-1.4e-8` sits well inside
it), and no gate's PASS/FAIL changes under this reading. This note documents the
precision gap for the record; it is not a retraction of any shipped claim.

## 11. Verifier map

`experimental/scripts/verify_dense_shell_prop_tail_reduction.py`. **The default (full)
run IS the discharge**: base anchor `J0* = 500`, pad `f* = 99/100`, PLUS the SIB-CERT
deep anchor `J0_SIB = 800`, pad `999/1000` (full mode only). Flags: `--quick` (dev
subset, shallow `J0 <= 200` — not a certified claim at that depth; V17-IA expectedly
misses at the shallow anchor; SIB-CERT is skipped, an informational SKIPPED line is
printed instead), `--table` (per-level `rho`/`V_17` table, now to `n = 800`),
`--fallback` (legacy informational alternative chain `(J0 = 430, f = 49/50,
theta* = 1/2 fixed)`, not part of the certified claim; SIB-CERT and LAM-INV are likewise
skipped there), and `--tamper-selftest`. **11 core gates determine the RESULT in the
default full mode** (8 in `--quick`/`--fallback`, where SIB-CERT, LAM-INV, and
FLOOR-DRIFT do not run); 4 informational gates plus the SIB-BAND gap gate (and, in
`--quick`/`--fallback`, the SIB-CERT/LAM-INV/FLOOR-DRIFT SKIPPED lines) are printed,
not counted (SIB-BAND is deliberately marked FAIL to keep the shallow-anchor
surrogate-vs-real gap visible as a historical exhibit, even though SIB-CERT now closes
that gap at the deep anchor). Every gate's message states its operative index window.
The full run measures **~380s** (build to `n=800` dominates; LAM-INV's NG=3841 field
census plus this revision's (C'-CAP) floor-box node census total ~40s — the node
census's cost is offset by the new memoization of the V15-IA/V17-IA censuses, which
LAM-INV's ceiling input and the report gates now share; 11/11 core PASS); `--quick` is
unaffected in cost (still a shallow `J0<=200` build); `--fallback` reaches `n=800`
(V18's grid is shared) but skips the SIB-CERT, LAM-INV, and FLOOR-DRIFT censuses.

- **F3 FLOORS** [core]. Re-certifies the floor family `r_i(J0*, t)` over the 41-parent
  grid, `i < 18`: positivity, LC-compatibility (non-increasing + floor `<=` actual `<=`
  cap), and the `i=0` b-vs-c halving-convention cross-check. The base-anchor
  certificate F3/MAG-BOX/V15-IA/V17-IA all consume. All checks PASS at `J0*=500,
  f*=99/100` (0 violations).
- **MAG-BOX** [core, **empirical cross-check of the now-proved clause (LAM-BOX)**].
  `lam` and mass-weighted `Lambda^+/-`: PROVED-CONDITIONAL INTERVAL (gate LAM-INV),
  monitoring RETAINED here as the empirical cross-check, not the sole evidence — box
  `lam in [0.72, 0.95]`, `Lambda^+ in [-1.17, -0.82]` (widened this revision, R1
  mitigation (b)), `Lambda^- in [-0.66, -0.35]`: realized `lam in [0.7759, 0.9190]`,
  `Lambda^+_mass in [-1.1429, -0.8883]`, `Lambda^-_mass in [-0.6334, -0.3788]`, per-entry
  `rho_i = c^+_i/c^-_i in [0.7734, 0.9259]`, all inside the boxes at every grid level;
  worst headroom over this proved-conditional category `0.0241` (`rho_16`, `n=48`).
  Arithmetic-mean `Lambda^+/-` variants: COMPUTED-monitored ONLY (NOT covered by the
  LAM-INV enclosure; LAB_LAMBOX's Q1 finding is they WIDEN with depth) — worst headroom
  `0.0196` (`n=48`), the overall tightest of all monitored quantities. **ALSO** (this
  revision) cross-checks the realized-vs-field correction-derivative `C'` at MAG-BOX's
  own 6 grid levels x 41 parents against `CPRIME` (the a-posteriori side of risk
  register R1, broader than gate LAM-INV's own sparser one-anchor sample): worst
  `0.0027 <= CPRIME = 0.006` (W=17 field object, round-4 window coherence), comfortable;
  SKIPPED under `--quick`/`--fallback` (gate
  LAM-INV does not run there). See Section 8.4 (LAM-BOX). **(round 2)** ALSO
  monitors the SIB-CERT **boundary slot** `w_17 := rho_17/lam_gc` against its own deep
  box `W17 = [0.999, 1.001]`, over `n in {500,...,800}` (`W17_GRID`, SIB-CERT's own
  operative domain, 7 levels x 41 parents) — the `(LAM-BOX)`-class hypothesis the
  BOUNDARY ANNEX (Section 8.4) needs; not attempted at shallow `n`, where it would be
  false (the annex's counterexample). Tamper `w17-shrink` shrinks this box below the
  realized range, isolated to this gate.
- **V15-IA THETA-BAND** [core, **load-bearing**]. The certified band-uniform enclosure of
  the Lemma A1 tangent seminorm (Section 5) over the *entire* certified LC ratio box, not
  the realized profile or a tested grid, folded by the certified Window Lemma factor
  `<=57/50`. The seminorm is a sum of `|differences of Möbius functions with different
  denominators|`, so it is **not** Möbius in `lam` and can attain an interior-`lam`
  maximum; the gate is therefore a **lam-minced rigorous enclosure** (`LAM_MINCE = 24`
  panels — mince `lam`, hull each Möbius-in-`lam` entry per panel, outer max over panels),
  **not** an endpoint-in-`lam` sufficiency claim. Certified `theta_band = 0.6020244`
  (exact Fraction `1505061/2500000`) — comfortably inside its own unconditional sanity
  ceiling `9/10`. This value is passed directly to gate V17-IA as `theta_star`; the two
  gates are chained, not independent checks of a shared fixed constant.
- **V16 THETASYMB** [core]. The exact Fraction polynomial identity of Lemma 3 plus the
  domain sign argument. `decide`-friendly (rational coefficients); no tamper.
- **V16b WINDOW** [core]. Lemma W1's asymptotic fact `289/256 <= 57/50` (exact
  rational), the grid check `sup spread_{i<18}(L)/spread_{i<17}(L) <= 57/50` (measured
  `1.1322` at `n=48`), and Lemma W2's structural read-set check.
- **V17 FORCING** [core]. `F_ext(n)*n^2` and `Curv(n)*n^2` bounded `<= 200` at the edge
  locus (measured worst `187.83` / `109.09`). Its message also reports, inline and
  **INFORMATIONAL**, the G2/alpha route-cut negative control of Section 9(i): the
  rho_prop-constrained band census, confirmed to **exceed** a `0.10` ceiling (`0.2886`).
- **V17-IA FORCING** [core, **load-bearing**]. The minced interval-arithmetic census of
  `F_box(J0*, f*) <= (1-theta_band)*tau*`: an exact-Fraction, width-2-locality enclosure
  (every index `i=0..16`'s marginal range, not only the two endpoints), box-maxed over
  the sibling-proportionality magnitude parameters (the forced-proportional surrogate).
  Certified `F_box(500, 99/100) = 0.02690175` vs threshold `(1-theta_band)*tau* =
  0.03018857` — **10.9% margin, PASS**. `tau*` enters as the exact-Fraction lower bound
  `TAU_STAR_FR = 0.075855330599169 (<= 3 log(TARGET))`, and the final PASS/FAIL
  comparison is exact Fraction. The gate also prints the equilibrium chain
  (`F_box/(1-theta_band) = 0.06759647 <= tau* = 0.07585533`; `(1/3)* = 0.02253216 <=
  log(TARGET) = 0.02528511`; `exp = 1.022788 <= TARGET = 1.02560749`), the locus, and the
  documented outward slop (`1e-9`, six orders of magnitude past the cascade's own
  floating-point precision).
- **V18 VTRACK** [core]. The deep-grid `rho_prop@i<17(n) <= 1.02560749` over
  `n in {48,...,800}` (24 levels, including the `340/400/430/450/500` deep tail and the
  new `550/600/650/700/750/800` extension added for the SIB-CERT deep anchor),
  monotone non-increasing, the `V_17(n)` values at every tested level (`0.1236` at
  `n=48` down to a smaller value at `n=800`), the `tau*` crossover (confirmed `n=62`), and
  an explicit base-coverage check (`max(grid) >= expect_max`, `expect_max` now `800`).
  The `--table` flag prints the full per-level `rho`/`V_17` table.
- **SIB-CERT** [core, FULL MODE ONLY — **discharges computed clause (SIB-BAND)**]. The
  geometric-center half-band wobble census (Section 8.4's GEOMETRIC-CENTER LEMMA: no
  assumption beyond (LAM-BOX)) re-run at the deep anchor `(J0_SIB, PAD_SIB) =
  (800, 999/1000)`, where it CLEARS the equilibrium threshold (margin `+7.4%`,
  round-2 exact value, Section 8.4) — covering the **real, non-proportional** cascade,
  not merely the forced-proportional surrogate V15-IA/V17-IA certify. Self-checks the
  outward sqrt bracket (`_SQ_HI^2 >= R_STAR_FR`) every run before running the (otherwise
  ~35s) census. **(round 2)** passes `boundary_band = (W17_LO_F, W17_HI_F)` so the single
  out-of-window census slot (`i=16`'s `x`, i.e. `w_17` — BOUNDARY ANNEX, Section 8.4)
  uses its own deep box (monitored by MAG-BOX) instead of `WOB_HALF`; every other slot
  is unaffected. SKIPPED (an informational line is printed instead) under
  `--quick`/`--fallback`, since the deep anchor needs the full `J0=800` build. See
  Section 8.4 (SIB-BAND) for the lemma, the annex, exact numbers, and sounding trend.
- **LAM-INV** [core, FULL MODE ONLY — **discharges computed clause (LAM-BOX)**]. The
  PROVED invariant-interval upgrade (`DERIV_LAMBOX.md`, Section 8.4 above): a live
  exact-Fraction spot-check of identity (I1) (residual `0`); one forward-pass
  T-invariance of the Birkhoff mass interval field (`NG=3841`) with `sc_exact`
  ray-normalization and `GMAX`-tolerance comparison, plus the a-posteriori
  `sup|Lambda|<=LIP_S` self-check; one forward-pass invariance of the coupled
  Lambda field with `CPRIME`-tolerance comparison, plus the a-posteriori
  `sup|Lambda'|<=LIP_L` self-check; a floor-box-**PROVED** bound `gamma<=GMAX`; and —
  this revision — a floor-box-**PROVED** bound `C'<=CPRIME` (the `(C'-CAP)` clause,
  DISCHARGED-conditional): the node census over all NG grid points of the exact-identity
  drop bound (Section 8.4's (C'-CAP) entry — certified worst `0.004245 <= 3/500`,
  `29%` margin, locus `t=0.5`; ingredient split printed on the gate line), consuming
  the (FOLD)-folded equilibrium ceiling from the UNTAMPERED, memoized V15-IA/V17-IA
  chain; the a-posteriori realized-vs-field monitor is RETAINED as the empirical
  cross-check (measured `0.0013` at LAM-INV's own sample; `0.0027` at MAG-BOX's broader
  grid). Base case (the finite grid) is cited from the existing MAG-BOX/V18 gates, not
  re-derived. Reports the proved intervals against the shipped (post-widening) boxes
  with headroom. A live self-check asserts the fast head-vector path (`_anchor_head_cvec`)
  reproduces `cvec` exactly before the census runs. SKIPPED (an informational line is
  printed instead) under `--quick`/`--fallback`, like SIB-CERT.
  Tampers: `laminv-grid` (NG far below the R4 threshold — the between-grid Lipschitz
  slop blows the final proved interval past the shipped box), `laminv-lip` (the
  a-posteriori `LIP_L` comparison threshold alone is lowered below the realized value,
  isolated to that one self-check line), `laminv-floor` (R1 stress: restores the
  pre-widening `-1.16` floor AND forces `CPRIME` to `2x` shipped, `0.008` — the gate
  must FAIL containment, matching the risk register's own finding), `cprime-bound-graze`
  (this revision: the certified (C'-CAP) node-census bound alone is doubled,
  `0.0085 > 3/500` — the proved-bound comparison FAILs; nothing upstream changes,
  isolated to this gate's line).
- **FLOOR-DRIFT** [core, FULL MODE ONLY — **first-class monitoring of the
  (FLOOR-PERSIST) COMPUTED clause; monitoring, NOT a proof** (this revision)]. (1) The
  drift mechanism directly: `rc_i(n2, s) >= rc_i(n1, s)` over consecutive deep-grid
  pairs with `n1 >= 500`, at all 123 monitored parameters (41 parents + 82 branch
  values), `i < 18` — worst step ratio `1.00005212` (edge parent, pair `750 -> 800`,
  `i=0`); the full-grid-from-48 worst is printed as informational. (2) The exact
  as-consumed floor margins (Section 8.4's (FLOOR-PERSIST) *Asserts*): worst
  `rc_i(n, t_pm)/(f* rc_i(J0, t)) = 1.010070` at `(500, 99/100)` (locus: edge parent,
  `n=500`, `i=17` — the parameter-transfer eats `~0.003%` of the `1%` pad) and
  `1.000989` at `(800, 999/1000)`. The gate line also prints, INFORMATIONAL, the
  Section 9(v) route-cut negative control (`_floor_census_routecut`): box-worst
  output-ratio/floor `0.579` (697/738 rows fail) at `(500, 99/100)`, `0.568` (738/738)
  at `(800, 999/1000)` — quantifying why no pointwise corner census can discharge this
  clause. Tamper `floordrift-margin` (raises the required drift ratio to `1.0001`,
  above the realized worst — isolated FAIL).
- **V15-GRID THETA** [informational]. `theta_tot <= 1/2` and `theta_win <= 27/100`, grid
  census over 41 parents to `n = 500`; plus the closed-form tangent seminorm `N_free <=
  0.9` (Lemma A1, evaluated at realized profiles only). Measured worst: `theta_tot =
  0.3766`, `theta_win = 0.2032`, `N_free = 0.4974` — a robustness cross-check, comfortably
  inside the certified `theta_band`, not part of the certified chain.
- **V15-CERT** [informational, grid-sampled cross-ref]. A grid-sampled tangent-seminorm
  cross-reference `theta_cert := N_free * (57/50 window fold) ~= 0.567` — a grid-sampled
  (not band-uniform) view, retained as a cross-check against the band-uniform V15-IA
  enclosure.
- **V17-INFO** [informational]. The G2/alpha route-cut negative control (see V17
  above).
- **V19 BRIDGE** [informational/alpha-only]. `w(n) <= 0.62` (measured worst `0.6115`).
  Not part of the RESULT tally: the shipped equilibrium chain never uses the tight
  integral bridge, only the loose `(1/3)` form plus the certified constant forcing.
- **SIB-BAND** [informational — the shallow-anchor exhibit; **DISCHARGED elsewhere by
  SIB-CERT above, kept exactly as shipped**]. Prints the wobble-extended censuses at the
  *shallow* anchor `(J0*, f*) = (500, 99/100)` (per-entry sibling wobble
  `w_i in [1/R*, R*]`): `theta_band_wob = 0.629641`, `F_box_wob = 0.0571211` vs threshold
  `0.0280937` — the extended forcing **EXCEEDS** the threshold by **103.3%** at *this*
  (shallow) anchor, so the extension does **NOT** close here. The tighter, still-sound
  geometric-center band `[1/sqrt R*, sqrt R*]` gives `F_box_wob = 0.0417911` (miss by 43%)
  at `(500, 99/100)` too. Deliberately marked **FAIL** and left unchanged, as the
  historical record of the shallow-anchor gap; the gap itself is now closed — see
  **SIB-CERT** above, which re-runs the same geometric-center half-band census at the
  deep anchor `(800, 999/1000)`, where it clears. Section 8.4 (SIB-BAND) has the lemma
  and the full sounding trend across anchors.

Tamper suite (22, each isolated to one report/info line): `f3-corrupt` (F3 — a `>1` pad
breaks the floor-`<=`-actual ordering), `magbox-shrink` (**MAG-BOX** — shrinks the
magnitude box so a realized `lam`/`Lambda^pm`/`rho_i` falls outside, flipping MAG-BOX to
FAIL), `theta-tot-gate` (`V15-GRID`, informational), `nfree-corrupt` (`V15-GRID` seminorm
corruption, informational), `theta-ia-tighten` (grazes gate V15-IA's own sanity ceiling
from `9/10` to `1/2`, isolated: the certified `theta_band` value itself, and hence gate
V17-IA's downstream line, is untouched), `theta-ia-sign` (**V15-IA** — flips the seminorm
enclosure's `max -> min` direction, caught by a realized-seminorm floor consistency check;
isolated because a *lower* `theta_band` only relaxes V17-IA, so the sign error cannot
silently pass through the load-bearing chain), `window-bound` (V16b), `forcing-bound`
(V17), `v17ia-graze` (V17-IA threshold graze — shrinks the threshold `20%`, flipping the
margin PASS to FAIL), `c1-target` (V18), `vtrack-level-drop` (V18 deep-level corruption —
drops the grid's top level, caught by the base-coverage check), `g2-ceiling` (the V17
informational sub-check — honest substitute), `bridge-w-gate` (V19, informational),
`sibcert-sqrt` (**SIB-CERT** — substitutes an explicitly inward rational bracket on
`sqrt(R*)`, tripping the gate's own outwardness self-check before the census runs),
`sibcert-pad` (**SIB-CERT** — swaps the deep anchor's pad from `999/1000` to the
shallower `99/100`, which sounds `-12.2%` at `J0=800`, flipping the margin PASS to
FAIL), `sibcert-band` (**SIB-CERT** — swaps the geometric-center half-band for the full
`[1/R*, R*]` band, which cannot clear at any depth, flipping to FAIL), `w17-shrink`
(**MAG-BOX**, round 2 — shrinks the boundary-slot box `W17` to a tiny interval strictly
below the realized `w_17` range on `W17_GRID`, flipping MAG-BOX, not SIB-CERT, to FAIL:
the boundary slot's hypothesis is monitored by MAG-BOX, and SIB-CERT merely *consumes*
the box `(W17_LO_F, W17_HI_F)` as a constant, so a shrunk box is a MAG-BOX-monitoring
failure, not a SIB-CERT-census one), `laminv-grid` (**LAM-INV** — `NG` cut far below the
R4 threshold so the between-grid Lipschitz slop blows the final proved interval past the
shipped box, flipping the containment checks to FAIL), `laminv-lip` (**LAM-INV** — the
a-posteriori `LIP_L` comparison threshold alone is lowered below the realized
`sup|Lambda'|`, isolated to that one self-check line; the field's own Lipschitz-bracket
construction is untouched), `laminv-floor` (**LAM-INV** — R1 stress: restores the
pre-widening `Lambda^+` floor `-1.16` AND forces `CPRIME` to `2x` shipped, `0.008` —
flips the `Lambda^+` containment check to FAIL, matching the risk register's own
prediction), `cprime-bound-graze` (**LAM-INV**, this revision — doubles the certified
(C'-CAP) node-census bound alone, `0.0085 > 3/500`: the proved-bound comparison FAILs;
the field construction, the monitored cross-check, and every other gate are untouched),
`floordrift-margin` (**FLOOR-DRIFT**, this revision — raises the required drift step
ratio to `1.0001`, above the realized worst `1.00005212`, flipping only FLOOR-DRIFT).
All 22 confirmed isolated to their own line at full (`J0*=500`/`J0_SIB=800`)
depth; no other gate's outcome changes under any tamper — `sibcert-band`, re-run as a
regression check this revision, remains isolated to SIB-CERT's own line with LAM-INV's
line (report index 9, appended after SIB-CERT) confirmed unaffected.

**Lean layer**: `experimental/lean/prop_tail_reduction/` — a statement-level companion
package (stdlib-only, no mathlib, no `sorry`, `decide`-only kernel checks, builds
clean). Scope, exactly: (1) Lemma 3's ring identity `75(1-x^2)-(6+3x)^2 =
-3(2x-1)(14x+13)` on `Int` coefficient lists, plus a denominator-cleared sign
corollary (`x = p/q`) certifying the polynomial inequality `theta~ <= 1/5` reduces to
*post-squaring* — the trig substitution `x = cos(2 pi t/3)` and the squaring step
itself stay informal/analytic; (2) Lemma W1's rational fact `289*50 <= 57*256` (i.e.
`289/256 <= 57/50`); (3) the deep-grid `rho_prop@i<17(j)` table and the `V_17` vs.
`tau*` crossover-at-`n=62` table, both transcribed from this packet's printed decimals
to exact rationals at printed precision, with threshold + strict-monotonicity checks
on the transcribed table itself (not a re-derivation of the underlying floating-point
computation); (4) the SIB-CERT deep-anchor threshold comparison (`sibcert_clears`,
denominator-cleared, conservative transcription); (5) the LAM-INV proved-interval
containments and the widened-floor consistency check; (6) — this revision — the
(C'-CAP) discharge comparison (`cprime_bound_clears`: the certified node-census bound
`<= 3/500`, cleared form) and the FLOOR-DRIFT transcriptions (drift step ratio `>= 1`,
both as-consumed margins `>= 1`, and the Section 9(v) route-cut exhibits `< 1` — the
kernel-checked negative). Everything else in this note — Lemma 1's reduction, Lemma 2's cascade,
Lemma A1's tangent seminorm (including the band-uniform enclosure, gate V15-IA), Lemma
W2's read-set argument, the composed theorem, and the residual ladder's strengthenings
(R-b/R-c) — stays informal by design; the Lean package does not claim otherwise.

**New socket for the statement layer (this packet, not built here).** The discharge's
own arithmetic (Section 0/8.1) is entirely rational comparisons once the certified
values are printed: `F_box`'s numerator vs the threshold `(1-theta_band)*tau*`'s
numerator (both exact Fractions, gates V15-IA/V17-IA), `2*F_box` vs `tau*` (the
equilibrium-ceiling check), and the grid-500 `rho_prop`/`V_17` table (an extension, by 6
rows, of the same transcribed-table pattern (3) already uses). A sibling may extend the
Lean package with these as additional `decide`-checkable rational facts — `theta_band` is
itself an exact Fraction (`1505061/2500000`) and would transcribe the same way as the
other rational facts here; none of that is attempted in this packet.

## 12. (PROP-TAIL) consumer framing

**Scope.** This section, and this packet generally, concerns only this repository's
experimental-profile-ledger track: #880's `|K| = 1` dense-shell class-sum dichotomy and
#885's INV-TAIL closure chain. It makes no claim about, and is not on the critical path
of, any separately submitted manuscript's conditionals — those are a distinct
obligation, out of scope here.

**What #885/#880 gain now.** Before this packet, (PROP-TAIL) was a single opaque
numeric persistence claim: "the measured monotone decay of a cross-index spread,
certified on a grid to `n = 60`, continues." This packet first reduced that scalar to a
certified structural frame — an exact reduction (Lemma 1) that removes the two-branch
coupling from the target; an exact spectral gap (Lemma 3, `theta~ <= 1/5`, closed
form); a certified one-step recursion with an exact tangent-direction seminorm
(Lemma A1) and a corrected window bookkeeping (Lemmas W1-W3); a composed joint
induction (Section 7) — and then **closed it** as a certified-census theorem MODULO the
enumerated computed clauses (Section 8.4): the deep-base equilibrium route (R-a, Section
8.1) clears the arithmetic slot on finite checks, certified by an exact-Fraction,
lam-minced interval-arithmetic census of the tangent seminorm (gate V15-IA) feeding an
exact-Fraction minced interval-arithmetic forcing census (gate V17-IA) at a re-certified
floor family (gate F3, magnitude box verified by MAG-BOX) with full base coverage to
`n = 500` (gate V18), **plus** the real-vs-proportional gap (the geometric-center wobble
census, gate SIB-CERT, at a deep anchor `J0=800`, discharging computed clause (SIB-BAND)
given (LAM-BOX) alone; Section 8.4), **plus** — the magnitude box itself
(gate LAM-INV: proved invariant intervals for `lam`/`Lambda^+`/`Lambda^-`, discharging
computed clause (LAM-BOX)-conditional on the floor box, the finite base-case census, and
an a-posteriori Lipschitz self-check; Section 8.4), **plus** — this revision — the
correction-derivative cap itself (the (C'-CAP) clause: the last monitored-only literal
becomes a PROVED floor-box node-census bound, `0.004245 <= 3/500`, with the monitor
retained as a cross-check; Section 8.4) and first-class monitoring of the one remaining
imported input (gate FLOOR-DRIFT for (FLOOR-PERSIST), whose census-discharge route is
simultaneously CLOSED as route-cut Section 9(v)).
**(PROP-TAIL) is DISCHARGED as a certified-census theorem MODULO the enumerated
computed clauses ((FOLD), (FLOOR-PERSIST); Section 8.4) — STATUS CONDITIONAL**,
given this packet's own certified gate set
(F3/MAG-BOX/V15-IA/V16/V16b/V17/V17-IA/V18/SIB-CERT/LAM-INV/FLOOR-DRIFT). The two load-bearing gates
(V15-IA/V17-IA) certify the forced-proportional surrogate `c^+ = lam c^-` at the
shallower `J0*=500` anchor; gate SIB-CERT separately certifies the real,
non-proportional cascade at the deeper `J0_SIB=800` anchor; gate LAM-INV separately
proves the magnitude box both load-bearing gates box-max over is itself an invariant
interval, not merely a measured range.

**What #885/#880 gain now, concretely.** #885's own (PROP-TAIL) conditional is **closed
modulo the Section 8.4 computed clauses** by this packet's certificates. #885's INV-TAIL
closure chain therefore becomes **unconditional at every `B` modulo those computed
clauses** on this repository's experimental-ledger track, and with it #880's `|K| = 1`
dense-shell class-sum dichotomy becomes **unconditional at every `B` modulo those
clauses**, given this packet's green certificates together with #885's own certified
chain. The two open items (R-b's sandwich, R-c's sharp Edgeworth-1 lemma) are
**strengthenings** toward the sharp `C/n^2` law, not obligations the discharge itself
carries — they remain independently attackable future work (Section 8.2-8.3), and the
mu-sign tightener (Section 0, Section 8.1's honesty note) is a recorded NEGATIVE (does
not carry as a clean finite corner check) that the discharge does not need. General `K`
remains conjectural and unaffected by this packet (unchanged from the predecessor).
