#!/usr/bin/env python3
"""Deterministic certificate for the Route-D marked-puncture recursion.

The certificate is deliberately small and exhaustive.  It checks the exact
erase/insert recursion for every predicate on the F_7 parent fibre, all local
deletion-hereditary truth assignments, and the three obstruction fixtures that
prevent the common marking from being discarded.

Lean companion: experimental/lean/route_d_marked_puncture_contact_recursion_v1/
Reproduce: (cd experimental/lean/route_d_marked_puncture_contact_recursion_v1 && lake build)
"""

from __future__ import annotations

import argparse
import copy
import itertools
import sys
from typing import Callable, Dict, Iterable, List, Sequence, Set, Tuple

Support = Tuple[int, ...]
Prefix = Tuple[int, ...]


class CertificateError(RuntimeError):
    """A failed or tampered certificate."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def canonical(xs: Iterable[int]) -> Support:
    return tuple(sorted(xs))


def locator_prefix(support: Support, modulus: int, depth: int) -> Prefix:
    """Coefficients a_1,...,a_depth of prod_{x in S}(1-x X)."""
    coeffs = [1] + [0] * depth
    for x in support:
        for degree in range(depth, 0, -1):
            coeffs[degree] = (coeffs[degree] - x * coeffs[degree - 1]) % modulus
    return tuple(coeffs[1:])


def deconvolve(prefix: Prefix, root: int, modulus: int) -> Prefix:
    """Recover child coefficients from a_d(parent)=a_d(child)-root*a_{d-1}(child)."""
    child: List[int] = []
    previous = 1
    for parent_coefficient in prefix:
        current = (parent_coefficient + root * previous) % modulus
        child.append(current)
        previous = current
    return tuple(child)


def fibre(modulus: int, domain: Sequence[int], weight: int, depth: int,
          target: Prefix) -> Tuple[Support, ...]:
    return tuple(
        support
        for support in itertools.combinations(domain, weight)
        if locator_prefix(support, modulus, depth) == target
    )


def least_root(support: Support, boundary: Sequence[int]) -> int | None:
    contacts = [b for b in boundary if b in support]
    return min(contacts) if contacts else None


def scalar_support(support: Support, scalar: int, modulus: int) -> Support:
    return canonical((scalar * x) % modulus for x in support)


def support_stabilizer(support: Support, modulus: int,
                       scalars: Sequence[int] | None = None) -> Tuple[int, ...]:
    if scalars is None:
        scalars = tuple(range(1, modulus))
    return tuple(a for a in scalars if scalar_support(support, a, modulus) == support)


def support_orbit(support: Support, modulus: int,
                  scalars: Sequence[int] | None = None) -> Tuple[Support, ...]:
    if scalars is None:
        scalars = tuple(range(1, modulus))
    return tuple(sorted({scalar_support(support, a, modulus) for a in scalars}))


def target_stabilizer(prefix: Prefix, modulus: int) -> Tuple[int, ...]:
    return tuple(
        a for a in range(1, modulus)
        if tuple((pow(a, d, modulus) * c) % modulus for d, c in enumerate(prefix, 1))
        == prefix
    )


def check_f7_recursion() -> Dict[str, object]:
    modulus = 7
    domain = tuple(range(1, modulus))
    target = (1,)
    boundary = (1, 2, 3)
    parents = fibre(modulus, domain, 3, 1, target)
    expected = ((1, 2, 3), (2, 5, 6), (3, 4, 6))
    require(parents == expected, f"F7 parent fibre changed: {parents!r}")

    expected_children = {(1, 2, 3): (2, 3), (2, 5, 6): (5, 6), (3, 4, 6): (4, 6)}
    expected_targets = {1: (2,), 2: (3,), 3: (4,)}
    for parent, child in expected_children.items():
        root = least_root(parent, boundary)
        require(root is not None, "parent unexpectedly misses the boundary")
        require(canonical(x for x in parent if x != root) == child, "wrong erased child")
        require(deconvolve(target, root, modulus) == expected_targets[root], "wrong deconvolution")
        require(locator_prefix(child, modulus, 1) == expected_targets[root], "child target mismatch")

    masks_checked = 0
    for mask in range(1 << len(parents)):
        q: Callable[[Support], bool] = lambda s, mask=mask: bool(mask & (1 << parents.index(s))) \
            if s in parents else False
        selected = {s for s in parents if q(s)}
        cells: Dict[int, Set[Support]] = {b: set() for b in boundary}
        carried: Dict[int, Set[Support]] = {b: set() for b in boundary}
        for parent in selected:
            root = least_root(parent, boundary)
            require(root is not None, "selected support misses boundary")
            cells[root].add(parent)
            child = canonical(x for x in parent if x != root)
            carried[root].add(child)

        require(set().union(*cells.values()) == selected, "least-contact cells fail to cover")
        for left, right in itertools.combinations(boundary, 2):
            require(cells[left].isdisjoint(cells[right]), "least-contact cells overlap")

        for root in boundary:
            explicit: Set[Support] = set()
            child_domain = tuple(x for x in domain if x != root)
            child_target = deconvolve(target, root, modulus)
            for child in fibre(modulus, child_domain, 2, 1, child_target):
                if any(a in child for a in boundary if a < root):
                    continue
                parent = canonical((*child, root))
                if q(parent):
                    explicit.add(child)
            require(explicit == carried[root], f"carried-Q bijection failed at root {root}")
            require({canonical((*child, root)) for child in explicit} == cells[root],
                    f"insert inverse failed at root {root}")
        masks_checked += 1
    require(masks_checked == 8, "not every parent predicate was checked")

    # For each parent/least-erased-child pair, the allowed hereditary states are
    # 00, 01, 11 (parent truth implies child truth).  Exhaust all 3^3 choices.
    allowed_states = ((False, False), (False, True), (True, True))
    hereditary_checked = 0
    strict_controls = 0
    pairs = tuple((s, expected_children[s], least_root(s, boundary)) for s in parents)
    for choices in itertools.product(allowed_states, repeat=len(pairs)):
        carried_counts = {b: 0 for b in boundary}
        coarse_counts = {b: 0 for b in boundary}
        strict = False
        for (_, _, root), (parent_q, child_q) in zip(pairs, choices):
            require(root is not None, "missing least root")
            require(not parent_q or child_q, "non-hereditary assignment admitted")
            carried_counts[root] += int(parent_q)
            coarse_counts[root] += int(child_q)
            strict = strict or (not parent_q and child_q)
        require(sum(carried_counts.values()) <= sum(coarse_counts.values()),
                "hereditary cardinality bound failed")
        hereditary_checked += 1
        strict_controls += int(strict)
    require(hereditary_checked == 27, "not all hereditary assignments were checked")
    require(strict_controls == 19, "strict heredity controls changed")
    return {
        "parent_fibre": parents,
        "least_roots": tuple(least_root(s, boundary) for s in parents),
        "child_targets": tuple(expected_targets[b] for b in boundary),
        "q_masks_checked": masks_checked,
        "hereditary_assignments_checked": hereditary_checked,
        "strict_heredity_controls": strict_controls,
    }


def check_f11_raw_overlap() -> Dict[str, object]:
    modulus = 11
    domain = tuple(range(1, modulus))
    target = (5, 0)
    boundary = (1, 2)
    parents = fibre(modulus, domain, 3, 2, target)
    require(parents == ((1, 2, 3),), f"F11 fixture changed: {parents!r}")
    parent = parents[0]
    raw = {b: {s for s in parents if b in s} for b in boundary}
    require(raw[1] & raw[2] == {parent}, "raw contact cells should overlap")
    least = {b: {s for s in parents if least_root(s, boundary) == b} for b in boundary}
    require(least[1] == {parent} and least[2] == set(), "least-root partition is wrong")
    targets = tuple(deconvolve(target, b, modulus) for b in boundary)
    require(targets == ((6, 6), (7, 3)), "F11 child targets changed")
    return {"parent_fibre": parents, "raw_overlap": len(raw[1] & raw[2]),
            "least_cell_sizes": (len(least[1]), len(least[2])), "child_targets": targets}


def check_f11_root_blind_q_obstruction() -> Dict[str, object]:
    modulus = 11
    root = 1
    pad = (2, 3, 6)
    subgroup = (1, 10)
    root_orbit = canonical((a * root) % modulus for a in subgroup)
    require(root_orbit == (1, 10), "F11 marked-root orbit changed")
    pad_orbit = support_orbit(pad, modulus, subgroup)
    require(pad_orbit == ((2, 3, 6), (5, 8, 9)), "F11 root-blind pad orbit changed")
    require(all(set(candidate).isdisjoint(root_orbit) for candidate in pad_orbit),
            "F11 pad hits the marked-root orbit")

    parent = canonical((*pad, root))
    parent_target = locator_prefix(parent, modulus, 2)
    pad_target = locator_prefix(pad, modulus, 2)
    require(parent_target == (10, 3), "F11 full target changed")
    require(target_stabilizer(parent_target, modulus) == (1,), "F11 full target is not primitive")
    require(pad_target == (0, 3), "F11 root-blind pad target changed")
    require(target_stabilizer(pad_target, modulus) == subgroup,
            "F11 pad-target stabilizer changed")

    q: Callable[[Support], bool] = lambda support: 5 not in support
    require(q(parent) and q(pad), "F11 deletion-hereditary Q control changed")
    q_values = tuple(q(candidate) for candidate in pad_orbit)
    require(q_values == (True, False), "F11 Q unexpectedly descends to root-blind pads")
    return {
        "parent_target_stabilizer": target_stabilizer(parent_target, modulus),
        "pad_target_stabilizer": target_stabilizer(pad_target, modulus),
        "marked_root_orbit": root_orbit,
        "root_blind_pad_orbit": pad_orbit,
        "root_blind_pad_orbit_size": len(pad_orbit),
        "q_parent_pad": (q(parent), q(pad)),
        "q_pad_values": q_values,
    }


def check_f7_root_blind_nonfree_obstruction() -> Dict[str, object]:
    modulus = 7
    root = 3
    pad = (1, 2, 4)
    subgroup = (1, 2, 4)
    root_orbit = canonical((a * root) % modulus for a in subgroup)
    require(root_orbit == (3, 5, 6), "F7 marked-root orbit changed")
    require(set(pad).isdisjoint(root_orbit), "F7 pad hits the marked-root orbit")

    parent = canonical((*pad, root))
    parent_target = locator_prefix(parent, modulus, 3)
    pad_target = locator_prefix(pad, modulus, 3)
    require(parent_target == (4, 0, 6), "F7 full target changed")
    require(target_stabilizer(parent_target, modulus) == (1,), "F7 full target is not primitive")
    require(pad_target == (0, 0, 6), "F7 root-blind pad target changed")
    require(target_stabilizer(pad_target, modulus) == subgroup,
            "F7 pad-target stabilizer changed")
    require(support_stabilizer(pad, modulus, subgroup) == subgroup,
            "F7 root-blind pad stabilizer changed")
    pad_orbit = support_orbit(pad, modulus, subgroup)
    require(pad_orbit == (pad,), "F7 H-fixed pad orbit changed")
    require(len(pad_orbit) == 1 and len(subgroup) == 3,
            "F7 nonfree root-blind orbit control failed")
    return {
        "parent_target_stabilizer": target_stabilizer(parent_target, modulus),
        "pad_target_stabilizer": target_stabilizer(pad_target, modulus),
        "pad_stabilizer": support_stabilizer(pad, modulus, subgroup),
        "marked_root_orbit": root_orbit,
        "root_blind_pad_orbit": pad_orbit,
        "root_blind_pad_orbit_size": len(pad_orbit),
        "subgroup_size": len(subgroup),
    }


def build_certificate() -> Dict[str, object]:
    return {
        "schema": "route-d-marked-puncture-contact-recursion-v1",
        "source_commit": "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e",
        "source_blobs": {
            "experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md":
                "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
            "agents.md": "2fea2bce6a348105f0016fcf739b5247bf408d93",
            "experimental/agents-log.md": "45b04597efb40741b807e48b290a0544f2fe6baf",
        },
        "status": "PROVED",
        "f7_exact_recursion": check_f7_recursion(),
        "f11_raw_overlap": check_f11_raw_overlap(),
        "f11_root_blind_q_obstruction": check_f11_root_blind_q_obstruction(),
        "f7_root_blind_nonfree_obstruction": check_f7_root_blind_nonfree_obstruction(),
    }


def validate_certificate(certificate: Dict[str, object]) -> None:
    require(set(certificate) == {"schema", "source_commit", "source_blobs", "status",
                                 "f7_exact_recursion",
                                 "f11_raw_overlap", "f11_root_blind_q_obstruction",
                                 "f7_root_blind_nonfree_obstruction"},
            "top-level certificate fields changed")
    require(certificate["schema"] == "route-d-marked-puncture-contact-recursion-v1",
            "wrong schema")
    require(certificate["source_commit"] == "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e",
            "wrong source commit")
    require(certificate["source_blobs"] == {
        "experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md":
            "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
        "agents.md": "2fea2bce6a348105f0016fcf739b5247bf408d93",
        "experimental/agents-log.md": "45b04597efb40741b807e48b290a0544f2fe6baf",
    }, "source blob identities changed")
    require(certificate["status"] == "PROVED", "status is not PROVED")
    f7 = certificate["f7_exact_recursion"]
    f11 = certificate["f11_raw_overlap"]
    q_obstruction = certificate["f11_root_blind_q_obstruction"]
    nonfree = certificate["f7_root_blind_nonfree_obstruction"]
    require(isinstance(f7, dict) and f7["q_masks_checked"] == 8, "Q-mask evidence missing")
    require(f7["hereditary_assignments_checked"] == 27, "heredity evidence missing")
    require(f7["strict_heredity_controls"] == 19, "strict heredity control missing")
    require(f7["least_roots"] == (1, 2, 3), "least-root marking erased")
    require(f7["child_targets"] == ((2,), (3,), (4,)), "deconvolution evidence changed")
    require(isinstance(f11, dict) and f11["raw_overlap"] == 1, "raw-overlap obstruction missing")
    require(f11["least_cell_sizes"] == (1, 0), "first-match deletion changed")
    require(f11["child_targets"] == ((6, 6), (7, 3)), "signed deconvolution changed")
    require(isinstance(q_obstruction, dict), "root-blind Q obstruction missing")
    require(q_obstruction["parent_target_stabilizer"] == (1,), "F11 parent primitivity missing")
    require(q_obstruction["pad_target_stabilizer"] == (1, 10), "F11 pad stabilizer missing")
    require(q_obstruction["marked_root_orbit"] == (1, 10), "F11 root mark erased")
    require(q_obstruction["root_blind_pad_orbit_size"] == 2, "F11 pad orbit changed")
    require(q_obstruction["q_parent_pad"] == (True, True), "F11 heredity control changed")
    require(q_obstruction["q_pad_values"] == (True, False), "F11 Q-invariance guard missing")
    require(isinstance(nonfree, dict), "root-blind nonfree obstruction missing")
    require(nonfree["parent_target_stabilizer"] == (1,), "F7 parent primitivity missing")
    require(nonfree["pad_target_stabilizer"] == (1, 2, 4), "F7 pad target stabilizer missing")
    require(nonfree["pad_stabilizer"] == (1, 2, 4), "F7 H-fixed pad missing")
    require(nonfree["marked_root_orbit"] == (3, 5, 6), "F7 root mark erased")
    require(nonfree["root_blind_pad_orbit_size"] == 1, "false subgroup divisor admitted")
    require(nonfree["subgroup_size"] == 3, "F7 subgroup size changed")


def tamper_selftest(certificate: Dict[str, object]) -> int:
    mutations = [
        ("status", lambda c: c.__setitem__("status", "OPEN")),
        ("source commit", lambda c: c.__setitem__("source_commit", "c4856fa")),
        ("wrong deconvolution sign/order", lambda c: c["f7_exact_recursion"].__setitem__(
            "child_targets", ((0,), (6,), (5,)))),
        ("omit earlier-boundary exclusion", lambda c: c["f7_exact_recursion"].__setitem__(
            "least_roots", (1, 1, 1))),
        ("replace carried Q by child Q", lambda c: c["f7_exact_recursion"].__setitem__(
            "strict_heredity_controls", 0)),
        ("force raw cells disjoint", lambda c: c["f11_raw_overlap"].__setitem__(
            "raw_overlap", 0)),
        ("delete first-match cell", lambda c: c["f11_raw_overlap"].__setitem__(
            "least_cell_sizes", (0, 1))),
        ("divide by subgroup order", lambda c: c["f7_root_blind_nonfree_obstruction"].__setitem__(
            "root_blind_pad_orbit_size", 3)),
        ("infer child freeness", lambda c: c["f7_root_blind_nonfree_obstruction"].__setitem__(
            "pad_stabilizer", (1,))),
        ("erase root mark", lambda c: c["f7_root_blind_nonfree_obstruction"].__setitem__(
            "marked_root_orbit", (3,))),
        ("infer Q invariance", lambda c: c["f11_root_blind_q_obstruction"].__setitem__(
            "q_pad_values", (True, True))),
    ]
    caught = 0
    for name, mutate in mutations:
        altered = copy.deepcopy(certificate)
        mutate(altered)
        try:
            validate_certificate(altered)
        except CertificateError:
            caught += 1
        else:
            raise CertificateError(f"tamper was not detected: {name}")
    require(caught == len(mutations), "tamper suite did not run completely")
    return caught


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)
    try:
        certificate = build_certificate()
        validate_certificate(certificate)
        f7 = certificate["f7_exact_recursion"]
        f11 = certificate["f11_raw_overlap"]
        q_obstruction = certificate["f11_root_blind_q_obstruction"]
        nonfree = certificate["f7_root_blind_nonfree_obstruction"]
        print(
            "positive-controls: "
            f"Q masks {f7['q_masks_checked']}; "
            f"hereditary assignments {f7['hereditary_assignments_checked']} "
            f"({f7['strict_heredity_controls']} strict)"
        )
        print(
            "obstruction-controls: "
            f"F11 raw overlap {f11['raw_overlap']}; "
            f"least cells {f11['least_cell_sizes']}; "
            f"root-blind Q orbit {q_obstruction['root_blind_pad_orbit_size']} "
            f"with values {q_obstruction['q_pad_values']}; "
            f"nonfree root-blind orbit {nonfree['root_blind_pad_orbit_size']} "
            f"vs subgroup {nonfree['subgroup_size']}"
        )
        if args.tamper_selftest:
            caught = tamper_selftest(certificate)
            print(f"tamper-selftest: caught {caught}/11 mutations")
        print("STATUS PROVED")
        return 0
    except (CertificateError, KeyError, TypeError, ValueError) as error:
        print(f"STATUS FAILED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
