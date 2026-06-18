I have enough from the source and audit chain to classify. Key checks: `def:residue` gives the slope condition `[I_S]_E = z[Bnum]_E` in `F[X]/(E)`; the banked Cycle 1 / Codex-local audits already contain the paired-readout reduction; Cycle 3 isolates the agreement gap; Cycle 5 / `ACTIVE_WALLS` name the missing invariant as a rigidity/value-count law analogous to `thm:rigidcyclo` / `thm:exactcount`.

Final classification: EXACT_NEW_WALL

Object:
Restricted W-F1-AA-RES rigidity half: same-slope kernel plus paired base readout.

Verdict:
Both parts are correct and source-valid, but neither is a new advance.
Part B is the already-banked Cycle 1/Codex paired-readout reduction verbatim.
Part A is a one-line corollary of banked slope-uniqueness plus a degree count.
Together they restate the residue equation as a kernel and a base factorization.
They do not count slopes or control agreement, so the rigidity wall stands.

Proof or cut:
1. def:residue slope cond is [I_S]_E = z[Bnum]_E in F[X]/(E), z in F.
2. Bnum != 0, deg Bnum < t = deg E, so [Bnum]_E != 0 (no E-multiple has deg<t).
3. Nonzero z-z' in F is a unit in F[X]/(E); so z(S) is unique (banked Cycle 2).
4. Hence z(S)=z(S') iff [I_S]_E=[I_S']_E iff E | (I_S - I_S') in F[X].
5. deg I_S, I_S' < a = k+t and deg E = t, so the quotient has degree < k.
6. Thus E | (I_S-I_S') iff I_S-I_S' in E*F_{<k}[X]. Part A holds (with E, over F).
7. D subset B gives B-valued Lagrange weights: I_S=interp_S(w0)+alpha interp_S(w1).
8. Ehat=lcm(E,E^tau) in B[X], E | Ehat, so [I_S]_E is read from I_S mod Ehat.
9. So [I_S]_E is determined by rho(S) in (B[X]/Ehat)^2. Part B holds (banked).
10. No false step: not ROUTE_CUT. Hypotheses are precise: not imprecise.
11. But Part A is only the kernel of the slope map; it says when slopes coincide.
12. It does not bound the number of distinct cosets (slopes) on the bad line.
13. Part B factors residue through base data; Cycle 1 warns this is not a count:
14. huge rho-fibers can carry few slopes, low-degree wi make I_S S-independent.
15. Neither part sees agreement nu(S)=|{x: I_S(x)=w(x)}| >= s_delta (Cycle 3).
16. So the claimed "rigidity half" is a restatement stopping at the wall.
17. The sharper missing invariant is named below; classification is EXACT_NEW_WALL.

Field ledger:
q_gen = p: base B; rho(S) and interp_S(w0),interp_S(w1) live in B[X]/Ehat.
q_line = p^2: slopes z and bad line F*[Bnum]_E live in F = F_{p^2}.
Kernel E*F_{<k}[X] is over F (I_S in F[X]); readout descends to B via Ehat.
q_chal: unused; no protocol denominator saving claimed.
No conj:B, prob:perfiber, line/list decoding, or ass:extension-mca-lift claim.
sigma=1 counterpacket not used; the statement is a reserve-agnostic restatement.

What to bank:
Do not bank as the rigidity half; it is kernel + banked reduction only.
Missing invariant (name it): a slope value-count / collision-rigidity law
bounding distinct z(S) in F over a-subsets that are on-line, noncontained,
and high-agreement (nu(S) >= s_delta), via rho on F*[Bnum]_E, reserve eta=sigma/n,
with a q_gen-vs-q_line ledger. This is the AA analogue of thm:rigidcyclo +
thm:exactcount: count the image on the agreement locus, not the kernel.

__FABLE_RS_MCA_PROXIMITY_PRIZE_RESEARCH_1781737175784_a0e29fe1fd76a_DONE__
