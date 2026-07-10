# CAP25 v13 raw: the signed-e_m inverse at the binding Mersenne-31 list row (a_+=1116023) is a Chebyshev-domain participation-ratio bound — nu*_ref = 2^5.781 ~ 55

Status: `PARTIAL`. Per-claim:
`REFERENCE` (target statement + provenance §1; exact reproduction of `nu*_ref = 2^5.781 ~ 55` §2; four-row table §5) /
`REDUCED` (the `(STAR) <=> PR <= nu*` reduction transfers verbatim to the M31 Chebyshev domain — domain-agnostic algebra, §3) /
`PROVED` (L1 value-distribution reduction on the Chebyshev domain §6a; the **new** Chebyshev-fold self-similarity lemma §6b — the faithful M31 analog of the mu_n packet's L2; the M31 dead-route margins §4; the w=1 non-collapse §6c) /
`MEASURED` (faithful Chebyshev toy §7 — the inverse holds with large room and behaves like the mu_n domain) /
`OPEN≡crux` (the bound `PR(Rhat) <= nu*_ref` itself — the finite-row primitive effective-support theorem, §8) /
`AUDIT` (weave §9).

**Verifier:** `experimental/scripts/verify_m31_signed_em_inverse.py`
(zero-arg, stdlib-only, `EMINV_AS_CAP_GB` / `EMINV_DATA_DIR` knobs, `~80 s`,
`RESULT: PASS (59/59 checks)`, exit 0): exact big-int M31-list ledger; the
`nu*_ref` arithmetic and both M31 dead-route margins; the four-row `nu*_ref`
table matched to `grande_finale.tex` `prop:q-exact-target`; the `(STAR)<=>PR<=nu*`
reduction sampled; L1 value-distribution on a Chebyshev domain; the Chebyshev-fold
self-similarity lemma over 960 quotient directions; the w=1 non-collapse (with a
full-group control that *does* collapse); the faithful Chebyshev toy against a
**recomputed** mu_n reference (byte-matching integrated PR #414: R=1.4923,
L1/C=0.5302, PR=20.50); Parseval + the PROVED energy floor gated on every shipped
row; twin-coset validity (chi 2-to-1, T_2-tower, D not product-closed);
offset-robustness; the falsification guard; and seven tamper self-tests.
Data: `experimental/data/cap25_v13_m31_signed_em_inverse.json`.

## What this is / is not (merge framing)

The participation-ratio packet (`cap25_v13_q_em_inverse_participation_ratio.md`,
integrated e83962ae, was PR #414) named the M31-list `nu*_ref = 2^5.781 ~ 55` as
*"the sharpest, most concrete standalone target the program has"* for the `(STAR)`
route — but its structural lemmas and toys are on the **multiplicative** subgroup
`mu_n` (the KoalaBear domain). The Mersenne-31 rows do **not** live on `mu_n`: the
usable finite symmetry is the **Chebyshev / twin-coset** structure of the norm-one
torus (`cap25_v13_m31_chebyshev_fixed_remainder_floor.md`, *"Domain correction"*;
`cap25_v13_qfin_rung_audit_m31.md` §1; `cap25_cap_v13_raw.tex` `sec:circle-geometry`,
`thm:fiber-descent`, `lem:cheb-fibers`). This packet supplies the **faithful
M31-domain content** of that node: it re-states the target on the correct domain,
proves the Chebyshev analog of the packet's `mu_n` self-similarity lemma, recomputes
the dead-route margins for the M31 row, and instruments a faithful Chebyshev toy.

It does **not** prove `U(1116023) <= B*`, close `prob:row-sharp-q` /
`def:q-row-atom`, or prove the signed-e_m inverse at M31-list. The bound itself
stays `OPEN≡crux`. Every claim carries a label. **No counterexample was found at
faithful toys** — consistent with the atom being true (`kappa <= 1.221`, was #407).

---

## 1. The target, stated exactly, with provenance  `REFERENCE`

The deployed binding row (`grande_finale.tex` `prop:q-exact-target`, L2061; the
`Mersenne-31 list` row; recomputed exactly, `verify` §1):

```
p = 2^31-1 = 2147483647   n = 2^21 = 2097152   k = 2^20 = 1048576   (list route K=k)
a_+ = 1116023   w = a_+-k = 67447   m = n-a_+ = 981129
B* = floor((2^31-1)^4/2^100) = 2^24-1 = 16777215
avg_ceil = ceil(C(n,a_+)/p^w) = 1993678       Delta_Q = log2(B*/avg_ceil) = 3.0730 bits
```

The signed-e_m object is the exact Fourier transform of the prefix fiber count
(`grande_finale.tex` `prop:fourier-audit`, L1156; Hughes's observation on the PR
#397 thread; Parseval-exact). For a domain `D subset F_p`, prefix map
`Phi_w(M) = (p_1(M),...,p_w(M))`, `N(z) = |Phi_w^{-1}(z)|`, `Fbar = C(n,m)p^{-w}`:

```
E(t) = sum_{|M|=m, M in D} e_p(t . Phi_w(M)) = e_m(v_t),  v_t=(e_p(f_t(x)))_{x in D},
       f_t(x)=sum_{i=1}^w t_i x^i,   e_p(x)=exp(2 pi i x/p),
max_z N(z) <= p^{-w}( C(n,m) + sum_{t!=0} |e_m(v_t)| ).                 (Fourier bound)
sum_{t!=0}|E(t)|^2 = p^w sum_z (N(z)-Fbar)^2.                           (Parseval)
```

By (Fourier bound) the row-sharp Q atom (`def:q-row-atom`, L2043;
`max_z |P_Q(z)| <= B*` after first-match payments) **follows from** the exact `L^1`
target named by the parent packet (`cap25_v13_q_pw2_concentration_floor.md` §7,
was #412; `cap25_v13_q_em_inverse_participation_ratio.md` §0, was #414):

```
(STAR)     sum_{t != 0} |e_m(v_t)|  <=  (K - 1) * C(n,m),      K = B*/ceil(avg).
```

The barrier-map single-lemma frontier item (`cap25_v13_route_d_barrier_map.md`,
open PR #431, node `O414` / M31-list #1) states the target in the form worked here:

> **[holmbuar] max-fiber signed-e_m inverse at M31-list** — `PR(Rhat) ≤ nu*_ref =
> 2^5.781 ≈ 55` (effective Fourier support ≈55 of `2^2090857` directions). Per #414
> this is *"the sharpest, most concrete standalone target the program has"* for the
> direct atom. *Closes:* `def:q-row-atom` at the binding row.

The `(STAR)` verbatim reformulation (participation-ratio packet §1, transferred to
this row):

```
Rhat(t) := e_m(v_t);   PR(Rhat) := ||Rhat||_1^2 / ||Rhat||_2^2   (participation ratio);
Gamma2 := p^w sum_z N(z)^2 / C^2 (>=1),   ||Rhat||_2^2 = C^2(Gamma2-1)   (Parseval);
(STAR)  <==>  PR(Rhat)  <=  nu* := (K-1)^2 / (Gamma2-1).
```

## 2. `nu*_ref = 2^5.781 ~ 55`, derived from the row constants  `REFERENCE`

At the `Gamma2-1 = 1` reference (`verify` §2, exact `Fraction`):

```
K       = B*/ceil(avg) = 16777215/1993678 = 8.415208            (matches tex ratio 8.4152)
nu*_ref = (K-1)^2 = (7.415208)^2 = 54.98531 = 2^5.780974 ~ 55
#dir    = p^w - 1,   log2(#dir) = 2090856.99995 (~ 2^2090857).
```

**Reading:** row-sharp Q at M31-list **follows once the signed-e_m spectrum has
effective (Fourier) support at most ~55 directions** out of `2^2090857`, calibrated
by its own `L^2` energy — a `2^-2090851` fraction of all directions must be
Fourier-negligible. `nu*_ref` is the `Gamma2-1 = 1` reference; the true budget is
`(K-1)^2/(Gamma2-1)`, sufficient whenever `Gamma2-1 <= 1` (the faithful toy §7 has
`Gamma2-1 = 0.0109`, so `nu*_ref` is the operative budget, `~92x` conservative).

## 3. The reduction transfers verbatim to the Chebyshev domain  `REDUCED`

`(STAR) <=> PR <= nu*` is pure algebra on the spectrum: divide `(STAR)^2` by the
fixed number `||Rhat||_2^2 = C^2(Gamma2-1)`. Nothing in the derivation uses the
geometry of `D` — (Fourier bound) and (Parseval) are stated for **any**
`D subset F_p` (`prop:fourier-audit`). So the equivalence holds unchanged at the
M31 Chebyshev twin-coset. `verify` §5 re-checks it on the faithful Chebyshev toy's
concrete spectrum (Parseval relerr `6.4e-15`) and confirms the `(STAR) <=> PR`
biconditional at sample budgets `K in {2,3,5}`.

This is the **only** part of the KoalaBear participation-ratio machinery that
carries to M31 with no new work. The structural lemmas (§6) do **not**: they were
`mu_n`-specific and must be re-derived for the Chebyshev domain.

## 4. The M31 dead-route margins (recomputed for this row)  `PROVED`

The two routes the parent packets proved dead at KB are dead here too, with
**exact new M31 margins** (`verify` §3):

| route | object | M31-list dead by | KB analog |
|---|---|---:|---:|
| `L^2` / `r=2` / Plancherel | `p^{w/2}` floor (trivial-support C-S) | **1,045,425.61 bits** | 1,045,396.58 (#412) |
| `L-infinity` / uniform per-direction | `beta* = (K-1)/(p^w-1)` | **2,090,854.11 bits** | 2,090,815.35 (#414) |

```
(w/2) log2 p = 1045428.50 bits;  L^2 floor short by (w/2)log2 p - log2(K-1) = 1045425.61.
L-infinity: a uniform |e_m|/C <= beta* must beat beta* = 2^-2090854.11; short by 2090854.11.
```

Both M31 margins **strictly exceed** the KB analogs: the M31 budget `K-1 = 7.415`
is tiny (vs KB's `4.8e6`), so every norm-inequality route is *even deader*. The win
can come only from **sparsity** (few large directions) plus **cancellation** (most
directions negligible) — the participation-ratio target of §1, not any
single-direction or second-moment inequality.

## 5. Four-row `nu*_ref` context  `REFERENCE`

`nu*_ref(row) = (K-1)^2`, `K = B*/ceil(avg)` (matched digit-for-digit to
`grande_finale.tex` `prop:q-exact-target`, `verify` §4):

| row | a_+ | w | K = B*/avg | log2 nu*_ref | log2(#dir) | domain |
|---|---:|---:|---:|---:|---:|---|
| KoalaBear MCA  | 1116048 | 67471 | 4807520.9295 | 44.394 | 2090837.54 | mult. coset `alpha mu_n` |
| KoalaBear list | 1116047 | 67471 | 4226236.5253 | 44.022 | 2090837.54 | mult. coset `alpha mu_n` |
| Mersenne-31 MCA  | 1116024 | 67447 | 9.5722 | 6.199 | 2090857.00 | Chebyshev / twin-coset |
| **Mersenne-31 list** | **1116023** | **67447** | **8.4152** | **5.781** | **2090857.00** | **Chebyshev / twin-coset** |

**M31-list is binding** (smallest `nu*_ref ~ 55`). The two M31 rows are the ones on
the Chebyshev domain — exactly the ones the `mu_n` machinery does not directly cover.

## 6. The faithful M31 (Chebyshev) structure  `PROVED`

**The domain.** `p' = 2^31-1 = 3 mod 4`, so `F_{p'^2} = F_{p'}(i)` and the norm-one
torus `U` (the circle group) is cyclic of order `p'+1 = 2^31` — a **pure 2-group**.
The deployed row is a standard-position **twin coset** `D_cal = gH cup g^{-1}H` of
size `2M`, `M = 2^21`; the x-coordinate map `chi(u) = Re(u)` is exactly 2-to-1
(`g^2 notin H`), landing on `D := chi(D_cal) subset F_{p'}`, `|D| = M = n`. For
`c | n` the Dickson/Chebyshev map `T_c` (`x -> T_c(x)`, `T_2(x)=2x^2-1`) is exactly
`c`-to-1 on `D` (`lem:cheb-fibers`, `thm:fiber-descent`). The toy uses the smallest
faithful analog: `p = 2^e-1` a small Mersenne prime (`p in {31,127}`, `U` a pure
2-group exactly as at deployment), `D` the x-projection of a twin coset of a
2-power subgroup of `U`; `verify` §9 confirms `chi` 2-to-1, the T_2-tower
`16,8,4,2,1`, `T_2` exactly 2-to-1, and that **`D` is NOT product-closed** (a
genuine Chebyshev domain, not a multiplicative subgroup).

### 6a. L1 (value-distribution reduction) — general, holds on Chebyshev D  `PROVED`

`e_m(v_t)` depends **only** on the value multiset `{f_t(x) : x in D}`:
`e_m(v_t) = [T^m] prod_s (1 + T e_p(s))^{N_t(s)}`, `N_t(s)=#{x in D: f_t(x)=s}`. So
the entire inverse is a statement about **level-set concentration of degree-w
polynomials on the Chebyshev domain**. Toy-verified on `D` (`verify` §6, identical
value-distributions give identical `|e_m|` to `9e-15`).

### 6b. Chebyshev-fold self-similarity — the faithful analog of the `mu_n` lemma L2  `PROVED` (new)

> **Lemma (Chebyshev fold).** If `f_t` is constant on the `T_c`-fibers of `D`
> (`c | n`; i.e. `f_t(x) = g(T_c(x))` as a function on `D`), then since `T_c` is
> exactly `c`-to-1 on `D`, the value multiset `{f_t(x): x in D}` is `c` copies of
> `{g(y): y in D_c}` (`D_c = T_c(D)`, the smaller twin coset), and
> ```
> e_m(v_t) = [T^m] ( E_g(T) )^c,   E_g(T) = prod_{y in D_c}(1 + T e_p(g(y))) = sum_j e_j(w_g) T^j.
> ```

**Proof.** Immediate from L1: the multiset is `c`-fold, so `prod_s(1+Te_p(s))^{N_t(s)}
= (prod_{y in D_c}(1+Te_p(g(y))))^c = E_g(T)^c`; extract `[T^m]`. The only input is
"`T_c` is `c`-to-1 on `D`", which the twin-coset tower guarantees. `verify` §7:
holds to `2.2e-14` over all `960` `c=2` quotient directions at `p=31,n=8`.

This is the M31 replacement for the `mu_n` packet's L2 (which used `x -> x^c`). Two
faithful cautions carried from `cap25_v13_qfin_rung_audit_m31.md`: (i) the clean
descent lives in the **Chebyshev basis** (`sum_x T_{cj}(x) = c sum_{y} c_M(y)T_j(y)`,
its `(*_T)`), not the monomial basis — ordinary power sums `p_i` do **not** vanish
off multiples of `c` for a `c`-symmetric `M`; (ii) the fiber *count* is nonetheless
basis-independent (invertible triangular change of basis, `char > w`), which is why
`|e_m|` — a function of the value multiset (L1) — is unaffected.

### 6c. w=1 does NOT collapse to `|e_m|=1` on the Chebyshev domain  `PROVED`

The `mu_n` packet recorded a full-group collapse: for `D = F_p^*` and `w=1`,
`|e_m(v_t)| = 1` exactly (cyclotomic identity, behind `prop:mode-null-false`). This
is a property of the **full** multiplicative group and holds on **neither** deployed
domain: on the Chebyshev `D` the w=1 magnitudes `|e_m|/C` range over `[0.0002,0.233]`
(`p=31`) and `[0,0.045]` (`p=127`) — genuinely spread (`verify` §8, with a
full-group control that *does* collapse to `1`). Honest structural difference: the
faithful M31 w=1 spectrum has no single-magnitude rigidity to lean on.

## 7. Faithful toy: the inverse holds with large room  `MEASURED`

Deployment-faithful regime (`avg >> 1`), the only regime that models the deployed
`avg_ceil = 1993678`. Chebyshev `p=127,n=16,m=8,w=1` (`avg=101.3`) beside the
`mu_n` reference (`cap25_v13_q_em_inverse_participation_ratio.md` §5, **recomputed**
here, `verify` §10):

| domain | p | n | m | w | avg | R_true | Gamma2-1 | L1/C | max\|e\|/C | PR | budget checks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Chebyshev** | 127 | 16 | 8 | 1 | 101.3 | **1.3026** | 0.0109 | **0.4298** | 0.04459 | **16.94** | PR≤55 ✓, L1/C≤7.42 ✓, R≤8.42 ✓ |
| mult. `mu_n` | 97 | 16 | 8 | 1 | 132.7 | 1.4923 | 0.0137 | 0.5302 | 0.02914 | 20.50 | (packet #414) |

Two measured facts:
1. **In the faithful regime the Chebyshev domain behaves essentially like the
   multiplicative one.** `PR = 16.9` (Chebyshev) vs `20.5` (`mu_n`) — both `<< 55`;
   `L1/C = 0.43` vs `0.53` — both `<< 7.42 = K-1`; `R_true = 1.30` vs `1.49` — both
   `<< 8.42 = K`. The signed-e_m spectrum is **genuinely sparse** and the raw
   `(STAR)`/`PR <= nu*_ref` holds with large room. The measurement is robust across
   twin-coset offsets (`PR in {16.4,16.9}`, `verify` §11). So **the inverse is
   almost certainly TRUE at M31-list; the wall is proof-method** — consistent with
   the `kappa <= 1.221` calibration (was #407) and the KB toy story.
2. **The primitive stratum carries the wall.** In the `w>=2` Chebyshev toys the
   primitive (coefficient-scale-1) directions hold **90–98%** of the `L^1` mass
   (`verify` §10, shares `0.905/0.922`) — the faithful analog of the `mu_n` packet's
   83–93%. Killing only the quotient (Chebyshev-fold-borne) directions is
   insufficient; the reduction must control the **primitive** Chebyshev spectrum.

## 8. Falsification guard + the named obstruction  `OPEN≡crux`

**Falsification search.** Above-bound spikes (`raw PR > nu*_ref`, `L1/C > K-1`)
occur **only** in the `avg << 1` regime — where the **atom itself fails**
(`R_true > K`): e.g. Chebyshev `p=31,n=8,w=2`, `avg=0.073`, has `PR=411.9 > 55` but
also `R=27.5 > 8.42` (`verify` §12). These are not counterexamples to
`inverse => atom`, and not the deployment regime. **No near-`nu*_ref` primitive
spike lacking the conjectured (approximately-Chebyshev-fold) structure was found in
the faithful `avg >> 1` regime.** Witness-first: had one appeared it would headline;
none did. (This is *consistent with* — and a faithful-domain sharpening of — the
masked-residual audit's finding that the raw `(STAR)` is overstrong only in a
non-faithful full-group `w=3` toy; §9.)

**The obstruction (headline OPEN).** What remains is exactly the **finite-row
primitive effective-support theorem on the Chebyshev value-sequence**
`(f_t(x))_{x in D}`: prove `PR(Rhat) <= nu*_ref ~ 55` after Chebyshev-fold
(quotient) directions are removed. This is the M31/Chebyshev counterpart of the open
structural steps 4–6 of `prob:entropy-inverse-q`'s `rem:entropy-inverse-skeleton`
(entropy-BSG `->` PFR/Green–Ruzsa structuralization `->` slice-derivative, or the
free-energy decay alternative; steps 5–6 flagged nonstandard) — now with the
**Dickson/Chebyshev** self-similarity (§6b) in place of the multiplicative one.
Nothing here closes it; §4 shows no single-direction or second-moment inequality can
reach it (dead by `> 10^6` bits).

## 9. Weave  `AUDIT`

- **Participation-ratio packet** — `cap25_v13_q_em_inverse_participation_ratio.md`
  (integrated e83962ae, was PR #414) — *extends / domain-faithful follow-on*. It
  named the M31-list `nu*_ref = 2^5.781` target and proved the `(STAR)<=>PR<=nu*`
  reduction; §3 here transfers that reduction to the Chebyshev domain, and §6b
  supplies the Chebyshev analog of its `mu_n` lemma L2. Non-conflicting: same open
  input, correct domain. Its `mu_n` §5 faithful toy is recomputed here (byte-match).
- **Concentration-floor packet** — `cap25_v13_q_pw2_concentration_floor.md`
  (integrated e83962ae, was PR #412) — *extends*. Its `p^{w/2}` `L^2` floor is
  recomputed for the M31 row (§4: `1,045,425.61` bits); §4 also adds the
  `L-infinity` column (`2,090,854.11` bits) for M31.
- **Masked-residual audit** — `cap25_v13_signed_em_masked_residual_audit.md`
  (was PR #413) — *scope-clarifying, non-conflicting*. It proves raw `(STAR)` is a
  **sufficient but possibly overstrong** certificate; its full-group `F_17` `w=3`
  toy has raw `1+L1_prim/C = 10.473 > 8.4152 = K` while `R_true = 2.672 < 8.4152`.
  Our §7 shows that overstrongness is an `avg<<1`/large-w artifact: in the faithful
  Chebyshev `avg>>1` toy `L1/C = 0.43 << K-1`. This packet treats the **raw**
  target (the barrier-map node); the masked `PR(E_Q on P_Q)` variant is #416's.
- **Eq-masked participation + lift-class refutation** —
  `cap25_v13_q_eq_masked_participation_ratio.md` (was #416) +
  `cap25_v13_liftclass_cost_model_refuted.md` (was #417) — *consistent-with*. #416's
  M31 masked route (`tau=0.4107`, triangle `10.473 -> 5.967 < 8.4152`) is
  **conditional** on an unpaid lift-class removal, which #417 **refutes**. We do not
  rely on masking; we treat the raw target and report it holds with room at faithful
  toys.
- **M31 domain sources** — `cap25_v13_m31_chebyshev_fixed_remainder_floor.md`
  (DannyExperiments, was #426; *"Domain correction"*) and
  `cap25_v13_qfin_rung_audit_m31.md` (ours; §1 circle geometry, identity `(*_T)`) —
  *provenance-consumed*. The Chebyshev/twin-coset domain, the `T_c` fold, and the
  monomial-vs-Chebyshev-basis caution are theirs; `cap25_cap_v13_raw.tex`
  `sec:circle-geometry` / `thm:fiber-descent` / `lem:cheb-fibers` is the paper-level
  source. **DannyExperiments' `CAP25-V13-M31-C1024-PAIRED-PREFIX-PRIMITIVE-Q` object
  is his and is untouched here** — a different (planted-residual) route.
- **Barrier map** — `cap25_v13_route_d_barrier_map.md` (open PR #431,
  `thresholds-route-d-barrier-map`) — *fills-in-node*. This packet supplies the
  Chebyshev-domain content of its node `O414` / M31-list single-lemma frontier #1.
- **Hughes / #397** — the Fourier identity `E(t)=e_m(v_t)` is Hughes's observation
  (PR #397 thread); consumed as provenance, re-verified Parseval-exact. #397's
  primitive full-rank signed-defect certificate is the primal side of this Fourier
  crux (KB row).
- **Binding-row calibration** — `cap25_v13_q_atom_binding_row_calibration.md` (was
  #407) — *consistent-with*. Its `kappa <= 1.221` matches the faithful `R_true ~ 1.3`
  (§7): the atom is almost certainly true; the wall is proof-method.

### One-line verdict
The signed-e_m inverse at the binding **Mersenne-31 list** row is a Chebyshev-domain
Fourier participation-ratio bound `PR(Rhat) <= nu*_ref = (K-1)^2 = 2^5.781 ~ 55`;
the `(STAR)<=>PR<=nu*` reduction transfers verbatim (domain-agnostic), the Chebyshev
self-similarity lemma is proved (new, toy-verified), the `L^2` and `L-infinity`
routes are dead by `1,045,425.61` / `2,090,854.11` bits, and the faithful Chebyshev
toy shows the inverse holds with large room (`PR = 16.9 << 55`) exactly like the
`mu_n` domain — but the bound itself, the finite-row primitive effective-support
theorem, stays `OPEN≡crux`. No counterexample at faithful toys.

## 10. Nonclaims (restated)

This packet does **not** prove:
```
U(1116023) <= B*, or any deployed safe row;
prob:row-sharp-q (grande_finale.tex L2177) or def:q-row-atom (L2043);
the signed-e_m inverse / PR <= nu*_ref at M31-list (the crux stays OPEN);
```
It does **not** touch DannyExperiments' `CAP25-V13-M31-C1024-PAIRED-PREFIX-PRIMITIVE-Q`
object (his; a different route). The faithful toys are all `w=1` (the only way to
reach `avg >> 1` at small `n,p`); the deployed row has `w = 67447`, so the toy
evidence is `w=1` evidence, honestly extrapolated — exactly the limitation the
`mu_n` packet carried.

## 11. Reproduce
```
python3 experimental/scripts/verify_m31_signed_em_inverse.py
#   RESULT: PASS (59/59 checks), exit 0 (~80 s) -- everything above, self-contained.
```
