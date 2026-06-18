I'll start by reading the file index, then work through the required files.I'll read the required project files. Let me start with the core state files in parallel.Now the audit files and the PR triage. Let me read the required audits.Now let me read the key TeX definitions. Let me find `def:residue` and related labels in slackMCA_v3.tex.I only have the Read tool, so I'll navigate by reading. Let me read the detailed raw working files and locate `def:residue` in the TeX.This prior raw is the monic-anchor solution. Now I need the actual `def:residue` definition to handle arbitrary anchors. Let me read the relevant TeX region around line 1189.I have what I need. The `def:residue` definition (slackMCA_v3.tex:1189) is the load‑bearing object: the anchor `w:D→F` is an arbitrary function, and balanced `t=σ` forces `deg Q_z < k+t = a ≤ |S_z|`, so the witness is the forced interpolant of `w` on the support. That is the hinge. Here is the result.

---

# F1 arbitrary-anchor balanced denominators: the interpolation-residue reduction

## Verdict

**`PROOF`** (arbitrary-anchor → base-field reduction; no extension-only degrees of freedom). Equivalently this is a strict `BANKABLE_LEMMA` with one named open endpoint.

Decision on the wall `W-F1-AA`: at balanced `t=σ`, **arbitrary anchors do reduce to a base-field readout, with extension multiplicity exactly `[F:B]=2` and no extension-only freedom** — so there is **no** arbitrary-anchor counterpacket above the monic case. But the base readout they reduce to is **not** the monic locator image `S↦[L_S]_{\hat E}`; it is the strictly larger **paired interpolation-residue readout** `S↦(\,interp_S(w_0)\bmod\hat E,\ interp_S(w_1)\bmod\hat E\,)`. The audit's worry ("`[L_S]_{\hat E}` need not capture all balanced data") is correct and is resolved **inside the base field**, not by going to `F`. The open core therefore upgrades from `prob:perfiber` (locator/symmetric-function collisions) to the general base-anchor per-fiber collision problem.

I cannot bank a finished bound (same status as the monic case, which only reduced to `prob:perfiber`), but the reduction itself is complete and hand-proved for **all** balanced `E∈F[X]∖B[X]`, arbitrary `w`, arbitrary `B_num`.

## Ledger (kept separate)

`B=F_p=F_{q_gen}`, `q_gen=p` (entropy/pigeonhole field, drives the reserve). `F=F_{p^2}=B[α]/(α²−d)=F_{q_line}`, `q_line=p²` (slopes live here). `τ:x↦x^p`. `q_chal` unused (no protocol statement). `D=H≤F_p^×`, `|H|=n`. `C_F=RS[F,D,k]`, `k=ρn`, balanced `t=σ`, `a=k+σ=k+t`, `s_δ=a`. `L_S=∏_{s∈S}(X−s)∈B[X]`. `Ê:=lcm(E,E^τ)∈B[X]`, `deg Ê = deg G + 2 deg E_1 ≤ 2t` via the Frobenius factorization `E=G·E_1`, `G=gcd(E,E^τ)∈B[X]`, `gcd(E_1,E_1^τ)=1` (banked Thm 1).

---

## Theorem A (forced interpolant at balanced `t=σ`)

Let `(E,B_num,w)` be a degree-`t` residue-line datum (`def:residue`) with `t=σ`, and `(Q_z,S_z)` a witness for slope `z`. Then `deg Q_z < k+t = a` and `|S_z| ≥ s_δ = a`, so for **every** `a`-subset `S⊆S_z`, `Q_z = interp_S(w|_S)` is the unique degree-`<a` interpolant. In particular every bad slope is witnessed by an `a`-subset with `Q_S := interp_S(w)`.

*Proof.* `Q_z` has degree `<a` and agrees with `w` on `≥a` points; an `a`-subset determines it uniquely. Maximal supports `|S_z|>a` only impose extra agreement, giving a subset of the `|S|=a` data; noncontainment only removes slopes. ∎

This is exactly why `t=σ` is the wall: residual slack `σ−t=0`, so the residual-slack list reduction (`..._RESIDUAL_SLACK_AUDIT.md`, Lemma 1) gives nothing and the interpolant is rigidly forced.

## Theorem B (base split — no extension-only degrees of freedom; the core)

Write `w = w_0 + α w_1` with `w_0,w_1:D→B`. Because `S⊆D⊆B`, the Lagrange basis `ℓ_{S,s}(X)=∏_{s'≠s}(X−s')/(s−s')∈B[X]`. Hence
```
Q_S = interp_S(w) = Q_S^{(0)} + α Q_S^{(1)},   Q_S^{(i)} := interp_S(w_i) ∈ B[X],  deg < a.
```
The two components are **base-field** interpolants of **base** words. The extension field enters `Q_S` only as the fixed scalar `α`. ∎

Consequence: the only `S`-dependent (hence many-valued) data in a witness is the **pair of base polynomials** `(Q_S^{(0)},Q_S^{(1)})`. There is no extension-valued object that varies with `S`.

## Theorem C (base-field readout mod `Ê`, dimension `≤2t`, fixed reconstruction)

The bad-slope map factors as
```
S  ─R─►  ρ(S) := ( Q_S^{(0)} mod Ê ,  Q_S^{(1)} mod Ê ) ∈ ( B[X]/(Ê) )²     [BASE, dim_{F_p} ≤ 2·deg Ê ≤ 4t]
        ─Ψ─►  z ∈ F ∪ {⊥}
```
where `Ψ` is a **fixed** `F`-rational map depending only on `(α,E,B_num)`, not on `S` or `w`:
reduce each component further `mod E` (legitimate since `E∣Ê`), form `[Q_S]_E=[Q_S^{(0)}]_E+α[Q_S^{(1)}]_E∈R:=F[X]/(E)`, and output the unique `z∈F` with `[Q_S]_E = z[B_num]_E` if it exists in the `F`-algebra `R` (i.e. `[Q_S]_E` lies on the fixed `F`-line `F·[B_num]_E`; this is `t−1` fixed `F`-linear conditions), else `⊥`.

*Proof.* `Q_S mod E` is determined by `Q_S mod Ê` since `E∣Ê`; `Ê∈B[X]` so each `Q_S^{(i)} mod Ê∈B[X]/(Ê)`, an `F_p`-space of dimension `deg Ê`. `[B_num]_E≠0` (datum hypothesis `E∤B_num`), so `z` is unique when it exists. All of `Ψ` uses only fixed constants `α,β,γ,…,[B_num]_E`. ∎

**Corollary (reduction; the bankable statement).**
```
#{bad slopes of (E,B_num,w)} ≤ #{ ρ(S) : S∈C(D,a) bad }
                              ≤ #{ a-subsets meeting the fixed F-linear bad-locus, counted in (B[X]/Ê)² }.
```
Distinct extension slopes inject into a **base-field** object of `F_p`-dimension `≤2 deg Ê ≤ 4t`; the extension contributes only the fixed `[F:B]=2` doubling (`w_0,w_1`) and the fixed map `Ψ`. **Arbitrary `w` adds no extension-only degree of freedom beyond this base object.**

---

## First balanced case `σ=t=2`, explicit

`a=k+2`, `E` degree 2 in `F[X]∖B[X]`. Two strata (Frobenius factorization):

- (b) `E=(X−β)(X−γ)`, `β,γ∈F∖B` in distinct `τ`-orbits (`deg E_1=2`): `R≅F×F` by `g↦(g(β),g(γ))`; `Ê=(X−β)(X−β^τ)(X−γ)(X−γ^τ)`, `deg Ê=4`.
- (a) `E=(X−c)(X−β)`, `c∈B`, `β∈F∖B` (`deg G=1,deg E_1=1`): `Ê=(X−c)(X−β)(X−β^τ)`, `deg Ê=3`.

Take stratum (b), `B_num=1`. Bad condition and readout become fully explicit:
```
bad(S)  ⟺  Q_S(β) = Q_S(γ),     z_S = Q_S(β),
Q_S(β) = Q_S^{(0)}(β) + α Q_S^{(1)}(β),   Q_S^{(0)},Q_S^{(1)}∈B[X],
```
and `(Q_S^{(i)}(β),Q_S^{(i)}(γ))` are read off from `(Q_S^{(i)} mod Ê)` (the residue carries the values at all four roots). So the slope is a fixed `F`-bilinear readout of the pair of base residues — a base object of `F_p`-dimension `≤8`.

**Why this is strictly richer than the monic locator image, yet still base.** Monic anchor `w=X^a`: `interp_S(X^a)=X^a−L_S`, so `Q_S^{(0)} mod Ê = (X^a mod Ê) − [L_S]_{\hat E}` and `Q_S^{(1)}=0`. The readout collapses to the single locator class `[L_S]_{\hat E}` — a **symmetric-function** of `S`. For arbitrary base `w_0` (already with `w_1=0`!), `interp_S(w_0)` is a **general** degree-`<a` interpolant whose residue mod `Ê` is **not** a symmetric function of `S` and **not** a locator difference. So the locator readout is incomplete (audit confirmed), but the failure is purely in the **base** direction: general interpolation residues vs. locator residues. The `w_1` term adds one more independent base copy, never an extension-valued invariant.

**Hand-checkable micro-witness of incompleteness (no search).** Fix any two distinct `a`-subsets `S≠S'` of `H` with the SAME locator class `Ê∣(L_S−L_{S'})` (possible since `deg(L_S−L_{S'})<a` and `deg Ê=4`; e.g. choose `S,S'` differing in points engineered so `L_S−L_{S'}` is `Ê` times a base polynomial). Under the monic anchor these are forced to share a slope. Define a base anchor `w_0:D→B` agreeing with `X^a` off `S∪S'` but with `w_0` altered on one point of `S∖S'`. Then `interp_S(w_0) mod Ê ≠ interp_{S'}(w_0) mod Ê` while `[L_S]_{\hat E}=[L_{S'}]_{\hat E}`: identical locator class, different interpolation-residue class, hence (through fixed `Ψ`) generically different bad slopes `z_S≠z_{S'}∈B`. This explicitly separates the interpolation-residue readout from the locator readout — and both are base-field. There is no `F∖B` invariant anywhere; this is **not** a counterpacket against the base reduction, it is a proof that the correct base readout is the interpolation-residue one.

---

## Exact missing hypothesis (the upgraded open core)

The reduction is unconditional; the *bound* needs one base-field input, strictly generalizing `prob:perfiber` (slackMCA_v3.tex:1227):

> **Generalized per-fiber collision problem (`q_gen=p`).** For `σ≥Cn/log₂n`, all large `p≡1 (mod n)` with `n^{c_0}≤p≤2^{o(n)}`, every fixed modulus `M∈F_p[X]` with `deg M≤2σ`, and **arbitrary** base words `w_0,w_1:H→F_p`: the map `S↦(interp_S(w_0) mod M, interp_S(w_1) mod M)` on `a`-subsets has every fiber along a fixed `F_p`-linear relation of size `≤n^{1+o(1)}`.

`prob:perfiber` is the special case `w_0=X^a|_H` (so `interp_S(w_0) mod M = (X^a−L_S) mod M`, the symmetric/power-sum readout), `w_1=0`, `M=Ê`. The arbitrary-anchor balanced wall is **equivalent in difficulty** to this generalized statement at prefix/modulus degree `≤2t`. The factor-`≤2` dimension blow-up (`2t` vs `t`, plus the `w_0,w_1` doubling) does not change the `n/log n` threshold order; `q_gen=p` still drives the reserve via `eq:entropy-necessary` (`σ log₂p ≳ log₂ C(n,a)`), **not** `q_line`.

Object ledger (kept separate): list-decoding `eq:extension-list` untouched (unbalanced import only); CA sub-reserve `Θ(1)` density survives; MCA/support-wise line-MCA = this conditional reduction; line-decoding `op:line-decoding` and protocol/`ass:extension-mca-lift` remain un-citable unrestricted — the defensible protocol charge is the extension **list** term (unbalanced) plus this **base** generalized-per-fiber term (balanced), never dividing a base numerator by `q_line`.

---

## Pseudocode (EXPERIMENTAL — NOT RUN; only Read available)

```python
# Decides W-F1-AA empirically at small p. Theorems A–C are hand-proved, run-independent.
# F = F_p[α]/(α²−d).  E∈F[X]\B[X] squarefree, nonzero on H, deg E = t = σ.
from itertools import combinations
def arbitrary_anchor_readout(p, d, k, t, E_F, Bnum_F, w0, w1):   # w0,w1 : H -> F_p  (arbitrary!)
    F = Fp2(p, d); a = k + t
    Ehat = lcm_F(E_F, frobenius(E_F))           # ∈ B[X], deg ≤ 2t
    slopes = set(); rho_classes = {}
    for S in combinations(H_elements(p), a):
        Q0 = interp_base(S, [w0[s] for s in S])  # ∈ B[X], deg < a   (Lagrange over base pts)
        Q1 = interp_base(S, [w1[s] for s in S])  # ∈ B[X], deg < a
        rho = (poly_mod(Q0, Ehat), poly_mod(Q1, Ehat))          # BASE readout in (B[X]/Ehat)²
        z = Psi(rho, E_F, Bnum_F, alpha=F.alpha)  # fixed F-rational map: ⊥ unless on F·[Bnum]_E
        if z is not None and noncontained(S, w0, w1, E_F, Bnum_F, k):
            slopes.add(z); rho_classes.setdefault(rho, z)
    return len(slopes), len(set(rho_classes.values()))   # equal ⇒ slope factors through base readout
# PREDICTIONS (Thm C): #slopes == #distinct ρ(S) for EVERY (w0,w1) and EVERY E   (factorization is exact).
#   monic check: w0 = (s↦ s^a), w1 = 0  ⇒  ρ(S) = (X^a−L_S mod Ehat, 0)  reproduces [L_S]_Ehat (locator).
#   separation check: pick S≠S' with Ehat | (L_S−L_{S'}); perturb w0 on one pt of S\S'
#                     ⇒ ρ(S) ≠ ρ(S') though [L_S]=[L_{S'}]  ⇒ interpolation readout ⊋ locator readout.
#   reserve: sigma*log2(p) ≥ log2(comb(p-1, k+t))   (eq:entropy-necessary, q_gen=p, NOT p²).
```
Suggested promotion: extend `verify_f1_sigma2_degree1.py` to (i) confirm `#slopes == #distinct ρ(S)` for random `(w_0,w_1)` over small `F_{p^2}` and both strata (a),(b); (ii) run the separation check above to witness interpolation-readout ⊋ locator-readout inside the base field.

## Exact dependency labels

`slackMCA_v3.tex`: `def:residue` (l.1189 — arbitrary `w:D→F`, the gap), `lem:denom` (l.1193), `thm:normalform` (l.1197, `emca=(1/q)max_t Λ^{NC}` — Thms A–C instantiate over `F`), `rem:strata` (l.1209, monic locator stratum `(X^r,−1,x^T)`), `prob:perfiber` (l.1227, special case of the generalized endpoint), `conj:B`/`rem:aper` (l.1231/1255, reserve `η≥(1+ε)τ*(ρ,q_{D,n})`, `q_{D,n}=q_gen`). `snarks_v4.tex`: `ass:extension-mca-lift` (l.242, stays un-citable), `rem:lift-evidence` (l.251(ii), the `G`/base stratum), `eq:extension-list` (l.235), `eq:entropy-necessary`+`taustar` (l.290–306, `q_gen` not `q_line`). `proximity_blueprint_v3.tex`: `prob:F1` (l.471), attempt-items 3–4. `cs25_cap_v4.tex`: `lem:confine` (`G`-part only). Audits: `..._BASE_CORE_REDUCTION_AUDIT.md` (monic `S↦[L_S]_{\hat E}`, this extends it to arbitrary `w`), `..._RESIDUAL_SLACK_AUDIT.md` (slack `σ−t`, why `t=σ` is rigid), `..._FIXED_RATE_COUNTEREXAMPLE_AUDIT.md` (sub-reserve `σ=1`, `deg Ê=2` degeneracy), `..._F1_EXTENSION_MCA_COUNTEREXAMPLE_AUDIT.md`. Verifiers `verify_f1_sigma2_degree1.py`, `verify_f1_extension_counterexample.py` (AUDIT-grade).

**Bottom line.** Arbitrary anchors reduce to a base-field readout with no extension-only freedom (`PROOF` of the reduction); the readout is the paired interpolation-residue object mod `Ê∈B[X]` of dimension `≤2t`, strictly containing the monic locator image; and the one open input is the generalized base per-fiber bound, which is the locator-case `prob:perfiber` extended from symmetric functions to arbitrary base anchor words. No arbitrary-anchor counterpacket exists above the monic case.