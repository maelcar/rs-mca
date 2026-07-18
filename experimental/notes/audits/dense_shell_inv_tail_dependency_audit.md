# Dense-shell `INV-TAIL` dependency audit

## Verdict

```text
Status: OPEN GAP / AUDIT
Upstream snapshot audited: a5750192a2fb4ff7e9f6b2f6bf77fa6652dffda7
Promotion rule: fail closed.
```

The dense-shell class-charge packet does not currently prove an all-depth
class-sum theorem. Its closed-form reductions remain useful, and its finite
scans are reproducible evidence, but the load-bearing tail inequalities are
open. A passing verifier or a building Lean shadow must not be read as
discharging either tail contract below.

This audit traces the claims in
`experimental/notes/thresholds/dense_shell_class_charges.md` to the Python
verifier, its JSON certificate, and the standalone Lean package. A finite
floating-point grid is **COMPUTED** evidence unless a separate continuum and
rounding enclosure is supplied.

## 1. Corrected tail contracts

The upstream packet mixed a broad envelope statement with the narrower pairs
actually consumed by the Master step. The audited interface now separates two
sufficient contracts and scopes both to the exact correlated pairs.

For `epsilon in [0,1/4]`, define

```text
pair 1: x1 = 7/36 - epsilon/9,  y1 = 1/4 + epsilon/9
pair 2: x2 = 5/12 - epsilon/9, y2 = 17/36 + epsilon/9
gap:    y1-x1 = y2-x2 = 1/18 + 2 epsilon/9.
```

The secant envelope at level `j` is the maximum, over every shared active
coefficient, of `|log(G_j(x)_i/G_j(y)_i)|/(y-x)`.

### 1.1 `INV-TAIL-SHARP`

For every `j >= 49` and every displayed `epsilon`, require:

```text
pair-1 correlated secant <= 0.85,
pair-2 correlated secant <= 1.61,
G_j(1/4-epsilon/3)_i >= 1.20 G_{j-1}(1/4+epsilon/9)_i
  for every shared active index i.
```

This is exactly the sharp bundle consumed by `(KEY)`. It is open.

The former superset claim—pair-2 `<=1.61` for every admissible pair in
`[0.3889,0.50]`—is not a valid replacement. A direct tree-recursion negative
control at `j=3`, `i=0`, `x=4/9`, `y=1/2` gives
`1.61013636047 > 1.61`. The verifier pins this witness, while certifying only
the correlated scope used downstream.

### 1.2 `INV-TAIL-LOOSE`

A weaker sufficient bundle replaces the two correlated caps by `1.086` and
`1.663` while retaining the share floor `1.20`. P8 reports a positive scalar
margin when these values are supplied. It does not derive them.

The proposed L4/L4' route to those loose caps still consumes:

```text
INV-TAIL-SHARE:
  the quantified all-level share floor;

INV-TAIL-CROSS:
  explicit uniform cross-child ratio bounds strong enough for L4';

INV-TAIL-CLOSURE:
  a proved invariant calculation showing that SHARE + CROSS propagate
  the regional family and imply 1.086/1.663 at all later levels.
```

Thus `INV-TAIL-LOOSE` is weaker only after these premises are stated and
proved. No shipped artifact currently does so.

## 2. P8 is implication-only

P8 substitutes the sharp and loose constant triples into `(KEY)`:

```text
(0.85,  1.61,  1.20)   -> sampled minimum about 0.030
(1.086, 1.663, 1.20)   -> sampled minimum about 0.015.
```

Its valid interface is

```text
supplied envelope caps + supplied child-share floor
  ==> the sampled KEY scalar is positive.
```

It does not calculate an envelope, prove the share floor, run L4', or cover
`j >= 49`. Its margins are implication-only, not evidence that either
`INV-TAIL` contract holds.

## 3. Finite evidence and certificate horizon

After the audit, P7 scans only the two correlated pairs on a 400-subinterval
`epsilon` grid, including both endpoints. It checks every coefficient rather
than silently dropping entries below a floating threshold. P12 checks 199
interior `epsilon` samples per level and likewise records zero omitted or
nonpositive denominators. A `--deep` run reaches `j=48`; it does not reach the
tail `j>=49`.

These are still **COMPUTED** floating-grid results:

- barycentric interpolation and ordinary binary floating arithmetic are used;
- no rigorous rounding enclosure is supplied;
- no modulus bounds the values between samples;
- P9's base floors use the largest adjacent sampled slope, not a proved
  Lipschitz constant.

The analytic Master-step algebra may therefore be used as a theorem *given*
its envelope/share hypotheses, while the finite P7/P9/P12 outputs remain
computed evidence under this audit's fail-closed standard.

The pre-audit JSON had SHA-256
`932a222fb8270a2350f3236e289466838fbdea3977c4f7794f3aba78b87c4fed`.
It was generated on the quick `jmax=16` path, omitted its horizon, and exposed
only a top-level `pass: true`. The repaired v2 generator honors
`--emit-cert --deep` and records:

- `deep: true`, `deep_scope: [P7,P12]`, an envelope/share horizon of `48`,
  and per-gate horizons (`P6=12`, `P7=48`, `P9=16`, `P12=48`);
- `check_status: PASS` only for finite checks, alongside
  `mathematical_verdict: OPEN_GAP` and `all_depth_proved: false`;
- `inv_tail_status: OPEN` and `general_k_status: CONJECTURAL`;
- `envelope_scope: exact-correlated-master-pairs` and the pair formulas;
- sharp and loose contract constants, both P8 margins, and the broad-pair
  negative control;
- coefficient-coverage counts for P7 and P12;
- the corrected parity-dependent charge identity and its old-formula witness.

The independent audit certificate binds the source artifacts by SHA-256. None
of these metadata repairs changes the mathematical verdict from **OPEN GAP**.

## 4. Dependency map

The permitted routes are:

```text
INV-TAIL-SHARP on exact correlated pairs + SHARE
                         |
                         v
                   sharp-cap (KEY)

INV-TAIL-SHARE + INV-TAIL-CROSS + proved L4' closure
                         |
                         v
             loose correlated caps 1.086 / 1.663
                         |
                         v
                   loose-cap (KEY)
```

Either completed route feeds the same conditional chain:

```text
(KEY) + purity at level j-1 + exact Master-step algebra
  -> MASTER M_j
  -> joint induction for cascade cone purity
  -> Phi domination and A-purity (R1-R3)
  -> R4 single-insertion tree identity
  -> positivity for |K|=1
  -> C1 kernel reduction plus the imported dense-shell sign of hatf
  -> the singleton support-class sign statement.
```

It does not establish general-`K` positivity, pointwise sign purity, a
product-profile schedule, adequacy, or any lower-reserve claim.

## 5. C3b correction: sum identity, one-way sufficiency

The reduction implemented by P11 has the form

```text
E_w[prod_K (a_k-1/2)] = positive_scale * sum_pi T_pi(K).
```

Consequently the global positivity statement is equivalent to positivity of
the *sum*. Positivity of every `T_pi(K)` is a useful sufficient strengthening:

```text
(forall pi, T_pi(K)>0)  ==>  E_w[prod_K(a_k-1/2)]>0.
```

The converse is not supplied. The audited C3b interface is therefore an exact
sum identity plus a condition **IMPLIED BY** per-prefix positivity, not an
equivalence with every summand.

For `|K|=1`, the R1-R4 route inherits the conditional/finite-evidence scope
above. For `|K|>=2`, P11 computes every tested prefix only for `B in {6,8}`.
Uniform general-K positivity remains **CONJECTURAL** and is not discharged by
either tail contract.

## 6. C6 correction: parity-dependent charge arithmetic

Let

```text
P_U     = sum_{h(sigma)>0 in class(U)} h(sigma),
N_U     = sum_{h(sigma)<0 in class(U)} |h(sigma)|,
Sigma_U = P_U-N_U,
omega_U = P_U,
s_U     = (-1)^(B-|U|),
W_U     = mass whose sign is opposite s_U.
```

Then the unconditional identity is

```text
omega_U = W_U + ((1+s_U)/2) Sigma_U.
```

Equivalently, `omega_U=Sigma_U+W_U` when `s_U=+1`, and `omega_U=W_U`
when `s_U=-1`. Within the class-sum sign law's actual scope, the positive-
parity formula becomes `|Sigma_U|+W_U`; the negative-parity formula does not.

The previous blanket formula `omega=Sigma_U+W_U always` was false. G6 now
checks the corrected identity from inverse-transform data and requires a
negative-parity counterexample to the old formula. Consumers must branch on
parity and must not treat the general-K conjecture as a proved sign law.

## 7. Lean coverage

The standalone module explicitly leaves MASTER, cone purity, and the leak
table outside Lean. It formalizes only:

- the support-class partition census through `B<=12`;
- the `T_9(x)-1` integer-polynomial factorization and zero cubic coefficient;
- flip-cardinality through `B<=8`.

It contains no tail contract, L4' closure, P8, MASTER theorem, class-sum
theorem, decorated-charge identity, or charge-arithmetic theorem. A successful
`lake build` verifies those finite shadows and provides no evidence for
`INV-TAIL`.

## 8. Repairs applied and remaining proof targets

This audit applies the following artifact-level repairs:

1. splits sharp and loose tail contracts and narrows P7 to the exact correlated
   pairs consumed by Master;
2. pins the overbroad pair-2 negative control;
3. changes C3b from per-prefix equivalence to the global-sum identity and a
   one-way sufficient condition;
4. replaces the parity-blind C6 formula and adds G6 plus a tamper;
5. labels floating P7/P9/P12 scans COMPUTED and records their finite horizon;
6. makes `--emit-cert --deep` honest about scope, status, domains, and
   coefficient coverage;
7. adds a source-bound, tamper-tested dependency-audit certificate.

The remaining mathematical targets are: rigorously enclose the finite
P7/P9/P12 continuum ranges; then prove the sharp tail bundle, or prove the
share/cross-child/closure package that yields the loose bundle. A separate
proof is required for uniform general-K positivity.

## 9. Nonclaims

- This audit does not refute either corrected tail contract; it records that
  the shipped artifacts do not prove one.
- It does not promote the finite numerical observations to continuum theorems.
- It does not challenge the imported dense-shell sign theorem for `hatf`.
- It does not turn `pass: true`, a deep horizon, or a zero-`sorry` Lean build
  into an all-depth result.
- It does not authorize paper, leaderboard, adequacy, or lower-reserve changes.
- No class-sum statement may be promoted from this audit alone. The allowed
  verdict is **OPEN GAP**.

## 10. Reproduction commands

From the repository root:

```sh
python3 experimental/scripts/verify_dense_shell_class_charges.py
python3 experimental/scripts/verify_dense_shell_class_charges.py --emit-cert --deep
python3 experimental/scripts/verify_dense_shell_class_charges.py --tamper-selftest
python3 experimental/scripts/verify_dense_shell_inv_tail_dependency_audit.py --check
python3 experimental/scripts/verify_dense_shell_inv_tail_dependency_audit.py --tamper-selftest
(cd experimental/lean/dense_shell_class_charges && lake build)
```

These commands reproduce and bind the finite artifacts. They do not change the
verdict above.
