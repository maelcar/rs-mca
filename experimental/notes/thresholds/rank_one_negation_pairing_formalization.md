# All-depth rank-one negation-pairing formalization

## Claim

Let `k` be a natural number and let `a < 3^k`.  For the recursive width-`k`
balanced-ternary support count `s3`,

```text
s3 ((3^k - a) % 3^k) k = s3 a k.
```

Equivalently, for an arbitrary natural representative, reduce it before
forming the natural-number complement:

```text
s3 ((3^k - (a % 3^k)) % 3^k) k = s3 (a % 3^k) k.
```

## Status

PROVED.

## Source audit

The authoritative statement is the digit-count pairing used in Lemma R(a),
Section 1 of
`experimental/notes/thresholds/rank_one_emission_arithmetic.md`, integrated at
`168e9ba0` from source packet #818 at `03fa2958`.  Its balanced-ternary
convention and upstream rank-one product law come from #816 at `98e2a620`.
The direct downstream emission consumers are #820 at `d5f67b4b` and #824 at
`2f5162fc`.

The source notation `s3(-a) = s3(a)` lives in the residue ring modulo `3^k`.
Transcribing it as unrestricted natural subtraction would silently change the
statement: `3^k - a` saturates when `a > 3^k`.  The naive unrestricted theorem
is false already at `k = 1`, `a = 4`, where the two support counts are `0` and
`1`.  Lean therefore exposes both a canonical-representative theorem with
`a < 3^k` and an arbitrary-representative theorem that reduces `a` first.

At `k = 0`, the arithmetic statement remains true: the modulus is `1` and the
only residue is zero.  There is then no nonzero pair.  The hierarchy
application ordinarily has `1 <= k <= B`; that application range is not needed
by the arithmetic kernel.

## Lean correspondence

The declarations are in
`experimental/lean/rank_one_emission_arithmetic/RankOneEmissionArithmetic.lean`.

- `s3_pow_sub` proves the induction kernel for `a <= 3^k`.
- `pairing_symmetry_all` proves the source-shaped theorem for every depth.
- `pairing_symmetry_mod` gives the normalized arbitrary-`Nat` form.
- `pairing_symmetry` preserves the former depths-1--7 API, now as a corollary
  of the all-depth proof rather than a finite `native_decide` scan.

The package README contains the complete source-label to Lean-name status map.

## Proof outline

Write `a = 3q + d`, where `d = a % 3`.

- If `d = 0`, the complement is `3(3^k - q)` and induction applies at `q`.
- If `d = 1`, the complement is `3(3^k - q - 1) + 2`; balanced decoding
  carries the final `2` and again applies induction at `q`.
- If `d = 2`, the complement is `3(3^k - q - 1) + 1`; the original digit `2`
  carries, so induction applies at `q + 1`.

All quotient, remainder, carry, and truncated-subtraction facts are explicit in
the Lean proof.  The arbitrary-representative wrapper uses positivity of
`3^k` and `Nat.mod_lt`.

## Validation

From `experimental/lean/rank_one_emission_arithmetic`:

```bash
lake clean
lake build
```

The build uses the pinned `leanprover/lean4:v4.14.0` toolchain.  The source
certificate is replayed from the repository root with:

```bash
python3 experimental/scripts/verify_rank_one_emission_arithmetic.py
python3 experimental/scripts/verify_rank_one_emission_arithmetic.py --tamper-selftest
```

The first command ends with `RESULT: PASS (20/20)`; the second ends with
`tamper-selftest: caught 7/7`.

The verifier's diagnostic word `ALL` refers to its finite `B = 6`,
`k in {1,2,3}` scan.  It remains useful independent evidence, but the Lean
induction is what establishes the digit-count identity for every `k`.

## Scope and nonclaims

This packet formalizes only the digit-count symmetry kernel.  It does not
formalize balanced-digit vectors or their uniqueness, the complex-valued
definition of `G`, reindexing and conjugation of its finite sum, the absence of
nonzero fixed points under negation, or the cosine formula that proves `G` is
real.  It does not prove Lemma R(b,c), positivity or nonvanishing of `G`, the
rank-one cube product law, an emission budget, one-pattern-per-class admission,
soundness, an all-depth greedy theorem, image-scale MI/MA, direct Sidon payment,
a residual ray compiler, a complete profile-envelope comparison, an unsafe
lower reserve, an MCA threshold, or any finite deployed-row or Proximity Prize
claim.
