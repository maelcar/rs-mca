## Verdict

**AUDIT**, not **PROVED**.

The internal algebra in `tex/cs25_cap_v4.tex` is mostly coherent **conditional on** the imported Crites–Stewart/ABF theorem being exactly the theorem stated as `thm:A`. I found no arithmetic counterexample in the repository’s finite-parameter cap calculation. The decisive gap is that the **primary Crites–Stewart theorem and ABF26 restatement were not available to verify**, while the repository itself says the imports are not yet independently checked (`cs25_cap_v4.tex:425-426`). Therefore Paper D’s universal field-size cap may be cited only as **conditional/audit-pending**, not as an unconditional theorem.

A secondary CS25 summary states a theorem of the expected shape: small correlated-agreement error for `RS(...,k)` implies list-decodability of `RS(...,k+1)` with list bound
[
L=\left\lceil \frac{\varepsilon q(q-n)}{q-n-k\varepsilon q}\right\rceil,
]
and for (\varepsilon < (q-n)/(2kq)), (L\le 2\varepsilon q). That matches Paper D’s algebraic constant after an (\eta)-relaxation, but it is **not the primary source** and appears to use an error-radius condition stated in terms of an integer (f), which must be checked against Paper D’s real-radius interval. ([HackMD][1])

The BCHKS fallback source was accessible. Its Theorem 1.9 gives a finite theorem relating list-decoding radius to a correlated-agreement failure with at least (q/(2n)) bad line challenges and pair distance at least (\delta-1/n). ([Mathematics at University of Toronto][2]) Its proof explicitly starts from a ball with more than (q) nearby codewords and constructs many bad (z)’s. ([Mathematics at University of Toronto][2]) That supports the qualitative fallback, but the repository’s exact `< q` versus `≤ q` / `≥ q` strictness still needs ABF26 or a local proof.

---

## 1. Import-audit table

| Repository claim                                                                                                             |                              Source label | Imported theorem needed                                                                                                                                                                         | Imported hypotheses                                                                                                            | Match                                        | Correction needed                                                                                                                                       | Impact                                                                                        |                                                                                                                                                                          |                                                                                                                                 |                                                                                                                                         |                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Crites–Stewart import `thm:A`: small `eca(C,δ)` forces small lists in `C^+=RS[F,D,k+1]`.                                     |                 `cs25_cap_v4.tex:128-135` | Exact finite theorem: if (\epsilon=\operatorname{eca}(C,\delta)\le \eta(q-n)/(kq)), then (\operatorname{Lst}(C^+,\delta)\le \lceil q\epsilon/(1-\eta)\rceil), or the exact formula implying it. | Finite field (F), (q=                                                                                                          | F                                            | ); (D\subset F), (                                                                                                                                      | D                                                                                             | =n); (C=RS[F,D,k]); (C^+=RS[F,D,k+1]); same CA normalization; same challenge field; admissible radius includes the repository’s use.                                     | **AUDIT**                                                                                                                       | Fetch primary CS25 Theorem 2 and ABF26 Theorem 5.3. State the exact formula, radius convention, rounding, (C^+), and field assumptions. | Central dependency. Without this, Paper D’s universal cap is not proved.  |
| Main universal cap theorem: list lower bound plus `thm:A` gives (\operatorname{emca}\ge\operatorname{eca}>(2k)^{-1}(1-n/q)). |                 `cs25_cap_v4.tex:219-247` | `thm:A` plus locator-fiber list lower bound for (C^+).                                                                                                                                          | (N\mid n), (a=n/N\mid k), ((1-\rho)N\ge 3), (\binom{N}{\rho N+2}\ge                                                            | B                                            | (q/k+1)), (D\subset B^\times\subset F^\times).                                                                                                          | **CONDITIONAL**                                                                               | If CS radius is only below (1-\rho-1/n), restrict the direct `eca` claim or prove only at (\delta_N=1-\rho-2/N) and extend the **MCA** cap by support-wise monotonicity. | The proof skeleton is sound if `thm:A` is exact. The “for every (\delta<1-\rho)” CA statement is vulnerable to radius mismatch. |                                                                                                                                         |                                                                           |
| Grand corollary: for (q<2^{256}), rates (1/2,1/4,1/8,1/16), get (>2^{-86}), and (>2^{-42}) if (q\ge2n).                      |                 `cs25_cap_v4.tex:259-288` | Main theorem.                                                                                                                                                                                   | (B\subset F), (D\subset B^\times), (N_\rho\mid n), (k=\rho n\le2^{40}), (q=                                                    | F                                            | <2^{256}).                                                                                                                                              | **CONDITIONAL**                                                                               | Mark the statement itself conditional, not only the caveat. Keep (q<2^{256}) versus `slackMCA_v3.tex`’s occasional (q\le2^{256}) consistent.                             | Arithmetic constants check out, but the result inherits the CS import audit status.                                             |                                                                                                                                         |                                                                           |
| Locator-fiber list lower bound for (C^+).                                                                                    |                 `cs25_cap_v4.tex:154-187` | None external.                                                                                                                                                                                  | (D\subset B^\times) is a multiplicative coset/order-(n) domain; (a=n/N); (a\mid k); (\ell_2=\rho N+2\le N).                    | **YES**                                      | Add one explicit note that the polynomial factorization is over (B) and that the count is over (                                                        | B                                                                                             | ), not (                                                                                                                                                                 | F                                                                                                                               | ).                                                                                                                                      | Valid list-decoding input. It proves only a list lower bound, not CA/MCA. |
| `eca(C,δ) ≤ emca(C,δ)` chain.                                                                                                |                 `cs25_cap_v4.tex:118-124` | None external.                                                                                                                                                                                  | No-proximity-loss `eca(C,δ)=eca(C,δ,δ)` and support-wise MCA definition.                                                       | **YES for no-loss CA**                       | Do not apply this chain to the BCHKS two-radius fallback without an explicit two-radius-to-MCA statement.                                               | Main theorem’s `eca → emca` step is fine; fallback does not automatically become no-loss MCA. |                                                                                                                                                                          |                                                                                                                                 |                                                                                                                                         |                                                                           |
| Extension-field version: (B\subset F), entropy over (B), challenges over (F).                                                |      `cs25_cap_v4.tex:253-255`, `374-405` | CS theorem must be over the ambient finite field (F) and sample line slopes (\gamma\in F).                                                                                                      | (D\subset B^\times), code alphabet (F), line challenge field (F).                                                              | **AUDIT**                                    | Verify CS25/ABF allows arbitrary finite fields and extension-field ambient codes, not only prime fields or (D\subset F_q) with no subfield distinction. | Extension-field cap and KoalaBear sextic deployment depend on this.                           |                                                                                                                                                                          |                                                                                                                                 |                                                                                                                                         |                                                                           |
| BCHKS fallback `thm:B`: small two-radius CA error implies (\operatorname{Lst}(C,\delta)<q).                                  |      `cs25_cap_v4.tex:137-143`, `346-364` | ABF26 restatement of BCHKS Theorem 1.9, or a local contrapositive proof.                                                                                                                        | (C=RS[F,D,k]), (k=\rho n), (\delta+2/n\le1-\rho-1/n), list-size threshold exactly `< q` or `≤ q`, two-radius CA normalization. | **AUDIT / CONDITIONAL**                      | Fetch ABF26 Theorem 5.2 or change the fallback list condition to a strict `>q` version and prove the contrapositive directly from BCHKS.                | Fallback supports a slacked CA statement, not the main no-loss universal MCA cap.             |                                                                                                                                                                          |                                                                                                                                 |                                                                                                                                         |                                                                           |
| Paper B native universal cap imports `capimport`.                                                                            |               `slackMCA_v3.tex:1464-1515` | Same CS theorem, but the statement there is less precise than Paper D’s `thm:A`.                                                                                                                | (q) prime power, (H\le F_q^\times), (n\le q/2), divisibility, quotient-core list lower bound.                                  | **CONDITIONAL**                              | Treat as superseded by Paper D’s more explicit import. Fix `δ∈(0,1−ρ]` and unspecified (C^+) if this remains cited.                                     | Paper B should not be used as an unconditional source for Paper D.                            |                                                                                                                                                                          |                                                                                                                                 |                                                                                                                                         |                                                                           |
| “Universal field-size cap” language in abstract.                                                                             | `cs25_cap_v4.tex:42-51`, caveat `425-426` | Verified CS/BCHKS imports.                                                                                                                                                                      | Same as above.                                                                                                                 | **NO as written / CONDITIONAL if relabeled** | Move conditionality into abstract, theorem heading, and corollary statement.                                                                            | Current wording risks citing an audit-pending import as a proved theorem.                     |                                                                                                                                                                          |                                                                                                                                 |                                                                                                                                         |                                                                           |

---

## 2. Field ledger

| Symbol         | Meaning in this audit                                                                            | Repository use                                                                                                          | Required discipline                                                                                                           |                                                                                            |                                                                                                                                                                                                        |          |                                                                         |                                |                 |   |                |   |                                                                                              |
| -------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ----------------------------------------------------------------------- | ------------------------------ | --------------- | - | -------------- | - | -------------------------------------------------------------------------------------------- |
| (q_{\rm gen})  | Field size used for generated locator/coefficient pigeonholing. In Paper D this is effectively ( | B                                                                                                                       | ).                                                                                                                            | `lemma:fiber` divides by (                                                                 | B                                                                                                                                                                                                      | ), not ( | F                                                                       | ) (`cs25_cap_v4.tex:154-167`). | Never replace ( | B | ) by ambient ( | F | ) in entropy/list lower bounds. Extension fields do not make the locator pigeonhole cheaper. |
| (q_{\rm line}) | Field size over which line challenges (\gamma) are sampled.                                      | In Paper D, (q_{\rm line}=q=                                                                                            | F                                                                                                                             | ) in `eca(C,δ)` (`cs25_cap_v4.tex:92-98`).                                                 | CS import must use the same challenge field (F). If CS samples only over a base field, the extension-field cap is not justified.                                                                       |          |                                                                         |                                |                 |   |                |   |                                                                                              |
| (q_{\rm chal}) | Protocol challenge field.                                                                        | Not independently modeled in Paper D; implicitly (q_{\rm chal}=q_{\rm line}=                                            | F                                                                                                                             | ) for the CA/MCA abstraction.                                                              | For protocol citations, state whether the verifier challenge field equals (F). Do not silently transfer a base-field CA bound to an extension-field protocol.                                          |          |                                                                         |                                |                 |   |                |   |                                                                                              |
| (B)            | Subfield containing (D) and locator coefficients; generated witness field.                       | (B\subset F), (D\subset B^\times); KoalaBear example has base (B=F_p), ambient (F=F_{p^6}) (`cs25_cap_v4.tex:323-332`). | Pigeonhole counts and explicit locator witnesses live over (B). Base-rational bad slopes in an extension have density about ( | B                                                                                          | /                                                                                                                                                                                                      | F        | ), so they cannot certify large extension-field CA error by themselves. |                                |                 |   |                |   |                                                                                              |
| (F)            | Ambient alphabet/challenge field for `RS[F,D,k]`.                                                | (q=                                                                                                                     | F                                                                                                                             | ) appears in the CS list upper bound, the (1-n/q) term, and the universal (q<2^{256}) cap. | The imported theorem must be valid over arbitrary finite ambient (F). The bound (q\ge n+1) follows from (D\subset F^\times); (q\ge2n) is only an extra hypothesis for the stronger (2^{-42}) constant. |          |                                                                         |                                |                 |   |                |   |                                                                                              |

---

## 3. Finite/asymptotic, field-size, rate/radius/list constants, and list-to-MCA status

### Finite versus asymptotic

Paper D’s cap calculation is a **finite-parameter statement**, not an asymptotic local-limit conjecture. The corollary fixes concrete (N)’s: (N=1024) for (\rho=1/2,1/4,1/8), and (N=2048) for (\rho=1/16) (`cs25_cap_v4.tex:259-288`). The arithmetic bounds are finite inequalities using (q<2^{256}), (k\le2^{40}), and (N\mid n).

The imported theorems must also be finite. BCHKS Theorem 1.9 is finite in (q,n,k), and gives a concrete (q/(2n)) lower bound. ([Mathematics at University of Toronto][2]) The CS theorem must be verified as finite with the exact same normalization; the secondary summary suggests it is finite, but the primary theorem was not fetched. ([HackMD][1])

### (q\ge n) and (q\ge2n)

Paper D’s main theorem does **not** require (q\ge2n). Since (D\subset F^\times) has size (n), the repository correctly uses (n\le q-1), hence (1-n/q\ge1/(n+1)), to get the weaker universal lower bound (>2^{-86}) (`cs25_cap_v4.tex:279-288`).

The stronger (>2^{-42}) statement **does** require (q\ge2n), because then
[
\frac1{2k}\left(1-\frac nq\right)\ge \frac1{4k}\ge2^{-42}
]
when (k\le2^{40}). This matches Paper D’s corollary. Paper B’s older cap tier requires (n\le q/2) for its (2^{-42})-style statement (`slackMCA_v3.tex:1505-1515`).

### Rates and radius constants

Paper D’s rate/radius constants are internally consistent:

[
\rho\in{1/2,1/4,1/8,1/16}.
]

For (\rho=1/2,1/4,1/8), (N=1024), so the advertised gap is (2/N=2^{-9}). For (\rho=1/16), (N=2048), so the gap is (2^{-10}). This matches `cs25_cap_v4.tex:259-276`.

The direct CA claim is stated for every

[
\delta\in[1-\rho-2/N,;1-\rho).
]

This is the most radius-sensitive part of the import. The secondary CS summary states the theorem using an integer error parameter (f), with an admissibility phrase of the form (f<n-k-1). ([HackMD][1]) If the primary theorem really excludes the last (1/n)-layer below capacity, then Paper D’s direct claim for **all** (\delta<1-\rho) is too broad. The MCA cap could still be saved by proving the lower bound at (\delta_N=1-\rho-2/N) and then invoking support-wise MCA monotonicity, but the repository’s stronger “`eca(C,δ)>...` for every (\delta)” statement would need to be weakened or separately proved.

### List-size constants

The main contradiction is algebraically correct if `thm:A` is correct.

Paper D uses (\eta=1/2). If

[
\operatorname{eca}(C,\delta)\le \frac1{2k}\left(1-\frac nq\right)
=\frac{q-n}{2kq},
]

then the imported theorem gives

[
\operatorname{Lst}(C^+,\delta)\le
\left\lceil 2q\operatorname{eca}(C,\delta)\right\rceil
\le
\left\lceil \frac{q-n}{k}\right\rceil
< \frac qk+1.
]

The fiber lemma gives

[
\operatorname{Lst}(C^+,\delta)\ge \binom{N}{\rho N+2}/|B|.
]

Thus the displayed hypothesis (\binom{N}{\rho N+2}\ge |B|(q/k+1)) contradicts the CS list upper bound (`cs25_cap_v4.tex:235-247`). This part is fine.

The BCHKS fallback has a stricter issue. BCHKS’s proof starts from a ball with **more than (q)** codewords. ([Mathematics at University of Toronto][2]) Paper D’s fallback theorem/restatement uses a conclusion `Lst(C,δ)<|F|`, whose contrapositive triggers at `Lst(C,δ)≥q` (`cs25_cap_v4.tex:137-143`). That exact strictness is not visibly justified by the BCHKS primary theorem alone. Either ABF26 Theorem 5.2 must supply the strict version, or the repository should strengthen the fallback list hypothesis to `> |B|q`.

### Is list decoding silently promoted to CA/MCA?

In the main theorem, the promotion is **not silent**, but it is **conditional**:

1. `lemma:fiber` proves only a list lower bound.
2. `thm:A` is the imported list-to-correlated-agreement conversion.
3. `fact:chain` gives (\operatorname{eca}\le\operatorname{emca}).

So the main Paper D chain is explicit.

The danger is citation discipline. The repository correctly says “lists, not lines” in `cs25_cap_v4.tex:197-199`, but the abstract and universal-cap wording should not read as unconditional while the import remains unaudited.

For BCHKS, the fallback proves a **two-radius CA** failure:

[
\operatorname{eca}(C,;1-\rho-1/N+2/n,;1-\rho-1/n)\ge1/(2n)
]

under its hypotheses (`cs25_cap_v4.tex:346-364`). That is not the same as no-proximity-loss `eca(C,δ)`, and it is not automatically an MCA threshold statement without an additional monotonicity/conversion lemma.

For interleaved rows, Paper D uses a base-code CA lower bound and a transfer lemma, not a raw list-decoding lower bound (`cs25_cap_v4.tex:201-215`, `334-344`). That direction is acceptable if the base-code CA result is already established.

---

## 4. Final status by claim class

| Claim class                                                                | Status                                      |
| -------------------------------------------------------------------------- | ------------------------------------------- |
| Locator/fiber list construction                                            | **PROVED locally**                          |
| Arithmetic of the finite universal cap constants                           | **PROVED locally, conditional on import**   |
| Crites–Stewart import as written in `thm:A`                                | **AUDIT**                                   |
| Paper D universal field-size cap as an unconditional theorem               | **AUDIT**                                   |
| Paper D universal field-size cap as a conditional theorem assuming `thm:A` | **CONDITIONAL**                             |
| BCHKS fallback qualitative support                                         | **CONDITIONAL / AUDIT on exact strictness** |
| “Error-one” or full prize conclusion                                       | **Not proved here; not part of this audit** |

**Final verdict: AUDIT.**
No counterexample was found in the repository’s internal algebra, but the imported Crites–Stewart theorem is the load-bearing external theorem and was not verified from the primary source.

---

## 5. Top five exact fixes/citations needed

1. **Fetch and quote the primary Crites–Stewart theorem.**
   Add the exact CS25 Theorem 2 statement and definitions, not only an ABF restatement. The repository must verify: finite-field scope, (D\subset F), (C^+=RS[F,D,k+1]), challenge field (\gamma\in F), CA normalization, radius convention, strict/weak inequalities, and the exact list formula.

2. **Derive `thm:A` as a lemma from the exact theorem.**
   Write the derivation:
   [
   L\le \left\lceil \frac{\epsilon q(q-n)}{q-n-k\epsilon q}\right\rceil
   \quad\Longrightarrow\quad
   L\le \left\lceil\frac{q\epsilon}{1-\eta}\right\rceil
   ]
   under (\epsilon\le\eta(q-n)/(kq)). Include rounding and boundary cases.

3. **Fix the radius interval.**
   If CS25 only applies for (f<n-k-1) or equivalently below (1-\rho-1/n), then Paper D must not claim direct `eca(C,δ)` lower bounds for every (\delta<1-\rho). Instead, prove the cap at (\delta_N=1-\rho-2/N) and explicitly extend only the **MCA threshold** using support-wise MCA monotonicity.

4. **Resolve BCHKS strictness.**
   Fetch ABF26 Theorem 5.2 or replace `binom(...) ≥ |B|q` by a strict `> |B|q` condition in the fallback. The accessible BCHKS proof uses a ball with more than (q) nearby codewords, so Paper D’s `Lst < q` restatement is not safely justified without that extra citation. ([Mathematics at University of Toronto][2])

5. **Promote conditionality into theorem-facing text.**
   Change abstract/corollary language from “we prove a universal cap” to “conditional on the CS25/ABF import.” The caveat at `cs25_cap_v4.tex:425-426` is too late; the theorem and corollary labels should carry the conditional status. Also add a field ledger near the theorem: (q_{\rm gen}=|B|), (q_{\rm line}=q_{\rm chal}=|F|), (F) ambient, (B) generated/domain field.

[1]: https://hackmd.io/%40zkpunk/CS25 "CS25-On Reed–Solomon Proximity Gaps Conjectures - HackMD"
[2]: https://www.math.toronto.edu/swastik/rs-proximity-gaps-2025.pdf "Improved Proximity Gaps for Reed–Solomon Codes"
