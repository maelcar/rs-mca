# Dense-shell class charges: the class-sum sign dichotomy, the master inequality, and certified charge arithmetic

## Status

```text
Status: labels are exact to the shipped artifacts, REPAIRED per audit
        #914 (COUNTEREXAMPLE verdict on the integrated a575019/#880
        packet: two claims were false as shipped, both corrected
        below with permanent regression gates P13/P14): every PROVED
        claim has a complete proof or is stated as an explicit
        hypothesis it depends on; every certified constant has a
        named verifier gate; COMPUTED-GRID/CONDITIONAL marks a
        finite-grid result with no continuum enclosure yet.
      + Integration-order note (PR #905 compatibility): PR #905
        (head 0000964, independently audited in #911 head 8d47b40)
        separately proposes discharging INV-TAIL for every B via a
        transfer-shape Arb certificate. If #905 integrates BEFORE
        this repair, read its "UNCONDITIONAL for every B" wording as
        COMPUTED-GRID/CONDITIONAL until audit #914's three enclosure
        gaps (3.5: P7 interpolation remainder, P9 observed-slope-as-
        bound, P12 endpoint-omitted sampling) are independently
        closed, and apply this repair's C3/C3b/3.2 hunks against
        #905's landed text with the same semantic outcome: sign-
        correct C6 (below), coupled-curve-scoped P7, hypothesis-
        labeled loose caps crediting #905 as producer. If this repair
        integrates FIRST, #905's later hunks should extend the SAME
        COMPUTED-GRID/CONDITIONAL label to the beyond-49 tail rather
        than reinstating UNCONDITIONAL outright.
      + PROVED (C1, kernel reduction): for U subseteq {0..B-1} the
        support-class sums of the inverse transform obey
          sum_{sigma in class(U)} h(sigma)
            = (1/c) sum_{xi dense} hatf(xi) prod_{i in U} 2cos(theta_i)
            = (-4)^{|U|} (1/c) sum_xi hatf(xi) prod_{k in K}(a_k - 1/2),
        K = {B - i : i in U} in scan coordinates: one line from the
        exact-support character sum and 2cos(2 pi u) = -4(a - 1/2).
      + PROVED (C2, the atom): the tightest inequality of the program,
          1/2 - a(t_out/3) >= need(eps) (1/2 - a(t_in/3)),
        eps in [0,1/4], t_in = 1/4 - eps/3, t_out = 5/12 + eps/3,
        need = sin(2 pi eps/3)/sin(2 pi (1/6 + eps/3)): product-to-sum
        gives sin(7pi/18) cos(phi) - sin(pi/18) cos(phi/2) on
        phi in [2pi/9, 4pi/9], strictly decreasing, endpoint value
        exactly sin^2(pi/18) > 0.
      + COMPUTED-GRID/CONDITIONAL (C3, master + purity + |K|=1
        dichotomy; DOWNGRADED from THEOREM by audit #914 -- 3.5 lists
        the exact open items that would restore THEOREM): the MASTER
        inequality G_j(t_out) >= need(eps) G_j(t_in) holds on every
        tested grid point — base cases j <= 5 proved (j = 1 = the
        ATOM, closed form; j = 2..5 slope-certified grids, gate P9),
        general step j >= 6 holds from three invariant floors tied by
        the single scalar (KEY) — and with it cone purity of G at
        every state and the |K|=1 class-sum dichotomy at every depth,
        via the chain R1-R4. Scope: for every B <= 49 — the three
        consumed floors (pair-1 envelope <= 0.85, pair-2 <= 1.61,
        child-share >= 1.20) are verifier-certified on the MASTER-
        consumed COUPLED child curves (s+r=4/9, r2+s2=8/9 — 3.2 Step
        B) at every level q = j-1 in [5,47] (gate P7 under --deep, a
        4x-denser eps-grid with both boundary endpoints included;
        measured sups 0.597/1.230, well inside cap) and child-share
        >= 1.20 (gate P12, min 1.215); (KEY) at exactly those caps has
        margin 0.030 (gate P8). Why COMPUTED-GRID and not THEOREM:
        P7's interpolated cascade carries no interpolation-remainder
        bound and no between-node continuum enclosure; P9 calls its
        bases "Lipschitz-certified" but the constant is an OBSERVED
        discrete slope used as a global bound; P12 samples 199
        interior epsilon values and omits both limiting endpoints.
        These are deterministic floating-grid checks, not continuum
        certificates (3.5). For ALL B, HYPOTHETICAL on the single
        named input (INV-TAIL): IF the same three floors persist for
        j >= 49, THEN the conclusion extends to every B. INV-TAIL's
        envelope part now has an external producer: PR #905 (head
        0000964) proves the all-j loose caps 1.086 pair-1 / 1.663
        pair-2 (after the L5 cancellation a'(t_+) - a'(t_-) =
        -a'(t/3)) and a 7/6 child-share floor via a positive two-state
        cone, MODULO #905's own finite Arb continuum certificate
        (independently audited in #911, head 8d47b40: symbolic half
        verified, Arb half not replayed there). (KEY) at (1.086,
        1.663, 1.20) has margin 0.015 (gate P8) as a CONDITIONAL check
        on those hypotheses, not a proof of them. Open: #905's Arb
        certificate replay, and — independently of #905 — the
        between-node continuum enclosures this packet still lacks;
        routes in 3.5.
      + PROVED (C3b, the general-K reduction; NARROWED by audit #914
        SHOULD item -- SUFFICIENT, not equivalent): for
        K = {k_1<...<k_r} positivity of every decorated subtree charge
          T_pi(K) = sum_i c_i b_i(g^pi_{k_1-1}) b_i(G^S(t_pi)) > 0
        (c_0 = 1, c_{i>=1} = 1/2; pi over depth-(k_1-1) prefixes; G^S
        the drift-decorated cascade, S the relative pattern) IMPLIES
        the dichotomy statement E_w[prod_K(a_k-1/2)] > 0 — termwise
        positivity of E_w = (4^B/W) sum_pi T_pi is SUFFICIENT for the
        positivity of the sum; the CONVERSE (global positivity forcing
        every T_pi > 0) is OPEN and not claimed. This matches what P11
        actually checks: the reduction identity plus ALL T_pi > 0,
        exhaustively over every K and every prefix, at B in {6, 8}
        only — not a proof of the converse at any B. |K| <= 1:
        T_pi > 0 PROVED with C3's scope (COMPUTED-GRID/CONDITIONAL,
        B <= 49; INV-TAIL beyond, see C3). |K| >= 2: T_pi > 0 verified
        EXHAUSTIVELY
        (every K, every prefix, B in {6, 8}, gate P11;
        no cancellation, min normalized term +9.9e-4) — CONJECTURAL
        in B; proof route = the aggregated joint two-walk cone. Two
        tidy candidate lemmas are REFUTED and must not be claimed:
        cone-purity of G^S (false from S = (1,2,3) on) and the
        decorated Master (min-ratio 0.045 << need at S = (1,2)).
      + COMPUTED (C4, exhaustive law): sign(class-sum(U)) =
        (-1)^{B-|U|} for EVERY U at B in {4,6,8,10} (all 2^B supports),
        min |class-sum| = 2.615 / 6.583 / 17.72 / 49.30 — growing along
        the chain, as #858 D5's min|hatf| does.
      + COMPUTED (C5, leak table at B = 10): pointwise wrong-sign
        |h|-mass share by |U|: 0 (exactly, |U| <= 3), 9.42e-6 (4),
        1.30e-3 (5), 7.84e-3 (6), 2.72e-2 (7), 6.63e-2 (8), 1.21e-1
        (9), 1.86e-1 (10). Purity is asymptotic in B - |U|; the
        emission arithmetic must carry the leak, not a threshold.
      + PROVED (C6, charge arithmetic; REPAIRED by audit #914 MUST
        item -- the old "Sigma_U + W_U always" identity is FALSE,
        deleted below, gate P13 pins the fix): omega(class) = h_+ =
        W_U + 1_{s_U=+1} |Sigma_U| exactly, where s_U = (-1)^{B-|U|}
        is the class-sum sign law, Sigma_U the signed class sum, W_U
        the wrong-sign mass (definitional: h_+ = sum of the positive
        class values). Equivalently, ALWAYS (no sign-law dependence):
        omega(class) = (M_U + Sigma_U) / 2, M_U = sum_class |h|. The
        s_U=+1 case reads |Sigma_U| + W_U = Sigma_U + W_U (since the
        law makes Sigma_U >= 0 there); the s_U=-1 case reads W_U alone
        — this is the note's wrong-parity formula below, already
        correct as shipped. Counterexample to the deleted "always"
        form: B=4, U={0}, s_U=-1, Sigma_U=-3.599182825207051,
        W_U=omega_U=0, so Sigma_U+W_U=-3.599... != 0 (audit #914; gate
        P13 exhaustively checks the corrected identity instead, every
        U, every B <= 8, both parities). |Sigma_U| is computable with
        a certified additive bar by the insertion DP below; W_U is the
        computed leak layer (the shipped table pins the per-|U|
        aggregate; per-class W_U is defined, not tabulated).
      + PROVED (C7, certified insertion DP): the u-state-collapsed
        function-valued transfer DP evaluates every subset charge in
        one pass; inserted levels carry one extra analytic factor
        2cos(2 pi w), so the #858-D6 Bernstein bar becomes
          eps(B, K, |S|) <= 4 lam^B fac^{|S|} rho^{-K} / (rho - 1),
        lam = 24.85, fac = 12.42, rho = 5 — still poly(B, log 1/eps).
        Instantiated at B = 6, K = 24: observed 3.6e-12, bars hold.
LANE: hard input 2 — thirteenth packet of the arc; the class-charge
        layer of the product-profile emission program (#842 transfer
        certificate -> #858 sign dichotomy -> THIS: class arithmetic).
        Fence (N1) respected: nothing here pays or claims lower reserve.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** /
**COMPUTED-GRID/CONDITIONAL** / **CONJECTURAL** / **EXPERIMENTAL** /
**AUDIT** / **COUNTEREXAMPLE**; COMPUTED marks exact deterministic
scans; "certified" always means a named gate of the shipped verifier.
Verifier: `experimental/scripts/verify_dense_shell_class_charges.py`
(stdlib only, deterministic; `RESULT: PASS (22/22)` in ~11s; `--deep`
certifies the coupled-curve q <= 47 / broad j <= 48 envelope-share
horizons in ~55s; `--tamper-selftest` catches `13/13`; gate P13
C6-PARITY and P14 ENV-BROAD are the audit #914 regression gates, P15
CERT-BIND attests the shipped certificate JSON against the note/script
bytes it certifies). AUDIT-REPAIRED 2026-07-18 per PR #914 (Codex-team
audit, COUNTEREXAMPLE verdict on the prior integration; not yet landed
in this tree as a separate audit note -- see agents-log.md here for
the repair record).
Lean skeleton: `experimental/lean/dense_shell_class_charges/`
(stdlib-only, builds, no sorry: the support-class partition census, the
T_9(x)-1 factorization whose cubic Vieta is the ATOM's endpoint
identity, and the index-flip involution).

## 1. Setting

Level-B chart, c = 3^B. Dense shell = the 2^B residues xi with all
balanced digits nonzero; hatf(xi) = the #842/#827 middle-coefficient
weight; #858: sign(hatf) = (-1)^B strictly on the shell. Inverse side
h(sigma) = (1/c) sum_{xi dense} hatf(xi) e(-xi sigma / c). For
U subseteq {0..B-1} the support class class(U) = {sigma : balanced
digits supported exactly on U}, |class(U)| = 2^{|U|}; the 3^B residues
partition into the 2^B support classes.

Scan machinery (#858 conventions): states u_k = (d_{k-1} + u_{k-1})/3,
u in [-1/2,1/2] folding to t = |u|; a(t) = sin^2(pi t); drift =
a - 1/2 = -cos(2 pi t)/2; children t_+ = (1+t)/3, t_- = (1-t)/3; the
i-indexed defining angles are the scan states in reverse (theta_i =
u_{B-i}) — the index flip below.

## 2. The kernel reduction (C1) and the dichotomy statement

Exact-support character sums factor: sum_{sigma in class(U)}
e(-xi sigma/c) = prod_{i in U} 2cos(2 pi xi 3^i / c). Hence

    class-sum(U) = (-4)^{|U|} (1/c) sum_{xi} hatf prod_{K}(a_k - 1/2),
    K = {B - i : i in U},

and since (-1)^B hatf = |hatf| > 0 (#858), the LAW
sign(class-sum(U)) = (-1)^{B - |U|} for every U is EQUIVALENT to the
drift-product positivity A_K = E_w[prod_{k in K}(a_k - 1/2)] > 0 for
every scan-position set K, weights |hatf| on the shell.

## 3. The master frame (proof layer)

Throughout: flipped coords b_i = (-1)^{deg-i} coeff_i; the cone is
{b >= 0 entrywise}; N_a acts by b'_i = w_{i-1}b_{i-1} + (a-1/2)b_i +
b_{i+1}/4 (w_0 = 1/2, w_i = 1/4); N_{a'} = N_a + (a'-a)I; N_a is
entrywise NONNEG iff a >= 1/2 (outer). MASTER is the inequality

    (M_j)  G_j(5/12 + eps/3) >= need(eps) G_j(1/4 - eps/3) entrywise,
           need(eps) = sin(2pi eps/3)/sin(pi/3 + 2pi eps/3),

for all eps in (0, 1/4), j >= 0; need increases to 1/2. The coupling
identity drift(t_out) need(eps) = |drift(t_in)| holds EXACTLY — need
is critical, not adjustable (tamper-pinned in the verifier).

### 3.1 The envelope invariants (differential form; L0-L4')

L0 (exact derivative recursion). With t_+ = (1+t)/3, t_- = (1-t)/3:
    DG_j(t) = (1/3)[Phi'_{j-1}(t_+) - Phi'_{j-1}(t_-)],
    Phi'(s) = N_{a(s)} DG_{j-1}(s) + a'(s) G_{j-1}(s),  DG_0 = 0,
a'(s) = pi sin(2pi s). (Phi(s) = (x - a(s))G(s) is even in s; the
d = -1 branch folds with chain factor -1/3; the flip turns the -a'
into +a' on b-entries.) Verifier P5 pins DG against exact finite
differences and the interpolated cascade.

L1 (zero top defect). top(G_j) = 2^{1-j}, t-independent: the top
coefficient obeys the offdiagonal-only recursion top_j =
2 (1/4) top_{j-1} (j >= 2), top_1 = 1. Hence DG top = 0 exactly: the
envelope is trivial at the top index; the active indices are low.

L2 (strict positivity). G_j(t)_i > 0 on t in [1/6, 1/2] (purity R1 +
the #858 b_0, b_1 bootstrap; interior floor certified). So
|DG_j(t)_i| <= L G_j(t)_i integrates with no zero-crossing to
    e^{-Lg} <= G_j(t')_i / G_j(t)_i <= e^{Lg},  g = |t' - t|.

L4 (one-step differential bound — the propagation). For t in
[1/6,1/2], writing G_pm = G_{j-1}(t_pm), V_pm = N_{a(t_pm)}G_pm,
s_-^+ = max(0, 1/2 - a(t_-)), and assuming the child envelopes with
constants L_pm:
    3|DG_j(t)_i| <= L_+ V_{+,i} + L_-(V_{-,i} + 2 s_-^+ G_{-,i})
                    + |a'(t_+)G_{+,i} - a'(t_-)G_{-,i}|.
(t_+ is always outer so N_{a(t_+)} is entrywise nonneg and absorbs
|DG_+| <= L_+ G_+ directly; the t_- branch pays the 2 s_-^+ buffer
when inner; the last term is the source.) Dividing by G_j(t)_i =
V_{+,i} + V_{-,i} and bounding shares (child-share S) and the source
(cross-child ratio) closes the family regionally (L4'): the invariant
set {E_diff, S, B} is closed under one recursion step; iterating the
closure map from the base cases, GIVEN the share and cross-child-
ratio inputs at their certified floors, yields the envelope for ALL
j at the loose caps {1.64, 2.02, 2.77, 3.24, 3.78} (after the L5
cancellation: 1.086 / 1.663 on the two pair supports) on the five
regions R1..R5 = [1/6,.22], [.22,.30], [.30,.38], [.38,.44],
[.44,.50]. This closure-map iteration is a hand derivation: no gate
in the shipped verifier implements or certifies it (audit #914), so
its output (1.086 / 1.663, and the 3.5 HYPOTHESIS caps generally) is
carried as an INPUT with an external producer (PR #905, C3) rather
than a claim this packet proves.

Sharp constants (what 3.2 consumes; every one a shipped gate): on the
MASTER-consumed COUPLED child curves (3.2 Step B: pair-1 s+r=4/9,
pair-2 r2+s2=8/9), gaps in [1/18, 1/9], levels q = j-1 in [5, 47]:
L <= 0.85 pair-1 (gate P7, --deep; measured sup 0.597), L <= 1.61
pair-2 (measured sup 1.230) — both well inside cap. This SUPERSEDES an
earlier broader (whole-support, arbitrary-pair) census that is FALSE
for pair-2 on its full stated domain: audit #914 found the entrywise
secant exponent reaches ~1.6101 at q = 3, x = 4/9, y = 1/2 (off both
coupled curves and below the q >= 5 the general step actually uses,
so out of MASTER's scope by construction — 3.5). That broader census
is kept as an informational, non-load-bearing exhibit (gate P14
ENV-BROAD, cap corrected to 1.62). Child-share G_j(t_in) >=
1.20 G_{j-1}(r) entrywise for 6 <= j <= 48 (gate P12, --deep; measured
min 1.215). No monotonicity in j is claimed or needed on the B <= 49
leg.

L5 (trace-derivative cancellation, PROVED — gate P5 certifies exactly
this identity, independent of the closure-map claim below).
Differentiating the three-branch trace a(t_+) + a(t/3) + a(t_-) = 3/2
gives
    a'(t_+) - a'(t_-) = -a'(t/3)   exactly  (gate P5),
so L4's source rewrites as a'_+(G_+ - G_-) - a'(t/3) G_- with
|G_+ - G_-|_i <= (e^D - 1) min(G_pm)_i envelope-small: the decoupled
regional closure fixed point (hand-derived, uncertified — see above)
drops from 1.95 to 1.086 on the pair-1 support (1.663 pair-2). The
all-j persistence of these two envelopes plus the child-share floor
is the named INV-TAIL input (3.5) — the sole external HYPOTHESIS of
the packet (distinct from the enclosure gaps within the certified
grid, which are a missing-rigor issue, not an extension hypothesis).

### 3.2 The MASTER theorem (base cases + the general step)

Base (M_1) — the ATOM (C2). G_1(t) = Tt_1 + (a(t/3) - 1/2)Tt_0 by
the trace identity, so b_1 = 1 >= need trivially and b_0-entries
reduce, after clearing sin(pi/3 + 2pi eps/3) > 0 and product-to-sum,
to H(phi) = sin(7pi/18)cos(phi) - sin(pi/18)cos(phi/2) >= 0 on
phi = 2pi(1+4eps)/9 in [2pi/9, 4pi/9]. On this range sin(phi/2) <
sin(phi), so H'(phi) <= -(sin(7pi/18) - (1/2)sin(pi/18))sin(phi) < 0:
H is strictly decreasing, and its endpoint value is
    H(4pi/9) = sin(pi/18)[sin(7pi/18) - sin(5pi/18)] = sin^2(pi/18)
(using cos(4pi/9) = sin(pi/18), cos(2pi/9) = sin(5pi/18), and
sin(7pi/18) - sin(5pi/18) = 2cos(pi/3)sin(pi/18) = sin(pi/18)). So
(M_1) holds with margin sin^2(pi/18) ~ 0.0301 — the tightest
inequality of the whole program, in closed form. (Lean shadow: the
cubic 8x^3 - 6x + 1 = 2T_3 + 1 inside T_9(x) - 1 =
(x-1)(2x+1)^2(8x^3-6x+1)^2 has Vieta root-sum 0 = this identity.)

Bases (M_2)..(M_5): Lipschitz-certified eps-grids (certified floors
0.174/0.125/0.0625/0.0312 > 0; verifier P9).

General step (j >= 6; uses NO (M_{j-1})). The four grandchildren:
t_out's children s = 7/36 - eps/9 (inner), s2 = 17/36 + eps/9;
t_in's children r = 1/4 + eps/9, r2 = 5/12 - eps/9 (both outer).
Exact identities: both pairs share the gap g = 1/18 + 2eps/9 in
(1/18, 1/9]; s + r = 4/9 and s2 + r2 = 8/9, so the diagonal shifts
are eps-free in g:
    D1 = a(r) - a(s)  = sin(4pi/9) sin(pi g) > 0   (pair-1 deficit),
    B2 = a(s2) - a(r2) = sin(pi/9)  sin(pi g) > 0   (pair-2 bonus).
With X = G_{j-1}(s), Y = G_{j-1}(r), X2 = G_{j-1}(s2), Y2 =
G_{j-1}(r2) (all >= 0 by purity at j-1) and N_{a(s)} = N_{a(r)} -
D1 I, N_{a(s2)} = N_{a(r2)} + B2 I:

    Delta := G_j(t_out) - need G_j(t_in)
           = N_{a(r)}(X - need Y) + N_{a(r2)}(X2 - need Y2)
             + B2 X2 - D1 X.

Step B (envelopes, directions tracked): X >= rho1 Y and X2 >= rho2 Y2
with rho1 = e^{-L1* g}, rho2 = e^{-L2* g} (H-E1/H-E2; rho1, rho2 >
need always); N_{a(r)}, N_{a(r2)} are entrywise nonneg (r, r2 outer),
and the two images recombine into exactly the children of t_in:
    N_{a(r)}(X - need Y) + N_{a(r2)}(X2 - need Y2)
        >= (rho_min - need) G_j(t_in),  rho_min = rho2.
Step C (the deficit): on indices 0..j-1, X <= Y/rho1 (the reverse
envelope) and G_j(t_in) >= GAMMA* Y (child-share H-S), so
    (rho_min - need) G_j(t_in) - D1 X
        >= [(rho_min - need) GAMMA* rho1 - D1] (Y/rho1) >= 0
by the single scalar inequality
    (KEY)  (e^{-L2* g} - need(eps)) GAMMA* e^{-L1* g}
                >= sin(4pi/9) sin(pi g),
instantiated at the gate-certified caps (L1*, L2*, GAMMA*) =
(0.85, 1.61, 1.20): every positive factor decreases and the deficit
increases in eps, so the LHS-RHS is strictly decreasing with
endpoint value 0.030 > 0 at eps -> 1/4 (gate P8, gate-certified with
no external hypothesis on the B <= 49 leg; the same inequality at the
HYPOTHESIS loose caps (1.086,
1.663, 1.20) has endpoint margin 0.015 — a CONDITIONAL check only,
carrying the beyond-49 leg IF those caps hold; producer PR #905, C3).
What remains is Delta_i >= B2 (X2)_i >= 0,
strict at i = 0, 1 (purity floors), and the top entry Delta_top =
2^{1-j}(1 - need) > 0 (L1's t-free top). So (M_j) holds, strict in
the low and top entries. QED (step).

Joint induction: (M_j) from {purity_{j-1}, envelopes, share} —
this section; purity_j from {(M_{j-1}), purity_{j-1}} — R1 in 3.3
(the master enters purity_j at the CHILD level j-1, so the joint
recursion is well-founded). The
downstream chain consumes (M_j) only non-strictly; all strictness is
purity-driven (b_0, b_1 bootstrap from G_0 = 1).

### 3.3 The reduction chain

Every step re-derived adversarially and verified numerically (gates
P10/P4; B <= 8):
    R1 master + purity_{j-1} => purity_j: for t = 1/4 + eps split
       N_in = P - sI; G_j(t) >= [drift(t_out) need - s] G(t_in)
       + P G(t_in) = P G(t_in) >= 0 since drift(t_out) need = s exactly.
    R2 => Phi-domination: Phi_out - need Phi_in =
       N_out(G_out - need G_in) + need (a_out - a_in) G_in, both
       nonneg; the second term is STRICT at coefficient 0 (feeds L2).
    R3 => A-purity: outer parent A = drift(t_out)(Phi_out - need
       Phi_in) >= 0 — the same need; inner parent trivial.
    R4 the exact tree identity (two (-1)^B flips cancel):
       A_k = 4^B sum_pi sum_i c_i b_i(g^pi_{k-1}) b_i(A_{B-k+1}(t_pi)),
       every prefix in the cone (including mid-pair and inner-ending
       prefixes — 2832 scanned at B <= 8, gate P10), so A_k > 0
       strictly via the i = 0
       term and the floors L1 (prefix b_0, b_1 > 0) and L2 (A-vector
       b_0, b_1 > 0, the R2 gap term).

### 3.4 General K

The decorated cascade G^S and the PROVED reduction to
    per-prefix charges T_pi(K) (Status C3b). The single-insertion
    binding-entry identity (top(A_j(t)) = 2^{-j}(1/2 - a(t/3)), so the
    decorated sibling min-ratio IS the atom curve) is proved and
    honestly single-insertion-scoped: for |S| >= 2 the top ratio is
    sum_d drift(t_d)(1/2 - a(t_d/3))-driven and crosses below need —
    the refutations above (both numerically pinned in the labs
    behind gate P11's census). Anchored sub-case k_1 = 1: dichotomy
    via b_0(G^S(0)) > 0 alone (gate P11: floor 0.15 over every S at
    B = 8, measured min 0.156).

### 3.5 Epistemic ledger of the proof layer

REPAIRED per audit #914 (2026-07-18): this ledger previously listed
"the loose-cap all-j envelope" as PROVED and framed INV-TAIL's support
as resting on that claim; neither was backed by a shipped gate. Both
are corrected below.

- PROVED in closed form: the ATOM (M_1) with margin sin^2(pi/18); all
  exact identities (coupling, D1/B2, gaps, tops, trace-derivative);
  L0, L1, the L4/L4' propagation MACHINERY (the recursive bound
  relating consecutive levels, as an if-then statement); (KEY)'s
  monotonicity (analytic argument in 3.2, not a grid observation) and
  closed-form endpoint value; the general step (M_j), j >= 6, GIVEN
  the sharp envelope + share constants; the chain R1-R4; the
  general-K reduction T_pi(K) > 0 for every prefix IMPLIES
  E_w[prod_K] > 0 (C3b, sufficient direction only).
- CERTIFIED (deterministic grids with slope slack, named gates —
  "certified" is exactly this, and is NOT a continuum enclosure): the
  MASTER-consumed COUPLED-CURVE envelope secants pair-1 <= 0.85 /
  pair-2 <= 1.61 at every level q = j-1 in [5, 47] (P7, --deep,
  measured sups 0.597 / 1.230); bases (M_2..M_5) (P9); the
  child-share floor 1.20 at 6 <= j <= 48 (P12, --deep). No
  monotonicity in j is claimed. The whole-support (non-coupled) census
  is COMPUTED and informational only (P14 ENV-BROAD): pair-1 holds
  even there (sup 0.789 <= 0.85) but pair-2 does NOT (sup ~1.6101 >
  the old false cap 1.61) — MASTER never consumes that broader claim,
  so this does not touch (M_j).
- HYPOTHESIS (audit #914 MUST item — was mislabeled PROVED): the
  loose all-j caps pair-1 <= 1.086, pair-2 <= 1.663 (after the L5
  cancellation), and a child-share floor, are asserted by the L4'
  closure-map argument in 3.1 but that argument is NOT implemented by
  any gate here. (KEY) at (1.086, 1.663, 1.20), margin 0.015, is
  therefore a CONDITIONAL check on these three numbers (P8), not a
  proof of them.
- (INV-TAIL, the single external hypothesis): "the three floors
  persist for every j >= 49: pair-1 secant <= 0.85, pair-2 <= 1.61 on
  the coupled curves, child-share >= 1.20." Producer: PR #905 (head
  0000964) proves all three (envelopes 1.086/1.663 and a 7/6
  child-share floor, tighter than needed since (KEY) at
  (1.086,1.663,7/6) is independently re-certified there with margin
  > 0.0057) via a positive two-state cone plus curvature bounds,
  MODULO #905's own finite 448-bit Arb continuum certificate. Audit
  #911 (head 8d47b40) independently re-derived the symbolic half and
  found it sound, but did NOT replay the Arb half (python-flint
  unavailable) — so INV-TAIL is OPEN from this packet's standpoint
  until that replay happens (by #911 or by integrating #905's own
  verifier gate) or until #905 lands and this packet's verifier reads
  its contract directly (3.5 Status note at the top of this file).
- OPEN (would raise C3 from COMPUTED-GRID/CONDITIONAL to THEOREM on
  the B <= 49 leg, independently of INV-TAIL): the three enclosure
  gaps audit #914 found in the shipped grids (citations are to the
  PRE-REPAIR verifier; the repair changed gate scope, not this
  underlying gap) — P7's interpolated cascade has no interpolation-
  remainder bound and no between-node continuum enclosure (was
  verifier :483-517, :610-649); P9's "Lipschitz-certified" bases use
  an OBSERVED discrete slope as a global Lipschitz bound, not a
  proven one (was :685-725); P12 samples 199 interior epsilon values
  and omits both limiting endpoints, with no cell enclosure (was
  :884-906). None of these are closed here; a genuine continuum
  certificate (interval arithmetic / Arb, as #905 uses for its own
  claims) is the natural route for all three.
- OPEN (C3b, audit #914 SHOULD item): the converse of the general-K
  reduction — global positivity E_w[prod_K] > 0 forcing every
  per-prefix T_pi(K) > 0 — is not claimed and not attempted; only the
  sufficient direction is used anywhere downstream.
- COMPUTED: the exhaustive law B <= 10 (G3); the leak table (G4);
  T_pi census B in {6, 8} (P11); the anchored-case floor (P11) and
  the cone-pure-S classes (labs); the parity-correct charge identity
  (C6), exhaustively over every U at every B <= 8 (P13).
- CONJECTURAL: T_pi(K) > 0 for all |K| >= 2 uniformly in B (the
  general-K dichotomy); no other conjecture is load-bearing.

## 4. The computed layers (C4, C5) and charge arithmetic (C6)

Law margins and the B = 10 leak table as in Status; the packet's
emission consequence (REPAIRED, audit #914 -- the old "Sigma_U + W_U
always" form is FALSE, gate P13 pins the fix): omega(class) = h_+ =
W_U + 1_{s_U=+1} |Sigma_U|, equivalently ALWAYS (M_U + Sigma_U) / 2
with M_U = sum_class |h|; on right-parity classes (s_U = +1), within
the sign law's scope (C3/C3b), this reads |Sigma_U| + W_U; the two
terms have different epistemic status (certified evaluable vs
computed), and consumers must carry them separately. Wrong-parity
classes (s_U = -1): omega = W_U (the leak alone) — the #820-style
overpay is bounded by the leak layer on dense shells at every depth.
Counterexample to the deleted always-form: B=4, U={0}, s_U=-1,
Sigma_U=-3.599182825207051, W_U=omega_U=0 (audit #914; gate P13).

## 5. The certified insertion DP (C7)

One backward function-valued pass (Chebyshev nodes in u, z-polynomial
payload, insertion factors at the flipped scan positions B - k + 1)
evaluates any subset charge; the D6 ellipse argument gains exactly one
2cosh factor per inserted level. Bars and instances in the verifier.

## 6. Nonclaims

- No claim off the dense shell; no uniform-in-B floor for the law
  margins (computed growth only).
- The leak table is COMPUTED at B = 10 (exact deterministic scan), not
  proved; no closed form claimed.
- The CLASS-SUM dichotomy and the POINTWISE purity layer are separate
  claims and must not be conflated: class-sum signs are (conjecturally)
  exact at every B; pointwise sign purity LEAKS from |U| >= 4 at
  B = 10 and is only asymptotic in B - |U|.
- Two false lemmas, explicitly NOT claimed (both numerically refuted):
  cone-purity of the decorated cascade G^S for |S| >= 2, and the
  decorated Master inequality. The load-bearing general-K statement is
  the per-prefix charge positivity T_pi(K) > 0 (C3b), nothing stronger.
- The binding-entry = atom identity of 3.4 is claimed for SINGLE
  insertions only.
- No monotonicity of the envelope constants in j is claimed (it is
  false at j = 4 -> 5); the B <= 49 leg never uses it.
- Of the #842-banked emission program, this packet delivers the class
  budget/charge layer only; the schedule and adequacy ports on
  product profiles remain the named next step.
- Nothing here touches lower reserve or the (N1) fence.
- No continuum enclosure is claimed anywhere in the proof layer (audit
  #914): every P7/P9/P12 bound is a finite-grid check with no
  interpolation-remainder or between-node/endpoint enclosure. C3 is
  labeled COMPUTED-GRID/CONDITIONAL, not THEOREM, exactly because of
  this (3.5).
- The general-K reduction (C3b) claims only that termwise T_pi(K) > 0
  is SUFFICIENT for E_w[prod_K] > 0; the converse is NOT claimed.
- The old universal charge identity "omega_U = Sigma_U + W_U always"
  and the old broad-domain P7 pair-2 cap 1.61 are explicitly NOT
  claimed (both were FALSE as shipped before this repair; audit #914,
  gates P13/P14).

## 7. Consumers and provenance

- #858 (sign dichotomy): supplies sign purity, prefix-cone machinery,
  and the D6 tail; this packet is its class-level sequel. CORRECTION
  to #858's consumers note: #858 stated that on dense shells
  "omega = h_+ is |h| ... classwide" and that the #820 sign-mixing
  overpay "cannot occur there" — that conflated class sums with
  pointwise values. The truth (this packet): CLASS-SUM budgets are
  one-signed (the law), but pointwise h leaks from |U| >= 4 at
  B = 10, so omega exceeds |Sigma_U| by exactly the leak mass W_U.
  The #820-style overpay is bounded by the leak layer, not absent.
- #842 (transfer certificate): the adjoint function-valued DP is
  upgraded here with insertion factors and certified bars — the
  u-register stays collapsed onto Chebyshev nodes, and each inserted
  level costs one extra 2cosh factor in the D6 bar.
- #827 (shell-mass law): its class |hatf|-mass identities pair with
  the leak layer for bookkeeping of the class |h|-mass (the M_U
  totals of section 4's identity).
- #818/#820/#824 (emission arithmetic, omega-soundness, adequacy):
  consume omega = W_U + 1_{s_U=+1}|Sigma_U| per class on dense shells
  (REPAIRED, audit #914: the old "Sigma_U + W_U" form is FALSE at
  s_U = -1, gate P13 pins the fix — see C6); the sign-mixing overpay
  IS the leak layer.
- #816 C4 (denominator argument): the strict-inequality backbone
  (1/4-avoidance) used throughout the trig atoms.
