Continues PR #495 (Johnson-scheme Delsarte LP saturation) and PR #480 (two-shell
wall §5).  Deploys the named non-LP next lever: the modular `F_p`-nullity certificate.

# CAP25 v13 raw: the modular `F_p`-nullity lever on the M31 two-shell cell is pair-uniform — it eliminates 0 of the 3,254,358 LP survivors, but forces `k<=760` on every regular realizer (8305 pairs)

Status per claim:
`PROVED` (the exact §5 nullity mechanism restated with every object pinned; the
grid `3,254,885` and the #495 surviving load `3,254,358` reproduced; the raw
`F_p`-nullity floor `L0-(n-w)=14,747,511` is **pair-uniform** and therefore
eliminates **0** pairs by itself; the no-collision lemma; the Class-I
integer-multiplicity forcing and the sharper Seidel bound `k<=760`, an exact
`8305`-pair structural elimination; the deployed sound elimination over the
unrestricted family class is exactly `0`) /
`PROVED-AT-TOYS` (soundness gates on the faithful `p=31,n=8`, all `62` exhaustive
`p=127,n=16` families incl. the size-`23` maximum, and the `p=127,n=32` size-`17`
witness; a direct `F_p`-nullity `=` integer-multiplicity demonstration on the
actual size-`23` Seidel matrix) /
`MEASURED` (the single-eigenvalue inclusion-moment cut is vacuous through `t=6`) /
`OPEN` (the deployed two-shell cell; the `3,254,358` survivors are
`F_p`-nullity-consistent; SDP / realizability is the only remaining lever).

**Verifier:** `experimental/scripts/verify_m31_band_nullity_certificate.py`
(zero-argument, stdlib-only; `RESULT: PASS (49/49 checks)`; ~90 s; 13 corruption
self-tests). **Data:**
`experimental/data/cap25_v13_m31_band_nullity_certificate.json`.

## 0. Result

PR #480 reduces every two-shell family above `B*` in the Mersenne-31 list row to
one of `3,254,885` integral-ratio pairs `(k,t)`; PR #495 proves the full
Johnson-scheme Delsarte LP saturates, eliminating exactly `527` and leaving
`3,254,358` LP-feasible pairs. Its named non-LP lever was the enormous modular
`-k` `F_p`-nullity of #480 §5. This note deploys it exactly.

```text
deployed:
  p=2^31-1=2147483647,  n=2^21=2097152,  m=981129,  w=67447,
  B*=2^24-1=16777215,   L0=B*+1=2^24=16777216=8n.

grid pairs                                         3254885
Johnson-LP survivors  (#495 load, reproduced)      3254358
F_p nullity floor  L0-(n-w) = 7n+w                 14747511  (pair-uniform)
raw §5 certificate eliminations                          0
deployed sound eliminations (unrestricted class)         0
Class-I (regular/integer-spectrum) k-bound              760   (#480 had 774)
Class-I structural eliminations  (k in 761..774)      8305
```

The headline is a precise **null**: the `F_p`-nullity floor is the *same integer*
`14,747,511` for every one of the `773` `k`-rows, so used raw it cannot separate
any two survivors. Every attempt to sharpen it into a pair-dependent constraint
either (i) collapses to an already-known LP/Seidel inequality, (ii) is vacuous
(the inclusion-moment cut), or (iii) is sound **only** for regular / integer-
spectrum realizers, where it does bite (`k<=760`). The unrestricted cell is
untouched. This is the exact wall that pushes to SDP / realizability.

## 1. The §5 nullity mechanism, every object pinned  `PROVED`

Let `F` be a size-`L` family of `m`-subsets in one depth-`w` power-sum fiber of
the M31 domain `D` (`|D|=n`), with two exchange distances `e1<e2`. Objects:

```text
X    : the L x n 0/1 incidence matrix (row = support indicator).
A    : the L x L 0/1 adjacency matrix joining the pairs at distance e1
       (symmetric, zero diagonal — a graph on the L supports).
t=e2-e1,  k=e2/t.
M=A+kI = t^{-1} X X^T + (e2-m) t^{-1} J.                        (1.1)
```

**Integral ratio and `k`.** (1.1) puts `col(M) ⊆ col(X)`, so `rank_R M <=
rank_R X <= n`. At `L=L0>n`, `M` is singular, `-k` is an eigenvalue of the
integral matrix `A`, hence `k∈Z`, `2<=k<=774`, `e1=(k-1)t`, `e2=kt` (#480 §2–3).

**Where `14,747,511` comes from.** All rows of `X` share their first `w` power
sums and their weight mod `p`. The `(w+1)×n` Vandermonde `V=(x^j)_{j=0..w,\,x∈D}`
has rank `w+1` (distinct nodes, `n>=w+1`), and `V X^T = c·1^T` for a fixed column
`c`. Hence the rows of `X` lie in a coset of `ker V`, and

```text
rank_Fp X <= n-w = 2,029,705.                                  (1.2)
```

`m,t≠0 mod p`, so (1.1) holds over `F_p`, and `col(M)⊆col(X)` gives
`rank_Fp(A+kI) <= n-w`. At `L=L0` the eigenvalue `-k` therefore has geometric
multiplicity over `F_p` at least

```text
L0-(n-w) = 16777216 - 2029705 = 14,747,511 = 7n+w.             (1.3)
```

**The integral-ratio pair `(k,t)`** parameterizes the shell scale: it fixes both
distances `e1=(k-1)t`, `e2=kt`, hence the two centered inner products
`a=1-e1/r`, `b=1-e2/r` with `r=m(n-m)/n`, and the target row `-k` of `A`. The
`3,254,885` grid pairs are all `(k,t)` with `2<=k<=774` surviving #480's Newton
(`e1>=w+1`) and centered-radius (`e1<=522118`, `e2<=m`) cuts (§4 below reproduces
the grid; the verifier regenerates it and both endpoint rows).

**Reproducing the #495 load.** The verifier runs the exact Johnson-scheme
Delsarte LP (normalized Eberlein eigenvalues, machine-checked against brute-force
`J(6,3),J(7,3),J(8,3)`) over the whole grid through eigenspace `j<=3`: it
eliminates `527` pairs (`187` at `j<=2`, set-identical to #481's closed form;
`340` at `j=3`), all with `e1∈[521834,522118]`, leaving `3,254,358`. Its
canonical eliminated-set SHA-256 and the four column checksums equal #495's to
the byte.

## 2. The raw floor is pair-uniform — it eliminates 0  `PROVED`

The floor (1.3) is `L0-(n-w)`, a fixed integer that **does not depend on**
`(k,t)`: it is `14,747,511` for all `773` `k`-rows and all `3,254,358` survivors.
A pair-uniform lower bound cannot distinguish one grid pair from another, so the
§5 nullity certificate, applied as a constraint on `(k,t)`, eliminates exactly
`0` pairs. (The verifier records `distinct_floor_values_over_grid = 1`.)

Everything below is an attempt to couple (1.3) to *pair-dependent* spectral data.
The obstacle is that the actual spectrum of `A` depends on the (unknown) family,
not on `(k,t)` — which is exactly why #495's LP, quantifying over all inner
distributions, saturated.

## 3. No-collision lemma and the collision dichotomy  `PROVED`

Write `S=2A-(J-I)` (the Seidel matrix: zero diagonal, `±1` off-diagonal). Then
`2M-J = S+(2k-1)I` has `col ⊆ col(X)`, so over `R` the eigenvalue `-(2k-1)` of
`S` has multiplicity `>= L0-n`, and over `F_p` nullity `>= L0-(n-w)=14,747,511`.
Two identities are **family-independent**:

```text
tr S = 0,        tr S^2 = L0(L0-1) = 281,474,959,933,440.       (3.1)
```

**No-collision lemma.** Let `T` be an integer symmetric matrix all of whose
eigenvalues are integers of absolute value `< p/2`, and `λ` an integer with
`|λ|<p/2`. Then `v_{x-λ}(χ_T mod p) = v_{x-λ}(χ_T over Q)`: the cofactor
`g=χ_T/(x-λ)^{μ}` has `g(λ)=∏(θ_i-λ)` with each factor a nonzero residue of
absolute value `< p`, so, `p` prime, `g(λ)≢0 mod p`. Hence the `F_p` algebraic
multiplicity of `λ` equals its integer multiplicity `μ`, and (geometric `<=`
algebraic over `F_p`) the `F_p` nullity of `T-λI` is `<= μ`.

For a Seidel matrix `|eigenvalue| <= L0-1`, so `2(L0-1)=33,554,430 < p`: the
lemma's hypothesis is automatic for any **integer-spectrum** realizer. This
splits every hypothetical realizer of a grid pair:

- **Class I** (integer Seidel spectrum; e.g. regular two-graphs, association-
  scheme and strongly-regular realizers). By the lemma the `F_p` nullity of
  `S+(2k-1)I` is `<= M`, the integer multiplicity of `-(2k-1)`; the rank bound
  makes it `>= 14,747,511`; hence `M >= 14,747,511`. Then (3.1) with
  Cauchy–Schwarz on the `<= L0-M` remaining eigenvalues gives
  `(2k-1)^2 <= (L0-1)(L0-M)/M`. Since the bound decreases in `M`, plugging the
  floor `M=14,747,511`,

  ```text
  (2k-1)^2 <= (L0-1)(n-w)/(7n+w) = 34,052,797,171,575 / 14,747,511 < 1521^2,
  1519^2 <= that < 1521^2   ⇒   2k-1 <= 1519   ⇒   k <= 760.     (3.2)
  ```

  (#480 used the weaker real floor `M>=7n`, getting `1547`, `k<=774`.) So **no
  Class-I family realizes any pair with `k∈{761,…,774}`** — exactly `8305` grid
  pairs (`8299` of them still LP-surviving). `PROVED` for Class I.

- **Class II** (irrational Seidel spectrum). Take the minimal consistent
  scenario: real multiplicity `μ=L0-n=7n` (real rank exactly `n`) and `F_p`
  nullity equal to the floor `7n+w`. The excess `w` is produced by a mod-`p`
  collision `(x+2k-1)^{w} | g(x) mod p`, i.e. `p^{w} | g(-(2k-1))`, where
  `g(-(2k-1))=∏(θ_i+2k-1)` runs over the `~n` non-`(-k)` eigenvalues. There is no
  **size** obstruction: `|g(-(2k-1))|` can be as large as `(L0-1)^{n}=2^{~5·10^7}`,
  vastly exceeding `p^{w}=2^{~2.1·10^6}`, so the required divisibility is
  arithmetically unforced-but-unobstructed. Thus for every grid pair the integer
  data `(μ=7n, \text{ collision-excess }=w)` is consistent with every derived
  constraint, and the certificate **eliminates no pair**. `PROVED` (a
  non-elimination; it does not assert any family exists).

**Deployed sound elimination over the unrestricted family class: `0`.** The raw
floor is null (§2); the Class-I bound does not apply to Class II; and Class II is
consistent for every pair. The `3,254,358` survivors are unchanged.

## 4. The inclusion-moment cut is vacuous through `t=6`  `MEASURED`

The single-forced-eigenvector inclusion-matrix inequality (from the `-k`
eigenvector of `A`, #495 §4) is

```text
C(m,t) - k·C(m-e1,t) + (k-1)·C(m-e2,t) >= 0.                    (4.1)
```

The verifier evaluates the minimum of (4.1) over the whole grid for `t=2,…,6`:
it is `+2,277,955,125 >= 0`. The cut fires nowhere; extending past #495's
`t∈{2,3,4}` adds nothing. This is the modular constraint that uses only the
extreme eigenvalue `-k`; §3 is what couples the whole eigenvalue column, and it
is only nonvacuous inside Class I.

## 5. Soundness gates  `PROVED-AT-TOYS`

A constraint that eliminates a realizable family is worthless. The verifier
reconstructs the faithful twin-coset toys and applies the §3 Class-I predicate
and the §4 inequality to each realizable two-shell family with its own toy
constants; **none is eliminated**:

```text
p=31,  n=8,  m=4, w=2 :  1 realizable family (size 2)        -> vacuous, kept
p=127, n=16, m=8, w=1 :  62 families, exhaustive;
                          5 have integral ratio and size > n-w=15 and so
                          engage the Class-I Seidel bound (incl. the size-23
                          maximum, shells {2,4}, k=2)         -> none eliminated
p=127, n=32, m=15,w=2 :  the size-17 witness, shells {7,8}   -> vacuous, kept
```

**p-regime, handled honestly.** The Class-I bound is sound exactly under the
no-collision lemma, whose hypothesis is `2(N-1) < p` at the operative size `N`.
At deployment `2(L0-1)<p` with a `64×` margin. At every *engaging* toy family
`2(L-1) <= 44 < 127 = p`, so the toys sit in the **same** no-collision regime,
not a different one; a genuine regime change would need a toy family of size
`>= (p+2)/2 = 65`, which none reach. The engaging families satisfy (3.2) at their
own size with room to spare (e.g. size-23: `q^2=9 <= (L-1)(L-M_lo)/M_lo=41.25`).

**Direct mechanism demonstration.** The verifier builds the actual `23×23`
Seidel matrix `S` of the size-23 maximum family and computes, by exact
elimination, `null_Q(S+3I)=14` and `null_{F_127}(S+3I)=14` — **equal**, the
`F_p` nullity faithfully reporting the integer multiplicity (`>=` the toy floor
`L-(n-w)=8`). At the tiny prime `p'=3`, where `2(L-1)=44 >= 3` breaks the margin,
the nullity jumps to `15`: a real mod-`p` collision, exactly the Class-II
phenomenon (3) controls. So the lemma is exhibited from both sides on a
realizable maximum family.

## 6. Wall and nonclaims

The residual `3,254,358` pairs are `F_p`-nullity-consistent. The modular lever is
**pair-uniform** and adds nothing over the LP on the unrestricted cell; its only
nonvacuous consequence is the Class-I structural bound `k<=760`. Combined with
#480 §6 (no quasi-symmetric design, no affine-binary/two-weight-code, no
common-core all-pairs construction fits the cell) and §3 here, the structural
narrowing is precise: a surviving pair with `k∈{761,…,774}` (the `8305`-pair
band) can be realized **only** by an irregular, irrational-Seidel-spectrum family
whose `-(2k-1)` real multiplicity is below `14,747,511` and which therefore
admits a specific mod-`p` collision of up to `w=67,447` conjugate eigenvalues
onto `-(2k-1)`; a surviving pair with `k<=760` may additionally be Class-I
(integer-spectrum), in which case its real multiplicity is `>=14,747,511` with no
collision. Neither branch is an `(k,t)`-elimination. The natural remaining levers
are therefore genuinely
non-LP and non-modular: a positive-semidefinite (SDP / three-point) bound, or a
direct realizability / clique argument. This matches #495's own diagnosis.

Nonclaims:

- This packet does **not** eliminate any of the `3,254,358` LP survivors, does
  not pay the two-shell cell `|F|<=B*`, and constructs no family above `B*`.
- The Class-I bound `k<=760` and its `8305`-pair elimination are sound **only**
  for integer-Seidel-spectrum (regular / scheme) realizers; they say nothing
  about irregular realizers, and do not reduce the OPEN survivor count.
- "Deployed sound elimination `= 0`" is a proof that this lever fails to
  eliminate, **not** a claim that any surviving pair is realizable.
- The no-collision lemma is a sufficient condition; the size-23 demonstration is
  `PROVED-AT-TOYS`, not a deployed theorem.

## 7. Reproduce

```text
ulimit -v 2097152; python3 experimental/scripts/verify_m31_band_nullity_certificate.py
```

The verifier pins the §5 constants, brute-force-certifies the Eberlein
eigenvalues, regenerates the `3,254,885` grid and the `527`/`3,254,358` LP split
(cross-checked to #495's SHA-256 and checksums), proves the floor pair-uniform,
recomputes the baseline `k<=774` and Class-I `k<=760` bounds and the `8305`-pair
count, confirms the inclusion-moment vacuity through `t=6`, runs the toy
soundness gates and the size-23 `F_p`-nullity demonstration, replays the JSON
packet, and rejects 13 independent corruptions.
