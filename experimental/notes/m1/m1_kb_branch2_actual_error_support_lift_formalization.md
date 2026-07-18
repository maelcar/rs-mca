# M1 branch-2 actual-error-support lift formalization

## Claim

Let `D` be a finite coordinate type over a field `F`, let `C` be a set of
words `D → F`, and put

\[
y_\gamma(x)=f_0(x)+\gamma f_1(x),\qquad
E_\gamma=\operatorname{supp}(y_\gamma-c).
\]

Suppose `c ∈ C` explains `y_γ` on a finite support `S`, the pair `(f₀,f₁)` is
not simultaneously explained on `S`, and `|E_γ| ≤ r`.  Then the full
agreement support

\[
S_\gamma^*=D\setminus E_\gamma
\]

contains `S`, has cardinality at least `|D| - r`, is explained by the same
codeword `c`, and remains pair-wise noncontained.  Consequently `γ` is
MCA-bad at agreement `|D| - r`.

For the source parameters `|S| = A`, `k + 1 ≤ A`, and `t = A - k`, an
actual-error cap `|E_γ| ≤ t - 1` yields MCA-badness at agreement
`|D| - t + 1`.

## Status

PROVED.

## Source audit and explicit repair

This formalizes only `Exact support and actual error support` and `Lift to the
deep agreement` in
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at source snapshot
`168e9ba0`, together with the corresponding deterministic certificate in
`experimental/data/certificates/m1-kb-branch2-rank-deep-owner-v1/`.  The source
proof architecture is due to Scott Hughes.

The source prints

\[
n-(t-1)=n-t+1.
\]

With natural-number subtraction this requires both `0 < t` and `t ≤ n`.
The first hypothesis is necessary already at `n = t = 0`; the second is
necessary at `n = 0`, `t = 1`.  The reusable core therefore remains at the
always-correct truncated endpoint `|D| - r`.  The source-facing wrapper does
not silently assume the endpoint identity: it derives `0 < t` from
`k + 1 ≤ A` and `t = A - k`, and derives `t ≤ |D|` from those hypotheses,
`S.card = A`, and `S ⊆ Finset.univ`.

The core statement needs no hypothesis `r ≤ |D|`; truncated subtraction makes
the conclusion valid for every natural `r`.

The source specializes to a finite field, an evaluation domain inside that
field, and a Reed--Solomon code.  None of field finiteness, coordinate-field
embedding, distinct evaluation points, linearity, or Reed--Solomon structure
is used by this support-only implication.  Lean therefore exposes the
smallest correct theorem for an arbitrary field, arbitrary finite coordinate
type, and arbitrary code set, while the source-facing wrapper preserves the
source's exact witness-cardinality hypotheses.

## Lean correspondence

The declarations are in
`experimental/lean/rs_mca_thresholds/RsMcaThresholds/ActualErrorSupportLift.lean`:

- `fullAgreementSupport` defines `S* = D \ E` using the existing
  `ExactSparsification.wordSupport`;
- `mem_fullAgreementSupport_iff` identifies membership with agreement by `c`;
- `fullAgreementSupport_card` proves `|S*| = |D| - |E|`;
- `fullAgreementSupport_witness` proves original-support inclusion, the
  cardinality lower bound, explanation by the same codeword, and upward
  persistence of noncontainment;
- `mcaBad_lift_of_wordSupport_card_le` packages those conclusions through the
  existing `GrandeFinale.MCABad` API;
- `nat_sub_pred_eq_sub_add_one` states the repaired natural-subtraction
  identity with both necessary hypotheses;
- `rankDepth_mcaBad_lift_of_wordSupport_card_le` derives those hypotheses from
  the source's exact-witness data and gives the repaired deep endpoint.

The module reuses `GrandeFinale.Explained`, `GrandeFinale.ExplainedPair`,
`GrandeFinale.MCABad`, and `RsMcaThresholds.ExactSparsification.wordSupport`
verbatim.  It introduces no replacement badness or support predicate.

## Producer and consumer interlocks

The source producer is PR #845.  The existing exact-sparsification API is PR
#781.  The standalone weighted-moment rank kernel in PR #912 is a logical
predecessor only after a separate application-specific matrix/support adapter
supplies the cap consumed here.  The formal deep-count consumer is PR #724;
the direct certificate consumer is PR #851, integrated by PR #864; and the
whole-packet predecessor consumer is PR #849.

## Validation

From `experimental/lean/rs_mca_thresholds`:

```bash
lake clean
lake exe cache get
lake build
lake env lean /tmp/PrintActualErrorSupportLift.lean
```

The clean package replay reports
`Build completed successfully (8093 jobs).`  The focused module build also
passed.  Printing
axioms for all six theorems reports only `propext`, `Classical.choice`, and
`Quot.sound` (the arithmetic identity uses only `propext` and `Quot.sound`).
The changed Lean source contains no `sorry`, `admit`, new `axiom`, or
`sorryAx` declaration.

The source certificate replay is:

```bash
python3 experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py --check
```

and reports `M1_KB_BRANCH2_RANK_DEEP_OWNER_V1_VERIFY_PASS`.

## Scope and nonclaims

This packet consumes an explicit explaining codeword and an already-proved
actual-error-support cap.  It does not prove the exact-support reduction,
derive equation (3) from a rank drop, identify PR #912's abstract weighted
moment matrix with the source matrix `M_A(γ)`, or turn raw rank drop into an
MCA-bad witness.  It constructs no RIM/Route-D/owner/payment adapter and proves
no pivot, tangent, or cyclotomic equivalence.  It proves no deep-MCA count,
global charge (including the deployed value `67472`), branch closure, or
KoalaBear row closure.
