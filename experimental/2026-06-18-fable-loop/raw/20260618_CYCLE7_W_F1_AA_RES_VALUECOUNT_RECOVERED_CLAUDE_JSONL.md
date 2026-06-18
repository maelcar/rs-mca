Final classification: BANKABLE_LEMMA

## Statement

Setting (hypotheses, all source-grounded). `B=\F_p`, `F=\F_{p^2}`, `\tau` the nontrivial element of `\mathrm{Gal}(F/B)`, `\alpha\in F\setminus B` with `\{1,\alpha\}` a `B`-basis. `D\subset B`, `|D|=n`. Degree-`t` residue-line datum `(E,Bnum,w)` of `def:residue`: `E\in F[X]\setminus B[X]`, `\deg E=t=\sigma`, `E` nonzero on `D`; `\deg Bnum<t`; `w:D\to F`. Balanced ledger (Cycle 4): `a=k+t=s_\delta=\lceil(1-\delta)n\rceil`. Write `w=w_0+\alpha w_1`, `w_i:D\to B`; for an `a`-subset `S` set `P_i^S=\mathrm{interp}_S(w_i)\in B_{<a}[X]` (base Lagrange coefficients, banked Cycle 1). `\widehat E=\mathrm{lcm}(E,E^\tau)\in B[X]`. **Separation hypothesis** (tangent + quotient-periodic, per `rem:aper` and Cycle-2 caveat 2): `[Bnum]_E\neq 0` and `\gcd(E,E^\tau)=1`, so `\deg\widehat E=2t` and CRT gives `F[X]/\widehat E\cong F[X]/E\times F[X]/E^\tau`.

The slope of `S` (when defined) is the unique `z\in F` with `[P_0^S]_E+\alpha[P_1^S]_E=z\,[Bnum]_E` in `F[X]/E`.

Part A — Slope is a base-linear-fractional functional of the readout; conjugate is co-determined.
The slope map factors as a fixed `B`-linear-fractional map of the base readout `\rho(S)=([P_0^S]_{\widehat E},[P_1^S]_{\widehat E})\in(B[X]/\widehat E)^2`. Explicitly, with the `B`-linear `\varphi(\bar P_0,\bar P_1)=[\bar P_0]_E+\alpha[\bar P_1]_E\in F[X]/E`, a support is on the bad line iff `\varphi(\rho(S))\in F\cdot[Bnum]_E`, and then `z=\varphi(\rho(S))/[Bnum]_E`. Applying `\tau` to the slope equation yields, in the conjugate factor `F[X]/E^\tau`,
```
[P0^S]_{E^τ} + α^τ [P1^S]_{E^τ} = z^τ [Bnum^τ]_{E^τ},
```
so the same base readout `\rho(S)` also determines `z^\tau`. Consequently the slope set is `\tau`-stable and
```
#{ distinct slopes z(S) : S noncontained a-subset on the bad line }
        ≤  #{ ρ(S) : S noncontained a-subset on the bad line }  ⊆ B[X]/Ehat,
```
i.e. the `F`-valued value-count is dominated by the cardinality of the base readout image (a `q_gen`-coordinate object of `B`-dimension `\le 2\deg\widehat E\le 4t`).

Part B — Exact transfer for base slopes (`z\in B`). Let `\theta\in B[X]/\widehat E` be the (`\tau`-fixed) CRT element with `\theta\equiv\alpha\ (E)`, `\theta\equiv\alpha^\tau\ (E^\tau)`, and `\widehat b\in B[X]/\widehat E` the `\tau`-fixed element with `\widehat b\equiv[Bnum]_E\ (E)`, `\widehat b\equiv[Bnum^\tau]_{E^\tau}\ (E^\tau)` (both exist and are base by `\tau`-invariance; if `Bnum\in B[X]` then `\widehat b=[Bnum]_{\widehat E}`). For `z\in B` (`z^\tau=z`), the two CRT factors combine into a single base-field equation
```
[P0^S]_Ehat + θ·[P1^S]_Ehat = z·b̂      in  B[X]/Ehat,   z ∈ B.        (★)
```
Equation (★) is exactly a base-field residue-line readout for the base datum `(\widehat E,\widehat b,\;w_0+\theta w_1)` over `(B,D,k)` at prefix `\le\deg\widehat E\le 2t`. Hence the base-slope sub-count is bounded by the base packing number `\Lambda^{\mathrm{NC}}` of that datum (`def:residue`/`thm:normalform` over `B`), and on subgroup/monomial strata in the stable range it is governed exactly by `thm:exactcount`/`thm:rigidcyclo`: base-slope count `=\Acl(N',\ell')=n^{\beta(\rho)/\ceff+o(1)}`.

Transfer boundary (the answer to "where does the cyclotomic count transfer"). The base-field count of `thm:exactcount` transfers to the `z\in B` slopes exactly (via (★)) and does not transfer to `z\in F\setminus B`: off-base slopes are not `\tau`-fixed, so they are not equivalent to any single base equation in `B[X]/\widehat E` and instead require controlling the full base-readout image of Part A. This is the precise residual core (see "remaining wall").

## Why this is not the forbidden same-slope kernel

The kernel statement `\mathrm{interp}_S(w)-\mathrm{interp}_{S'}(w)\in E\cdot F_{<k}[X]` (Cycle 6B) answers "when is `z(S)=z(S')`." Parts A and B instead answer "what controls `\#\{z(S)\}`": A exhibits the slope as a fixed base-linear-fractional image of `\rho(S)` and bounds the count by the base-readout image; B reduces the entire `z\in B` stratum to a base `\Lambda^{\mathrm{NC}}` instance and imports `thm:exactcount` verbatim. Neither is a kernel/descent restatement.

## Source dependencies

`def:residue` (slackMCA_v3.tex:1189), `thm:normalform` (:1197), `prob:perfiber` (:1227), `conj:B` (:1231), `rem:aper` (:1255), `thm:rigidcyclo` (:737), `thm:exactcount` (:1148), `prop:qfloor` (:1273) for the `\Acl` form; banked Cycle 1 paired readout, Cycle 2 caveats (Ehat / unique-slope / `a`-subset noncontainment loss), Cycle 3 noncontainment subset lemma, Cycle 4 `a=s_\delta`. Galois descent + CRT are standard. No use of `ass:extension-mca-lift` (snarks_v4.tex:242), no `q_chal`, no line/list-decoding.

## Field ledger

`q_gen=p` (`B=\F_p`: `D`, `w_0,w_1`, readouts `\rho(S)`, `\theta`, `\widehat b`, `\widehat E`, and the entire `z\in B` stratum (★) live here). `q_line=p^2` (`F=\F_{p^2}`: `E,Bnum,\alpha,z` and the off-base slopes). `q_chal`: unused. The lemma's content is that the value-count is structurally a `q_gen` object (base readout image), with `q_line` re-entering only through off-base slopes.

## Parameter ledger

`n=|D|`; `k=\rho n`; `t=\sigma=a-k`; `a=k+t=s_\delta=\lceil(1-\delta)n\rceil`; reserve `\eta=\sigma/n`; radius `\delta`; extension degree `e=2`; `\deg\widehat E=2t` (quotient/lcm order), readout `B`-dimension `2\deg\widehat E\le 4t`; first finite test `t=\sigma=2` (`\deg\widehat E=4`, readout dim `\le 8`). No list arity invoked.

## Proof / audit notes

A: `E\mid\widehat E` always, so `\rho(S)` determines `[P_i^S]_E`; `\tau` is a ring iso `F[X]/E\to F[X]/E^\tau` fixing `B[X]`, giving the conjugate equation; `B`-linearity of `\varphi` and `|\rho(S)\text{-image}|` bounding `\#\{z\}` is immediate since `z=\varphi(\rho(S))/[Bnum]_E` is a fixed function of `\rho(S)`. B: `(\alpha,\alpha^\tau)` and `([Bnum]_E,[Bnum^\tau]_{E^\tau})` are `\tau`-fixed under the CRT action `(u,v)\mapsto(v^\tau,u^\tau)`, hence base; `z=z^\tau` collapses (*)+(**) onto the fixed subring `B[X]/\widehat E`, which is precisely the base residue-line form of `def:residue`/`thm:normalform`. The `\gcd(E,E^\tau)=1` and `[Bnum]_E\neq0` hypotheses are exactly the tangent/quotient-periodic separations the wall requires; without them CRT and unique-`z` fail (correctly excluded). Consistency with the `\sigma=1` counterpacket: at `t=1`, `\deg\widehat E=2`, readout `\le\F_p^4`; the bound `\#\{z\}\le\#\rho(S)` permits `\Theta(p^2)` because the base-readout image is large at sub-reserve `\eta\to0` — A relocates, and does not close, that regime, as required.

## Remaining wall (not claimed proved)

The off-base count `\#\{z\in F\setminus B\}` equals the number of distinct base readouts whose `\varphi`-image meets `F\cdot[Bnum]_E` off the base sub-line `B\cdot[Bnum]_E`. Bounding this by `n^{1+o(1)}` above corrected reserve `\eta\ge(1+\epsilon)\taustar(\rho,q_{gen})` is exactly a base-field instance of `prob:perfiber`/`conj:B` for the fixed-anchor varying-support locus — now honestly in `q_gen` coordinates. This is the genuinely open core; A+B reduce it from an `F`-count to this base-readout-image incidence count and dispatch the `z\in B` stratum exactly.

## What Codex should bank / test next

Bank: (A) the base-linear-fractional slope functional + `#slopes ≤ #base-readouts` + conjugate co-determination; (B) the exact base-slope reduction (★) to the base datum `(\widehat E,\widehat b,w_0+\theta w_1)` and the `thm:exactcount` transfer for `z\in B`; and the transfer boundary (base slopes transfer, off-base do not).

Test (`t=\sigma=2` finite certificate, per P2): pick smallest `p\equiv1\bmod n` with `D\le\F_p^\times` a subgroup, `k=\rho n`, `a=k+2`; pick `E\in\F_{p^2}[X]` degree 2 with `\gcd(E,E^\tau)=1` and `E` nonzero on `D`, `Bnum\neq0` with `[Bnum]_E\neq0`; pick base words `w_0,w_1:D\to\F_p`. Enumerate `a`-subsets `S`, compute `\rho(S)\in(\F_p[X]/\widehat E)^2`, the slope `z(S)\in\F_{p^2}` on the bad line, and the noncontainment flag (Cycle 3). Certify three statistics: (i) `\#\{z(S)\}\le\#\{\rho(S)\}` (Part A); (ii) the `z\in\F_p` sub-count equals the base `\Lambda^{\mathrm{NC}}` of `(\widehat E,\widehat b,w_0+\theta w_1)` computed independently via (★) (Part B); (iii) `\{z(S)\}` is `\tau`-stable. A discrepancy in (i)–(iii) falsifies the lemma; agreement plus an off-base excess `\#\{z\in\F_{p^2}\setminus\F_p\}\gg n^{1+o(1)}` at corrected reserve would be the first above-reserve counterpacket and should be promoted to a COUNTERPACKET run. Reuse `f1_extension_slope_sweep.py` / `mca_slope_scan.py` harnesses with the readout taken over `\widehat E` rather than `E`.
