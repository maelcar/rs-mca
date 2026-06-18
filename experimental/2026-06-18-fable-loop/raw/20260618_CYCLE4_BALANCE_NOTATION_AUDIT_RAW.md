Now let me read the active walls, banked lemmas, and the key tex definitions.Now the critical source: the tex definitions. Let me find `def:residue` and surrounding context.I don't have bash. Let me use grep via the available tools — actually I only have Read. Let me read the relevant sections of the tex file directly. First I need to locate them.I have `def:residue`. Two things are now clear from source: `a = k+t` is the degree bound on `Q_z` (`deg Q_z < k+t`), and the support size is `|S_z| >= s_delta = ceil((1-delta)n)`. Let me confirm what "balanced t=sigma" and "slack sigma" mean in the loop, and whether `sigma = s_delta - k`. Let me read the Cycle 1/Cycle 2 raw and the blueprint's prob:F1.Let me check the residual-slack audit and the blueprint's prob:F1 to pin down `sigma` and the balanced relation.I now have everything needed. The decisive source is the banked residual-slack lemma, which fixes the notation: `a = k+sigma`, `|S_z| >= k+sigma`, so `s_delta = k+sigma` and the balanced case `t=sigma` forces `a = k+t = s_delta`. This directly contradicts Cycle 3's premise `s_delta >> a`.

```text
Final classification: ROUTE_CUT

Verdict:
Cycle 3's W-F1-AA-AGR is not source-valid as a balanced-case wall. It was built on
the inequality s_delta >> a = k+t, which is false in the balanced regime: by the
banked residual-slack notation sigma = s_delta - k, so balanced t=sigma gives
a = k+t = k+sigma = s_delta exactly. Cycle 3's false step is treating t as a
constant (t=2) while letting s_delta-k = ceil(eta n) be large -- that is the
*unbalanced* regime t<sigma, not balanced. In the genuine balanced case every
a-subset S has |S| = a = s_delta, so nu(S) >= s_delta is automatic and adds no
condition. The noncontainment lemma is correct and is kept; the high-agreement
"rigidity" sub-wall is cut. Restored balanced live wall: pure slope-image packing
for a = s_delta subsets (the arbitrary-base-anchor paired analogue of prob:perfiber,
with no agreement layer).

Notation audit:
- sigma in the F1/Cycle 2 target. From the banked F1 Residual-Slack lemma
  (def:residue): deg Q_z < k+t, |S_z| >= k+sigma. Since s_delta = ceil((1-delta)n)
  and delta = 1-rho-eta with k = rho n, s_delta = k + ceil(eta n). Hence
  sigma = s_delta - k = ceil(eta n). YES, sigma = s_delta - k here. (Distinct from
  the prefix-length sigma >= Cn/log_2 n in prob:perfiber/the monomial stratum; the
  operative F1 sigma is the agreement slack above k.)
- Balanced t=sigma => a = k+t = k+sigma = s_delta. YES, a = s_delta exactly.
  Consequence: for constant eta, sigma = Theta(n), so balanced t=sigma forces
  t = Theta(n). "Test case t=sigma=2" is balanced only if eta n = 2 (tiny radius,
  where again a = k+2 = s_delta). One cannot hold t=sigma AND s_delta-k >> t; the
  two are mutually exclusive. That contradiction is the false step.
- nu(S) >= s_delta in the balanced case. ADDS NOTHING. An a-subset has
  |S| = a = s_delta, and interp_S(w) agrees with w on all of S, so nu(S) >= s_delta
  automatically. The "high-agreement gap" exists only when a < s_delta, i.e. t<sigma.
- Balanced nonzero-numerator noncontainment lemma. CORRECT. Strongest source-valid
  form: for a degree-t datum (E,B,w) from def:residue with B != 0 (equivalently
  [B]_E != 0, since deg B < t = deg E), every support S with |S| >= a = k+t is
  noncontained, for every slope z. Proof (direction half alone): if G in F_{<k}[X]
  had GE = -B on S, then GE+B has degree < k+t = a and vanishes on >= a points, so
  GE+B = 0, forcing E | B, impossible for 0 != deg B < deg E. Containment needs both
  A and G explained; failure of G suffices. In the balanced case |S_z| >= s_delta = a
  covers every genuine witness, so noncontainment is automatic and free there.

Corrected bank:
KEEP from Cycle 3: the balanced noncontainment subset lemma (BANKED_LEMMAS
"F1 Balanced Noncontainment Subset Lemma") -- correct as written.
CUT from Cycle 3: W-F1-AA-AGR as a *balanced* wall, and the ACTIVE_WALLS claim that
"nu(S) >= s_delta" is the remaining filter "beyond choosing the a-subset" with
s_delta >> a. That premise is false when t=sigma. High-agreement is not a new
balanced invariant; where a<s_delta it is exactly the already-banked residual-slack
list object (slack sigma-t), routed to the list/local-limit ledger -- not a new wall.

Corrected live wall:
W-F1-AA (balanced, restored): with t=sigma so a=k+t=s_delta, bound the number of
distinct scalar slopes z in F such that some (k+t)-subset S of D has
[interp_S(w)]_E = z[Bnum]_E (equivalently rho(S)=(interp_S(w0),interp_S(w1)) mod Ehat
lands on the line F*[Bnum]_E), after tangent/contained (Bnum != 0, z != 0) and
quotient-periodic (rem:aper) separation. Every such subset is automatically a
genuine noncontained witness (its own support has size s_delta), so this is exactly
slope-image packing for a=s_delta subsets -- the arbitrary-base-anchor paired
analogue of prob:perfiber, with NO separate agreement-rigidity layer. The unbalanced
wall t<sigma stays where it already is: the banked residual-slack reduction to the
list/local-limit ledger at residual slack sigma-t (this is the only place
high-agreement / nu(S) >= s_delta is a live condition).

What to bank:
Bank the correction: sigma = s_delta - k in the F1 residue target, so the balanced
case t=sigma is exactly a = k+t = s_delta. In that case the Cycle 3 noncontainment
lemma makes every genuine witness automatically noncontained, and the high-agreement
condition nu(S) >= s_delta is automatic (it equals |S|), so W-F1-AA-AGR is vacuous as
a balanced wall and is cut. High-agreement is real only in the unbalanced regime
t<sigma, where it is the already-banked residual-slack list object, not a new wall.
The restored balanced live target is slope-image / bad-locus packing for the paired
base readout on a=s_delta subsets (arbitrary-base-anchor analogue of prob:perfiber).
Next prompt should attack that packing bound directly -- bounding distinct slopes z
with some a-subset on F*[Bnum]_E after tangent/quotient-periodic separation -- and
must not reintroduce an agreement-rigidity sub-wall in the balanced regime or claim
ass:extension-mca-lift, a q_chal denominator saving, or a line/list-decoding theorem.
```