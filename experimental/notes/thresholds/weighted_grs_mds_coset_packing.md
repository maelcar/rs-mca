# Weighted [2K,K,K+1] MDS coset packing at the deployed Grand List row

## Status

`PROVED` / `EXACT CONSTANTS` / `DOES NOT CLOSE THE DEPLOYED TARGET`.

This note proves an unconditional support-packing upper bound for every coset
of a weighted `[2K,K,K+1]` GRS code. The proof uses only the MDS minimum
distance and elementary subset packing. Its deployed integer envelope is much
too large to prove the pending one-row Grand List ceiling.

The companion verifier is
`experimental/scripts/verify_weighted_grs_mds_coset_packing.py`. It uses only
the Python standard library and contains no `assert` statements.

## Source anchors and novelty boundary

The publication base is
`origin/main@9262f63cf093a7510a2df435f220390f59e2bcd5`.

The following existing notes fix the surrounding notation and ledger:

- `experimental/notes/l1/l1_syndrome_catalecticant_shells.md` identifies exact
  one-row list shells with fixed-syndrome error shells;
- `experimental/notes/m1/m1_johnson_anticode_toolkit.md` records the generic
  support anticode lemma specialized below;
- `experimental/notes/l2/affine_interleaved_shell_compression.md` derives the
  deployed base-field one-row target `T`; and
- `experimental/notes/thresholds/projective_line_lift_feasibility_wall.md`
  records the stronger global projective-line realization wall that remains
  open.

The proof here is self-contained. The new package is the exact
`[2K,K,K+1]` coset-shell specialization, its all-shell sum, and the corrected
deployed arithmetic. It neither replaces nor solves the global projective-line
wall.

## Object and field ledger

```text
object:                 base-field one-row Hamming list
code:                   linear [2K,K,K+1] MDS code
deployed realization:   weighted GRS_K(H,v) over F_p
evaluation set:         2K distinct base-field points
list radius:            K-sigma (closed)
agreement threshold:    K+sigma (closed)
list/base field:        F_p
challenge denominator:  p^6, only in the downstream target T
MCA/CA/line object:      none
first-match catalogue:  none
extension-field payment:none
```

Let `C` be a linear `[2K,K,K+1]` code over a field `F`, where `K` is even,
and let `P` be a full-rank parity-check matrix with kernel `C`. For a syndrome
`s`, define

\[
  \mathcal E_s:=\{e\in F^{2K}:Pe=s\},\qquad
  L_{\le t}(s):=|\{e\in\mathcal E_s:\operatorname{wt}(e)\le t\}|.
\]

If `y` has syndrome `s`, the map `c -> y-c` is a bijection from codewords in
the closed radius-`t` ball about `y` to the displayed error set. Thus this is
exactly the one-row list size. For

\[
  C=\operatorname{GRS}_K(H,v)
   =\{(v_xf(x))_{x\in H}:\deg f<K\},
\]

distinct evaluation points and nonzero multipliers give the required
`[2K,K,K+1]` MDS parameters. No other GRS structure enters the proof.

## Primary theorem

**Theorem (MDS coset packing).** Let `K >= 44` be even and let
`1 <= sigma < K/2`. For every syndrome `s` of a linear
`[2K,K,K+1]` MDS code,

\[
\boxed{
 L_{\le K-\sigma}(s)
 \le
 1+\sum_{\delta=\sigma}^{K/2-1}
 \frac{\binom{2K}{K-2\delta}}
      {\binom{K-\delta}{K-2\delta}}
 <
 1+\frac{11}{10}
 \frac{\binom{2K}{K-2\sigma}}
      {\binom{K-\sigma}{K-2\sigma}} .
}
\tag{1}
\]

In particular, (1) applies to every weighted `[2K,K,K+1]` GRS coset.

### Proof: the low branch

Two distinct errors in the same syndrome class differ by a nonzero codeword,
so

\[
  \operatorname{wt}(e-e')\ge K+1.                    \tag{2}
\]

If both errors have weight at most `K/2`, then

\[
  \operatorname{wt}(e-e')
  \le \operatorname{wt}(e)+\operatorname{wt}(e')\le K,
\]

contradicting (2). Hence the union of all exact shells of weight at most
`K/2` contains at most one error. This is the `1` in (1).

### Proof: one high shell

Fix

\[
  \sigma\le\delta\le K/2-1,\qquad
  w:=K-\delta,\qquad r_\delta:=K-2\delta>0.
\]

For two distinct weight-`w` errors in the same syndrome class, with supports
`E` and `E'`, equations (2) and
`supp(e-e') subseteq E union E'` give

\[
  K+1\le |E\cup E'|=2w-|E\cap E'|.
\]

Therefore

\[
  |E\cap E'|\le 2w-K-1=K-2\delta-1=r_\delta-1.       \tag{3}
\]

No `r_delta`-subset can consequently lie in two supports in this shell. If
`M_{K-delta}(s)` is the number of its errors, double-counting those subsets
gives

\[
  M_{K-\delta}(s)\binom{K-\delta}{K-2\delta}
  \le \binom{2K}{K-2\delta}.                           \tag{4}
\]

Summing (4) over all high weights from `K/2+1` through `K-sigma` and adding
the low branch proves the first inequality in (1).

### Proof: geometric domination

Write

\[
 B_\delta:=
 \frac{\binom{2K}{K-2\delta}}
      {\binom{K-\delta}{K-2\delta}}
 =\frac{(2K)!\,\delta!}{(K+2\delta)!\,(K-\delta)!}.
\]

Adjacent terms satisfy

\[
 \frac{B_{\delta+1}}{B_\delta}
 =\frac{(\delta+1)(K-\delta)}
        {(K+2\delta+1)(K+2\delta+2)}.                 \tag{5}
\]

After clearing denominators, the assertion that (5) is less than `1/11` is

\[
\begin{aligned}
 &(K+2\delta+1)(K+2\delta+2)
   -11(\delta+1)(K-\delta)\\
 &=15\left(\delta-\frac{7K}{30}\right)^2
   +\frac{11K^2}{60}+17\delta-8K+2>0.                 \tag{6}
\end{aligned}
\]

For `K >= 44`, the part `11K^2/60-8K+2` is already positive: it is increasing
in this range and equals `74/15` at `K=44`. Thus every ratio in (5) is
strictly below `1/11`. Extending the finite tail to an infinite geometric
series gives

\[
 \sum_{\delta=\sigma}^{K/2-1}B_\delta
 <B_\sigma\sum_{j\ge0}11^{-j}
 =\frac{11}{10}B_\sigma,
\]

which proves the second inequality in (1). \(\square\)

## Correct integer branch names

Put

\[
 N_\sigma:=\binom{2K}{K-2\sigma},\qquad
 D_\sigma:=\binom{K-\sigma}{K-2\sigma}.
\]

The high-shell count is an integer strictly below
`11 N_sigma/(10 D_sigma)`. Its integer envelope is therefore

\[
 U_{\mathrm{high}}
 :=\left\lfloor\frac{11N_\sigma-1}{10D_\sigma}\right\rfloor
 =\left\lceil\frac{11N_\sigma}{10D_\sigma}\right\rceil-1. \tag{7}
\]

The complete list includes the possible low-branch error, so the full bound is

\[
 U_{\mathrm{list}}:=U_{\mathrm{high}}+1
 =\left\lceil\frac{11N_\sigma}{10D_\sigma}\right\rceil.   \tag{8}
\]

`U_high` is not the full list bound; `U_list` is.

## Deployed constants and target comparison

The deployed base-field row is

```text
p       = 2^31-2^24+1 = 2,130,706,433,
n       = 2^21        = 2,097,152 = 2K,
K       = 2^20        = 1,048,576,
sigma                  = 67,471,
m       = K+sigma      = 1,116,047,
t       = n-m=K-sigma  = 981,105.
```

Here `p>n` and `n` divides `p-1`, although the packing proof needs only a
weighted GRS evaluation set of `n` distinct points. The downstream all-arity
compiler retains the literal challenge denominator `p^6`:

```text
B* = floor(p^6/2^128)
   = 274,980,728,111,395,087,

T  = floor(((B*+1)(p-n+m)-1)/p)
   = 274,854,110,496,187,592.
```

Thus the pending sufficient statement is
`L_{<=981105}(s) <= T` for every base-field syndrome.

For the first packing term,

\[
 r_\sigma=K-2\sigma=913{,}634,
\]

and

\[
 \frac{N_\sigma}{D_\sigma}
 =\frac{\binom{2{,}097{,}152}{913{,}634}}
        {\binom{981{,}105}{913{,}634}}.
\]

The exact envelopes (7)-(8) both have `517,030` decimal digits. Their
fingerprints are

```text
U_high = 904729988050617145947819275983...
         ...447267321596643140059698004080,

U_list = 904729988050617145947819275983...
         ...447267321596643140059698004081.
```

In particular,

```text
U_list > T,
floor(U_list/T) has 517,013 decimal digits and begins
329167348604439498924431336018...
```

The comparison is a route failure, not a lower bound on the actual list. The
MDS packing theorem is correct, but its upper envelope is roughly
`3.29 * 10^517012` times the required one-row target. It therefore supplies
no deployed closure.

## Hostile-audit disposition

The source packet also contained an apolar/complete-intersection route. It is
deliberately excluded from this package because it is unnecessary for (1).
In particular:

- an affine degree-bounded primitive-pair count is only an ambient upper
  bound, not an exact homogeneous locator census; and
- exact Mobius deduplication requires its alternating signs. Deleting negative
  terms can give a coarse upper bound, but not the exact deduplicated count.

Neither statement is used by the theorem or verifier.

## Ledger impact and explicit nonclaims

The exact claim layer moved is narrow: every weighted `[2K,K,K+1]` GRS coset
now has the unconditional support-packing bound (1), with a replayed deployed
integer envelope. The exact next wall is unchanged: a stronger GRS-specific
global constraint is required to prove `L_{<=981105}(s) <= T`.

This note makes the following explicit nonclaims.

- No deployed one-row ceiling or all-arity Grand List closure is proved.
- No official score or leaderboard value moves.
- No exact locator census is claimed.
- No theorem for arbitrary `[n,K]` codes is claimed; the scope is
  `[2K,K,K+1]` MDS.
- No apolar or complete-intersection structural theorem is packaged.
- No received word with a large list is constructed, and no lower bound on an
  actual list follows from `U_list>T`.
- No Grand MCA, CA, line-decoding, first-match, or field-transfer claim is
  made.
- No stable paper TeX is changed.

## Replay

Run both modes and compare their output:

```text
python3 experimental/scripts/verify_weighted_grs_mds_coset_packing.py
python3 -O experimental/scripts/verify_weighted_grs_mds_coset_packing.py
cmp <normal-output> <optimized-output>
```

The canonical output file is
`experimental/data/certificates/weighted-grs-mds-coset-packing/verifier_output.txt`.
