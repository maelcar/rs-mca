#!/usr/bin/env python3
"""Independent audit of the integrated dense-shell class-charge packet.

This verifier does not import the audited verifier. It reimplements only the
definitions needed for two counterexamples, pins the four audited source blobs,
and inspects the literal source/certificate contracts. A PASS means that the
COUNTEREXAMPLE audit is reproduced; it does not certify the target theorem.

stdlib only, deterministic, and nonzero exit on any failed audit check.
"""

import ast
import hashlib
import json
import math
import sys
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "experimental/notes/thresholds/dense_shell_class_charges.md"
TARGET = ROOT / "experimental/scripts/verify_dense_shell_class_charges.py"
CERT = (ROOT / "experimental/data/certificates/dense-shell-class-charges"
        / "dense_shell_class_charges.json")
LEAN = (ROOT / "experimental/lean/dense_shell_class_charges"
        / "DenseShellClassCharges.lean")

EXPECTED_SHA256 = {
    NOTE: "e4448ba13c871b012c2e7b3d0f9cf4104313c80817403f74d5f827c1621f0360",
    TARGET: "afa150cae1287cf9919e31a36d449dd466834e9d883022f9085d221a7f49f8ce",
    CERT: "932a222fb8270a2350f3236e289466838fbdea3977c4f7794f3aba78b87c4fed",
    LEAN: "40c24498420116373b287fbc5743c235d5d6bde8aa6a70378d831bc24d87413c",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def balanced_digits(x, B):
    y = x % (3 ** B)
    out = []
    for _ in range(B):
        d = y % 3
        if d == 2:
            d = -1
        y = (y - d) // 3
        out.append(d)
    return out


def scan_states(word):
    u = 0.0
    out = []
    for d in word:
        u = (d + u) / 3.0
        out.append(u)
    return out


def middle_coefficient(word):
    poly = [1.0]
    for u in scan_states(word):
        t = 2.0 * math.cos(2.0 * math.pi * u)
        new = [0.0] * (len(poly) + 2)
        for k, coefficient in enumerate(poly):
            new[k] += coefficient
            new[k + 1] += coefficient * t
            new[k + 2] += coefficient
        poly = new
    return poly[len(word)]


def word_to_xi(word, B):
    return sum(d * 3 ** i for i, d in enumerate(word)) % (3 ** B)


def charge_counterexample():
    B = 4
    support = (0,)
    modulus = 3 ** B
    words = list(product((-1, 1), repeat=B))
    xis = [word_to_xi(word, B) for word in words]
    weights = [middle_coefficient(word) for word in words]
    sigmas = [
        sigma for sigma in range(modulus)
        if tuple(i for i, d in enumerate(balanced_digits(sigma, B)) if d)
        == support
    ]
    values = []
    for sigma in sigmas:
        value = sum(
            weight * math.cos(2.0 * math.pi * ((xi * sigma) % modulus)
                              / modulus)
            for xi, weight in zip(xis, weights)
        ) / modulus
        values.append(value)

    expected_sign = -1
    sigma_sum = sum(values)
    wrong_mass = sum(abs(value) for value in values
                     if value * expected_sign < 0.0)
    omega = sum(max(value, 0.0) for value in values)
    total_variation = sum(abs(value) for value in values)
    return {
        "sigmas": sigmas,
        "values": values,
        "sigma_sum": sigma_sum,
        "wrong_mass": wrong_mass,
        "omega": omega,
        "universal_rhs": sigma_sum + wrong_mass,
        "corrected_rhs": wrong_mass + (abs(sigma_sum)
                                       if expected_sign > 0 else 0.0),
        "general_rhs": (total_variation + sigma_sum) / 2.0,
    }


def mult_root(coefficients, root):
    out = [0.0] * (len(coefficients) + 1)
    for i, coefficient in enumerate(coefficients):
        out[i] += (0.5 - root) * coefficient
        out[i + 1] += (0.25 if i >= 1 else 0.5) * coefficient
        if i >= 1:
            out[i - 1] += 0.25 * coefficient
    return out


def add(left, right):
    out = [0.0] * max(len(left), len(right))
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] += value
    return out


def subtract(left, right):
    out = [0.0] * max(len(left), len(right))
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] -= value
    return out


def scale(factor, values):
    return [factor * value for value in values]


def a_of(t):
    return math.sin(math.pi * t) ** 2


def da_of(t):
    return math.pi * math.sin(2.0 * math.pi * t)


def gd_direct(j, u):
    """Direct joint (G_j,DG_j) tree recursion, with no interpolation."""
    if j == 0:
        return [1.0], [0.0]
    plus = (1.0 + u) / 3.0
    minus = (1.0 - u) / 3.0
    gp, dp = gd_direct(j - 1, plus)
    gm, dm = gd_direct(j - 1, minus)
    g = add(mult_root(gp, a_of(plus)), mult_root(gm, a_of(minus)))
    dplus = subtract(mult_root(dp, a_of(plus)), scale(da_of(plus), gp))
    dminus = subtract(mult_root(dm, a_of(minus)), scale(da_of(minus), gm))
    d = scale(1.0 / 3.0, subtract(dplus, dminus))
    return g, d


def flip(coefficients):
    degree = len(coefficients) - 1
    return [value if (degree - i) % 2 == 0 else -value
            for i, value in enumerate(coefficients)]


def secant_exponent(x, y, j=3, index=0):
    gx = flip(gd_direct(j, x)[0])[index]
    gy = flip(gd_direct(j, y)[0])[index]
    ratio = min(gx / gy, gy / gx)
    exponent = -math.log(ratio) / (y - x)
    return gx, gy, ratio, exponent


def literal_function_locations(tree, value):
    locations = set()
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for child in ast.walk(node):
            if (isinstance(child, ast.Constant)
                    and isinstance(child.value, (int, float))
                    and not isinstance(child.value, bool)
                    and abs(float(child.value) - value) < 1e-14):
                locations.add(node.name)
    return locations


def strip_lean_comments(text):
    """Remove nested block and line comments from the pinned Lean source."""
    out = []
    depth = 0
    i = 0
    while i < len(text):
        if depth and text.startswith("/-", i):
            depth += 1
            i += 2
        elif depth and text.startswith("-/", i):
            depth -= 1
            i += 2
        elif depth:
            i += 1
        elif text.startswith("/-", i):
            depth = 1
            i += 2
        elif text.startswith("--", i):
            end = text.find("\n", i)
            if end == -1:
                break
            out.append("\n")
            i = end + 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def run(cap=1.61, identity="universal", quiet=False):
    checks = []

    def record(name, detail, ok):
        checks.append((name, detail, bool(ok)))

    for path, expected in EXPECTED_SHA256.items():
        actual = sha256(path)
        record("source pin: " + path.name, actual, actual == expected)

    note_text = NOTE.read_text(encoding="utf-8")
    target_text = TARGET.read_text(encoding="utf-8")
    target_tree = ast.parse(target_text, filename=str(TARGET))
    certificate = json.loads(CERT.read_text(encoding="utf-8"))

    charge = charge_counterexample()
    if identity == "universal":
        identity_rhs = charge["universal_rhs"]
    elif identity == "corrected":
        identity_rhs = charge["corrected_rhs"]
    else:
        raise ValueError("unknown identity mode")
    charge_ok = (
        charge["sigmas"] == [1, 80]
        and all(abs(value + 1.7995914126035255) < 2e-13
                for value in charge["values"])
        and abs(charge["omega"] - identity_rhs) > 3.0
        and abs(charge["omega"] - charge["corrected_rhs"]) < 1e-13
        and abs(charge["omega"] - charge["general_rhs"]) < 1e-13
    )
    record(
        "C6 universal identity counterexample",
        "Sigma=%.15g W=%.15g omega=%.15g Sigma+W=%.15g"
        % (charge["sigma_sum"], charge["wrong_mass"], charge["omega"],
           charge["universal_rhs"]),
        charge_ok,
    )

    gx, gy, ratio, endpoint_L = secant_exponent(4.0 / 9.0, 0.5)
    interior_y = 0.499999
    interior_x = interior_y - 1.0 / 18.0
    _, _, _, interior_L = secant_exponent(interior_x, interior_y)
    envelope_ok = (endpoint_L > cap and interior_L > cap
                   and ratio < math.exp(-cap / 18.0))
    record(
        "P7 pair-2 counterexample",
        "Gx=%.16g Gy=%.16g L(endpoint)=%.15g L(interior)=%.15g cap=%.3f"
        % (gx, gy, endpoint_L, interior_L, cap),
        envelope_ok,
    )

    statement_ok = (
        "omega(class) = h_+ =" in note_text
        and "Sigma_U + W_U exactly" in note_text
        and "Wrong-parity classes:\nomega = W_U" in note_text
        and "pair-2 <= 1.61 on [0.3889, 0.50]" in note_text
        and 'PAIR2 = ("pair-2 [.3889,.50]", 0.38889, 0.49995)'
            in target_text
        and "def secant_env(Glev, j, lo, hi, gmin, gmax, n=110):"
            in target_text
    )
    record("statement/gate mismatch is present",
           "note includes .50; gate ends .49995 on a 110-cell grid",
           statement_ok)

    loose_locations = {
        "1.086": literal_function_locations(target_tree, 1.086),
        "1.663": literal_function_locations(target_tree, 1.663),
    }
    loose_ok = all(locations == {"gate_key"}
                   for locations in loose_locations.values())
    record("loose-cap literals are P8 inputs only", repr(loose_locations),
           loose_ok)

    finite_grid_ok = (
        "maxslope = max(maxslope, abs(dmins[k] - dmins[k - 1]) / h)"
            in target_text
        and "for k in range(1, 200):" in target_text
        and "G_at(Glev" in target_text
        and "interpolation remainder" not in target_text.lower()
    )
    record("continuum enclosures are absent",
           "P9 observed slope; P12 199 interior samples; no remainder field",
           finite_grid_ok)

    metadata = {"source_sha256", "script_sha256", "commit", "command",
                "deep", "jmax", "horizon"}
    cert_ok = (
        not metadata.intersection(certificate)
        and certificate.get("pass") is True
        and abs(certificate["envelope_sups"]["pair2"]
                - 1.6078949860283844) < 1e-15
        and ('elif "--emit-cert" in sys.argv:\n'
             '        allok, margins, leak, extra = run()') in target_text
        and 'elif "--deep" in sys.argv:' in target_text
    )
    record("certificate is shallow and unbound",
           "missing metadata=" + ",".join(sorted(metadata)), cert_ok)

    lean_text = LEAN.read_text(encoding="utf-8")
    lean_code = strip_lean_comments(lean_text).lower()
    lean_ok = (
        "content (the MASTER inequality, cone purity, the leak table) lives in"
            in lean_text
        and "sorry" not in lean_code
        and "admit" not in lean_code
        and "axiom " not in lean_code
    )
    record("Lean source is a clean finite skeleton",
           "no placeholder; analytic MASTER explicitly out of scope", lean_ok)

    if not quiet:
        for name, detail, ok in checks:
            print(("PASS" if ok else "FAIL") + " | " + name + " | " + detail)
        passed = sum(ok for _, _, ok in checks)
        print("RESULT: %s (%d/%d)" %
              ("PASS" if passed == len(checks) else "FAIL", passed,
               len(checks)))
        print("STATUS: COUNTEREXAMPLE")
    return all(ok for _, _, ok in checks), checks


def tamper_selftest():
    normal_ok, _ = run(quiet=True)
    _, loose_cap_checks = run(cap=1.611, quiet=True)
    _, corrected_identity_checks = run(identity="corrected", quiet=True)
    loose_failures = {name for name, _, ok in loose_cap_checks if not ok}
    identity_failures = {
        name for name, _, ok in corrected_identity_checks if not ok
    }
    caught = int(normal_ok and loose_failures == {
        "P7 pair-2 counterexample"
    }) + int(normal_ok and identity_failures == {
        "C6 universal identity counterexample"
    })
    ok = normal_ok and caught == 2
    print("TAMPER SELFTEST: %s (%d/2 caught)" %
          ("PASS" if ok else "FAIL", caught))
    print("STATUS: COUNTEREXAMPLE")
    return ok


if __name__ == "__main__":
    if "--tamper-selftest" in sys.argv[1:]:
        success = tamper_selftest()
    elif sys.argv[1:]:
        print("usage: %s [--tamper-selftest]" % sys.argv[0], file=sys.stderr)
        success = False
    else:
        success, _ = run()
    raise SystemExit(0 if success else 1)
