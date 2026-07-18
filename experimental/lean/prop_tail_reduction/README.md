# prop_tail_reduction

Statement-level Lean layer for the (PROP-TAIL) discharge (stdlib-only, no
mathlib, no `sorry`): kernel-checks the claim's exact/finite arithmetic core
via `decide` on `Int`/`Nat`/`List` data — the polynomial identity behind
`theta~(t) <= 1/5`, its sign-corollary inequality, the window constant
`289/256 <= 57/50`, two rational-data tables (the deep-grid
`rho_prop@i<17(j)` gate and the `V_17` vs. `tau*` crossover at `n=62`),
the SIB-CERT deep-anchor threshold comparison (`sibcert_clears`), the
LAM-INV proved-interval containments (`lamInv_*_inside`, widened-floor
consistency), and — round 4 — the (C'-CAP) discharge comparison
(`cprime_bound_clears`: certified node-census bound `<= 3/500`, cleared
form) plus the FLOOR-DRIFT transcriptions (`floordrift_step_ge_one`,
`floordrift_margins_ge_one`, and the Section 9(v) route-cut negative
`floordrift_routecut_misses`).

Transcription caveat: the tables and the round-4 literals transcribe
COMPUTED/certified values (printed decimals) to exact rationals at printed
precision, in the conservative direction (upper bounds up, lower bounds
down). The kernel checks the resulting rational comparisons — not the
correctness of the floating/exact-Fraction computation that produced the
decimals (the verifier's own exact-Fraction comparisons are the primary
certificate; these are the transcribed-statement shadow).

Out of scope, kept informal (all analytic content): the trig reduction
`theta~(t) = sqrt3 sin(2 pi t/3)/(6+3 cos(2 pi t/3))` and the substitution
`x = cos(2 pi t/3)`; the squaring step; `tau* = 3*log(1.02560749...)`
(transcendental); all contraction-rate / Birkhoff / CLT arguments.

Predecessor package (same conventions): `experimental/lean/inv_tail_closure/`.
Note: `experimental/notes/thresholds/dense_shell_inv_tail_closure.md` S7.
Verifier: `experimental/scripts/verify_dense_shell_inv_tail_closure.py`, V13.
