# The omega-sound emission floor: T3's cap is against the wrong measure, the fix is one identity, and compiler soundness discharges

## Status

```text
Status: COUNTEREXAMPLE (S1) + PROVED (S2, the fix): band-uniform T3's
        floor 2^s |hcube_v(D)| <= sum_eps |h(sigma_eps)| is sound against
        the cube |h|-ell^1 exactly as stated -- but the grammar's charge
        is omega = h_+ (#716 Sec 6 dialect: a semantic piece may charge
        up to sum_{S in U_i} omega(S)).  Against sum_eps h_+ the floor
        OVERPAYS on 263 of 558 hierarchy (piece, class) pairs at B = 6:
        128 sign-mixed classes overpaid, plus 135 of the 137 ZERO-charge
        (all-negative) classes paid positively (the other 2 pay zero;
        witness (k, r, v) = (3, 12, 011110), all 16 h-values negative).
        The omega-sound cap is ONE exact identity away:
            sum_eps h_+ = ( sum_eps |h| + 2^s hcube_v(empty) ) / 2 ,
        i.e. cap = (T3's budget + the signed flat coefficient)/2 --
        closed-form from quantities the rank-one packets already
        compute, and G-table-computable on hierarchy pieces.
      + PROVED (S3, safety): on single-sign NONNEGATIVE (flat) classes
        the T3 floor is already omega-sound (|h| = h there, so floor ==
        cap); single-sign NEGATIVE classes are exactly the zero-charge
        overpay cases above, and the corrected rule pays them zero.  All
        previously-used territory is single-sign nonnegative: depth-1
        symmetric pieces (31/31 classes positive), subgroup unions, and
        the maximal band's positive levels.  The #791 flat-cube
        reduction consumed the floor ONLY there: it is untouched.
      + PROVED (S4, soundness discharged): the corrected rank-one rule
        -- pay min(2^s |hcube_v(D*)|, sum_eps h_+), one pattern per
        class (#818 E3's cap), pieces disjoint (the decomposition
        definition) -- never overpays omega, per class, per piece, and
        globally (payments sum to at most Omega_+ by disjointness).
        The admission decision's compiler-level soundness obligation
        (band-uniform Nonclaims; fold-charge Sec 5) is DISCHARGED as
        arithmetic: 0 violations.
      + COMPUTED (S5, full adequacy): on EVERY charged hierarchy
        (piece, class) pair at B = 6 the argmax payment already reaches
        the positive charge (2^s |hcube(D*)| >= sum_eps h_+, 421/421),
        so the corrected rule pays hierarchy pieces IN FULL -- no
        efficiency loss anywhere at the verified scale.  A general-B
        proof of best >= cap is open.
LANE: hard input 2 ("image-scale MI + MA, or a direct Sidon payment",
        agents.md L51) -- eighth packet of the arc (forcing -> typing ->
        reduction -> scope -> compression -> classification -> admission
        arithmetic -> ADMISSION SOUNDNESS): with the floor corrected,
        rank-one emission carries NO remaining soundness obligation, and
        at B = 6 no adequacy loss either.  The admission decision on
        hierarchy pieces is now a pure grammar-acceptance question
        (soundness universally; adequacy at the verified scale).
        Input-2 residual: that
        acceptance, genuinely non-hierarchy bands, atlas totality (the
        Codex team's lane), large-q Sidon.  Fence (N1)
        (thm:aperiodic-one-ray-saturation) respected: nothing here pays
        or claims lower reserve.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.  The identity, the
safety statements, and the discharge are proved; the violation counts and
full-adequacy are `B = 6` COMPUTED facts.  Verifier:
`experimental/scripts/verify_omega_sound_emission_floor.py` (stdlib only,
deterministic, `RESULT: PASS (12/12)`, `--tamper-selftest` catches `5/5`,
~0.2 s).  Machine-readable certificate:
`experimental/data/certificates/omega-sound-emission-floor/omega_sound_emission_floor.json`.
Lean statement stub (decidable `native_decide` identities, no `sorry`, no
mathlib): `experimental/lean/omega_sound_emission_floor/` (`lake build`
succeeds).  No `.tex`/`.pdf` is edited.

## Interfaces

Paper labels (`experimental/rs_mca_thresholds.tex`, base commit `02728b2`;
read, none edited): **`prop:partial-occupancy-fourier` (PO3/PO4)**;
**`thm:aperiodic-one-ray-saturation` (SAT1)**: fence (N1).

Consumed packets on their OWN BRANCHES -- **the twisted-coset packet
(#816) and the emission-arithmetic packet (#818)** (OPEN PRs, NOT yet
integrated at base `02728b2`): the rank-one product law, G-tables,
budgets, and argmax schedule are their content; every fact used here is
RE-DERIVED and RE-VERIFIED self-containedly (this verifier rebuilds
hatf, the cube data, and the G-tables from scratch), so nothing depends
on integration order.

Integrated in-tree packets (consumed and credited, not reproved):
- **The band-uniform packet** (#795, `band_uniform_cube_reduction.md`):
  T3 is the object under audit.  Its floor statement is TRUE as written
  (against the cube ell^1); what S1 shows is that the COMPILER-relevant
  measure is omega = h_+, and against that the floor needs the S2 cap.
  Its Nonclaims line ("the compiler-level soundness obligation ... is
  part of the admission decision itself") is exactly the obligation S4
  discharges.
- **The fold-charge packet** (#791, `fold_charge_localization.md`): its
  Sec-0 grammar dialect (signed CS-P vs semantic ell^1-via-emission) and
  Sec-5 reduction are consumed; S3 proves the reduction is untouched
  (its construction pays only single-sign territory, where floor == cap).
- **The transverse-charge packet** (#776): omega, Omega_+, and the
  decomposition-piece formalism (its Sec 0) are the accounting frame.
- **avdeevvadim's #716 Sec 6**: the charge-condition split this packet's
  soundness notion lives in.
- **Codex team's atlas-totality lane** (in progress, theirs): unchanged.

---

## 0. Setup

Chart, classes, signatures, `wtil`, `s3`, `G_{k,r}(l)`, symmetric depth-k
pieces, budgets, and the argmax pattern `D*` as in #816/#818 (OPEN PRs --
self-contained here per Interfaces); `omega(S) = h(Phi(S))_+ / ||h||_2`
and pieces/charges as in the transverse-charge packet Sec 0.  Throughout,
per-class quantities are in unnormalized `h`-units on signature
representatives (the fiber multiplicity `w_s` and `1/||h||_2` scale both
sides of every comparison identically).

---

## 1. S1 + S2: the catch and the one-identity fix

> **S1 (counterexample).**  T3's floor is not omega-sound: at `B = 6`,
> over all symmetric hierarchy pieces (`k in {1,2,3}`, all `r`-pairs) and
> all classes, `2^s |hcube_v(D*)| > sum_eps h_+(sigma_eps)` on 263 of the
> 558 (piece, class) pairs.  The breakdown is mechanistic: 128 are
> SIGN-MIXED classes (the cosine character takes both signs; `|h|`-mass
> exceeds `h_+`-mass), and 135 are single-sign NEGATIVE classes -- 137
> pairs carry zero charge, and on 135 of them the floor pays positively
> (the other 2 have zero argmax too).  Witness: the piece
> `{xi == +-12 mod 27}`, class `v = 011110` -- every `h(sigma_eps) < 0`,
> `sum h_+ = 0`, argmax payment `0.979 > 0`.
>
> **S2 (the omega-sound cap).**  For every band and class,
> ```text
> sum_eps h_+(sigma_eps) = ( sum_eps |h(sigma_eps)| + 2^s hcube_v(empty) ) / 2 ,
> ```
> since `h_+ = (|h| + h)/2` pointwise and `sum_eps h = 2^s hcube_v(empty)`
> by definition of the mean coefficient.  On hierarchy pieces the cap is
> G-table-computable: `h = 2 G(s_low) cos(phi_tau)` (Lemma R of #818), so
> `sum_eps h_+ = 2^{s_low + 1} |G| sum_{tau : sign(G) cos(phi_tau) > 0}
> |cos(phi_tau)|` -- an `O(2^k)` explicit sum.

**Proof of S2.**  The two displayed identities; nothing else. `square`

Verified: the identity to `8.9e-16` and the G-form to `2.0e-13` over ALL
558 pairs; the violation counts and the witness exactly (deterministic
integer counts).

**Reading.**  T3 is not WRONG -- its statement and proof are about the
cube `ell^1`, and both survive.  The catch is at the compiler interface:
the grammar's semantic pieces charge `omega = h_+`, and the floor
overpays through TWO mechanisms -- on sign-mixed classes `|h|`-mass
strictly exceeds `h_+`-mass, and on all-negative classes there is no
charge at all yet `|hcube|` is positive.  Both mechanisms live on
twisted territory (the cosine character turns classes negative or
mixed), which is why the discrepancy went unnoticed while the only
admitted primitive was flat-cube on single-sign-nonnegative territory.

---

## 2. S3: all previously-used territory is safe

> **S3.**  On any class where `h` has a single sign (all
> `h(sigma_eps) >= 0` or all `<= 0`): if nonnegative, `sum |h| = sum h_+`
> and the floor equals the cap; if nonpositive, `sum h_+ = 0` and a rule
> crediting omega pays nothing.  Consequently depth-1 symmetric pieces,
> subgroup-cylinder unions, and the maximal band (where `h = wtil(s) -
> M/c` is class-constant; floor == cap exactly on the positive levels)
> are unaffected, and the #791 flat-cube reduction -- whose (=>)
> construction pays exactly the maximal band's positive levels -- is
> untouched by the correction.

**Proof.**  Pointwise `|h| = h` on nonnegative classes; class-constancy
on the named territories is #818 E4(a)/#816 C1/fold-charge Thm C(a).
`square`

Verified: worst single-sign overpay `1.4e-15`; depth-1 overpay exactly
`0`; the maximal-band closed form.

---

## 3. S4: compiler soundness discharges

> **S4.**  The CORRECTED rank-one rule -- against a decomposition into
> disjoint pieces, pay each (class, one certificate-named pattern `D*`)
> at `min(2^s |hcube_v(D*)|, sum_eps h_+)` -- is compiler-sound against
> omega: per class (the min), per piece (classes partition a
> fold-measurable piece's supports, and syndrome sets of distinct classes
> are disjoint), and globally (pieces are disjoint by the decomposition
> definition, so payments sum to at most `Omega_+`).  With #818's E3
> (one pattern per class necessary) and this cap, NO soundness
> obligation on rank-one emission remains open: the admission decision
> is purely whether the grammar ACCEPTS the rule.

**Proof.**  The three levels are the min, disjointness of class syndrome
sets (re-verified Lemma-N structure), and disjointness of pieces.  Units:
the payment is credited at the same `w_s/||h||_2` scaling as the charge
(Setup) -- `min(best, pos) <= pos` survives any positive common scaling,
and for a fold-measurable piece containing several classes the per-class
`w_s` factors differ but the capped payments still add to at most the
piece's charge `sum_{S in U_i} omega(S)` (class syndrome sets are
disjoint, so the piece charge is the sum of per-class charges).
Fence (N1) is untouched because omega-credited payments never claim
reserve. `square`

Verified: 0 violations over all pairs.

---

## 4. S5: at the verified scale, the corrected rule pays in full

> **S5 (COMPUTED).**  On every charged (piece, class) pair at `B = 6`
> (421 of 558), `2^s |hcube_v(D*)| >= sum_eps h_+`: the min in S4 is
> always the cap, and the corrected rule collects the class's ENTIRE
> positive charge.  Hierarchy pieces are paid in full -- the soundness
> correction costs nothing in adequacy at the verified scale.

A general-`B` proof of `2^s |hcube(D*)| >= sum h_+` on rank-one classes
is open (it would make full adequacy a theorem); the `B = 6` fact is
exhaustive, not sampled.

---

## Nonclaims

- **NOT a refutation of T3**: its statement (cap against the cube
  `ell^1`) and proof are correct; S1 corrects the COMPILER-facing
  reading only.  The band-uniform packet itself flagged this obligation
  as open -- S1/S4 close it, they do not contradict it.
- **NOT a proof of admission**: soundness and (verified-scale) adequacy
  are discharged, but no emission rule is added to the grammar; the
  acceptance itself remains the open decision.
- **S5 is a `B = 6` computed fact**; the counts (263/558, 135, 421/421)
  are exhaustive at `B = 6` over symmetric pieces at `k in {1,2,3}`.
- **Base 3 only**; single cosets and asymmetric profiles follow by the
  same identity but are not scanned here.
- Floats under exact Parseval + Lemma-N guards; the identity itself is
  exact arithmetic.
- **NOT a reserve payment**: fence (N1) respected.

## Consumers

- **The admission decision (#791 Sec 5, #716 Sec 7.1, #818 Sec 6)**: the
  soundness obligation named in band-uniform's Nonclaims is DISCHARGED;
  the decision is now pure grammar acceptance, with the corrected floor
  `min(2^s |hcube(D*)|, (budget + 2^s hcube(empty))/2)` as the rule's
  payment line.
- **The band-uniform packet (#795)**: T3 gains its compiler-facing
  corollary; its named-pattern schedule should quote the S2 cap.
- **The emission-arithmetic packet (#818)**: its budgets/argmax feed the
  corrected rule unchanged; its E4 shares are unaffected (shares compare
  coefficients, not omega).
- `rs_mca_thresholds.tex`: paste-ready remark after the PO4 material --
  "emission payments must be capped by the positive part, not the
  ell^1: sum h_+ = (sum|h| + 2^s * flat coefficient)/2, closed-form on
  hierarchy pieces; with that cap rank-one emission is compiler-sound,
  and at the verified scales it pays hierarchy pieces in full" --
  visible hypotheses: #749-corrected class, base-3 chart, q=2 rooting.

## Reproducibility

```bash
python3 experimental/scripts/verify_omega_sound_emission_floor.py
# -> RESULT: PASS (12/12)
python3 experimental/scripts/verify_omega_sound_emission_floor.py --tamper-selftest
# -> tamper-selftest: caught 5/5
python3 experimental/scripts/verify_omega_sound_emission_floor.py --emit-certificate \
  experimental/data/certificates/omega-sound-emission-floor/omega_sound_emission_floor.json
cd experimental/lean/omega_sound_emission_floor && lake build
# -> Build completed successfully
```
