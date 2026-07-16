#!/usr/bin/env python3
"""Replay the rank-15 exact two-flat final-41 source certificate.

Standard library only.  Every gate uses explicit exceptions, so ``python -O``
cannot remove a verification check.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, replace
import hashlib
import json
from pathlib import Path
import string
import sys
from typing import Any, Callable, NoReturn


HERE = Path(__file__).resolve().parent
CERTIFICATE_PATH = HERE / "certificate.json"
EXPECTED_OUTPUT_PATH = HERE / "verifier_output.txt"
TAMPER_OUTPUT_PATH = HERE / "tamper_output.txt"
MANIFEST_PATH = HERE / "SHA256SUMS.txt"

EXPECTED_CERTIFICATE_SHA256 = "493e24507abd11a0b65991019a33e6b39eb35227ce13db38cb99865633adf730"
EXPECTED_OUTPUT_SHA256 = "508de3ff9e7335f707c588a4485b0d78294682432b6ceb39bf0adba110dbcd43"
EXPECTED_TAMPER_OUTPUT_SHA256 = "a906161ea97994ca7d11f4d40cb5f3bb9995f15866a4a8f7555aebffc146787b"
EXPECTED_MANIFEST_FILES = frozenset(
    {
        "README.md",
        "certificate.json",
        "tamper_output.txt",
        "verifier_output.txt",
        "verify_rank15_two_flat_final41_source_cap.py",
    }
)


class VerificationError(RuntimeError):
    """Raised when any certificate, parser, or frozen-artifact gate fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_json_constant(value: str) -> NoReturn:
    raise VerificationError(f"non-finite JSON constant rejected: {value}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str, "JSON object key is not a string")
        require(key not in result, f"duplicate JSON key rejected: {key}")
        result[key] = value
    return result


def strict_json_loads(payload: str) -> Any:
    try:
        return json.loads(
            payload,
            object_pairs_hook=unique_object,
            parse_constant=reject_json_constant,
        )
    except VerificationError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise VerificationError(f"invalid JSON rejected: {exc}") from exc


def require_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    require(type(value) is dict, f"{label} must be an object")
    actual = set(value)
    require(actual == expected, f"{label} keys changed: {sorted(actual)}")
    return value


def require_int(value: Any, label: str) -> int:
    require(type(value) is int, f"{label} must be an integer, not {type(value).__name__}")
    return value


def require_nonnegative_int(value: Any, label: str) -> int:
    result = require_int(value, label)
    require(result >= 0, f"{label} must be nonnegative")
    return result


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def c2(value: int) -> int:
    return value * (value - 1) // 2


@dataclass(frozen=True, slots=True)
class Parameters:
    p: int
    n: int
    K: int
    m: int
    list_size: int
    section_cap: int


@dataclass(frozen=True, slots=True)
class Claim:
    u_min: int
    u_max: int
    bound: int
    boundary_u: int
    boundary_margin: int
    source_interval_min: int
    expected_margins: tuple[tuple[int, int], ...]


@dataclass(frozen=True, slots=True)
class LocalCut:
    name: str
    target: int
    constant: int
    charges: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class Certificate:
    schema: str
    parameters: Parameters
    claim: Claim
    pair_budget: int
    mod13_budget: int
    gamma: tuple[int, ...]
    local_cuts: tuple[LocalCut, ...]


@dataclass(frozen=True, slots=True)
class CutAudit:
    name: str
    cases: int
    minimum_slack: int
    witness: int


@dataclass(frozen=True, slots=True)
class OptimizerAudit:
    cache: dict[tuple[int, int], int]
    branches_checked: int
    balanced_successors_rejected: int


@dataclass(frozen=True, slots=True)
class Replay:
    margins: dict[int, int]
    first_closed: int
    closed_count: int
    f_min: int
    f_max: int
    optimizer: OptimizerAudit


def parse_certificate_data(raw: Any) -> Certificate:
    root = require_keys(
        raw,
        {"schema", "parameters", "claim", "budgets", "gamma", "local_cuts"},
        "certificate",
    )
    require(
        root["schema"] == "rank15-two-flat-final41-source-cap-v1",
        "certificate schema changed",
    )

    parameter_raw = require_keys(
        root["parameters"],
        {"p", "n", "K", "m", "list_size", "section_cap"},
        "parameters",
    )
    parameters = Parameters(
        **{
            key: require_int(parameter_raw[key], f"parameters.{key}")
            for key in ("p", "n", "K", "m", "list_size", "section_cap")
        }
    )
    require(
        parameters == Parameters(2_130_706_433, 2_097_152, 1_048_576, 1_116_047, 212, 15),
        "deployed parameter interface changed",
    )

    claim_raw = require_keys(
        root["claim"],
        {
            "u_min",
            "u_max",
            "bound",
            "boundary_u",
            "boundary_margin",
            "source_interval_min",
            "expected_margins",
        },
        "claim",
    )
    expected_margins_raw = claim_raw["expected_margins"]
    require(type(expected_margins_raw) is list, "expected_margins must be a list")
    expected_margins: list[tuple[int, int]] = []
    for index, row in enumerate(expected_margins_raw):
        require(type(row) is list and len(row) == 2, f"margin row {index} malformed")
        expected_margins.append(
            (
                require_int(row[0], f"margin[{index}].u"),
                require_int(row[1], f"margin[{index}].value"),
            )
        )
    claim = Claim(
        u_min=require_int(claim_raw["u_min"], "claim.u_min"),
        u_max=require_int(claim_raw["u_max"], "claim.u_max"),
        bound=require_int(claim_raw["bound"], "claim.bound"),
        boundary_u=require_int(claim_raw["boundary_u"], "claim.boundary_u"),
        boundary_margin=require_int(claim_raw["boundary_margin"], "claim.boundary_margin"),
        source_interval_min=require_int(
            claim_raw["source_interval_min"], "claim.source_interval_min"
        ),
        expected_margins=tuple(expected_margins),
    )
    require(
        (
            claim.u_min,
            claim.u_max,
            claim.bound,
            claim.boundary_u,
            claim.boundary_margin,
            claim.source_interval_min,
        )
        == (1_043_917, 1_043_957, 211, 1_043_916, 878, 1_043_592),
        "accepted theorem boundary changed",
    )
    require(
        tuple(u for u, _ in claim.expected_margins)
        == tuple(range(claim.u_min, claim.u_max + 1)),
        "expected margin states are not the exact contiguous claim interval",
    )

    budget_raw = require_keys(root["budgets"], {"pair", "mod13"}, "budgets")
    pair_budget = require_nonnegative_int(budget_raw["pair"], "budgets.pair")
    mod13_budget = require_nonnegative_int(budget_raw["mod13"], "budgets.mod13")
    require(pair_budget == c2(parameters.list_size), "pair budget is not C(212,2)")
    require(mod13_budget == 41_340, "mod-13 budget changed")

    gamma_raw = root["gamma"]
    require(type(gamma_raw) is list and len(gamma_raw) == 16, "gamma must have 16 entries")
    gamma = tuple(
        require_nonnegative_int(value, f"gamma[{index}]")
        for index, value in enumerate(gamma_raw)
    )

    cuts_raw = root["local_cuts"]
    require(type(cuts_raw) is list and len(cuts_raw) == 3, "local_cuts must have 3 entries")
    cuts: list[LocalCut] = []
    for index, item in enumerate(cuts_raw):
        cut_raw = require_keys(
            item, {"name", "target", "constant", "charges"}, f"local_cuts[{index}]"
        )
        require(type(cut_raw["name"]) is str, f"local_cuts[{index}].name must be text")
        charges_raw = cut_raw["charges"]
        require(
            type(charges_raw) is list and len(charges_raw) == 16,
            f"local_cuts[{index}].charges must have 16 entries",
        )
        cuts.append(
            LocalCut(
                name=cut_raw["name"],
                target=require_int(cut_raw["target"], f"local_cuts[{index}].target"),
                constant=require_nonnegative_int(
                    cut_raw["constant"], f"local_cuts[{index}].constant"
                ),
                charges=tuple(
                    require_nonnegative_int(value, f"local_cuts[{index}].charges[{j}]")
                    for j, value in enumerate(charges_raw)
                ),
            )
        )
    local_cuts = tuple(cuts)
    require(
        tuple((cut.name, cut.target) for cut in local_cuts)
        == (("cut_a", 15), ("cut_b", 14), ("cut_c", 15)),
        "local-cut identities changed",
    )
    for h in range(4, 14):
        require(
            local_cuts[0].charges[h] == local_cuts[1].charges[h] == c2(h - 2),
            f"common cut-1 charge changed at h={h}",
        )
    require(local_cuts[2].charges == gamma, "cut_c and gamma differ")
    require(all(value == 0 for value in gamma[:4]), "gamma must vanish below occupancy 4")

    return Certificate(
        schema=root["schema"],
        parameters=parameters,
        claim=claim,
        pair_budget=pair_budget,
        mod13_budget=mod13_budget,
        gamma=gamma,
        local_cuts=local_cuts,
    )


def load_certificate() -> tuple[Certificate, dict[str, Any], str]:
    payload = CERTIFICATE_PATH.read_bytes()
    digest = sha256_bytes(payload)
    require(digest == EXPECTED_CERTIFICATE_SHA256, "certificate SHA-256 mismatch")
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("certificate is not ASCII") from exc
    raw = strict_json_loads(text)
    certificate = parse_certificate_data(raw)
    require(type(raw) is dict, "parsed certificate root changed type")
    return certificate, raw, digest


def verify_manifest() -> int:
    try:
        lines = MANIFEST_PATH.read_text(encoding="ascii").splitlines()
    except (OSError, UnicodeError) as exc:
        raise VerificationError(f"cannot read checksum manifest: {exc}") from exc
    entries: dict[str, str] = {}
    hexdigits = set(string.hexdigits.lower())
    for index, line in enumerate(lines, start=1):
        require(len(line) >= 67 and line[64:66] == "  ", f"manifest line {index} malformed")
        digest = line[:64]
        name = line[66:]
        require(
            len(digest) == 64 and set(digest) <= hexdigits and digest == digest.lower(),
            f"manifest digest {index} malformed",
        )
        require(name and "/" not in name and "\\" not in name, f"manifest name {index} unsafe")
        require(name not in entries, f"duplicate manifest entry: {name}")
        entries[name] = digest
    require(set(entries) == EXPECTED_MANIFEST_FILES, "manifest file set changed")
    for name, expected in entries.items():
        actual = sha256_bytes((HERE / name).read_bytes())
        require(actual == expected, f"manifest checksum mismatch: {name}")
    return len(entries)


def rank_one_bound(parameters: Parameters, lower_universal: int) -> tuple[int, int, int, int]:
    best = -1
    first = -1
    last = -1
    count = 0
    for actual_u in range(lower_universal, parameters.K):
        numerator = (parameters.n - actual_u) * (parameters.m - parameters.K + 1)
        denominator = (parameters.m - actual_u) ** 2 - (
            parameters.n - actual_u
        ) * (parameters.K - 1 - actual_u)
        incidence = (parameters.n - actual_u) // (parameters.m - actual_u)
        johnson = numerator // denominator if denominator > 0 else 10**100
        value = min(incidence, johnson)
        if value > best:
            best = value
            first = last = actual_u
            count = 1
        elif value == best:
            last = actual_u
            count += 1
    require(best >= 0, "rank-one recurrence scanned an empty range")
    return best, first, last, count


def verify_section_cap(certificate: Certificate) -> tuple[int, int, int, int]:
    p = certificate.parameters
    first_result = rank_one_bound(p, certificate.claim.u_min + 1)
    require(first_result[0] == p.section_cap, "lower-endpoint rank-one cap changed")
    for u in range(certificate.claim.u_min, certificate.claim.u_max + 1):
        value, _, _, _ = rank_one_bound(p, u + 1)
        require(value <= p.section_cap, f"proper-section cap failed at u={u}")
    return first_result


def verify_local_cut(cut: LocalCut, list_size: int) -> CutAudit:
    require(2 <= cut.target <= 15, f"{cut.name}: invalid target")
    target_weight = cut.target - 1
    cases = 0
    minimum_slack: int | None = None
    witness = -1
    distinguished = 0
    while distinguished * target_weight <= list_size - 1:
        remaining = list_size - 1 - distinguished * target_weight
        dp = [0] * (remaining + 1)
        for capacity in range(1, remaining + 1):
            best = dp[capacity - 1]
            for h in range(2, 16):
                if h == cut.target:
                    continue
                weight = h - 1
                if weight <= capacity:
                    best = max(best, dp[capacity - weight] + cut.charges[h])
            dp[capacity] = best
        maximum_charge = cut.charges[cut.target] * distinguished + dp[remaining]
        allowance = c2(distinguished) + cut.constant
        slack = allowance - maximum_charge
        require(slack >= 0, f"{cut.name}: local cut failed at distinguished={distinguished}")
        if minimum_slack is None or slack < minimum_slack:
            minimum_slack = slack
            witness = distinguished
        cases += 1
        distinguished += 1
    require(minimum_slack is not None, f"{cut.name}: no cases checked")
    return CutAudit(cut.name, cases, minimum_slack, witness)


def pair_cost(h: int) -> int:
    return c2(h)


def mod13_cost(h: int) -> int:
    return 0 if h <= 2 else h * (h - 2)


def cut1_cost(h: int) -> int:
    return h * c2(h - 2) if 4 <= h <= 13 else 0


def cut2_cost(h: int, gamma: tuple[int, ...]) -> int:
    return h * gamma[h] if 4 <= h <= 13 else 0


def resource_costs(h: int, gamma: tuple[int, ...]) -> tuple[int, int, int, int]:
    return pair_cost(h), mod13_cost(h), cut1_cost(h), cut2_cost(h, gamma)


def verify_discrete_convexity(gamma: tuple[int, ...]) -> None:
    previous = (-1, -1, -1, -1)
    for h in range(1, 13):
        current = tuple(
            right - left
            for left, right in zip(resource_costs(h, gamma), resource_costs(h + 1, gamma))
        )
        require(all(value >= 0 for value in current), f"negative upgrade cost at h={h}")
        require(
            all(a <= b for a, b in zip(previous, current)),
            f"resource increments are not componentwise nondecreasing at h={h}",
        )
        previous = current


def balanced_resource_costs(
    count: int,
    base_h: int,
    upgrades: int,
    gamma: tuple[int, ...],
) -> tuple[int, int, int, int]:
    if count == 0:
        require(upgrades == 0, "zero-count balanced vector has upgrades")
        return (0, 0, 0, 0)
    maximum = count * (13 - base_h)
    require(0 <= upgrades <= maximum, "balanced upgrade count out of range")
    layers, partial = divmod(upgrades, count)
    low_h = base_h + layers
    high_h = low_h + 1
    require(low_h <= 13 and (partial == 0 or high_h <= 13), "balanced occupancy exceeds 13")
    low_cost = resource_costs(low_h, gamma)
    high_cost = resource_costs(high_h, gamma) if partial else low_cost
    return tuple(
        (count - partial) * a + partial * b for a, b in zip(low_cost, high_cost)
    )


def common_lower_budget(certificate: Certificate, n15: int, n14: int) -> int:
    cut_a, cut_b, _ = certificate.local_cuts
    m = certificate.parameters.list_size
    from_15 = (
        c2(n15)
        + m * cut_a.constant
        - cut_a.charges[15] * 15 * n15
        - cut_a.charges[14] * 14 * n14
    )
    from_14 = (
        c2(n14)
        + m * cut_b.constant
        - cut_b.charges[15] * 15 * n15
        - cut_b.charges[14] * 14 * n14
    )
    return min(from_15, from_14)


def second_lower_budget(certificate: Certificate, n15: int, n14: int) -> int:
    cut_c = certificate.local_cuts[2]
    m = certificate.parameters.list_size
    return (
        c2(n15)
        + m * cut_c.constant
        - cut_c.charges[15] * 15 * n15
        - cut_c.charges[14] * 14 * n14
    )


def optimize_full_directions(
    f: int,
    residual_h: int,
    certificate: Certificate,
) -> tuple[int, int, int]:
    # These short tables keep the literal 6.6-million-branch enumeration
    # practical in Python without changing the C++ optimizer's search space.
    pair_table = tuple(pair_cost(h) for h in range(16))
    mod13_table = tuple(mod13_cost(h) for h in range(16))
    cut1_table = tuple(cut1_cost(h) for h in range(16))
    cut2_table = tuple(cut2_cost(h, certificate.gamma) for h in range(16))
    resource_tables = (pair_table, mod13_table, cut1_table, cut2_table)
    increments = tuple(
        tuple(table[h + 1] - table[h] for table in resource_tables)
        for h in range(13)
    )

    residual_cost = tuple(table[residual_h] for table in resource_tables)
    residual_15 = int(residual_h == 15)
    residual_14 = int(residual_h == 14)
    list_size = certificate.parameters.list_size
    pair_budget = certificate.pair_budget
    mod13_budget = certificate.mod13_budget
    cut_a, cut_b, cut_c = certificate.local_cuts
    a15, a14 = cut_a.charges[15], cut_a.charges[14]
    b15, b14 = cut_b.charges[15], cut_b.charges[14]
    c15, c14 = cut_c.charges[15], cut_c.charges[14]
    best = -1
    branches = 0
    successors_rejected = 0

    for full_15 in range(f + 1):
        for full_14 in range(f - full_15 + 1):
            branches += 1
            n15 = full_15 + residual_15
            n14 = full_14 + residual_14
            n15_pairs = n15 * (n15 - 1) // 2
            n14_pairs = n14 * (n14 - 1) // 2
            from_15 = (
                n15_pairs
                + list_size * cut_a.constant
                - a15 * 15 * n15
                - a14 * 14 * n14
            )
            from_14 = (
                n14_pairs
                + list_size * cut_b.constant
                - b15 * 15 * n15
                - b14 * 14 * n14
            )
            cut1_budget = min(from_15, from_14)
            cut2_budget = (
                n15_pairs
                + list_size * cut_c.constant
                - c15 * 15 * n15
                - c14 * 14 * n14
            )
            if cut1_budget < 0 or cut2_budget < 0:
                continue

            fixed_pair = residual_cost[0] + 105 * full_15 + 91 * full_14
            fixed_mod13 = residual_cost[1] + 195 * full_15 + 168 * full_14
            if fixed_pair > pair_budget or fixed_mod13 > mod13_budget:
                continue

            low = f - full_15 - full_14
            if residual_h >= 14 and low != 0:
                continue
            budgets = (
                pair_budget - fixed_pair,
                mod13_budget - fixed_mod13,
                cut1_budget - residual_cost[2],
                cut2_budget - residual_cost[3],
            )
            if budgets[2] < 0 or budgets[3] < 0:
                continue

            if low == 0:
                low_incidence = 0
            else:
                remaining = [
                    budget - low * cost for budget, cost in zip(budgets, residual_cost)
                ]
                if (
                    remaining[0] < 0
                    or remaining[1] < 0
                    or remaining[2] < 0
                    or remaining[3] < 0
                ):
                    continue
                upgrades = 0
                for h in range(residual_h, 13):
                    step = increments[h]
                    number = low
                    for index, increment in enumerate(step):
                        if increment:
                            number = min(number, remaining[index] // increment)
                    upgrades += number
                    for index, increment in enumerate(step):
                        remaining[index] -= number * increment
                    if number < low:
                        break
                low_incidence = low * residual_h + upgrades

                layers, partial = divmod(upgrades, low)
                balanced_h = residual_h + layers
                balanced = tuple(
                    (low - partial) * table[balanced_h]
                    + partial * table[balanced_h + 1]
                    for table in resource_tables
                )
                require(
                    all(cost <= budget for cost, budget in zip(balanced, budgets)),
                    "greedy layer result is not feasible",
                )
                maximum_upgrades = low * (13 - residual_h)
                if upgrades < maximum_upgrades:
                    next_layers, next_partial = divmod(upgrades + 1, low)
                    next_h = residual_h + next_layers
                    successor = tuple(
                        (low - next_partial) * table[next_h]
                        + next_partial * table[next_h + 1]
                        for table in resource_tables
                    )
                    require(
                        any(cost > budget for cost, budget in zip(successor, budgets)),
                        "balanced one-unit successor remained feasible",
                    )
                    successors_rejected += 1

            full_incidence = 15 * full_15 + 14 * full_14 + low_incidence
            best = max(best, full_incidence)

    require(best >= 0, f"no relaxed pattern for f={f}, residual_h={residual_h}")
    return best, branches, successors_rejected


def build_optimizer_cache(certificate: Certificate) -> OptimizerAudit:
    verify_discrete_convexity(certificate.gamma)
    cache: dict[tuple[int, int], int] = {}
    branches = 0
    successors = 0
    for f in range(211, 229):
        for residual_h in range(1, 16):
            best, checked, rejected = optimize_full_directions(f, residual_h, certificate)
            cache[(f, residual_h)] = best
            branches += checked
            successors += rejected
    require(len(cache) == 270, "optimizer cache size changed")
    return OptimizerAudit(cache, branches, successors)


def replay_margins(certificate: Certificate) -> Replay:
    p = certificate.parameters
    optimizer = build_optimizer_cache(certificate)
    margins: dict[int, int] = {}
    observed_f: list[int] = []
    for u in range(certificate.claim.source_interval_min, certificate.claim.u_max + 1):
        residual_n = p.n - u
        degree = p.K - 1 - u
        agreement = p.m - u
        require(degree > 0 and agreement > 0, f"invalid residual state u={u}")
        f, residual_weight = divmod(residual_n, degree)
        require(0 < residual_weight < degree, f"non-strict residual weight at u={u}")
        require((f, 1) in optimizer.cache, f"optimizer cache misses f={f}")
        observed_f.append(f)
        capacity = max(
            degree * optimizer.cache[(f, residual_h)] + residual_weight * residual_h
            for residual_h in range(1, 16)
        )
        margins[u] = capacity - p.list_size * agreement

    negative_states = [u for u in sorted(margins) if margins[u] < 0]
    require(negative_states, "no closed child state found")
    first_closed = negative_states[0]
    closed_count = sum(
        margins[u] < 0
        for u in range(certificate.claim.u_min, certificate.claim.u_max + 1)
    )
    return Replay(
        margins=margins,
        first_closed=first_closed,
        closed_count=closed_count,
        f_min=min(observed_f),
        f_max=max(observed_f),
        optimizer=optimizer,
    )


def verify_claim_interval(claim: Claim, margins: dict[int, int]) -> None:
    for u in range(claim.u_min, claim.u_max + 1):
        require(u in margins, f"claimed state not replayed: u={u}")
        require(margins[u] < 0, f"claimed state is not closed: u={u}, margin={margins[u]:+d}")


def verify_replay(certificate: Certificate, replay: Replay) -> None:
    claim = certificate.claim
    require(replay.f_min == 211 and replay.f_max == 228, "observed f range changed")
    require(replay.first_closed == claim.u_min, "first closed endpoint changed")
    require(replay.closed_count == claim.u_max - claim.u_min + 1 == 41, "closed count changed")
    require(replay.margins[claim.boundary_u] == claim.boundary_margin, "boundary margin changed")
    verify_claim_interval(claim, replay.margins)
    actual = tuple((u, replay.margins[u]) for u in range(claim.u_min, claim.u_max + 1))
    require(actual == claim.expected_margins, "claimed margin table changed")


def render_main(certificate: Certificate, certificate_sha256: str) -> str:
    section_cap, cap_first, cap_last, cap_count = verify_section_cap(certificate)
    cut_audits = tuple(
        verify_local_cut(cut, certificate.parameters.list_size)
        for cut in certificate.local_cuts
    )
    replay = replay_margins(certificate)
    verify_replay(certificate, replay)

    lines = [
        "RANK15_TWO_FLAT_FINAL41_SOURCE_CAP",
        f"certificate_sha256={certificate_sha256}",
        "parameters="
        f"p{certificate.parameters.p},n{certificate.parameters.n},K{certificate.parameters.K},"
        f"m{certificate.parameters.m},M{certificate.parameters.list_size}",
        f"section_cap=F_m1({certificate.claim.u_min + 1})={section_cap};"
        f"maximizers={cap_first}..{cap_last};count={cap_count}",
    ]
    for audit in cut_audits:
        lines.append(
            f"local_cut={audit.name};cases={audit.cases};"
            f"minimum_slack={audit.minimum_slack};witness={audit.witness}"
        )
    lines.extend(
        [
            "discrete_convex_exchange=PASS;resources=4;occupancies=1..13",
            f"optimizer_cache={len(replay.optimizer.cache)};f={replay.f_min}..{replay.f_max};"
            f"branches={replay.optimizer.branches_checked};"
            f"successors_rejected={replay.optimizer.balanced_successors_rejected}",
            f"BOUNDARY u={certificate.claim.boundary_u} margin={certificate.claim.boundary_margin:+d} OPEN",
        ]
    )
    lines.extend(
        f"MARGIN u={u} margin={replay.margins[u]:+d}"
        for u in range(certificate.claim.u_min, certificate.claim.u_max + 1)
    )
    lines.extend(
        [
            f"FIRST_CLOSED={replay.first_closed}",
            f"CLOSED_COUNT={replay.closed_count}",
            f"REPLACEMENT=D2[{certificate.claim.u_min}..{certificate.claim.u_max}]<={certificate.claim.bound}",
            f"UNRESOLVED={certificate.claim.source_interval_min}..{certificate.claim.boundary_u};count=325",
            "NONCLAIMS=parent_recurrence,366_child_closure,arrangement_transport,rank16,Grand_List,Grand_MCA,score_movement",
            "RESULT: PASS",
        ]
    )
    return "\n".join(lines) + "\n"


def expect_rejected(label: str, action: Callable[[], Any]) -> str:
    try:
        action()
    except VerificationError as exc:
        return f"TAMPER {label}: REJECTED ({exc})"
    raise VerificationError(f"tamper was accepted: {label}")


def replace_cut_charge(cut: LocalCut, index: int, delta: int) -> LocalCut:
    charges = list(cut.charges)
    charges[index] += delta
    return replace(cut, charges=tuple(charges))


def render_tamper(certificate: Certificate, raw: dict[str, Any]) -> str:
    replay = replay_margins(certificate)
    verify_replay(certificate, replay)
    lines: list[str] = ["RANK15_TWO_FLAT_FINAL41_TAMPER_SELFTEST"]

    extended_claim = replace(certificate.claim, u_min=certificate.claim.boundary_u)
    lines.append(
        expect_rejected(
            "boundary_u_min_1043916",
            lambda: verify_claim_interval(extended_claim, replay.margins),
        )
    )

    coefficient_mutations = (
        ("cut_a_h15_plus_1", 0, 15),
        ("cut_b_h14_plus_1", 1, 14),
        ("cut_c_h15_plus_1", 2, 15),
    )
    for label, cut_index, charge_index in coefficient_mutations:
        mutated = replace_cut_charge(certificate.local_cuts[cut_index], charge_index, 1)
        lines.append(
            expect_rejected(
                label,
                lambda mutated=mutated: verify_local_cut(
                    mutated, certificate.parameters.list_size
                ),
            )
        )

    lines.append(
        expect_rejected(
            "parser_duplicate_key",
            lambda: strict_json_loads('{"schema":"a","schema":"b"}'),
        )
    )

    unknown = deepcopy(raw)
    unknown["unexpected"] = 1
    lines.append(
        expect_rejected("parser_unknown_field", lambda: parse_certificate_data(unknown))
    )

    floating = deepcopy(raw)
    floating["parameters"]["n"] = 2_097_152.0
    lines.append(
        expect_rejected("parser_float_integer", lambda: parse_certificate_data(floating))
    )

    boolean = deepcopy(raw)
    boolean["parameters"]["section_cap"] = True
    lines.append(
        expect_rejected("parser_bool_integer", lambda: parse_certificate_data(boolean))
    )

    lines.append(
        expect_rejected(
            "parser_nonfinite_constant",
            lambda: strict_json_loads('{"value":NaN}'),
        )
    )
    lines.append("TAMPER_RESULT: PASS")
    return "\n".join(lines) + "\n"


def emit_frozen(rendered: str, path: Path, expected_sha256: str) -> None:
    payload = rendered.encode("ascii")
    frozen = path.read_bytes()
    require(sha256_bytes(frozen) == expected_sha256, f"frozen output hash changed: {path.name}")
    require(payload == frozen, f"replayed output differs from frozen file: {path.name}")
    sys.stdout.buffer.write(payload)


def main(argv: list[str]) -> int:
    try:
        certificate, raw, certificate_sha256 = load_certificate()
        verify_manifest()
        if not argv:
            emit_frozen(
                render_main(certificate, certificate_sha256),
                EXPECTED_OUTPUT_PATH,
                EXPECTED_OUTPUT_SHA256,
            )
        elif argv == ["--tamper-selftest"]:
            emit_frozen(
                render_tamper(certificate, raw),
                TAMPER_OUTPUT_PATH,
                EXPECTED_TAMPER_OUTPUT_SHA256,
            )
        else:
            raise VerificationError(f"unsupported arguments: {argv}")
    except (OSError, VerificationError) as exc:
        print(f"VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
