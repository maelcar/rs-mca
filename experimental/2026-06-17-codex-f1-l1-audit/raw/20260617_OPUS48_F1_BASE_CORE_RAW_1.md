I'll start by reading the file index and then the priority files specified in the task.Let me read the priority audit files and verification scripts in parallel.Now the verification scripts and the balanced CRT audit, plus the residual slack raw which has the key construction details.Let me read the raw residual-slack and balanced-CRT files, plus the status ledger and open problems.I have substantial context from the two prior raw outputs (residual-slack and balanced-CRT) and their audits. Critically, the balanced-CRT audit flagged that its "Theorem 2" conjugate-pairing dichotomy is **false as stated**. Let me verify the load-bearing labels in the actual TeX before writing, so my confinement argument is grounded.This Read tool uses offset/limit, not view_range. Let me adjust.I have enough to write a rigorous answer. I've verified the load-bearing labels directly (`def:residue`, `thm:normalform`, `conj:B`, `rem:aper`, `rem:strata`, `eq:entropy-necessary`/`taustar`, `eq:extension-list`, `ass:extension-mca-lift`/`rem:lift-evidence`, `prob:perfiber`), read the two prior raw outputs (residual-slack and balanced-CRT) and their audits, and noted the audit's two real holes: the conjugate-pairing dichotomy is false as stated, and the slice cap was only argued for aligned directions. My contribution fixes those and pins the wall to the base-field core.

No `bash`/code execution tool is wired up in this session (only `Read`), so all results are hand-proved; pseudocode is marked not-run.

---

# F1 Balanced Extension Denominators: the slope-collision reduction to the base-field core

## 1. Executive verdict (5 lines)

No unconditional theorem and no surviving above-reserve counterexample; the balanced wall collapses onto the base-field core. PROVED: two supports give the **same** extension slope iff $\hat E\mid(L_S-L_{S'})$ where $\hat E:=\mathrm{lcm}(E,E^\tau)\in B[X]$ has degree $\deg G+2\deg E_1\le 2\sigma$ ($E=G\,E_1$, $G\in B[X]$ the conjugate-symmetric core, $E_1$ conjugate-free). Hence distinct bad slopes inject into a **base-field** $(\le2\sigma)$-dimensional symmetric-function readout — the extension creates no new object, only a factor-$\le2$ dimension blow-up. Confinement saves $p^{\deg G}$ on $G$ and **nothing** on $E_1$ (base locators surject onto $F[X]/(E_1)$), correcting the false dichotomy. The repaired above-reserve theorem is therefore implied by `prob:perfiber` at effective prefix $\le2\sigma$; below reserve it explodes ($\sigma=1$ is the $\deg\hat E=2$ degeneracy), matching banked families.

---

## 2. Formal statements

Setup: $B=\F_p=\F_{\qgen}$, $F=\F_{p^2}=\F_p[\alpha]/(\alpha^2-d)=\F_{\qline}$, $\tau:x\mapsto x^p$ the nontrivial $\mathrm{Gal}(F/B)$ element, $D=H\le\F_p^\times$, $n=|H|$, $C_F=\RS[F,D,k]$, $k=\rho n$, $a=k+\sigma$, $s_\delta=a$, $\delta=1-a/n$. Datum $(E,B_{\rm num},w)$ as in `slackMCA_v3.tex:def:residue`, $\deg E=t$, $E\nmid B_{\rm num}$, $E$ nonzero on $D$, $E\in F[X]\setminus B[X]$. Balanced regime $t\in[\sigma-\Theta(n/\log n),\sigma]$. For $g\in F[X]$, $g^\tau$ applies $\tau$ to coefficients. $L_S=\prod_{s\in S}(X-s)\in B[X]$.

**Theorem 1 (Frobenius factorization; PROVED).** Every squarefree $E$ nonzero on $D$ factors uniquely as $E=G\cdot E_1$ with $G\in B[X]$ (monic, the *conjugate-symmetric core*) and $\gcd(E_1,E_1^\tau)=1$ (the *conjugate-free part*). Moreover $E\in B[X]\iff\deg E_1=0$. *(This corrects the false "conjugate-paired vs not" dichotomy: a base factor times an unpaired extension factor has $E\notin B[X]$ yet $\gcd(E,E^\tau)\ne1$.)*

**Theorem 2 (slope-collision = base-field $\hat E$-equivalence; PROVED, the key lemma).** Set $\hat E:=\mathrm{lcm}(E,E^\tau)=G\,E_1E_1^\tau\in B[X]$, $\deg\hat E=\deg G+2\deg E_1$. For the monic degree-$a$ anchor $w$, the support-wise line-MCA bad slopes of $(E,B_{\rm num},w)$ are
$$\{\,z\in F:\ \exists\,S\in\tbinom{D}{a},\ [L_S]_E\in[X^a]_E-z[B_{\rm num}]_E\,\},$$
and two supports $S,S'$ yield the **same slope** iff $\hat E\mid(L_S-L_{S'})$, i.e. $[L_S]_{\hat E}=[L_{S'}]_{\hat E}$ in $B[X]/(\hat E)$. Consequently
$$\#\{\text{bad slopes}\}\ \le\ \#\{\,[L_S]_{\hat E}\in B[X]/(\hat E):\ S\text{ lies on the line}\,\}\ \le\ \min\!\big(\qline,\ |B[X]/(\hat E)|\big)=\min(p^2,p^{\deg\hat E}).$$
Since $\deg\hat E\le 2\sigma$ (with equality iff $E_1$ totally conjugate-free of degree $\sigma$), the distinct-slope count injects into a **base-field** symmetric-readout of $\F_p$-dimension $\le2\sigma$.

**Theorem 3 (corrected confinement; PROVED).** $\mathcal I=\{[L_S]_E\}\subseteq R=F[X]/(E)$ projects under CRT $R\cong F[X]/(G)\times F[X]/(E_1)$ to: (i) the $G$-part lies in the $B$-form $B[X]/(G)$, $\dim_{\F_p}=\deg G$ — confined, saving $p^{\deg G}$; (ii) the $E_1$-part is **all** of $B[X]/(E_1E_1^\tau)\cong F[X]/(E_1)$, $\dim_{\F_p}=2\deg E_1$ — **no confinement**. Thus the unconfined extension danger is carried exactly by $\deg E_1$, and `cs25_cap_v4.tex:lem:confine` deflates only the $G$-part.

**Theorem 4 (slice cap, $\sigma=2$ split, arbitrary direction; PROVED).** For $E=(X-\alpha)(X-\beta)$, $\alpha,\beta\in F\setminus B$ non-conjugate, any fixed tail $T$ ($|T|=a-2$) and any direction $(b_1,b_2)=(B_{\rm num}(\alpha),B_{\rm num}(\beta))\ne0$, the Vieta slice $\{x,y\}\mapsto z$ obeys one $F$-linear equation in $(e_1',e_2')=(x{+}y,xy)\in\F_p^2$, hence has $\le p$ solutions; the slice contributes $\le p=\Theta(n)$ slopes. The $\Theta(n)$ rate is realized exactly when the two recorded $F$-functionals are $\F_p$-proportional (a one-parameter choice of $T$). *No single algebraic slice (any direction) reaches $\qline^{\Omega(1)}$ or constant density.*

**Exact wall (EXACT_NEW_WALL, restated and sharpened).** Above the corrected reserve $\sigma\ge Cn/\log n$ (equivalently `eq:entropy-necessary` with $\qgen=p$: $\sigma\log_2p\gtrsim\log_2\binom na$), the repaired balanced extension-line MCA bound $\Lambda^{\rm NC}_{t,\delta}(D,k)\le n^{1+o(1)}$ holds **iff** the base-field readout $S\mapsto[L_S]_{\hat E}\in B[X]/(\hat E)$ has $\le n^{1+o(1)}$-rich fibers along any line — i.e. `prob:perfiber` with prefix length $\sigma$ replaced by readout dimension $\deg\hat E\le2\sigma$. This is `conj:B`/`conj:final-mca` read at the $\le2\sigma$ Frobenius coordinates; the extension multiplies the recorded base dimension by $\le2$ and changes no threshold order.

---

## 3. Full parameter ledger

| symbol | meaning | value / regime |
|---|---|---|
| $B$ | base = generated = entropy field | $\F_p$ |
| $F$ | extension = line = witness field | $\F_{p^2}=\F_p[\alpha]/(\alpha^2-d)$, $d$ nonsquare |
| $\qgen$ | generated/entropy field size (pigeonhole, `eq:entropy-necessary`) | $p$ — **never replaced by $F$** |
| $\qline$ | line-experiment field (slopes sampled) | $p^2$ |
| $\qchal$ | verifier challenge field | $=\qline$ only after a protocol proof |
| $H=D$ | evaluation subgroup, $H\subseteq\F_p^\times$ | $n=|H|$ |
| $k,\rho;\ a,\sigma$ | dimension, rate; agreement, slack | $k=\rho n$, $\rho\in\{1/2,1/4\}$; $a=k+\sigma$ |
| $\delta,\eta$ | radius, reserve | $\delta=1-a/n$, $\eta=\sigma/n$ |
| corrected reserve | regime of interest | $\sigma\log_2\qgen\ge(1{+}\eps)\log_2\binom na$, i.e. $\sigma\ge Cn/\log n$ |
| $t=\deg E$ | denominator degree | balanced $t\in[\sigma-\Theta(n/\log n),\sigma]$ |
| $E=G\,E_1$ | denom = sym-core $\times$ conj-free | $G\in B[X]$, $\gcd(E_1,E_1^\tau)=1$, $E\notin B[X]\iff\deg E_1\ge1$ |
| $\hat E$ | $\mathrm{lcm}(E,E^\tau)\in B[X]$ | $\deg\hat E=\deg G+2\deg E_1\le2\sigma$ — **effective readout dim** |
| $\mu,\nu,e$ | list arity, interleaving, $[F:B]$ | $1,1,2$ |

---

## 4. Proof / obstruction analysis (answers to questions 1–3, paths A–E)

**Theorem 1.** Take $G:=\gcd(E,E^\tau)$ monic; $G^\tau=\gcd(E^\tau,E)=G$ so $G\in B[X]$. Put $E_1=E/G$; since $E$ is squarefree and $G\in B[X]$, $E^\tau/G=E_1^\tau$ and $\gcd(E_1,E_1^\tau)=\gcd(E,E^\tau)/G=1$. $E\in B[X]\iff E=E^\tau\iff E_1=E_1^\tau$, which with coprimality forces $\deg E_1=0$. $\square$ (Path B settled: products $(X-\alpha_i)(X-\alpha_i^\tau)$ are exactly the $G$-part, land in $B[X]$, and are confined; "genuinely extension" $=\deg E_1\ge1$.)

**Theorem 2 (load-bearing).** At $t=\sigma$ the witness degree budget is $\deg Q_z<k+t=a$ with $|S|\ge a$, so $Q_z=\mathrm{interp}_S(w)$ is *forced* and equals $X^a-L_S$ for monic $w$ (`def:residue`; residual slack $0$, so the residual-slack reduction `..._RESIDUAL_SLACK_AUDIT.md` Lemma 1 gives nothing — this is *why* $t=\sigma$ is the wall). The bad condition is $[X^a-L_S]_E=z[B_{\rm num}]_E$, one $z$ per $S$ when $[B_{\rm num}]_E\ne0$. Equal slopes $\iff[L_S]_E=[L_{S'}]_E\iff E\mid(L_S-L_{S'})$. As $L_S-L_{S'}\in B[X]$, applying $\tau$ gives $E^\tau\mid(L_S-L_{S'})$, hence $\hat E=\mathrm{lcm}(E,E^\tau)\mid(L_S-L_{S'})$; conversely $\hat E\mid g\Rightarrow E\mid g$. So slope-equality is the **base-field** congruence $[L_S]_{\hat E}=[L_{S'}]_{\hat E}$, $\hat E\in B[X]$, $\deg\hat E\le2\sigma$. $\square$

**Theorem 3.** $\phi:B[X]\to F[X]/(E_1)$ has kernel $\{g\in B[X]:E_1\mid g\}=(E_1E_1^\tau)\cap B[X]=(E_1E_1^\tau)_{B[X]}$, so $\mathrm{im}\,\phi\cong B[X]/(E_1E_1^\tau)$, $\dim_{\F_p}=2\deg E_1=\dim_{\F_p}F[X]/(E_1)$: surjective. So base locators are unconfined on $E_1$. On $G\in B[X]$, $[L_S]_G\in B[X]/(G)$, the $B$-form, $\dim_{\F_p}=\deg G<2\deg G$: confined. $\square$ (This is the correct replacement for the audited-false dichotomy and `rem:lift-evidence`(ii): the known $\F_{\qgen}$-valued families live in the $G$/base stratum; the open danger is the $E_1$ stratum.)

**Theorem 4 + question 2/path D.** With $L_S=L_T(X-x)(X-y)$, $L_S(\gamma)=L_T(\gamma)(\gamma^2-e_1'\gamma+e_2')$. The collinearity $b_2L_S(\alpha)-b_1L_S(\beta)=\kappa$ is $\F_p$-affine in $(e_1',e_2')$ with $F$-coefficients $-(b_2L_T(\alpha)\alpha-b_1L_T(\beta)\beta)$ and $(b_2L_T(\alpha)-b_1L_T(\beta))$; generic rank $2$ over $\F_p\Rightarrow\le1$ solution, engineered rank $1\Rightarrow\le p$. So $\le\Theta(n)$ per slice, **any** direction — there is no Vieta-slice route to large balanced families. $\square$

**Questions 1 & 3 (density/reserve, paths A, C, E).** By Theorem 2, $\#\text{slopes}=|\mathcal L\cap\mathcal I|$ for an affine $F$-line $\mathcal L$ (the $p^2$ points $[X^a]_E-z[B_{\rm num}]_E$) meeting $\mathcal I=\{[L_S]_E\}$, and distinct slopes inject into the base-field image $\{[L_S]_{\hat E}\}\subseteq B[X]/(\hat E)$, $|\cdot|\le p^{\deg\hat E}$. The generic expected hit of one line on $\mathcal I$ is $\le\binom na\,p^2/p^{2\sigma}=\binom na/\qline^{\,\sigma-1}$. Above reserve, `eq:entropy-necessary` with $\qgen=p$ gives $\binom na\le p^{\sigma/(1{+}\eps)}\ll p^{2(\sigma-1)}$, so the generic line **misses** $\mathcal I$ ($\sigma\ge2$). The theorem needs the *worst* line, i.e. the no-rich-fiber statement for the readout $S\mapsto[L_S]_{\hat E}$ on $a$-subsets of $H\subseteq\F_p^\times$ — a $\le2\sigma$-dimensional $\F_p$-linear readout of subset symmetric functions. That is the per-fiber collision problem `prob:perfiber` with $\sigma\rightsquigarrow\deg\hat E\le2\sigma$. A larger prefix only *strengthens* the constraint (smaller fibers), so:

> **Conditional theorem (CONDITIONAL on `prob:perfiber`).** If the base-field per-fiber bound holds at prefix $2\sigma$ (no harder than at $\sigma$), then $\Lambda^{\rm NC}_{t,\delta}\le n^{1+o(1)}$ for all balanced extension data above the corrected reserve. **Question 1: NO** — balanced $t=\sigma$ cannot produce $>n^{1+o(1)}$ extension-valued bad slopes above reserve unless the base core itself fails. **Question 2: NO** Vieta-slice construction reaches $\qline^{\Omega(1)}$ (Theorem 4). **Question 3: YES** the packing bound is provable from the base core via Theorem 2.

**Sub-reserve / $\sigma=1$ sanity check (PROVED consistency).** $\sigma=1$, $E=X-\alpha$ ($\alpha\notin B$): $G=1$, $E_1=X-\alpha$, $\hat E=(X-\alpha)(X-\alpha^\tau)$, $\deg\hat E=2$. Effective dim $2=2\sigma$ is tiny vs $\binom na$, no reserve, fibers huge $\Rightarrow\Theta(p^2)$ slopes — exactly the banked `..._FIXED_RATE_COUNTEREXAMPLE_AUDIT.md`. Every fixed-$\sigma$ family has $\deg\hat E\le2\sigma=O(1)\ll$ budget: explosion, but sub-reserve, no threat to the above-reserve target. **The $\sigma=1$ blow-up is precisely the $\deg\hat E=2$ degeneracy and provably does not transfer above reserve.**

**$t=\sigma-1$ (residual slack 1).** Lemma 1 (`..._RESIDUAL_SLACK_AUDIT.md`) injects bad slopes into the slack-$1$ list of $w$ in $\RS[F,D,k+\sigma-1]$; the same $\hat E$ analysis applies with $\deg E=\sigma-1$, $\deg\hat E\le2(\sigma-1)$. It sits on the identical wall, one degree-drop constraint lighter — no separate obstruction.

**Object-by-object ledger (required separation).**
- **List decoding:** untouched; Theorem 2 is a slope-collision identity, not a list bound. Unbalanced data still import `eq:extension-list`. (CONDITIONAL)
- **CA:** sub-reserve families give $\eca(C_F,\delta)\ge\Theta_\sigma(1)$ (direction $-B_{\rm num}/E$ non-containable when $E\notin B[X]$). (COUNTEREXAMPLE, sub-reserve)
- **MCA:** above reserve $=$ the conditional theorem (CONDITIONAL on `prob:perfiber` at prefix $\le2\sigma$); below reserve $\Theta(1)$ density (PROVED for $\sigma=1$, CONJECTURAL for fixed $\sigma\ge2$ split).
- **Support-wise line-MCA:** the exact object of Theorems 2–4. (PROVED reductions)
- **Line-decoding:** $\emca\le a_{\rm LD}/\qline$ would inherit $a_{\rm LD}=n^{1+o(1)}$ above reserve, $\ge\Theta(p^2)$ sub-reserve. (CONJECTURAL, `op:line-decoding`)
- **Curve-MCA:** out of scope (affine lines only). (N/A)
- **Protocol ledger:** `ass:extension-mca-lift` stays un-citable unrestricted. Defensible replacement: charge the extension **list** term for unbalanced data (`eq:extension-list`) **and** a balanced **base-core** term = `prob:perfiber` at prefix $\le2\sigma$. Keep $\qgen\ne\qline\ne\qchal$. (AUDIT)

---

## 5. Exact dependency list (by source file and label)

- `tex/slackMCA_v3.tex`: `def:residue` (l.1189, witness/noncontained, $\Lambda^{\rm NC}_{t,\delta}$), `lem:denom` (l.1193), `thm:normalform` (l.1197, $\emca=\frac1q\max_t\Lambda^{\rm NC}_t$ — Theorem 2 instantiates this over $F$), `thm:closure` (l.1213), `rem:strata` (l.1209, $\mathcal B_T$ stratum = path C / the $G$-confined case via `thm:exactslack`), `prob:perfiber` (l.1227, **the base core my reduction targets**), `conj:B` (l.1231, slack-MCA threshold; $q_{D,n}=\qgen$, reserve $\eta\ge(1{+}\eps)\taustar(\rho,\qgen)$), `rem:aper` (l.1255, quotient-periodic separation), `conj:final-mca`/`conj:final-locator` (referenced by `rem:aper`).
- `tex/snarks_v4.tex`: `ass:extension-mca-lift` (l.242, target), `rem:lift-evidence` (l.251, esp. (ii) — corrected by Theorem 3), `eq:extension-list` (l.235), `eq:entropy-necessary`+`taustar` (l.290–306, **uses $\qgen$ not $\qline$**), `op:extension-mca` (l.765, `sec:mca-objects`), `op:line-decoding` (l.265/770), `eq:interleaved-mca` (l.274).
- `tex/proximity_blueprint_v3.tex`: `prob:F1` (l.471), "How to attempt" item 3 ($E\in F[X]\setminus B[X]$) and item 4 (Galois orbits → Theorem 1), sub-reserve note (l.482–484).
- `tex/cs25_cap_v4.tex`: `lem:confine` (subfield confinement, base-rational/$G$-part case; used in Theorem 3).
- Audits: `20260617_OPUS48_F1_RESIDUAL_SLACK_AUDIT.md` (Lemma 1 residual slack $\sigma-t$; located this wall), `20260617_OPUS48_F1_FIXED_RATE_COUNTEREXAMPLE_AUDIT.md` (Remark S / sub-reserve $\sigma=1$), `20260617_OPUS48_F1_BALANCED_CRT_AUDIT.md` (its holes 1–4 fixed here: Thm 1 monic-only → general anchor noted; false dichotomy → Theorem 1; aligned-only slice → Theorem 4), `20260617_F1_EXTENSION_MCA_COUNTEREXAMPLE_AUDIT.md`. Verifiers `verify_f1_fixed_rate_slice.py`, `verify_f1_sigma2_degree1.py`, `verify_f1_extension_counterexample.py` (counts AUDIT). Ledgers `02_STATUS_LEDGER.md`, `03_OPEN_PROBLEMS_AND_BACKLOG.md` (rank-3 F1).

---

## 6. Reproducible pseudocode (EXPERIMENTAL — NOT RUN; no code tool in this session)

Decides the wall empirically at small $p$; Theorems 1–4 are hand-proved and run-independent.

```python
# Balanced t=sigma extension packing via the hat_E base-field readout (Theorem 2).
# F = F_p[u]/(u^2-d).  E in F[X]\B[X], squarefree, nonzero on H.
from itertools import combinations
def hatE_readout_collisions(p, d, k, sigma, E_coeffs_F):   # exact, small p
    F = make_Fp2(p, d); a = k + sigma
    G  = gcd_F(E_coeffs_F, frobenius(E_coeffs_F))          # conj-symmetric core (in B[X])
    E1 = polydiv_F(E_coeffs_F, G)                          # conj-free part
    hatE = lcm_F(E_coeffs_F, frobenius(E_coeffs_F))        # = G*E1*E1^tau in B[X], deg<=2*sigma
    classes = {}                                           # [L_S]_hatE  ->  one representative slope
    for S in combinations(H_elements(p), a):
        LS  = prod_poly([(X - s) for s in S])              # in B[X]
        key = poly_mod(LS, hatE)                           # base-field B[X]/(hatE) class
        z   = slope_from(LS, E_coeffs_F)                   # ([X^a]-[L_S]) / [Bnum]  in F  (None if off-line)
        if z is not None: classes.setdefault(key, z)
    return len(set(classes.values())), len(hatE)-1         # #distinct slopes, deg hatE
# PREDICTIONS (Thm 2 + reserve, q_gen = p NOT p^2):
#   deg hatE = deg G + 2 deg E1 <= 2*sigma                                  (PROVED)
#   sigma=1 (deg hatE=2):                 #slopes = Theta(p^2)               (PROVED, sub-reserve)
#   fixed sigma>=2, E1 conj-free:         #slopes = Theta(p^2)               (CONJECTURAL, sub-reserve)
#   sigma>=C n/log n:  E[#hits/line] <= C(n,a)/q_line^(sigma-1) -> 0;
#                      #slopes <= n^{1+o(1)}  iff prob:perfiber holds at prefix deg hatE<=2 sigma
def reserve_cleared(p, k, sigma):
    from math import comb, log2
    return sigma*log2(p) >= log2(comb(p-1, k+sigma))       # eq:entropy-necessary, q_gen=p
```
Suggested promotion: extend `verify_f1_sigma2_degree1.py` to (a) split non-conjugate $E=(X-\alpha)(X-\beta)$ and (b) base$\times$extension $E=(X-c)(X-\beta)$, confirm $\deg\hat E=4$ resp. $3$ and $\Theta(p^2)$ sub-reserve slopes, then push $\sigma$ up at fixed small $p$ to watch the count drop as the readout fibers thin — the empirical signature of the wall.

---

## 7. Route verdict

**BANKABLE_LEMMA.**

The new PROVED content is bankable and was not in the prior two F1 answers: (1) the **Frobenius factorization** $E=G\,E_1$ correcting the audited-false conjugate-pairing dichotomy (Theorem 1); (2) the **corrected confinement** — saving $p^{\deg G}$ on the symmetric core and *none* on the conjugate-free part, which surjects (Theorem 3); (3) the **slope-collision identity** $z_S=z_{S'}\iff[L_S]_{\hat E}=[L_{S'}]_{\hat E}$ in $B[X]/(\hat E)$ with $\deg\hat E=\deg G+2\deg E_1\le2\sigma$ (Theorem 2); and (4) the **arbitrary-direction slice cap** $\Theta(n)$ at $\sigma=2$ (Theorem 4). Together these reduce the balanced extension wall — above the corrected reserve — to the **base-field per-fiber collision core `prob:perfiber` at effective prefix $\le2\sigma$**, with $\qgen=p$ (never $\qline$) driving the reserve and the extension costing only a factor-$\le2$ in recorded dimension.

**Do I see a route to a full solve?** A full *unconditional* solve of the balanced wall is not available here, and the obstruction is now exactly located: the balanced extension-line MCA bound above reserve is **equivalent in difficulty to `prob:perfiber`** (the acknowledged hard open core of the entire monomial program), differing only by the factor-$\le2$ effective-dimension blow-up which does not change the $n/\log n$ threshold order. So F1-balanced introduces **no new field-extension obstruction** — it is solved *relative to* the base core. The route to a full solve is therefore: prove `prob:perfiber` (equivalently, the no-rich-fiber bound for the $\F_p$-symmetric-function readout) at prefix $2\sigma$; then Theorem 2 closes F1-balanced for $t\in\{\sigma,\sigma-1\}$ and, with Lemma 1, all unbalanced $t$. No main papers were edited.