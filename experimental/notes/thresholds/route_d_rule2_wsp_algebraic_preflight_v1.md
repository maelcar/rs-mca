# Route-D Rule-2 WSP algebraic preflight v1

STATUS: COUNTEREXAMPLE

## Result

This packet executes the algebraic part of the singleton-heavy top-seam
Rule-2 construction on the exact `F_31` fixture from shipment `#920`, exact commit `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`.  It
refutes the inference

```text
Rule-2 certificate shape + exact support cost one
  => numerical payment or a complete first-match deletion.
```

The construction is lossless and preserves the marked common core, but it
does not instantiate a numerical payment theorem.

The fixed primitive corpus has `119` packets in `28` nonzero cells.  One
representative per cell leaves `91` algebraic Rule-2 emissions.  With the
source-oriented boundary-pair order, lexicographic in the packet support
`T`, exactly `6` emissions satisfy the named reduced-weight extension
predicate and `85` are nonextension, Vandermonde-full, projectively primitive
algebraic WSP candidates.  Exhausting every representative choice proves the
order-invariant statement:

```text
every one-representative-per-cell choice emits 91 certificates;
at most 10 are extension certificates;
at least 81 are nonextension projectively primitive algebraic candidates.
```

This is a local pre-first-match candidate lower bound.  It is not a
ledger claim, because the fixture does not construct branch-excess units
`(B,C)`, canonical packets `Pi(B,C)`, the `P1` strict-distance decision, or
all prior global first-match filters.

## Exact fixture

Work over `F_31` on `D=F_31^*` with

```text
k=12, A=15, j=15, t=3, w=2,
E={1,2,3}, f=1_E, g(x)=x^12, gamma=0,
B={1,2,3,4,5,7,10,11,12,18,19,20,21,26,28},
z=Phi_2(B)=(30,9).
```

Enumerate

```text
T=(B\R) union A,
R subset B\E,
A subset D\B,
|R|=|A|=3,
Phi_2(T)=z.
```

The deterministic enumeration gives `121` mates.  For
`nu=1_A-1_R`, projective primitivity means that

```text
h*nu = +nu or h*nu = -nu
```

has only `(h,+)=(1,+)`.  Exactly `119` mates are projectively primitive.
The mark is always

```text
G=B\R,
B=G union R,
T=G union A.
```

## Source-oriented cell embedding

For each packet use the source-side orientation

```text
U=L_A,
U-c=L_R,
c=const(L_A)-const(L_R)=-nu_3/3 in F_31.
```

The verifier checks all three identities from the locators and moments.  The
Rule-1 key `(r,c,U,beta)` has no duplicate on the primitive corpus.  Grouping
by `(r,c)=(3,c)` gives `28` cells with size histogram

```text
{1:1, 2:4, 3:5, 4:8, 5:3, 6:4, 7:1, 8:1, 9:1}.
```

The `28` representatives fit the one-row nonzero-cell capacity `p-1=30`.
This is a cell-count check, not a payment for the other `91` packets.

## Rule-2 algebra

For a representative `(R_0,A_0)` and another packet `(R,A)` in the same
cell, put

```text
U_0=L_A0,       U_0-c=L_R0,
U=L_A,          U-c=L_R,
L_+=U_0*(U-c),
L_-=(U_0-c)*U.
```

Cancel `H=gcd(L_+,L_-)` and write `M_+=L_+/H`, `M_-=L_-/H`.  The reduced
signed weight is

```text
mu = 1_A0 + 1_R - 1_R0 - 1_A.
```

For every emitted certificate the verifier independently checks:

- `M_+` and `M_-` are monic, split, coprime, nonidentical, and of equal
  degree;
- `deg(M_+-M_-) <= deg(M_+)-r-1`;
- the multiplicity factorization of `M_+` and `M_-` equals the displayed
  weight;
- `mu_0=mu_1=mu_2=mu_3=0`;
- the lexicographic `4`-column Vandermonde pivot is nonzero and the
  degree-`0..3` Vandermonde has full row rank;
- support collapse and the `|supp(mu)|=r+2` BC case never occur;
- the reduced weight is projectively primitive;
- `U` is recovered from `(U_0,H,M_-)`, and the carried `G` reconstructs the
  deleted algebraic packet without loss.

The last item proves exact support cost one.  It does not prove that any
ledger pays that unit.

## Primary source-oriented replay

The upstream boundary packet is ordered lexicographically by its support pair.
In this fixture the outside support is the fixed `B`, so the primary replay
chooses the least `T` in each cell.  Its `91` emitted certificates have

```text
support-size histogram       {8:32, 10:40, 12:19}
extension mu_4=0              6
extension support histogram  {10:5, 12:1}
nonextension candidates      85
candidate support histogram  {8:32, 10:35, 12:18}.
```

The `6` extension certificates are classified by the algebraic predicate only.
No numerical payment is inferred from that classification.

## Auxiliary `(R,A)` replay

For comparison, choosing the lexicographically least `(R,A)` in each cell
emits the same `91` certificates but gives `3` extensions and `88`
nonextension candidates.  The support histogram is

```text
{8:40, 10:30, 12:21}.
```

The three extension comparisons are:

```text
c=5:
  (R0,A0)=((5,11,19),(15,24,27))
  (R,A)  =((12,26,28),(6,14,15))
c=26:
  (R0,A0)=((4,7,26),(16,22,30))
  (R,A)  =((5,12,20),(15,23,30))
c=28:
  (R0,A0)=((5,7,11),(13,14,27))
  (R,A)  =((7,19,28),(8,17,29)).
```

These `3/88` values are order-dependent diagnostics, not the main theorem.

## Order-invariant census

There are `484` ordered distinct same-cell comparisons.  Every reduced
support has size `8`, `10`, or `12`; their histogram is

```text
{8:198, 10:188, 12:98}.
```

Exactly `32` comparisons extend and all `452` nonextension comparisons are
projectively primitive.  Exhausting the representative choices cell by cell
shows that the total number of extensions ranges from `1` to `10`.  Therefore
every one-representative-per-cell choice leaves between `81` and `90`
nonextension projectively primitive algebraic candidates.

## Ownership

The upstream Rule-2 source states two separate facts:

1. certificate recovery gives exact support cost one;
2. a finite weighted primitive SP/Padé bound is still required.

The Route-D barrier map records this as the open conditional obligation
`A2`, owned by `weighted_primitive_sp_pade_bound`.  This packet instantiates no printed
`B_WSP_full` or genuine first-match owner interface.

Accordingly:

- the `91` comparisons are **emitted algebraic certificates**, not paid
  supports;
- the extension predicate classifies `6` primary certificates outside the
  nonextension algebraic subproblem, but does not pay them;
- the primary `85`, auxiliary `88`, and invariant `>=81` counts are
  **pre-first-match algebraic candidate counts**;
- none is called the official `N_WSP_full(z)`;
- none is called a genuine first-match unit;
- the common core `G` remains carried throughout.

The actual-incidence rank-drop owner from shipment `#920`, exact commit `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0` is also a different
object: it accepts an actual MCA-bad slope only when every maximal minor of
the ambient MCA Hankel matrix vanishes.  The `F_31` fixture is full rank, so a
nonzero WSP Vandermonde pivot does not create a rank-drop payment.

## Exact provenance

The algebraic source snapshot is commit
`c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.

- `experimental/notes/thresholds/rowsharp_q_singleton_topseam_v1.md`, blob
  `dda538a9a36cd0c8e267c11600a49cdc5bf054d1`;
- `experimental/scripts/verify_rowsharp_q_singleton_topseam_v1.py`, blob
  `dc4a7235b3274fbcc5ef0ed8bd8c96620b04a5a1`;
- `experimental/notes/thresholds/cap25_v13_route_d_barrier_map.md`, blob
  `ea896eca8bf89038b76469e51b6dd70eb83d3c02`;
- `experimental/data/cap25_v13_route_d_barrier_map.json`, blob
  `4d3d068cf80cd5912c998d86411e8baf33ece156`;
- `experimental/scripts/verify_route_d_barrier_map.py`, blob
  `2243a8c987d0493cb5f48f52b6174f735312e54a`;
- `experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md`, blob
  `ddfce00907f34128b324a64041f4e0ec8957b7d3`;
- `experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py`, blob
  `1702842190da45806e5a52e932aa4b8dab951ffe`;
- `agents.md`, blob `2fea2bce6a348105f0016fcf739b5247bf408d93`;
- predecessor `experimental/agents-log.md`, blob
  `45b04597efb40741b807e48b290a0544f2fe6baf`.

Shipment `#920` is exact commit
`a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`:

- `experimental/notes/thresholds/route_d_marked_rim_all_minors_adapter_v1.md`,
  blob `f24ce928df7e7170c1b4f3228d5fe9b184be50b4`;
- `experimental/scripts/verify_route_d_marked_rim_all_minors_adapter_v1.py`,
  blob `ace3e859b917ae87eeffb8c0e7c37155520e311e`;
- `experimental/lean/route_d_marked_rim_all_minors_adapter_v1/RouteDMarkedRimAllMinorsAdapterV1.lean`,
  blob `78e46c6ab97d97191c567041f81a6ca05e76cf41`.

## Nonclaims

- This packet does not prove or refute the deployed
  `67472*2130706433` support certificate or the KoalaBear safe row.
- It does not call exact support cost one a numerical payment.
- It does not charge the `91` emissions to the `28` representative cells.
- It does not call reduced-weight extension certificates extension-valued MCA
  slopes; the fixture slope is the base-valued `gamma=0`.
- It applies no extension payment theorem.
- It does not call any candidate the official `N_WSP_full(z)` or a genuine
  first-match unit.
- It does not claim that the fixture has executed `(B,C)`, `P1`, or the prior
  global first-match filters.
- It does not infer rank drop from one selected pivot minor.
- It does not use the shared slope `gamma=0` to pay marked support
  multiplicity.
- It does not discard the common-core mark `G`.
- It does not infer a deployed-field bound from `28/91/6/85`, `3/88`, or the
  invariant `>=81` counts.
- It does not claim that sparse/Padé certificate shape alone bounds finite
  multiplicity.

## Reproduction

```bash
python3 experimental/scripts/verify_route_d_rule2_wsp_algebraic_preflight_v1.py
python3 -O experimental/scripts/verify_route_d_rule2_wsp_algebraic_preflight_v1.py
python3 experimental/scripts/verify_route_d_rule2_wsp_algebraic_preflight_v1.py --tamper
```

The verifier uses only the Python standard library and reconstructs the
fixture from definitions.
