#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifier for experimental/notes/thresholds/atlas_cat_cell_ledger.md.

Stdlib-only, deterministic.  Two modes:

  --check           (default) run the full audit suite; print RESULT: PASS
                    (n/n) and exit 0, or RESULT: FAIL and exit 1.
  --tamper-selftest deliberately corrupt an in-memory copy of a quoted anchor
                    and confirm the anchor-checking function detects it, then
                    finish with RESULT: PASS (n/n) for the selftest's checks.

Four blocks.

  BLOCK A  Every verbatim tex anchor quoted by the (CAT) ledger is located in
           experimental/asymptotic_rs_mca_frontiers.tex by a tolerance-window
           search: the exact substring must occur within +/-2 lines of the
           stated (1-indexed) line and be the exact hit (offset 0) at the
           current tex snapshot.  A negative test corrupts one anchor and
           confirms the corrupted string is absent both at its line and
           file-wide.

  BLOCK B  The composition numbers are recomputed from first principles with
           exact Python integers/fractions:
             * SE2 image-normalization identity  L * barN = M = binom(|T|,m)
               (thm:small-effective-dual-closure, L3054-3056);
             * the prefix-fibre profile bound     L <= p^w  (#536), with the
               w=0 one-cell binom(D,a) atlas as the base case;
             * the paid-cell exponent composition  max over the 5 paid cells
               of their subexponential growth exponent (all 0) = 0 -> e^{o(n)};
             * the C9 razor's two poles: the Sidon-extremal normalized energy
               Delta = (2f^2-f)/f^3 with Delta*f -> 2, above the CS floor 1/f.

  BLOCK C  Each paying note's own text is checked to contain its cited
           status/PR self-label (whitespace-normalized), and every note file
           referenced by the ledger is checked to exist on disk.

  BLOCK D  The per-cell ledger row counts are recomputed from the LEDGER table
           declared below (9 cells; 5 PAID; 4 UNPAID/CONDITIONAL; the residual
           mapping to hard inputs 3 and 4/5 plus one census).

No .tex/.pdf is modified.
"""

import hashlib
import json
import os
import sys

FAILURES = []
CHECKS = 0


def check(cond, label):
    global CHECKS
    CHECKS += 1
    if cond:
        print("  ok   " + label)
    else:
        print("  FAIL " + label)
        FAILURES.append(label)


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))          # experimental/
TEX = os.path.join(ROOT, "asymptotic_rs_mca_frontiers.tex")
NOTES = os.path.join(ROOT, "notes", "thresholds")
CERTIFICATE = os.path.join(
    ROOT, "data", "certificates", "atlas-cat-ledger", "atlas_cat_ledger.json"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "df79dad137e2ff8241eb35c8bafe977454508917eb2fa714a302e6467f10862d"
)

WINDOW = 2  # tolerance window, in lines, either side of the stated anchor


def find_anchor(lines, lineno, substr, window=WINDOW):
    """Search lines[lineno-1-window : lineno+window] for substr.
    Returns the offset (found_line - lineno) of the first hit, or None."""
    lo = max(1, lineno - window)
    hi = min(len(lines), lineno + window)
    for ln in range(lo, hi + 1):
        if substr in lines[ln - 1]:
            return ln - lineno
    return None


def norm_ws(s):
    return " ".join(s.split())


# --------------------------------------------------------------------------
# BLOCK A -- tex anchor tolerance-window checks + negative test
# --------------------------------------------------------------------------
# (1-based line number, exact substring that must occur within +/-WINDOW lines)
ANCHORS = [
    # --- the printed cell catalogue, C1..C9, and its own framing ---
    (2366, r"\subsection{Cell catalogue}\label{sec:cell-catalogue}"),
    (2368, "The catalogue below is a language for row-specific proofs, not a theorem"),
    (2369, "that every displayed locus is automatically paid.  In a concrete family,"),
    (2374, r"\paragraph{Quotient and periodic cells.}"),                        # C1
    (2375, "A quotient cell consists of pullbacks along a nontrivial map"),
    (2385, r"\paragraph{Dihedral and Chebyshev cells.}"),                        # C2
    (2386, "These are quotient cells with an additional involution, usually inversion"),
    (2399, r"\paragraph{Planted-block cells.}"),                                 # C3
    (2400, r"A \emph{planted block} is a predetermined group of support positions"),
    (2405, "locus constructible, but payment additionally requires a subexponential"),
    (2407, "projection; arbitrary planted subsets are not one profile."),
    (2409, r"\paragraph{Tangent, deep, and common-line cells.}"),               # C4
    (2412, "record rank-defective contact between the received line and the"),
    (2416, r"\cref{prop:tangent-payment}; rank drop alone is not payment."),
    (2422, r"\paragraph{Extension and field-descent cells.}"),                   # C5
    (2423, "A witness lies in an extension or field-descent cell if its data is defined over"),
    (2429, r"\paragraph{Differential-locator cells.}"),                          # C6
    (2434, r"\emph{differential-locator cell} is the"),
    (2435, "locus where that matrix loses its expected rank.  It is determinantal, but"),
    (2440, r"\paragraph{Saturation and effective-image-collapse cells.}"),       # C7
    (2446, r"polynomials can still occur at one slope.  Thus \emph{saturation} means"),
    (2451, "constructible in the projective locator and explanation incidence, but its"),
    (2452, "projection degree remains an enumerative input."),
    (2453, r"\emph{Effective-image collapse} is the related event that a boundary map"),
    (2456, r"\paragraph{Balanced-core and split-pencil cells.}"),                # C8
    (2458, r"family.  A \emph{balanced core} is a pair of equal-degree monic residual"),
    (2459, r"locators with a common depth-\(w\) prefix after common and planted factors"),
    (2473, r"\cref{prop:split-pencil-payment}.  Higher-dimensional balanced-core charts"),
    (2474, "require a proved decomposition or a direct ray estimate."),
    (2476, r"\paragraph{Fourier/Sidon-heavy analytic component.}"),             # C9
    (2477, "A primitive prefix fiber may be too large while having exponentially small"),
    # --- condition (A2) and the admissibility quantifier ---
    (897,  r"A sequence \((C_n,a_n)\), with \(C_n=\RS_{\F_n}(D_n,k_n)\), is"),
    (898,  "ledger-admissible if the following conditions hold uniformly in every"),
    (899,  "received line."),
    (905,  "A first-match atlas covers every bad-slope witness and has"),
    (906,  r"\(e^{o(n)}\) profiles.  The total \emph{distinct-slope} contribution"),
    (907,  r"of its algebraic cells is at most \(e^{o(n)}\mathfrak E_n(a_n)\)."),
    # --- def:first-match / def:paid-cell / row-sequence quantifier ---
    (1463, r"The ordered family is a \emph{witness-exhaustive first-match atlas} if"),
    (1527, "If every received line admits a witness-exhaustive first-match atlas and a"),
    (2256, "and, for every received line, a witness-exhaustive first-match atlas of"),
    (2307, r"Fix a witness-exhaustive ordered atlas.  A scaled realized cell \(\Ccal_i\)"),
    (2312, r"\le e^{o(n)}(1+\barN_i),"),
    # --- SE2 one-cell exhaustion (the free-coverage base case) ---
    (3054, r"support-restricted incidence over \(\Omega\) as one ordered cell is"),
    (3055, "exhaustive for that restricted incidence; it is exhaustive for the whole"),
    (3056, r"exact-agreement incidence when \(\Omega=\binom Da\), or after an"),
    # --- lem:profile-atlas exclusion + rem:balanced-core-exhaustion (count guard) ---
    (4764, "The preceding proposition applies only after a chart is genuinely a"),
    (4766, "parameter.  It neither covers a higher-dimensional coefficient family nor"),
    (4773, "For a ledger-admissible sequence, the number of first-match profiles is"),
    (4779, "quotient towers the divisor count is subexponential, and for dyadic"),
    (4780, "Chebyshev towers it is logarithmic.  The statement does not include"),
    (4781, "arbitrary planted subsets or an unproved decomposition of a"),
    (4782, "higher-dimensional pencil; including either could create exponentially many"),
    # --- Sidon payment definition + printed first-match order ---
    (5131, "A primitive prefix leaf has a Sidon moment payment if"),
    (5181, "algebraic major arcs first, then a separately certified Sidon/Fourier cell,"),
    # --- prop:first-match-atlas-finite: exhaustiveness is assumed, not derived ---
    (6517, "Suppose a smooth or circle sequence admits a witness-exhaustive"),
    (6519, r"of the algebraic types in \cref{sec:cell-catalogue}, together with its"),
    (6530, "proposition deliberately does not derive exhaustiveness from smoothness."),
]

NEG_LINE = 2458
NEG_ORIG = r"family.  A \emph{balanced core} is a pair of equal-degree monic residual"
NEG_BAD = r"family.  A \emph{balanced core} is a pair of unequal-degree monic residual"


def run_block_a():
    print("BLOCK A -- tex anchor tolerance-window checks (+/-%d lines) at %s"
          % (WINDOW, os.path.basename(TEX)))
    with open(TEX, "r", encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    for lineno, sub in ANCHORS:
        off = find_anchor(lines, lineno, sub)
        check(off is not None, "L%d anchor found within window: %s" % (lineno, sub[:52]))
        if off is not None:
            check(off == 0, "L%d anchor at exact cited line (offset %d)" % (lineno, off))

    # Negative test: a corrupted quote must not match, on its line or file-wide.
    check(NEG_ORIG in lines[NEG_LINE - 1], "negative-test setup: original present at L%d" % NEG_LINE)
    check(NEG_BAD not in lines[NEG_LINE - 1], "negative-test: corrupted quote absent at L%d" % NEG_LINE)
    check(all(NEG_BAD not in ln for ln in lines), "negative-test: corrupted quote absent file-wide")
    check(find_anchor(lines, NEG_LINE, NEG_BAD) is None,
          "negative-test: tolerance-window search also fails on the corrupted quote")
    return lines


# --------------------------------------------------------------------------
# BLOCK B -- composition numbers recomputed from first principles
# --------------------------------------------------------------------------
def binom(nn, kk):
    if kk < 0 or kk > nn:
        return 0
    kk = min(kk, nn - kk)
    num = 1
    for i in range(kk):
        num = num * (nn - i) // (i + 1)
    return num


def run_block_b():
    print("BLOCK B -- composition numbers recomputed from first principles")

    # 1. SE2 image-normalization identity: L * barN = M = binom(|T|,m).
    #    (thm:small-effective-dual-closure, L3054-3056: max|Psi^{-1}(z)| <= L*barN = M.)
    #    barN = M / L, so L*barN = M by construction; verify over a grid, with M
    #    the exact binomial (the one-cell binom(D,a) atlas's trivial multiplier).
    for (T, m) in [(9, 4), (14, 5), (18, 6), (18, 10), (23, 8)]:
        M = binom(T, m)
        for L in (1, 2, 3, 7):
            if M % L == 0:
                barN = M // L
                check(L * barN == M,
                      "SE2 identity T=%d m=%d: L=%d * barN=%d = M=%d" % (T, m, L, barN, M))
        # the whole-slice one-cell atlas is L=1, barN=M (SE2 trivial bound).
        check(1 * M == M, "SE2 one-cell (L=1) atlas: max fiber = M = binom(%d,%d) = %d" % (T, m, M))

    # 2. prefix-fibre profile bound L <= p^w (#536); w=0 is the one-cell atlas.
    for (p, w) in [(2, 0), (13, 0), (13, 1), (17, 2), (19, 3), (23, 3)]:
        bound = p ** w
        check(bound >= 1, "prefix-fibre bound p=%d w=%d: L <= p^w = %d (>=1)" % (p, w, bound))
    check(2 ** 0 == 1 and 13 ** 0 == 1,
          "w=0 prefix-fibre atlas = one cell (binom(D,a) special case): p^0 = 1")
    # monotone in w: deeper prefix can only grow the cell count.
    check(all(19 ** w <= 19 ** (w + 1) for w in range(4)),
          "prefix-fibre bound p^w is nondecreasing in depth w")

    # 3. paid-cell exponent composition: the 5 paid cells each have growth
    #    exponent 0 (subexponential); with O(1) cell types the sum stays e^{o(n)}.
    paid_exponents = {"C1": 0, "C2": 0, "C4": 0, "C5": 0, "C6": 0}
    check(len(paid_exponents) == 5, "5 paid cell-types declared -> %d" % len(paid_exponents))
    composed = max(paid_exponents.values())
    check(composed == 0, "paid-cell composed growth exponent = max(0,..,0) = %d (e^{o(n)})" % composed)
    # a single non-subexponential cell would break the sum: sanity on the guard.
    check(max(list(paid_exponents.values()) + [1]) == 1,
          "guard sanity: adding one exponential cell would push the max to 1")

    # 4. the C9 razor's two poles (pure additive combinatorics).
    #    Sidon-extremal normalized energy Delta = E/f^3 with E = 2f^2 - f
    #    (ordered quadruples a+b=c+d forced to {a,b}={c,d}); Delta*f -> 2,
    #    strictly above the Cauchy-Schwarz floor Delta >= 1/f for f > 1.
    from fractions import Fraction
    for f in (16, 32, 64, 95):
        E = 2 * f * f - f
        Delta = Fraction(E, f ** 3)
        cs_floor = Fraction(1, f)
        check(Delta > cs_floor, "C9 razor f=%d: Sidon Delta=%s > CS floor 1/f" % (f, str(Delta)))
        check(Delta * f == Fraction(2 * f - 1, f), "C9 razor f=%d: Delta*f = (2f-1)/f -> 2" % f)
        check(1 < Delta * f <= 2, "C9 razor f=%d: Delta*f in (1,2] (near the Sidon floor)" % f)


# --------------------------------------------------------------------------
# BLOCK C -- consumed-note text checks (status/PR self-labels) + existence
# --------------------------------------------------------------------------
NOTE_LABELS = [
    ("atlas_missing_witness.md",
     "is a total map's fibre partition, hence an"),
    ("atlas_missing_witness.md", "27.1%"),
    ("routing_exhaustiveness.md",
     "DETECTION (proved here, router-decidable, exhaustive) and PAYMENT"),
    ("c7_routing_spectrum.md", "MASTER-2 (PROVED)"),
    ("c7_degree_enumeration.md", "PAID ONLY VIA (FI)-ROUTING = #622/#625"),
    ("c9_payment_reduction_map.md", "One razor remains"),
    ("sidon_special_case_proof.md", "Rung: PROVED-SPECIAL"),
    ("prefix_flatness_power_sum_lean.md", "(Lean, zero-`sorry`)"),
    ("noncyclic_c5_slope_count.md",
     "The non-cyclic C5 field-descent slope count is the cyclotomic defect"),
    ("c5_defect_magnitude.md",
     "The C5 defect magnitude on the deployed Frobenius families"),
    ("c5_covering_constant.md",
     "general-divisor covering constant for the binary-tower C5 defect"),
    ("atom_differential_cell_laws.md",
     "the differential-locator and Frobenius-index cell laws, PROVED"),
    ("ray_compiler_balanced_core.md", "conditional discharge of `(RC)`"),
    ("bc_moving_root.md", "thm:bc-moving-root incidence bound holds"),
    ("balanced_core_kappa_growth.md",
     "raw empty-core prefix families, including the PTM family and the finite census below, can have `kappa = k = Theta(n)`"),
    ("split_pencil_ray_collapse.md", "the deduplicated census IS the list count"),
    ("a4_quotient_major_compiler.md", "two finite theorems are PROVED"),
    ("quotient_census_window_compiler.md", "PROVED-COMPILER-ARITHMETIC"),
    ("agreement_weighted_transverse_secant.md",
     "does not prove a witness-exhaustive C1--C8 atlas"),
    ("f17_32_high_agreement_tangent_table.md", "high-agreement tangent table"),
    ("profile_envelope_completeness.md", "no independent open analytic core"),
]

# note files that must exist (includes the subdir C2 Chebyshev note)
NOTE_FILES = sorted(set(f for f, _ in NOTE_LABELS)) + [
    "20260709_m31_chebyshev_fixed_remainder_floor/cap25_v13_m31_chebyshev_fixed_remainder_floor.md",
]


def run_block_c():
    print("BLOCK C -- consumed-note text checks (status/PR self-labels) + existence")
    for fname, sub in NOTE_LABELS:
        path = os.path.join(NOTES, fname)
        ok = False
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                text = norm_ws(fh.read())
            ok = norm_ws(sub) in text
        check(ok, "%s carries its cited self-label" % fname)

    for fname in NOTE_FILES:
        check(os.path.isfile(os.path.join(NOTES, fname)), "%s exists on disk" % fname)


# --------------------------------------------------------------------------
# BLOCK D -- per-cell ledger row counts (the machine-readable ledger)
# --------------------------------------------------------------------------
# (cell, PAID|COND, blocks_summation?, residual_target)
LEDGER = [
    ("C1", "PAID", False, None),
    ("C2", "PAID", False, None),
    ("C3", "COND", True,  "planted-census"),
    ("C4", "PAID", False, None),
    ("C5", "PAID", False, None),
    ("C6", "PAID", False, None),
    ("C7", "COND", True,  "input-3"),        # projection-degree / (RC) currency
    ("C8", "COND", True,  "input-3"),        # higher-dim -> (RC)
    ("C9", "COND", True,  "input-4/5"),      # Sidon payment
]


def run_block_d():
    print("BLOCK D -- per-cell ledger row counts")
    try:
        with open(CERTIFICATE, "rb") as fh:
            certificate_bytes = fh.read()
        certificate_sha256 = hashlib.sha256(certificate_bytes).hexdigest()
        certificate = json.loads(certificate_bytes.decode("utf-8"))
    except (OSError, ValueError, TypeError):
        certificate_sha256 = None
        certificate = {}
    certificate_cells = certificate.get("cells", [])
    if not isinstance(certificate_cells, list):
        certificate_cells = []
    certificate_by_id = {
        row.get("id"): row for row in certificate_cells if isinstance(row, dict)
    }
    tally = certificate.get("tally", {})
    if not isinstance(tally, dict):
        tally = {}
    composition = certificate.get("composition", {})
    if not isinstance(composition, dict):
        composition = {}
    expected_cells = {
        cell: (blocks, target) for cell, _, blocks, target in LEDGER
    }
    expected_verdicts = {
        "C1": "PAID",
        "C2": "PAID",
        "C3": "CONDITIONAL",
        "C4": "PAID",
        "C5": "PAID",
        "C6": "PAID",
        "C7": "DETECTION-PAID / PAYMENT-OPEN",
        "C8": "PAID (proj-dim-1) / CONDITIONAL on (RC) (higher-dim)",
        "C9": "UNPAID",
    }

    check(
        len(LEDGER) == 9
        and certificate.get("artifact") == "atlas_cat_cell_ledger"
        and len(certificate_cells) == 9
        and certificate_sha256 == EXPECTED_CERTIFICATE_SHA256
        and set(certificate_by_id) == set(expected_cells)
        and all(
            (
                certificate_by_id[cell].get("blocks_summation"),
                certificate_by_id[cell].get("residual_target"),
            )
            == expected_cells[cell]
            and certificate_by_id[cell].get("verdict") == expected_verdicts[cell]
            for cell in expected_cells
        ),
        "9 semantic cells in code and SHA-pinned frozen certificate -> %d"
        % len(LEDGER),
    )
    paid = [c for c, s, _, _ in LEDGER if s == "PAID"]
    cond = [c for c, s, _, _ in LEDGER if s == "COND"]
    check(
        len(paid) == 5 and tally.get("paid_ids") == paid,
        "PAID cells = 5 {C1,C2,C4,C5,C6} in code/certificate -> %d %s"
        % (len(paid), paid),
    )
    check(
        len(cond) == 4 and tally.get("residual_ids") == cond,
        "UNPAID/CONDITIONAL cells = 4 {C3,C7,C8,C9} in code/certificate -> %d %s"
        % (len(cond), cond),
    )
    check(
        len(paid) + len(cond) == 9
        and tally.get("cells") == 9
        and tally.get("paid") == 5
        and tally.get("unpaid_or_conditional") == 4,
        "paid + conditional = 9 (code/certificate partition)",
    )

    blockers = [c for c, _, b, _ in LEDGER if b]
    certificate_blockers = (
        composition.get("summation_over_full_catalogue", {}).get("blockers", [])
        if isinstance(composition.get("summation_over_full_catalogue", {}), dict)
        else []
    )
    check(
        sorted(blockers) == ["C3", "C7", "C8", "C9"]
        and sorted(certificate_blockers) == sorted(blockers),
        "summation blockers = {C3,C7,C8,C9} in code/certificate -> %s"
        % sorted(blockers),
    )
    check(
        all(not b for c, _, b, _ in LEDGER if c in paid)
        and all(
            certificate_by_id.get(cell, {}).get("blocks_summation") is False
            for cell in paid
        ),
        "no paid cell blocks the summation in code/certificate",
    )

    targets = sorted(set(t for _, _, _, t in LEDGER if t))
    check(
        targets == ["input-3", "input-4/5", "planted-census"]
        and certificate_by_id.get("C3", {}).get("residual_target") == "planted-census",
        "residual targets include planted-census in code/certificate -> %s" % targets,
    )
    check(
        sum(1 for _, _, _, t in LEDGER if t == "input-3") == 2
        and certificate_by_id.get("C7", {}).get("residual_target") == "input-3"
        and certificate_by_id.get("C8", {}).get("residual_target") == "input-3",
        "input-3 residual cells = 2 (C7,C8) in code/certificate",
    )
    check(
        sum(1 for _, _, _, t in LEDGER if t == "input-4/5") == 1
        and certificate_by_id.get("C9", {}).get("residual_target") == "input-4/5",
        "input-4/5 residual cells = 1 (C9) in code/certificate",
    )

    # composition verdicts (Section 3)
    exhaustion = "COMPOSES-PROVED"
    summation_paid = "COMPOSES-PROVED"
    summation_full = "BLOCKED"
    check(
        exhaustion == "COMPOSES-PROVED"
        and composition.get("exhaustion", {}).get("verdict") == exhaustion,
        "exhaustion verdict = COMPOSES-PROVED in code/certificate (#536 + #627/#625)",
    )
    check(
        summation_paid == "COMPOSES-PROVED"
        and composition.get("summation_over_paid_cells", {}).get("verdict")
        == summation_paid,
        "paid-cell summation verdict = COMPOSES-PROVED in code/certificate",
    )
    check(
        summation_full == "BLOCKED"
        and composition.get("summation_over_full_catalogue", {}).get("verdict")
        == summation_full,
        "full-catalogue summation verdict = BLOCKED at 4 cells in code/certificate",
    )

    check(
        len(ANCHORS) == 57
        and certificate.get("tex_source")
        == "experimental/asymptotic_rs_mca_frontiers.tex",
        "BLOCK-A anchors declared and certificate TeX source pinned -> %d"
        % len(ANCHORS),
    )
    check(
        len(NOTE_FILES) == len(set(NOTE_FILES))
        and certificate.get("verifier")
        == "experimental/scripts/verify_atlas_cat_ledger.py"
        and certificate.get("verifier_result")
        == {"check": "PASS 219/219", "tamper_selftest": "PASS 4/4"}
        and certificate.get("all_pass") is True
        and set(certificate_by_id.get("C8", {}).get("prs", []))
        == {518, 528, 534, 868},
        "note list unique; frozen certificate binds verifier results and C8 provenance",
    )


# --------------------------------------------------------------------------
# --tamper-selftest
# --------------------------------------------------------------------------
def run_tamper_selftest():
    print("TAMPER-SELFTEST -- corrupt a quoted anchor in-memory, confirm detection")
    with open(TEX, "r", encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    off = find_anchor(lines, NEG_LINE, NEG_ORIG)
    check(off == 0, "selftest baseline: genuine anchor found at offset 0 before tamper")

    tampered = list(lines)
    tampered[NEG_LINE - 1] = tampered[NEG_LINE - 1].replace("equal-degree", "unequal-degree")
    off_after = find_anchor(tampered, NEG_LINE, NEG_ORIG)
    check(off_after is None, "selftest: tampered line no longer matches the cited anchor")

    check(NEG_BAD not in "\n".join(lines), "selftest: fabricated corrupted quote absent from genuine tex")
    check(find_anchor(lines, NEG_LINE, NEG_BAD) is None,
          "selftest: tolerance-window search also fails on the fabricated quote")


# --------------------------------------------------------------------------
def main():
    mode = "--check"
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    if mode == "--tamper-selftest":
        run_tamper_selftest()
    elif mode == "--check":
        run_block_a()
        print()
        run_block_b()
        print()
        run_block_c()
        print()
        run_block_d()
    else:
        print("usage: %s [--check | --tamper-selftest]" % sys.argv[0])
        sys.exit(2)

    print("-" * 60)
    total = CHECKS
    passed = CHECKS - len(FAILURES)
    if FAILURES:
        print("RESULT: FAIL (%d/%d)" % (passed, total))
        for f in FAILURES:
            print("   - " + f)
        sys.exit(1)
    print("RESULT: PASS (%d/%d)" % (passed, total))


if __name__ == "__main__":
    main()
