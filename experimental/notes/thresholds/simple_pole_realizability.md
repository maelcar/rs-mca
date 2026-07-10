# Simple-pole lower-reserve realizability (frontiers input 5 / #524 L-3)

**Status:** EXPERIMENTAL / AUDIT.
**Verdict:** **PROVED** (realizability holds unconditionally on the SB2 window)
**+ corrected two-regime bracket** (the AUDIT caveat of #524 L-3 dissolves).

Target: `experimental/asymptotic_rs_mca_frontiers.tex`.
Attacks hard input 5 (lower reserve / unsafe-side comparison): settle whether
`prop:simple-pole-lower`'s witness construction is realizable exactly on the
window where SB2 of `thm:unconditional-support-envelope-bracket` invokes it.

Consumes (never attacks): scottdhughes #498/#501/#505; Codex #517 (named the
three hypotheses -- root counting, pole averaging, value-to-bad-slope geometry);
LegaSage #521/#532 (statement-level lower-reserve anchors). Builds directly on
the delta-audit #524 (`asymptotic_frontiers_delta_audit.md`, ledger entry L-3),
which flagged this as `AUDIT` but did not settle it. Off-limits: Danny #529,
latifkasuli #518.

Verifier: `experimental/scripts/verify_pole_realizability.py` -> `RESULT: PASS
(18 checks)`, ~53 s, stdlib only.

---

## 1. Anatomy (labels + lines in `asymptotic_rs_mca_frontiers.tex`)

**MCA-bad slope** (L187-201): slope `g` is support-wise MCA-bad at agreement `a`
if some support `S`, `|S|>=a`, explains `r0+g r1` (a deg-`<k` poly matches on
`S`) but does not simultaneously explain the pair. Equivalently (both received
words are deg-`<k`-explained on `S` iff each is): **`g` is bad via `S` iff
`r0+g r1` is explained on `S` and `r1` is not** (then `r0` is not either).
`B^MCA_{C,Gamma}(a)` = max over received pairs of #distinct bad slopes in `Gamma`.

**Lower leg -- pole reserve** `prop:simple-pole-lower` (L6180, "Exact unsafe
test"), reused as `P(a)` in SB1 (L6217-6223):

```
  L(a) = ceil( binom(n,a) |B|^{-(a-k-1)} )                      (identity list floor)
  M(L) = ceil( L(q-n) / (q-n + k(L-1)) )                        (4.2, L2006)
  P(a) = ceil( (|Gamma|/q) * M(L(a)) )                          (challenge-restricted)
  P(a) > B*  ==>  a unsafe.
```

Its three-step provenance (the realizability *surface*, named by Codex #517):

1. **root counting / value-to-bad-slope** -- `thm:collision-aware-pole` (L1996):
   given `L` distinct dim-`(k+1)` codewords agreeing with one word on `>=m>=k+1`
   points, one received line for the dim-`k` code has `>=M(L)` distinct MCA-bad
   slopes. Proof: at a pole `alpha`, `P_i(alpha)=P_j(alpha)` at `<=k` poles
   (deg-`<=k` difference has `<=k` roots); pole averaging gives a pole with
   `<=k binom(L,2)/(q-n)` collisions; Cauchy-Schwarz `L^2<=M sum m_i^2` yields
   `M(L)` distinct values.
2. **pigeonhole list** -- `prop:exact-prefix-list` (L1965, bijection): the dim-
   `(k+1)` codewords agreeing with `U_z` on `>=a` points are exactly `(U_z-Q_S)`,
   `S` in the depth-`w` prefix fiber (`w=a-k-1`); some word has list size
   `>= L(a)`. `cor:identity-prefix-floor` (L2031, 4.3) packages `B^MCA(a)>=M(L(a))`.
3. **pole/outer averaging** -- `prop:simple-pole-lower` proof (L6201-6208):
   shifting the line `(r0,r1)->(r0+d r1,r1)` translates the bad-slope set `Z` by
   `-d`; averaging over `d in F` gives some translate with `>= |Z||Gamma|/q`
   bad slopes inside `Gamma`.

**Upper leg** `prop:exact-support-upper` (L1361, 2.2): `U(a)=min{|Gamma|,
binom(n,a)}` (injective noncommon-support map -- #524 checked proof).

**Bracket** `thm:unconditional-support-envelope-bracket` (L6211):
`P(a_-)>B*`, `U(a_+)<=B*`, `a_-<a_+`  ==>  `a_- < a* <= a_+` (SB3, L6231);
adjacent ==> `a*=a_+`; SB4 (L6235) `binom(n,k+1)<=B* ==> a*=k+1`.

**Deep-regime machinery** (the true numerator, used to test overshoot):
- `thm:deep-regime-upper` (L1790, 3.5): linear `C`, min weight `d`, `r=n-a`,
  `3r<=d-1` ==> `B^MCA(a)<=r+1`.
- `prop:universal-tangent-floor` (L1833, 3.6): `B^MCA_{C,Gamma}(a) >=
  min{|Gamma|,n-a+1}` for **every** `a>=k+1`, unconditionally.
- `cor:exact-deep-numerator` (L1854): for RS, `3(n-a)<=n-k` ==>
  `B^MCA_{C,Gamma}(a) = min{|Gamma|, n-a+1}` **exactly** (`E(a)` below).
- `thm:intro-unconditional-asymptotic-deep` (L249): in the deep regime the
  threshold is exactly `a*=n-B*+1` -- and it is proved from the tangent floor,
  **not** from `P`.

Write `E(a)=min{|Gamma|, n-a+1}`, `a_deep = ceil((2n+k)/3)` (first deep `a`,
since RS has `d-1=n-k`).

---

## 2. The realizability question, and its resolution

The bracket's lower leg is sound at `a_-` iff `P(a_-) <= B^MCA_{C,Gamma}(a_-)`
(i.e. `P` is a genuine, realizable floor). #524's L-3 caveat: `P` "overshoots
the true `r+1` numerator inside the deep regime", so realizability must be
pinned. Two facts settle it.

### 2a. Min-distance rigidity: the true list is `<=1` above `(n+k)/2` [PROVED]

The dim-`(k+1)` code `C^+ = RS(D,k+1)` has minimum distance `d^+ = n-k`. Let
`c_1 != c_2` be two `C^+`-codewords each agreeing with a received word on `>=a`
coordinates, with agreement sets `A_1,A_2`. On `A_1 cap A_2` both equal the
received word, so `c_1-c_2` (a nonzero deg-`<=k` polynomial) vanishes there;
having `<=k` roots forces `|A_1 cap A_2| <= k`. Hence
`|A_1 cup A_2| = 2a - |A_1 cap A_2| >= 2a-k`, and `<= n`, so

```
    a list of size >= 2  requires  2a - k <= n,  i.e.  a <= (n+k)/2.        (star)
```

So for `a > (n+k)/2` the **true** list size is `<= 1`. This is exactly the
Johnson-distance-`>= w+1` content of `prop:prefix-rigidity-full` (L2044):
distinct supports in one depth-`w` fiber differ in `>= w+1 = a-k` places, so
overlap `<= k`.

### 2b. The deep regime is strictly inside the list-`<=1` zone [PROVED, gated A1/A2]

```
    a_deep = ceil((2n+k)/3) > (n+k)/2   <=>   (2n+k)/3 > (n+k)/2   <=>   n > k,
```
always true (`k<n`), with margin `(2n+k)/3-(n+k)/2 = (n-k)/6 > 0`. Verified for
all `n<=219`, every `k<n` (check A1/A2).

### 2c. Consequently `P` never overshoots -- it collapses to `1` in the deep regime [PROVED, gated B1/B2]

The pigeonhole floor cannot exceed the true list: the biggest prefix fiber has
`>= L(a)` supports, each a genuine distinct `C^+`-codeword agreeing on `>=a`
points (`prop:exact-prefix-list`), so `L(a) <= true list`. Combined with (star),
for `a>(n+k)/2` we get `L(a) <= 1`, hence **`L(a)=1`**. Equivalently the pure
arithmetic bound

```
    binom(n,a) <= |B|^{a-k-1}     for all  a > (n+k)/2   (|B|>=n)             (B1)
```

is forced (a failure would make `prop:exact-prefix-list` contradict the `C^+`
minimum distance -- a genuine bug). **Gated: 0 failures over 83 892 cases**
(all `a>(n+k)/2`, `|B| in {n,n+1,2n}`, `n<=69`). Therefore throughout the deep
regime `a>=a_deep > (n+k)/2`:

```
    L(a)=1  =>  M(L(a))=M(1)=1  =>  P(a)=ceil(|Gamma|/q)=1     (0<|Gamma|<=q).
```

**Gated: `L(a)=1` and `P(a)=1` on the whole deep regime, 0 failures over
310 144 cases** (check B2). The "raw heuristic `binom(n,a)|B|^{-w}` overshoots
`r+1`" reading of #524 is about the pre-ceiling value; the *realized* floor is
`P=1`, which cannot overshoot anything: `1 <= E(a)`. **No overshoot occurs.**

### 2d. `P` is a valid realizable floor everywhere [PROVED, gated D1/D2; brute E1-E3]

Since `L(a) <= true list` and `M` is monotone when `q-n>=k` (and `M<=1`-capped
otherwise), `M(L(a)) <= M(true list) <= B^MCA(a)`; the outer average keeps the
`|Gamma|/q` factor, so `P(a) <= B^MCA_{C,Gamma}(a)` **unconditionally** (given
`q>n` and the prefix-field hypothesis, sec. 4). As a *consistency* certificate,
`P` never exceeds the exact upper `U(a)` either:

```
    P(a) <= U(a)   for ALL  a in [k+1,n]     -- 0 failures / 711 288 cases   (D1)
    P(a) <= E(a)   on the deep regime        -- 0 failures / same grid       (D2)
```

Brute force (faithful support-wise noncommon MCA count, sec. 5):
- **E1** deep `F5,n=4,k=1,a=3` (reproduces #524, exhaustive `5^8`):
  `B^MCA=2=E=r+1`, and `P=1<=2`.
- **E2** shallow `F11,n=3,k=1,a=2` (exhaustive `11^6`, the SB2 window):
  `P=3 <= B^MCA=3 <= U=3` -- realizable and **tight to `U`** -- and
  `B^MCA=3 > E=2`: here `P` strictly tightens the reserve.
- **E3** non-constant `k=2, F7, n=4, a=3` (sampled): `P=2 <= B^MCA <= U=4`.

---

## 3. Overshoot / realizability map

Coordinates: agreement `a in [k+1,n]`; deep boundary `a_deep=ceil((2n+k)/3)`;
list boundary `(n+k)/2` (from (star)); `E(a)=min{|Gamma|,n-a+1}` = universal
tangent floor. Zone census over 711 288 parameter tuples (check D4):

| zone | agreement range | `L(a)` | `P(a)` vs true count | role |
|---|---|---|---|---|
| **shallow, list>=2** | `k+1 <= a <= (n+k)/2` | can be `>1` | `P` realizable; can be `P>E` (strict) or `P=E` | **`P` operative**, may beat tangent floor |
| **intermediate** | `(n+k)/2 < a < a_deep` | `=1` | `P=1 <= E` | `P` trivial; tangent floor `E` operative |
| **deep** | `a >= a_deep` | `=1` | `P=1 = min(...)-bounded <= E`; `E` **exact** | `P` redundant; `E=B^MCA` exact |

- **`P` overshooting the true numerator: EMPTY zone** -- never observed; `P<=U`
  everywhere and `P<=E=B^MCA` on the deep regime (D1/D2). The failure mode
  "unsafe-side lower reserve not actually crossing the target" does **not** occur.
- **`P` realizable-and-strictly-useful** (`P>E`): occurs **only** in the shallow
  `a<=(n+k)/2` band, non-deep -- 3 034/711 288 tuples, **all** in that band
  (D4). Example `k=1,n=4,q=13,a=2`: `L=6, M=4, P=4 > E=3`, `U=6`.
- **`P` realizable-but-redundant** (`P<=E`, `P` collapsed): the entire deep +
  intermediate range `a>(n+k)/2` (`P=1`).

**SB2 window extraction.** For `B*>=1`, `{a : P(a)>B*}` is contained in the
shallow band `a<=(n+k)/2` (elsewhere `P=1`). So SB2 invokes `P` **only on
`a_- <= (n+k)/2`** -- precisely the window where the identity list is realizable
(`L(a)>=1` genuine codewords) and (star) rules out the deep overshoot.
**Realizability holds exactly on the SB2 window.** [rung 3(i) PROVED]

---

## 4. Realizability hypotheses (the surface, made explicit)

`P(a) <= B^MCA_{C,Gamma}(a)` holds under, and only needs:

- **(H1)** `q = |F| > n` -- an auxiliary pole `alpha in F\D` exists and the
  collision average runs over `q-n >= 1` poles (`thm:collision-aware-pole`).
- **(H2)** `D subseteq B subseteq F` with `B` closed under the support-locator
  prefix map (a **subfield** suffices): then every `a`-support has its depth-`w`
  locator prefix in `B^w`, so the pigeonhole "`binom(n,a)` supports over `|B|^w`
  prefixes" (`prop:exact-prefix-list`) is valid and `L(a)` is a genuine list
  floor. This is the load-bearing hypothesis behind `L(a)<=true list`.
- **(H3)** *(presentation, not soundness)* on the deep window `3(n-a)<=n-k` the
  operative and exact leg is `E(a)=min{|Gamma|,n-a+1}` (`cor:exact-deep-numerator`);
  `P` is used on the shallow window `a<=(n+k)/2`, where `P=1` cannot occur for a
  nontrivial reserve.

No hypothesis is *missing* for soundness -- `P` is a valid lower bound wherever
it is `>1` -- but (H1)-(H3) are the "realizability/regime hypotheses" #524 L-3
asked to see printed next to SB2.

---

## 5. Corrected honest lower reserve (two-regime bracket)

The universal tangent floor makes both legs unconditional lower bounds:

```
    B^MCA_{C,Gamma}(a)  >=  max{ P(a), E(a) },   E(a)=min{|Gamma|, n-a+1}.
```

Unsafe test (honest form): `max{P(a_-),E(a_-)} > B*`. This is strictly stronger
than `P(a_-)>B*` and needs no case split for soundness. The clean two-regime
reading:

- **Deep window `a >= a_deep`** (`3(n-a)<=n-k`): `E` is **exact**,
  `B^MCA = min{|Gamma|,n-a+1}`; the bracket collapses to an **equality**, and if
  `1<=B*<=n-k-1` and `3(B*-1)<=n-k` the threshold is exactly `a*=n-B*+1`
  (`thm:intro-unconditional-asymptotic-deep`, already in the paper). `P` is
  redundant here.
- **Shallow window `a <= (n+k)/2`**: `P` is a genuine realizable floor that can
  exceed `E` (mapped band), tightening the unsafe reserve. This is where SB2
  actually invokes `P`.

So the AUDIT caveat dissolves into a cleaner statement: **the deep leg is the
exact count `E`; the pole floor `P` is a valid, realizable strengthening on the
shallow window and is never invoked (nontrivially) inside the deep regime.**
This is the ideal outcome flagged in the task ladder.

---

## 6. Per-claim labels

| # | claim | verdict | basis |
|---|---|---|---|
| C1 | `P(a) <= B^MCA(a)` unconditionally (given H1,H2) | **PROVED** | consumes `prop:exact-prefix-list`+`thm:collision-aware-pole`+outer avg; cross-checked `P<=U` D1 |
| C2 | true list `<= 1` for `a>(n+k)/2` (star) | **PROVED** | `C^+` min-distance / `prop:prefix-rigidity-full`; brute B3 |
| C3 | deep regime strictly inside list-`<=1` zone | **PROVED** | `a_deep>(n+k)/2` iff `n>k`; A1/A2 |
| C4 | `L(a)=1`, `P(a)=1` on the deep regime | **PROVED** | (star)+pigeonhole; arithmetic B1 (83 892 cases), B2 (310 144 cases) |
| C5 | `P` never overshoots the true numerator (empty overshoot zone) | **PROVED** | D1 (`P<=U`, 711 288), D2 (`P<=E` deep) |
| C6 | `P` strictly useful (`P>E`) only in shallow `a<=(n+k)/2` band | **PROVED** | zone census D4 (3 034 cases, all in band) |
| C7 | SB2 invokes `P` only on `a_- <= (n+k)/2` (realizability on the window) | **PROVED** | `P=1` above the band + monotonicity |
| C8 | brute-force realizability & tightness (deep + shallow + k=2) | **PROVED (finite)** | E1 (`F5` exhaustive), E2 (`F11` exhaustive), E3 (`F7` sampled) |
| C9 | two-regime bracket `B^MCA>=max{P,E}`, `E` exact on deep | **PROVED** | `prop:universal-tangent-floor`+`cor:exact-deep-numerator`; D3 |
| -- | general-linear-code equality beyond RS toy families | NOT CLAIMED | brute force is RS toy scale only |

Difference from siblings: #524 L-3 flagged this `AUDIT` and asked for the
hypotheses to be printed; **this note proves realizability on the SB2 window
and supplies the corrected two-regime bracket**, turning the caveat into a
theorem-level statement. LegaSage #521/#532 anchor the legs at statement level
(and Lean deployed rows) but do not resolve the pole-construction realizability.

---

## 7. Proposed paper change (definitive #524 L-3, `asymptotic_rs_mca.md` convention)

### Ledger entry L-3' (supersedes #524 L-3; bracket lower-leg realizability RESOLVED)

- **Source:** this note; `verify_pole_realizability.py` (18 gated checks).
- **Status:** `AUDIT` -> **RESOLVED / PROVED** (realizability) + **PROMOTION
  CANDIDATE** (two-regime bracket wording).
- **Paper impact on `thm:unconditional-support-envelope-bracket` (L6211):**
  1. Print the realizability/regime hypotheses next to SB1/SB2: **(H1)** `q>n`;
     **(H2)** `D subseteq B` with `B` prefix-closed (subfield) so `L(a)` is a
     genuine list floor.
  2. Add one clause: *"On the deep window `3(n-a)<=n-k` the lower leg is the
     exact count `E(a)=min{|Gamma|,n-a+1}` (`cor:exact-deep-numerator`); the
     pole floor `P` is invoked only on the shallow window `a<=(n+k)/2`, where
     `L(a)>=1` genuine dim-`(k+1)` codewords realize it. On the deep window
     `L(a)=1` (min-distance rigidity, since `a>(n+k)/2`), so `P(a)=1` and `P`
     never overshoots the true numerator."*
  3. Optionally state the unified honest reserve `B^MCA(a) >= max{P(a),E(a)}`
     and the unsafe test `max{P(a_-),E(a_-)}>B*` -- both legs unconditional
     lower bounds (`prop:universal-tangent-floor`, `prop:simple-pole-lower`).
  4. Retire the "overshoot inside the deep regime" phrasing of #524 L-3: the
     realized floor is `P=1` there, so there is no overshoot; the deep leg is
     the *exact* `E`, and the bracket collapses to an equality (already covered
     by `thm:intro-unconditional-asymptotic-deep`).
- **Next action:** the "Unconditional" title stays honest once (H1)-(H2) and the
  deep/shallow split are printed. No TeX/PDF edited here (audit convention).

---

## 8. Wall / dead cheap routes (checked)

- **Precise statement.** For `C=RS_F(D,k)`, `q>n`, `D subseteq B` prefix-closed,
  `Gamma` nonempty, and `k+1<=a<=n`: `P(a) <= B^MCA_{C,Gamma}(a) <= U(a)`
  (realizable floor), with `P(a)=1` whenever `a>(n+k)/2`; on `3(n-a)<=n-k`,
  `B^MCA = E(a) = min{|Gamma|,n-a+1}` exactly. SB2 invokes `P` only on the
  shallow window `a_-<=(n+k)/2`.
- **Dead route 1 (naive):** "use `P` as the lower leg in the deep regime" --
  dead, `P=1` there (B2); must use `E`.
- **Dead route 2:** "prove `P<=B^MCA` by a fresh construction in the deep
  regime" -- unnecessary and impossible to make nontrivial: the true list is
  `<=1` (star), so no construction yields `>1` bad-slope-via-list there;
  `E`/tangent floor is the only nontrivial deep floor.
- **Dead route 3:** "`P` might overshoot for large `|B|`" -- larger `|B|` only
  *shrinks* `L(a)` and `P`; worst case is `|B|=n`, already gated (B1).
- **Dead route 4:** "the outer `|Gamma|/q` average could fail to land in
  `Gamma`" -- it is a translation of the bad-slope set intersected with
  `Gamma`; averaged occupancy `>= |Z||Gamma|/q` (consumed from
  `prop:simple-pole-lower` proof, #517-formalized).

---

## 9. Replay

```bash
python3 experimental/scripts/verify_pole_realizability.py
# -> RESULT: PASS (18 checks)   (~53s, stdlib only)
```
