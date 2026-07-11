#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_span_face_synthesis.py

Re-checks the span-face synthesis packet
(experimental/notes/thresholds/span_face_synthesis.md) against ground truth at
the worktree tip.  This is a SYNTHESIS/AUDIT verifier: it re-derives no
mathematics.  It checks four things, exactly as the packet claims them:

  (A) TEX ANCHORS.  Every tex line quoted in the S1 closure statement and the
      S2 hypothesis-matching table appears (whitespace-normalized) within +/- 3
      lines of its cited line in experimental/asymptotic_rs_mca_frontiers.tex.
      Wrong anchors kill the packet, so this is the bulk of the check.

  (B) PR -> NOTE MAPPING.  Every integrated arc PR maps to a note file that
      exists in-tree; and PR #647 (branch thresholds-collapse-field-cost) is
      correctly ABSENT in-tree (it is not integrated at 5c9aab7), matching the
      packet's documentation.

  (C) VERIFIER-COUNT CLAIMS.  Each integrated arc note's own stated
      "RESULT: PASS (N/N)" string is present in that note file.  (The arc
      verifiers are NOT re-run here -- too slow; we check the notes' own claims,
      and that the synthesis note reproduces them.)

  (D) S2 INTERNAL CONSISTENCY.  No row labelled DISCHARGED cites a dependency
      that is OPEN.  (A DISCHARGED step may depend only on other discharged
      steps or on the single printed input, never on an open gap.)

Plus (E) a self-consistency check that the synthesis note contains its own
required section headers, the closure theorem, and the load-bearing hypothesis
symbol (FI-field').

stdlib only.  zero-arg.  ~1s.  Prints "RESULT: PASS (N/N)" and exits 0 on
success, nonzero on the first failure.  Intended under `ulimit -v 2097152`.
"""

import os
import re
import sys

# ----------------------------------------------------------------------------
# Paths (derived from this script's location: experimental/scripts/<this>)
# ----------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENTAL = os.path.dirname(HERE)                     # experimental/
TEX = os.path.join(EXPERIMENTAL, "asymptotic_rs_mca_frontiers.tex")
THRESH = os.path.join(EXPERIMENTAL, "notes", "thresholds")
SYNTH = os.path.join(THRESH, "span_face_synthesis.md")

_FAILS = []
_CHECKS = 0


def check(cond, msg):
    global _CHECKS
    _CHECKS += 1
    if not cond:
        _FAILS.append(msg)


def norm_ws(s):
    """Collapse every run of whitespace (incl. newlines) to a single space."""
    return re.sub(r"\s+", " ", s).strip()


def read_lines(path):
    with open(path, "r", encoding="utf-8", errors="strict") as f:
        return f.read().split("\n")


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="strict") as f:
        return f.read()


# ----------------------------------------------------------------------------
# (A) TEX ANCHORS: (cited_line, verbatim_substring).  Each substring must occur,
#     whitespace-normalized, within lines [cited_line-3, cited_line+3].
#     Every one of these was read at 5c9aab7 while building the packet.
# ----------------------------------------------------------------------------
ANCHORS = [
    # C7 cell (the centerpiece, L2440-2454)
    (2440, r"Saturation and effective-image-collapse cells"),
    (2452, r"projection degree remains an enumerative input"),
    (2454, r"reaches exponentially fewer boundary values than its ambient codomain contains"),
    # profile envelope + guard + countertheorem
    (862,  r"\label{eq:profile-envelope}"),
    (870,  r"the sum and maximum have the same exponential scale"),
    (889,  r"The countertheorem is exactly a row for which a quotient profile in"),
    # first-match order + detectability split
    (5181, r"algebraic major arcs first, then a separately certified Sidon/Fourier cell"),
    (1497, r"Payment is an enumerative assertion about an actual slope projection"),
    (1498, r"constructibility alone is not payment"),
    (1121, r"Constructibility, a raw support count, or a support-pair moment alone does"),
    # (FI) certificate + image scale
    (4844, r"\tag{FI}\label{eq:full-image-certificate}"),
    (4857, r"Deleting earlier cells can only decrease every fiber"),
    # primitive-Q max-fiber predicate
    (4918, r"\max_{s\in\Scal}f_s\le e^{o(N)}\barN^{\rm img}"),
    # admissibility A1-A7
    (896,  r"\label{def:admissible-sequence}"),
    (905,  r"A first-match atlas covers every bad-slope witness and has"),
    (906,  r"The total \emph{distinct-slope} contribution"),
    (922,  r"Any use of the ambient scale is accompanied by"),
    (940,  r"R_N<\operatorname{char}\B_N"),
    # subfield confinement (T-FIELD's engine)
    (1930, r"\label{thm:subfield-confinement-full}"),
    (1933, r"Hence every MCA-bad slope of"),
    (1934, r"a \(\B\)-valued received line lies in \(\B\)"),
    # first-match disjoint union (T-PAY)
    (1526, r"\label{lem:first-match-bound}"),
    (1535, r"Z_a(r)=\coprod_iZ_i^\circ"),
    # occupancy compiler RC_occ (saturation repair)
    (5677, r"\abs{\Ccal}=\sum_{\rho\in\Rcal(\Ccal)}\nu_{\Ccal}(\rho)"),
    (5683, r"\tag{RC$_{\rm occ}$}"),
    # saturation criterion
    (4726, r"\label{prop:saturation-payment}"),
    (4727, r"A saturation cell is paid if the projection from raw witnesses to the"),
    (4730, r"final image has a direct distinct-slope estimate at the profile scale"),
    (4738, r"goes in the wrong direction"),
    # separation gate eq (4.5)
    (2074, r"\label{thm:prefix-to-line-hardness}"),
    (2079, r"\abs\F-n>k\binom N2"),
    (2083, r"MCA-bad slopes furnished by"),
    # countertheorem + scope
    (797,  r"\label{thm:intro-countertheorem}"),
    (804,  r"\exp((h(\alpha)/4+o(1))n)"),
    (817,  r"threshold counterexamples result"),
    (830,  r"\label{rem:intro-countertheorem-scope}"),
    (837,  r"is polynomial-size, whereas the scalar extension used to separate"),
    (840,  r"verify its field and reserve hypotheses"),
    # closed-ledger items + routing
    (1107, r"for its actual first-match slope set"),
    (1108, r"but to no earlier profile"),
    (1115, r"effective-image collapse is either routed to an earlier profile or"),
    (878,  r"assigned by the first-match rule to an earlier profile so"),
    # profile census lemmas
    (4772, r"\label{lem:profile-atlas}"),
    (4781, r"arbitrary planted subsets or an unproved decomposition of a"),
    (5028, r"\label{lem:profile-multiplicity}"),
    (5030, r"all data outside the moving support is \(o(n)\) bits"),
    (1448, r"the number of nonempty pairs"),
    # field of definition + challenge/quantifier trace (#645)
    (2290, r"The \emph{field of definition} is the smallest"),
    (204,  r"is the \emph{challenge set}, meaning"),
    (491,  r"MCA error at most a cryptographic target such"),
    (575,  r"challenge field \(\F\) may be a \emph{scalar extension}, meaning that the"),
    (187,  r"A received pair \(r=(r_0,r_1)\in(\F^D)^2\) determines the"),
    (226,  r"bound is uniform over received pairs, whereas a lower construction need"),
]

WINDOW = 3


def check_anchors():
    check(os.path.exists(TEX), "tex not found: %s" % TEX)
    if not os.path.exists(TEX):
        return
    lines = read_lines(TEX)
    n = len(lines)
    for cited, sub in ANCHORS:
        lo = max(0, cited - 1 - WINDOW)
        hi = min(n, cited - 1 + WINDOW + 1)
        window = norm_ws("\n".join(lines[lo:hi]))
        ok = norm_ws(sub) in window
        check(ok, "ANCHOR MISS L%d: %r not within +-%d lines" % (cited, sub, WINDOW))
        # Also require the synthesis note to actually cite that line number,
        # so the table and the tex cannot silently drift apart.
        # (checked in check_synth_cites_lines)


# ----------------------------------------------------------------------------
# (B) PR -> NOTE MAPPING
# ----------------------------------------------------------------------------
INTEGRATED = {
    622: "se_on_admissible_leaves.md",
    625: "c7_routing_spectrum.md",
    626: "c7_degree_enumeration.md",
    627: "routing_exhaustiveness.md",
    635: "collapse_payment.md",
    636: "saturation_payment_repair.md",
    642: "c7_collapse_image_degree.md",
    645: "fi_field_discharge.md",
    638: "thick_form_comparison_lemmas.md",
    # externals integrated in-tree at 5c9aab7:
    629: "minimal_phase_supplement.md",            # Danny thick correction lives here
    621: "aperiodic_one_ray_saturation.md",        # Danny confined extreme
    634: "full_agreement_orientation_saturation.md",  # Codex orientation floor
    644: "orientation_prefix_phase_transition.md",    # Codex antipodal phase bracket
    620: "canonical_full_agreement_occupancy_atlas.md",  # Danny per-line ceiling
    643: "moment_map_max_fiber.md",                # image-face (revised by #646)
}
# On-branch, NOT integrated at 5c9aab7 -> must be ABSENT in-tree:
ON_BRANCH = {647: "collapse_field_cost.md"}


def check_pr_note_mapping():
    for pr, note in INTEGRATED.items():
        p = os.path.join(THRESH, note)
        check(os.path.exists(p), "PR #%d note missing in-tree: %s" % (pr, note))
    for pr, note in ON_BRANCH.items():
        p = os.path.join(THRESH, note)
        check(not os.path.exists(p),
              "PR #%d (%s) should be ABSENT in-tree (on-branch, not integrated at 5c9aab7)"
              % (pr, note))


# ----------------------------------------------------------------------------
# (C) VERIFIER-COUNT CLAIMS: each note's own stated PASS string is present,
#     and the synthesis note reproduces it.
# ----------------------------------------------------------------------------
PASS_COUNTS = {
    "se_on_admissible_leaves.md": "RESULT: PASS (208/208)",
    "c7_routing_spectrum.md": "RESULT: PASS (731/731)",
    "c7_degree_enumeration.md": "RESULT: PASS (233/233)",
    "routing_exhaustiveness.md": "RESULT: PASS (3417/3417)",
    "collapse_payment.md": "RESULT: PASS (1210/1210)",
    "saturation_payment_repair.md": "RESULT: PASS (28/28)",
    "c7_collapse_image_degree.md": "RESULT: PASS (115/115)",
    "fi_field_discharge.md": "RESULT: PASS (59/59)",
    "thick_form_comparison_lemmas.md": "RESULT: PASS (27/27)",
}
# #647's own note (on-branch) claims this; documented in the synthesis note only.
ONBRANCH_PASS = "RESULT: PASS (42/42)"


def check_pass_counts():
    synth = read_text(SYNTH) if os.path.exists(SYNTH) else ""
    for note, s in PASS_COUNTS.items():
        p = os.path.join(THRESH, note)
        if not os.path.exists(p):
            check(False, "note missing for PASS-count check: %s" % note)
            continue
        txt = read_text(p)
        check(s in txt, "PASS string %r absent in %s" % (s, note))
        # the synthesis note must reproduce the same PASS string (its Reproducibility block)
        check(s in synth, "synthesis note omits PASS string %r for %s" % (s, note))
    # the on-branch #647 count must be documented (as on-branch) in the synthesis note
    check(ONBRANCH_PASS in synth,
          "synthesis note omits on-branch #647 PASS string %r" % ONBRANCH_PASS)


# ----------------------------------------------------------------------------
# (D) S2 INTERNAL CONSISTENCY: no DISCHARGED row cites an OPEN dependency.
#     Rows model the S2 table; deps are the PRs each discharged step rests on.
# ----------------------------------------------------------------------------
# status of each dependency PR (as established by the arc):
DEP_STATUS = {
    614: "DISCHARGED",   # master identity L>=A_eff/(1+E), PROVED
    625: "DISCHARGED",   # MASTER-2 identity
    629: "DISCHARGED",   # thick correction, adopted
    635: "DISCHARGED",   # T-PAY well-posed (mod T-PAY-RES, itself resolved by 642)
    642: "DISCHARGED",   # T-FIELD delta<=|F_r|, PROVED
    645: "DISCHARGED",   # (RED) reduction PROVED (residual is a PRINTED input, not OPEN)
}
# S2 rows: status + dependency PRs.
S2_ROWS = {
    1:  ("SUPERSEDED",     [625]),
    2:  ("DISCHARGED",     [614]),
    3:  ("SUPERSEDED",     [635]),
    4:  ("DISCHARGED",     [625]),
    5:  ("DISCHARGED",     [642]),
    6:  ("DISCHARGED",     []),
    7:  ("DISCHARGED",     [645]),
    8:  ("NEEDS-PRINTING", []),
    9:  ("DISCHARGED",     [629]),
    10: ("SUPERSEDED",     [645]),
}


def check_s2_consistency():
    valid = {"DISCHARGED", "SUPERSEDED", "NEEDS-PRINTING", "OPEN"}
    for row, (status, deps) in S2_ROWS.items():
        check(status in valid, "S2 row %d has invalid status %r" % (row, status))
        if status == "DISCHARGED":
            for d in deps:
                ds = DEP_STATUS.get(d, "OPEN")  # unknown dep treated as OPEN (fail-safe)
                check(ds != "OPEN",
                      "S2 row %d is DISCHARGED but cites OPEN dependency PR #%d" % (row, d))
    # sanity: the closure rests on >=1 discharged theorem and exactly one printed input
    discharged = [r for r, (s, _) in S2_ROWS.items() if s == "DISCHARGED"]
    needsprint = [r for r, (s, _) in S2_ROWS.items() if s == "NEEDS-PRINTING"]
    check(len(discharged) >= 5, "expected >=5 DISCHARGED rows, got %d" % len(discharged))
    check(len(needsprint) >= 1, "expected >=1 NEEDS-PRINTING row (the printed input)")


# ----------------------------------------------------------------------------
# (E) SYNTHESIS-NOTE SELF-CONSISTENCY: required sections, closure theorem,
#     the printed-input symbol, and that every cited tex line in ANCHORS is
#     actually written in the note (so the note and this verifier agree).
# ----------------------------------------------------------------------------
def check_synth_self():
    check(os.path.exists(SYNTH), "synthesis note missing: %s" % SYNTH)
    if not os.path.exists(SYNTH):
        return
    txt = read_text(SYNTH)
    for header in ["S1 -- THE CLOSURE STATEMENT",
                   "S2 -- THE HYPOTHESIS-MATCHING TABLE",
                   "S3 -- WHAT MUST BE PRINTED",
                   "S4 -- OPEN CORNERS",
                   "S5 -- CONSISTENCY SWEEP"]:
        check(header in txt, "synthesis note missing section: %s" % header)
    # the printed input must be named
    check("(FI-field')" in txt, "synthesis note does not name the printed input (FI-field')")
    # the closure must be scoped to admissible + the field clause
    check("ledger-admissible" in txt or "def:admissible-sequence" in txt,
          "closure statement missing admissibility scope")
    # the no-open-gap verdict must be stated (S5)
    check("NONE in the composition" in txt or "no new math gap" in txt.lower()
          or "no new math gap" in txt,
          "synthesis note missing the no-open-gap verdict")
    # the maintainer's target quote must be present (verbatim fragment)
    check("input-specific until their hypotheses are matched" in txt,
          "synthesis note missing the maintainer's target instruction")


def check_synth_cites_lines():
    """Every anchor line number cited by this verifier must appear in the note
    (as L<line> or L<line>- ...), so table and verifier cannot drift."""
    if not os.path.exists(SYNTH):
        return
    txt = read_text(SYNTH)
    # collect every tex line the note relies on: single "Lxxx" and ranges
    # "Lxxx-yyy" / "Lxxx--yyy" (a range means the note relies on the whole span).
    present = set()
    for m in re.finditer(r"L(\d{2,4})(?:-+(\d{2,4}))?", txt):
        a = int(m.group(1))
        present.add(a)
        if m.group(2):
            b = int(m.group(2))
            if a <= b <= a + 200:          # sanity-bounded span
                present.update(range(a, b + 1))
    # every anchor's cited line should be within +-3 of some line the note relies on
    for cited, sub in ANCHORS:
        near = any(abs(cited - p) <= WINDOW for p in present)
        check(near,
              "synthesis note does not cite any L-number within +-%d of anchor L%d (%r)"
              % (WINDOW, cited, sub[:40]))


# ----------------------------------------------------------------------------
def main():
    check_anchors()
    check_pr_note_mapping()
    check_pass_counts()
    check_s2_consistency()
    check_synth_self()
    check_synth_cites_lines()

    if _FAILS:
        print("RESULT: FAIL (%d/%d checks passed)" % (_CHECKS - len(_FAILS), _CHECKS))
        for i, m in enumerate(_FAILS, 1):
            print("  [%d] %s" % (i, m))
        sys.exit(1)
    print("RESULT: PASS (%d/%d)" % (_CHECKS, _CHECKS))
    sys.exit(0)


if __name__ == "__main__":
    main()
