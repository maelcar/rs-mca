# Cycle 5 Prompt: Restored W-F1-AA Slope-Image Packing

No internet. You are Claude Opus 4.8 running as a high-effort theorem worker for the RS-MCA / Proximity Prize project.

Work only from mounted project files. Read:

1. `input_project/ACTIVE_WALLS.md`
2. `input_project/BANKED_LEMMAS.md`
3. `input_project/CUTS_AND_FALSE_ROUTES.md`
4. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE4_BALANCE_NOTATION_ROUTE_CUT_AUDIT.md`
5. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE2_PAIRED_BASE_READOUT_RETRY_AUDIT.md`
6. `input_project/upstream_main_20260618/tex/slackMCA_v3.tex`, especially `def:residue`, `prob:perfiber`, `conj:B`, and the monomial/prefix rigidity statements around `thm:rigidcyclo` if needed.
7. `input_project/upstream_main_20260618/tex/proximity_blueprint_v3.tex`, only as needed for `prob:F1` and the notation `a`, `sigma`.

Current banked facts:

- Source notation: `a=ceil((1-delta)n)`, `sigma=a-k`.
- Balanced means `t=sigma`, hence `k+t=a=s_delta`.
- In a nonzero-numerator residue-line datum, every support of size at least `a=k+t` is automatically noncontained.
- Quadratic arbitrary anchors reduce to the paired base readout

```text
rho(S)=(interp_S(w0) mod Ehat, interp_S(w1) mod Ehat),
Ehat=lcm(E,E^tau) in B[X].
```

Cut facts:

- Do not use `W-F1-AA-AGR` as a balanced wall.
- Do not add a high-agreement condition in the balanced case; `|S|=a=s_delta`.
- Do not use raw uniform fiber bounds over arbitrary anchors.

Target:

Attack restored `W-F1-AA`:

For quadratic `B=F_p`, `F=F_{p^2}`, `D subset B`, balanced `t=sigma`, `a=k+t=s_delta`, nonzero numerator `Bnum`, and arbitrary `w=w0+alpha*w1`, bound the number of distinct scalar slopes `z in F` for which some `a`-subset `S subset D` satisfies

```text
[interp_S(w)]_E = z [Bnum]_E,
```

equivalently `rho(S)` lands on the bad line `F*[Bnum]_E`, after tangent/zero-numerator and quotient-periodic contributions are separated.

Pick exactly one classification:

1. `BANKABLE_LEMMA`: prove a nontrivial slope-image/bad-locus packing lemma, or reduce it to a smaller named source-valid combinatorial object.
2. `COUNTERPACKET`: produce explicit finite or symbolic data showing too many distinct balanced slopes after tangent/zero-numerator and quotient-periodic cases are separated.
3. `ROUTE_CUT`: show the restored `W-F1-AA` wall is not source-valid; identify the false step.
4. `EXACT_NEW_WALL`: isolate the first missing invariant sharper than "paired-readout slope-image packing."

Mandatory focus:

- Work in the balanced regime only: `a=s_delta`.
- Noncontainment is automatic for `Bnum != 0`; do not spend the answer on it unless you find a flaw.
- The object is a slope image, not a support fiber.
- Keep `q_gen`, `q_line`, `q_chal`, `B`, and `F` separate.
- Do not claim `ass:extension-mca-lift`, protocol denominator savings, list decoding, or line decoding.

Output format:

```text
Final classification: <BANKABLE_LEMMA / COUNTERPACKET / ROUTE_CUT / EXACT_NEW_WALL>

Object:
<exact theorem/counterpacket/wall name>

Short verdict:
<one paragraph>

Proof / counterpacket / wall:
<source-valid argument with parameters>

Field and status audit:
<q_gen/q_line/q_chal/B/F and what is or is not proved>

What to bank:
<one short paragraph>
```

Hard limit: keep the final answer under 6000 words. Do not survey the whole repo.
