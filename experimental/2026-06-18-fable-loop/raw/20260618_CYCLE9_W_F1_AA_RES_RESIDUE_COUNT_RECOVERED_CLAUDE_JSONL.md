I've now read the wall history, the Cycle 6B/7/8 audits, the Cycle 8 checker, and the governing source statements (`def:residue`, `thm:normalform`, `prob:perfiber`, `conj:B`, `rem:aper`, `thm:rigidcyclo`, `thm:exactcount`). Here is my attack.

---

Final classification: EXACT_NEW_WALL

## Summary of the attack

Cycle 8 reduced the live object to the raw extension residue
`R_E(S) = [interp_S(w0)+alpha interp_S(w1)]_E in F[X]/E` on balanced `a=k+t` supports. The wall as currently *written* (ACTIVE_WALLS, Cycle 8 audit) asks to bound the **raw residue value count** `#{R_E(S)}` by `n^{1+o(1)}`. I claim that target is the wrong invariant, and I can prove why with an exact structural decomposition. The genuinely sharper missing invariant is a **bad-line incidence (landing) count**, and the reserve `eta=sigma/n` enters exactly as the codimension `t-1` of that line.

## 1. Bankable structural sub-result: locator–quotient decomposition

Let `W = interp_D(w) in F[X]`, `deg W <= n-1`, be the global interpolant of the arbitrary word `w=w0+alpha w1` on all of `D` (it exists because `D subset B` gives base-field Lagrange coefficients, so `W = W0 + alpha W1` with `Wi = interp_D(wi) in B[X]`). For an `a`-subset `S`, let `L_S = prod_{d in S}(X-d)`, `deg L_S = a`, and `Q_S = floor(W / L_S)`. Then:

```text
W = L_S Q_S + interp_S(w),   deg interp_S(w) < a,   deg Q_S <= n-1-a = j-1,
```

where `j := n - a = r - t` is the **co-support size** (`r=n-k`). Reducing mod `E`:

```text
R_E(S) = [W]_E - [L_S]_E [Q_S]_E   in F[X]/E.
```

Two consequences that are bankable now:

- `[W]_E` is **constant in `S`**, so `#{R_E(S)} = #{[L_S Q_S]_E}`. This is the structural decomposition in terms of `L_S` and the low-degree quotient `Q_S` requested as Angle 1, with the degree of `Q_S` pinned to the co-support size `j-1`, not to `t`.
- Parametrizing by the omitted set `T=D\S` (`|T|=j`, `L_S = L_D L_T^{-1}` in `(F[X]/E)^*`, all factors invertible since `E(d)!=0`), one gets the clean **true upper bound**

```text
#{R_E(S)} <= C(n, n-a) = C(n, r-t).
```

For fixed `j=r-t` this is `<= n^{j}`, i.e. polynomial but with exponent `j`. It equals `n^{1+o(1)}` only when `j<=1` (`t>=r-1`, the trivial top of reserve). So the raw-count bound `n^{1+o(1)}` is **not** delivered by this decomposition for any `j>=2`.

## 2. Why the raw-count reading of the wall is the wrong object (partial route-cut)

The MCA-relevant quantity in `def:residue`/`thm:normalform`/`Lambda^{NC}` is **not** `#{R_E(S)}`. It is the number of distinct **slopes** `z in F`, where `S` is bad-with-slope-`z` iff

```text
R_E(S) = z [Bnum]_E,    z in F (a scalar).
```

So a support contributes a slope **only when its residue lands on the one-dimensional `F`-subspace** `F[Bnum]_E subset F[X]/E`. This subspace has codimension `t-1` over `F` (`F[X]/E` is `t`-dimensional over `F`; the bad line is `1`-dimensional).

This immediately separates two counts that the current wall conflates:

- C1 (raw): `#{R_E(S)}` — generically `Theta(C(n,j))` above reserve for arbitrary anchors (different co-supports give different residues; there is `p^{2t} >> C(n,j)` room when `t` is large). So C1 already exceeds `n^{1+o(1)}` once `j>=2`. A raw counterpacket is therefore trivial and **not MCA-meaningful** — it refutes only the literal raw-count phrasing, not the slope count.
- C2 (slope/MCA): `#{ z in F : exists S, R_E(S) = z[Bnum]_E }` — the bad-line landing count. This is `Lambda^{NC}`-relevant and is the real target.

This is exactly why the banked `sigma=1` packet is sub-reserve in a way I can now make precise: at `t=1`, `F[X]/E ~= F` is one-dimensional, the bad line is codimension `0` (the whole space), so **C1 = C2** and both reach `Theta(q_line)`. For `t>=2` the bad line is a proper codim-`(t-1)` subspace and `C2 << C1`. The reserve mechanism is literally "raise `t` to thin the bad line."

## 3. The EXACT_NEW_WALL (strictly sharper invariant)

```text
W-F1-AA-RES-LINE-INCIDENCE:
For B=F_p, F=F_{p^2}, D subset B, separated aperiodic E (deg E=t=sigma,
gcd(E,E^tau)=1, E nonzero on D), nonzero numerator Bnum (deg<t), arbitrary
base anchors w0,w1, and balanced a=k+t=s_delta, bound the bad-line incidence
count
   N_line = #{ z in F : exists a-subset S with [W]_E - [L_S]_E[Q_S]_E = z[Bnum]_E }
        = # distinct slopes,
where Q_S=floor(W/L_S), deg Q_S <= j-1, j=n-a=r-t.
Equivalently: bound the number of co-supports T (|T|=j) whose locator-quotient
residue [L_S Q_S]_E lands in the codimension-(t-1) line [W]_E - F[Bnum]_E.
The reserve eta=sigma/n=t/n controls the codimension t-1 of the target line;
the conjectural n^{1+o(1)} is an incidence bound, not a cardinality bound.
```

This is strictly sharper than `W-F1-AA-RES-RESIDUE-COUNT` because:

- it replaces a set-cardinality (`#{R_E(S)}`) with an **incidence count** between the locator-quotient image and a fixed codim-`(t-1)` line;
- it is the actual `Lambda^{NC}` slope count (`thm:normalform`), so a bound here feeds MCA, whereas a raw-count bound does not;
- it isolates the reserve as the codimension of the line, explaining the `t=1` sub-reserve degeneration exactly and removing the temptation to refute via raw counts.

It is theorem-sized and actionable: it is an incidence problem between a structured combinatorial family `{(L_S, Q_S)}` and a linear subspace, with the degree-`(j-1)` quotient as the only genuinely free low-degree datum.

## Source dependencies

- `slackMCA_v3.tex:def:residue`, `thm:normalform` — the MCA object is the noncontained **slope** count `Lambda^{NC}`, i.e. residues on the bad line, not raw residues. This is what licenses the C1/C2 split.
- `slackMCA_v3.tex:prob:perfiber`, `conj:B`, `rem:aper` — the `n^{1+o(1)}` target and reserve/aperiodic framing; `conj:B`'s `q_{D,n}` generated-field correction is consistent with the count staying `q_line`-indexed off the line.
- `thm:rigidcyclo`/`thm:exactcount` — used only to note their rigidity is the **monomial/cyclotomic** antipodal-pair structure (`mu_N` subgroup); arbitrary anchors have no such symmetry, so no `q_gen` rigidity transfers (answering the prompt's Angle 3: no `q_gen` rigidity remains; honest counting is a `q_line` per-fiber incidence problem). Not imported beyond their proved strata.
- Cycle 6B kernel `interp_S(w)-interp_S'(w) in E*F_{<k}[X]` — recovered as the fiber of the incidence map, not reopened as the wall.
- Cycle 8 isomorphism — used as the bridge; twist not reopened.
- Cycle 3 nonzero-numerator noncontainment — guarantees every `|S|=a` support is noncontained, so landings are genuine slopes.

## Field ledger

- `q_gen = p`, `B = F_p`: domain `D`, anchors `w0,w1`, components `W0,W1`, locators `L_S,L_T` (base-field, since `D subset B`).
- `q_line = p^2`, `F = F_{p^2}`: `E`, `Bnum`, residues `R_E(S)`, the bad line `F[Bnum]_E`, slopes `z`. Residue space `F[X]/E` has `p^{2t}` elements; bad line has `<= p^2`. The count stays `q_line`-governed; no automatic collapse to `q_gen` (consistent with Cycle 8).
- `q_chal`: unused. No protocol/denominator/list/line-decoding claim.

## Parameter ledger

- `n=|D|`, `k=rho n`, `a=ceil((1-delta)n)=s_delta`, `sigma=a-k`, balanced `t=sigma`, `a=k+t`.
- `r=n-k`; co-support `j=n-a=r-t`; reserve `eta=sigma/n=t/n`.
- `deg E=t`, `deg Bnum<t`, `deg Q_S<=j-1`, `deg(L_S Q_S)<=a+j-1=n-1`.
- Bad line: `1`-dim over `F`; codimension `t-1` in `F[X]/E`.
- No quotient order, interleaving, or list arity used (separated/aperiodic `E`, `rem:aper`).

## Proof / audit notes

- Decomposition (§1) is elementary Euclidean division plus mod-`E` reduction; fully rigorous. The degree bound `deg Q_S<=j-1` is the only quantitative input and is tight.
- `#{R_E(S)} <= C(n,j)` is rigorous (the map factors through the choice of `T`).
- The C1/C2 split is definitional from `def:residue` (slope `z` is a scalar; badness needs `R_E(S) in F[Bnum]_E`). The claim "C1 generically `Theta(C(n,j))`" is stated as a generic/heuristic separation, not a theorem; the finite check (below) is to confirm the **mechanism** (`C1>>C2` for `t>=2`, `C1=C2` for `t=1`), not the asymptotic rate. Small-`n` finite data illustrates the mechanism only.
- This does **not** prove `prob:perfiber`, `conj:B`, any `n^{1+o(1)}` bound, any `q_gen` saving, or any protocol/MCA/list/line claim.

## What Codex should bank / test next

Bank:
- the locator-quotient decomposition `R_E(S)=[W]_E-[L_S]_E[Q_S]_E`, `deg Q_S<=n-a-1`, with `[W]_E` constant in `S`;
- the raw upper bound `#{R_E(S)} <= C(n,n-a)`;
- the C1 (raw) vs C2 (bad-line slope) distinction and the codimension-`(t-1)` identification of reserve;
- the sharpened wall `W-F1-AA-RES-LINE-INCIDENCE`.

Do **not** bank: any `n^{1+o(1)}` incidence bound, any refutation of the *slope*-count wall, or a `q_gen` collapse.

Test (extend the Cycle 8 checker, keeping fields separate):
- `B=F_7`, `F=F_49`. Two regimes on `D=F_7`: (i) `t=2,k=3,a=5,j=2` (separated aperiodic `E`, deg 2); (ii) `t=1,k=4,a=5,j=2` (`E` linear over `F`).
- Enumerate all `a`-subsets `S` (equivalently co-supports `T`, `|T|=j`). For random base anchors `w0,w1:D->B` and nonzero `Bnum`:
  1. verify the decomposition `R_E(S)==[W]_E-[L_S Q_S]_E` and `deg Q_S<=j-1`;
  2. tabulate `C1 = #distinct R_E(S)` and `C2 = #distinct slopes z` (those `S` with `R_E(S) in F*[Bnum]_E`);
  3. confirm regime (i) gives `C2 << C1` (bad line codim 1) and regime (ii) gives `C2 == C1` (bad line = whole space), reproducing the `sigma=1` sub-reserve behavior as the codim-0 endpoint.
- Then scan small growing `p`/`n` at fixed `j=2` to watch whether `C2` stays `n^{1+o(1)}`-like while `C1` tracks `C(n,2)`; emit a certificate of the gap. This is the minimal data that distinguishes the real (incidence) wall from the trivial raw-count statement.
