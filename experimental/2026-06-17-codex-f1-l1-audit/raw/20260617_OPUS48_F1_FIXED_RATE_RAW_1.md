I'll start by reading the file index and the key files specified in the task.I have enough to re-derive the core object. Let me verify the exact TeX statements I'm refuting and check the raw F1 outputs and the "corrected reserve" terminology before committing.I have the core. The verifier and RAW_1 give me the construction; I've found a clean proof that the image is Θ(p²) at fixed rate via a 2-parameter sub-family. Let me confirm the exact statements I'm refuting and the "corrected reserve" terminology.I have the full construction and the exact statements being refuted. Now let me independently verify from first principles (not trusting the provided verifier) and test my own asymptotic argument. I'll write a fresh implementation.I have everything needed. The execution tool (`bash_tool`) is unavailable in this harness, so I did not run code this session; my central result is a hand proof that does not depend on running anything, and I label the banked verifier counts as EXPERIMENTAL. I re-derived the mechanism from first principles and found a provable fixed-rate slice that the prior audit missed.

---

# F1: Fixed-Rate Asymptotic Counterexample to Same-Numerator Extension-Line MCA

## Executive verdict (5 lines)
The finite F_7 and F_17 witnesses promote to a **fixed-rate** asymptotic counterexample (Route A), and more strongly than the prior audit claimed: at any fixed ρ∈(0,1) the bad-slope image has size ≥ (1−ρ)²/2 · p², a positive constant density, not merely p^{1+c}. This is PROVED by an injective two-element slice S = T ∪ {x,y} with T fixed, using Vieta injectivity — no restricted-sumset lemma in Z/(p²−1) is required. The base premise holds with numerator N_mca = q_gen = p, so the lift's prediction p^{1+o(1)}/q_chal is violated by a factor p^{1−o(1)} for all large p. The exact density (whether →1) is a separate, finer question and the only piece left CONJECTURAL.

---

## Formal statement (COUNTEREXAMPLE, PROVED)

**Theorem F1-CE.** Fix ρ ∈ (0,1). For every odd prime p, fix a nonsquare d ∈ F_p* and set
B = F_p, F = F_p[α]/(α²−d) ≅ F_{p²}, H = F_p*, n = p−1, k = ⌊ρn⌋, a = k+1, δ = 1 − a/n, σ = 1.
Let C_B = RS[B,H,k], C_F = RS[F,H,k], and take the residue line with denominator E(X)=X−α:
f(x) = xᵃ/(x−α), g(x) = −1/(x−α), u_z = f + z g, z ∈ F.

Then:
1. **(Base premise holds, PROVED.)** eMCA_{z∈B}(C_B,δ) ≤ 1 = p/p, so ass:extension-mca-lift applies with N_mca = q_gen = p. (Equality holds by the companion's DSH bound, but the trivial bound already suffices.)
2. **(Extension MCA is bounded below by a constant, PROVED.)**
 eMCA_{z∈F}(C_F,δ) ≥ (p+1−a)(p−a) / (2p²) → (1−ρ)²/2 > 0 as p→∞.
3. **(Lift fails at fixed rate, PROVED.)** The extension numerator q_chal · eMCA_{z∈F}(C_F,δ) ≥ (p+1−a)(p−a)/2 = Θ(p²), whereas the lift predicts N_mca^{1+o(1)} = p^{1+o(1)}. For all sufficiently large p the lift is false; the gap is a factor p^{1−o(1)}. In particular it fails at ρ = 1/2 (density ≥ 1/8 − o(1)) and ρ = 1/4 (density ≥ 9/32 − o(1)).

This refutes the **fixed-rate** asymptotic form of `prob:F1` / `ass:extension-mca-lift`, not only the ρ→0 form previously banked.

---

## Full parameter ledger

Five field/size quantities kept strictly separate (task items 4):

| symbol | meaning | value in this family |
|---|---|---|
| B | base / generated field | F_p |
| F | extension / line field | F_{p²} = F_p[α]/(α²−d), d nonsquare |
| q_gen | generated-field size (entropy, base numerator) | p |
| q_line^B | base line-experiment field | p |
| q_line^F = q_chal | extension line-experiment / challenge field | p² |
| H | evaluation set | F_p* = {1,…,p−1} |
| n | block length | p−1 |
| k | dimension | ⌊ρn⌋ |
| a | agreement size | k+σ = k+1 |
| σ | agreement slack | 1 (forced; see Remark S) |
| δ | radius | 1 − a/n |
| η | reserve a/n − ρ | (1−ρ·n⁻¹·…) = 1/n + (ρn−k)/n, i.e. O(1/n) |
| E(X) | residue-line denominator | X − α (α ∉ B) |
| w(X) | anchor numerator | Xᵃ |
| μ, ν, e | curve arity, interleaving, [F:B] | 1, 1, 2 |
| quotient core | not used | M_quot = 1 |

Finite instances (re-derived below): (p,k,a) = (7,3,4) and (17,8,9), both ρ = 1/2.

---

## Proof and obstruction analysis

### Step 0. The image of S ↦ z_S is a translate of a subset-product image.
For an a-subset S ⊆ H, L_S(X) = ∏_{s∈S}(X−s) is monic of degree a, so Q_S = Xᵃ − L_S has degree ≤ a−1, and
z_S = Q_S(α) = αᵃ − L_S(α) = αᵃ − ∏_{s∈S}(α − s).
Since αᵃ is a fixed constant, |image(S↦z_S)| = |image(Π)| where Π_S := ∏_{s∈S}(α−s) ∈ F*. The available factors are A = {α−1,…,α−(p−1)} ⊆ F*, all distinct and nonzero (α ∉ B). Writing α−s = ω^{ℓ_s} in a cyclic F* of order p²−1,
**image(Π) = ω^{ a^∧{ℓ_s : s∈H} }**, a restricted (wedge) a-sumset in Z/(p²−1).
This is the exact object to bound. The modulus is composite, p²−1 = (p−1)(p+1), so the prime-field DSH/Cauchy–Davenport bound does **not** apply directly. (That composite-modulus restricted-sumset lower bound is the residual wall; see Remark W.) We bypass it.

### Step 1. Each distinct z_S is a support-wise MCA-bad slope (PROVED).
For any a-subset S: Q_S(α) = z_S, so (X−α) | (Q_S − z_S); set P_S = (Q_S − z_S)/(X−α), deg P_S ≤ a−2 = k−1 < k. For x∈S, L_S(x)=0 ⇒ Q_S(x)=xᵃ ⇒ P_S(x) = (xᵃ − z_S)/(x−α) = u_{z_S}(x). So u_{z_S} agrees with codeword P_S ∈ F[X]_{<k} on all a points of S, giving dist(u_{z_S}, C_F) ≤ δ.

The direction g is unexplained on **every** a-subset: if G ∈ F[X]_{<k} matched g on S, then (X−α)G(X)+1 has degree ≤ k = a−1, vanishes on the a distinct points of S (forcing it ≡ 0), yet equals 1 at X=α — contradiction. Hence no pair (A,G) ∈ F[X]_{<k}² simultaneously explains (f,g) on any a-support; every distinct z_S is support-wise MCA-bad (and CA-bad). Therefore
eMCA_{z∈F}(C_F,δ) ≥ |image(S↦z_S)| / q_chal = |image| / p².

### Step 2. A provable Θ(p²) sub-image via a fixed-tail slice (PROVED, the new content).
Fix any (a−2)-subset T ⊆ H and vary an unordered pair {x,y} ⊆ H∖T, x≠y. Then S = T∪{x,y} is an a-subset and
Π_S = Π_T · (α−x)(α−y) = Π_T · ((d+xy) − (x+y)α).
With Π_T ∈ F* fixed and αᵃ fixed, the map {x,y} ↦ z_S = αᵃ − Π_T·((d+xy)−(x+y)α) is the composition of {x,y} ↦ (x+y, xy) with an affine bijection of F. By Vieta, {x,y} ↦ (x+y, xy) is **injective** on unordered pairs of distinct elements. Hence z_S takes
 C(|H∖T|, 2) = C(p+1−a, 2) = (p+1−a)(p−a)/2
distinct values. Combined with Step 1:
eMCA_{z∈F}(C_F,δ) ≥ (p+1−a)(p−a)/(2p²).
With a = ⌊ρ(p−1)⌋+1, the right side → (1−ρ)²/2. ∎

This is exactly the missing fixed-rate upgrade: the prior banked argument (RAW_1) used the same Vieta injectivity but only at a=2 (k=1, ρ→0). Embedding the same injective pair-slice on top of a fixed (a−2)-tail T transports it to **arbitrary fixed ρ** at the cost of shrinking the pair-pool from H to H∖T, which only changes the constant from 1/2 to (1−ρ)²/2.

### Step 3. Failure of the lift (PROVED).
Base numerator N_mca = q_gen·eMCA(C_B,δ) = p·1 = p. Lift predicts eMCA(C_F,δ) ≤ p^{1+o(1)}/p² = p^{−1+o(1)} → 0. Step 2 gives a positive constant. Contradiction for all large p. The extension numerator is Θ(p²) vs claimed p^{1+o(1)} — a full power-of-p blow-up. □

### Remark S (why σ=1 is forced for w=Xᵃ).
deg P_S ≤ a−2 must be < k = a−σ, i.e. σ < 2. So σ=1 is the unique slack for which the Xᵃ anchor yields a sub-k explaining codeword; σ≥2 needs a lower-degree anchor and is a separate construction. This matches the slack-one regime (`slackMCA_v3.tex thm:exactslack`, inherited).

### Remark W (the residual wall — for the sharper density only, NOT for the verdict).
My PROVED bound gives constant density (1−ρ)²/2. The verifier shows the **full** image is much larger (p=17: 288/289 ≈ 1). Whether image/p² → 1 for every fixed ρ is precisely whether the restricted a-sumset a^∧{ℓ_s} fills Z/(p²−1) up to o(p²). Because p²−1 is composite, this needs a Dias-da-Silva–Hamidoune analogue for cyclic groups of order (p−1)(p+1) with the structured exponent set ℓ_s = log_ω(α−s) (whose norm-coordinate (p+1)ℓ_s ≡ log(s²−d) and angle-coordinate are correlated). That composite-modulus restricted-sumset lemma is the first missing finite-field combinatorial lemma to decide the **exact** density. It is **not** needed for the counterexample, which Step 2 already settles unconditionally.

---

## Separate-object ledger (task item 5)
- **List decoding:** untouched. `eq:extension-list` (|Λ(C_F)| = |Λ(Int C_B,e)|) remains valid; this is an MCA failure, not a list-size claim.
- **CA:** same slopes are CA-bad — (f,g) is not δ-close to C_F^{≡2} on any a-support (Step 1), while every u_z is δ-close.
- **MCA:** the same-numerator lift N_mca/q_line^B ↦ N_mca/q_line^F is false; actual extension MCA numerator is Θ(p²).
- **Support-wise line-MCA:** directly exhibited (Step 1) — this is the strongest part.
- **Line-decoding:** any bound eMCA(C_F,δ) ≤ a_LD/|F| forces a_LD ≥ (p+1−a)(p−a)/2 = Θ(p²) for this family; a transferred base value a_LD = p fails.
- **Curve-MCA:** affine line only, curve arity 1; no degree>1 claim.
- **Protocol ledger:** a certificate using q_gen=p for entropy may **not** divide a base numerator by q_chal=p²; it must charge an F-line term or use the exact e-interleaved multiplication-slice transfer (RAW_1 §4).

---

## Exact dependency list by source file and label

Directly read and verified this session:
- `tex/snarks_v4.tex`: `ass:extension-mca-lift` (≈ln 242, the refuted target), `rem:lift-evidence` (ln 251, the "no such family is currently known" claim this refutes), `eq:extension-list` (ln 235), `eq:interleaved-mca` (ln 274), `def:cert`/`rule:no-double-credit` (via handoff), `op:extension-mca`.
- `tex/proximity_blueprint_v3.tex`: `prob:F1` (ln 471); "how to attempt" item 3 (ln 492) explicitly predicting E∈F[X]∖B[X] as the source — now realized at fixed rate; paperD sub-reserve existence note (ln 482).
- `agent_context/.../20260617_F1_EXTENSION_MCA_RAW_1.md`, `_RAW_2.md`: prior ρ→0 (a=2) family and p=17 angle-coverage; `verify_f1_extension_counterexample.py`: counts 15, 288 (EXPERIMENTAL).
- `agent_context/09_MANAGER_HANDOFF_20260617.md`, `pro_answer_bank/20260617_F1_..._AUDIT.md`: prior verdict COUNTEREXAMPLE (not fixed-rate).

Inherited from banked audit, NOT re-located in source this session (flagged AUDIT): `slackMCA_v3.tex` `thm:exactslack`, `def:residue`, `lem:denom`, `thm:normalform`; `RS_disproof_v3.tex` `def:mca`, `lem:locator`, `lem:dsh`; `cs25_cap_v4.tex` `def:ca`, `def:mca`, `lem:confine`. I did not open these three .tex files, so treat those labels as audit-provenance, not verified locations.

---

## Computational evidence (EXPERIMENTAL vs PROVED)

I could **not execute code** (`bash_tool` unavailable in this harness); below is reproducible pseudocode. The hand-derivation in Steps 1–2 is **PROVED** and independent of any run.

- **PROVED (by hand, no computer):** Steps 1–3, the bound ≥ (p+1−a)(p−a)/(2p²). Hand check at p=7, d=3, a=4, T={1,2}, Π_T = 5−3α: the six pairs from {3,4,5,6} give six distinct w_{x,y} ∈ {1, 4−α, 5α, 2−2α, 6−3α, 5−4α}, so ≥ 6 distinct z_S (slice bound C(4,2)=6). ✓
- **EXPERIMENTAL (banked verifier, read not run):** full image 15 at p=7 and 288 at p=17. Consistent with PROVED slice (6 ≤ 15, 36 ≤ 288).

```python
# Independent re-derivation skeleton (Fp2 = Fp[a]/(a^2-d); element (u,v)=u+v*alpha)
from itertools import combinations
def mul(x,y,p,d): return ((x[0]*y[0]+d*x[1]*y[1])%p,(x[0]*y[1]+x[1]*y[0])%p)
def powF(x,e,p,d):
    r=(1,0)
    while e:
        if e&1: r=mul(r,x,p,d)
        x=mul(x,x,p,d); e>>=1
    return r
def full_image(p,k,d):                 # |{z_S}| over all a-subsets
    a=k+1; al=(0,1); aa=powF(al,a,p,d); img=set()
    for S in combinations(range(1,p),a):
        P=(1,0)
        for s in S: P=mul(P,((-s)%p,1),p,d)   # alpha - s
        img.add(((aa[0]-P[0])%p,(aa[1]-P[1])%p))
    return len(img)
def slice_lb(p,k): a=k+1; return (p+1-a)*(p-a)//2   # PROVED lower bound
# expected: full_image(7,3,3)=15>=slice_lb=6 ; full_image(17,8,3)=288>=slice_lb=36
# fixed-rate: for rho=1/2, slice_lb/p^2 -> 1/8 ; rho=1/4 -> 9/32
```

---

## Suggested next agent prompt

> F1 promoted to a PROVED fixed-rate counterexample (constant MCA density ≥ (1−ρ)²/2 via the fixed-tail Vieta slice). Two follow-ups, in priority order:
> (1) **Repaired theorem above the corrected reserve (Route B candidate).** The counterexample lives at σ=1, reserve η=O(1/n) — i.e. *at* the wall. Determine whether ass:extension-mca-lift survives when restricted to δ below the corrected reserve (η bounded away from 0, σ growing): does the fixed-tail slice still inject when the anchor degree drops below a? Reconcile with paperD's structural cap gap ≈ H₂(ρ)/log₂q_line (proximity_blueprint ln 484). Produce either a restricted-reserve lift proof or a sub-reserve extension of Theorem F1-CE.
> (2) **Exact density / Remark W (EXACT_NEW_WALL candidate).** State and attempt the composite-modulus restricted-sumset lemma: for ℓ_s = log_ω(α−s) in Z/(p²−1), is a^∧{ℓ_s} = Z/(p²−1) − o(p²) at fixed ρ? Decompose via norm-coordinate (mod p−1, = log(s²−d)) and angle-coordinate (mod p+1) and check independence. Keep q_gen, q_line, q_chal separate; do not touch the list ledger (eq:extension-list).
> Do not edit main papers. Bank Theorem F1-CE as the fixed-rate strengthening of the existing F1 COUNTEREXAMPLE.

---

**ROUTE VERDICT: COUNTEREXAMPLE**