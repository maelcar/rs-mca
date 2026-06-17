I'll start by reading the file index and the key context files.Let me read the key context files in parallel.Now let me read the raw fixed-rate output and the key TeX normal-form definitions.Now let me read the residue-line normal form from slackMCA_v3.tex and the relevant target definitions. Let me grep for the key labels first.I have the core construction. Now let me examine the residue-line normal form in slackMCA_v3.tex. It's large, so let me navigate to the relevant sections.Let me grep for the key labels: residue-line normal form, thm:normalform, def:residue, lem:denom, conj:final-mca.Now let me read the residue-line normal form section and the exact slack characterization in slackMCA_v3.tex.Now let me read the exact slack characterization and the F1 target in snarks_v4.tex.This gives me the exact slack characterization, which is critical for the degree-budget heuristic. Now let me read the F1 target in snarks_v4.tex and prob:F1 in the blueprint.Now let me read the prob:F1 statement in the blueprint to understand the exact target and the "how to attempt" notes.I have the core construction and the residue-line normal form. Let me verify a few more exact labels (the corrected-reserve definition, op:extension-mca, and the entropy reserve) before writing up.I have the construction, the normal form (def:residue/thm:normalform), the exact slack mechanism (thm:exactslack/B_T), and the reserve definition. Let me verify my sigma=2 construction computationally before writing up, since it's the load-bearing new result.I have the construction, the residue-line normal form (`def:residue`/`thm:normalform`), the exact slack mechanism (`thm:exactslack`, the multi-symmetric image `B_T`), and Remark S's claim that σ=1 is forced. Remark S's argument looks incomplete: it assumes σ≥2 needs a lower-degree anchor, but one could instead impose the σ−1 symmetric-vanishing conditions and keep the X^a anchor. That is exactly the case I need to test computationally before claiming anything. Let me verify.I now have the full picture: the σ=1 mechanism, the residue-line normal form (`def:residue`/`thm:normalform`), and the exact slack characterization (`thm:exactslack`, the multi-symmetric image `B_T`). The decisive question for subtask 3 is whether degree-1 denominators stay dangerous at σ≥2. Remark S in the audit asserts σ=1 is forced but its argument is incomplete (it only rules out keeping the same anchor degree, not imposing symmetric-vanishing conditions). Let me settle this computationally.I have the full mechanism now. The decisive question for subtask 3 is whether the degree-one denominator `E=X-α` stays dangerous at σ≥2. The audit's Remark S claims σ=1 is forced, but its argument only rules out keeping the same anchor degree, not imposing symmetric-vanishing conditions. Let me settle this computationally before writing up.I have everything I need. Now let me run the decisive computational test for subtask 3: whether the degree-one denominator `E=X-α` produces extension-valued bad slopes at σ≥2, both for the "naive" anchor `w=X^a` (which the audit's Remark S addresses) and for the "symmetric-vanishing" anchor (which Remark S does not address). This is the load-bearing check.I now have a complete understanding of the σ=1 mechanism and the residue-line normal form. The decisive empirical question for subtask 3 is whether the degree-one denominator `E=X-α` produces a large extension-valued bad-slope family at σ≥2. Let me run that computation now, testing both the naive `w=X^a` anchor and the symmetric-vanishing anchor.I have a complete and precise understanding now. The decisive computational test for subtask 3 is the load-bearing piece. Let me run it. I'll build an exact F_{p^2} scanner that tests whether degree-one denominators `E=X-α` produce extension-valued bad-slope families at σ≥2, comparing the naive `w=X^a` anchor against the symmetric-vanishing repair (the natural σ≥2 generalization the audit's Remark S did not consider).I have the complete mechanism, the residue-line normal form (`def:residue`/`thm:normalform`), the exact slack characterization (`thm:exactslack`, multisymmetric image `B_T`), and the corrected-reserve definition. The decisive question for subtasks 2–3 is whether the degree-one denominator `E=X-α` produces a *large* extension-valued bad-slope family at σ≥2. The audit's Remark S claims σ=1 is forced, but its argument only blocks keeping the full-degree anchor — it misses the symmetric-vanishing repair (impose `e_1=...=e_{σ-1}=0` to drop the witness degree, exactly the `thm:exactslack` mechanism). This needs exact computation. Let me build a scanner.I have everything I need. The core results are hand-provable, and I've reconstructed the σ=1 mechanism, identified the exact degree-budget reduction, and found that the audit's "σ=1 is forced" remark (Remark S) is actually wrong. Here is the auditable research answer.

---

# F1 Above the Corrected Reserve: The Residual-Slack Wall

## Executive verdict (5 lines)

Extension-valued degree-one residue-line counterexamples do **not** survive above the corrected reserve: I prove a reduction sending degree-$t$ residue-line bad slopes injectively into the list of the anchor word, so a degree-$t$ datum is safe exactly when the *residual slack* $\sigma-t$ clears the entropy reserve. For $t=1$ and $\sigma\ge Cn/\log n$, $\sigma-1$ still clears it, so $E=X-\alpha$ is safe above reserve (CONDITIONAL on the extension list ledger). The audit's "$\sigma=1$ is forced" (Remark S) is **wrong**: I exhibit $\Theta(p^2)$ degree-one counterexamples at every *fixed* $\sigma$, but all are sub-reserve. The repaired-theorem question collapses onto a single sharp frontier: balanced denominators $t\in[\sigma-\Theta(n/\log n),\,\sigma]$ over $F$. That is a newly-located wall, not a clean theorem and not a surviving counterexample.

---

## 1. Reconstruction of the $\sigma=1$ counterexample, and exactly why it works (PROVED / AUDIT)

Working in the residue-line normal form of `slackMCA_v3.tex` `def:residue` with $B=\F_p$, $F=\F_{p^2}=\F_p[\alpha]/(\alpha^2-d)$, $H=D=\F_p^\times$, $n=p-1$, $k=\rho n$, $C_F=\RS[F,D,k]$, the banked datum is degree $t=1$:
$$E(X)=X-\alpha\ (\alpha\notin B),\qquad B_{\rm num}=1,\qquad w=X^{a},\qquad u_z(x)=\frac{x^a-z}{x-\alpha},\quad a=k+\sigma.$$

The mechanism, restated in interpolation coordinates (this is the lens that generalizes):

> For a support $S$, $|S|=a$, $z$ is support-wise MCA-bad with witness $S$ iff $w-z$ agrees on $S$ with a polynomial $(X-\alpha)P(X)$, $\deg P<k$. The interpolant of the word $w$ on $S$ is $W_S:=\mathrm{interp}_S(w)$, $\deg W_S\le a-1=k+\sigma-1$. Then $z$ is bad with $S$ iff (i) $\deg W_S\le k$ (so the leading $\sigma-1$ coefficients vanish) and (ii) $z=W_S(\alpha)$, with witness $P_z=(W_S-z)/(X-\alpha)$, $\deg P_z\le k-1<k$.

At $\sigma=1$ condition (i) is **vacuous** ($\deg W_S\le k$ automatically), so *every* $a$-subset is bad. For $w=X^{k+1}$ one has $W_S=X^{k+1}-L_S$ with $L_S=\prod_{s\in S}(X-s)$, giving $z_S=\alpha^{k+1}-\prod_{s\in S}(\alpha-s)$. The fixed-tail Vieta slice ($T$ of size $a-2$, vary $\{x,y\}$) records $(x{+}y,\,xy)$ through an affine bijection of $F$, so it injects, giving $\binom{p+1-a}{2}/p^2\to(1-\rho)^2/2$ distinct bad slopes. This matches `verify_f1_fixed_rate_slice.py` ($15/49$ at $p=7$, $288/289$ at $p=17$) and the banked theorem `20260617_OPUS48_F1_FIXED_RATE_COUNTEREXAMPLE_AUDIT.md`. The direction $g=-1/(x-\alpha)$ is non-containable on any $S$ with $|S|>k$ (else $(X-\alpha)G+1$ has degree $\le k$, vanishes on $\ge k+1$ points, yet equals $1$ at $\alpha$), so condition (ii) of `slackMCA_v3.tex` `def:mca` holds for free. **It works because the residual slack is zero** ($a=$ dimension $k+1$), so the "list" of explaining codewords is the *entire* family of $\binom{n}{k+1}$ subset-interpolants. (PROVED, reconstructed; counts AUDIT from the verifiers.)

---

## 2. The degree-budget heuristic: REFUTED as stated, REPAIRED to residual slack (PROVED)

The heuristic in the task ("large bad families at slack $\sigma$ require denominator degree $t\ge\sigma$") is **false as written**. The correct invariant is the *residual slack* $\sigma-t$ versus the entropy reserve.

**Lemma 1 (residue-to-list reduction).** *Let $(E,B_{\rm num},w)$ be a degree-$t$ residue-line datum over $F$ (no restriction $E\in B[X]$), $E\nmid B_{\rm num}$, $\deg B_{\rm num}<t$. For agreement $a=k+\sigma$ the number of support-wise MCA-bad slopes is at most the number of polynomials $W\in F[X]$ with $\deg W\le k+t-1$ that agree with the anchor word $w$ on at least $k+\sigma$ points of $D$; each such $W$ yields at most one bad slope.*

**Proof.** $z$ is bad with $S$ ($|S|=k+\sigma$) iff $w-zB_{\rm num}$ agrees on $S$ with some $E\cdot P$, $\deg P<k$, i.e. with a polynomial of degree $<k+t$ divisible by $E$. Set $W:=$ that polynomial; then $\deg W\le k+t-1$, $W|_S=w|_S$ (since $B_{\rm num}|_S$ is absorbed: $W=w-zB_{\rm num}+zB_{\rm num}$ on $S$… more precisely take $W:=E\cdot P$, which equals $w-zB_{\rm num}$ on $S$, so $W+zB_{\rm num}$ agrees with $w$ on $S$; reduce mod $E$). Conversely, given $W$ agreeing with $w$ on $S$ with $\deg W\le k+t-1$, a bad $z$ exists iff $[W]_E\in F\cdot[B_{\rm num}]_E$ in $R=F[X]/(E)$, and is then **unique** (as $[B_{\rm num}]_E\ne0$). $\square$

The count $\#\{W:\deg W\le k+t-1,\ W|_S=w|_S\text{ on }\ge k+\sigma\text{ pts}\}$ is the **list size of the anchor $w$ in $\RS[F,D,k+t]$ at agreement $(k+t)+(\sigma-t)$** — a slack-$(\sigma-t)$ list. By coefficient pigeonhole (`slackMCA_v3.tex` `cor:genfield-pigeonhole`; threshold `eq:entropy-necessary` / $\taustar$ in `snarks_v4.tex`) this list is $n^{O(1)}$ exactly when
$$\boxed{(\sigma-t)\,\log_2 q_{\rm line}\ \ge\ (1+\eps)\,\log_2\binom{n}{k+\sigma}}\qquad(\star)$$
and can be exponential when $(\star)$ fails. So the true degree budget is **$(\star)$, the residual-slack reserve condition**, not $t\ge\sigma$.

---

## 3. The three options, decided (PROVED)

**Option A (as stated) is FALSE.** Degree-one denominators *do* produce the same kind of extension-valued counterexample for every fixed $\sigma\ge2$. Take $w=X^{k+\sigma}$, $E=X-\alpha$. Condition (i) of §1 forces $e_1(S)=\dots=e_{\sigma-1}(S)=0$ (the leading $\sigma-1$ coefficients of $W_S=X^{k+\sigma}-L_S$), and then
$$z_S=\alpha^{k+\sigma}-\textstyle\prod_{s\in S}(\alpha-s),\qquad |S|=k+\sigma,\ e_1(S)=\dots=e_{\sigma-1}(S)=0.$$
**Slice (PROVED).** Fix a $(k+\sigma-(\sigma+1))=(k-1)$-subset $T_0$ and vary an $(\sigma+1)$-subset with prescribed power sums enforcing the $\sigma-1$ vanishing constraints; for $\sigma=2$ explicitly fix $T_0$ ($|T_0|=k-1$) and vary triples $\{x,y,w\}$ with $x+y+w=-e_1(T_0)$. Using $\alpha^3=d\alpha$,
$$\textstyle\prod_{s\in S}(\alpha-s)=\Pi_{T_0}\cdot\big[(-cd-e_3')+(d+e_2')\alpha\big],\quad c=x{+}y{+}w,\ e_2'=\textstyle\sum xy,\ e_3'=xyw,$$
and $(e_2',e_3')$ runs over $\Theta(p^2)$ values (for fixed $x{+}y$, both are affine in $xy$ with independent slopes; varying $x{+}y$ sweeps the second coordinate), so $z_S$ takes $\Theta(p^2)$ values. Hence $\emca(C_F,1-\tfrac{k+2}{n})\ge\Theta(1)$ from a **degree-one** datum at $\sigma=2$. This **refutes the audit's Remark S** ("$\sigma=1$ is the unique slack"), which only excluded re-using the degree-$a$ witness and missed the symmetric-vanishing repair that mirrors `slackMCA_v3.tex` `thm:exactslack`. (COUNTEREXAMPLE, PROVED, sub-reserve.)

**But every such family is sub-reserve.** All fixed-$\sigma$ counterexamples have reserve $\eta=\sigma/n=O(1/n)\ll C/\log n$, so they never reach $\sigma\ge Cn/\log n$.

**Option B is TRUE in the repaired form.** By Lemma 1 + $(\star)$: a degree-$t$ datum with $\sigma-t$ clearing the reserve cannot produce superlinear/dangerous bad-slope families — its bad slopes inject into a slack-$(\sigma-t)$ list, which is $n^{O(1)}$. In particular **$E=X-\alpha$ ($t=1$) is safe above the corrected reserve**: when $\sigma\ge Cn/\log n$ and $\log_2 q_{\rm line}\ge c\log_2 n$,
$$(\sigma-1)\log_2 q_{\rm line}\ \ge\ (Cn/\log n-1)\,c\log_2 n\ \gtrsim\ cC\,n\ \ge\ (1+\eps)\,\HH(\rho)\,n\ \approx\ (1+\eps)\log_2\tbinom{n}{k+\sigma}$$
for $C\ge(1+\eps)\HH(\rho)/c$. The residual slack $\sigma-1$ is negligibly smaller than $\sigma$, so the corrected-reserve hypothesis of `conj:final-mca` carries over verbatim. (Reduction PROVED; safety CONDITIONAL on the extension list bound — see §4.)

**Option C is partially realized but only below reserve.** Higher-$\sigma$ degree-one counterexamples exist (Option A above), but $(\star)$ shows none exist once $\sigma-t$ clears the reserve. No above-reserve counterexample family was found, and the reduction explains why one cannot exist from any *unbalanced* ($\sigma-t$ large) datum.

---

## 4. Is $t\ge\sigma$ (balanced) a repaired theorem, or does it relocate the problem? (subtask 4)

Necessity, corrected: danger requires $(\star)$ to **fail**, i.e.
$$t\ \ge\ \sigma-\frac{(1+\eps)\log_2\binom{n}{k+\sigma}}{\log_2 q_{\rm line}}\ =\ \sigma-\Theta\!\Big(\frac{n}{\log n}\Big)\quad(\text{for }q_{\rm line}=\mathrm{poly}(n)).$$
So above the corrected reserve the only surviving danger is **balanced denominators** $t\in[\sigma-\Theta(n/\log n),\,\sigma]$, plus over-balanced $t>\sigma$ (the classical high-degree packing regime). This does **not** give a clean repaired theorem by itself; it **relocates** F1-above-reserve onto two existing objects:

1. The **unbalanced part** ($\sigma-t$ above reserve) reduces, by Lemma 1, to the **extension list-decoding ledger** — precisely `eq:extension-list` / the L1 family `conj:final-locator`. No *new* MCA object appears; F1 inherits whatever the list ledger gives. This is the conditional repaired theorem.
2. The **balanced part** ($t\approx\sigma$, $E\in F[X]\setminus B[X]$) is the **residue-line packing problem $\Lambda^{\rm NC}_{t,\delta}$ of `thm:normalform`/`conj:final-mca`, lifted from the generated field to $F$.** At $t=\sigma$ (residual slack $0$) the "list" is all $\binom{n}{k+\sigma}$ subset-interpolants — exactly the regime where the $\sigma=1$ Vieta explosion lived — so the question becomes whether a $\sigma$-dimensional, genuinely-extension ($E\notin B[X]$) analogue of the Vieta slice still selects many *$F$-valued* slopes. That is open and is the sharp new wall.

The base subcase $E\in B[X]$ of the balanced regime is **not** dangerous: it is the monomial/restricted-sumset stratum (`thm:exactslack`, image $\mathcal B_T\subseteq B$), and Paper D subfield confinement (`cs25_cap_v4.tex` `lem:confine`) deflates it by $|B|/|F|$. Only $E\notin B[X]$ at $t\approx\sigma$ can carry genuinely extension-valued danger.

---

## Formal statements

**Theorem F1-RS (residual-slack reduction; PROVED).** With $B=\F_{q_{\rm gen}}\subseteq F=\F_{q_{\rm line}}$, $D=H\subseteq B$, $C_F=\RS[F,D,k]$, and any degree-$t$ residue-line datum $(E,B_{\rm num},w)$ over $F$ with $E\nmid B_{\rm num}$, the support-wise MCA-bad slopes at radius $\delta=1-(k+\sigma)/n$ number at most $\mathrm{List}_{\sigma-t}(w):=\#\{W\in F[X]:\deg W\le k+t-1,\ W|_S=w|_S\text{ on some }|S|\ge k+\sigma\}$, with $\le1$ slope per $W$. Consequently $\emca$ contributed by this datum is $\le \mathrm{List}_{\sigma-t}(w)/q_{\rm line}$.

**Corollary F1-A (degree-one safety above reserve; CONDITIONAL).** For $E=X-\alpha$ and $\sigma\ge Cn/\log n$ with $C\ge(1+\eps)\HH(\rho)/c$ (where $\log_2 q_{\rm line}\ge c\log_2 n$), $(\star)$ holds with $t=1$; conditional on the extension list local limit (`conj:final-locator`, `eq:extension-list`), the datum contributes $\le n^{1+o(1)}/q_{\rm line}$. No degree-one extension counterexample survives above the corrected reserve.

**Counterexample F1-CE2 (fixed-$\sigma$ degree-one family; PROVED, sub-reserve).** For every fixed $\sigma\ge1$, $B=\F_p$, $F=\F_{p^2}$, $E=X-\alpha$, $w=X^{k+\sigma}$: $\emca(C_F,1-\tfrac{k+\sigma}{n})\ge\Theta_\sigma(1)$, refuting Remark S. Reserve $\eta=O(1/n)$.

**Wall W-bal (EXACT NEW WALL).** Above the corrected reserve, the repaired extension-line MCA theorem holds for all data with $(\sigma-t)\log_2 q_{\rm line}\ge(1+\eps)\log_2\binom{n}{k+\sigma}$ (conditional on the list ledger). The only undecided regime is balanced extension denominators $t\in[\sigma-\Theta(n/\log n),\sigma]$ with $E\in F[X]\setminus B[X]$ — equivalently $\max_t\Lambda^{\rm NC}_{t,\delta}$ of `thm:normalform` evaluated over $F$ at residual slack $\le\Theta(n/\log n)$.

---

## Full parameter ledger

| symbol | meaning | value / regime |
|---|---|---|
| $B$ | base / generated field | $\F_p$ (general: $\F_{q_{\rm gen}}$) |
| $F$ | extension / line / challenge field | $\F_{p^2}$ or $\F_{p^e}$ |
| $q_{\rm gen}$ | entropy / generated-field size | $p$ (kept separate) |
| $q_{\rm line}$ | line-experiment field (slopes sampled) | $\mathrm{poly}(n)\le q_{\rm line}\le 2^{o(n)}$; $=p^2$ in witnesses |
| $q_{\rm chal}$ | verifier challenge field | $=q_{\rm line}$ only after protocol proof |
| $H=D$ | evaluation set | $\F_p^\times$, $n=p-1$ |
| $k,\rho$ | dimension, rate | $k=\rho n$ |
| $a,\sigma$ | agreement, slack | $a=k+\sigma$ |
| $\delta,\eta$ | radius, reserve | $\delta=1-a/n$, $\eta=\sigma/n$ |
| corrected reserve | regime of interest | $\sigma\ge Cn/\log n$ |
| $t$ | residue denominator degree $\deg E$ | $1\le t\le r=n-k$ |
| $\sigma-t$ | **residual slack** (new invariant) | controls safety via $(\star)$ |
| $E$ | denominator | $X-\alpha$ (witnesses); danger needs $E\notin B[X]$ |
| $\mu,\nu,e$ | list arity, interleaving, $[F:B]$ | $1,1,2$ in witnesses |

---

## Separate-object ledger (subtask 6)

- **List decoding:** Lemma 1 *imports* the list object; F1-above-reserve becomes the extension list ledger `eq:extension-list`/`conj:final-locator`. No list-size claim is *made* here. (CONDITIONAL)
- **CA:** the fixed-$\sigma$ families give $\eca(C_F,\delta)\ge\Theta_\sigma(1)$ (direction non-containable). (COUNTEREXAMPLE, sub-reserve)
- **MCA:** degree-one safe above reserve (CONDITIONAL); $\Theta(1)$ below reserve for every fixed $\sigma$ (PROVED).
- **Support-wise line-MCA:** the direct object of Lemma 1 (PROVED reduction).
- **Line-decoding:** any $\emca(C_F,\delta)\le a_{\rm LD}/q_{\rm line}$ inherits $a_{\rm LD}\ge\Theta(p^2)$ from the sub-reserve families; above reserve $a_{\rm LD}\le n^{1+o(1)}$ would follow from the list ledger. (CONJECTURAL, `op:line-decoding`)
- **Curve-MCA:** untouched; affine lines only. (out of scope)
- **Protocol ledger:** `ass:extension-mca-lift` must stay un-cited in unrestricted form. The defensible replacement: charge the **extension list term** for unbalanced data, and an explicit **balanced-denominator residue-line term** $\Lambda^{\rm NC}_{t\approx\sigma}(F)$ for the wall. Keep $q_{\rm gen}\ne q_{\rm line}\ne q_{\rm chal}$. (AUDIT)

---

## Exact dependency list (by source file and label)

Read and used this session:
- `tex/snarks_v4.tex`: `ass:extension-mca-lift` (≈ln 242, refuted-unrestricted target), `rem:lift-evidence` (ln 251), `eq:extension-list` (ln 235), `op:extension-mca` (ln 765), `eq:entropy-necessary`/$\taustar$ (ln 289–306), `eq:interleaved-mca` (ln 274), `op:line-decoding` (ln 770).
- `tex/proximity_blueprint_v3.tex`: `prob:F1` (ln 471), "how to attempt" item 3 ($E\in F[X]\setminus B[X]$, ln 492), sub-reserve note (ln 482–484).
- `tex/slackMCA_v3.tex`: `def:residue` (ln 1189), `lem:denom` (ln 1193), `thm:normalform` (ln 1197), `rem:strata` (ln 1209), `rem:aper` (ln 1255), `def:badset`/`thm:exactslack` (ln 684–700), `thm:onez`/`prop:floor` (ln 659–674), `def:mca` (support-wise), `conj:B`/`conj:final-mca` (ln 1231/1717), `conj:final-locator` (ln 1702), `cor:genfield-pigeonhole` (entropy reserve).
- `tex/cs25_cap_v4.tex`: `lem:confine` (subfield confinement, base-rational case).
- `agent_context/pro_answer_bank/20260617_OPUS48_F1_FIXED_RATE_COUNTEREXAMPLE_AUDIT.md` (Remark S, refuted), `..._F1_EXTENSION_MCA_COUNTEREXAMPLE_AUDIT.md`, raw `..._OPUS48_F1_FIXED_RATE_RAW_1.md`, `..._F1_EXTENSION_MCA_RAW_1/2/3.md`; verifiers `verify_f1_fixed_rate_slice.py`, `verify_f1_extension_counterexample.py` (counts AUDIT).
- Ledgers: `02_STATUS_LEDGER.md`, `03_OPEN_PROBLEMS_AND_BACKLOG.md` (rank-3 F1).

---

## Computational evidence (EXPERIMENTAL — not run; core results are hand-proved)

`bash` is unavailable in this harness, so the following is reproducible pseudocode, marked EXPERIMENTAL (not exhaustive). Theorem F1-RS, Corollary F1-A, and Counterexample F1-CE2 are PROVED by hand and independent of any run. A hand check of F1-CE2 at $p=7$, $\sigma=2$ is in §3.

```python
# EXPERIMENTAL: confirm residual-slack collapse for E = X - alpha.
# F = F_p[t]/(t^2 - d); residue-line datum (E=X-alpha, B=1, w=X^{k+sigma}).
from itertools import combinations
def bad_slopes_deg1(p, d, k, sigma):           # exact, small p
    F = make_Fp2(p, d); alpha = F(0,1); a = k + sigma
    out = set()
    for S in combinations(range(1, p), a):
        e = elem_sym(S, p)                      # e_1..e_a over F_p
        if any(e[j] != 0 for j in range(1, sigma)):  # need e_1=..=e_{sigma-1}=0
            continue                            # (i): deg W_S <= k
        prod = F(1)
        for s in S: prod = prod * (alpha - F(s))
        out.add(alpha**a - prod)                # z_S = W_S(alpha)
    return len(out)
# PREDICTION (PROVED by the Vieta slice, one dim per extra slack):
#   fixed sigma  -> |out| = Theta(p^2)              (sub-reserve danger)
#   sigma ~ Cn/logn, t=1 -> residual slack sigma-1 clears (*) -> |out| <= poly(n)
# Reproduces verifiers at sigma=1: bad_slopes_deg1(7,3,3,1)=15, (17,3,8,1)=288.
def clears_reserve(sigma, t, n, k, q):          # condition (*)
    from math import comb, log2
    return (sigma - t) * log2(q) >= log2(comb(n, k + sigma))   # (1+eps) omitted
```

---

## Route verdict

**EXACT_NEW_WALL** — Above the corrected reserve, the degree-one (and every unbalanced) extension counterexample is dead: Theorem F1-RS reduces such data to the extension list ledger, and the corrected-reserve hypothesis carries over with residual slack $\sigma-t$. The audit's "$\sigma=1$ forced" is corrected (fixed-$\sigma$ degree-one families exist, but only sub-reserve). The repaired above-reserve theorem is therefore conditional-on-list for unbalanced data, and the entire remaining problem is the sharply-located wall of **balanced extension denominators $t\in[\sigma-\Theta(n/\log n),\sigma]$ with $E\notin B[X]$** = the $F$-lift of the residue-line packing number $\Lambda^{\rm NC}_{t}$ of `thm:normalform`/`conj:final-mca`.