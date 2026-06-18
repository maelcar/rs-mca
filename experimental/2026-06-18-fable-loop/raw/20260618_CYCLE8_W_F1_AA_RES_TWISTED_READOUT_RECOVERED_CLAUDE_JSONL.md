Permission to run code was denied, so I verified the algebra by hand (including reproducing the Cycle 7 `F_5` example exactly). I did not write files since this harness has no write tool and `input_project` is read-only; I give Codex a complete verification spec inline.

Final classification: BANKABLE_LEMMA

## Statement

Setup as in the wall: `B=F_p`, `F=F_{p^2}`, `tau` the nontrivial Galois automorphism, `D subset B`, `n=|D|`, `k`, balanced `t=sigma`, `a=k+t=s_delta`. `E in F[X]` has `deg E=t`, nonzero on `D`. Separated case: `gcd(E,E^tau)=1`, so `Ehat=lcm(E,E^tau)=E*E^tau in B[X]` has `deg Ehat=2t`. Anchors `w=w0+alpha*w1`, `w_i:D->B`, `P_i=interp_S(w_i) in B[X]`, `deg P_i < a=k+t`. CRT class `theta in B[X]/Ehat` with `theta==alpha mod E`, `theta==alpha^tau mod E^tau`. Twisted readout

```text
T_theta(S) = [P0]_Ehat + theta*[P1]_Ehat  in B[X]/Ehat.
```

Lemma (Twisted-Readout Weil-Restriction Structure Law). In the separated case:

(1) Weil-restriction isomorphism. Reduction-mod-`E`
```text
pi : B[X]/Ehat  -->  F[X]/E,   pi([g]) = [g]_E
```
is a ring isomorphism, and `pi(theta)=alpha`. (`theta` is nonconstant in `B[X]/Ehat` iff `alpha notin B`, i.e. always in the genuinely twisted case.)

(2) The twisted readout is the genuine residue, repackaged.
```text
pi( T_theta(S) ) = [interp_S(w)]_E,   hence   T_theta(S) = pi^{-1}( [interp_S(w)]_E ).
```
Therefore, for any family of supports,
```text
#{ distinct T_theta(S) } = #{ distinct [interp_S(w)]_E in F[X]/E }.
```
The distinct-value count of the twisted readout equals exactly the residue-line value count of the arbitrary-anchor datum `(E, Bnum, w)` over `F`. It is governed by `q_line=p^2`, not by `q_gen=p`; the readout introduces no base-field collapse and no extra spreading.

(3) Exact commutator (isolation of the Cycle 7 failure). With the degree-`<2t` representative of `theta` and `L_S=prod_{d in S}(X-d)` (`deg L_S=a`),
```text
theta*interp_S(w1) - interp_S(theta*w1) = L_S * R_S,   deg R_S <= 2t-2,
```
so
```text
T_theta(S) = [ interp_S(w0+theta*w1) ]_Ehat + [ L_S * R_S ]_Ehat.
```
The correction `[L_S R_S]_Ehat` is generally nonzero; this is precisely why `theta` cannot be absorbed into the pointwise word, yet it does not obstruct the count because of (2).

(4) Collision law. On `a=k+t` supports,
```text
T_theta(S)=T_theta(S')  <=>  [interp_S(w)]_E=[interp_S'(w)]_E
                          <=>  interp_S(w)-interp_S'(w) in E*F_{<k}[X].
```
Thus the twisted-readout collision relation is identical to the Cycle 6B same-slope kernel; the twist relabels but does not change it.

## Proof notes (hand-verified)

- pi is a ring hom since `E | Ehat`. Injective: if `g in B[X]`, `deg g<2t`, `E|g` in `F[X]`, apply `tau` (fixes `g`, sends `E` to `E^tau`) to get `E^tau|g`; coprimality gives `Ehat|g`, forcing `g=0`. Both sides have `p^{2t}` elements, so pi is bijective, hence a ring iso. `pi(theta)=[theta]_E=[alpha]_E=alpha`.
- theta is Galois-fixed: applying `tau` to its two congruences swaps them, so `tau(theta)` solves the same CRT system; uniqueness gives `tau(theta)=theta`, i.e. `theta in B[X]/Ehat`.
- (2): `interp_S(w)=P0+alpha*P1` because `D subset B` gives base-field Lagrange coefficients (banked Cycle 1). Apply pi: `pi(T_theta(S))=[P0]_E+alpha*[P1]_E=[P0+alpha*P1]_E=[interp_S(w)]_E`.
- (3): `theta*P1` and `interp_S(theta*w1)` agree at every `d in S` (both equal `theta(d)w1(d)`), so `L_S` divides the difference. Degrees: `deg(theta*P1) <= (2t-1)+(k+t-1)=k+3t-2`, subtract `deg L_S=k+t` to get `deg R_S<=2t-2`.
- (4): equal pi-images iff equal residues mod `E` (pi injective); on `a`-supports `deg(interp_S(w)-interp_S'(w))<k+t` and `deg E=t` give quotient degree `<k` (Cycle 6B).
- Cycle 7 reconciliation: `p=5`, `Ehat=X^2+1` (`t=1`, `k=1`, `E=X-i` over `F_25`), `S={0,1}`, `w1=(0,1)`. Then `P1=X`, `theta=X`, `theta*P1=X^2`, `interp_S(theta*w1)=X`, commutator `X^2-X=L_S` with `R_S=1` (`deg 0=2t-2`); mod `Ehat`: `-1-X`, matching the audit's `-1` vs `X`. Consistent.

## Why this is honest, not a forbidden repeat

It does not absorb `theta` into `w0+theta*w1` (the absorption is written with its explicit nonzero correction and the count is done through pi, not through the word). It does not import `thm:exactcount`/`thm:rigidcyclo` through a false base datum. It is not merely the same-slope kernel: it adds the exact iso (2) and commutator (3). It makes no claim about `q_chal`, MCA, list/line decoding, or protocol savings. The count in (2) lands on `F[X]/E` over `q_line`, so it explicitly refuses the `q_gen` collapse that would have closed the wall illegitimately.

## Source dependencies

- `slackMCA_v3.tex` `def:residue` (residue-line datum; the count in (2) is its `Lambda^{NC}_{t,delta}` value set for `(E,Bnum,w)`), `thm:normalform` (residue-line normal form), `prob:perfiber` (the residual count is a per-fiber collision instance), `rem:aper` (separated vs quotient-periodic), `conj:B` (the unresolved `n^{1+o(1)}` prediction the residual count feeds).
- Banked: F1 Arbitrary-Anchor Paired Base Readout (Cycle 1), Slope-Uniqueness/Dimension caveats (Cycle 2, `Ehat` over full `E`; dim `2 deg Ehat`), Balanced Noncontainment Subset Lemma (Cycle 3), `a=s_delta` (Cycle 4), Kernel-is-not-the-wall (Cycle 6B), Twisted Readout Transfer Boundary (Cycle 7).
- `thm:rigidcyclo`/`thm:exactcount` are NOT used (they remain unavailable for arbitrary anchors).

## Field ledger

- `q_gen=p` = `B=F_p`: field of `D`, `w0`, `w1`, `Ehat`, `theta`, and the quotient `B[X]/Ehat`.
- `q_line=p^2` = `F=F_{p^2}`: field of `E`, `Bnum`, slopes `z`, and the genuine residue `[interp_S(w)]_E in F[X]/E`. The value count (2) is a `q_line` count.
- `q_chal`: unused; no protocol/challenge denominator claimed.

## Parameter ledger

- `n=|D|`, `k=rho n`, `a=ceil((1-delta)n)`, `sigma=a-k`, balanced `t=sigma`, `a=k+t=s_delta`.
- `deg E=t`, `deg Ehat=2t` (separated), quotient `B`-dimension `2t`, isomorphic as a ring to `F[X]/E` of `F`-dimension `t`.
- `deg R_S <= 2t-2`. First finite test `t=sigma=2`: `deg Ehat=4`, `deg R_S<=2`.
- No quotient-order / interleaving / list arity used.

## Residual wall (what is still open, stated sharply)

The lemma collapses `W-F1-AA-RES-TWISTED-READOUT` back onto its honest core: bound `#{ distinct [interp_S(w)]_E : S an a-subset on the bad line }` in `F[X]/E`. This is exactly the arbitrary-anchor `Lambda^{NC}_{t,delta}` count of `prob:perfiber`, with no twist artifact remaining. The genuinely missing invariant is now:

```text
W-F1-AA-RES-RESIDUE-COUNT:
above corrected reserve eta=sigma/n, bound the F-residue value count
S -> [interp_S(w0)+alpha*interp_S(w1)]_E  by n^{1+o(1)},
for arbitrary base anchors w0,w1, aperiodic E (separated from E^tau).
```

This is sharper than the twisted formulation (the twist is now provably inert) and is the clean entry point to `conj:B` for arbitrary anchors.

## What Codex should bank / test next

Bank: the lemma above (iso (1), count identity (2), commutator (3), collision law (4)) as BANKABLE_LEMMA, and `W-F1-AA-RES-RESIDUE-COUNT` as the sharpened residual wall.

Verification harness (must compute `T_theta` directly; compare to `interp_S(w0+theta*w1)` only as a negative control):

1. `p=7`; `F=F_p[a]/(a^2-NR)`, `NR` a nonresidue; `tau:a->-a`. `D=B=F_7`, `n=7`, `t=sigma=2`, `k=2`, `a=k+t=4`.
2. Random `E=X^2+c1 X+c0 in F[X]` with `c1` or `c0` having nonzero `a`-part (so `E notin B[X]`), nonzero on `D`, and `gcd(E,E^tau)=1` (separated). Set `Ehat=E*E^tau in B[X]` (`deg 4`), `Bnum` random nonzero `deg<2`.
3. Compute `theta in B[X]/Ehat` by CRT (`theta==alpha mod E`, `alpha^tau mod E^tau`); assert `theta` has nonconstant representative and `[theta]_E==alpha`.
4. Random `w0,w1:D->B`. Over all `a=4`-subsets `S`: `P_i=interp_S(w_i)`; `Tval=([P0]_Ehat+theta*[P1]_Ehat) mod Ehat`; `Rres=[P0+alpha*P1]_E in F[X]/E`.
5. Assert `pi(Tval)=Rres` (reduce `Tval` mod `E`), and that `#distinct Tval == #distinct Rres`. (Confirms (1),(2).)
6. Commutator: assert `theta*P1 - interp_S(theta*w1)` is divisible by `L_S` with quotient degree `<=2t-2=2`; assert `Tval == [interp_S(w0+theta*w1)]_Ehat + [L_S*R_S]_Ehat`, and exhibit some `S` where `[L_S*R_S]_Ehat != 0` (negative control proving non-absorption). (Confirms (3).)
7. Collision: for equal-`Tval` pairs assert `interp_S(w)-interp_S'(w) in E*F_{<k}[X]`. (Confirms (4).)
8. Report the residue count vs `q_line=49` to seed `W-F1-AA-RES-RESIDUE-COUNT` data (do not claim a bound from one instance).
