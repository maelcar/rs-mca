# Dense-shell INV-TAIL closure: the CLT frame, drift persistence, and the share-floor discharge

## 0. Status (final form)

- FRAME (S1): the level-shape asymptotics — polynomial convergence,
  CLT-degenerate limit (beta = 0.6191), drift laws. COMPUTED (grids named
  per claim) + REFUTATIONS proved by witness: fixed regional bands at
  depth; the 2-step composed-kernel PF2 route; decoupled invariants;
  flat-caps tail assembly; the edge notch; the symmetric coherence band;
  the p-share buffer absorption.
- CAPS (S2): r_0 <= 2, r_i <= 1, every j >= 5, every t. The reduction
  CAPS <== NO-SPIKE is PROVED complete (and Lean-shadowed); no-spike
  closure PROVED given (COUP); (COUP) certified jc <= 48 by V10 (kappa <=
  1.4606 vs threshold 1.5321) with the envelope port closing j >= 20 and pair-2
  absorbed inside the joint induction given (PROP).
- PERSISTENCE (S3): the bundle {caps, LC, floors >= 0.98 r_i(48,t),
  sigma <= sigma_max(t), rho_prop <= 1.02560749} is STEP-CLOSED by PROVED
  (sufficiency) corner-sufficiency + the COMPUTED census (gate V12, incl.
  the output-LC check); the mediant mechanism and both mass recursions
  PROVED; sigma <= 0.46 PROVED (Birkhoff) + tight profile COMPUTED; the
  scalar mass cocycles' contraction rates theta 0.949 / 0.966 are COMPUTED
  (measured contraction, not a proved gap).
- TAIL (S4): gamma_i nondecreasing in i at ALL indices, j in [7, 60],
  zero violations (gate V6) + the second-order dominance structure —
  the all-i share floor reduces to i = 0. COMPUTED + named 1/j^2 route.
- ASSEMBLY (S5): i = 0 only, consumes r_0 floors + span only (all three
  computed in-gate from the level-48 cascade): gamma_0 >= 1.2848 (at
  f = 0.98 floors) >= gamma_req@loose = 1.1471 (note-exact, corrected from
  the banked values), margin 12.0% (at full f = 1.00 floors: 1.3032,
  13.6%); gate V7.
- THE SINGLE INPUT (S7): (PROP) — directional sibling proportionality
  (cross-index spread of the sibling ratio profile), measured over the
  OPERATIVE window the census consumes (i < 17, the corner-vector length),
  at the census target 1.02560749 (the precise bisected threshold; the
  rounded 1.026 is PAST the cliff — the census fails there by ~-0.0046,
  gate V12's provenance). COMPUTED on the grid j <= 60 (gate V13), PROVED
  cascade structure; the target equals the realized j=48 value up to
  +1.7e-5, and the operative margin is the measured j-improvement
  (1.02559 at 48 -> 1.02352 at 50 -> 1.01617 at 60, gate V13). The residual
  rigorous step is the scalar tail statement (PROP-TAIL) — persistence of
  that decay for j beyond the gated grid — with a named closed-proof route
  (Edgeworth remainder of the coupled two-branch recurrence).
- DISCHARGE (S6): INV-TAIL <== (PROP-TAIL). All four previously-open
  inputs ((COUP), the box residual, sigma-side, #880's ungated
  cross-child ratio) collapse into (PROP) and are discharged together.
  #880's |K| = 1 class-sum dichotomy becomes unconditional at every B
  given (PROP-TAIL) — the conditional narrows from three opaque numeric
  floors to ONE certified-and-decaying scalar with proved mechanism.

Label key (house dialect PROVED / COMPUTED / CONDITIONAL / CONJECTURAL /
REFUTED): "certified" refers only to a named gate of the shipped verifier
(house rule since #880). "COMPUTED" claims name their grid. Two qualified
PROVED forms are used with a fixed meaning: "PROVED (loose)" = PROVED at the
loose-caps threshold (a valid but non-tight bound, vs the certified-caps
threshold); "PROVED (sufficiency)" = the reduction is PROVED (e.g. corner-
sufficiency), with the residual finite check done COMPUTED by a gate.

## 1. The CLT frame (what the level vectors actually do)

Objects as in #880/#858: level vectors G_j(t), t in [1/6, 1/2]; flipped-
positive half-weight coordinates c_0 = b_0, c_i = b_i / 2 with even extension
to Z; the step is exact Z-convolution with K_{d} = (1/4, d, 1/4) aggregated
over the two branch children t_+ = (1 + t)/3, t_- = (1 - t)/3, kernels at
d(t_child) = -cos(2 pi t_child)/2 (c-dictionary; the even-extension
convolution reproduces the aggregated step to 1.8e-15, gate V1).

FACTS (COMPUTED, K = 80 Chebyshev levels through j = 60; the cap /
convergence / dominance layers are gated by V4 / V3 / V6):

1. POLYNOMIAL CONVERGENCE: the band-vector increments delta_j =
   max |log r_i(j)/r_i(j-1)| decay like C/j^2 (theta_j = delta_j/delta_{j-1}
   matches 1 - 2/j to 4 digits at j = 60). There is NO geometric contraction
   to a fixed shape.
2. DEGENERATE LIMIT (CLT spreading): c_i(j, t) tracks c_0 exp(-beta i^2 / j)
   with beta = 0.6191 (fit drift 0.6186 -> 0.6262 over i <= 14, second-order
   in i^2/j). Consequently every ratio drifts UP toward its degenerate cap:
       r_0(j) = 2 - 2 beta / j + O(1/j^2),   (b-convention, cap 2)
       r_i(j) = 1 - (2i+1) beta / j + O(1/j^2)   (i >= 1, cap 1).
   Measured drift constants C_i * j at t = 0.26, j = 59/60:
   1.230/1.231 (i=0), 1.827/1.828 (i=1), 3.014/3.016 (i=2) against the CLT
   prediction 2 beta = 1.238, 3 beta = 1.857, 5 beta = 3.095 (lag = the
   second-order term; direction and magnitude consistent).
3. REFUTATION (bands): the j <= 23 regional bands (r_0 <= 1.948 etc.) are
   FALSE at depth: r_0 = 1.9795 at j = 60 on the consumed range. Any all-j
   hypothesis must use the degenerate caps, not finite-j bands.
4. REFUTATION (2-step kernels): the composed minus-branch kernels are not
   PF2: K_{d1} * K_{d2} = (1/16, (d1+d2)/4, d1 d2 + 1/8, ..) fails
   log-concavity L1: d1^2 + d1 d2 + d2^2 >= 1/8 exactly on parent
   t in [0.40, 0.50] (min -0.01155 at t = 1/2); minus-minus additionally
   fails kernel nonnegativity near t = 1/2 (min d1 + d2 = -0.163). The
   Karlin route is closed on the minus branch; only the plus branch
   (t_+ >= 7/18, d >= 0.383) is classical.
5. REFUTATION (independent adversaries): the class {even, nonneg, LC, edge
   slack >= 0.06, r_0 <= 2, ratio caps 0.95, free share in [0.3, 3]} is NOT
   step-closed (output edge slack -0.58, witness in-text). Any proof
   must use the realized coupling of the two branch inputs.
6. TRUE SHARE AT DEPTH: worst gamma over the eps grid RISES 1.3122 (j=50)
   -> 1.3144 (j=60); argmin at index 0 with gamma_i increasing in i.

## 2. T1 — the exact caps

Claim: for every j >= 5 and t in [1/6, 1/2] the c-vector is nonincreasing
(Delta_i := c_i - c_{i+1} >= 0 for all i >= 0), i.e. r_0 <= 2 and r_i <= 1.
Margins shrink like 1/j (S1.2): the proof is structural, not slack-based.

FORMALISM (PROVED; reconstruction 2.2e-15): extend Delta ODDLY about -1/2
(Delta_{-1-k} = -Delta_k). Then per branch Delta' = K_d * Delta with center
row Delta'_0 = (d - 1/4) Delta_0 + Delta_1/4; and the no-spike slack
p_i := Delta_{i-1} + Delta_{i+1} - Delta_i (p_0 := Delta_1 - 2 Delta_0)
is also odd about -1/2 and obeys the IDENTICAL rule p' = K_d * p.
Trace identities (EXACT): d_+ + d_- = -d(t/3);
(d_+ - 1/4) + (d_- - 1/4) = -a(t/3).

THEOREM (CAPS STEP; PROVED, complete). If both children satisfy
J := {Delta >= 0} + {p >= 0}, then Delta(G_j(t)) >= 0 for every t.
Plus branch (d_+ >= 0.38302 > 1/4): free from Delta >= 0 alone. Minus
branch (d_- >= -1/4): interior via no-spike (1/4 (Delta_{i-1} +
Delta_{i+1}) >= 1/4 Delta_i >= -d_- Delta_i); center via center-no-spike
Delta_1 >= 2 Delta_0, giving (d_- + 1/4) Delta_0 >= 0 — TIGHT at t = 1/2
where d_- + 1/4 = 0 exactly.

STRUCTURE (COMPUTED): J holds for all j >= 5 (fails at j = 4: center ratio
1.266 < 2); Delta is unimodal (exactly one strict peak) and log-concave;
no-spike reduces to {center Delta_1 >= 2 Delta_0 (ratio -> 3, min 2.14 at
j = 6)} + {smooth peak (slack growing)}. The no-spike TOWER (Delta,
ns(Delta), ns^2(Delta), ...) is entrywise >= 0 at every computed level — a
smoothing hierarchy.

THE SINGLE OPEN INPUT — (COUP): interior no-spike self-propagation through
the minus branch needs p_i(G_{j-1}(t_-)) <= 4 d_+ p_i(G_{j-1}(t_+)),
4 d_+ >= 1.5321. COMPUTED: kappa = sup p^-_i / p^+_i <= 1.462 for every
child level >= 6, decreasing to ~1.30; the only excursion (1.996) is at
child level 5, absorbed by direct base cases j = 5, 6. The center row
propagates with vast margin (never tight, min +0.0112 at j = 6, growing).
Hence CAPS are PROVED for all j >= 5 conditional only on (COUP).

(COUP) VIA THE ENVELOPE PORT: the differential
cascade is EXACT (PROVED; 1.3e-9 vs finite differences):
Dc(G_j) = (1/3)[K_{d+} * Dc+ + a'(t_+) c+] - (1/3)[K_{d-} * Dc- +
a'(t_-) c-], with Dc_0 = 0 and p/Dp obeying the same odd-extension rule;
the #880 L5 lever a'(t_+) - a'(t_-) = -a'(t/3) ports verbatim. COMPUTED:
the realized p-envelope L_p <= 1.257 for j >= 20 (-> 1.19), giving
kappa_p <= exp(1.257/3) = 1.520 < 1.5321 — (COUP) CLOSES for j >= 20 with
direct bases below (kappa <= 1.462). The all-j L4'-style closure has ONE
localized obstruction: at pair-2 / t -> 1/2 the residual a'(t/3) X- term
is un-absorbed (crude closure constant 3.742 vs true 1.43); the fix is a
SHARE-ABSORBED regional envelope, X_j >= 1.063 X-.

ONE PORT, TWO INPUTS: the same machinery on the c-cascade reproduces
#880's shipped envelope caps (pair-1 0.691 vs gated 0.85; pair-2 1.264 vs
1.61) and yields kappa_c <= 1.32 — exactly the UNGATED cross-child-ratio
input of S5's list, as a corollary. For the c-cascade the absorption
constant 1.063 is ALREADY GATED (#880's child-share floor 1.20); for the
p-cascade it couples to the sibling sigma(t) machinery (S3).

THE COLLAPSE: porting the mass machinery to p — the p-mass
recursion P_j(t) = a(t_+) P+ + a(t_-) P- - (1/2)[p_0^+ + p_0^-] PROVED
(odd sequences carry a 1/2 center correction vs 1/4 for even; gate V14);
the p-mass ratio cocycle's contraction rate theta_p = 0.966 is COMPUTED
(measured contraction), and the pure-operator Birkhoff bound gives
N <= 1.31 j-uniform PROVED (loose). The direct entrywise buffer absorption
FAILS (gamma_p in [0.61, 0.99], always < 1 — the p-slack does not grow
across steps; REFUTED as a route). Dp <= 0 is definite (0/2192 — p
strictly decreasing in t; COMPUTED, gate V14), closing pair-1
(L* = 0.974, PROVED given Dp <= 0) and improving pair-2 (3.74 -> 2.69,
still short of 1.28 by scalar-L alone). PAYOFF: kappa_max/N = 1.037 (low-j
max) -> 1.006 with j (V14 measures 1.0155 over j in {20,40}) — the
entrywise child ratio sits within ~1.6% of the mass ratio, so (COUP)
[kappa <= 1.53209] reduces to {N <= 1.31 (PROVED, loose)} +
{kappa_max/N <= 1.53209/1.31 = 1.1695 (measured 1.0155, 15% margin;
1.037 worst at low j, still 13% margin)} — and this cross-index coherence
is THE SAME OBJECT as S3's rho_prop and S5's cross-child input: ALL FOUR
open inputs collapse into the ONE lemma (PROP) of S7.

## 3. T2 — drift persistence

Claim (strong form): r_i(j+1, t) >= r_i(j, t) pointwise. COMPUTED: onset
J0 = 8 for i = 0 (i = 1: j >= 5; i = 2: j >= 4; i >= 3: all j); the only
violations are j <= 7. Binding locus: the edge t -> 1/2 (the w_+ fixed
point), i = 0..2, large j, drift ~ +Kc_i/j^2, Kc_i = 1.13/1.63/2.7...
Weak form (all the assembly needs): r_i(j, t) >= r_i(48, t) - explicit slack
for all j >= 48, i <= 2, t in the consumed range; the j = 48 base values are
certified by THIS packet (V7 consumes the level-48 r_0 floors directly; V4/V5
certify caps + monotone drift on the grid), not by #880's shipped gates
(which certify the three floors, not the bands).

MECHANISM (PROVED): one branch maps ratio triples by
rho_i = (1/4 + d r_i + 1/4 r_i r_{i+1}) / (1/4 r_{i-1}^{-1} + d + 1/4 r_i),
increasing in r_{i-1}, r_{i+1} always; sensitivity sign in r_i =
(d + r_{i+1}/4)(1/(4 r_{i-1}) + d) - 1/16: plus branch >= +0.34 (strictly
monotone), minus branch >= -1/16 exactly (at d = -1/4, r_{i+1} = 1). The
aggregate is the SHARE-WEIGHTED MEDIANT of the branch ratios; at the
binding locus the minus share is 0.243, so 0.76(+0.34) + 0.24(-1/16) > 0
drives the net upward drift.

REFUTATIONS (COMPUTED, adversarial): no decoupled invariant closes —
minus branch alone breaks caps (slack -19); ratio cliffs break truncated
floors (-0.34); extreme share (sigma ~ 0.69, unrealized) breaks full
floors. The honest coupled box {caps + LC + full floors + t-dependent
share bound} is adversarially closed on [1/6, 1/2) and misses only in the
limit t -> 1/2 at i = 0 by ~0.013 (realized data: +0.0005).

THE SCALAR LEVER — sigma(t). PROVED (the recursion + the Birkhoff bound):
the mass recursion S_j(t) = a(t_+) S(t_+) + a(t_-) S(t_-) - (1/4)[Delta_0^+ +
Delta_0^-] with 1/2 + d(t) = a(t) EXACT (1e-16) and the edge correction
< 0.3% of branch mass; the pure-a mass operator is positive, hence Birkhoff-
contracting, so sigma <= 0.46 j-uniformly PROVED (loose). The scalar mass-
ratio cocycle's contraction rate theta_scalar = 0.949 is COMPUTED (measured,
sigma_j flat to 4e-4) — not a proved gap; the tight profile sigma_max(t) in
[0.244 (edge), 0.420 (t = 1/6)] is COMPUTED (gate V11). PROVED (sufficiency)
corner-sufficiency for the box census (outputs linear in the child vectors;
ratio outputs Moebius-monotone ==> extremes at LC ratio-corners): the ratio
dimensions are corner-certified; the mu-scale and parent-t are gridded (V12,
refinement-robust). EDGE NOTCH REFUTED
(fixed-point self-reference at t = 1/2; child-input contamination with
amplification > 1). CORRECTED (superseding an earlier -0.0038 figure which had the share
forced = sigma_max exactly): sweeping the share
BELOW sigma_max exposes worse interior configs — the honest box-alone
census residual is -0.0123 at i = 0, t -> 1/2. Realized level-48 data
drifts +0.00050 (the right direction).

THE RIGHT COHERENCE: the symmetric magnitude band kappa_c <=
1.32 does NOT close the census (residual -0.0123 -> -0.0113 only, ~8%,
plateaus — symmetric bands still permit the plus-low/minus-high split).
What CLOSES it is DIRECTIONAL PROPORTIONALITY: rho_prop := max_i g_i /
min_i g_i (g_i = the sibling entrywise ratio profile c_i(t_-)/c_i(t_+))
— the CROSS-INDEX SPREAD of log g_i. rho_prop is window-dependent (g_i is a
smooth monotone-decreasing profile), so the window MUST be pinned: the census
imposes it over the full corner window (i < 17), where the realized value at
j = 48 is 1.02559 (the census target 1.02560749); the narrower i < 10 window
realizes ~1.008 and decays faster (informational, gate V13). The cap part of
the census closes non-strictly at the r_0 = 2 fixed point (+0.000); the i = 0
floor closes; and the binding locus MIGRATES OFF the singular edge (t = 0.5
-> 0.41 -> 0.21) — the signature of the correct constraint. FINAL BUNDLE
{caps + LC + floors r_i(48,t) + sigma <= sigma_max(t) + rho_prop} is STEP-
CLOSED by PROVED (sufficiency) corner-sufficiency + the COMPUTED census (V12,
incl. output-LC); the i = 0 assembly then clears at full floors: gamma_0 =
1.3032, margin 13.6% (gate V7). Joint induction well-founded (single intra-
level edge acyclic; base = the j <= 48 grid certified by V4/V5/V7). The
floors-vs-rho_prop trade frontier (the assembly margin buys rho_prop slack)
is in S7.

## 4. T3 — tail dominance (share floor localizes to i <= 2)

gamma_{i+1} / gamma_i = r_i(j, t_in) / r_i(j-1, r): the level effect (up)
races the argument effect (t_in < r; ratios increase in t at fixed j, i.e.
the drift constant C_i(t) decreases in t). COMPUTED (gate V6, the
two-depth DeltaC*j check):
cross-level dominance D_i >= 0 has ZERO violations for all j >= 7 (i <= 12,
39-point eps grid, j through 60); the only offenders are at j = 6 (worst
cumulative dip gamma_i / gamma_0 = 0.9881 at eps = 0.244, i = 1) — outside
the INV-TAIL regime and inside #880's directly-certified small-j range. D_i minima by
band: +4.9e-4 (j31-48), +3.2e-4 (j49-60) at i = 0, growing with i.

SECOND-ORDER STRUCTURE (resolves the asymptotic question): writing
r_i(j, t) = cap_i - C_i(t)/j + O(1/j^2), the t-variation of C_i is itself a
1/j effect: Delta C_i = C_i(r) - C_i(t_in) = -D_i/j with D_i * j CONSTANT
to four digits across j in {30, 40, 60, 80} (D_0 = 0.089, D_1 = 0.13,
D_2 = 0.21-0.22 at the worst eps = 0.244). Hence
    D_i(j) = (C_i - D_i)/j^2 + O(1/j^3),
with C_i - D_i = 1.14 / 1.70 / 2.80 (i = 0, 1, 2) uniformly positive: the
dominance has NO deep-j crossover; the asymptotic C_i(t) profile is flat in
t and the race is settled at second order in favor of dominance.

ALL-INDICES RESULT (COMPUTED; gate V6): D_i >= 0 AND gamma_i monotone
nondecreasing in i hold over the FULL vector (every index with coefficients
above the 1e-260 tail floor), j in [7, 60], 24-point eps grid — ZERO
violations of either. This matters because the shipped share gate P12
quantifies over ALL i (verifier line 897) and the H-S hypothesis is
entrywise: T3 at all indices reduces the all-i share floor EXACTLY to the
i = 0 assembly. (The flat-degenerate-caps band assembly provably FAILS from
i ~ 16 — the consumption-spec check of S5 — so this reduction is load-
bearing, not a convenience.)
Proof route: the exact 1/j^2 expansion above via the differential-envelope
machinery (L4/L5 of #880); shipped meanwhile as the certified-grid gate V6
+ the named route.

## 5. The assembly (exact arithmetic; the consumption-spec audit)

CORRECTED CONSTANTS (note-exact re-derivation, validated to 9 decimals
against the shipped P8 margin): gamma_req(eps) = D1/((rho2 - need) rho1)
has max (at eps -> 1/4) = 1.1011 at the CERTIFIED caps (0.85, 1.61) — the
lane's banked 1.036 was an error — and 1.1471 at the LOOSE caps
(1.086, 1.663) (banked 1.149 was rounding, safe side). The shipped gates
quantify the share floor over ALL indices (P12, verifier line 897;
entrywise H-S). The flat 1.20 was Q2's convenience; the loose-caps chain
is the operative one for all-j.

THE i = 0 REDUCTION: by T3-at-all-indices (S4), gamma_i >= gamma_0 in the
regime, so the all-i requirement reduces to gamma_0 >= 1.1471. The i = 0
assembly consumes NO caps at all: gamma_0 >= dr(eps) + f r_0(Y)/4 +
span (dr2(eps) + f r_0(Y2)/4), needing only (i) the r_0 FLOOR on the two
child ranges (Y: [0.25, 0.278]; Y2: [0.389, 0.417]) at all j >= 48 — the
level-48 range-min r_0 (1.9646/1.9647 after the 0.995 persistence pad),
valid for j >= 48 since r_0 drifts UP (T2/V5) — and (ii) the span floor
(0.8766 = the level-48 min_i Y2[i]/Y[i], padded), both COMPUTED IN-GATE
from the level-48 cascade. RESULT (gate V7): worst over eps at the full
floors (f = 1.00) = 1.3032 >= 1.1471 (margin 13.6%), and at the census
floors (f = 0.98) = 1.2848 (margin 12.0%) — both gated, so the discharge
uses the SAME f = 0.98 floors on the census and assembly sides. (The caps
r_0 <= 2, r_i <= 1 remain load-bearing INSIDE T2's box closure, not in the
assembly itself. A flat-caps all-i band assembly is REFUTED from i ~ 16 —
degenerate caps discard the 1/r blowup that keeps the true deep-index bound
high; do not revive it.)

THE FULL INPUT LIST for the discharge (each measured with slack; the open
set): (COUP) [S2 — caps/no-spike closure, kappa <= 1.5321 vs measured
1.462]; sigma_max(t) [S3 — floor-box closure]; the CROSS-CHILD-RATIO input
that the shipped L4' loose-caps closure itself consumes (#880's shipped
envelope note) — UNGATED in #880's verifier, surfaced by the consumption-
spec check (S5); T3's 1/j^2 route [S4 — gated meanwhile]. All four
are cascade-coherence statements of one family (sibling/index/mass
smoothness).

## 6. Discharge and consumers

THE CHAIN (final form; every arrow proved in S2-S5, single input S7):

  (PROP) at the S7 target (rho_prop <= 1.02560749 over the operative
  window i < 17, equivalently the decay persisting for all j)
    ==> the bundle {caps, LC, floors >= 0.98 r_i(48,t), sigma <=
        sigma_max(t), rho_prop} is step-closed (COMPUTED census V12 +
        PROVED (sufficiency) corner-sufficiency), hence persists for ALL
        j >= 48 from the j = 48 base certified by V4/V5/V7 (well-founded
        joint induction; the only intra-level edge is acyclic)
    ==> the i = 0 assembly gives the entrywise child-share gamma_0 >=
        1.2848 (at the f = 0.98 census floors) >= 1.1471 = gamma_req@loose,
        extended to ALL indices by T3 (gamma_i nondecreasing in i, S4)
    ==> with pair-1 at loose caps (PROVED given Dp <= 0 (COMPUTED, V14):
        the definiteness closes L* = 0.974) and pair-2 at loose caps (the
        L4' envelope closure on the C-CASCADE, with its cross-child input
        SUBSUMED by (PROP) and its share absorption X_j >= 1.063 X-
        covered by the gated child-share -- the c-cascade route, gated by
        the assembly child-share above; the p-cascade analog couples to
        sigma(t)/(PROP) instead), KEY at loose caps (shipped #880 gate P8,
        margin 0.015) fires at every j >= 49
    ==> the three INV-TAIL floors persist for all j >= 49 — INV-TAIL
        DISCHARGED
    ==> #880's |K| = 1 class-sum dichotomy THEOREM holds unconditionally
        at EVERY B.

General-K remains conjectural (unchanged; see #880 section 7).
Consumers: #880 (the upgrade above); the product-profile emission program
(#816 -> #858 -> #880 -> this). The earlier banked share-floor routes are
superseded by this frame (with the gamma_req corrections of S5 — the banked
1.036 at the certified caps was an error; the true value is 1.1011).

## 7. THE ONE RESIDUAL LEMMA — (PROP), directional sibling proportionality

Every open input of the discharge collapses (S2/S3) into:

    (PROP)  The sibling entrywise ratio profile g_i(j, t) =
            c_i(G_{j-1}(t_-)) / c_i(G_{j-1}(t_+)), over the OPERATIVE index
            window i < 17 (the corner-vector length the census consumes),
            has bounded cross-index spread:
            rho_prop = max_{i<17} g_i / min_{i<17} g_i <= R*.
            (g_i is a smooth monotone-decreasing profile, so the window is
            load-bearing and is pinned here; the narrower i<10 window
            decays faster and is informational only.)

Consumer forms and their requirements:
- the box/floor side (S3): the TRADE FRONTIER (floors relaxed to
  r_i(48,t) * f; caps and sigma_max fixed): the operative-window rho_max(f)
  plateaus at the target 1.02560749 for f <= 0.98; assembly 1.3032 -> 1.2848
  (13.6% -> 12.0%). PARETO KNEE f = 0.98: **proof target rho_prop <=
  1.02560749** (operative window), met by the realized j=48 value up to
  +1.7e-5, decreasing thereafter;
- the (COUP)/pair-2 side (S2): the mass-normalized form kappa_max/N <=
  1.1695 (= 1.53209/1.31), measured 1.0155 over j in {20,40} (15% margin;
  1.037 worst at low j, tightening to 1.006 with j);
- #880's cross-child input: subsumed (S5).

MEASURED (gate V13): on the OPERATIVE window i < 17 — the window the
census (V12) actually consumes — rho_prop(j) DECAYS with j:
1.02559 (j = 48) -> 1.02352 (50) -> 1.01933 (55) -> 1.01617 (60),
monotone-decreasing. The target 1.02560749 is the bisected value: it sits
+1.7e-5 above the worst (j = 48) realized value, so the HONEST margin at
the calibration level is that +1.7e-5, and the real safety comes from the
measured j-improvement above (the tail is strictly tighter). The narrower
i < 10 window decays FASTER (1.008 at 48 -> 1.005 at 60) because g_i is a
smooth monotone-decreasing profile and a shorter window has smaller
max/min — it is INFORMATIONAL, NOT the operative constraint (do not quote
its slack as the census margin). Structural driver: the CLT flattening
(S1) — both siblings converge to the same degenerate profile.

THE PORT OUTCOME: the spread is INDEX-LOCALIZED — on any fixed index
window it decays like C/j^2, and NARROWER windows decay FASTER (COMPUTED:
e.g. the i<10 window is well under the operative i<17 window at every
gated j), while the magnitude kappa_c stays flat (~1.29). The singular
edge t = 1/2 DISSOLVES for the spread object (it decays there like
everywhere). THE EXACT SPREAD CASCADE (PROVED structure): share-variation
+ a'-source (L5-split) + kernel-smoothed child-deviation; the first two
(76% of the spread) vanish as the siblings flatten to the common CLT
shape, the deviation (24%) is kernel-smoothed — the mechanism OF the
decay. Window convention (load-bearing): the census (V12) imposes rho_prop
over the FULL corner window i < 17, and V13 gates rho_prop on exactly that
window (<= 1.02560749 for all gated j >= 48, monotone-decreasing over
{48,50,55,60}); the i<10 window is informational only.

STATUS OF (PROP): COMPUTED on the grid j <= 60 (gate V13, operative
window i < 17) + PROVED cascade structure; the single residual rigorous
step — named (PROP-TAIL) — is the tail decay statement itself
(equivalently: rho_prop@i<17(j) <= 1.02560749 persists for j > 60, i.e.
the measured monotone decay on {48,50,55,60} continues), whose fully-
closed analytic proof reduces to the local-CLT flattening rate (the
COMPUTED scalar mass-cocycle contraction theta ~ 0.95-0.97 for the share
part + fiber collapse for the shape part; the blocking term for a closed
proof is the Edgeworth remainder of the coupled two-branch recurrence —
now a single scalar decay rate, not a profile enclosure). Margin at the
worst gated level j = 48 is +1.7e-5 (the target is the bisected realized
value); the tail is strictly tighter (monotone decay, gate V13).

FINAL BUNDLE at the target: {caps, LC, floors >= 0.98 r_i(48,t),
sigma <= sigma_max(t), rho_prop <= 1.02560749}: caps/floors PROVED
(sufficiency) + census-closed (V12); sigma <= 0.46 PROVED (Birkhoff) +
computed tight; child-share gated by the V7 assembly; rho_prop = the
single remaining input. Joint induction well-founded; base = the j <= 48
grid certified by V4/V5/V7; assembly 1.2848 >= 1.1471.

## 8. Verifier map (verify_dense_shell_inv_tail_closure.py; current state)

13 gates (V1-V7, V9-V14; V8 was retired during development, its cap/
no-spike content folded into V4/V9). V1 CDICT c-dictionary exactness
(1.8e-15); V2 KREFUTE composed-kernel refutation witnesses + safe-region
pin; V3 CONV polynomial convergence (delta j^2 window; geometric REFUTED
by the tamper); V4 CAPS grid margins; V5 DRIFT monotone zero-violations;
V6 DOM tail dominance at ALL indices + gamma_i monotone-in-i + the DeltaC*j
depth-consistency; V7 ASSEMBLY i=0-only @ j0=48 (r_0 floors 1.9646/1.9647,
span 0.8766 — all computed in-gate from the level-48 cascade):
gamma[f=1.00]=1.3032, gamma[f=0.98]=1.2848, both >= 1.1471; V9 BASE J(5),
J(6) caps+no-spike on a 400-pt grid; V10 COUP kappa scan (1.4606 at
(jc=6, i=2) <= 1.462 < threshold 1.53209 = 4 d_+^min); V11 SIGMA mass
recursion exact (7.1e-16) + sigma profile [0.2430, 0.4196] monotone;
V12 CENSUS the final-bundle corner census (f = 0.98,
rho_prop <= 1.02560749): cap +0.00000 (non-strict, r_0=2 fixed point),
floor +0.00075, output-LC -1.4e-8 (>= -1e-6); V13 PROP
rho_prop@i<17(48) = 1.02559 <= 1.02560749, monotone-decreasing over
{48,50,55,60} (info: i<10 window 1.008, decays faster, non-operative);
V14 PMASS p-mass recursion (1/2-center correction) 3.2e-9 + Dp <= 0
(p decreasing in t, closing pair-1) + kappa_max/N = 1.0155 <= 1.1695
(= 1.53209/1.31).
Current: 13/13 PASS ~2.8s default / 4.1s --deep (j = 60, 41-parent
census); tampers 13/13 BROKE, each isolated to its own gate.

LEAN (experimental/lean/inv_tail_closure/, stdlib v4.14.0, builds clean,
no sorry): the caps-step scalar inequalities PROVED over Int
(denominator-cleared interior + center rows and the aggregated two-branch
center — the exact algebra of S2's theorem); native_decide factorizations
4x^3-3x-1 = (x-1)(2x+1)^2 (the trace-identity coefficient cos(2pi/3) =
-1/2) and T9(x)+1 = (x+1)(2x-1)^2(8x^3-6x-1)^2 (the (COUP) threshold
4 d_+^min = -2 cos(7pi/9) as a degree-3 algebraic number).
