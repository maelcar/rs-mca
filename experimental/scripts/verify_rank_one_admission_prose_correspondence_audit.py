#!/usr/bin/env python3
"""Audit the repaired rank-one admission prose/source correspondence.

The counterexample reproduced here is deliberately narrow.  At pre-repair
upstream ``c4856fa6``, the #866 audit said that the grammar-only overclaim was
``FIXED IN PROSE`` even though only the #824 note had been repaired.  Four
integrated producer/consumer notes still promoted local scalar accounting to a grammar-only
admission residual.  This is a counterexample to that prose/source-binding
claim, never to the T4 capped-Walsh inequality or the S4 omega cap.

This verifier imports none of the audited verifiers.  It pins fourteen live
artifacts by both their exact Git-blob SHA-1 and byte SHA-256, checks the
repaired prose boundary, compares literal verifier data with checked JSON,
checks the local historic Git objects, and checks the stated Lean boundary.
Stdlib only and deterministic.

Normal output is exactly::

    RESULT: PASS (N/N)
    STATUS: COUNTEREXAMPLE

``--tamper-selftest`` independently tests a source-byte change, restoration
of stale grammar-only prose, unscoped payment promotion, certificate-status
promotion, and six independent historic-pin corruptions.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[2]
PRE_REPAIR_UPSTREAM = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
INTEGRATION_COMMITS = {
    818: "168e9ba0280e069a8bd552a6e2098bb9248c70b7",
    820: "168e9ba0280e069a8bd552a6e2098bb9248c70b7",
    824: "168e9ba0280e069a8bd552a6e2098bb9248c70b7",
    827: "168e9ba0280e069a8bd552a6e2098bb9248c70b7",
    842: "168e9ba0280e069a8bd552a6e2098bb9248c70b7",
    866: "06b2a6fb8c49a5ec0e23b9103af7c92a328fcabf",
}
HISTORIC_MANIFEST_SHA256 = (
    "a76d1e68fcdc92a69af1d516a6fcf9f5471d1291516433d24485851d5f6635e0"
)

RANK_ONE_ARITHMETIC = (
    "experimental/notes/thresholds/rank_one_emission_arithmetic.md"
)
OMEGA_FLOOR = "experimental/notes/thresholds/omega_sound_emission_floor.md"
OMEGA_VERIFIER = "experimental/scripts/verify_omega_sound_emission_floor.py"
OMEGA_CERT = (
    "experimental/data/certificates/omega-sound-emission-floor/"
    "omega_sound_emission_floor.json"
)
OMEGA_LEAN = (
    "experimental/lean/omega_sound_emission_floor/"
    "OmegaSoundEmissionFloor.lean"
)
SHELL_LAW = "experimental/notes/thresholds/shell_mass_spectral_law.md"
PRODUCT_TRANSFER = (
    "experimental/notes/thresholds/product_profile_transfer_certificate.md"
)
ADMISSION_AUDIT = (
    "experimental/notes/audits/rank_one_admission_interface_audit.md"
)
GREEDY_NOTE = "experimental/notes/thresholds/rank_one_greedy_adequacy.md"
ADMISSION_VERIFIER = (
    "experimental/scripts/verify_rank_one_admission_interface.py"
)
ADMISSION_CERT = (
    "experimental/data/certificates/rank-one-admission-interface/"
    "rank_one_admission_interface.json"
)
GREEDY_VERIFIER = "experimental/scripts/verify_rank_one_greedy_adequacy.py"
GREEDY_CERT = (
    "experimental/data/certificates/rank-one-greedy-adequacy/"
    "rank_one_greedy_adequacy.json"
)
GREEDY_LEAN = (
    "experimental/lean/rank_one_greedy_adequacy/"
    "RankOneGreedyAdequacy.lean"
)

PINNED_PATHS = (
    RANK_ONE_ARITHMETIC,
    OMEGA_FLOOR,
    OMEGA_VERIFIER,
    OMEGA_CERT,
    OMEGA_LEAN,
    SHELL_LAW,
    PRODUCT_TRANSFER,
    ADMISSION_AUDIT,
    GREEDY_NOTE,
    ADMISSION_VERIFIER,
    ADMISSION_CERT,
    GREEDY_VERIFIER,
    GREEDY_CERT,
    GREEDY_LEAN,
)


# These pins are intentionally fail-closed.  Any audited artifact change must
# be independently reviewed and both content digests updated before this audit
# can pass again.
POST_REPAIR_PINS: dict[str, dict[str, str]] = {
    RANK_ONE_ARITHMETIC: {
        "git_blob_sha1": "85d685ccf3e59c948875775da7ef00027739d439",
        "sha256": "572e01eb9cdfe6f500d463d746a3d4f7d46be1b13039ba7d9bd1425f0224a399",
    },
    OMEGA_FLOOR: {
        "git_blob_sha1": "0ae2bbd8702f862c00e0ce055a7bffc0791f38f0",
        "sha256": "a6eef96e773447c533814c386fd5c5178b924e7c5bb4e8ad78d053685d89c913",
    },
    OMEGA_VERIFIER: {
        "git_blob_sha1": "07b51f1185196701603a446958a2d45baafc003b",
        "sha256": "2042bd3999c41b29f8ad44c7ddca98e28e66918a0435f027b43982aa0ea91fd6",
    },
    OMEGA_CERT: {
        "git_blob_sha1": "3b63ebdec1bc5eccfc9d7590932c35a25a79f58e",
        "sha256": "8b81716670be0ca276f7758cca7411a35d47833b55ff75dc3e8513b941bfac0c",
    },
    OMEGA_LEAN: {
        "git_blob_sha1": "daabb3978bfd61fa4a258ab5139b4cc44c01bec2",
        "sha256": "c79da984b2b0ee834c084307f89e1c3f1cc6994900f16aa1f2f7a3f2dd383b01",
    },
    SHELL_LAW: {
        "git_blob_sha1": "56fe9959d70b4177004afdbb6a6accc7a4d8b505",
        "sha256": "c72f00e271e0da37e3ea79e195b3e0da789b6e54db43a67b317992255f31493b",
    },
    PRODUCT_TRANSFER: {
        "git_blob_sha1": "bb14a7f09da68965d824799ca9dfd1a5925b3ff0",
        "sha256": "0cfa04bcfd2fd53353b217a9a25c7d174da8e8e08369ca8a0be0fb87f91a9104",
    },
    ADMISSION_AUDIT: {
        "git_blob_sha1": "fe3e33f2c827d49dea540dcb89bc168e96c7aac5",
        "sha256": "391f492fdd5f2a61853427d5ff3f9fb658cf09001e4013186bf87dc2fa9c0aa4",
    },
    GREEDY_NOTE: {
        "git_blob_sha1": "e2a0078b85ab74d571204ac1482caa8adc8a23b3",
        "sha256": "87fee28e26c1209faf1a967f1694d04875932f7156563864b7613d540bfd6c30",
    },
    ADMISSION_VERIFIER: {
        "git_blob_sha1": "ecf1118e5ed3a79524bd2879234afa17ed2abb00",
        "sha256": "747e3bf31d1abed79afa0192e6c9f80d83df32bf080af55f1221963f2b8417e4",
    },
    ADMISSION_CERT: {
        "git_blob_sha1": "4a632f9fd355bac564ba113c68b996f1105ce409",
        "sha256": "15a8509e9048025e229f038fa08405ccb0fa6459d33d075bb0ff4e1e2ac7030c",
    },
    GREEDY_VERIFIER: {
        "git_blob_sha1": "4e3d902dc7bee82c11dc683b83c4d9e4b830c105",
        "sha256": "1dc06f309b291d7bf1a2c3e12f671e9362ee696f3086e733f27db0b3987ed602",
    },
    GREEDY_CERT: {
        "git_blob_sha1": "d1b4b3ea94891f4404621783721435d1361a6a7e",
        "sha256": "f11470cdd7db37f3448b5ad69e0e5ad9a194ce95bbe6d2a0bacfbdc7dae5078f",
    },
    GREEDY_LEAN: {
        "git_blob_sha1": "d364fc46475b39fd837a02f8ca0154171a70c4bf",
        "sha256": "bc15da3770ced7a5eaf89436560912b001900553c702fa166a2fa3226c60d985",
    },
}


# Immutable evidence for the state audited at PRE_REPAIR_UPSTREAM.  Excerpts
# are byte-exact substrings of those blobs, including their historical wraps.
HISTORIC_EVIDENCE: dict[str, dict[str, Any]] = {
    RANK_ONE_ARITHMETIC: {
        "producer_pr": 818,
        "producer_head": "03fa29587b5a5f75e53b57aa7153a1132acfdd51",
        "blob_sha1": "03df4497d81b4b37fb78b2267a2fcb174b0ed300",
        "sha256": "03c19def9af114fa45b4b134b308a9257cef7849e36d50eb49bb076db7b7e7b9",
        "stale_excerpts": (
            "the admission decision's inputs are now\n"
            "        closed-form.  The question itself remains open and is now:\n"
            "        \"does the certificate grammar admit RANK-ONE emission with T3's\n"
            "        one-pattern floor?\"",
            "**The grammar decision itself** (open, unchanged in kind): does the\n"
            "   compiler admit rank-one emission with T3's one-pattern floor?",
        ),
    },
    OMEGA_FLOOR: {
        "producer_pr": 820,
        "producer_head": "d5f67b4b0546b0f036af101036d7397afb74035e",
        "blob_sha1": "8d8f9b043a798f27e7d22f647c5304f95adfff23",
        "sha256": "a29e4682aad5be95fe4d5ca16245432fa8a480a2da74a496c8c1ca9ab5d31671",
        "stale_excerpts": (
            "The admission decision on\n"
            "        hierarchy pieces is now a pure grammar-acceptance question\n"
            "        (soundness universally; adequacy at the verified scale).",
            "NO soundness\n"
            "> obligation on rank-one emission remains open: the admission decision\n"
            "> is purely whether the grammar ACCEPTS the rule.",
            "the\n"
            "  soundness obligation named in band-uniform's Nonclaims is DISCHARGED;\n"
            "  the decision is now pure grammar acceptance, with the corrected floor",
        ),
    },
    OMEGA_VERIFIER: {
        "producer_pr": 820,
        "producer_head": "d5f67b4b0546b0f036af101036d7397afb74035e",
        "blob_sha1": "ee39de610d01c5dcc462d7d44b27deaff6f08414",
        "sha256": "6f9b85eebb46a1030bd844147c428efb025ea9d01a27bb9ed18f5c02588a6e50",
        "stale_excerpts": (
            "Verifier: the omega-sound emission floor (compiler soundness discharged).",
            "compiler soundness is arithmetic, 0 violations.",
            "corrected rule pays hierarchy pieces IN FULL.",
            "S5: corrected rule pays IN FULL on every charged pair",
        ),
    },
    OMEGA_CERT: {
        "producer_pr": 820,
        "producer_head": "d5f67b4b0546b0f036af101036d7397afb74035e",
        "blob_sha1": "e61ce3e3bfd198a3e8983d9a0c2fbef8610a2c76",
        "sha256": "4b4864557377273b7a0197f3204197e5caecc7ada91dcc9628e35e998a06a663",
        "stale_excerpts": (),
    },
    OMEGA_LEAN: {
        "producer_pr": 820,
        "producer_head": "d5f67b4b0546b0f036af101036d7397afb74035e",
        "blob_sha1": "8062cfe7162c5b1236cd3c72c7733dd7accffcb8",
        "sha256": "8587303252c4174d93a562b3c8011a5406e32c54354d0821aa5b5d363fd7819e",
        "stale_excerpts": (),
    },
    SHELL_LAW: {
        "producer_pr": 827,
        "producer_head": "1512ff45c093ddbd4951000a78adfc4ab913a4a8",
        "blob_sha1": "be949c194e5d5233cf8c8c577785d7e37c077dc5",
        "sha256": "57a8521197d79ef9757f65162d912f6dd06f8262361f8ab9014f280260dbc273",
        "stale_excerpts": (
            "Input-2 residual: the admission acceptance (#824),\n"
            "        product-profile emission (NEW, named here), whether asymptotic",
        ),
    },
    PRODUCT_TRANSFER: {
        "producer_pr": 842,
        "producer_head": "ea8318ff5bda33072f81667c4fa8f9893e1f8f78",
        "blob_sha1": "6365c94944ff2d8059ec53f8d8c6e1cfafc88c29",
        "sha256": "29ec195f210bca5e7ffe597166653b24744191c7f46219c8b2adfe80dc675b60",
        "stale_excerpts": (
            "Input-2 residual: the admission\n"
            "        acceptance, those three steps, non-product non-hierarchy",
        ),
    },
    ADMISSION_AUDIT: {
        "producer_pr": 866,
        "producer_head": "0b45db15d9739c7194d817cd2fc00af72dfac23e",
        "blob_sha1": "d46c62639071f21b822f247bacabe54080a8ca7b",
        "sha256": "ac8bf14464be4ab43bdfb403fea0f3a4514759393a6f3885bcf2abc996789b77",
        "stale_excerpts": (
            "\"grammar acceptance alone remains\":            OPEN GAP / FIXED IN PROSE",
        ),
    },
    GREEDY_NOTE: {
        "producer_pr": 866,
        "producer_head": "0b45db15d9739c7194d817cd2fc00af72dfac23e",
        "blob_sha1": "166449c661a0615fdb3c733e0857d3213177708c",
        "sha256": "64e0a88494e48494e906b2a79b358a6656fe2e70681d5055b5be685f362186ba",
        "stale_excerpts": (),
    },
    ADMISSION_VERIFIER: {
        "producer_pr": 866,
        "producer_head": "0b45db15d9739c7194d817cd2fc00af72dfac23e",
        "blob_sha1": "ef4e4b28485da6da18cdf31ac8c56dc44a457fad",
        "sha256": "42340a2de3f5417e3d453826ff2603d2b9cfd5de79ca006c4a49239398b83ca0",
        "stale_excerpts": (),
    },
    ADMISSION_CERT: {
        "producer_pr": 866,
        "producer_head": "0b45db15d9739c7194d817cd2fc00af72dfac23e",
        "blob_sha1": "d14924faf6e786f132195cf7130b6682a15bd252",
        "sha256": "8722646da230e5dd64412759afefef560a4a11c51ec896e96eaedcbac4f108c3",
        "stale_excerpts": (),
    },
    GREEDY_VERIFIER: {
        "producer_pr": 824,
        "producer_head": "2f5162fc9f25a82c4508c449bdfed35b51b44199",
        "blob_sha1": "9b6e0ad4ed18aaba61b63940ae62fd18e9efc8c1",
        "sha256": "70257d229c45a2fe28409c5275330c25148fce04f3bedf0a1f0d6c3fa7dcaa1f",
        "stale_excerpts": (
            "depth <= 3 hierarchy pieces are paid in full by\n"
            "                         one pattern",
            "FULLY adequate at EVERY depth:",
        ),
    },
    GREEDY_CERT: {
        "producer_pr": 824,
        "producer_head": "2f5162fc9f25a82c4508c449bdfed35b51b44199",
        "blob_sha1": "cfafec6a733ff0c8d9cf00491cb73d47a6d584d6",
        "sha256": "a2855d5505c1976fec5b8cca21ded8ec0fcd523478757f7b3679eec2d12415a9",
        "stale_excerpts": (),
    },
    GREEDY_LEAN: {
        "producer_pr": 824,
        "producer_head": "2f5162fc9f25a82c4508c449bdfed35b51b44199",
        "blob_sha1": "3e11e3d2ee02bab798eb25de02fa5f6d3316ab2c",
        "sha256": "ad80ce541b5a18f2c2ca003a8f5a96e75eca23a37bcde3a90214c2118f0c80f8",
        "stale_excerpts": (),
    },
}


CANONICAL_BOUNDARY = (
    "The governing profile-payment interface remains OPEN: an actual "
    "same-owner first-match cell, an (A4) analytic/Sidon payment, a separate "
    "(A6)/(RC) distinct-slope bound, and a uniform subexponential aggregate "
    "census."
)

REPAIRED_CONSUMERS = (
    RANK_ONE_ARITHMETIC,
    OMEGA_FLOOR,
    SHELL_LAW,
    PRODUCT_TRANSFER,
)

OBLIGATION_NOTES = REPAIRED_CONSUMERS + (ADMISSION_AUDIT, GREEDY_NOTE)

UNUSED_INTERFACE_INPUTS = (
    "same-owner first-match profile cell",
    "A4 analytic/Sidon payment",
    "A6/RC distinct-slope bound",
    "uniform subexponential aggregate census",
)

GREEDY_SCOPE = {
    "certifies": "local scalar capped-Walsh accounting",
    "does_not_certify": list(UNUSED_INTERFACE_INPUTS),
}

OMEGA_SCOPE = {
    "certifies": "local scalar omega-cap accounting",
    "does_not_certify": list(UNUSED_INTERFACE_INPUTS),
}

GENERIC_STALE_MARKERS = (
    "pure grammar acceptance",
    "pure grammar-acceptance",
    "purely whether the grammar accepts",
    "fixed in prose",
)

UNSCOPED_MARKERS = {
    OMEGA_FLOOR: (
        "full adequacy",
        "pays in full",
        "paid in full",
        "pays hierarchy pieces in full",
        "hierarchy pieces are paid in full",
        "entire positive charge",
        "no efficiency loss anywhere",
    ),
    GREEDY_LEAN: ("pays in full", "paid in full"),
    RANK_ONE_ARITHMETIC: (
        "covers every hierarchy piece",
        "is closed for hierarchy pieces",
        "closed for hierarchy pieces",
    ),
}


@dataclass
class Checks:
    total: int = 0
    failures: list[str] = field(default_factory=list)

    def gate(self, condition: bool, label: str) -> None:
        self.total += 1
        if not condition:
            self.failures.append(label)

    @property
    def passed(self) -> int:
        return self.total - len(self.failures)


def normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def historic_manifest_sha256(
    evidence: Mapping[str, Mapping[str, Any]] = HISTORIC_EVIDENCE,
    upstream: str = PRE_REPAIR_UPSTREAM,
    integrations: Mapping[int, str] = INTEGRATION_COMMITS,
) -> str | None:
    try:
        payload = {
            "upstream": upstream,
            "integrations": {
                str(key): value
                for key, value in sorted(integrations.items())
            },
            "evidence": dict(evidence),
        }
        encoded = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    except (TypeError, ValueError):
        return None
    return sha256_bytes(encoded)


@lru_cache(maxsize=None)
def local_git(*args: str) -> tuple[int, bytes]:
    env = os.environ.copy()
    env.update(
        {
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_OPTIONAL_LOCKS": "0",
        }
    )
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=10,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return 127, b""
    return result.returncode, result.stdout


def git_commit(identifier: str) -> bytes | None:
    type_code, object_type = local_git("cat-file", "-t", identifier)
    if type_code != 0 or object_type.strip() != b"commit":
        return None
    body_code, body = local_git("cat-file", "commit", identifier)
    return body if body_code == 0 else None


def git_path_oid(revision: str, relative: str) -> str | None:
    code, output = local_git(
        "rev-parse", "--verify", f"{revision}:{relative}"
    )
    if code != 0:
        return None
    identifier = output.decode("ascii", errors="replace").strip()
    return identifier if re.fullmatch(r"[0-9a-f]{40}", identifier) else None


def git_blob(identifier: str) -> bytes | None:
    code, data = local_git("cat-file", "blob", identifier)
    return data if code == 0 else None


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    code, _ = local_git(
        "merge-base", "--is-ancestor", ancestor, descendant
    )
    return code == 0


def source_pin_matches(relative: str, data: bytes) -> bool:
    expected = POST_REPAIR_PINS[relative]
    return (
        git_blob_sha1(data) == expected["git_blob_sha1"]
        and sha256_bytes(data) == expected["sha256"]
    )


def read_sources(
    overrides: Mapping[str, bytes] | None = None,
) -> dict[str, bytes]:
    supplied = {} if overrides is None else dict(overrides)
    return {
        relative: supplied.get(relative, (ROOT / relative).read_bytes())
        for relative in PINNED_PATHS
    }


def decode(source: Mapping[str, bytes], relative: str) -> str:
    return source[relative].decode("utf-8")


def stale_absent(relative: str, text: str) -> bool:
    live = normalize(text)
    historic = HISTORIC_EVIDENCE[relative]["stale_excerpts"]
    if any(normalize(excerpt) in live for excerpt in historic):
        return False
    if relative in OBLIGATION_NOTES:
        return not any(marker in live for marker in GENERIC_STALE_MARKERS)
    return True


def unscoped_absent(relative: str, text: str) -> bool:
    live = normalize(text)
    return not any(
        marker in live for marker in UNSCOPED_MARKERS.get(relative, ())
    )


def literal_values_for_key(source: str, key: str) -> list[Any]:
    tree = ast.parse(source)
    values: list[Any] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key_node, value_node in zip(node.keys, node.values):
            if not isinstance(key_node, ast.Constant) or key_node.value != key:
                continue
            try:
                values.append(ast.literal_eval(value_node))
            except (TypeError, ValueError):
                values.append(None)
    return values


def target_profile_status_ok(certificate: Mapping[str, Any]) -> bool:
    status = certificate.get("status")
    return (
        isinstance(status, dict)
        and status.get("rank_one_profile_payment")
        == "NOT_CERTIFIED_BY_THIS_IDENTITY"
        and status.get("hard_input_2") == "OPEN"
    )


def strip_lean_comments(text: str) -> str:
    """Remove nested block and line comments without using Lean tooling."""
    out: list[str] = []
    depth = 0
    index = 0
    while index < len(text):
        if depth and text.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and text.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif text.startswith("/-", index):
            depth = 1
            index += 2
        elif text.startswith("--", index):
            newline = text.find("\n", index)
            if newline == -1:
                break
            out.append("\n")
            index = newline + 1
        else:
            out.append(text[index])
            index += 1
    return "".join(out)


def check_historic_table(
    checks: Checks,
    evidence: Mapping[str, Mapping[str, Any]] = HISTORIC_EVIDENCE,
    upstream: str = PRE_REPAIR_UPSTREAM,
    integrations: Mapping[int, str] = INTEGRATION_COMMITS,
) -> None:
    sha1_pattern = re.compile(r"[0-9a-f]{40}\Z")
    sha256_pattern = re.compile(r"[0-9a-f]{64}\Z")
    expected_prs = set(INTEGRATION_COMMITS)

    checks.gate(
        historic_manifest_sha256(evidence, upstream, integrations)
        == HISTORIC_MANIFEST_SHA256,
        "historic manifest digest mismatch",
    )

    checks.gate(
        sha1_pattern.fullmatch(upstream) is not None,
        "historic upstream pin is not a full SHA",
    )
    checks.gate(
        set(evidence) == set(PINNED_PATHS),
        "historic evidence path set differs from the live pin set",
    )
    checks.gate(
        set(integrations) == expected_prs,
        "historic integration PR set changed",
    )
    checks.gate(
        git_commit(upstream) is not None,
        "historic upstream pin is not a locally available commit",
    )

    for producer_pr, integration in sorted(integrations.items()):
        checks.gate(
            isinstance(producer_pr, int) and producer_pr > 0,
            f"malformed integration PR {producer_pr!r}",
        )
        checks.gate(
            isinstance(integration, str)
            and sha1_pattern.fullmatch(integration) is not None,
            f"PR #{producer_pr}: malformed integration commit",
        )
        body = (
            git_commit(integration)
            if isinstance(integration, str)
            else None
        )
        checks.gate(
            body is not None,
            f"PR #{producer_pr}: integration commit is unavailable",
        )
        checks.gate(
            isinstance(integration, str)
            and git_is_ancestor(integration, upstream),
            f"PR #{producer_pr}: integration is not an ancestor of pre-repair upstream",
        )
        pr_pattern = (
            rb"(?<![0-9])#" + str(producer_pr).encode("ascii") + rb"(?![0-9])"
        )
        checks.gate(
            body is not None and re.search(pr_pattern, body) is not None,
            f"PR #{producer_pr}: pinned integration message omits the PR",
        )

    for relative in PINNED_PATHS:
        raw_row = evidence.get(relative, {})
        row = raw_row if isinstance(raw_row, Mapping) else {}
        producer_pr = row.get("producer_pr")
        producer_head = row.get("producer_head")
        blob_sha1 = row.get("blob_sha1")
        sha256 = row.get("sha256")
        excerpts = row.get("stale_excerpts")

        checks.gate(
            isinstance(producer_pr, int) and producer_pr > 0,
            f"{relative}: malformed producer PR",
        )
        checks.gate(
            isinstance(producer_head, str)
            and sha1_pattern.fullmatch(producer_head) is not None,
            f"{relative}: malformed producer head",
        )
        checks.gate(
            isinstance(blob_sha1, str)
            and sha1_pattern.fullmatch(blob_sha1) is not None,
            f"{relative}: malformed historic blob SHA-1",
        )
        checks.gate(
            isinstance(sha256, str)
            and sha256_pattern.fullmatch(sha256) is not None,
            f"{relative}: malformed historic SHA-256",
        )
        checks.gate(
            isinstance(excerpts, tuple)
            and all(isinstance(item, str) and item for item in excerpts),
            f"{relative}: malformed historic excerpt tuple",
        )
        checks.gate(
            isinstance(producer_head, str)
            and git_commit(producer_head) is not None,
            f"{relative}: producer head is not a locally available commit",
        )

        integration = (
            integrations.get(producer_pr)
            if isinstance(producer_pr, int)
            else None
        )
        checks.gate(
            isinstance(integration, str),
            f"{relative}: producer PR lacks a pinned integration",
        )
        head_oid = (
            git_path_oid(producer_head, relative)
            if isinstance(producer_head, str)
            else None
        )
        integration_oid = (
            git_path_oid(integration, relative)
            if isinstance(integration, str)
            else None
        )
        upstream_oid = git_path_oid(upstream, relative)
        checks.gate(
            head_oid == blob_sha1,
            f"{relative}: producer-head path differs from historic blob",
        )
        checks.gate(
            integration_oid == blob_sha1,
            f"{relative}: integration path differs from historic blob",
        )
        checks.gate(
            upstream_oid == blob_sha1,
            f"{relative}: pre-repair upstream path differs from historic blob",
        )

        blob = git_blob(blob_sha1) if isinstance(blob_sha1, str) else None
        checks.gate(blob is not None, f"{relative}: historic blob is unavailable")
        checks.gate(
            blob is not None and git_blob_sha1(blob) == blob_sha1,
            f"{relative}: historic blob Git SHA-1 does not recompute",
        )
        checks.gate(
            blob is not None and sha256_bytes(blob) == sha256,
            f"{relative}: historic blob SHA-256 does not recompute",
        )
        if isinstance(excerpts, tuple):
            for index, excerpt in enumerate(excerpts):
                checks.gate(
                    isinstance(excerpt, str)
                    and blob is not None
                    and excerpt.encode("utf-8") in blob,
                    f"{relative}: historic excerpt {index} is not byte-exact",
                )


def historic_table_ok(
    evidence: Mapping[str, Mapping[str, Any]] = HISTORIC_EVIDENCE,
    upstream: str = PRE_REPAIR_UPSTREAM,
    integrations: Mapping[int, str] = INTEGRATION_COMMITS,
) -> bool:
    checks = Checks()
    check_historic_table(checks, evidence, upstream, integrations)
    return not checks.failures


def check_live_hashes(checks: Checks, source: Mapping[str, bytes]) -> None:
    sha1_pattern = re.compile(r"[0-9a-f]{40}\Z")
    sha256_pattern = re.compile(r"[0-9a-f]{64}\Z")
    checks.gate(
        set(POST_REPAIR_PINS) == set(PINNED_PATHS),
        "post-repair pin path set differs from the required source set",
    )
    for relative in PINNED_PATHS:
        expected = POST_REPAIR_PINS[relative]
        checks.gate(
            sha1_pattern.fullmatch(expected["git_blob_sha1"]) is not None,
            f"{relative}: malformed Git blob SHA-1 pin",
        )
        checks.gate(
            sha256_pattern.fullmatch(expected["sha256"]) is not None,
            f"{relative}: malformed SHA-256 pin",
        )
        checks.gate(
            git_blob_sha1(source[relative]) == expected["git_blob_sha1"],
            f"{relative}: live Git blob SHA-1 mismatch",
        )
        checks.gate(
            sha256_bytes(source[relative]) == expected["sha256"],
            f"{relative}: live SHA-256 mismatch",
        )


def check_note_boundaries(checks: Checks, source: Mapping[str, bytes]) -> None:
    canonical = normalize(CANONICAL_BOUNDARY)
    for relative in REPAIRED_CONSUMERS:
        text = decode(source, relative)
        checks.gate(
            canonical in normalize(text),
            f"{relative}: canonical open profile-payment boundary is absent",
        )

    for relative in OBLIGATION_NOTES:
        text = decode(source, relative)
        live = normalize(text)
        checks.gate(stale_absent(relative, text), f"{relative}: stale prose remains")
        checks.gate(
            unscoped_absent(relative, text),
            f"{relative}: unscoped payment-promotion wording remains",
        )
        checks.gate(
            re.search(r"same-owner.{0,48}first-match", live) is not None,
            f"{relative}: same-owner first-match input is not explicit",
        )
        checks.gate("a4" in live, f"{relative}: A4 input is not explicit")
        checks.gate(
            "a6" in live and "rc" in live,
            f"{relative}: A6/RC input is not explicit",
        )
        checks.gate(
            "aggregate census" in live,
            f"{relative}: aggregate census input is not explicit",
        )
        checks.gate(
            re.search(
                r"remain(?:s)? (?:mathematical )?"
                r"(?:open|necessary|obligations)",
                live,
            )
            is not None,
            f"{relative}: open/remaining status is not explicit",
        )

    audit = normalize(decode(source, ADMISSION_AUDIT))
    checks.gate("fixed in prose" not in audit, "audit retains FIXED IN PROSE")
    checks.gate(
        all(f"#{number}" in audit for number in (818, 820, 824, 827, 842)),
        "audit does not identify #824 versus all four stale consumers",
    )
    checks.gate(
        "does not refute" in audit and "s4" in audit and "t4" in audit,
        "audit does not fence the T4/S4 mathematics",
    )


def check_admission_certificate(
    checks: Checks, source: Mapping[str, bytes]
) -> None:
    verifier = decode(source, ADMISSION_VERIFIER)
    certificate = json.loads(decode(source, ADMISSION_CERT))

    script_inputs = literal_values_for_key(verifier, "inputs_not_used")
    script_status = literal_values_for_key(verifier, "rank_one_profile_payment")
    cert_interface = certificate.get("interface", {})
    cert_inputs = cert_interface.get("inputs_not_used")

    checks.gate(
        script_inputs == [cert_inputs],
        "admission verifier inputs_not_used differ from checked certificate",
    )
    checks.gate(
        script_status == [certificate.get("status", {}).get("rank_one_profile_payment")],
        "admission verifier payment status differs from checked certificate",
    )
    checks.gate(
        target_profile_status_ok(certificate),
        "admission certificate promotes profile payment or hard input 2",
    )
    checks.gate(
        cert_interface.get("inputs_used") == ["cube values"],
        "admission certificate uses more than the scalar cube input",
    )
    checks.gate(
        isinstance(cert_inputs, list)
        and all(item in cert_inputs for item in UNUSED_INTERFACE_INPUTS),
        "admission certificate omits a required unused interface input",
    )
    checks.gate(
        "profile payment not certified" in normalize(verifier),
        "admission verifier output does not say profile payment is not certified",
    )
    checks.gate(
        all(item in verifier for item in UNUSED_INTERFACE_INPUTS),
        "admission verifier source omits a certificate interface literal",
    )


def check_scalar_scope(checks: Checks, source: Mapping[str, bytes]) -> None:
    verifier = decode(source, GREEDY_VERIFIER)
    verifier_norm = normalize(verifier)
    certificate = json.loads(decode(source, GREEDY_CERT))
    script_scopes = literal_values_for_key(verifier, "scope")

    checks.gate(
        certificate.get("scope") == GREEDY_SCOPE,
        "greedy certificate lacks the exact local-scalar scope",
    )
    checks.gate(
        script_scopes == [GREEDY_SCOPE],
        "greedy verifier literal scope differs from checked certificate",
    )
    checks.gate(
        certificate.get("claims") == ["T1", "T2", "T3", "T4"],
        "greedy certificate arithmetic claim list changed",
    )
    checks.gate(
        "local scalar capped-walsh accounting" in verifier_norm,
        "greedy verifier does not scope adequacy to scalar accounting",
    )
    checks.gate(
        all(normalize(item) in verifier_norm for item in UNUSED_INTERFACE_INPUTS),
        "greedy verifier omits a does-not-certify interface literal",
    )
    checks.gate(
        stale_absent(GREEDY_VERIFIER, verifier),
        "greedy verifier retains unscoped paid-in-full wording",
    )


def check_omega_scope(checks: Checks, source: Mapping[str, bytes]) -> None:
    verifier = decode(source, OMEGA_VERIFIER)
    verifier_norm = normalize(verifier)
    certificate = json.loads(decode(source, OMEGA_CERT))
    script_scopes = literal_values_for_key(verifier, "scope")

    checks.gate(
        certificate.get("scope") == OMEGA_SCOPE,
        "omega certificate lacks the exact local-scalar scope",
    )
    checks.gate(
        script_scopes == [OMEGA_SCOPE],
        "omega verifier literal scope differs from checked certificate",
    )
    checks.gate(
        certificate.get("claims") == ["S1", "S2", "S3", "S4", "S5"],
        "omega certificate arithmetic claim list changed",
    )
    checks.gate(
        "local scalar omega-cap accounting" in verifier_norm,
        "omega verifier does not scope soundness to scalar accounting",
    )
    checks.gate(
        all(normalize(item) in verifier_norm for item in UNUSED_INTERFACE_INPUTS),
        "omega verifier omits a does-not-certify interface literal",
    )
    checks.gate(
        stale_absent(OMEGA_VERIFIER, verifier),
        "omega verifier restores historic unscoped wording",
    )
    checks.gate(
        "compiler soundness" not in verifier_norm,
        "omega verifier retains compiler-soundness promotion wording",
    )
    checks.gate(
        "pays in full" not in verifier_norm,
        "omega verifier retains pays-IN-FULL promotion wording",
    )


def check_lean_scope(checks: Checks, source: Mapping[str, bytes]) -> None:
    lean = decode(source, GREEDY_LEAN)
    lean_norm = normalize(lean)
    code = strip_lean_comments(lean)
    checks.gate(
        unscoped_absent(GREEDY_LEAN, lean),
        "greedy Lean header retains unscoped paid-in-full wording",
    )
    checks.gate(
        "analytic results (proved in note + python verifier; not in lean)"
        in lean_norm,
        "Lean source does not declare analytic results outside Lean",
    )
    checks.gate(
        re.search(r"\b(?:sorry|admit|axiom)\b", code, flags=re.IGNORECASE)
        is None,
        "Lean code contains sorry/admit/axiom",
    )
    checks.gate(
        "theorem greedy_cap_sound" in code,
        "Lean arithmetic shadow lost its capped-payment lemma",
    )

    omega = decode(source, OMEGA_LEAN)
    omega_norm = normalize(omega)
    omega_code = strip_lean_comments(omega)
    checks.gate(
        "analytic results (proved in note + python verifier; not in lean)"
        in omega_norm,
        "omega Lean source does not declare analytic results outside Lean",
    )
    checks.gate(
        re.search(r"\b(?:sorry|admit|axiom)\b", omega_code, flags=re.IGNORECASE)
        is None,
        "omega Lean code contains sorry/admit/axiom",
    )
    checks.gate(
        "theorem positive_part_identity" in omega_code,
        "omega Lean arithmetic shadow lost its positive-part identity",
    )
    checks.gate(
        "local scalar soundness" in omega_norm
        and "scalar-accounting-sound" in omega_norm,
        "omega Lean header is not scoped to local scalar accounting",
    )
    checks.gate(
        "compiler-sound" not in omega_norm,
        "omega Lean header retains compiler-sound promotion wording",
    )
    checks.gate(
        "pays every charged class in full" not in omega_norm,
        "omega Lean header retains paid-in-full promotion wording",
    )


def run_checks(
    overrides: Mapping[str, bytes] | None = None,
) -> tuple[bool, Checks]:
    source = read_sources(overrides)
    checks = Checks()
    check_historic_table(checks)
    check_live_hashes(checks, source)
    check_note_boundaries(checks, source)
    check_admission_certificate(checks, source)
    check_omega_scope(checks, source)
    check_scalar_scope(checks, source)
    check_lean_scope(checks, source)
    return not checks.failures, checks


def tamper_selftest() -> tuple[bool, int, int]:
    normal_ok, _ = run_checks()
    caught = 0

    source = read_sources()
    changed = source[RANK_ONE_ARITHMETIC] + b"\n"
    caught += int(
        normal_ok and not source_pin_matches(RANK_ONE_ARITHMETIC, changed)
    )

    restored = (
        decode(source, OMEGA_FLOOR)
        + "\n"
        + HISTORIC_EVIDENCE[OMEGA_FLOOR]["stale_excerpts"][0]
        + "\n"
    )
    caught += int(normal_ok and not stale_absent(OMEGA_FLOOR, restored))

    unscoped = (
        decode(source, OMEGA_FLOOR)
        + "\nHierarchy pieces are paid in full.\n"
    )
    caught += int(normal_ok and not unscoped_absent(OMEGA_FLOOR, unscoped))

    certificate = json.loads(decode(source, ADMISSION_CERT))
    promoted = copy.deepcopy(certificate)
    promoted["status"]["rank_one_profile_payment"] = "PROVED"
    caught += int(normal_ok and not target_profile_status_ok(promoted))

    caught += int(
        normal_ok and not historic_table_ok(upstream="0" * 40)
    )

    historic = copy.deepcopy(HISTORIC_EVIDENCE)
    integrations = dict(INTEGRATION_COMMITS)
    historic[RANK_ONE_ARITHMETIC]["producer_pr"] = 1818
    integrations[1818] = integrations.pop(818)
    caught += int(
        normal_ok
        and not historic_table_ok(
            evidence=historic, integrations=integrations
        )
    )

    historic = copy.deepcopy(HISTORIC_EVIDENCE)
    historic[OMEGA_FLOOR]["producer_head"] = "0" * 40
    caught += int(normal_ok and not historic_table_ok(evidence=historic))

    historic = copy.deepcopy(HISTORIC_EVIDENCE)
    historic[SHELL_LAW]["blob_sha1"] = "0" * 40
    caught += int(normal_ok and not historic_table_ok(evidence=historic))

    historic = copy.deepcopy(HISTORIC_EVIDENCE)
    historic[PRODUCT_TRANSFER]["sha256"] = "0" * 64
    caught += int(normal_ok and not historic_table_ok(evidence=historic))

    historic = copy.deepcopy(HISTORIC_EVIDENCE)
    historic[ADMISSION_AUDIT]["stale_excerpts"] = (
        "absent byte-exact historic excerpt",
    )
    caught += int(normal_ok and not historic_table_ok(evidence=historic))

    total = 10
    return normal_ok and caught == total, caught, total


def print_failures(checks: Checks) -> None:
    for failure in checks.failures:
        print(f"FAIL: {failure}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="reject live, prose, status, and historic-pin corruption",
    )
    args = parser.parse_args()

    if args.tamper_selftest:
        ok, caught, total = tamper_selftest()
        print(
            f"TAMPER SELFTEST: {'PASS' if ok else 'FAIL'} "
            f"({caught}/{total} caught)"
        )
        print("STATUS: COUNTEREXAMPLE")
        return 0 if ok else 1

    ok, checks = run_checks()
    print(
        f"RESULT: {'PASS' if ok else 'FAIL'} "
        f"({checks.passed}/{checks.total})"
    )
    print("STATUS: COUNTEREXAMPLE")
    if not ok:
        print_failures(checks)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
