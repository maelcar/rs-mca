# Complete profile-envelope comparison with the target: a completeness ledger

**Lane.** Hard input **4** of `agents.md` (L49): *"complete profile-envelope
comparison with the target"* --- and submission-strategy item 5 (L63--64),
*"compare the complete profile envelope, not only the identity prefix term,
against the actual target and lower reserve."* The maintainer requests
adversarial proof audits of the five hard inputs; this packet closes the
*assembly* (the input-4-unique wrapper) and pins the single residual, showing it
is **not an independent open object** but exactly inputs 2 and 3.

**Target file:** `experimental/asymptotic_rs_mca_frontiers.tex` (base commit
`36de5bf`). **No `.tex`/`.pdf` edited.**
**Verifier:** `experimental/scripts/verify_profile_envelope_completeness.py`
(stdlib-only, zero-arg, exact `Fraction`/bigint, `RESULT: PASS (2366 checks)`,
~0.1 s under `ulimit -v 2097152`). Byte-verifies all 18 quoted anchors
(negative-tested: a corrupted pin line fails), and recomputes every exponent,
band edge, sum=max gap, add-back inequality, and deployed bracket.

**Verdict.** The complete comparison factors as
```
  input 4  =  (PROVED wrapper)  o  (per-cell upper payment)
           =  [ envelope-exponent = max over classes ; identity-dominance band ;
               exact add-back AB1-AB3 ; target/finite bracket ]                      <- proved / in-tree
           o  [ uniform Sidon/(A4)/(FI) upper on the primitive residual  +  (RC) ]    <- = inputs 2 and 3
```
The LOWER (failure) direction of every class is **unconditional** (QR6
pigeonhole). The UPPER (domination) direction of every non-trivial class couples
**only** to input 2 (Sidon/`(A4)`/`(FI)`) or input 3 (`(RC)`). Therefore input 4
has **no independent open analytic core**: once inputs 2 and 3 are supplied, the
comparison with the target closes through the proved wrapper. The one named
statement that would complete input 4 on its own terms is `(PEU)` in section 4.

**Boundaries respected.** scottdhughes `(MI)`/`(MA)`/entropy-inverse
(#498/#501/#505) consumed as input, never attacked. `(FI)`/RC per-cell inputs
(#528/#530/#534/#535/#536, #635) consumed. Danny #529/#631, latifkasuli #518,
Codex Lean envelope definitions (#517) untouched. This is a research/audit
packet, not a formalization or a tex edit.

**Credit / differentiation.**
- **`envelope_identity_window.md`** (Holm Buar / holmbuar, PR #542) proves the
  identity-dominance *window* criterion `(DOM)` and its wall for the single
  cheapest field-drop quotient. **This packet consumes that criterion** and
  extends it to the *complete class inventory* (Chebyshev, planted, remainder,
  partial-occupancy, balanced-core), the multi-scale sum=max reduction, and the
  exact add-back, then states the target-side factorization above.
- **`profile_envelope_vs_target.md` / `.json`** (LegaSage #520) pins the envelope
  *formula* `E=1+(n-a+1)+sum(1+barN)` and four deployed adjacent-row brackets at
  *statement* level; its explicit nonclaims are *"does not prove closed ledger or
  e^{o(n)} domination."* **This packet supplies exactly the domination
  factorization it disclaims**, and re-derives its finite bracket as SB1--SB4.
- **`fi_full_image_primitive.md`** (#528/#534/#535/#536) settles payment at
  *effective-image* scale and characterizes the `(FI)` converter to *ambient*
  scale; **`c7_collapse_image_degree.md`** (#635/#634/#631) settles the last
  effective-image-collapse cell. These are the per-cell upper inputs this packet
  *routes to* (input 2), not re-proves.
- **`profile_envelope_numerics_audit.md`** dual-route-checks the collision-aware
  lower at the four rows; **`asymptotic_profile_envelope_audit.md`** (#524)
  reproduces the obstruction at `GF(11^2..23^2)`. Both are consumed as the
  lower/finite evidence base.

---

## 1. The objects (verbatim, gated by `file:line`)

### 1.1 The complete profile envelope (`eq:profile-envelope`, L858--862)

For a received line `(r0,r1)` and agreement `a`, with `Lambda(r0,r1;a)` the
realized profiles whose first-match cells are nonempty (L849--851), and with
`A_lam=|B_lam|^{R_lam}`, `L_lam=|Phi_lam(Omega^0_lam)|`,
`barN_lam=|Omega^0_lam|/L_lam` (L852--856):
```
   E_n(a) = 1 + (n - a + 1) + sup_{(r0,r1)} sum_{lam in Lambda(r0,r1;a)} (1 + barN_lam).   (1.6)
```
`barN_lam` is *"the average full-slice fiber size at the realized image scale"*
(L865--866). The sum *"includes the identity profile and all quotient,
Chebyshev, planted, and remainder profiles that meet that line; the supremum
makes the envelope a row-level quantity"* (L867--869), and *"with subexponentially
many profiles, the sum and maximum have the same exponential scale"* (L869--870).
Ambient scale `barN^amb=|Omega^0|/A` may replace `barN_lam` *only* after the
full-image certificate `L_lam >= e^{-o(n)}A_lam` `(FI)` (L874--876).

### 1.2 The target (`eq:target-entropy` L6108--6112; `lem:safe-side` L6154;
`eq:exact-safe-budget` L6159; `eq:exact-unsafe-budget` L6194)

The target is the cryptographic bad-slope ceiling `B*_n = floor(eps*_n |Gamma_n|)`
(L6115--6116), with ledger overhead `ell_n=o(n)` bits so the certified numerator
is `2^{ell_n} E_n` (L6116--6118). Agreement `a` is *safe* if
`B^{MCA}_{C_n,Gamma_n}(a) <= B*_n` and *unsafe* otherwise (L6118--6119).
The **safe side** (`lem:safe-side`, `eq:exact-safe-budget`, L6154--6160):
```
   2^{ell_n} E_n(a_n) <= B*_n     =>   a_n is safe.                                  (13.2)
```
The **unsafe side** (`eq:exact-unsafe-budget`, L6188--6195): a collision-aware
pole-line list of size `L_n` makes `a_n` unsafe when the printed
outer-ceiling exceeds `B*_n` (13.3). The identity scale is
`barN_1 = C(n,a)|B|^{-w}`, `w=a-k-1`, with
`(1/n) log2 barN_1 = H2(rho+g) - beta*g + o(1)` (`def:integer-staircase-detail`
L6667--6669; `eq:target-entropy`). Write `h := H2(rho+g)`, `s := g*beta`, so the
**identity exponent** is `e1 = h - s`.

### 1.3 The dominance premise the whole threshold theory assumes

`barN_1` *"is a safe numerator budget **only after the full profile envelope has
been proved to be** `e^{o(n)} barN_1`"* (`def:integer-staircase-detail`
L6670--6672). `prop:entropy-crossing-detail` (L6675--6685) opens *"Assume the
full profile envelope is `e^{o(n)} barN_1` in a window."* `cor:frontier-final`
(L6913--6922) reduces the frontier to the zero of `H2(rho+g)-beta*g` *"only in
the stated identity-dominant, subexponential-target regime."* The finite-scope
statement `thm:unconditional-support-envelope-bracket` (SB1--SB4, L6211--6240)
uses the **trivial** support upper `U(a)=min{|Gamma|, C(n,a)}`, not `E_n` ---
these are the exact rows; the *asymptotic* comparison is where `E_n` enters.

**Hard input 4 is precisely: prove (or bound the failure of) `E_n(a) <=
e^{o(n)} barN_1(a)` in the target window, over the full profile sum.**

---

## 2. The competitor exponents (`COMPUTED`, exact)

The engine is `prop:identity-quotient-comparison` (QR6--QR9, L3884--3948). QR6
(`eq:qr-natural-scale`, L3887--3889) is a **proved pigeonhole lower bound**
```
   barN_{c,r}(w) = C(N-|phi(R)|, m) |B_phi|^{-floor(w/c)},   N=n/c, m=(a-r)/c,
```
and QR8 (`eq:qr-comparison-general`, L3911--3916) gives the per-`n` exponent of
the depth-`c`, remainder-`r`, field-drop-`lambda_c` quotient profile:
```
   (1/n) log2 barN_{c,r}(w) = (1/c)(h - s) + (s/c)(1 - lambda_c) + o(1)
                            = (1/c)(h - lambda_c * s) =: e_c,   lambda_c = log|B_c|/log|B| in (0,1].
```
Verifier **Section A** confirms the two forms are equal as exact `Fraction`s over
a grid, that `e_c` is decreasing in `c` and in `lambda`, and the countertheorem
crossing: `s=h, c=2, lambda=1/2 => e_2 = h/4`, byte-matching
`thm:smooth-quotient-obstruction`'s exponent `(1/4)h(alpha)` (L4016--4018).

**Class inventory (the *complete* competitor set of (1.6)).**

| class | exponent | lower dir | upper dir | couples to |
|---|---|---|---|---|
| identity | `e1 = h - s` | `PROVED` | `PROVED` | self |
| power-quotient `(c)` | `e_c=(1/c)(h-lambda_c s)` | `PROVED` (QR6) | `CONDITIONAL` | input 2: `(A4)`/`(FI)` |
| Chebyshev `(c)` | `= e_c` (`T_c` lift) | `PROVED` (QR6) | `CONDITIONAL` | input 2: `(A4)`/`(FI)` |
| planted | `x 2^b`, `b<=2`: `e^{o(n)}` | `PROVED` | `PROVED` | exact |
| remainder | `w>=r` exact; `w<r` prefix `x e^{o(n)}` | `PROVED` | `CONDITIONAL` | input 2: `(A4)` |
| partial-occupancy | add-back AB1--AB3 | `PROVED` | `CONDITIONAL` | input 2: per-cell `U_lam` |
| balanced-core | ray bound | `PROVED` (lower) | `CONDITIONAL` | input 3: `(RC)` |

- **Chebyshev = power-quotient** by `rem:qr-chebyshev` (L3857--3871): after
  `phi -> b^{-1}phi` normalization *"the theorem therefore applies to the
  Chebyshev folding map `T_c` ... it gives the same statement verbatim"*; the
  fixed/ramified endpoints form an exceptional set of size `b` with *"crude total
  exceptional-point multiplier at most `2^b`, with `b<=2` for involution-fixed
  endpoints."*
- **Planted** multiplies a quotient term by `<= 2^b` (L3866--3867); for fixed or
  `o(n)` planted depth this is an `e^{o(n)}` perturbation, no new exponent
  (Section A5: `(b/n) -> 0`, monotone).
- **Remainder**: `w>=r` recovers the remainder exactly, `w<r<c` reduces to an
  ordinary remainder prefix problem times `e^{o(n)}` quotient choices (remark
  L3950--3960); unbounded `c=c_n -> infinity` costs only `2^{n/c}=e^{o(n)}`.
- **Balanced-core / partial-occupancy** are bounded *by* the envelope via `(RC)`
  (`hyp:ray-compiler`) and the add-back lemma (section 3), not new exponent
  terms.

**Reduction (envelope exponent).** On the exponential scale, because the `1` and
`n-a+1` terms are linear (exponent 0) and the profile sum is a sup over
`e^{o(n)}` profiles,
```
   (1/n) log2 E_n(a) = max( 0, e1, max_{(c,lambda)} e_c ) + o(1).
```
The exponential competitors are **exactly** the identity term and the field-drop
quotient/Chebyshev terms; planted/remainder are `e^{o(n)}` and
balanced-core/partial-occupancy are envelope-bounded. *(This reduction is the
content flagged for PI re-derivation in `envelope_identity_window.md` section 7;
this packet supplies the class-by-class citations and the exact add-back that
close it, modulo the per-cell upper payment.)*

---

## 3. The complete comparison, assembled (`PROVED` wrapper)

### 3.1 Multi-scale sum = max (`COMPUTED`, Section C)

The sum in (1.6) ranges over all folding scales `c | gcd(n,m)`, each Chebyshev
scale, and the remainder profiles. The number of divisors `d(n)` is
subexponential (`d(n) <= n`, `(log2 d(n))/n -> 0`, verified monotone), so
`2^{Mn} <= sum_c 2^{e_c n} <= d(n) 2^{Mn}` with `M = max_c e_c`, i.e. the per-`n`
log gap over the max is `<= (log2 d(n))/n -> 0`. Sum and max share one
exponential scale (matching L869--870). Exact integer check at `n in {24,48,120,240}`.

### 3.2 Identity-dominance band (`PROVED`, Section B; consumes #542)

With cheapest folding `(c,lambda)`, `lambda<1`, `(IDW)` `<=>` the predicate
`(DOM)` `e_c <= max(0, e1)` for every competitor, and `(DOM)` holds **iff**
```
   s <= kappa_low * h    (kappa_low  = (c-1)/(c-lambda) in (0,1]),   or
   s >= kappa_high * h   (kappa_high = 1/lambda in [1,inf)).
```
Verifier Section B checks `DOM == band` on a `(h,s,c,lambda)` grid and the
**wall**: the zero-target crossing `s=h` is *strictly inside* the failure band
`(kappa_low h, kappa_high h)` for every `lambda<1` and `c>=2` (so the corollary's
identity specialization is unavailable at the crossing); for `lambda=1` (prime
image field / no scaled-subfield folding) the band collapses to the point `s=h`
and dominance holds everywhere.

### 3.3 Exact profile add-back (`PROVED`, Section D)

`lem:exact-profile-addback` (AB1--AB3, L7260--7298): with per-`lambda` budgets
`U_lam <= kappa_lam(1 + |Omega_lam|/L_lam)`, image factor `eta_lam=A/L_lam`, and
multiplicity `mu = max_S #{lambda: S in Omega_lam}`,
```
   sum U_lam <= 2 sum kappa_lam |Omega_lam|/L_lam           (AB1)
             <= 2 kappa eta mu |Omega|/A                    (AB3, uniform).
```
Section D checks AB1=AB2<=AB3 on a concrete family and the **necessity of image
coverage** (remark L7310--7324): a bijection on an `M`-set partitioned into
singletons gives `LHS=2M`, inner-`RHS=2`, ratio `M -> infinity` --- so *"exact
support add-back alone is insufficient"*; the `eta,mu` factors are logically
required. This is the exact accounting that reduces *partial-occupancy
domination* to the per-cell budgets `U_lam <= kappa_lam barN_lam`.

### 3.4 Target comparison over all classes (`COMPUTED`, Section E)

Safe iff `2^{ell_n} exp( n * max(0,e1,max_c e_c) ) <= B*_n` (13.2). Two regimes,
both exact:
- **identity-dominant** (`lambda=1`): envelope exponent `= max(0,e1)`; comparison
  reduces to the one-variable identity crossing (`cor:intro-identity-frontier`).
- **quotient-dominant** (`c=2,lambda=1/2,s=h`, the `thm:smooth-quotient-obstruction`
  point): envelope exponent `= h/4 > 0 = e1`; `(IDW)` fails by exactly `h/4`,
  unconditionally (QR6). The comparison then needs the *quotient* term against
  the target, not the identity term.

The **finite** side is exact and unconditional: at the four deployed adjacent
rows, `thm:unconditional-support-envelope-bracket` gives `P(a0) > B* >= U(a1)`
with `a1=a0+1`, hence `a* = a1` (SB2 -> SB3/SB4). Section E recomputes the
bracket from the committed integers (LegaSage #520 / #524).

---

## 4. The residual, pinned as ONE named statement (`OPEN`, = inputs 2 + 3)

Everything above is the *proved* wrapper. The single remaining direction is the
per-cell **upper** payment, which the paper itself names at L1086--1092 as *"a
Sidon payment on the residual obtained after every quotient, subfield, planted,
and remainder profile has been removed, together with uniform profile-envelope
domination of the exact partial-occupancy terms and a higher-dimensional
transverse-secant bound."*

> **(PEU) Primitive-residual envelope upper.** For every ledger-admissible
> smooth/circle row and every realized primitive first-match residual profile
> `lambda` (after all named quotient/Chebyshev/planted/remainder profiles are
> removed), the first-match slope budget obeys
> `U_lam <= e^{o(n)} (1 + barN_lam)` at the profile's realized image scale,
> uniformly in the received line, where `barN_lam` is the effective-image scale
> unless `(FI)` `L_lam >= e^{-o(n)} A_lam` upgrades it to ambient.

Given `(PEU)`, section 3's add-back (AB3) and multi-scale sum (3.1) yield
`E_n(a) <= e^{o(n)}( 1 + (n-a) + sum_c barN_{c} )`, and the band criterion (3.2)
plus the target reserve (13.2) complete the comparison with `B*_n`. **`(PEU)` is
not new open content of input 4:** its Sidon/`(A4)` content is hard input 2
(scottdhughes `(MI)`/`(MA)`, `fi_full_image_primitive.md`, `c7_collapse_image_degree.md`),
and its balanced-core/transverse-secant content is hard input 3 (`(RC)`,
`residual ray compiler for higher-dimensional balanced cores`). Hence:

**Gap-analysis verdict.** *Input 4 = the proved wrapper (envelope-exponent =
max-over-classes; identity-dominance band + wall; exact add-back AB1--AB3;
target/finite bracket) composed with `(PEU)`, and `(PEU) = inputs 2 and 3`.
Input 4 has no residual open object independent of 2 and 3.* The sharpest honest
tex phrasing is therefore not *"complete profile-envelope comparison with the
target"* as a fifth independent unknown, but *"assemble the (proved) envelope
add-back and identity-dominance band against the target, conditional on the
primitive-residual payment (inputs 2, 3)."*

---

## 5. Proposed paper change (ledger entry; **no tex edited here**)

Suggested, not applied; integration-dependency flags noted.

> **Entry: profile-envelope completeness factorization (hard input 4).**
> **Source:** this packet (`profile_envelope_completeness.md`,
> `verify_profile_envelope_completeness.py`), consuming #542 (window criterion),
> #520/#524 (formula + finite bracket), #528/#535/#536/#635 (per-cell upper).
> **Paper impact (suggested):**
> 1. After `def:integer-staircase-detail` (L6673) add a remark: the full
>    profile envelope's exponent is `max(0, e1, max_c e_c)` with competitors
>    exactly the identity and field-drop quotient/Chebyshev terms
>    (`prop:identity-quotient-comparison`, `rem:qr-chebyshev`), planted/remainder
>    being `e^{o(n)}` and partial-occupancy/balanced-core bounded by
>    `lem:exact-profile-addback`/`(RC)`.
> 2. Re-scope input 4 in `agents.md`/summary from an independent hard input to
>    *"the (proved) add-back + identity-dominance-band assembly, conditional on
>    the primitive-residual payment `(PEU) = inputs 2, 3`."*
> **Nonclaims.** Does not prove `(PEU)`/`(A4)` (inputs 2, 3); does not close the
> deployed finite rows beyond the committed adjacent bracket; the multi-scale and
> add-back checks are structural, not a deployed-scale numeric certificate.
> **Integration dependency.** Item 1's remark should land after inputs 2/3'
> payment lemmas are promoted, so `(PEU)` is a citation rather than a hypothesis.

---

## 6. Per-claim label ledger

| # | Claim | Status |
|---|-------|--------|
| C1 | 18 tex anchors byte-verify at pinned lines; corrupted pin fails (negative-tested) | `AUDIT` (verifier Section P) |
| C2 | `e_c=(1/c)(h-lambda s)` equals QR8 two-term form; `=h/4` at the CE crossing | `PROVED` (algebra; Section A) |
| C3 | Chebyshev `(c)` exponent `= power-quotient (c)` (`T_c` lift, `rem:qr-chebyshev`) | `AUDIT` (citation; Section A) |
| C4 | Planted `x2^b` (`b<=2`) and unbounded `c` contribute `e^{o(n)}`, no new exponent | `PROVED` (Section A5) + `AUDIT` (citation) |
| C5 | Envelope exponent `= max(0, e1, max_c e_c)`; competitor set complete | `PROVED` reduction; upper dir `CONDITIONAL` on inputs 2/3 |
| C6 | Multi-scale sum `=` max: `2^{Mn} <= sum <= d(n)2^{Mn}`, `(log2 d)/n -> 0` | `COMPUTED` (Section C) |
| C7 | `(IDW) <=> (DOM)`; band `{s<=kappa_low h} U {s>=kappa_high h}`; wall at `s=h` | `PROVED` (Section B; consumes #542) |
| C8 | Add-back AB1<=AB2<=AB3 exact; image coverage necessary (`2M` vs `2`) | `PROVED` (Section D) |
| C9 | Complete target comparison: `lambda=1` identity-dominant; CE point excess `h/4` | `COMPUTED` (Section E) |
| C10 | Finite bracket `P(a0)>B*>=U(a1)`, `a*=a1` at 4 deployed rows | `COMPUTED` (Section E; committed integers) |
| C11 | `(PEU)` completes input 4 and `(PEU) = inputs 2, 3`; no independent open core | `OPEN` (pinned statement) / `AUDIT` (factorization) |

---

## 7. Flagged for PI re-derivation

1. **Reduction completeness (C5).** That the exponential competitors are exactly
   identity + field-drop quotient/Chebyshev rests on the class citations
   (L3866--3867 planted, L3950--3960 remainder, `(RC)`/add-back for
   balanced-core/partial-occupancy). Re-check at statement level; the *failure*
   side (C2/C7) is unconditional and does not depend on it.
2. **`(PEU) = inputs 2, 3` (C11).** Confirm the primitive-residual upper payment
   carries no content beyond `(A4)`/`(FI)` (input 2) and `(RC)` (input 3); if a
   genuinely new transverse-secant obstruction exists at higher balanced-core
   dimension, it belongs to input 3, not input 4.

**Recommended next lane.** *Lower reserve / unsafe-side comparison* (hard input
5): the same field-drop quotient list feeds `prop:simple-pole-lower`'s `P(a)` on
the *unsafe* side, so a mirror "quotient-list reserve" criterion would pair with
this envelope side to close both brackets of
`thm:unconditional-support-envelope-bracket`.
