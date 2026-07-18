# Dense-shell class charges: integrated statement and verifier audit

**Status: COUNTEREXAMPLE**

**Audited object:** integration `a5750192a2fb4ff7e9f6b2f6bf77fa6652dffda7`
from PR #880 head `e465ee4422e04ba212611c97ccc7e2f8395c62bc`. The
threshold note, verifier, JSON certificate, and Lean source have SHA-256
digests pinned by
`experimental/scripts/verify_dense_shell_class_charges_audit.py`.

**Attribution:** the audited packet is by Holm Buar. This independent audit
replays its checks, compares each promoted statement with the literal verifier,
and tests omitted boundaries. It does not propose a new proof route.

## Verdict

Two integrated statements are false as written. In addition, the advertised
`B <= 49` theorem relies on finite-grid claims without continuum enclosures,
while the beyond-49 tail separately invokes loose constants that the shipped
verifier never produces. The four-grandchild algebra and `KEY` arithmetic
survive when their envelope and share inputs are treated as hypotheses; no
counterexample to that narrower coupled step was found.

### MUST — repair the universal charge identity

`experimental/notes/thresholds/dense_shell_class_charges.md:68-72` and
`:339-344` assert

```text
omega_U = Sigma_U + W_U always,
```

where `W_U` is the mass having the sign opposite to
`s_U = (-1)^(B-|U|)`. The same formula is exposed to consumers at
`:395-398`. It is correct only when `s_U=+1`.

The defining Fourier sum already gives a counterexample at `B=4`, `U={0}`.
The class consists of `sigma=1,80`, and its two values are

```text
h = [-1.7995914126035255, -1.7995914126035255].
```

Thus `s_U=-1`, `Sigma_U=-3.599182825207051`, and
`W_U=omega_U=0`, whereas `Sigma_U+W_U=-3.599182825207051`.

The correct identity under the class-sum sign law is

```text
omega_U = W_U + 1_{s_U=+1} |Sigma_U|.
```

Without the sign law, if `M_U=sum_class |h|`, the always-valid identity is
`omega_U=(M_U+Sigma_U)/2`. Delete the universal `Sigma_U+W_U` wording and
repair any consumer that copied it. The note's immediately following
wrong-parity formula `omega_U=W_U` is correct.

### MUST — P7's advertised pair-2 certificate is false

The note claims an entrywise secant exponent at most `1.61` on pair-2 support
`[0.3889,0.50]`, for every gap in `[1/18,1/9]`, at
`experimental/notes/thresholds/dense_shell_class_charges.md:183-190` and
`:308-315`. Direct evaluation of the verifier's exact recurrence, without
its interpolation layer, gives the coefficient-0 counterexample

```text
j = 3, x = 4/9, y = 1/2, y-x = 1/18
flip(G_3(x))[0] = 0.4941825271377098
flip(G_3(y))[0] = 0.4518963851007805
L = -log(min(Gx/Gy,Gy/Gx))/(y-x) = 1.6101363604711996 > 1.61.
```

This is not an endpoint-rounding artefact: `y=0.499999` and
`x=y-1/18` give `L=1.61013217413034`.

The gate does not see either point. It silently implements pair 2 as
`[0.38889,0.49995]` at
`experimental/scripts/verify_dense_shell_class_charges.py:563`, then tests
only the 111 nodes made by `secant_env(..., n=110)` at `:610-649`. The JSON
therefore records `1.6078949860283844`, not the supremum on the stated domain.

**Risk limit.** This counterexample falsifies the broad P7 statement and its
continuum-certificate interpretation, not the coupled `MASTER` step. The JSON
faithfully records the maximum of its truncated shallow grid. The coupled step
consumes envelope levels `q=j-1 >= 5`, while this example is at `q=3`; its
pair-2 children also satisfy the tighter relation `x+y=8/9`, which the example
does not. A minimal repair is to state the actual `MASTER`-consumed envelope
levels (`q=j-1=5..47` for the `B<=49` leg), restrict the gate to the two
coupled child curves, and supply a continuum enclosure including their
boundaries.

### MUST — downgrade finite C3 until its grids have enclosures

The note labels the `B<=49` result a theorem at
`experimental/notes/thresholds/dense_shell_class_charges.md:24-35`. Literal
inspection of the verifier shows:

- P7 uses an interpolated cascade with no interpolation remainder
  (`:483-517`) and a finite secant grid with no between-node enclosure
  (`:610-649`).
- P9 calls its bases Lipschitz-certified, but derives `maxslope` from adjacent
  sampled values and then treats that observed slope as a global bound
  (`:685-725`).
- P12 samples 199 interior epsilon values, omits both limiting endpoints, and
  supplies no cell enclosure (`:884-906`).

These are deterministic floating-grid checks, not continuum certificates.
Until finite enclosures are supplied, the `B<=49` leg should be labelled
computed-grid/conditional rather than `THEOREM`.

### MUST — treat the loose tail caps as unproduced hypotheses

The finite `B<=49` leg uses the sharp `0.85/1.61/1.20` inputs, not the loose
caps. Separately, `1.086` and `1.663` occur as numerical inputs only inside
`gate_key`, at
`experimental/scripts/verify_dense_shell_class_charges.py:655-680`. P8 checks
`KEY` **given** those values; no closure map or all-level envelope gate
produces them. This contradicts the `PROVED all-j loose caps` wording at note
lines `38-43`, `174-200`, `255-256`, and `303-320`. The all-B
`INV-TAIL` support must treat both values as hypotheses until a producer is
integrated; P8 should be described as a conditional implication.

### SHOULD — narrow two interface claims

- C3b says global positivity is **equivalent** to positivity of every prefix
  charge at note lines `45-54`. P11 establishes
  `E_w=(4^B/W) sum_pi T_pi` and exhaustively checks all terms only for
  `B in {6,8}` at verifier lines `815-849`. Termwise positivity is
  sufficient; positivity of a sum does not by itself prove every term
  positive. Replace `EQUIVALENT` with a sufficient per-prefix obligation
  unless a converse is added.
- The shipped JSON is fresh for the shallow run, but is not bound to a source,
  command, or horizon. `--emit-cert` calls shallow `run()` at verifier lines
  `963-980`; the `--deep` branch is separate at `:982-983`. The JSON
  contains no commit, source hash, script hash, command, `deep`, or `jmax`
  field, and the verifier never loads it. It therefore cannot attest the
  note's `j<=48` claim even though a fresh deep replay prints PASS.

### NOTE — clean checks and exact scope

- `python3 experimental/scripts/verify_dense_shell_class_charges.py` and its
  `--deep` run both print `RESULT: PASS (19/19)`; the tamper self-test
  catches `9/9` mutations. Those results are compatible with the findings
  above because the false boundary and missing producers are outside the
  literal gates.
- `lake build` succeeds for
  `experimental/lean/dense_shell_class_charges` with no `sorry`, `admit`,
  or added axiom. Its formal scope is the finite partition census through
  `B<=12`, an integer polynomial factorization/coefficient shadow, and the
  flip-cardinality census through `B<=8`. It does not formalize `MASTER`,
  `KEY`, the analytic envelopes, C3, or the consumer identity; the source
  header accurately calls it a skeleton.
- The four-grandchild coordinate identities, the decomposition of `Delta`,
  and the scalar `KEY` direction check out conditional on the stated
  componentwise envelope/share hypotheses.

## Deterministic reproduction

Run, using only the Python standard library:

```bash
python3 experimental/scripts/verify_dense_shell_class_charges_audit.py
python3 -O experimental/scripts/verify_dense_shell_class_charges_audit.py
python3 experimental/scripts/verify_dense_shell_class_charges_audit.py --tamper-selftest
```

The normal and optimized runs print `STATUS: COUNTEREXAMPLE` and exit zero
only when the pinned sources, both counterexamples, and the provenance checks
all match. The tamper self-test confirms that loosening the P7 cap or
substituting the correct parity-dependent identity is rejected as a purported
counterexample.
