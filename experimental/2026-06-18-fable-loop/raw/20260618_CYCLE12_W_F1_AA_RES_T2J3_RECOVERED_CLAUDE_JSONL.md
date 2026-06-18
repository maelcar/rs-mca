I have the full ledger, the source definitions (`def:residue`, `thm:normalform`, `prob:perfiber`, `conj:B`, `rem:aper`), the Cycle 9 locator‑quotient reduction, and the Cycle 11 `j=2` closed form. One constraint: code execution is disabled in this environment (the Jupyter tool was denied and there is no shell), so I derive everything analytically and ship the scanner as a spec rather than running it. I flag the numerics as pending.

---

## Classification: `EXACT_NEW_WALL`

(carrying an embedded `BANKABLE_LEMMA`: the `t=2,j=3` quotient closed form and the bad‑locus quadric with its leading coefficient. The slope bound itself is **not** reachable by the Cycle‑11 method and reduces to one precisely‑named missing invariant.)

---

## Exact statement

**Bankable structural part (rigorous).** In the regime
`B=F_p`, `F=F_{p^2}`, `D⊆B`, `w=w0+α w1` with `w0,w1:D→B`, `E∈F[X]` separated/aperiodic with `deg E=t=2` nonzero on `D`, `deg Bnum<2`, `[Bnum]_E≠0`, balanced `a=k+t`, `σ=t=2`, and `j=n−a=r−t=3` (so `a=n−3`, `k=n−5`, `deg Q_S≤2`), write `W=interp_D(w)=Σ W_m X^m`, top coefficients `W_{n-1},W_{n-2},W_{n-3}∈F`, and co-support `T=D\S` with `τ_i=e_i(T)`, `E_i=e_i(D)`. Then the locator quotient `W=L_S Q_S+I_S` has the closed form

```text
Q_S = W_{n-1}·X^2
    + (W_{n-2}+W_{n-1}E_1)·X
    + (W_{n-3}+W_{n-2}E_1+W_{n-1}(E_1^2-E_2))
    − τ1·( W_{n-1}X + W_{n-2}+W_{n-1}E_1 )
    + τ2·( W_{n-1} ).
```

For `D=F_p` (`E_1=E_2=0`) this collapses to

```text
Q_S = W_{n-1}(X^2 − τ1 X + τ2) + W_{n-2}(X − τ1) + W_{n-3}.
```

So `Q_S` is **affine in (τ1,τ2)=(e1(T),e2(T)) and independent of τ3=e3(T)**. This is the exact `j=3` analogue of Cycle 11's `Q_S=C(X−s_T)+C1`: the quotient sees one *more* co-support parameter (`τ2`) but still **not** the top one (`τ3`).

**Bad-line incidence equation (rigorous).** Set `A=F[X]/E` (`dim_F A=2`), wedge `∧:A×A→F` the `2×2` determinant, `W_E=[W]_E`, `B_E=[Bnum]_E`, `L_{D,E}=[L_D]_E`, `μ=[Q_S]_E`, `λ=[L_T]_E`. Since `E` is nonzero on `D`, `λ` is a unit with `N_{A/F}(λ)=∏_{d∈T}E(d)≠0`. A slope `z` exists for `T` iff

```text
Δ(T) := ( W_E·λ − L_{D,E}·μ ) ∧ ( B_E·λ ) = 0,
```

and then `z` is unique (Cycle 2). Using `N(λ)=det(M_λ)` and `λ=λ0−τ3` with `λ0=ξ3−τ1ξ2+τ2ξ` (`ξ=[X]_E` etc.):

```text
Δ = (W_E∧B_E)·( τ3^2 − Tr(λ0)τ3 + N(λ0) ) − ⟨μ,λ0⟩ + τ3·⟨μ,1⟩,
⟨x,y⟩ := (L_{D,E}x) ∧ (B_E y).
```

`Δ` is a **quadric surface in (τ1,τ2,τ3)∈A^3**, and

```text
[τ3^2] Δ = W_E ∧ B_E = [W]_E ∧ [Bnum]_E.
```

So, exactly as in Cycle 11, the coefficient of the *free top co-support parameter squared* is `∧([W]_E,[Bnum]_E)`; `Δ≡0` forces the global/tangent endpoint.

**Wall part (the new obstruction).** Cycle 11's bound `C2=O(n)` came **only** from solution-counting: at `j=2`, the bad locus is a conic in 2-dim co-support space, meeting `≈ C(n,2)/p = O(n)` subsets for `n≈p`, so trivially `C2=O(n)`. At `j=3` the bad locus is the quadric `Δ=0` in **3-dim** co-support space, meeting

```text
#{T : Δ(T)=0} ≈ C(n,3)/p ≈ n^2/6   (n=p),
```

which for `D=F_p` (`n=p`) is `Θ(n^2)=Θ(q_line)` — **the solution-counting bound is vacuous**. Hence the `t=2` line-incidence law has its **first genuine wall exactly at `j=3`**, and any nontrivial `C2` bound must come from *slope collapse*, not solution-counting.

---

## Proof / counterpacket data

Derivation of `Q_S` (rigorous): `deg I_S<a=n−3`, so the three top coefficients `X^{n-1},X^{n-2},X^{n-3}` of `W` come entirely from `L_S Q_S`. Matching them with `L_S=Σ(−1)^m e_m(S)X^{a−m}` gives `q_2=W_{n-1}`, `q_1=W_{n-2}+W_{n-1}e_1(S)`, `q_0=W_{n-3}+W_{n-2}e_1(S)+W_{n-1}(e_1(S)^2−e_2(S))`. Substituting `e_1(S)=E_1−τ1`, `e_2(S)=E_2−E_1τ1+τ1^2−τ2` (disjoint-union symmetric identities) yields the boxed form; the `W_{n-1}`-coefficient of `q_0` simplifies to `E_1^2−E_2−E_1τ1+τ2`. Independence from `τ3` is structural: only `e_1(S),e_2(S)` enter, which depend on `τ1,τ2` (and constants `E_i`) but never `τ3`. ∎

Incidence/`Δ`: `[I_S]_E∈F·B_E ⇔ [I_S]_E∧B_E=0` (true line characterization since `B_E≠0` in `dim 2`). From `L_T·I_S=L_T W−L_D Q_S` reduced mod `E`: `λ[I_S]_E=λW_E−L_{D,E}μ`, so `[I_S]_E∧B_E` scaled by the unit `λ` gives `Δ` above. The norm expansion `det(M_{λ0−τ3})=τ3^2−Tr(λ0)τ3+N(λ0)` and bilinearity of `⟨·,·⟩` give the displayed quadric and `[τ3^2]Δ=W_E∧B_E`. ∎

Why it is a wall, not a proof or a counterpacket:
- Not `PROOF`/`BANKABLE` of a `C2` bound — the only available bound is `C2≤#{Δ=0}=O(n^2)=Θ(q_line)`, vacuous for `n≈p`. The Cycle-11 collapse mechanism (slope factors through one co-support parameter) **fails**: `z(T)` genuinely depends on `τ1,τ2,τ3` (via `μ(τ1,τ2)` and `λ(τ1,τ2,τ3)`), so the fibers are not forced small by the closed form alone.
- Not `COUNTERPACKET` — this regime is **sub-reserve** (`η=σ/n=2/n→0`), and large `C2` sub-reserve is *expected* and is **forbidden** as a refutation of corrected-reserve `conj:B`. I also cannot exhibit explicit excess-slope data without running the scanner (disabled here).

**The exact missing invariant.** The slope map `z|_{{Δ=0}}` sends the `≈ n^2/6` solution subsets to its image. For fixed `z`, the locus is a **line** `ℓ_z=ker M(z)` in `(τ1,τ2,τ3)`-space (`M(z)` is the `2×4` matrix of the two `A`-components, entries affine in `z`). Thus

```text
C2 = #{ z : ℓ_z meets the cubic-splitting locus of D },
   = (#solution-T) / (avg fiber size),  fiber = #{3-subsets of D on ℓ_z}.
```

The wall is precisely: **the generic fiber size of `z` on `{Δ=0}` = the typical number of distinct-root cubics `X^3−τ1X^2+τ2X−τ3` split over `D` along a line `ℓ_z`.** If generic lines `ℓ_z` carry `Θ(n)` split cubics, then `C2=Θ(n)=n^{1+o(1)}` (collapse holds, law survives). If the relevant `ℓ_z` are the special "fixed `(τ1,τ2)`, vary `τ3`" directions (where `Δ=0` is a quadratic in `τ3` with `≤2` roots, contributing `O(1)` per `(τ1,τ2)`), then `C2` can reach `Θ(n^2)=Θ(q_line)` and the law fails sub-reserve. This split — **generic vs. axis-aligned direction of `ℓ_z` against the cubic-splitting locus** — is the single new invariant that replaces the Cycle 11 conic.

---

## Field ledger

```text
q_gen  = p        B=F_p   : D, w0, w1, base locators L_S, L_D, L_T, τ_i=e_i(T)
q_line = p^2      F=F_{p^2}: α, E, Bnum, residues in A=F[X]/E, slopes z, ∧, N_{A/F}
q_chal = unused (no protocol/challenge object invoked)
B, F kept strictly separate; no q_gen collapse claimed.
```

## Parameter ledger

```text
n=|D| (start D=F_p, n=p)    t=σ=deg E=2     j=n−a=r−t=3
a=k+t=n−3                   k=n−5           r=n−k=5
deg Q_S≤j−1=2               deg Bnum<2, [Bnum]_E≠0
co-support |T|=3, params e1(T),e2(T),e3(T); Q_S indep. of e3(T)
bad line F[Bnum]_E ⊂ A: codim t−1=1     reserve η=σ/n=2/n (sub-reserve)
Δ: total degree 2 in (τ1,τ2,τ3); [τ3^2]Δ=[W]_E∧[Bnum]_E
```

## Source dependencies (by label)

- `slackMCA_v3.tex:def:residue` (≈L1189) — slope/witness `Q_z≡zB mod E`, noncontainment.
- `slackMCA_v3.tex:thm:normalform` (≈L1197) — `emca=(1/q)·max_t Λ^{NC}`; slopes are the object, not raw residues.
- `slackMCA_v3.tex:prob:perfiber` (≈L1227), `conj:B` (≈L1231) — corrected-reserve `n^{1+o(1)}` is **above-reserve**; this regime is sub-reserve.
- `slackMCA_v3.tex:rem:aper` (≈L1255) — quotient-periodic denominators stay separated; `E` aperiodic.
- Cycle 9 locator-quotient `W=L_S Q_S+I_S`, `[I_S]_E=[W]_E−[L_S Q_S]_E`; Cycle 11 `j=2` conic and `[free^2]Δ=∧([W]_E,[Bnum]_E)`; Cycle 2 slope-uniqueness; Cycle 3 auto-noncontainment for `|S|≥a`, `Bnum≠0`.

---

## What Codex should bank

1. **`F1 t=2,j=3 quotient closed form`** (`BANKABLE_LEMMA`): the boxed `Q_S` (general `D` and `D=F_p`); `Q_S` is affine in `(e1(T),e2(T))` and **independent of `e3(T)`**.
2. **`F1 t=2,j=3 bad-locus quadric`** (`BANKABLE_LEMMA`): `Δ(τ1,τ2,τ3)` is a degree-2 surface with `[e3(T)^2]Δ=[W]_E∧[Bnum]_E`; `Δ≡0` ⇔ tangent/global endpoint (same resonance signature as Cycle 11).
3. **`F1 j=3 solution-counting vacuity`** (`EXACT_NEW_WALL`): for `n≈p`, `#{Δ=0}≈C(n,j)/p` is `O(n)` at `j=2` but `Θ(n^2)=Θ(q_line)` at `j=3`; Cycle 11's method dies exactly here.
4. **`W-F1-AA-RES-T2J3` missing invariant**: generic fiber size of `z|_{{Δ=0}}` = typical count of `D`-split cubics along the line `ℓ_z=ker M(z)`; collapse ⇒ `C2=Θ(n)`, no collapse ⇒ `C2` up to `Θ(q_line)`.

## What Codex must NOT bank

- Any `C2` bound (upper or lower) as proved — it is open pending the fiber invariant + scanner.
- Raw residue cardinality `C1` as the MCA object.
- Any refutation of `conj:B`: this regime is sub-reserve (`η=2/n`); large `C2` here is not an above-reserve counterpacket.
- Any `q_gen` collapse; any protocol/MCA/CA/list-/line-decoding/SNARK consequence; any extension to `j≥4`, `t≥3`.
- Cycle 11 beyond `t=2,j=2`.

---

## Suggested verifier/checker (spec — not executed here)

Extend `20260618_cycle11_t2_j2_line_incidence_verify.py`. Pseudocode:

```text
for p in {7,11,13,17,19} (n=p, D=F_p):
  pick nonresidue nr -> F=F_{p^2}; choose alpha=(0,1)
  for trials:
    E = random monic deg-2 in F[X], separated gcd(E,E^tau)=1, aperiodic, nonzero on D
    Bnum: deg<2, [Bnum]_E != 0   (sweep random AND adversarial: Bnum ∥ leading data)
    w0,w1: D->B random; w=w0+alpha*w1; W=interp_D(w)
    a=n-3 (t=2,j=3)
    # (A) verify closed form
    for S in C(D,a):
      T=D\S; (t1,t2,t3)=e1,e2,e3(T)
      Q_S = pdivmod(W,L_S).q
      assert Q_S == W_{n-1}(X^2-t1 X+t2)+W_{n-2}(X-t1)+W_{n-3}   # D=F_p
      assert coeff of Q_S has NO dependence on t3   # vary T with same (t1,t2)
    # (B) incidence + slope
      I_S = W - L_S Q_S
      RE = [I_S]_E
      z = line_scalar(RE, [Bnum]_E)      # None if RE not ∥ [Bnum]_E
      assert (z is not None) == (Delta(t1,t2,t3)==0)   # cross-check quadric
      if z: record z, and (t1,t2,t3)
    report: C1=#distinct RE, C2=#distinct z, #solution-T,
            [tau3^2]Delta == wedge([W]_E,[Bnum]_E),
            histogram of fiber sizes #{T -> given z}   # <-- the wall invariant
  EMIT counterpacket bundle if C2 grows ~ n^2 (note: sub-reserve, not a conj:B refutation)
```

Targets to read off: (i) confirm `[τ3^2]Δ=[W]_E∧[Bnum]_E`; (ii) the **fiber-size histogram** of `z` — its mean is the deciding invariant (`Θ(n)` ⇒ `C2=Θ(n)`; `O(1)` ⇒ `C2=Θ(n^2)`); (iii) keep `q_gen=p`, `q_line=p^2` columns separate; (iv) optionally run `t=3,j=2` (P2) for the codimension-2 comparison.

Verification status: closed form and `Δ`/leading-coefficient are proved by hand above; the fiber-collapse numerics are **pending** (no execution available in this environment).
