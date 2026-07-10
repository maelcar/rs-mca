# KB signed-`e_m`: exact mixed twist-orbit `L2` energy gives a uniform toy-family `L1` bound

Status: `PROVED` (the mixed-axis Parseval identity, twist-orbit count, coset
invariance, and Cauchy--Schwarz bound) / `MEASURED` (exact three-coset replay) /
`ANALYSIS` (scope relative to PR #467) / `OPEN` (deployment and masked transfer).

## Claim  `PROVED`

Continue the PR #467 toy at

```text
(p,n,m,w) = (193,64,30,2),   H = mu_64 subset F_193^*.
```

For every multiplicative coset `D=alpha H`, let

```text
N_D(z1,z2) = #{M subset D : |M|=30,
                sum_(x in M) x=z1, sum_(x in M) x^2=z2},
E_D(t1,t2) = sum_z N_D(z) e_p(t1 z1+t2 z2),
S_mix(D) = sum_(t1!=0,t2!=0) |E_D(t1,t2)|.
```

By the prefix Fourier identity used in PR #467,
`E_D(t1,t2)=e_m((e_p(t1*x+t2*x^2))_(x in D))`; hence `S_mix` is exactly the
mixed signed-`e_m` sum requested here.

Then the entire three-coset toy family satisfies the rigorous bound

```text
(S_mix(D)/C)^2
  <= 200854868855373833216
     / 284866887702733424996141587472161
  = 7.050832424755927189e-13,

S_mix(D)/C
  <= 839692349898 / 10^18
  = 0.000000839692349898,

C = binom(64,30) = 1620288010530347424.
```

The last decimal is an **upward** rational ceiling, not a rounded estimate.
Thus the mixed-orbit signed sum cannot be as large as `C` anywhere in this toy
coset family.  This is an upper bound for the requested mixed-orbit component;
it is not a deployed-row bound.

## Proof

### 1. Exact mixed-axis energy  `PROVED`

Put

```text
N_1(z1) = sum_z2 N_D(z1,z2),
N_2(z2) = sum_z1 N_D(z1,z2).
```

Unnormalized finite Fourier Parseval gives

```text
sum_(t1,t2) |E_D(t1,t2)|^2 = p^2 sum_(z1,z2) N_D(z1,z2)^2,
sum_t1 |E_D(t1,0)|^2       = p   sum_z1 N_1(z1)^2,
sum_t2 |E_D(0,t2)|^2       = p   sum_z2 N_2(z2)^2.
```

The origin has energy `C^2` and is counted on both axes.  Inclusion--exclusion
therefore gives the exact mixed-frequency energy

```text
E_mix := sum_(t1!=0,t2!=0) |E_D(t1,t2)|^2
       = p^2 sum N_D^2 - p sum N_1^2 - p sum N_2^2 + C^2.
```

The exact subset DP in the verifier yields

```text
total nonzero energy    = 50420855234751011040
linear-axis energy      = 488790592
quadratic-axis energy   = 207138020418762144
mixed energy E_mix      = 50213717213843458304

E_mix / total nonzero energy
  = 1569178662932608072 / 1575651726085969095
  = 0.9958918185750092300...
```

This upgrades PR #467's floating mixed-`L2` share to an exact integer identity
for the toy family.

### 2. Twist orbits and `L2`-to-`L1`  `PROVED`

There are

```text
(p-1)^2 = 36864
```

mixed modes.  Since `t1!=0`, every mixed mode is primitive under the KB twist
action

```text
h.(t1,t2) = (h t1, h^2 t2),   h in H,
```

so every orbit has size `n=64`.  Hence the mixed modes form exactly

```text
36864/64 = 576
```

twist orbits.  If `a_O` is the common magnitude on orbit `O`, then

```text
S_mix = 64 sum_O a_O,
E_mix = 64 sum_O a_O^2.
```

Cauchy--Schwarz on the 576 orbit amplitudes gives

```text
S_mix^2 <= 64^2 * 576 * sum_O a_O^2
        = 36864 * E_mix.
```

Dividing by `C^2` and substituting the exact energy above gives the stated
rational bound.  No floating signed-`e_m` computation is used in the proof.

### 3. Uniformity over the coset family  `PROVED`

Scaling `H` by `alpha!=0` sends a fiber target by the bijection

```text
(z1,z2) -> (alpha z1, alpha^2 z2).
```

It also sends mixed frequencies by the inverse coordinate scaling.  Thus the
joint fiber table, both marginal square sums, `E_mix`, and `S_mix` are permuted,
not changed.  Since `[F_193^*:H]=3`, representatives `1,5,25` cover every
distinct coset.  The verifier independently recomputes all three exact fiber
tables and checks the coordinate permutation entry by entry.

## Interpretation  `ANALYSIS`

PR #467 found that mixed primitive modes carry almost all of the toy's `L2`
energy.  That fact alone did not bound their `L1` contribution.  The identity
above supplies such a bound using only exact fiber collisions and the finite
mixed-orbit count.  It is deliberately modest: Cauchy--Schwarz discards the
two-heavy-orbit shape observed in #467, but it is rigorous and uniform over the
complete toy coset family.

The argument becomes useful at another row only after that row supplies a
strong enough exact or proved mixed collision-energy bound.  Replacing the toy
energy by a loose deployed second-moment estimate would reproduce the already
known dead `L2` route.

## Open scope  `OPEN`

This packet does not prove:

```text
the mixed-orbit bound at the deployed KB row;
the raw signed-e_m inverse or def:q-row-atom;
a bound after first-match masking;
twist stability of the theorem-facing mask;
transfer from subgroup index 3 to subgroup index 1016;
U(1116048) <= B* or any adjacent safe row.
```

The remaining atomic input is a deployed mixed collision-energy or tail bound
that beats the finite row margin without importing the dead unrestricted
second-moment estimate.

## Verifier  `MEASURED`

`experimental/scripts/verify_kb_mixed_orbit_l2_bound.py` is zero-argument and
stdlib-only.  It recomputes the joint and marginal fiber tables, every integer
above, all three cosets, the exact rational ceiling, the committed JSON, and ten
live tamper tests in which a corrupted value reaches and fails a real gate.

```bash
ulimit -v 2097152
python3 experimental/scripts/verify_kb_mixed_orbit_l2_bound.py
```

Data: `experimental/data/cap25_v13_kb_mixed_orbit_l2_bound.json`.
