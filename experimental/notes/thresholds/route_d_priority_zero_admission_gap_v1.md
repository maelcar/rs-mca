# Route-D priority-zero admission gap v1

STATUS: COUNTEREXAMPLE

## Result

The checked CAP25-v13 KoalaBear row-sharp-Q Route-D artifacts do not define an
executable residual after the eight named priority-zero deletions.  The names
occur only in an `examples` list under one aggregate item.  That item contains
no typed projectors, predicates, relative precedence, disjointness theorem,
owner-recovery maps, marked residual, or checked correspondence with the older
ten-branch first-match order.

Thus “after the exact named first-match deletions” does not currently denote a
machine-defined support set.  This is a counterexample to schema executability,
not a primitive target above

```text
67472*2130706433 = 143763024447376.
```

The deployed support certificate remains open rather than false.

## Exact schema audit

The singleton certificate's complete priority-zero object is

```json
{
  "priority": 0,
  "name": "earlier_global_first_match_branches",
  "examples": [
    "generated_field",
    "quotient_planted",
    "sparse_pade_hankel",
    "m1_window_shadow",
    "rank_drop_pivot",
    "bc_chart",
    "sp_shift_pair",
    "extension_slope"
  ]
}
```

Its key set is exactly `examples, name, priority`.  The rest of the singleton
layer is

```text
0 earlier_global_first_match_branches
1 strict_distance_child(B,C)
2 construct canonical packet Pi(B,C)
3 repeated_side_pair_reuse / planted_switch_core_fiber
4 cross_pair_multiplicity_aware_sp_pade
5 residual_route_d_cell_charge.
```

This layer assumes priority zero has already produced unpaid branch-excess
units `(B,C)`; it does not construct them from the original marked supports.
The exact identifier `D_prim` occurs zero times in the pinned source artifacts.
`G_gen_support(z)` and `D_full_rank_prim(z)` occur as prose/JSON target strings,
not constructed sets.

The older ledger separately prints

```text
1 contained or noncontained failure
2 rank-drop or pivot failure
3 tangent / common-line / residue-line
4 quotient-periodic or divisor-stabilized
5 planted / prefix-structured
6 extension-valued slope
7 base generated-field collision
8 sparse sigma or sparse-support
9 M1 half-turn / coefficient-shadow
10 primitive Q-fin residual.
```

There is no checked relative order among the eight examples and no checked map
to this ten-owner order.  The semantic gaps are material:

- `generated_field` resembles old branch 7, whose printed charge is image-only;
- `quotient_planted` merges old branches 4 and 5;
- `rank_drop_pivot` resembles old branch 2 but is moved inside the aggregate;
- `m1_window_shadow` resembles old branch 9;
- the new `extension_slope` predicate `mu_(r+1)=0` is not the old
  extension-valued slope in `F_(p^6) minus F_p`;
- `bc_chart` and `sp_shift_pair` are new names;
- old branches 1 and 3 are omitted, while old branch 10 is the terminal
  residual rather than a deletion.

A generic first-match add-back formalization exists, but no Route-D instance
supplies these projectors.  The later M1 atlas manifest also fails closed: its
deployed family records zero represented rows, all `67472` missing, an
unproved adapter, and excludes raw supports from its owner unit.  That capacity
record is not a genuine support residual.

## Typed owner audit

| object | printed unit and bound | missing support interface |
| --- | --- | --- |
| generated collision | at most `t*p` image cells | a cell may contain many supports; no raw-support fiber bound is printed |
| `DEEP_MCA_RANK_DROP` | at most `t` distinct slopes for one fixed received pair, globally once | no injection from marked supports into `Z_rankdrop(f,g) x F_p` |
| Rule 1 planted switch | exact descent | the cost `|G_(beta,A)|-1` has no accepted planted/core ledger |
| Rule 2 weighted SP/Padé | exact recovery and support cost one | no finite `B_WSP_full` or bound for `N_WSP_full(z)` |
| strict-distance child | algebraic predicate | no typed payment theorem |
| residual row cell | conditional one-cell charge | `|R_D|<=t` is a hypothesis and the actual survivor set is undefined |

The actual-incidence all-maximal-minors theorem gives a valid eligibility
route: on an actual marked incidence, all maximal minors vanish exactly when
the field-native matrix has rank below `t`.  It does not turn a distinct-slope
owner into a per-support owner.  The literal common core `G` must remain carried
through any support-fiber map.  Likewise, cost-one Rule-2 recovery proves
losslessness, not a finite sum.

## Exact arithmetic and slack

For `p=2130706433` and `t=67472`, the verifier checks

```text
t*p                         = 143763024447376
t*(p-1)                     = 143763024379904
1+t*(p-1)                   = 143763024379905
t*p-(1+t*(p-1))             = 67471
retained exact-lift         = 11440
t*p+11440                   = 143763024458816
target floor                = 274836936291722953
conditional integer slack   = 274693173267264137.
```

The arithmetic implication

```text
unpaid leaves <= 1+|R_D|*(p-1) <= 1+t*(p-1) <= t*p
```

is correct once the typed compiler and row budget are proved.  The final slack
is not a first-match owner and cannot absorb an undefined residual.  A larger
allowance would require a complete revised ledger with every competing charge
printed and no double use.

## Sibling-SHA consequences

The following sibling shipments sharpen, but do not repair, admission:

- commit `36d560d7421dace47bf48b3fecc9389adaf0977b`, note blob
  `b11def86906c467fc5a1b07caf14a07108b430f6`, proves Rule-2 recovery but no
  numerical payment;
- commit `91a9e31284adb34a1dfe5c71e434aa709ba2d3fe`, note blob
  `97f6b77a877e7c7d8efdf4661ccf84856bd5d0fc`, refutes
  `raw marked support packet = branch-excess unit`;
- commit `332153d6e74403e3ad20f367ff4a3df8406a30bf`, note blob
  `6ce5a571ca05f774a6569a9c78d9cb69e8fc896a`, finds canonical-core contact in
  every comparison occurrence and no vanishing owner-eligible pivot;
- commit `909f0c4e1a884f362576b19d4a379656ba3843a1`, note blob
  `ce926bbdcc96e1168f9440f02ba8f2cfba95dcf6`, refutes promotion of the raw
  fixed-base `>=81` floor through a disjoint all-depth tree and has toy
  `|R_D|=4>3`;
- commit `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`, note blob
  `f24ce928df7e7170c1b4f3228d5fe9b184be50b4`, supplies the all-minors rank
  adapter only after actual incidence exists;
- commit `5343c5876e559e33b6d3bb332cb2d55edbfbcc4b`, note blob
  `7f8f2042c5fe0f5eb45f36f626ee47e4967e95c9`, supplies marked puncture
  recursion but no executable first-match predicate or deletion heredity.

All six have parent `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.
They are consumed as immutable sibling statements, not a merged history.

## Theorem A: executable priority-zero admission

**Theorem A.** For every primitive target `z`, construct a finite marked
universe `X_z`, eight typed predicates in a declared precedence order, and

```text
tag_z : X_z ->
  {generated, quotient, sparse, m1, rank, bc, sp, extension, survivor}.
```

Prove exhaustive disjoint classification, owner-typed recovery, literal `G`
preservation, actual-incidence data for a rank tag, and construction of an
actual `(B,C)` and canonical `Pi(B,C)` for every survivor.  Raw support
multiplicity must not be identified with child multiplicity.

## Theorem B: marked residual compiler and payment

**Theorem B.** On Theorem A's literal survivor set:

1. strict-distance units enter a typed owner;
2. Rule-1 repeats enter a printed planted-core ledger;
3. all-minors-vanishing actual incidences enter the rank owner together with a
   marked support-fiber injection;
4. a full-rank Rule-2 defect meeting `G` satisfies an executable earlier
   deletion or enters a new marked-contact owner with printed cost;
5. remaining full-rank WSP packets have a finite bound or a `G`-preserving row-cell injection;
6. `|R_D|<=t`;
7. the unpaid-leaf set is literally `G_gen(z) disjoint_union D_prim(z)`.

Then

```text
|G_gen(z)|+|D_prim(z)|
  <= 1+|R_D|*(p-1)
  <= 1+t*(p-1)
  <= t*p.
```

Theorem A must precede further WSP enumeration: without admission, a raw
finite corpus cannot establish an official post-deletion floor.

## Exact provenance

The base snapshot is `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.

- Prefix reduction commit `e83962ae5ad7bacb391b691ffd37f0abef977b83`:
  note blob `591c91a6aac6b48db0c16abc586b74d7a51e44e2`, certificate blob
  `908ee64976b46b9d8b5bd6015dd8c031dc17df6f`.
- Singleton commit `84b393ec1bc52fa662756bd117a45537007d086a`:
  note blob `dda538a9a36cd0c8e267c11600a49cdc5bf054d1`, certificate blob
  `6a8aa0c61eeebfa93b97e157b3bc72f8c3dce892`.
- Frozen first-match ledger commit
  `0955594bf354b6a396574b65fbb242715edd3267`, note blob
  `63057656657bed1e9c7ab2e2e515164ccb039d5c`.
- Rank/deep owner note blob `ddfce00907f34128b324a64041f4e0ec8957b7d3`.
- Generic add-back commit `764f1c0243770baa437d4ae790b1448afa091680`,
  Lean blob `2da56854413d4f77eedab4ea9878f913991202b3`.
- M1 manifest commit `168e9ba0280e069a8bd552a6e2098bb9248c70b7`,
  deployed-family blob `77285eae5ffed831e1ae4849703c356103798304`.

The verifier hashes exact base artifacts, reads pinned sibling blobs from the
local Git object database, checks the singleton JSON, and runs fail-closed
mutations.

## Nonclaims

- No primitive deployed target above `143763024447376` is exhibited.
- No official residual or `N_WSP_full(z)` is constructed.
- No image cell, schema-capacity slot, or distinct slope is retyped as support.
- No raw packet is called a branch-excess unit.
- The common core is never discarded or replaced by an image-only label.
- No low-moment, Johnson-packing, mode-at-null, image-only, or zero-defect
  shortcut is used.

## Reproduction

```bash
python3 experimental/scripts/verify_route_d_priority_zero_admission_gap_v1.py
python3 -O experimental/scripts/verify_route_d_priority_zero_admission_gap_v1.py
python3 experimental/scripts/verify_route_d_priority_zero_admission_gap_v1.py --tamper
python3 -O experimental/scripts/verify_route_d_priority_zero_admission_gap_v1.py --tamper
(cd experimental/lean/route_d_priority_zero_admission_gap_v1 && lake build)
```

The verifier is deterministic and uses only the Python standard library plus
read-only access to the local Git object database.
