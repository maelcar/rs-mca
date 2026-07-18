# M1 branch-2 weighted moment rank formalization

## Claim

Let `F` be a field, let `E` be a finite set of distinct elements of `F`, and
let `w : F → F` be nonzero on `E`.  For natural numbers `t,m` with
`|E| ≤ m`, define

\[
M_{a,b}=\sum_{x\in E}w(x)x^{a+b},
\qquad 0\le a<t,\quad 0\le b<m.
\]

Then

\[
\operatorname{rank}_F M=\min(t,|E|).
\]

The exact all-natural rank-drop consequence is

\[
\operatorname{rank}_F M<t\iff |E|<t.
\]

If `0 < t`, this is equivalent to the source's form

\[
\operatorname{rank}_F M<t\iff |E|\le t-1.
\]

## Status

PROVED.

## Source audit and explicit repair

This formalizes the factorization and rank identity in
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at source snapshot
`168e9ba0` and its
certificate directory
`experimental/data/certificates/m1-kb-branch2-rank-deep-owner-v1/`.
The source proof architecture is due to Scott Hughes.

The rank identity preserves the stated hypotheses.  The printed
natural-number corollary was under-specified at one allowed endpoint: for
`t = 0` and `E = ∅`, the left side `rank M < t` is false, while the right side
`|E| ≤ t - 1` is true because natural subtraction truncates.  The Lean module
does not silently strengthen the rank theorem.  It proves the all-`t` form
`|E| < t`, an equivalent all-`t` conjunction
`0 < t ∧ |E| ≤ t - 1`, and the source's `≤ t - 1` corollary under the
explicit hypothesis `0 < t`.  The deployed source has `t = 67,472`.

The source application has `m = j + 1` and `|E| ≤ j`; the formalized theorem
uses only the weaker hypothesis `|E| ≤ m` formalized for this kernel.  No
finiteness assumption on the ambient field is needed.

## Factorization

For

\[
V_r(E)_{x,a}=x^a,
\]

Lean proves the entrywise identity

\[
M=V_t(E)^{\mathsf T}\operatorname{diag}(w|_E)V_m(E).
\]

The condition `|E| ≤ m` makes `V_m(E)` surjective, nonzero weights make the
diagonal map surjective, and the rectangular Vandermonde rank is
`min(|E|,t)`.  Surjectivity of the two right factors leaves the rank of
`V_t(E)ᵀ`, giving the claim.

## Lean correspondence

The declarations are in
`experimental/lean/powersum_rigidity/PowersumRigidity/WeightedMomentRank.lean`:

- `weightedMomentMatrix_factorization`;
- `weightedMomentMatrix_rank`;
- `weightedMomentMatrix_rank_lt_iff_card_lt`;
- `weightedMomentMatrix_rank_lt_iff_pos_and_card_le_sub_one`;
- `weightedMomentMatrix_rank_lt_iff_card_le_sub_one`.

The package-level theorem map is in
`experimental/lean/powersum_rigidity/README.md`.

Validation command:

```bash
cd experimental/lean/powersum_rigidity
lake build
```

Validation completed from a clean package state.  The package-wide `lake build`
passed.  Printing axioms for the factorization, rank theorem, and all three
rank-drop corollaries reports exactly `propext`, `Classical.choice`, and
`Quot.sound`.  A scan of the changed Lean source finds no `sorry`, `admit`, new
`axiom`, or `sorryAx` declaration.

## Scope and nonclaims

This theorem is only the standalone weighted moment-matrix rank identity.  It
consumes an already supplied distinct support and nonzero weights.  It neither
extracts those data from a Route-D/RIM packet nor identifies
`rim_rank_drop_pivot` with the ambient MCA Hankel rank-drop branch.  It proves
no bad-incidence, first-match, deep-MCA owner, support-count, or Route-D payment
statement.  In particular, it does not construct the missing Route-D
RIM-to-owner adapter and does not close the KoalaBear row.
