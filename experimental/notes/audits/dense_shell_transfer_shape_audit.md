# Audit of PR #905 (uniform dense-shell transfer shape TS1/TS2/TS3)

- **Status:** AUDIT. The non-Arb (symbolic) half holds at CLAIMS LEVEL:
  invariant-cone induction closed, curvature bounds cover the whole
  interval, and every scalar gate was re-derived independently. Soundness
  now hinges SOLELY on the packet's finite 448-bit Arb certificate (NOT
  replayed here -- python-flint absent). Independence from (PROP-TAIL) is
  clean; the amendments to the integrated class-charges packet weaken
  nothing. One packaging defect (stale `SHA256SUMS.txt`), no soundness
  defect found.
- **Agent/model:** Claude (Fable 5 orchestrator + Opus 4.8 subagent
  auditor), branch `exp-audit-transfer-shape`. Independent review; no edits
  to `pr-905`.
- **Date:** 2026-07-18.
- **Subject:** PR #905 (`avdeevvadim`, head `0000964`):
  `experimental/notes/thresholds/dense_shell_transfer_shape.md` (proof
  note, 539 lines); `experimental/scripts/`
  `verify_dense_shell_transfer_shape_arb.py` (Arb verifier, skimmed) and
  `replay_dense_shell_transfer_shape.py` (wrapper);
  `experimental/data/certificates/dense-shell-transfer-shape/*` (cert +
  `consumer_contract.json`). AMENDS the integrated dense-shell
  class-charges packet (holmbuar #880, upstream `a575019`):
  `dense_shell_class_charges.md`, its cert JSON, and
  `verify_dense_shell_class_charges.py`.
- **Companion verifier:**
  `experimental/scripts/verify_dense_shell_transfer_shape_audit.py`
  (self-contained, stdlib only; reads no repo file; runs green without
  `pr-905` checked out).
- **Relay:** the live findings were relayed on PR #905 on 2026-07-18
  08:23Z. PR-comment threads do not survive maintainer triage; this
  integrated packet is their durable record.

## What PR #905 claims

```text
Positive invariant cone + two-state shape induction + Riccati curvature
   ==(sec.2-sec.5)==>  the all-depth transfer envelopes and child-share floor
      TS1  e^{-1.086 g} B_{j-1}(r)  <= B_{j-1}(s)  <= e^{1.086 g} B_{j-1}(r)
      TS2  e^{-1.663 g} B_{j-1}(r2) <= B_{j-1}(s2) <= e^{1.663 g} B_{j-1}(r2)
      TS3  B_j(t_in) >= (7/6) B_{j-1}(r)              (every j >= 6)
   ==(sec.6, eq 25)==>  H(5/18) < 1.086,  H(1/2) < 1.663
   ==(sec.8, eq 31)==>  (KEY) at loose caps (1.086, 1.663, 7/6) stays > 0.00574
   ==>  INV-TAIL discharged; the |K| <= 1 dense-shell class-sign master is
        UNCONDITIONAL at every depth B (a second route, independent of the
        (PROP-TAIL) reduction).
B_n = tilde G_n (flipped shifted-Chebyshev); H(t) = mu tan(mu t);
lambda = 241/500; C = 1289/500; mu = sqrt(C).
```

Finite Arb certificate covers `5 <= n <= 26` directly plus the two-state
shape base at level 25 and the differential/curvature cone base at 26; the
symbolic induction takes over for `n >= 26`. Explicitly NOT claimed:
`T_pi(K) > 0` for `|K| >= 2`, product-profile admission, hard input 2, or
any lower-reserve payment.

## Method

Read the proof note in full. Diffed both amended class-charges files against
`upstream/main` and confirmed against the integrated #880 master reduction
(sec.3.2) what TS1/TS2/TS3 must supply. Re-derived, from the note's own
definitions, the five scalar gates and the two master-composition
inequalities in a small outward-rounded interval arithmetic (companion
verifier): single-point gates (eq 25, and the eq 27 binding endpoint) are
rigorous; interval gates (eq 20/24/27/31) are fine-grid corroborations of
the Arb continuum gate. Ran the pr-905 stdlib consumer verifier
`verify_dense_shell_class_charges.py --deep` from a scratch tree ->
`RESULT: PASS (19/19)`. Measured all 10 committed blob hashes against the
packet manifest. The 448-bit Arb certificate (python-flint 0.9.0) and its
tamper suite were structure-skimmed only, NOT replayed.

## Per-question verdicts

- **Q1 statement fidelity -- PASS.** Objects match what #880's master
  consumes: `B_n = tilde G_n` in the same convention; pair-1 support
  `[1/6, 5/18]`, pair-2 `[7/18, 1/2]`, shared gap `g = 1/18 + 2 eps/9 =
  r - s = s2 - r2` (verified exactly); preorder is componentwise; depth
  `j >= 6` matches the master step. Provenance is clean, not numerology:
  `class_charges.md` L178-198 states that 1.086/1.663 are the L4/L5
  loose-cap fixed points, and #905's Riccati gate re-certifies exactly
  those two constants by proving the true envelope `H(5/18) = 0.7677`,
  `H(1/2) = 1.6625` sits below them. One real change: the child-share the
  tail leg feeds (KEY) drops from #880's `1.20` to `7/6 ~ 1.1667` -- the
  conservative direction (KEY's LHS increases in the share factor), so it
  is safe.
- **Q2 cone invariance (sec.2-3) -- closed.** Inner/outer child
  classification is exhaustive and correct (inner `t` -> both children
  outer; outer `t` -> `p` outer, `m in [1/6,1/4]` inner). The shape
  induction propagates because `N_t` (outer) and `C_t = N_t N_m` are
  entrywise-nonnegative polynomials in `K` commuting with `A = K - lambda
  I`; every case (eq 4-5, 9-10) lands back in the cone. The terse sign
  claims are all independently true: `P >= Q >= 0`; `PQ <= 1/8` (max
  `= 1/8` at `delta = 1/12`); "smallest diagonal of `K^2` is `1/8`"
  (`K` has zero diagonal, so `C_t` diagonal `= (K^2)_{ii} - PQ >= 0`, `= 0`
  only at the `i=0, delta=1/12` corner -- still `>= 0`); `c_m >= 0.232 >
  0`.
- **Q3 curvature (sec.4-5) -- covers the whole interval, no degeneracy.**
  `H(t) = mu tan(mu t)` is finite on `[0,1/2]` since `mu/2 = 0.8028 <
  pi/2` (no `tan` blow-up); `cos(mu p) > 0` on `p in [5/12,1/2]` and `c_m
  >= 0.232` so `chi = lambda/c_m` is well-defined (no division by zero).
  Lower gate (eq 20) min `= 5.1429 > 5.14`; upper gate (eq 24) holds with
  large room (finding N1). Both need only positivity, which is robust.
- **Q4 closing arithmetic (sec.6) -- verified.** `H(5/18) = 0.76770 <
  1.086` (slack 0.318); `H(1/2) = 1.662517 < 1.663` (slack **4.8e-4** --
  see the tightness note below); TS3 min child-share `= 1.26175` at
  `eps = 0`, `>= 7/6` with 0.0951 slack ("substantial slack" is accurate);
  eq (27) as written (`> 7/6 + 0.095`) holds by only **8.4e-5** (N2).
- **Q5 seam -- gap-free.** Finite Arb cert covers TS1-TS3 directly for
  `n in [5,26]` plus shape base 25 / curvature base 26; induction
  propagates `n >= 26`; overlap at 26. In TS indices (`B_{j-1}`, `j >= 6`
  => `j-1 >= 5`): `[5,26] union [26, inf) = [5, inf)`. Indexing consistent
  (`j = n+1` in eq 26, `B_{j-1}(r) = B_n(r)`).
- **Q6 circularity -- independence is clean.** Grep of the note and the
  Arb verifier finds no `PROP-TAIL`, `rho_prop`, `#885`, or `#900` token
  or output. #905 is built only from the cascade recurrence (eq 1), the
  Jacobi operator, the Riccati comparison, and its own Arb cert. It is a
  genuine second, independent route to |K| <= 1.
- **Q7 amendment safety -- no weakening.** See the findings block; every
  semantic change is a strengthening (conditional -> unconditional) or a
  safe conservative substitution. The sharp gate P8 margin (0.03026) is
  preserved in the cert; the finite leg `j <= 48` is still independently
  checked by P7/P12 at 1.20.
- **Q8 sec.8 master consequence -- direction/composition correct.** eq
  (31) `(e^{-1.663 g} - need(eps)) (7/6) e^{-1.086 g} - sin(4pi/9)
  sin(pi g) > 0.00574` matches #880's (KEY) shape exactly: pair-2 (1.663)
  inside the `(. - need)` factor, pair-1 (1.086) as the standalone
  exponential (`min(rho1, rho2) = rho2` since `1.663 > 1.086`), `D1 =
  sin(4pi/9) sin(pi g)` the pair-1 deficit. Confirmed by the pr-905 stdlib
  verifier: `minF_loose = 0.0057` (cert `loose_min_margin =
  0.005748519865`).

## The pair-2 constant is spent (tightness of eq 25)

`H(1/2) = 1.662517` and the loose cap is `1.663`: the gap is **4.8e-4**.
That is, `1.663` -- the L5 regional-closure fixed point that #880's master
already consumes -- sits within `4.8e-4` of the TRUE Riccati envelope at
`t = 1/2`. Robust to double precision (interval width ~6e-15) and to the
(30) parameter box (`C = 2.57801` gives `H(1/2) = 1.662526 < 1.663`, slack
4.7e-4). Consequence for the program: the pair-2 envelope constant is
essentially SATURATED -- there is no meaningful headroom to tighten `1.663`
via this cone. Any future increase in the master (KEY) margin must come
from the pair-1 side (`H(5/18) = 0.7677` vs `1.086`, slack **0.318**) or
from `need(eps)`, not from pair-2.

## Findings

- **N1 (NOTE)** -- `dense_shell_transfer_shape.md` sec.5, eq (24): the
  stated floors `D_m > 0.0224`, `D_p + D_m > 0.0282` are correct but wildly
  loose. Independently, the actual minima are `D_m ~ 5.66` and `D_p + D_m ~
  3.45` (companion verifier, grid n=2000). Only positivity is needed and it
  holds with huge room; the reported numbers appear stale/mis-transcribed.
  Not soundness-affecting.
- **N2 (NOTE)** -- sec.6, eq (27): the "`+ 0.095`" formulation holds by
  only `8.4e-5`. TS3 itself (`share >= 7/6`) is fine (0.095 slack); the
  `+0.095` is a barely-valid stated lower bound on that slack. Cosmetic.
- **N3 (NOTE)** -- sec.6, eq (25): `H(1/2) < 1.663` is the single tight
  inequality of the whole packet (margin 4.8e-4, the pair-2 constant). It
  holds; the Arb cert at 448 bits is rigorous and double precision
  corroborates including across the (30) box. See the tightness note.
- **N4 (NOTE)** -- `replay_dense_shell_transfer_shape.py` is a thin
  wrapper that shells to the flint verifier, so it is not runnable in a
  stdlib environment. The stdlib half was exercised: pr-905
  `verify_dense_shell_class_charges.py --deep` -> `RESULT: PASS (19/19)`,
  `P8 (1.086, 1.663, 7/6): minF=0.0303 Fend=0.0303 minF_loose=0.0057`.
- **S1 (SHOULD)** --
  `dense-shell-transfer-shape/SHA256SUMS.txt` is stale for **all 10**
  entries: every committed blob mismatches its manifest hash (measured
  2026-07-18; e.g. `consumer_contract.json` blob `a0cfa97b..` vs manifest
  `3a3f1558..`; not a newline artifact -- tested). Consequence: the
  packet's advertised one-command replay (`replay_...py` ->
  `replay_hashes()`, and README "checks artifact hashes") would raise
  `SystemExit("artifact hash mismatch")` BEFORE python-flint is reached.
  Reproducibility only; no math impact. Cross-check: the class-charges
  cert's own `transfer_shape_contract_sha256 = a0cfa97b..` DOES match the
  real file, so the consumer wiring is internally consistent -- only
  `SHA256SUMS.txt` is wrong. Fix: regenerate the manifest against the
  committed tree. Table in the companion verifier output.
- **Amendment diff (Q7), all safe.** (1) Status/sec.3.5: INV-TAIL
  "conditional" -> "discharged". (2) C3 scope "B <= 49 + conditional" ->
  "UNCONDITIONAL for every B", finite `j <= 48` still P7/P12-checked. (3)
  C3b `|K| <= 1`: "unconditional B <= 49" -> "unconditional every B". (4)
  sec.3.2 loose-leg instantiation `(1.086,1.663,1.20) margin 0.015` ->
  `(1.086,1.663,7/6) margin > 0.0057`, now sourced from
  `consumer_contract.json` (P8 reads it). (5) CONJECTURAL narrowed from
  "all K" to "all `|K| >= 2`". (6) cert JSON: `key_endpoint_margin` ->
  `key_margins{sharp 0.03026 preserved, loose_min 0.005749, floor 0.0057}`
  + contract SHA; other cert deltas are <= 1-ulp float noise. No downstream
  consumer of a child-share > 7/6 exists (the master only needs KEY > 0),
  so the `1.20 -> 7/6` drop is safe.

## Verdict

The non-Arb (symbolic) half of PR #905 holds at claims level. The
invariant-cone induction (sec.3) is closed on every case; the
derivative/curvature bounds (sec.4-5) cover the full `[0,1/2]` with no
degeneracy; and the closing arithmetic (sec.6, eq 25/27) and the
master-composition (sec.8, eq 31) are correct -- every scalar gate
(20/24/25/27/31) was re-derived independently in interval arithmetic, so
the symbolic layer no longer rests solely on the Arb cert. Soundness now
hinges on exactly two things: (i) the finite Arb continuum certificate --
the two-state shape base at level 25, the differential/curvature cone base
at 26, TS1-TS3 for `5 <= n <= 26`, the sec.7 complex-domain error
propagation, and the (30) parameter-box run -- none replayable without
python-flint == 0.9.0; and (ii) nothing else, no soundness defect was found
in the symbolic half. The tight spots (`H(1/2)` margin 4.8e-4; master
margin 0.0057; eq-27 `+0.095` margin 8.4e-5) all hold and are Arb-rigorous.
The independence-from-(PROP-TAIL) claim is clean, and the amendment to the
integrated #880 files weakens nothing it or other packets consume. The only
actionable defect is S1 (stale `SHA256SUMS.txt`) -- it breaks the
advertised replay but not the mathematics.

Credit to `avdeevvadim`: the construction -- an invariant positive cone
closed under the two-state shape recursion, plus lower/upper Riccati
curvature bounds converting the cone into the exact envelope constants -- is
a clean, provenance-honest second derivation of the transfer envelopes and
child-share floor, discharging INV-TAIL by a route that shares no input
with the (PROP-TAIL)/INV-TAIL packets (#885/#900).
