# The C5 defect magnitude on the deployed Frobenius families

**Lane.** The **one OPEN residual** of PR #607
(`noncyclic_c5_slope_count.md`, Rung 4.2): #607 proved (Theorem A) that the C5
field-descent slope count is the cyclotomic defect `p^{d_p(G,I)}`,
`d_p(G,I)=|G|-|Z_p(G,I)|`, for **every** finite abelian slope group `G` with
`p \nmid |G|` (cyclic or not), but this bound is **payment-grade only when
`d_p(G,I)=o(|G|)`**. #607 measured a **trivial-Frobenius floor**
(`p \equiv 1 \pmod{\exp G}` gives `d_p=|G|-|I|`, vacuous) and left open whether
the **deployed** profile families the frontiers tex routes through C5 dodge it.
This note proves the magnitude bound on those families and settles the residual.

**Verifier.** `experimental/scripts/verify_c5_defect_magnitude.py` (stdlib-only,
zero-arg, `PASS: 151 checks`, ~38 s under `ulimit -v 2097152`; recomputes every
number below — Frobenius orders, orbit sizes, defect values, the sharp
threshold, Danny's Theorem 2, the necklace theorem, the decay census, and an
independent `F_{p^k}` fibre realization).

**Highest rung reached: 5 (magnitude PROVED on the one genuinely
Frobenius-active deployed family; the other two deployed families structurally
dodge the C5 defect payment; honest residual = the general binary-tower covering
constant).**

## One-line headline

*Across the **cyclic** slope groups the frontiers tex actually deploys, the C5
defect splits by the single integer `o=\operatorname{ord}_N(p)`: `o=1`
(prime-field `N\mid p-1`) is the vacuous floor **but is not a genuine C5 leaf**
(Frobenius fixes the profile, so its subfield profile equals the identity
profile, L2426); `o=2` (circle/twin-coset `N\mid p+1`, Frobenius `=` inversion)
obeys the **exact sharp law** `d_p=|G|-|I\cup(-I)|` with a threshold at prefix
depth `R=|G|/2`; and the **binary tower** (`N\mid 2^s-1`, `o=\operatorname{ord}_N(2)`)
is genuinely active with `d_2=O(1)` already at `R\ge|G|/2` — proved outright for
`N=2^s-1` by a **necklace/bit-rotation** argument and for prime `N` with `2` a
primitive root, and measured `O(1)` for every composite `N\mid 2^s-1` tested. So
the C5 payment is subexponential (indeed `O(1)`) on the one deployed family that
routes through it, at deep prefix `R\ge|G|/2` — i.e. on low-rate rows.*

---

## Rung 1 — FAMILY EXTRACTION: the deployed `(G,I,p)` triples

Source of truth: `asymptotic_rs_mca_frontiers.tex`. The extension/field-descent
cell **C5** is `L2422-2427`; its payment (per #545 `gap2_collapse_routing.md`
and #607) is the fibre bound `p^{d_p(G,I)}` where the slope group `G` is the
frequency group of the descended profile, `I\subseteq\hat G` is the syndrome
prefix, and Frobenius is `\chi\mapsto\chi^p`. The **deployed** field-descent
domains named in the tex are exactly two, **both with cyclic slope group** (a
finite subgroup of `K^\times` is cyclic):

| family | tex anchor | slope group `G` | prime `p` | Frobenius on `\hat G\cong\Z/N` | `o=\operatorname{ord}_N(p)` |
|--------|-----------|-----------------|-----------|--------------------------------|------------------|
| **F1 circle / twin-coset** | `def:circle-twin-domain` L2656 | `\Z/N`, `N\mid p+1` (torus `\UU=\{u:u^{p+1}=1\}`, order `p+1`) | odd `p\equiv3\!\!\pmod 4` | `c\mapsto pc\equiv -c` (**inversion**, since `u^p=u^{-1}`) | **2** |
| **F2 binary tower** | `rem:characteristic-two-rows` L2705 | `\Z/N`, `N\mid 2^s-1` (`N` odd) | `2` | `c\mapsto 2c` | `\operatorname{ord}_N(2)` (up to `s`) |
| **F0 prime-field dyadic** *(control)* | Danny #451 §7 excluded row | `\Z/N`, `N\mid p-1` | prime field `F_p` | `c\mapsto pc\equiv c` (**trivial**) | **1** |

The **syndrome profile** `I` is the **one-sided power-sum prefix**
`I=\{a,a+1,\dots,a+R-1\}` of depth `R` (the first `R` weighted power sums
`p_j(S)=\sum_{t\in S}\text{(wt)}\,t^{\,j}`), exactly as in Danny #451 Theorem 1
and #607. `R=|I|` is the prefix depth; `N=|G|` is the frequency-group order.
`[label: AUDIT — exact tex extraction; verifier TRICH.* confirms every `o`.]`

**Deviation from brief (flagged).** The brief's sketch named "QM31 / M31 tower
profiles." Those strings **do not occur** in `asymptotic_rs_mca_frontiers.tex`
(grep: only `binary-field` L400/L2706 and `circle`/`twin-coset`). They appear
only in Danny #451 §7's *uncovered-row* list. Mapped onto the trichotomy above:
**Mersenne-31 / KoalaBear** are **prime fields** (`p=2^{31}-1`,
`p=2^{31}-2^{24}+1`), so their multiplicative rows are **F0** (`N\mid p-1`,
`o=1`) — the trivial floor / not-a-C5-leaf (below). **QM31** `=F_{(2^{31}-1)^4}`
is a degree-4 extension: a genuine descent `F_{p^4}/F_p` with Frobenius of
**bounded order `\le 4`**, hence a **bounded-order** family analogous to F1
(needs a deep prefix; see Rung 3). Genuinely **non-cyclic** (product/tensor)
slope groups would require an *interleaved* row, which the tex explicitly places
**out of scope** (`rem:characteristic-two-rows` L2713-2715, "requires a separate
comparison theorem"). **Consequence:** #607's non-cyclic Theorem A is a
generalization *ahead of deployment*; the deployed magnitude question is the
three **cyclic** families F0/F1/F2. `[label: AUDIT — deviation documented.]`

---

## Rung 2 — the Frobenius-order trichotomy (the governing integer)

> **Lemma 1 (order trichotomy).** For a cyclic slope group `G=\Z/N` with
> `p\nmid N`, the Frobenius `c\mapsto pc` has order `o=\operatorname{ord}_N(p)`,
> and for the deployed families:
> `N\mid p-1\Rightarrow o=1`;  `N\mid p+1,\ N>2\Rightarrow o=2`;
> `N\mid 2^s-1` minimal `\Rightarrow o=\operatorname{ord}_N(2)\mid s`.

*Proof.* `N\mid p-1\Leftrightarrow p\equiv1`; `N\mid p+1\Leftrightarrow
p\equiv-1` (order 2 unless `N\le2`); the tower order is by definition. `\square`
The **defect depends only on `o` and the prefix**: `Z_p(N,I)=\bigcup_{c\in I}\{
c,pc,\dots,p^{o-1}c\}` and `d_p=N-|Z_p|`. `[label: PROVED — verifier TRICH.*,
ORBIT.* (closed form `\ell(c)=\operatorname{ord}_{N/\gcd(c,N)}(p)` vs iterated
orbit, all elements), DEFECT.2way (two independent routes agree).]`

---

## Rung 3 — magnitude per family

### 3.0 F0 trivial floor (`o=1`) — and why it is **not** a C5 leaf

For `N\mid p-1`, `Z_p(N,I)=I` and `d_p=N-|I|=N-R` — **maximal**, flat in the
Frobenius data (verifier `ORDER1.floor`, `TAMPER.floor`). This is #607's measured
vacuous floor. **But it never charges a C5 payment.** The C5 cell (L2426) is
invoked precisely when *"its natural subfield profile can be **larger** than the
identity profile."* When `o=1`, Frobenius fixes every frequency, so the
subfield (Frobenius-invariant) profile **equals** `I` **equals** the identity
profile: there is no enlargement, the trigger condition fails, and the leaf is
the **identity cell**, paid by the identity term — not a field-descent cell. The
`p^{N-R}` value is the trivial codimension bound, never a C5 charge.
`[label: PROVED (`d_p=N-R`) + AUDIT (structural: `o=1\Rightarrow` subfield
profile `=` identity profile `\Rightarrow` not a C5 leaf, honest reading of
L2426).]`

### 3.1 F1 circle / twin-coset (`o=2`) — exact law and sharp threshold

Frobenius is **negation** `c\mapsto-c` (inversion on the norm-one torus,
`u^p=u^{-1}`). Hence `Z_p(N,I)=I\cup(-I)` and

> **Theorem 2 (order-2 exact defect).**
> `d_p(N,I)=|G|-|I\cup(-I)|=N-2|I|+\#\{c\in I:\ -c\in I\}.`
> For the deployed **one-sided prefix** `I=\{0,\dots,R-1\}`:
> `d_p=\max(0,\ N-2R+1)`. Therefore `d_p=0` for `R>N/2`, `d_p=\Theta(N)` for
> `R/N` bounded below `1/2`, and the transition at `R=N/2` is **sharp**.

Verified on **every** interval position and length for
`N\in\{6,8,12,14,18,24\}` (`ORDER2.law`), the prefix threshold
`d=\max(0,N-2R+1)` (`ORDER2.threshold`), and the *centered/symmetric* profile
`I=\{-w,\dots,w\}` where `-I=I` gives the maximal `d=N-|I|` (`ORDER2.symmetric`)
— a second route to a vacuous bound, dodged because the deployed syndrome prefix
is **one-sided**, not centered. `[label: PROVED — exact closed form, census-exact
on all `(a,R)`; the threshold is sharp.]`

So the circle row's C5 defect is subexponential **iff the prefix reaches half
the torus, `R\ge N/2`**. This is a *deep-prefix / low-rate* condition (Rung 5),
and it is the exact frontier Danny #451 §7 flagged as uncovered
(`0<R/N\le1/2`). `[label: PROVED.]`

### 3.2 F2 binary tower (`o=\operatorname{ord}_N(2)`) — genuinely active

This is Danny #451 Theorem 2's mechanism at `p=2`, `N\mid 2^s-1`. Three proved
sub-results plus a census:

> **Theorem 3a (necklace / bit-rotation, `N=2^s-1`).** For `N=2^s-1`, doubling
> `c\mapsto2c \bmod N` is the **cyclic bit-rotation** of the `s`-bit binary
> representation. Every nonzero, non-all-ones `s`-bit string has a `0` bit, so a
> rotation with **leading bit `0`**, i.e. a representative in `[1,2^{s-1}]`.
> Hence `\{1,\dots,2^{s-1}\}` meets **every** nonzero doubling-coset, so
> `Z_2(N,\{1,\dots,R\})=(\Z/N)\setminus\{0\}` for `R\ge2^{s-1}=(N+1)/2`, giving
> `d_2=1` (only the fixed point `0`, absent from the prefix). Including `0`
> (`I=\{0,\dots,R-1\}`) gives `d_2=0`.

Verified `s=3..12` (`NECKLACE.half` `d=1` at `R=(N+1)/2`; `NECKLACE.cover` every
nonzero coset meets `[1,2^{s-1}]`; `NECKLACE.zero` `d=0` with `0`). `[label:
PROVED — clean `O(1)` at half prefix for the canonical tower unit group.]`

> **Theorem 3b (primitive root).** If `N` is prime and `2` is a primitive root
> mod `N` (`o=N-1`), every nonzero frequency has orbit `(\Z/N)\setminus\{0\}`, so
> `d_2\le1` for any interval meeting a nonzero frequency — for **all** `R\ge1`.

Verified (`ACTIVE.primroot`, incl. general `p` primitive roots). `[label:
PROVED.]`

> **Theorem 3c (Danny #451 Theorem 2, reproduced).** `p=5`, `N=2^s`,
> `R\ge\kappa N\Rightarrow d_5\le 2^{J_\kappa-1}`, `J_\kappa=\lceil\log_2(4/\kappa)
> \rceil`, using `\operatorname{ord}_{2^r}(5)=2^{r-2}`.

Verified by exhausting all interval positions/lengths for `s\le6` and worst-case
`R=\lceil\kappa N\rceil` for `s=7..10` (`DANNY2.order`, `DANNY2.bound`). `[label:
PROVED (reproduction) — the active-cyclic exemplar; our F2 is its `p=2` analog.]`

**Census (`DECAY.*`, the decisive curve).** `d_2(N,\{1..R\})/N` vs `R/N`, for
`N\mid 2^s-1` spanning near-primitive to structured:

```
 N=  31 ord=  5   R/N: 0.10→0.677 0.25→0.355 0.50→0.032 0.75→0.032 0.90→0.032 1.00→0
 N= 127 ord=  7   R/N: 0.10→0.614 0.25→0.228 0.50→0.008 0.75→0.008 0.90→0.008 1.00→0
 N= 255 ord=  8   R/N: 0.10→0.608 0.25→0.184 0.50→0.004 0.75→0.004 0.90→0.004 1.00→0
 N=2047 ord= 11   R/N: 0.10→0.511 0.25→0.097 0.50→0.001 0.75→0.001 0.90→0.001 1.00→0
 N=4095 ord= 12   R/N: 0.10→0.485 0.25→0.079 0.50→0.000 0.75→0.000 0.90→0.000 1.00→0
 N=  11 ord= 10   R/N: (flat 0.091 = 1/11 until 1.00→0)     [2 primitive root]
 N=  29 ord= 28   R/N: (flat 0.035 = 1/29 until 1.00→0)     [2 primitive root]
```

Readout: for **every** `N\mid2^s-1` tested, `d_2` has collapsed to `O(1)`
(`d\le2`) by `R/N=1/2`, and the larger `N` (more, longer cosets) mix faster.
The curve is monotone non-increasing in `R` (`DECAY.monotone`) and reaches
`d/N\le0.12` by `R/N=0.9` on the primitive/near-primitive rows
(`DECAY.active_small`). `[label: MEASURED — `O(1)` at deep prefix on all tested
`N\mid2^s-1`; the general-`N` proof of `d_2=O(1)` at `R\ge N/2` is the honest
residual (Rung 5).]`

---

## Rung 4 — independent fibre realization (Theorem-A cross-check)

To confirm the defect **is** the fibre exponent (not just an orbit count), the
verifier realizes `G=\Z/N` over `F_{p^k}` (`k=\operatorname{ord}_N(p)`,
`\zeta` a primitive `N`-th root of unity), builds the `F_p`-linear syndrome map
`x\mapsto(\sum_g x_g\zeta^{cg})_{c\in I}`, and checks (`FIBER.*`, 8 leaves across
all three families):

- **`F_p`-rank `=|Z_p(I)|`** exactly (Theorem A dimension count), so
  `\dim\ker=d_p`; and
- for `p=2`, full `\Omega=\{0,1\}^N`: **every nonempty fibre `=2^{d_p}`**
  (bound tight); for `p>2` Boolean `\Omega`: max fibre `\le p^{d_p}`.

This ties the abstract magnitude to the actual per-slope fibre size on circle
(`N=8\mid7+1`), tower (`N=15\mid2^4-1`), and trivial (`N=5\mid11-1`) leaves.
`[label: MEASURED — field-realized, independent of the orbit computation.]`

---

## Rung 5 — the (A5) route, deployment bridge, and outcome

### 5.1 (A5) verdict

(A5) (`def:admissible-sequence` L935-941): power-sum coordinates require
`R_N<\operatorname{char}\B_N`; small-characteristic leaves retain elementary
coordinates. **Does (A5) exclude the vacuous regime?**

- **By itself, no.** The trivial floor `o=1` needs `N\mid p-1`, i.e. `p\ge N+1`,
  so `R\le N<p=\operatorname{char}` — (A5)'s `R_N<\operatorname{char}` is
  **automatically satisfied**, so (A5) does not exclude `o=1`.
- **The exclusion is structural, from the C5 cell itself:** `o=1\Rightarrow`
  subfield profile `=` identity profile `\Rightarrow` not a field-descent leaf
  (Rung 3.0). This closes the *vacuous floor* unconditionally — it is simply the
  wrong cell.
- **(A5)'s char-2 branch is where the active family lives.** Char-2 leaves
  "retain elementary coordinates" — and the binary tower **F2** is exactly a
  char-2 field-descent leaf, with Frobenius `x\mapsto x^2` **active**. The
  Fourier/Frobenius defect count (Theorem A) is coordinate-agnostic, so it
  applies verbatim; (A5) routes F2 into the elementary-coordinate lane without
  weakening the defect bound.

`[label: PARTIAL/PROVED — (A5) alone does not exclude the floor; the C5-cell
trigger condition does. Verdict: the vacuous `o=1` floor is structurally
excluded; (A5) is not the mechanism.]`

### 5.2 Deployment bridge `R/N = 1-\text{rate}`

The deep regime is `3(n-a)\le n-k` (`thm:deep-regime-upper` L1785,
`prop:tangent-payment` L4670), and the natural syndrome depth is the redundancy
`R=n-k=(1-\rho)\,n` at code rate `\rho`. So the prefix ratio `r=R/N` is governed
by `1-\rho` (up to the domain-to-group ratio `n/N`). The threshold `R\ge N/2`
is therefore a **low-rate** condition (`DEPLOY.*` checks the arithmetic:
`\rho\le1/2\Rightarrow r\ge1/2\Rightarrow` circle `d_p=0`; `\rho>1/2\Rightarrow`
circle `d_p=\Theta(N)`). Deployed FRI/circle rows are low rate
(`\rho\in\{1/2,1/4,1/8,\dots\}`). `[label: AUDIT/MEASURED — the identification
`R=n-k` is the natural full-syndrome reading; pinning `r\ge1/2` for a **specific**
row still needs that row's `(|G|,R)` — the residual deployment check below.]`

### 5.3 What closes, and the honest wall

**Closes (unconditional on these routes):**
1. **Binary tower F2** — the one deployed family that genuinely routes through
   C5 with active Frobenius: `d_2=O(1)` at `R\ge N/2`, **proved** for `N=2^s-1`
   (necklace) and prime `N` with `2` primitive, reproducing Danny #451 Theorem 2
   at `p=2`. So `#545` routing `+` `#607` count `+` this magnitude bound is a
   **complete unconditional C5 chain on the binary-tower cell** at deep prefix.
   `[PROVED]`
2. **Circle / twin-coset F1** — exact sharp law `d_p=|G|-|I\cup(-I)|`; the C5
   payment is subexponential **iff `R\ge|G|/2`** (deep prefix), and the sharp
   threshold pins exactly where a shallow-prefix circle leaf would be vacuous.
   `[PROVED]`
3. **Trivial floor F0** — reclassified: `o=1` leaves are identity cells, not C5;
   the `d_p=N-R` floor never charges a C5 payment. So it is **not** a
   counterexample to uniform C5 payment. `[PROVED + AUDIT]`

**The honest wall (next atomic statement):**

> **Residual.** Prove `d_2(N,\{1..R\})=o(N)` (ideally `O_\kappa(1)`) for **every**
> `N\mid2^s-1` at `R\ge\kappa N` — the general-divisor binary-tower covering
> constant. Proved here for `N=2^s-1` (necklace) and prime `N` with `2` a
> primitive root; **measured `O(1)`** for all composite `N\mid2^s-1` tested
> (`N\in\{255,2047,4095\}`), but the uniform constant over the full divisor
> lattice (adversarial `N` where a `\kappa N`-interval could miss many short
> cosets) is not proved. Equivalently: is the doubling-coset partition of
> `\Z/N` **interval-covering** at density `\kappa` for every `N\mid2^s-1`? Plus
> the **deployment check** `R\ge|G|/2` (`\rho\le1/2` after the `n/N` domain
> factor) for the specific circle rows.

`[label: OPEN — the residual is now one clean covering constant, not the whole
non-cyclic magnitude question.]`

---

## Per-claim label summary

| claim | label |
|-------|-------|
| deployed C5 families are the two cyclic rows F1 (circle, `N\|p+1`) + F2 (tower, `N\|2^s-1`); QM31/M31 absent from tex | `AUDIT` (extraction + deviation) |
| Frobenius-order trichotomy `o=1/2/\operatorname{ord}_N(2)`; defect `= N-|Z_p|` two ways | `PROVED` |
| F0 `o=1`: `d_p=N-R` maximal | `PROVED` |
| F0 is **not** a C5 leaf (subfield profile `=` identity profile) | `AUDIT` (structural, L2426) |
| **Theorem 2**: F1 order-2 exact law `d_p=N-|I\cup-I|`; sharp threshold `d_p=\max(0,N-2R+1)` | `PROVED` (census-exact) |
| F1 symmetric/centered profile gives vacuous `d=N-|I|`; deployed prefix is one-sided | `PROVED` |
| **Theorem 3a**: F2 `N=2^s-1` necklace `\Rightarrow d_2=1` at `R\ge(N+1)/2` | `PROVED` |
| **Theorem 3b**: F2 primitive-root `\Rightarrow d_2\le1` | `PROVED` |
| **Theorem 3c**: Danny #451 Theorem 2 (`p=5,N=2^s`) reproduced | `PROVED` (reproduction) |
| F2 census: `d_2=O(1)` at `R/N=1/2` on all `N\|2^s-1` tested | `MEASURED` |
| fibre realization: `F_p`-rank `=|Z_p|`; `p=2` full `\Omega` fibre `=2^{d_p}` (tight) | `MEASURED` |
| (A5) `R_N<\operatorname{char}` does **not** exclude the floor; the C5 trigger does | `PROVED/PARTIAL` |
| deployment bridge `R/N=1-\rho`; low-rate `\Rightarrow R\ge N/2` | `AUDIT/MEASURED` |
| C5 payment subexponential on all deployed routes at deep prefix (F2 proved, F1 threshold, F0 rerouted) | `PROVED` (F2) + `PROVED` (F1 conditional on `R\ge N/2`) |
| general-`N\|2^s-1` covering constant `d_2=o(N)` at `R\ge\kappa N` | `OPEN` |

**Credit / lineage.** Defect object, cyclic Theorem 1 bound, and the dyadic
active exemplar (Theorem 2, `\operatorname{ord}_{2^r}(5)=2^{r-2}`):
**DannyExperiments #451** (`asymptotic_c9_frobenius_cyclotomic_defect.md`),
whose §7 named exactly these uncovered rows (prime-field `N\|p-1`, circle/
twin-coset, KoalaBear/M31/QM31) — this note certifies them. Non-cyclic Theorem A,
the orbit closed form, and the trivial-Frobenius floor: **PR #607**
(`noncyclic_c5_slope_count.md`). C5 routing: **#545**
(`gap2_collapse_routing.md`). Frobenius-closure primitive
`(\sum a_i\omega_i)^p=\sum a_i\omega_i^p` is Lean-backed zero-`sorry`
(`c9_frobenius_closure_lean_backing.md`, `sum_smul_pow`).
`GF(p^k)`/`rank_fp` idiom reused from `verify_noncyclic_c5_count.py` (#607).

**Boundaries respected.** `(MI)`/`(MA)`/entropy-inverse (scottdhughes) consumed
as black box, never attacked. Danny #529, latifkasuli #518 untouched. No
`.tex`/`.pdf` edited (audit-ledger discipline). The circle-vs-tower routing and
the low-rate deployment reading are stated as `AUDIT`, not claimed as tex edits.
