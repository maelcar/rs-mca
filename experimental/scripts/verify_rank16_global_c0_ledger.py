#!/usr/bin/env python3
"""Exact replay for the rank-16 global c=0 first-match ledger.

Python 3 standard library only.  This verifier checks:
  * the deployed denominator compiler and target;
  * the canonical agreement-side owner;
  * the exact 110-profile nested-pattern owner already integrated on main;
  * the joint mixed complete-error-shadow owner;
  * disjoint first-match arithmetic and the 1,682 remaining profiles;
  * the first unpaid q64 cell and its exact zero-reserve suffix threshold;
  * the uniform fixed-27-core and fixed-26-core incidence transitions;
  * optional byte-level verification of the supplied archive source manifest.

It deliberately proves arithmetic/certificate obligations only.  The theorem
proof explaining why the combinatorial inequalities apply is supplied in the
accompanying response/README.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from dataclasses import dataclass, replace
from math import comb
from pathlib import Path
from typing import Iterable


P = 2_130_706_433
N = 2_097_152
K = 1_048_576
M = 1_116_047
U = 1_043_459
TARGET_EXPECTED = 274_854_110_496_187_592
PATTERN_REFERENCE_CAP = 121_502_836_610_262


class VerificationError(RuntimeError):
    """Raised when an exact certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


@dataclass(frozen=True)
class ReplayParameters:
    p: int = P
    n: int = N
    k: int = K
    m: int = M
    u: int = U
    target_shift: int = 0
    delta_shift: int = 0
    q64_blocks: int = 64
    residual_e16_max: int = 15
    fixed27_incidence: int = 28
    fixed26_incidence: int = 378
    first_match: bool = True


def archive_manifest_audit(archive_root: Path) -> dict[str, int]:
    manifest = archive_root / "SOURCE_SHA256SUMS.txt"
    source_root = archive_root / "source"
    require(manifest.is_file(), "SOURCE_SHA256SUMS.txt is missing")
    require(source_root.is_dir(), "source directory is missing")

    listed: dict[str, str] = {}
    for line_number, raw in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        pieces = line.split(maxsplit=1)
        require(len(pieces) == 2, f"malformed manifest line {line_number}")
        digest, rel = pieces
        rel = rel.lstrip("*")
        require(rel.startswith("source/"), f"non-source manifest path at line {line_number}")
        require(rel not in listed, f"duplicate manifest path: {rel}")
        listed[rel] = digest.lower()

    actual_paths = sorted(
        str(path.relative_to(archive_root)).replace("\\", "/")
        for path in source_root.rglob("*")
        if path.is_file()
    )
    require(set(actual_paths) == set(listed), "manifest/source file-set mismatch")

    total_bytes = 0
    total_lines = 0
    for rel in actual_paths:
        data = (archive_root / rel).read_bytes()
        actual_digest = hashlib.sha256(data).hexdigest()
        require(actual_digest == listed[rel], f"SHA-256 mismatch: {rel}")
        total_bytes += len(data)
        # splitlines() matches the complete-read line inventory, including a
        # final unterminated line if one is present.
        total_lines += len(data.decode("utf-8", errors="strict").splitlines())

    require(len(actual_paths) == 89, "unexpected authoritative source-file count")
    require(total_bytes == 1_222_183, "unexpected authoritative source-byte count")
    require(total_lines == 30_522, "unexpected authoritative source-line count")
    return {
        "source_files": len(actual_paths),
        "source_bytes": total_bytes,
        "source_lines": total_lines,
        "manifest_matches": len(actual_paths),
    }


def enumerate_profiles(e16_max: int) -> list[tuple[int, int, int, int, int, int]]:
    """Enumerate all residual nested profiles in canonical lexicographic order."""
    profiles: list[tuple[int, int, int, int, int, int]] = []
    for e20 in range(0, 0 + 1):
        for e19 in range(2 * e20, 1 + 1):
            for e18 in range(2 * e19, 3 + 1):
                for e17 in range(2 * e18, 7 + 1):
                    for e16 in range(2 * e17, e16_max + 1):
                        for e15 in range(2 * e16, 32 + 1):
                            profile = (e15, e16, e17, e18, e19, e20)
                            require(
                                profile[0] >= 2 * profile[1]
                                and profile[1] >= 2 * profile[2]
                                and profile[2] >= 2 * profile[3]
                                and profile[3] >= 2 * profile[4]
                                and profile[4] >= 2 * profile[5],
                                f"invalid nested profile generated: {profile}",
                            )
                            profiles.append(profile)
    return profiles


def profile_stream(profiles: Iterable[tuple[int, int, int, int, int, int]]) -> bytes:
    return "".join(
        ",".join(str(value) for value in profile) + "\n" for profile in profiles
    ).encode("ascii")


def nested_pattern_payment() -> dict[str, object]:
    """Reconstruct the integrated exact payment for 110 e15=32 profiles."""
    # A state is (leaf weight, all-one counts at sizes 2,4,...,2^height).
    # Ordered children retain literal 64-leaf fiber patterns.
    states: dict[tuple[int, tuple[int, ...]], int] = {
        (0, ()): 1,
        (1, ()): 1,
    }
    for height in range(1, 7):
        size = 1 << height
        nxt: defaultdict[tuple[int, tuple[int, ...]], int] = defaultdict(int)
        for (left_weight, left_counts), left_number in states.items():
            for (right_weight, right_counts), right_number in states.items():
                weight = left_weight + right_weight
                counts = tuple(
                    a + b for a, b in zip(left_counts, right_counts)
                ) + (int(weight == size),)
                nxt[(weight, counts)] += left_number * right_number
        states = dict(nxt)

    weight32_total = sum(
        number for (weight, _), number in states.items() if weight == 32
    )
    require(weight32_total == comb(64, 32), "64-leaf weight-32 census")

    rows: list[tuple[tuple[int, int, int, int, int, int], int]] = []
    for (weight, counts), number in states.items():
        if weight != 32:
            continue
        e16, e17, e18, e19, e20, _e21 = counts
        if e16 <= 15 and e17 <= 7 and e18 <= 3 and e19 <= 1 and e20 == 0:
            rows.append(((32, e16, e17, e18, e19, e20), number))

    paid = [
        (profile, number)
        for profile, number in rows
        if number <= PATTERN_REFERENCE_CAP
    ]
    unpaid = [
        (profile, number)
        for profile, number in rows
        if number > PATTERN_REFERENCE_CAP
    ]
    return {
        "rows": rows,
        "paid": paid,
        "unpaid": unpaid,
        "paid_profiles": frozenset(profile for profile, _ in paid),
        "paid_total": sum(number for _, number in paid),
    }


def largest_x_with_phi_at_most_target(
    *, target: int, agreement_owner: int, shadow_universe: int, paired: int
) -> int:
    def phi(x: int) -> int:
        return agreement_owner + paired + x + (shadow_universe - paired - x) // 29

    lo = 0
    hi = shadow_universe - paired
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if phi(mid) <= target:
            lo = mid
        else:
            hi = mid - 1
    return lo


def replay(params: ReplayParameters = ReplayParameters()) -> dict[str, object]:
    p, n, k, m, u = params.p, params.n, params.k, params.m, params.u
    t = n - m
    target = TARGET_EXPECTED + params.target_shift

    p6 = p**6
    denominator = 2**128
    bstar, p6_remainder = divmod(p6, denominator)
    threshold_numerator = (bstar + 1) * (p - t)
    compiled_target = (threshold_numerator - 1) // p
    adjacent_gap_lower = threshold_numerator - p * compiled_target
    adjacent_gap_upper = p * (compiled_target + 1) - threshold_numerator

    b64 = 2**15
    b32 = 2**16
    n64 = params.q64_blocks
    n32 = 32
    h64 = (k - 1) // b64
    h32 = (k - 1) // b32

    agreement_e15_33 = comb(n64, h64 + 1) // comb(33, h64 + 1)
    johnson_ball_e15_34 = 1 + 34 * (n64 - 34)
    agreement_e15_34 = comb(n64, 34) // johnson_ball_e15_34
    agreement_e16_16 = comb(n32, h32 + 1) // comb(16, h32 + 1)
    agreement_owner = agreement_e15_33 + agreement_e15_34 + agreement_e16_16
    pattern = nested_pattern_payment()
    pattern_paid_profiles = pattern["paid_profiles"]
    require(isinstance(pattern_paid_profiles, frozenset), "pattern profile set")
    pattern_owner = int(pattern["paid_total"])

    delta = n - 2 * m + k - 1 + params.delta_shift
    s64 = delta // b64
    shadow_universe = comb(n64, s64 + 1)
    paired = comb(n32, 14)

    # The function z + floor((C-z)/29) is nondecreasing: if C-z has
    # residue 0 mod 29, the increment is 0; otherwise it is 1.
    joint_increment_residues = tuple(
        1 + ((residue - 1) // 29) - (residue // 29) for residue in range(29)
    )
    mixed_owner = paired + (shadow_universe - paired) // 29
    f29_only_cap = shadow_universe // 29
    nonpaired_direct_ceiling = shadow_universe - paired

    # First-match order: agreement owner, 110 exact profile cells, then the
    # mixed top-complement owner on the remaining family.
    global_paid = agreement_owner + pattern_owner + mixed_owner
    allowance = target - global_paid
    violation_residual = allowance + 1

    profiles = enumerate_profiles(params.residual_e16_max)
    profile_bytes = profile_stream(profiles)
    profile_digest = hashlib.sha256(profile_bytes).hexdigest()
    require(
        pattern_paid_profiles.issubset(set(profiles)),
        "paid profiles outside residual census",
    )
    remaining_profiles = [
        profile for profile in profiles if profile not in pattern_paid_profiles
    ]
    remaining_profile_bytes = profile_stream(remaining_profiles)
    remaining_profile_digest = hashlib.sha256(remaining_profile_bytes).hexdigest()
    uniform_profile_cap, allowance_remainder = divmod(
        allowance, len(remaining_profiles)
    )
    violation_quotient, violation_remainder = divmod(
        violation_residual, len(remaining_profiles)
    )
    forced_profile = (
        violation_residual + len(remaining_profiles) - 1
    ) // len(remaining_profiles)
    uniform_profile_total = (
        global_paid + len(remaining_profiles) * uniform_profile_cap
    )

    residual_after_28 = t - 28 * b64
    first_unpaid_footprint_min = n64 - 32
    first_unpaid_extra_touched_min = first_unpaid_footprint_min - 28
    first_unpaid_q32_complete_max = 13

    x_star = largest_x_with_phi_at_most_target(
        target=target,
        agreement_owner=agreement_owner + pattern_owner,
        shadow_universe=shadow_universe,
        paired=paired,
    )

    def phi_nonpaired(x: int) -> int:
        return (
            agreement_owner
            + pattern_owner
            + paired
            + x
            + (shadow_universe - paired - x) // 29
        )

    fixed27_core_count = comb(n64, 27)
    fixed26_core_count = comb(n64, 26)

    def r27(r: int) -> int:
        return (r * fixed27_core_count) // params.fixed27_incidence

    def r26(r: int) -> int:
        return (r * fixed26_core_count) // params.fixed26_incidence

    def phi_all_f28(x: int) -> int:
        return agreement_owner + pattern_owner + x + (shadow_universe - x) // 29

    fixed27_cap6 = r27(6)
    fixed27_cap7 = r27(7)
    fixed27_total6 = phi_nonpaired(fixed27_cap6)
    fixed27_total7 = phi_nonpaired(fixed27_cap7)

    fixed26_cap116 = r26(116)
    fixed26_cap117 = r26(117)
    fixed26_cap130 = r26(130)
    fixed26_total116 = phi_all_f28(fixed26_cap116)
    fixed26_total117 = phi_all_f28(fixed26_cap117)
    fixed26_total130 = phi_all_f28(fixed26_cap130)

    generator_degree = (m - u) - (k - u - 1)
    post_27_core_degree = t - 27 * b64
    post_28_fiber_degree = post_27_core_degree - b64
    pade_width = post_27_core_degree - generator_degree
    cross_roots_six = 6 * b64
    cross_degree_cap = 2 * post_27_core_degree
    degree_interval_multiples = tuple(
        multiple
        for multiple in range(0, post_27_core_degree + b64, b64)
        if generator_degree <= multiple <= post_27_core_degree
    )

    return {
        "params": params,
        "p6": p6,
        "denominator": denominator,
        "bstar": bstar,
        "p6_remainder": p6_remainder,
        "compiled_target": compiled_target,
        "target": target,
        "adjacent_gap_lower": adjacent_gap_lower,
        "adjacent_gap_upper": adjacent_gap_upper,
        "t": t,
        "delta": delta,
        "b64": b64,
        "b32": b32,
        "n64": n64,
        "n32": n32,
        "h64": h64,
        "h32": h32,
        "agreement_e15_33": agreement_e15_33,
        "agreement_e15_34": agreement_e15_34,
        "agreement_e16_16": agreement_e16_16,
        "agreement_owner": agreement_owner,
        "pattern_rows": pattern["rows"],
        "pattern_paid": pattern["paid"],
        "pattern_unpaid": pattern["unpaid"],
        "pattern_paid_profiles": pattern_paid_profiles,
        "pattern_owner": pattern_owner,
        "s64": s64,
        "shadow_universe": shadow_universe,
        "paired": paired,
        "joint_increment_residues": joint_increment_residues,
        "f29_only_cap": f29_only_cap,
        "mixed_owner": mixed_owner,
        "nonpaired_direct_ceiling": nonpaired_direct_ceiling,
        "global_paid": global_paid,
        "allowance": allowance,
        "violation_residual": violation_residual,
        "profiles": profiles,
        "profile_bytes": profile_bytes,
        "profile_digest": profile_digest,
        "remaining_profiles": remaining_profiles,
        "remaining_profile_bytes": remaining_profile_bytes,
        "remaining_profile_digest": remaining_profile_digest,
        "uniform_profile_cap": uniform_profile_cap,
        "allowance_remainder": allowance_remainder,
        "violation_quotient": violation_quotient,
        "violation_remainder": violation_remainder,
        "forced_profile": forced_profile,
        "uniform_profile_total": uniform_profile_total,
        "residual_after_28": residual_after_28,
        "first_unpaid_footprint_min": first_unpaid_footprint_min,
        "first_unpaid_extra_touched_min": first_unpaid_extra_touched_min,
        "first_unpaid_q32_complete_max": first_unpaid_q32_complete_max,
        "x_star": x_star,
        "phi_x_star": phi_nonpaired(x_star),
        "phi_x_star_plus_one": phi_nonpaired(x_star + 1),
        "fixed27_core_count": fixed27_core_count,
        "fixed27_cap6": fixed27_cap6,
        "fixed27_cap7": fixed27_cap7,
        "fixed27_total6": fixed27_total6,
        "fixed27_total7": fixed27_total7,
        "fixed26_core_count": fixed26_core_count,
        "fixed26_cap116": fixed26_cap116,
        "fixed26_cap117": fixed26_cap117,
        "fixed26_cap130": fixed26_cap130,
        "fixed26_total116": fixed26_total116,
        "fixed26_total117": fixed26_total117,
        "fixed26_total130": fixed26_total130,
        "generator_degree": generator_degree,
        "post_27_core_degree": post_27_core_degree,
        "post_28_fiber_degree": post_28_fiber_degree,
        "pade_width": pade_width,
        "cross_roots_six": cross_roots_six,
        "cross_degree_cap": cross_degree_cap,
        "degree_interval_multiples": degree_interval_multiples,
    }


def verify(v: dict[str, object]) -> None:
    params = v["params"]
    require(isinstance(params, ReplayParameters), "parameter record type")

    require(params.first_match, "first-match owner order disabled")
    require(is_prime(params.p), "deployed field modulus is not prime")
    require(params.p - 1 == 1016 * params.n, "deployed subgroup divisibility")
    require(params.n == 2**21 and params.k == 2**20, "deployed n/K mismatch")
    require(v["t"] == 981_105, "canonical selected-complement size")
    require(v["generator_degree"] == 67_472, "degree-saturated generator degree")

    require(v["p6"] == 93_571_093_019_388_561_295_270_373_781_649_880_353_786_165_192_103_559_169, "p^6")
    require(v["denominator"] == 340_282_366_920_938_463_463_374_607_431_768_211_456, "2^128 denominator")
    require(v["bstar"] == 274_980_728_111_395_087, "Bstar")
    require(v["p6_remainder"] == 301_186_360_634_199_111_531_904_678_745_128_042_497, "p^6 remainder")
    require(v["compiled_target"] == TARGET_EXPECTED, "compiled target")
    require(v["target"] == TARGET_EXPECTED, "target mutation")
    require(v["adjacent_gap_lower"] == 79_209_528, "lower adjacent gap")
    require(v["adjacent_gap_upper"] == 2_051_496_905, "upper adjacent gap")

    require(v["n64"] == 64 and v["n32"] == 32, "dyadic image sizes")
    require(v["h64"] == 31 and v["h32"] == 15, "agreement shadow thresholds")
    require(v["agreement_e15_33"] == 55_534_064_877_048_198, "e15=33 cap")
    require(v["agreement_e15_34"] == 1_586_961_812_468_508, "e15=34 cap")
    require(v["agreement_e16_16"] == 601_080_390, "e16=16 cap")
    require(v["agreement_owner"] == 57_121_027_290_597_096, "agreement owner")
    require(len(v["pattern_rows"]) == 166, "residual e15=32 profile count")
    require(len(v["pattern_paid"]) == 110, "exact pattern paid profile count")
    require(len(v["pattern_unpaid"]) == 56, "exact pattern unpaid profile count")
    require(
        sum(number for _, number in v["pattern_rows"])
        == comb(64, 32) - 601_080_390,
        "residual e15=32 pattern total",
    )
    require(v["pattern_owner"] == 904_093_061_906_432, "exact pattern owner")

    require(v["delta"] == 913_633, "canonical complement intersection bound")
    require(27 * int(v["b64"]) <= int(v["delta"]) < 28 * int(v["b64"]), "q64 mixed-shadow threshold")
    require(v["s64"] == 27, "q64 mixed-shadow s")
    require(v["shadow_universe"] == 1_118_770_292_985_239_888, "q64 28-shadow universe")
    require(v["paired"] == 471_435_600, "paired q32 count")
    require(set(v["joint_increment_residues"]) == {0, 1}, "joint optimization monotonic increments")
    require(v["joint_increment_residues"].count(0) == 1, "joint optimization residue pattern")
    require(v["f29_only_cap"] == 38_578_285_965_008_272, "f29-only cap")
    require(v["mixed_owner"] == 38_578_286_420_187_472, "mixed owner")
    require(v["nonpaired_direct_ceiling"] == 1_118_770_292_513_804_288, "nonpaired direct ceiling")

    require(v["global_paid"] == 96_603_406_772_691_000, "global paid subtotal")
    require(v["allowance"] == 178_250_703_723_496_592, "remaining allowance")
    require(v["violation_residual"] == 178_250_703_723_496_593, "violator residual")

    profiles = v["profiles"]
    require(isinstance(profiles, list), "profile collection type")
    require(len(profiles) == 1_792, "residual profile count")
    require(profiles[0] == (0, 0, 0, 0, 0, 0), "first canonical profile")
    require(profiles[-1] == (32, 15, 7, 3, 1, 0), "last canonical profile")
    require(len(set(profiles)) == len(profiles), "duplicate residual profile")
    require(v["profile_digest"] == "e1c6056e40e0e8888d2324ca7105bed27238a01b4f3362cea05f7162396be461", "profile stream SHA-256")
    require(len(v["profile_bytes"]) == 24_114, "profile stream byte count")
    remaining_profiles = v["remaining_profiles"]
    require(isinstance(remaining_profiles, list), "remaining profile collection type")
    require(len(remaining_profiles) == 1_682, "remaining profile count")
    require(len(set(remaining_profiles)) == len(remaining_profiles), "duplicate remaining profile")
    require(
        set(remaining_profiles).isdisjoint(v["pattern_paid_profiles"]),
        "paid profile survived first-match removal",
    )
    require(
        v["remaining_profile_digest"]
        == "7dfa0fba111addf8ef4568821e2ce451de094c1ccef5de3468e80bd7e0373cfe",
        "remaining profile stream SHA-256",
    )
    require(len(v["remaining_profile_bytes"]) == 22_590, "remaining profile stream byte count")
    require(v["uniform_profile_cap"] == 105_975_448_111_472, "uniform profile cap")
    require(v["allowance_remainder"] == 688, "allowance/profile remainder")
    require(v["violation_quotient"] == 105_975_448_111_472, "violator quotient")
    require(v["violation_remainder"] == 689, "violator remainder")
    require(v["forced_profile"] == 105_975_448_111_473, "forced profile size")
    require(v["uniform_profile_total"] == TARGET_EXPECTED - 688, "uniform profile ledger total")

    require(v["residual_after_28"] == 63_601, "post-f28 residual size")
    require(v["first_unpaid_footprint_min"] == 32, "first-unpaid q64 footprint")
    require(v["first_unpaid_extra_touched_min"] == 4, "first-unpaid extra touched q64 fibers")
    require(v["first_unpaid_q32_complete_max"] == 13, "first-unpaid q32 full-fiber maximum")
    require(v["x_star"] == 184_616_800_285_050_042, "zero-reserve suffix threshold")
    require(v["phi_x_star"] == TARGET_EXPECTED, "zero-reserve threshold total")
    require(v["phi_x_star_plus_one"] == TARGET_EXPECTED + 1, "zero-reserve threshold sharpness")

    require(params.fixed27_incidence == 28, "fixed-27 incidence multiplicity")
    require(v["fixed27_core_count"] == 846_636_978_475_316_672, "27-core count")
    require(v["fixed27_cap6"] == 181_422_209_673_282_144, "fixed-27 cap at r=6")
    require(v["fixed27_total6"] == 271_769_678_181_377_208, "fixed-27 total at r=6")
    require(TARGET_EXPECTED - int(v["fixed27_total6"]) == 3_084_432_314_810_384, "fixed-27 r=6 margin")
    require(v["fixed27_cap7"] == 211_659_244_618_829_168, "fixed-27 cap at r=7")
    require(v["fixed27_total7"] == 300_964_056_749_491_576, "fixed-27 total at r=7")
    require(int(v["fixed27_total7"]) - TARGET_EXPECTED == 26_109_946_253_303_984, "fixed-27 r=7 excess")

    require(params.fixed26_incidence == comb(28, 26), "fixed-26 incidence multiplicity")
    require(v["fixed26_core_count"] == 601_557_853_127_198_688, "26-core count")
    require(v["fixed26_cap116"] == 184_605_055_457_023_936, "fixed-26 cap at r=116")
    require(v["fixed26_total116"] == 274_842_770_207_052_152, "fixed-26 total at r=116")
    require(TARGET_EXPECTED - int(v["fixed26_total116"]) == 11_340_289_135_440, "fixed-26 r=116 margin")
    require(v["fixed26_cap117"] == 186_196_478_348_894_832, "fixed-26 cap at r=117")
    require(v["fixed26_total117"] == 276_379_316_447_479_224, "fixed-26 total at r=117")
    require(int(v["fixed26_total117"]) - TARGET_EXPECTED == 1_525_205_951_291_632, "fixed-26 r=117 excess")
    require(v["fixed26_cap130"] == 206_884_975_943_216_480, "fixed-26 cap at r=130")
    require(v["fixed26_total130"] == 296_354_417_573_031_160, "fixed-26 total at r=130")
    require(int(v["fixed26_total130"]) - TARGET_EXPECTED == 21_500_307_076_843_568, "fixed-26 r=130 excess")

    require(v["post_27_core_degree"] == 96_369, "post-27-core locator degree")
    require(v["post_28_fiber_degree"] == 63_601, "post-extra-fiber locator degree")
    require(v["pade_width"] == 28_897, "normalized Pade quotient width")
    require(v["cross_roots_six"] == 196_608, "six-fiber root count")
    require(v["cross_degree_cap"] == 192_738, "cross-polynomial degree cap")
    require(int(v["cross_roots_six"]) > int(v["cross_degree_cap"]), "six-fiber root inequality")
    require(v["degree_interval_multiples"] == (), "block multiple in final degree interval")


def render(v: dict[str, object], archive: dict[str, int] | None) -> list[str]:
    lines = ["RANK16_GLOBAL_C0_FIRST_MATCH_LEDGER: PASS"]
    if archive is not None:
        lines.append(
            "archive_source="
            f"files:{archive['source_files']} bytes:{archive['source_bytes']} "
            f"lines:{archive['source_lines']} sha256:{archive['manifest_matches']}/{archive['source_files']}"
        )
    lines.extend(
        [
            f"p6={v['p6']}",
            f"Bstar={v['bstar']} p6_remainder={v['p6_remainder']}",
            f"target={v['target']} adjacent_gaps={v['adjacent_gap_lower']},{v['adjacent_gap_upper']}",
            "agreement_owner="
            f"{v['agreement_e15_33']}+{v['agreement_e15_34']}+{v['agreement_e16_16']}={v['agreement_owner']}",
            "pattern_owner="
            f"{v['pattern_owner']} paid_profiles={len(v['pattern_paid'])} "
            f"unpaid_pattern_profiles={len(v['pattern_unpaid'])}",
            f"mixed_shadow_owner={v['mixed_owner']} f29_only={v['f29_only_cap']} paired={v['paired']}",
            f"global_paid={v['global_paid']} allowance={v['allowance']} violation_residual={v['violation_residual']}",
            "all_profiles="
            f"{len(v['profiles'])} stream_bytes={len(v['profile_bytes'])} sha256={v['profile_digest']}",
            "remaining_profiles="
            f"{len(v['remaining_profiles'])} "
            f"stream_bytes={len(v['remaining_profile_bytes'])} "
            f"sha256={v['remaining_profile_digest']}",
            "profile_wall="
            f"cap:{v['uniform_profile_cap']} allowance_remainder:{v['allowance_remainder']} "
            f"violation_remainder:{v['violation_remainder']} forced:{v['forced_profile']}",
            "first_unpaid="
            "c0,f64=28,non-q32-paired,footprint>=32,extra_touched>=4,q32_full<=13 "
            f"residual={v['residual_after_28']}",
            f"first_unpaid_direct_ceiling={v['nonpaired_direct_ceiling']}",
            "zero_lower_cell_reserve_first_cell_threshold="
            f"{v['x_star']} total={v['phi_x_star']} next_total={v['phi_x_star_plus_one']}",
            "fixed27_uniform_r6="
            f"{v['fixed27_cap6']} total={v['fixed27_total6']} "
            f"margin={TARGET_EXPECTED - int(v['fixed27_total6'])}",
            "fixed27_uniform_r7="
            f"{v['fixed27_cap7']} total={v['fixed27_total7']} "
            f"excess={int(v['fixed27_total7']) - TARGET_EXPECTED}",
            "fixed26_uniform_r116="
            f"{v['fixed26_cap116']} total={v['fixed26_total116']} "
            f"margin={TARGET_EXPECTED - int(v['fixed26_total116'])}",
            "fixed26_uniform_r117="
            f"{v['fixed26_cap117']} total={v['fixed26_total117']} "
            f"excess={int(v['fixed26_total117']) - TARGET_EXPECTED}",
            "active_pencil_uniform_r130="
            f"{v['fixed26_cap130']} total={v['fixed26_total130']} "
            f"excess={int(v['fixed26_total130']) - TARGET_EXPECTED}",
            "source_degrees="
            f"g:{v['generator_degree']} post27:{v['post_27_core_degree']} "
            f"post28:{v['post_28_fiber_degree']} pade_width:{v['pade_width']}",
            "pending826_scope="
            "fixed root-free generator, one syndrome/projective ray, fixed 27-core; no global owner",
            "scope=one arbitrary received word; three owners charged once before generator/syndrome/ray partitions",
            "RESULT=PASS",
        ]
    )
    return lines


def tamper_selftest() -> None:
    base = ReplayParameters()
    mutations = (
        replace(base, target_shift=1),
        replace(base, delta_shift=1),
        replace(base, q64_blocks=63),
        replace(base, residual_e16_max=16),
        replace(base, fixed27_incidence=27),
        replace(base, fixed26_incidence=377),
        replace(base, first_match=False),
    )
    caught = 0
    for mutation in mutations:
        try:
            verify(replay(mutation))
        except VerificationError:
            caught += 1
    require(caught == len(mutations), "tamper self-test did not reject every mutation")
    print(f"TAMPER_SELFTEST: PASS ({caught}/{len(mutations)} rejected)")


def write_profiles(path: Path, profiles: list[tuple[int, int, int, int, int, int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="") as handle:
        handle.write("e15,e16,e17,e18,e19,e20\n")
        for profile in profiles:
            handle.write(",".join(str(value) for value in profile) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--archive-root",
        type=Path,
        help="root containing SOURCE_SHA256SUMS.txt and source/; verifies all source bytes",
    )
    parser.add_argument("--write-profiles", type=Path)
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.tamper_selftest:
        tamper_selftest()
        return

    values = replay()
    verify(values)
    archive = archive_manifest_audit(args.archive_root) if args.archive_root else None
    if args.write_profiles:
        write_profiles(args.write_profiles, values["remaining_profiles"])
    print("\n".join(render(values, archive)))


if __name__ == "__main__":
    main()
