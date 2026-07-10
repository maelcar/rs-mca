# KB mixed twist-orbit energy across a subgroup-index ladder: the coset refinement is ceilinged at `sqrt(index)`

Status per claim:

- `PROVED`: the exact per-coset energy decomposition `sum_kappa E_kappa = E_mix`;
  the rigorous heavy/light **coset-split** `L1` bound; the folding lemma
  `f_t(x)=f_t(s-x)`; and the **method-ceiling theorem** that the coset split
  improves the mixed-orbit `L1` bound over plain Cauchy--Schwarz by at most a
  factor `sqrt([F_p^*:H])`.
- `MEASURED`: a 25-point graded ladder in subgroup index `[F_p^*:H]` and field
  `p`, with the exact energies, orbit-amplitude profile, heavy-coset count, and
  Cauchy--Schwarz slack at each point (`#475`'s index-3 point recomputed
  byte-identical as an anchor).
- `REFUTED`: the small-value-set / popular-sum hypothesis as a *determinant* of
  the heavy mixed orbits (it is a correlate, not a predictor).
- `OPEN`: the deployed transfer. The ceiling theorem shows *this* structure
  cannot cross the deployed margin; the atomic input of `#475` (a
  better-than-second-moment handle on `E_mix` itself) is untouched.

This continues PR `#467` (signed-`e_m` inverse narrowed to the mixed twist-orbit
wall) and PR `#475` (exact mixed-axis `L2` energy -> toy `L1` bound at
`(193,64,30,2)`, index 3). `#475`'s open scope — *"a deployed mixed
collision-energy or tail bound that beats the finite row margin without importing
the dead unrestricted second-moment estimate"* — is the lane. The ladder is the
transfer instrument: the deployed KB row has subgroup index `1016`.

**Verifier:** `experimental/scripts/verify_kb_mixed_orbit_index_ladder.py`
(zero-argument, stdlib-only, `RLIMIT_AS`-capped at 2 GiB, ~17 s,
`RESULT: PASS (846/846 checks; tampers 17/17)`).
Data: `experimental/data/cap25_v13_kb_mixed_orbit_index_ladder.json`.

## What this is / is not

`#475` proved one rigorous `L1` bound at one toy (index 3) by Cauchy--Schwarz on
`576` twist orbits. This packet asks the *transfer* question head-on: does the
mechanism strengthen or weaken as the subgroup index climbs toward the deployed
`1016`? It supplies (i) an exact energy decomposition finer than `#475`'s (per
`s`-coset, not just total mixed), (ii) a rigorous bound that exploits it, and
(iii) a **proof that the exploitation has a hard ceiling** of `sqrt(index)`.

It does **not** prove a deployed bound, the raw/masked signed-`e_m` inverse, or
`U(1116048)<=B*`. It imports **no** unrestricted second-moment estimate.

---

## 1. Exact per-coset energy decomposition  `PROVED`

Fix `(p,n,m,w=2)`, `H=mu_n subset F_p^*`, `C=binom(n,m)`. For `D=H` let
`N(z_1,z_2)=#{M subset D: |M|=m, (sum x, sum x^2)=(z_1,z_2)}` and
`E(t)=sum_z N(z) e_p(t.z)=e_m((e_p(t_1 x+t_2 x^2))_{x in D})`, the mixed
signed-`e_m` sum. `#475`'s mixed-axis Parseval identity is

```text
E_mix = sum_{t_1,t_2 != 0} |E(t)|^2 = p^2 sum N^2 - p sum N_1^2 - p sum N_2^2 + C^2.
```

**Coordinates.** A mixed mode `(t_1,t_2)` with `t_1,t_2 != 0` is equivalent to
`(s,t_2)` with `s = -t_1/t_2 != 0`, since `f_t(x)=t_1 x + t_2 x^2 = t_2 x(x-s)`.
The KB twist `h.(t_1,t_2)=(h t_1, h^2 t_2)` acts by `s -> s/h`, `t_2 -> h^2 t_2`;
the invariant `s^2 t_2` labels orbits, so **twist orbits `<-> (J=s^2 t_2, coset(s))`**
with `J in F_p^*` and `coset(s) in F_p^*/H`. There are `index=(p-1)/n` cosets,
each carrying `p-1` orbits, `(p-1)^2/n` orbits total.

**Per-coset energy (new).** For an `H`-coset `kappa` of `s`,

```text
E_kappa := sum_{t mixed, coset(-t_1/t_2)=kappa} |E(t)|^2
         = sum_{s in kappa} ( p sum_y R_s(y)^2 - C^2 ),
   R_s(y) = #{M: sumsq(M) - s.sum(M) = y} = sum_{z_1} N(z_1, y + s z_1),
```

a **sheared marginal** of the joint fiber table. Each `p sum_y R_s(y)^2 - C^2` is
an exact integer, so `E_kappa` is an exact integer and
`sum_kappa E_kappa = E_mix` (verified exactly at every ladder point with
`p <= 151`; the verifier asserts the identity and recomputes `#475`'s
`(193,64,30)` value `E_mix = 50213717213843458304` byte-identically).

**Why the coset is the right unit  `PROVED`.** Galois `sigma_a: zeta_p -> zeta_p^a`
sends `E(t) -> E(at)`, so the multiset `{|E(t)|^2}` is permuted by scaling
`t -> at`, which fixes `s` (hence `coset(s)`) and scales `J`. Scaling is
transitive on the `p-1` values of `J` inside a coset, so `sum_{O in kappa} |E|^2`
is Galois-stable, hence a **rational integer**; a single twist orbit's energy is
generically an *irrational* algebraic integer (§3 exhibits `A_0`). **The
`s`-coset is the finest exactly-rational refinement of `E_mix`.** This is the
sharp reason the strong (per-orbit, phase-driven) concentration cannot be
rigorously exploited: only the coarser, across-coset concentration is
exactly-rational.

## 2. The index ladder  `MEASURED`

25 points, `w=2`, `m ~ n/2`, over families `n in {6,12,20,30}` (varying index at
fixed `n`) plus large-subgroup anchors `n in {48,54,64}` at low index. Two
control axes matter: the index `I=(p-1)/n` and the **subgroup largeness**
`lambda = n/sqrt(p)` (equivalently `n^2/p`; the deployed row has `lambda ~ 45`).
Let `beta_1 = E_{kappa*}/E_mix` be the heaviest-coset energy fraction.

```text
family n=6  : I= 1  2  5 10 21 51 100 -> beta_1= 1.00 .65 .33 .18 .092 .039 .020   (beta_1*I -> 2.0)
family n=12 : I= 1  3  5  9 13 20  26 -> beta_1= 1.00 .53 .38 .21 .21 .116 .108
family n=20 : I= 2  5  9 20          -> beta_1= .73 .65 .42 .15
family n=30 : I= 1  2  5  7          -> beta_1= 1.00 .55 .48 .92   (I=7 is a resonance)
anchors     : (97,48) (109,54) (193,64), I=2,2,3, lambda=4.9,5.2,4.6 -> beta_1= .9998 .9925 .9996
```

Two clean readings, one wall:

1. **Small subgroup (`lambda < 1`): concentration disperses.** `beta_1 ~ c(n)/I`
   (for `n=6`, `beta_1*I -> 2.0`). Across-coset structure vanishes as the index
   climbs. `E_mix/C^2` grows roughly linearly in `I`; the CS slack
   `CS_bound/S_mix` grows then saturates (`n=6 -> 1.37`, `n=12 -> 2.24`).

2. **Large subgroup (`lambda > 4`, the deployed regime): one coset dominates.**
   At the anchors `beta_1 >= 0.99` — nearly all mixed energy sits in a single
   `s`-coset — and the CS slack is large (`6.9`--`14.7`).

3. **The wall is the joint corner.** `beta_1` is pushed to `1` by large `lambda`
   and to `0` by large `I`. Exact toys reach large-`lambda`/small-`I`
   (`beta_1 ~ 1`) and small-`lambda`/large-`I` (`beta_1 ~ 0`), but the `binom(n,m)
   < 2^64` exact-cell bound (which caps `n <~ 66` at `m~n/2`) **forbids the
   large-`lambda`/large-`I` corner** — exactly the deployed row
   (`lambda ~ 45, I=1016`). The ladder structurally cannot observe deployed
   concentration.

## 3. Heavy-orbit structure  `PROVED` folding / `REFUTED` predictor

**Folding lemma `PROVED`.** For a mixed mode, `s=-t_1/t_2` gives
`f_t(s-x)=f_t(x)` for all `x` (verified exhaustively over all mixed modes at
`(13,12,6)` and `(41,20,10)`):

```text
f_t(s-x)-f_t(x) = t_1 s + t_2 s^2 - 2x(t_1+t_2 s) = 0   since t_1 + t_2 s = 0.
```

So `f_t` is invariant under the involution `x -> s-x`; on `H` its value set has
size `<= n - P(s)`, `P(s)=` #paired `{x,s-x} subset H`, and
`r_H(s)=#{x in H: s-x in H}=2P(s)+[s/2 in H]` is **constant on `H`-cosets**
(verified at `(61,12,6)`). This is the mixed / *ramification* analogue of the
small-value-set families of PR `#465` (which established, on the C9 side via the
identical object `mu_hat(c)=e_m(v_c)/C`, that large signed-`e_m` concentrates on
small value sets). Here `w=2` caps folding at half, so mixed value sets never
reach `#465`'s extreme `k in {2,3,4}` arcs.

**But popular sums do not predict the heavy orbit  `REFUTED`.** Ranking cosets by
exact `E_kappa` vs by `r_H` (or value-set size, or collision sum) agrees only
`2/3` of the top-3, never fully. Decisively, at the `(211,30,15)` resonance the
verifier records the heaviest orbit `t=(13,65)`:

```text
value set 28 of 30, only 2 folded pairs, yet |E|/sqrt(C) = 40.84   (generic ~ 1),
exact autocorrelation A_0 = sum_r g_r^2 = 114037737322042,
g_r = #{M: t.Phi(M) = r}.
```

The *maximally* folded coset there has `r_H=8` (value set 26) but only `2.4%` of
the energy, while the dominant coset has `r_H=5`; and at `(61,30,15)` the
most-folded orbit (7 pairs) is *sub-generic* (`|E|/sqrt(C)=0.73`). **The
amplifier of a heavy mixed orbit is a global subset-sum resonance — a large
`A_0` autocorrelation of the projected counts — not the local value-set
degeneracy of `f_t`.** This sharpens `#465` within the mixed subspace: small
value set is neither necessary nor sufficient there.

## 4. The coset-split bound and its ceiling  `PROVED`

Write `S_mix = n sum_O a_O`, `a_O=|E(t_O)|`, `E_kappa = n sum_{O in kappa} a_O^2`.
Peel the `K` heaviest cosets; Cauchy--Schwarz inside each coset (`p-1` orbits)
and over the light remainder (`N_light` orbits) gives the rigorous bound

```text
S_mix <= sum_{kappa heavy} sqrt( n (p-1) E_kappa )  +  sqrt( n N_light E_light ),
```

with `E_light = E_mix - sum_heavy E_kappa` and all radicands exact integers (the
verifier uses exact integer square-root ceilings). Plain `#475` is
`S_mix <= sqrt((p-1)^2 E_mix)`. Define `gain = CS_ceiling / split_ceiling >= 1`.
The ladder gains are modest generically (`1.01`--`1.18`) and large only at
concentration (`1.69` at the `(211,30,15)` resonance and `(193,64,30)` anchor).

**Method-ceiling theorem  `PROVED`.** By subadditivity of the square root
(`sqrt a + sqrt b >= sqrt(a+b)`) and `N_light >= (I-K)(p-1) >= p-1` when `I>K`,

```text
split >= sqrt(n(p-1) E_heavy) + sqrt(n(p-1) E_light) >= sqrt( n(p-1) E_mix ),
```

so, since `CS = (p-1) sqrt(E_mix)` and `(p-1)/n = I`,

```text
gain = CS / split  <=  (p-1) sqrt(E_mix) / sqrt(n(p-1) E_mix)  =  sqrt(I) = sqrt(index),
```

with equality iff the entire mixed energy lies in one `s`-coset. The verifier
gates the exact core `split_ceiling^2 >= n(p-1) E_mix` and `gain <= sqrt(index)`
at every point. **The coset refinement can beat plain Cauchy--Schwarz by at most
a factor `sqrt(index)`.**

## 5. Deployed statement  `OPEN` wall + falsifier

Deployed KB-MCA row (pinned from `cap25_v13_q_moment_floor_reconciliation.md`):

```text
p = 2^31-2^24+1 = 2130706433,  n = 2^21,  m = 981104,  w = 67471,
a_+ = 1116048,  B* = 274980728111395087,  index = (p-1)/2^21 = 1016.
```

**The ceiling theorem is deployment-facing and unconditional.** At `index=1016`
the coset split can improve `#475`'s Cauchy--Schwarz by at most

```text
sqrt(1016) = 31.87x = 4.994 bits,
```

**even under the most favorable hypothesis** that the entire deployed mixed
energy concentrates in a single `s`-coset (`beta_1 = 1`). The dead unrestricted
second-moment / Plancherel route is short by `1,045,396.58` bits per stratum
(`cap25_v13_q_em_inverse_participation_ratio.md` §1, HARD BOUNDARY (a); not
imported here). A `<6`-bit refinement cannot cross a `~1.045e6`-bit deficit.

Conditional deployed statement, with a **named finite hypothesis**:

> **(H-conc).** The deployed mixed energy `E_mix^{dep}` is carried, up to a
> fraction `delta`, by `K=O(1)` deployed `s`-cosets.
>
> **Consequence.** Even with `(H-conc)` at `delta=0`, `K=1`, the coset split
> gives `S_mix^{dep} <= sqrt(1016)^{-1} * CS^{dep}` — a `4.994`-bit gain. The
> deficit that must be paid lives in `E_mix^{dep}` itself, not in the
> Cauchy--Schwarz slack; the coset structure does not touch it.

So the honest bank is a **PROVED negative about this method**: the mixed
twist-orbit coset structure, in its most concentrated possible form, is a
sub-6-bit polish of Cauchy--Schwarz at the deployed index and cannot supply
`#475`'s missing atom. The atom remains a genuinely-better-than-second-moment
bound on the deployed mixed collision energy `E_mix^{dep}` (equivalently a
tail/threshold bound on the *per-orbit*, phase-driven amplitudes, which §1 shows
are not exactly-rational and therefore invisible to any coset-level argument).

**Falsifier (what would revive the transfer).** Extend the *exact* ladder into
the jointly-large corner `lambda >~ 10`, `index >~ 10` (requires breaking the
`2^64` cell bound — big-integer cells or a coset-restricted exact DP) and measure
`beta_1` and the per-orbit amplitude tail. The transfer is alive **iff** at large
`lambda` the concentration escapes the `s`-coset level, i.e. a *sub-coset*,
exactly-rational, `Omega(1)`-mass structure appears whose `L1` payment is not
ceilinged by `sqrt(index)`. The present data (coset-level `beta_1` capped, gain
`<= sqrt(index)`) predicts it does not.

## 6. Boundaries, weave, nonclaims  `AUDIT`

- **HARD BOUNDARY (a).** No unrestricted second-moment estimate is used. The
  bound is built from the *exact* toy `E_mix` and its *exact* coset
  decomposition; the deployed statement names concentration as a hypothesis and
  then proves it insufficient. The `1,045,396.58`-bit dead margin is cited, not
  invoked.
- **HARD BOUNDARY (b).** The `d>w` tail of `E_mix` is the disjoint-PTE count
  `D_d` whose uniform-in-`d` asymptotic law `D_d ~ binom(N,d)binom(N-d,d)Q^{-w}`
  is the named open step of PR `#448` (scottdhughes, B1 bridge). Not proved or
  claimed here; cited as the adjacent controller of `E_mix^{dep}`.
- **`#475` / `#467`.** Extends both: `#475`'s single index-3 bound becomes a
  25-point ladder with an exact per-coset refinement and a proved ceiling;
  `#467`'s "two heavy orbits" observation is explained (per-orbit phase
  resonance) and shown *not* to be coset-exploitable.
- **`#465` (scottdhughes).** Its major-arc = small-value-set law is credited and
  used; this packet is the mixed-`w=2` regime where that law is weakest (folding
  caps `k` at `~n/2`; the heavy amplifier is global, not small-`k`).
- **`#412` concentration floor.** The twist-orbit machinery is existing input;
  the exact per-coset (Galois-rational) refinement and the `sqrt(index)` ceiling
  are the new quantitative content.

### Nonclaims

This packet does **not** prove:

```text
U(1116048) <= B* or any adjacent safe row;
the raw or masked signed-e_m inverse at KB-MCA;
def:q-row-atom / prob:row-sharp-q;
a deployed mixed collision-energy bound;
the disjoint-PTE count asymptotic law (#448);
any concentration statement in the deployed large-lambda/large-index corner.
```

No faithful-to-scope counterexample was found; the deployed inverse remains a
proof-method wall. What is newly *proved* is that the mixed twist-orbit coset
structure is not the tool that breaches it.

## 7. Reproduce

```bash
ulimit -v 2097152
python3 experimental/scripts/verify_kb_mixed_orbit_index_ladder.py
# RESULT: PASS (846/846 checks; tampers 17/17), exit 0, about 17 seconds
```
