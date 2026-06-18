# Cycle 3 Prompt: Attack W-F1-AA Noncontainment And Slope-Image Packing

No internet. You are Claude Opus 4.8 running as a high-effort theorem worker for the RS-MCA / Proximity Prize project.

Work only from the mounted project files. Read the file index first, then read only:

1. `input_project/ACTIVE_WALLS.md`
2. `input_project/BANKED_LEMMAS.md`
3. `input_project/CUTS_AND_FALSE_ROUTES.md`
4. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE2_PAIRED_BASE_READOUT_RETRY_AUDIT.md`
5. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CODEX_LOCAL_PAIRED_BASE_READOUT_AUDIT.md`
6. `input_project/upstream_main_20260618/tex/slackMCA_v3.tex`, only `def:residue`, `thm:normalform`, `prob:perfiber`, `conj:B`.
7. `input_project/upstream_main_20260618/tex/proximity_blueprint_v3.tex`, only `prob:F1`.

Do not re-prove the Cycle 2 paired-readout factorization unless you find a flaw. It is banked as:

```text
rho(S)=(interp_S(w0) mod Ehat, interp_S(w1) mod Ehat),
Ehat=lcm(E,E^tau) in B[X].
```

Current exact wall `W-F1-AA`:

Bound the number of distinct scalar slopes `z in F` for which there exists an `a=k+t` subset `S` whose paired base readout lands on the fixed bad line

```text
F * [Bnum]_E in F[X]/(E)
```

and whose original witness remains noncontained after tangent/contained and quotient-periodic cases are separated.

Your task:

Pick exactly one outcome and justify it.

1. `BANKABLE_LEMMA`: prove a nontrivial slope-image packing lemma for `W-F1-AA`, with exact hypotheses. It may be conditional on a named, smaller source-valid combinatorial object if the reduction is strict and useful.
2. `COUNTERPACKET`: produce explicit finite or symbolic data showing too many distinct noncontained slopes for the paired base readout after tangent/contained cases are separated. You must verify noncontainment; raw large fibers do not count.
3. `ROUTE_CUT`: show the `W-F1-AA` formulation is not source-valid. Give the first false step and a counterexample.
4. `EXACT_NEW_WALL`: isolate the first missing invariant in the noncontainment or subset-shrinking step. This must be sharper than "prove slope-image packing".

Mandatory focus:

- The hard point is not raw fiber size. Low-degree anchors can make raw fibers huge.
- The hard point is whether a large support `S_z` with noncontainment can be replaced by an `a`-subset without losing the noncontained obstruction, or whether the slope-image count must remember larger supports.
- Decide whether noncontainment can be certified by a bounded-size sub-support. If yes, state and prove the certificate-size lemma. If no, give a counterexample or an exact new wall.
- Keep `q_gen`, `q_line`, `q_chal`, `B`, and `F` separate.
- Do not claim `ass:extension-mca-lift`, a protocol denominator saving, a list-decoding theorem, or a line-decoding theorem.

Output format:

```text
Final classification: <BANKABLE_LEMMA / COUNTERPACKET / ROUTE_CUT / EXACT_NEW_WALL>

Object:
<exact object name>

Short verdict:
<one paragraph>

Proof / counterpacket / wall:
<source-valid argument with parameters>

Noncontainment audit:
<exact statement about whether noncontainment survives shrinking or needs larger supports>

What to bank:
<one short paragraph>
```

Hard limit: keep the final answer under 6000 words. If you cannot prove or refute the wall, output a precise `EXACT_NEW_WALL` focused on the noncontainment invariant.
