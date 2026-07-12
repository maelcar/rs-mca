# Lower reserve / unsafe-side comparison: adversarial route/coverage audit (hard input 5)

**Status:** `AUDIT` (adversarial route/coverage map of hard input 5).
**Verdict:** **VERIFIED-CURRENT / NO PRINT CHANGE FORCED.** The printed
lower-reserve/unsafe-side obligation is decomposed into 11 discrete routes;
**7 are PAID** by integrated tree material and in-paper theorems, **2 are
PAID-ON-INTEGRATION** of open PRs (#669, #680; with #690 as audit-tier
corroboration of a paid route), and **2 coupled routes remain OPEN**. The
umbrella phrasing ("complete profile envelope with the target and lower
reserve") is still the sharpest honest form because those two residuals are
genuinely open; no printed statement is forced to change.

Target: `experimental/asymptotic_rs_mca_frontiers.tex` (read at
`upstream/main` = `36de5bf`). Attacks the maintainer's hard input 5
(`agents.md` L50 "lower reserve / unsafe-side comparison"; adversarial failure
mode `agents.md` L98 "unsafe-side lower reserve not actually crossing the
target"). This is the unsafe-side analogue of the same-pattern coverage audits
of hard inputs 2 and 4.

**Consumes (never attacks or extends — corners stay with their owners):**
- **DannyExperiments #669** — challenge-restricted syndrome-secant lower bound
  (`syndrome_secant_challenge_lower.md`), `PROVED`;
- **DannyExperiments #680** — exact full-field capacity-adjacent frontier
  (`full_field_capacity_adjacent_frontier.md`), `PROVED` conditional on #669;
- **latifkasuli #690** — envelope-rung-ledger deployed lower-side floor audit
  (`envelope_rung_ledger.md`), `NO ISSUE`.
Also consumes the already-integrated `simple_pole_realizability.md`,
`mca_unsafe.md`, `unsafe_at_crossing.md`, and `certified_valueset_lower.md`,
and the in-paper unconditional deep/tangent theorems.

**Verifier:** `experimental/scripts/verify_lower_reserve_unsafe_coverage.py`
-> `RESULT: PASS (45 checks)`, ~5 s, stdlib only. It byte-verifies every quoted
anchor at its cited line (negative-tested: corrupted quotes must be absent),
recomputes every echoed number, and reproduces `B^MCA(3)=2` over `F5` by
exhaustive support-wise MCA count.

---

## 1. The printed obligation (primary sources, verbatim)

Hard input 5 is stated in four coupled places. Quotes are byte-verified at the
cited line by the verifier.

**Umbrella (abstract), `asymptotic_rs_mca_frontiers.tex` L159--162:**
> "the unrestricted positive-density frontier still requires a
> witness-exhaustive atlas, image-scale MI and MA or a direct / Sidon payment,
> residual ray bounds, and **comparison of the complete profile / envelope with
> the target and lower reserve**."

**Umbrella (effective-normalization theorem recap), L777--782:**
> "An unrestricted smooth/circle profile-envelope theorem still requires ...
> **complete envelope domination, and / the target and lower reserve
> comparisons**."

**Definitional (the object to supply), L980--986:**
> "a *certified profile-list construction* is an explicit list inside one
> identity, quotient, Chebyshev, or remainder / profile, together with the
> **pole and challenge-intersection estimates that / prove its bad-slope count
> exceeds the target**."

**Target-reserve, unsafe side, L6135--6139:**
> "on the unsafe side it is the amount / **by which the logarithm of a proved
> bad-slope construction exceeds** / `log_2 B_n^*`."

The obligation therefore has two faces. **(i) A lower bound / unsafe test:** a
proved bad-slope construction whose count provably exceeds `B_n^*` at some
`a_-`. **(ii) Sharpness:** that `a_-` must land within `o(n)` of the true safe
crossing, so the target-aware bracket (`thm:intro-asymptotic-rs-mca`, L988;
`thm:main-ledger`, L1125) closes. Face (ii) is where the paper is explicit that
this is an *input*: `cor:intro-identity-frontier` (L6280--6281)
> "**assumes, rather than / deduces** from exponent notation, that quantitative
> reserves furnish the / **exact safe and unsafe tests within** `o(n)` of that
> crossing";

and `prop:entropy-crossing-detail` (L6675, "Target-aware crossing criterion")
requires (L6683--6684)
> "a quantitative reserve dominates / all errors and pole collisions."

---

## 2. Obligation decomposition and route classification

Each route is one discrete piece of hard input 5, with its primary anchor and
its coverage verdict. Labels: **PAID** (integrated tree or in-paper theorem),
**PAID-ON-INTEGRATION** (of a named open PR), **OPEN** (exact statement given).

| # | Route (anchor) | Verdict | Paid by |
|---|---|---|---|
| **O3** | Exact unsafe test / identity pole floor `P(a)>B*` (L6180 `prop:simple-pole-lower`, eq 13.3 L6194); realizability | **PAID** | `simple_pole_realizability.md` (integrated): `P(a) <= B^MCA_{C,Gamma}(a)` unconditionally given `q>n` + prefix-closed `B`; realizable exactly on the SB2 window |
| **O4** | Literal target reserve / unconditional bracket SB2: `P(a_-)>B*`, `U(a_+)<=B*` (L6211 `thm:unconditional-support-envelope-bracket`; L6239 "literal target reserve ... no asymptotic placeholder") | **PAID** | in-paper (unconditional finite comparison) + lower-leg realizability (`simple_pole_realizability.md`) |
| **O6** | Target-reserve definition, unsafe side (L6135--6139) | **PAID** | definitional; instantiated by O3/O8 |
| **O8** | Deep-regime unsafe side, unconditional exact threshold `a*=n-B*+1` (L249 `thm:intro-unconditional-asymptotic-deep`; L1833 `prop:universal-tangent-floor`; L1854 `cor:exact-deep-numerator`) | **PAID** | in-paper; `E(a)=min{|Gamma|,n-a+1}` is exact on `3(n-a)<=n-k`, all characteristics, no atlas/Fourier/RC |
| **O9** | Deployed-row lower leg `L(a0)>B*` at the four adjacent rows (finite adjacent certificate) | **PAID** + **AUDIT** | `mca_unsafe.md` + `unsafe_at_crossing.md` (integrated, `PROVED`); corroborated PAID-ON-INTEGRATION by **latifkasuli #690** (no rung fires at `a0+1`) |
| **O5a** | Certified profile-list, **identity** profile with challenge-intersection LB (L980--986) | **PAID** | `simple_pole_realizability.md` (identity list `L(a)` realized by genuine dim-`(k+1)` codewords on `a<=(n+k)/2`) |
| **O5b** | Certified profile-list, **value-set / knife-edge** profile | **PAID** | `certified_valueset_lower.md` (integrated): `|F|>B*` with `e1 mod p` injective |
| **D1** | `a=k+1` unsafe for **every** target `eps<1`, uniform in `Gamma`, `log q=o(n)` | **PAID-ON-INTEGRATION #669** | **DannyExperiments #669** syndrome-secant second-moment + challenge average; eq (2) fraction `-> 1` |
| **D2** | `a=k+1` **full-field** `eps=2^-128` exact transition `q_crit=2^128 binom(n,k+1)`; top-two-row `a=k+2` consumer | **PAID-ON-INTEGRATION #680** | **DannyExperiments #680** (stacked on #669); three integer branches at `s=1`, closed endpoint |
| **O5c** | Certified profile-list, **quotient / Chebyshev / remainder** profiles with challenge-intersection LB (the "any larger ... list" clause, L6197) | **OPEN** | — |
| **O7** | Crossing sharpness in the **intermediate identity-dominant window** `(n+k)/2 < a_- < a_deep`: an unsafe `a_-` within `o(n)` of the interior entropy crossing `g_{T,n}` (L6280--6281 assumption; L6683--6684 reserve requirement) | **OPEN** | — |

**Counts: 7 PAID (O3,O4,O6,O8,O9,O5a,O5b) + 2 PAID-ON-INTEGRATION (#669, #680;
plus #690 audit-tier on O9) + 2 OPEN (O5c, O7).**

---

## 3. Coverage inventory: what each consumed input pays

### 3a. Integrated tree material (PAID today)
- **`simple_pole_realizability.md`** (frontiers input 5, prior audit). Proves
  the pole floor `P` is a realizable lower bound and supplies the corrected
  **two-regime reserve** `B^MCA_{C,Gamma}(a) >= max{P(a), E(a)}`,
  `E(a)=min{|Gamma|,n-a+1}`: deep window `a>=a_deep=ceil((2n+k)/3)` has `E`
  *exact*; shallow window `a<=(n+k)/2` has `P` a genuine strengthening; the
  intermediate window has `P` collapsed to `1`. Pays **O3, O4, O5a**, and the
  realizability half of the SB2 comparison.
- **`mca_unsafe.md` / `unsafe_at_crossing.md`.** `B_C(a_safe-1)>B*` at the
  adjacent unsafe grid point, by an exhaustive collision-free / collided split.
  Pays **O9** (deployed lower leg).
- **`certified_valueset_lower.md`.** Value-set lower bound `|F|>B*` (injective
  `e1 mod p`) for knife-edge rows. Pays **O5b**.
- **In-paper unconditional theorems.** `thm:intro-unconditional-asymptotic-deep`
  (L249), `prop:universal-tangent-floor` (L1833), `cor:exact-deep-numerator`
  (L1854), and `thm:unconditional-asymptotic-rs-mca` (shallow-prefix exponent).
  Pay **O8** and anchor **O6**.

### 3b. Open PRs (PAID-ON-INTEGRATION)
- **DannyExperiments #669** — a *new* unsafe-side mechanism distinct from the
  pole floor. Parity-column span second moment (Cauchy--Schwarz `|U_t| >=
  N_t q^{2t}/S_t(q)`) plus transversal syndrome-line incidence and a
  challenge average. Its eq (2), specialized to `a=k+1` (`t=R-1`),
  `B^MCA(k+1) >= ceil(G(q-1)N/(q(N+q-1)))`, `N=binom(n,k+1)`, has fraction
  `-> 1` when `k/n->rho` and `log q=o(n)`; hence `a=k+1` is unsafe for every
  `limsup eps<1`, uniformly in `Gamma`. Pays **D1**. It explicitly does not
  certify a safe row or either prize threshold — its corner stays its own.
- **DannyExperiments #680** (stacked on #669) — closes the full-field
  `eps=2^-128` case at `s=1` into an exact iff transition
  `q_crit=2^128 binom(n,k+1)` below the official cap `q<2^256`, with the
  top-two-row consumer `a*=k+2` on the displayed integer interval. Pays **D2**.
  Its own "remaining wall": in the branch `binom(n,k+2)>B*` one must locate the
  *first deeper lower crossing* — that is exactly route **O7** below.
- **latifkasuli #690** — the complete lower-side floor ledger at the four moved
  deployed adjacent pairs (`21` dyadic rungs x `4` slack profiles, exact integer
  mass vs `B*`): **no rung fires** at `a0+1`, verdict `NO ISSUE`. AUDIT-tier
  corroboration of **O9** (paid-on-integration). The single sub-bit watch-item
  (`m31_mca`, `Gceil`, `c=2048`, margin `-0.3938` bits) does not fire at the
  proved `b=0` endpoint multiplier; the verifier reproduces its `b=1`
  sensitivity flip.

---

## 4. Gap analysis: the two coupled OPEN residuals

The paid routes tile the unsafe side at its **endpoints** and on the **deployed
finite rows**, but leave one interior asymptotic band, in two coupled directions
of the comparison:

**O5c (which profiles).** `prop:simple-pole-lower` (L6196--6198) states its
conclusion "with `L_n` replaced by **any larger identity, quotient, Chebyshev,
or remainder-profile list** proved for the dimension-`k_n+1` code." Only the
identity list (O5a) and the value-set list (O5b) are supplied with a
challenge-intersection lower bound. The quotient / Chebyshev / remainder
profile-list constructions of the *general* profile envelope are an input, not a
theorem: `def` at L980--986 requires "the pole and challenge-intersection
estimates that prove its bad-slope count exceeds the target" for each such
profile, and these are not produced in general.

**O7 (where the crossing is).** Between the two paid endpoints there is an
interior band. Concretely, with `E(a)=min{|Gamma|,n-a+1}`,
`a_deep=ceil((2n+k)/3)`, and the identity-list boundary `(n+k)/2`:

- `a=k+1` (and the top-two `a=k+2`): paid-on-integration by #669/#680.
- `a >= a_deep`: paid — `E` exact (O8).
- deployed finite rows: paid (O9).
- **`(n+k)/2 < a_- < a_deep`, identity-dominant, interior crossing:** here the
  pole floor has collapsed (`P(a)=1`, verified) and `E(a)` is a valid but
  *not-proved-exact* lower bound; neither the `k+1` mechanism nor the deep
  tangent floor lands within `o(n)` of the interior entropy crossing `g_{T,n}`.
  This is precisely the band `cor:intro-identity-frontier` **assumes** away
  (L6280--6281) and that `prop:entropy-crossing-detail` flags as needing a
  reserve that "dominates all errors and pole collisions" (L6683--6684).

### Sharpest remaining honest statement (OPEN)

> Let `C_n=RS_{F_n}(D_n,k_n)` be a ledger-admissible smooth/circle row sequence
> with full-field or certified-intersection challenge `Gamma_n`, `k_n/n->rho`,
> an identity-dominant agreement window, and an interior entropy crossing
> `0 < g_{T,n} < 1-rho_n` (so `F_n(g)=H_2(rho_n+g)-beta_n g` meets the target
> level `tau_n=n^{-1}log_2(1+B_n^*)` transversally) whose crossing agreement
> `a_n=k_n+1+g_{T,n} n+o(n)` lies in the intermediate/shallow band
> `(n+k_n)/2 < a_n < a_deep`, i.e. strictly below the deep regime and strictly
> above the `k+1` shell. **Exhibit a certified profile-list construction —
> inside one identity, quotient, Chebyshev, or remainder profile — that is
> unsafe at some `a_{-,n}=a_n-o(n)`.** Equivalently, prove that the two-regime
> lower reserve `max{P(a),E(a)}` (or a profile-specific list floor carrying its
> own challenge-intersection lower bound) crosses `B_n^*` within `o(n)` of the
> safe crossing, for all sufficiently large `n`.

Discharging this **unconditionalizes** `cor:intro-identity-frontier` (removes
its "assumes, rather than deduces" clause) and closes DannyExperiments #680's
"first deeper lower crossing" wall. O5c and O7 are logically coupled: a general
profile-list construction that reaches the interior crossing supplies both.

---

## 5. Print determination (verified-current, #684 pattern)

Given the coverage above, **the printed umbrella phrasing is the sharpest honest
form and no printed statement is forced to change:**

- The abstract (L159--162) and recap (L777--782) say the complete-profile-
  envelope-vs-target-and-lower-reserve comparison "still requires ..." — and
  routes **O5c + O7 are genuinely open**, so the umbrella claim is accurate.
  Narrowing it to any paid endpoint (deep regime, `k+1`, or the SB2 finite
  window) would wrongly under-state a broad open input, exactly the error the
  hard-input-2/4 audits avoided.
- Every unsafe-side theorem the paper does print — `prop:simple-pole-lower`
  (O3), `thm:unconditional-support-envelope-bracket` (O4),
  `thm:intro-unconditional-asymptotic-deep` (O8) — is verified current and
  correctly labelled unconditional; the "literal target reserve ... no
  asymptotic placeholder" claim (L6239) holds.

**Optional, non-forced adjacency (defer to owner).** `simple_pole_realizability.md`
already proposes (its section 7) printing the realizability hypotheses `q>n`
and prefix-closed `B` and the unified reserve `B^MCA >= max{P,E}` next to
SB1/SB2. That proposal stands on its own; this audit does not duplicate or
override it and forces nothing.

---

## 6. Per-claim labels

| # | claim | verdict | basis |
|---|---|---|---|
| A | 24 obligation anchors byte-current at `36de5bf`, negative-tested | **AUDIT** | verifier ANCHOR block |
| B | routes O3,O4,O6,O8,O9,O5a,O5b PAID | **PAID** | integrated notes + in-paper theorems (cited) |
| C | D1 paid-on-integration #669 (`a=k+1` unsafe, all `eps<1`) | **COMPUTED** | eq (2) fraction `-> 1`, `>2^-128` for `n<=512` |
| D | D2 paid-on-integration #680 (`q_crit=2^128 binom(n,k+1)`; same-domain pair) | **COMPUTED** | closed endpoint + `3^96 < 2^128 binom(128,65) < 3^160` |
| E | O9 audit-tier corroboration #690 (no rung fires; `b=1` flip) | **COMPUTED** | `B*=2^24-1`; `2*12,769,758 > 16,777,215` |
| F | two-regime realizability arithmetic (`a_deep>(n+k)/2 iff n>k`; `P` collapse; E1/E2) | **COMPUTED** | grids (0 failures) + toy `L,M,P` |
| G | `B^MCA(a=3)=2` over `F5`, so pole floor `P=1` realizable, non-overshooting | **PROVED (finite)** | exhaustive `5^8` support-wise MCA count |
| H | O5c and O7 open (sharpest statement in section 4) | **OPEN** | absence of a general profile-list / interior-crossing construction |
| -- | any safe-side / envelope-domination / prize-threshold claim | NOT CLAIMED | this is a lower-side coverage map only |

---

## 7. Replay

```bash
python3 experimental/scripts/verify_lower_reserve_unsafe_coverage.py
# -> RESULT: PASS (45 checks)   (~5 s, stdlib only)
```
