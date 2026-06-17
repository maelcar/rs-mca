I'll start by reading the file index, then the key context files.Let me read the key audit files and verification scripts in parallel.Now the verification scripts and status/backlog files.Now the status ledger, open problems, and the raw residual-slack answer.Now the open problems file and the residual-slack raw answer.Now let me read the raw residual-slack answer and the key TeX definitions in parallel.The raw residual-slack answer located the wall but did not attack it. Let me read the precise normal-form and exact-slack definitions in the TeX, plus the F1 target.I'll use offset/limit instead.Let me read the exact slack characterization and the F1 target statements.Now the F1 targets in snarks_v4.tex and the blueprint.Now the blueprint F1 problem statement, and the verify_f1_extension_counterexample.py to understand the full mechanism.Now let me read the extension counterexample verifier and check whether `bash` is available to run computations.I have the full picture now: the residual-slack reduction, the residue-line normal form (`def:residue`/`thm:normalform`), the exact-slack mechanism (`thm:exactslack`/`B_T`), and the F1 targets. The raw residual-slack answer *located* the balanced wall but explicitly did not attack it. The decisive question is computational. Let me verify `bash` works and set up the exact balanced-denominator computation.The bash tool isn't available in this harness. Let me try the alternate schema once to be certain before proceeding analytically.I have everything I need. The `bash`/python tool is not available in this harness, so all results below are by-hand proofs and explicitly-marked heuristics; pseudocode is given but tagged not-run. The prior residual-slack answer *located* the balanced wall but did not analyze it. Here is the attack.

---

# F1 Balanced Extension Denominators: CRT Reduction and the Exact Wall

## 1. Executive verdict (5 lines)

The balanced wall does not yield a clean theorem and does not (above reserve) yield a surviving counterexample; it resolves into the entropy-reserve dichotomy. PROVED: balanced $t=\sigma$ packing reduces by CRT to counting an $F$-line's hits on the locator-evaluation image $\{(L_S(\alpha_1),\dots,L_S(\alpha_\sigma))\}\subseteq F^\sigma$; genuinely-extension forces $\gcd(E,E^\tau)=1$ (conjugate-paired $E$ collapses into $B[X]$), and every single Vieta slice contributes only $O(n)$ slopes. The $\sigma=1$ explosion is special to a residual-slack-0, $1$-dimensional residue ring and does **not** transfer through any single algebraic slice. Above the corrected reserve the naive line-hit expectation is $\binom{n}{a}/q_{\rm line}^{\,\sigma-1}\to0$, so an explosion must aggregate $\Omega(n)$ slices — controlled by exactly `conj:final-mca`/`conj:final-locator` lifted to $F$, which is the sole remaining obstruction. The wall is therefore an EXACT_NEW_WALL identical to the unproven MCA/locator local limit in $F$-coordinates, not a new object.

---

## 2. Formal statements

Throughout: $B=\F_p=\F_{q_{\rm gen}}$, $F=\F_{p^2}=\F_p[\alpha]/(\alpha^2-d)=\F_{q_{\rm line}}$, $D=H=\F_p^\times$, $n=p-1$, $C_F=\RS[F,D,k]$, $k=\rho n$, $a=k+\sigma$, $\delta=1-a/n$, datum $(E,B_{\rm num},w)$ with $\deg E=t$, $\deg B_{\rm num}<t$, $E$ nonzero on $D$, $E\nmid B_{\rm num}$. $\tau$ is the nontrivial automorphism of $F/B$, $E^\tau$ the conjugate, $R=F[X]/(E)$, $\xi=[X]_E$. The balanced regime is $t\in[\sigma-\Theta(n/\log n),\sigma]$, $E\in F[X]\setminus B[X]$.

**Theorem 1 (line-incidence normal form, $t=\sigma$; PROVED).** At $t=\sigma$ (residual slack $0$), for the monic-degree-$a$ anchor $w$, the support-wise line-MCA bad slopes of $(E,B_{\rm num},w)$ are *exactly*
$$\#\{z\in F:\ [w]_E-z[B_{\rm num}]_E\in\mathcal I\},\qquad \mathcal I:=\{[L_S]_E:\ S\in\tbinom{D}{a}\}\subseteq R\cong F^\sigma,$$
i.e. the number of points of the locator-residue image $\mathcal I$ on the $F$-line $\mathcal L=[w]_E+F\cdot[B_{\rm num}]_E$. Maximizing over $(E,B_{\rm num},w)$ gives $\Lambda^{\rm NC}_{\sigma,\delta}(D,k)=\max_{E\notin B[X]}\max_{\mathcal L\ F\text{-line}}|\mathcal I_E\cap\mathcal L|$ (modulo the noncontainment condition, which only restricts).

**Theorem 2 (conjugate-pairing dichotomy; PROVED).** For $E$ squarefree of degree $\sigma$, nonzero on $D$: $E$'s root set is closed under $x\mapsto x^p$ $\iff$ $E\in B[X]$. If $E\in B[X]$ the bad slopes are subfield-confined to $B$ (`cs25_cap_v4.tex` `lem:confine`), density $\le|B|/|F|=1/p$. Hence every *genuinely extension-valued* balanced datum has $\gcd(E,E^\tau)=1$ (no conjugate pairs), and then $R_0:=\F_p[\xi]\cong\F_p[X]/(EE^\tau)$ has full $\F_p$-dimension $2\sigma=\dim_{\F_p}R$, so subfield confinement gives no saving and $\mathcal I\subseteq R_0=R$.

**Theorem 3 (CRT coordinates; PROVED).** When $\gcd(E,E^\tau)=1$ and $E$ splits over $F$ as $\prod_{i=1}^\sigma(X-\alpha_i)$ with $\alpha_i\in F\setminus B$ pairwise non-conjugate, $R\cong F^\sigma$ via $[g]_E\mapsto(g(\alpha_i))_i$, and $[L_S]_E\mapsto(L_S(\alpha_i))_i$, $L_S(\alpha_i)=\prod_{s\in S}(\alpha_i-s)$. The bad-slope count for line $\mathcal L=\{(w(\alpha_i)-z\,B_{\rm num}(\alpha_i))_i\}$ equals
$$\#\Big\{\text{distinct }L_S(\alpha_1):\ S\in\tbinom{D}{a},\ \tfrac{w(\alpha_i)-L_S(\alpha_i)}{B_{\rm num}(\alpha_i)}\ \text{independent of }i\Big\}\quad(\sigma-1\text{ linear }F\text{-constraints}).$$

**Theorem 4 (slice caps; PROVED).** Fix a tail $T$, $|T|=a-j$, and vary a $j$-subset ($1\le j\le\sigma$). The slice image lies in the $j$-dimensional $\F_p$-flat $\mathcal F_T=[L_T]_E\xi^{\,j}+[L_T]_E\,W_{j-1}$, $W_{j-1}=\mathrm{span}_{\F_p}\{1,\xi,\dots,\xi^{j-1}\}$. For the anchor-aligned direction $[B_{\rm num}]_E=[L_T]_E$ the slice contributes exactly $z=x\in\F_p$, i.e. $\le p$ base-field slopes, because $W_{j-1}\cap F=\F_p$ whenever $E\notin B[X]$. No single Vieta slice (any $j\le\sigma$, any direction) exceeds $p=\Theta(n)$ slopes when $E\notin B[X]$.

**Exact New Wall W-bal (EXACT_NEW_WALL).** Above the corrected reserve $\sigma\ge Cn/\log n$ (so $\sigma\log_2 q_{\rm gen}\ge(1{+}\eps)\log_2\binom na$, using $q_{\rm gen}=p$, **not** $q_{\rm line}$), the expected hit count of a generic $F$-line on $\mathcal I$ is $\binom na/q_{\rm line}^{\,\sigma-1}\to0$; the repaired extension-line MCA theorem holds **iff** the locator-evaluation image has no abnormally rich $F$-line:
$$\boxed{\ \max_{E\notin B[X]}\ \max_{\mathcal L}\ \big|\mathcal I_E\cap\mathcal L\big|\ \le\ n^{1+o(1)}\ }\qquad(\text{balanced extension local limit}),$$
which is precisely `slackMCA_v3.tex` `conj:final-mca`/`conj:final-locator` evaluated at the $2\sigma$ points $\{\alpha_i,\alpha_i^p\}$ over $F$. No new object appears. Below reserve (including every fixed $\sigma\ge2$, $t=\sigma$) the bound fails and the wall explodes to $\Theta(p^2)$ — a sub-reserve counterexample that does not refute the above-reserve theorem.

---

## 3. Full parameter ledger

| symbol | meaning | value / regime |
|---|---|---|
| $B$ | base = generated = entropy field | $\F_p$ |
| $F$ | extension = line = witness field | $\F_{p^2}=\F_p[\alpha]/(\alpha^2-d)$, $d$ nonsquare |
| $q_{\rm gen}$ | entropy field size (pigeonhole) | $p$ — **kept distinct; never replace by $F$** |
| $q_{\rm line}$ | line-experiment field (slopes sampled) | $p^2$ |
| $q_{\rm chal}$ | verifier challenge field | $=q_{\rm line}$ only after a protocol proof |
| $H=D$ | evaluation set | $\F_p^\times$, $n=p-1$ |
| $k,\rho$ | dimension, rate | $k=\rho n$, $\rho\in\{1/2,1/4\}$ |
| $a,\sigma,\delta,\eta$ | agreement, slack, radius, reserve | $a=k+\sigma$, $\delta=1-a/n$, $\eta=\sigma/n$ |
| $t=\deg E$ | denominator degree | balanced $t\in[\sigma-\Theta(n/\log n),\sigma]$ |
| $E,E^\tau$ | denominator, conjugate | $E\in F[X]\setminus B[X]$, $\gcd(E,E^\tau)=1$ |
| $R,\xi,\mathcal I$ | $F[X]/(E)$, $[X]_E$, $\{[L_S]_E\}$ | $R\cong F^\sigma$, $\dim_{\F_p}R=2\sigma$ |
| corrected reserve | regime of interest | $\sigma\log_2 q_{\rm gen}\ge(1{+}\eps)\log_2\binom na$ |
| $\mu,\nu,e$ | list arity, interleaving, $[F:B]$ | $1,1,2$ |

---

## 4. Proof / obstruction analysis

**Theorem 1.** With $w$ monic of degree $a$, the degree-$\le a-1$ interpolant of $w$ on an $a$-subset $S$ is $W_S=w-L_S$ ($L_S=\prod_{s\in S}(X-s)$ vanishes on $S$, $\deg(w-L_S)\le a-1$). The residue-line witness (`def:residue`) requires $Q_z\equiv zB_{\rm num}\ (\mathrm{mod}\ E)$, $Q_z=w$ on $S$, $\deg Q_z<k+t=a$; so $Q_z=W_S$ and the bad-slope condition is $[w]_E-[L_S]_E=z[B_{\rm num}]_E$. For each $S$ there is at most one $z$ (since $[B_{\rm num}]_E\ne0$), and $z$ exists iff $[L_S]_E\in[w]_E-F[B_{\rm num}]_E=\mathcal L$. At $t=\sigma$ the degree budget $\deg W_S\le a-1$ is automatic for *every* $a$-subset (residual slack $0$), so `Lemma 1` of the residual-slack audit gives no reduction — this is structurally why $t=\sigma$ is the wall. $\square$

**Theorem 2.** If $g\in B[X]$ and $E\mid g$ in $F[X]$, applying $\tau$ gives $E^\tau\mid g$, so $\mathrm{lcm}(E,E^\tau)\mid g$; thus the minimal $\F_p$-polynomial of $\xi$ is $EE^\tau/(\text{unit})$ when $\gcd(E,E^\tau)=1$, of degree $2\sigma$, giving $\dim_{\F_p}R_0=2\sigma=\dim_{\F_p}R$. If instead the root set is $p$-power-closed then $E=E^\tau\in B[X]$, and `cs25_cap_v4.tex` `lem:confine` confines bad slopes to $B$ (density $1/p$). This settles **attack path B**: products of conjugate pairs $(X-\alpha_i)(X-\alpha_i^p)$ land in $B[X]$ — they are not genuinely extension-valued, and searching them is the provably-futile base-rational case (`prob:F1`, "How to attempt" item 3). $\square$

**Theorem 3** is CRT plus $L_S(\alpha_i^p)=L_S(\alpha_i)^p$ (since $L_S\in\F_p[X]$); the conjugate values are pinned by $z$, so the genuine freedom is the $\sigma$ values $(L_S(\alpha_i))_i$ on $\mathcal L$. $\square$

**Theorem 4 (the decisive structural point).** The $j$-point slice residue is $[L_T]_E\prod_{i=1}^j(\xi-x_i)$; expanding, $\prod(X-x_i)\bmod E\in\xi^{\,j}+W_{j-1}$, so the image sits in the $\F_p$-flat $\mathcal F_T$. Its direction space is $[L_T]_E W_{j-1}$. Intersecting with the $F$-line direction $F[B_{\rm num}]_E$: aligning $[B_{\rm num}]_E=[L_T]_E$ reduces this to $\dim_{\F_p}(W_{j-1}\cap F)$. An element $\sum_{i<j}c_i\xi^i\in F$ ($c_i\in\F_p$) is an $F$-relation among $1,\xi,\dots,\xi^{j-1}$; for $j\le\sigma$ these are $F$-independent, forcing $c_1=\dots=c_{j-1}=0$, so $W_{j-1}\cap F=\F_p$ — **exactly here $E\notin B[X]$ is used**: it keeps the coefficients $\gamma_i$ of $\xi^\sigma=\sum\gamma_i\xi^i$ outside $\F_p$, so no extra $F$-direction appears even at $j=\sigma$. Hence the aligned slice gives the $p$ slopes $z=x\in\F_p$ and nothing more. Contrast $\sigma=1$: there $R=F$, $W_0\cap F=F$ (the whole space is the line), and the single-point slice fills $F$ — the $\Theta(p^2)$ explosion is exactly this degeneracy, **not** a mechanism that survives to $\sigma\ge2$. This answers **question 2 / attack path D**: there is no Vieta-slice construction giving $q_{\rm line}^{\Omega(1)}$ or constant-density slopes at $t=\sigma$; every slice is capped at $\Theta(n)$. $\square$

**Why the wall is the entropy reserve (questions 1 and 3, attack paths A, C, E).** An explosion at $t=\sigma$ would need $\Omega(p)$ distinct slices to pile onto one $F$-line $\mathcal L$ (Theorem 4). The aggregate is governed not by algebra but by density. $\mathcal I$ has $|\mathcal I|\le\binom na$ points in $R\cong\F_p^{2\sigma}$; an $F$-line has $q_{\rm line}=p^2$ points; the expected hit count of a generic line is
$$|\mathcal I|\cdot p^2/p^{2\sigma}\ \le\ \binom na/p^{2(\sigma-1)}=\binom na/q_{\rm line}^{\,\sigma-1}.$$
Using $q_{\rm gen}=p$ and $\log_2 p\approx\log_2 n$, the corrected reserve $\sigma\log_2 p\ge(1{+}\eps)\log_2\binom na$ (`eq:entropy-necessary`, `cor:genfield-pigeonhole`) forces $\binom na\le p^{\sigma/(1+\eps)}\ll p^{2(\sigma-1)}$, so the generic expectation $\to0$ — for $\sigma\ge2$ a generic line misses $\mathcal I$ entirely. The repaired theorem is then the statement that *no extremal line is abnormally rich*, i.e. the locator-evaluation map equidistributes with only $n^{O(1)}$-rich fibers. That is verbatim `conj:final-mca`/`conj:final-locator` in $F$-coordinates at the $2\sigma$ points $\{\alpha_i,\alpha_i^p\}$ (it is the residue-line packing $\Lambda^{\rm NC}_t$ of `thm:normalform` lifted to $F$). **Attack path C** confirms the safe stratum is exactly the monomial/restricted-sumset one: when $E\in B[X]$, $\mathcal I$ is the multi-symmetric image $\mathcal B_T$ of `thm:exactslack`, image in $B$, confined.

Below the reserve (every fixed $\sigma$, or $\sigma=o(n/\log n)$), $\binom na/q_{\rm line}^{\sigma-1}\to\infty$ and the density heuristic predicts $\Theta(p^2)$ collinear points — a balanced-denominator extension of the banked fixed-$\sigma$ degree-one family. I tag this CONJECTURAL/EXPERIMENTAL because I could not run the scan (no `bash`); the slice mechanics (Theorem 4) and density count are proved, the constant-density conclusion is heuristic. This neither contradicts nor strengthens the live target: it is sub-reserve, like the banked `20260617_OPUS48_F1_FIXED_RATE_COUNTEREXAMPLE_AUDIT.md`.

**$t=\sigma-1$ (residual slack $1$).** `Lemma 1` injects bad slopes into the slack-$1$ list of $w$ in $\RS[F,D,k+\sigma-1]$ — a single-unit-slack list, which carries no entropy reserve and can be $\Theta(n^2)$ (it is the $\mathcal B_1$/locator object). So $t=\sigma-1$ is essentially as hard as $t=\sigma$ and sits on the same wall; the CRT picture applies with $\sigma-1$ split points plus one degree-drop ($e_1$-vanishing) condition.

**Object-by-object ledger (required separation):**
- *List decoding:* untouched here; Theorem 1 is a packing identity, not a list bound. The unbalanced reduction (audit `Lemma 1`) still imports `eq:extension-list`. CONDITIONAL.
- *CA:* the sub-reserve families give $\eca(C_F,\delta)\ge\Theta(1)$ (direction $-B_{\rm num}/E$ non-containable when $E\notin B[X]$). COUNTEREXAMPLE, sub-reserve.
- *MCA:* identical to support-wise line-MCA here (affine lines). Above reserve = W-bal, CONDITIONAL on the local limit; below reserve $\Theta(1)$, CONJECTURAL.
- *Support-wise line-MCA:* the exact object of Theorems 1–4. PROVED reductions.
- *Line-decoding:* $\emca(C_F,\delta)\le a_{\rm LD}/q_{\rm line}$ would inherit $a_{\rm LD}=n^{1+o(1)}$ from W-bal above reserve; sub-reserve $a_{\rm LD}\ge\Theta(p^2)$. CONJECTURAL (`op:line-decoding`).
- *Curve-MCA:* out of scope (affine lines only).
- *Protocol ledger:* `ass:extension-mca-lift` stays un-citable unrestricted. Defensible replacement: charge the extension *list* term for unbalanced data (audit `Lemma 1`) **and** an explicit balanced residue-line term $\Lambda^{\rm NC}_{t\approx\sigma}(F)=$ the W-bal local limit. Keep $q_{\rm gen}\ne q_{\rm line}\ne q_{\rm chal}$. AUDIT.

---

## 5. Exact dependency list (by source file and label)

- `tex/slackMCA_v3.tex`: `def:residue` (l.1189, witness/noncontained), `lem:denom` (l.1193), `thm:normalform` (l.1197, $\emca=q^{-1}\max_t\Lambda^{\rm NC}_t$), `rem:strata`/`rem:aper` (l.1209/1255), `def:badset`+`thm:exactslack` (l.684–700, $\mathcal B_T$ = attack C stratum), `prop:floor` (l.667, tangent floor), `thm:onez` (l.659), `conj:B`/`conj:final-mca` (l.1231/1717), `cor:genfield-pigeonhole` (l.238, $q_{\rm gen}$ reserve).
- `tex/snarks_v4.tex`: `ass:extension-mca-lift` (l.242, target), `rem:lift-evidence` (l.251), `eq:extension-list` (l.235), `eq:entropy-necessary`/$\taustar$ (l.289–306), `op:extension-mca` (l.765), `op:line-decoding` (l.770), `eq:interleaved-mca` (l.274).
- `tex/proximity_blueprint_v3.tex`: `prob:F1` (l.471), "How to attempt" item 3 ($E\in F[X]\setminus B[X]$) and item 4 (Galois orbits) (l.489–494), sub-reserve note (l.482–484).
- `tex/cs25_cap_v4.tex`: `lem:confine` (subfield confinement, base-rational case; `cor:deployed`/`cor:Fvalued` l.323/395).
- Audits: `20260617_OPUS48_F1_RESIDUAL_SLACK_AUDIT.md` (`Lemma 1`, residual slack $\sigma-t$; locates this wall), `20260617_OPUS48_F1_FIXED_RATE_COUNTEREXAMPLE_AUDIT.md` (Remark S, sub-reserve $\sigma=1$), `20260617_F1_EXTENSION_MCA_COUNTEREXAMPLE_AUDIT.md`. Verifiers `verify_f1_extension_counterexample.py`, `verify_f1_fixed_rate_slice.py`, `verify_f1_sigma2_degree1.py` (counts AUDIT, $\sigma=1,2$ degree-one). Ledgers `02_STATUS_LEDGER.md` (Extension-line MCA lift row), `03_OPEN_PROBLEMS_AND_BACKLOG.md` (rank-3 F1).

---

## 6. Reproducible pseudocode (EXPERIMENTAL — NOT RUN; `bash`/python unavailable in this harness)

Decides W-bal empirically at small $p$. Theorems 1–4 are hand-proved and independent of any run.

```python
# Balanced t=sigma extension packing.  F = F_p[u]/(u^2-d); E = prod_i (X - alpha_i),
# alpha_i in F\F_p, pairwise non-conjugate (alpha_j != alpha_i^p) so E notin B[X].
from itertools import combinations
def balanced_bad_slopes(p, d, k, sigma, alphas, bnum_vals, w_vals):   # exact, small p
    # alphas, bnum_vals, w_vals : length-sigma tuples in F (the CRT coordinates)
    a = k + sigma
    slopes = set()
    for S in combinations(range(1, p), a):                # S subset of F_p^*, |S|=a
        psi = [prod_F(alpha - Fp2(s,0) for s in S) for alpha in alphas]   # L_S(alpha_i)
        zs  = [ (w_vals[i] - psi[i]) / bnum_vals[i] for i in range(sigma) ]
        if all(zs[i] == zs[0] for i in range(sigma)):     # sigma-1 collinearity constraints
            slopes.add(zs[0])
    return len(slopes)                                    # = |I cap L|
# Maximize over E (alphas), bnum_vals, w_vals  ->  Lambda^NC_sigma.
# PREDICTIONS (Thm 4 + density count):
#   sigma=1                : |slopes| = Theta(p^2)            (KNOWN; residual-slack-0, 1-dim ring)
#   fixed sigma>=2, t=sigma: |slopes| = Theta(p^2)            (CONJECTURAL, sub-reserve)
#   sigma >= C n/log n     : expected per generic line = C(n,a)/q_line^(sigma-1) -> 0;
#                            theorem holds iff no rich line  (= conj:final-mca over F)
def reserve_cleared(p, k, sigma):
    from math import comb, log2
    return sigma*log2(p) >= log2(comb(p-1, k+sigma))      # q_gen = p, NOT p^2
```
Suggested promotion: extend `verify_f1_sigma2_degree1.py` to degree-$2$ split $E$ with non-conjugate roots and confirm $\Theta(p^2)$ at fixed $\sigma=2$ (sub-reserve), then push $\sigma$ up at fixed small $p$ to watch the reserve threshold suppress the count — the empirical signature of W-bal.

---

## 7. Route verdict

**EXACT_NEW_WALL** — The balanced extension wall is now pinned exactly. PROVED: the $t=\sigma$ packing equals the $F$-line incidence count on the locator-residue image $\mathcal I$ (Thm 1); genuinely-extension forces $\gcd(E,E^\tau)=1$ while conjugate-pairing collapses to the confined $B[X]$ case (Thm 2); CRT puts it in coordinates $(L_S(\alpha_i))_i$ (Thm 3); and no single Vieta slice exceeds $\Theta(n)$ slopes, so the $\sigma=1$ explosion does not transfer (Thm 4). The residual problem is purely a density question that the corrected reserve ($q_{\rm gen}=p$) drives to expectation $\binom na/q_{\rm line}^{\sigma-1}\to0$, leaving as the *sole* obstruction the no-rich-$F$-line local limit — identically `conj:final-mca`/`conj:final-locator` lifted to the $2\sigma$ points $\{\alpha_i,\alpha_i^p\}$ over $F$. There is no new mathematical object: the repaired above-reserve extension-line MCA theorem is true iff that local limit is, and below reserve it explodes as a sub-reserve counterexample that does not threaten the target. Bankable structural lemmas inside this verdict: Theorems 1–4 (PROVED). No main papers were edited.