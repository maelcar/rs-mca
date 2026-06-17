# First 10 Agent Prompts

These prompts are narrow, source-grounded, and output-oriented. They assume the agent starts from this repo snapshot and does not edit main papers unless explicitly instructed.

## 1. Theorem-Label Extraction

Read `agent_context/extract_labels.py`, `tex/RS_disproof_v3.tex`, `tex/slackMCA_v3.tex`, `tex/cs25_cap_v4.tex`, `tex/snarks_v4.tex`, and `tex/proximity_blueprint_v3.tex`. Regenerate `agent_context/04_THEOREM_LABEL_MAP.md`, then audit the generated statuses manually for the top 40 labels used by Papers B-D. Output a table with columns: source, label, generated status, corrected status, reason, and cross-paper dependency. Do not edit main TeX files.

## 2. Crites-Stewart Import Audit

Audit the Crites-Stewart import used in `tex/cs25_cap_v4.tex:128` and `tex/slackMCA_v3.tex:1471`. Compare against the original CS25 theorem and ABF26 restatement. Check admissible `delta`, augmented code `C+`, CA normalization, sampling field, strict/weak inequalities, constants in the `eta=1/2` contrapositive, and `Lst(C,delta) <= Lst(C+,delta)`. Output a pass/fail table and a final status: "import matches exactly" or "import needs correction: ...".

## 3. Paper A Finite-Claim Reproduction

Reproduce the finite arithmetic in Paper A, especially `tex/RS_disproof_v3.tex:517` V1-V5. Build or specify an exact script certificate for Fermat coverage, locator end-to-end expansion at `p=257`, pigeonhole list sizes at `p=17`, BabyBear/KoalaBear deployed divisor inequalities, and the `N=16,r=9` sieve mechanism. Output JSON-like certificates and a human table. Tag each output PROVED if exhaustive, EXPERIMENTAL if heuristic.

## 4. Quotient-Profile Scanner

Implement `scripts/quotient_profile.py` without installing new packages. Inputs: `n,k,a` or `n,k,sigma`, optional dither range `r=0..16`. Compute all active divisor scales `M | gcd(n,k)` satisfying `M>1`, `a-k<M`, `k/M <= n/M-1`, and output `N=n/M`, `log2 binom(n/M-1,k/M)`, and pass/fail against a supplied list exponent `B_L`. Reproduce `snarks_v4` dyadic one-step hygiene for `k=rho*n-1`. Output JSON and Markdown.

## 5. Entropy-Margin Scanner

Implement `scripts/entropy_margin.py`. Inputs: `n,k,a,q_gen` or `rho,eta,n,q_gen`. Compute `entres=(a-k)log2(q_gen)-log2 binom(n,a)`, entropy ratio, and approximate `tau*(rho,q_gen)`. Reproduce the feasibility rows in `tex/snarks_v4.tex:313` for KoalaBear/BabyBear, Goldilocks, 128-bit, and 252-bit generated fields at `rho=1/2`. Output exact integer binomial size, decimal logs, and AUDIT status.

## 6. `q=17,n=16` Exhaustive Locator Fiber Scan

Build a bounded exhaustive scan for locator fibers over `F_17` with `H=F_17^*`, `n=16`, `rho=1/2` and `rho=1/4`, and small `sigma in {1,2,3}`. Start with monomial-prefix words, then include arbitrary interpolants if feasible. For each largest fiber, tag quotient-periodic, aperiodic, or unknown, and record supports or hashes sufficient to reproduce. Output whether any aperiodic fiber violates the expected local-limit shape in this tiny regime.

## 7. MCA Bad-Slope Scan

Implement a small exact MCA bad-slope scanner for `p in {17,97,257}`, `n=16`, `rho=1/2`, and slack `T in {1,2,3}`. Reproduce canonical-line counts from `tex/slackMCA_v3.tex:1756` where applicable. For each bad slope, output a witness support and classify it as tangent, canonical monomial, quotient-periodic, asymmetric, or residue-line. Tag results PROVED for exhaustive finite searches, EXPERIMENTAL for sampled line families.

## 8. Extension-Line Bad-Slope Search Over `F_{p^2}`

Search for genuinely extension-valued MCA/CA bad-slope witnesses over `B=F_p`, `F=F_{p^2}` for `p in {5,7,17}`, small `H <= B^*`, and `rho=1/2`. Exclude `B`-valued pairs using subfield confinement (`tex/cs25_cap_v4.tex:374`). Parameterize residue-line denominators `E in F[X] \ B[X]` with degree `t<=2`. Output either a full witness packet `(B,F,H,k,delta,E,Bnum,w,z,S,Q_z)` or an absence certificate for the bounded search.

## 9. Interleaved-List Tiny-Case Enumeration

For tiny RS instances, directly enumerate `Lambda(Int(C,2),delta)` and compare against the product bound `Lambda(C,delta)^2`. Focus on quotient-core received words and monomial-prefix received words. Output whether interleaving actually multiplies list size, shares supports, or shows a new obstruction. Include `q_line`, `mu=2`, `n,k,delta`, and list-over-field budget impact.

## 10. SNARK Ledger Certificate Schema

Draft a JSON schema for Paper C's field-separated reserve certificate `def:cert` at `tex/snarks_v4.tex:436`. Include fields for `q_arith`, `q_gen`, `q_line`, `q_chal`, `B`, `F`, `n,k,rho,delta,a,sigma,mu,nu,e,B_L,A_M`, entropy margin, quotient profile, list bound, MCA/line-decoding theorem or assumption, extension status, and failure-ladder scan. Emit one sample obstruction-audit certificate for a dyadic toy parameter set and mark it AUDIT, not PROVED.
