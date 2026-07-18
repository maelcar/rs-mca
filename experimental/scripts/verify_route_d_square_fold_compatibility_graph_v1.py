#!/usr/bin/env python3
"""Verify the Route-D square-fold compatibility-graph counterexample.

This stdlib-only verifier checks the exact local fold alphabet, reconstructs
the nine-member target-erased F23 K3,3 fixture with literal common core G={6}, verifies the
moment, primitive, and target-tag conditions, and exhausts every subgraph of K3,3 to check
the pseudoforest/orientation equivalence. It constructs no actual incidence
matrix or pivot and performs no rank-drop routing.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from collections.abc import Mapping, Sequence


P = 23
DOMAIN = tuple(range(1, P))
G = (6,)

SOURCE_PINS = {
    "base_commit": "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e",
    "prefix_commit": "e83962ae5ad7bacb391b691ffd37f0abef977b83",
    "prefix_note_blob": "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
    "singleton_commit": "84b393ec1bc52fa662756bd117a45537007d086a",
    "singleton_note_blob": "dda538a9a36cd0c8e267c11600a49cdc5bf054d1",
    "f23_precursor_commit": "f23a3b78a6bbe1d50a81b3976f92aa7c135ab300",
    "f23_precursor_note_blob": "5214d5d7fc91dab3f5ba12aabf5fef0c26922e9b",
    "f23_precursor_verifier_blob": "678463a3a188ecdb07c7bd7cd6f66401895d0eeb",
    "marked_transfer_commit": "332153d6e74403e3ad20f367ff4a3df8406a30bf",
    "marked_transfer_note_blob": "6ce5a571ca05f774a6569a9c78d9cb69e8fc896a",
    "marked_fold_commit": "3d9e4c01ac8dce2e6d9f73b3ab124977f8e18835",
    "marked_fold_note_blob": "13479a4b8de5f495508375a16366b62efe39acab",
    "admission_gap_commit": "8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67",
    "admission_gap_note_blob": "fdeabf0708cb8806feefae9322ed9002339332cf",
    "all_minors_commit": "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0",
    "all_minors_note_blob": "f24ce928df7e7170c1b4f3228d5fe9b184be50b4",
    "actual_rank_owner_note_blob": "ddfce00907f34128b324a64041f4e0ec8957b7d3",
    "square_fold_predecessor_commit": "f64e03a1215653eeafe3186df55269273d9f7653",
    "square_fold_predecessor_note_blob": "301144d04458027131779907f7f74aa5a6682bf4",
    "square_fold_predecessor_verifier_blob": "2507f09115c7eefbc86025dbaf204ea83c744283",
    "square_fold_predecessor_lean_blob": "ab061b3c53a320fbb8881bab4e6fa8e573f83248",
}

EXPECTED_FIXTURE_SHA256 = "e1ccd6f443731dd628870bdc9d05a513c2437d09346489b90f0eabfc08e3611b"
EXPECTED_TARGET_TAGGED_GRAPH_SHA256 = "17c7c8a0449a7a35f4cf314643442c345d019271ff7b04b4cd26c054e233680f"
PRECURSOR_ROWS_DIGEST = "de477753d921638e65fdbd346e6f4a7359afb51760ce32c82861bb3173ad0ce2"
ALL_FOLD_ROWS_DIGEST = "f6ac27af0adff1a4e864c0b565c9e3b3e524c08ab7bfac9ac940e7f1583b8877"
PRE_EXTENSION_GRAPH_DIGEST = "9bb01a03239c81b4e8110ba55f835f22366920346e00dbe3fef5c9c486519853"
PUBLISHED_GRAPH_DIGESTS = {
    "base": "620013449005471279d314a991283f139d2f31169d084b6ff1cdf2c1058018b5",
    "pivot_left": "e63135d2e226e81ca22626735d5eee0d00025e6df1809658ac271f223196556d",
    "pivot_right": "cff105369ac7be403c85f2c5ff594b19b085883919550533059ae5bdf83fd6fd",
    "pivot_both": "1e750b6d342f1c9c39576be1ecc3d7d7abda57d295c6778d1dc0417e5c370cb8",
}


class CertificateError(RuntimeError):
    """Raised when a fail-closed certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def sha256_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def square_fibers() -> tuple[tuple[int, int, int], ...]:
    seen: set[int] = set()
    fibers = []
    for root in DOMAIN:
        image = root * root % P
        if image in seen:
            continue
        seen.add(image)
        chosen = min(root, P - root)
        fibers.append((image, chosen, P - chosen))
    fibers.sort()
    require(len(fibers) == 11, "F23 square-fiber count drift")
    return tuple(fibers)


ROOT_BY_IMAGE = {image: root for image, root, _ in square_fibers()}

EVEN_LABELS = (
    {1: 2, 4: 2, 2: -2, 3: -2},
    {1: -2, 4: -2, 2: 2, 3: 2},
    {1: 2, 6: 2, 3: -2, 4: -2},
)

ODD_LABELS = (
    {8: 2, 9: 2, 12: -2, 16: -2},
    {8: -2, 9: -2, 12: 2, 16: 2},
    {9: 2, 12: 2, 16: -2, 18: -2},
)


def exact_alphabet() -> tuple[tuple[int, int], ...]:
    return tuple(sorted({(a + b, a - b) for a in (-1, 0, 1) for b in (-1, 0, 1)}))


EXPECTED_ALPHABET = (
    (-2, 0), (-1, -1), (-1, 1), (0, -2), (0, 0), (0, 2),
    (1, -1), (1, 1), (2, 0),
)


def locally_admissible(even: int, odd: int) -> bool:
    return (even - odd) % 2 == 0 and abs(even) + abs(odd) <= 2


def reconstruct(even: Mapping[int, int], odd: Mapping[int, int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    positive: set[int] = set()
    negative: set[int] = set()
    for image, root, opposite in square_fibers():
        u_value = even.get(image, 0)
        sigma_value = odd.get(image, 0)
        require(locally_admissible(u_value, sigma_value), "local alphabet violation")
        at_root = (u_value + sigma_value) // 2
        at_opposite = (u_value - sigma_value) // 2
        require(at_root in (-1, 0, 1) and at_opposite in (-1, 0, 1),
                "decoded coefficient drift")
        for point, coefficient in ((root, at_root), (opposite, at_opposite)):
            if coefficient == 1:
                positive.add(point)
            elif coefficient == -1:
                negative.add(point)
    require(positive.isdisjoint(negative), "reconstructed sides meet")
    return tuple(sorted(positive)), tuple(sorted(negative))


def moment(positive: Sequence[int], negative: Sequence[int], degree: int) -> int:
    return (sum(pow(root, degree, P) for root in positive)
            - sum(pow(root, degree, P) for root in negative)) % P


def projectively_primitive(positive: Sequence[int], negative: Sequence[int]) -> bool:
    weight = {root: 1 for root in positive}
    weight.update({root: -1 for root in negative})
    for scalar in DOMAIN:
        for sign in (1, -1):
            if (scalar, sign) == (1, 1):
                continue
            transformed = {scalar * root % P: sign * coefficient
                           for root, coefficient in weight.items()}
            if transformed == weight:
                return False
    return True


def sparse(label: Mapping[int, int]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(label.items()))


def build_fixture() -> list[dict[str, object]]:
    images = (1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18)
    require(tuple(ROOT_BY_IMAGE[image] for image in images)
            == (1, 5, 7, 2, 11, 10, 3, 9, 6, 4, 8), "root orientation drift")
    require(exact_alphabet() == EXPECTED_ALPHABET, "exact alphabet drift")
    require(all(locally_admissible(u, sigma) == ((u, sigma) in EXPECTED_ALPHABET)
                for u in range(-3, 4) for sigma in range(-3, 4)),
            "alphabet characterization drift")

    rows: list[dict[str, object]] = []
    for even_index, even in enumerate(EVEN_LABELS):
        require(sum(even.values()) == 0, "even degree-zero drift")
        require(sum(value * image for image, value in even.items()) % P == 0,
                "even degree-one drift")
        for odd_index, odd in enumerate(ODD_LABELS):
            require(sum(value * ROOT_BY_IMAGE[image] for image, value in odd.items()) % P == 0,
                    "odd degree-zero drift")
            require(set(even).isdisjoint(odd), "channel pools meet")
            positive, negative = reconstruct(even, odd)
            require(len(positive) == len(negative) == 8, "side-size drift")
            require(set(G).isdisjoint(positive) and set(G).isdisjoint(negative),
                    "literal common core lost")
            marked_s = tuple(sorted((*G, *positive)))
            marked_t = tuple(sorted((*G, *negative)))
            require(set(marked_s) & set(marked_t) == set(G), "marked intersection drift")
            moments = tuple(moment(positive, negative, degree) for degree in range(5))
            require(moments[:3] == (0, 0, 0), "prefix-moment drift")
            require(moments[3] != 0, "extension degeneration entered")
            require(projectively_primitive(positive, negative), "primitive filter drift")
            require(sum(value * value for value in even.values())
                    + sum(value * value for value in odd.values()) == 32,
                    "quadratic size constraint drift")
            rows.append({
                "even_index": even_index,
                "odd_index": odd_index,
                "G": G,
                "even": sparse(even),
                "odd": sparse(odd),
                "positive": positive,
                "negative": negative,
                "S": marked_s,
                "T": marked_t,
                "moments_0_through_4": moments,
                "primitive": True,
            })
    require(len(rows) == 9, "K3,3 row count drift")
    require(len({row["S"] for row in rows}) == 9, "marked parents collided")
    return rows


def add_weight(weight: dict[int, int], root: int, coefficient: int) -> None:
    value = weight.get(root, 0) + coefficient
    if value:
        weight[root] = value
    else:
        weight.pop(root, None)


def signed_weight(*terms: tuple[Sequence[int] | set[int], int]) -> dict[int, int]:
    weight: dict[int, int] = {}
    for roots, coefficient in terms:
        for root in roots:
            add_weight(weight, root, coefficient)
    return weight


def locator_pair(roots: Sequence[int]) -> tuple[int, int, int]:
    left, right = sorted(roots)
    return ((left * right) % P, (-(left + right)) % P, 1)


def polynomial_roots(poly: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        point for point in DOMAIN
        if sum(coefficient * pow(point, degree, P)
               for degree, coefficient in enumerate(poly)) % P == 0
    )


def weight_moment(weight: Mapping[int, int], degree: int) -> int:
    return sum(coefficient * pow(root, degree, P)
               for root, coefficient in weight.items()) % P


def weight_projectively_primitive(weight: Mapping[int, int]) -> bool:
    for scalar in DOMAIN:
        for sign in (1, -1):
            if (scalar, sign) == (1, 1):
                continue
            transformed: dict[int, int] = {}
            for root, coefficient in weight.items():
                add_weight(transformed, scalar * root % P, sign * coefficient)
            if transformed == weight:
                return False
    return True


def enumerate_predecessor_packets() -> list[dict[str, object]]:
    packets: list[dict[str, object]] = []
    for side_a in itertools.combinations(DOMAIN, 2):
        core = (10 - sum(side_a)) % P
        if core == 0 or core in side_a:
            continue
        locator_u = locator_pair(side_a)
        locator_v = ((locator_u[0] - 17) % P, locator_u[1], 1)
        side_r = polynomial_roots(locator_v)
        if len(side_r) != 2 or core in side_r:
            continue
        require(set(side_a).isdisjoint(side_r), "predecessor packet sides meet")
        packets.append({
            "S": tuple(sorted((core, *side_a))),
            "S_prime": tuple(sorted((core, *side_r))),
            "G": (core,),
            "A": tuple(sorted(side_a)),
            "R": side_r,
            "U": locator_u,
        })
    packets.sort(key=lambda packet: (packet["S"], packet["S_prime"]))
    require(len(packets) == 75, "predecessor packet census drift")
    require(len({packet["U"] for packet in packets}) == 75,
            "predecessor Rule-1 key collision appeared")
    return packets


def predecessor_h_roots(representative: Mapping[str, object],
                        packet: Mapping[str, object]) -> tuple[int, ...]:
    return tuple(sorted(
        (set(representative["A"]) & set(packet["A"]))
        | (set(representative["R"]) & set(packet["R"]))
    ))


def fold_weight(weight: Mapping[int, int]) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (image, weight.get(root, 0) + weight.get(negative, 0),
         weight.get(root, 0) - weight.get(negative, 0))
        for image, root, negative in square_fibers()
    )


def reconstruct_folded_weight(folded: Sequence[tuple[int, int, int]]) -> dict[int, int]:
    fiber_by_image = {image: (root, negative)
                      for image, root, negative in square_fibers()}
    recovered: dict[int, int] = {}
    for image, occupancy, signed in folded:
        require((occupancy + signed) % 2 == 0
                and (occupancy - signed) % 2 == 0,
                "predecessor fold parity drift")
        root, negative = fiber_by_image[image]
        add_weight(recovered, root, (occupancy + signed) // 2)
        add_weight(recovered, negative, (occupancy - signed) // 2)
    return recovered


def lex_weighted_pivot(weight: Mapping[int, int]) -> int:
    support = sorted(weight)
    require(len(support) >= 3, "predecessor pivot support too small")
    columns = [
        (weight[root] % P, weight[root] * root % P,
         weight[root] * root * root % P)
        for root in support[:3]
    ]
    matrix = [[columns[column][row] for column in range(3)] for row in range(3)]
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    ) % P


def predecessor_rows_digest(rows: Sequence[Mapping[str, object]]) -> str:
    serializable = [{
        "G": row["G"], "A": row["A"], "R": row["R"], "U": row["U"],
        "lambda_weight": row["lambda"], "mu3": row["mu3"],
        "support": row["support"], "profile": row["profile"],
    } for row in rows]
    return sha256_json(serializable)


def build_predecessor_rows() -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    packets = enumerate_predecessor_packets()
    representative = packets[0]
    require(representative == {
        "S": (1, 2, 7), "S_prime": (1, 4, 5), "G": (1,),
        "A": (2, 7), "R": (4, 5), "U": (14, 14, 1),
    }, "predecessor representative drift")
    a0, r0 = set(representative["A"]), set(representative["R"])
    pre_extension: list[dict[str, object]] = []
    retained: list[dict[str, object]] = []
    h_one_count = 0
    for packet_index, packet in enumerate(packets[1:], start=1):
        if predecessor_h_roots(representative, packet):
            continue
        h_one_count += 1
        core = set(packet["G"])
        side_a, side_r = set(packet["A"]), set(packet["R"])
        mu = signed_weight((a0, 1), (side_r, 1), (r0, -1), (side_a, -1))
        require(all(weight_moment(mu, degree) == 0 for degree in range(3)),
                "predecessor Rule-2 moment drift")
        mu3 = weight_moment(mu, 3)
        contact = signed_weight((a0 & core, 1), (r0 & core, -1))
        off_core = dict(mu)
        for root, coefficient in contact.items():
            add_weight(off_core, root, -coefficient)
        require(set(off_core).isdisjoint(core), "predecessor literal G lost")
        folded = fold_weight(off_core)
        require(reconstruct_folded_weight(folded) == off_core,
                "predecessor even/odd reconstruction drift")
        for exponent in range(3):
            even_moment = sum(occupancy * pow(image, exponent, P)
                              for image, occupancy, _ in folded) % P
            odd_moment = sum(signed * root * pow(image, exponent, P)
                             for (image, _, signed), (_, root, _) in
                             zip(folded, square_fibers())) % P
            require(even_moment == weight_moment(off_core, 2 * exponent),
                    "predecessor even moment drift")
            require(odd_moment == weight_moment(off_core, 2 * exponent + 1),
                    "predecessor odd moment drift")
        row = {
            "packet_index": packet_index,
            "G": packet["G"], "A": packet["A"], "R": packet["R"],
            "U": packet["U"],
            "profile": (len(a0 & core), len(r0 & core)),
            "mu": tuple(sorted(mu.items())),
            "lambda": tuple(sorted(off_core.items())),
            "even": tuple((image, occupancy) for image, occupancy, _ in folded
                          if occupancy),
            "odd": tuple((image, signed) for image, _, signed in folded if signed),
            "pivot": lex_weighted_pivot(off_core),
            "support": len(off_core),
            "mu3": mu3,
        }
        pre_extension.append(row)
        if mu3 != 0:
            require(len(off_core) >= 5, "predecessor non-full support survived")
            require(weight_projectively_primitive(mu)
                    and weight_projectively_primitive(off_core),
                    "predecessor primitive filter drift")
            retained.append(row)
    extensions = [row for row in pre_extension if row["mu3"] == 0]
    require(h_one_count == 56 and len(pre_extension) == 56,
            "predecessor H=1 census drift")
    require(len(extensions) == 1 and len(retained) == 55,
            "predecessor extension deletion drift")
    require(predecessor_rows_digest(retained) == PRECURSOR_ROWS_DIGEST,
            "predecessor retained digest drift")
    require(sha256_json(retained) == ALL_FOLD_ROWS_DIGEST,
            "predecessor canonical row serialization drift")
    return pre_extension, retained, extensions[0]


def graph_labels(row: Mapping[str, object], *, left_pivot: bool,
                 right_pivot: bool) -> tuple[object, object]:
    left = (row["G"], row["even"])
    right = (row["G"], row["odd"])
    if left_pivot:
        left = (*left, row["pivot"])
    if right_pivot:
        right = (*right, row["pivot"])
    return left, right


def derived_graph(rows: Sequence[Mapping[str, object]], *, left_pivot: bool = False,
                  right_pivot: bool = False) -> dict[str, object]:
    row_edges = [graph_labels(row, left_pivot=left_pivot,
                              right_pivot=right_pivot) for row in rows]
    serialized_edges = [
        (row["packet_index"], left, right)
        for row, (left, right) in zip(rows, row_edges)
    ]
    unique_edges = set(row_edges)
    left_vertices = {edge[0] for edge in unique_edges}
    right_vertices = {edge[1] for edge in unique_edges}
    adjacency: dict[tuple[str, object], set[tuple[str, object]]] = defaultdict(set)
    for left, right in unique_edges:
        left_node, right_node = ("L", left), ("R", right)
        adjacency[left_node].add(right_node)
        adjacency[right_node].add(left_node)
    unseen = set(adjacency)
    component_shapes = []
    while unseen:
        start = next(iter(unseen))
        queue = deque([start])
        vertices: set[tuple[str, object]] = set()
        edge_twice = 0
        while queue:
            vertex = queue.popleft()
            if vertex in vertices:
                continue
            vertices.add(vertex)
            unseen.discard(vertex)
            edge_twice += len(adjacency[vertex])
            queue.extend(adjacency[vertex])
        component_shapes.append((len(vertices), edge_twice // 2))
    left_degrees = Counter(len(adjacency[("L", vertex)]) for vertex in left_vertices)
    right_degrees = Counter(len(adjacency[("R", vertex)]) for vertex in right_vertices)
    vertex_count = len(left_vertices) + len(right_vertices)
    edge_count = len(unique_edges)
    component_count = len(component_shapes)
    return {
        "left_vertices": len(left_vertices),
        "right_vertices": len(right_vertices),
        "row_edges": len(row_edges),
        "edges": edge_count,
        "duplicate_edges": len(row_edges) - edge_count,
        "components": component_count,
        "component_shapes": tuple(sorted(component_shapes)),
        "cycle_rank": edge_count - vertex_count + component_count,
        "left_degree_histogram": {str(key): value
                                  for key, value in sorted(left_degrees.items())},
        "right_degree_histogram": {str(key): value
                                   for key, value in sorted(right_degrees.items())},
        "digest": sha256_json(serialized_edges),
    }


def graph_certificate(graph: Mapping[str, object]) -> dict[str, object]:
    return {
        key: graph[key] for key in (
            "left_vertices", "right_vertices", "row_edges", "edges",
            "duplicate_edges", "components", "cycle_rank",
            "left_degree_histogram", "right_degree_histogram", "digest",
        )
    }


def deleted_edge_is_isolated(pre_extension: Sequence[Mapping[str, object]],
                             retained: Sequence[Mapping[str, object]],
                             extension: Mapping[str, object]) -> bool:
    pre_edges = [graph_labels(row, left_pivot=False, right_pivot=False)
                 for row in pre_extension]
    retained_edges = [graph_labels(row, left_pivot=False, right_pivot=False)
                      for row in retained]
    extension_edge = graph_labels(extension, left_pivot=False, right_pivot=False)
    left_degree = Counter(left for left, _ in pre_edges)
    right_degree = Counter(right for _, right in pre_edges)
    retained_left = {left for left, _ in retained_edges}
    retained_right = {right for _, right in retained_edges}
    pre_without_extension = [
        edge for row, edge in zip(pre_extension, pre_edges)
        if row["packet_index"] != extension["packet_index"]
    ]
    return (pre_without_extension == retained_edges
            and left_degree[extension_edge[0]] == 1
            and right_degree[extension_edge[1]] == 1
            and extension_edge[0] not in retained_left
            and extension_edge[1] not in retained_right)


Edge = tuple[int, int]


def component_counts(left_count: int, right_count: int, edges: Sequence[Edge]) -> tuple[tuple[int, int], ...]:
    adjacency: dict[tuple[str, int], list[tuple[str, int]]] = defaultdict(list)
    for left, right in edges:
        left_vertex = ("L", left)
        right_vertex = ("R", right)
        adjacency[left_vertex].append(right_vertex)
        adjacency[right_vertex].append(left_vertex)
    unseen = set(adjacency)
    counts = []
    while unseen:
        start = next(iter(unseen))
        queue = deque([start])
        vertices: set[tuple[str, int]] = set()
        edge_twice = 0
        while queue:
            vertex = queue.popleft()
            if vertex in vertices:
                continue
            vertices.add(vertex)
            unseen.discard(vertex)
            edge_twice += len(adjacency[vertex])
            queue.extend(adjacency[vertex])
        counts.append((len(vertices), edge_twice // 2))
    require(all(0 <= left < left_count and 0 <= right < right_count for left, right in edges),
            "edge endpoint drift")
    return tuple(sorted(counts))


def is_pseudoforest(left_count: int, right_count: int, edges: Sequence[Edge]) -> bool:
    return all(edge_count <= vertex_count
               for vertex_count, edge_count in component_counts(left_count, right_count, edges))


def has_indegree_one_orientation(left_count: int, right_count: int, edges: Sequence[Edge]) -> bool:
    for choices in itertools.product((0, 1), repeat=len(edges)):
        left_load = [0] * left_count
        right_load = [0] * right_count
        for choice, (left, right) in zip(choices, edges):
            if choice == 0:
                left_load[left] += 1
            else:
                right_load[right] += 1
        if max(left_load, default=0) <= 1 and max(right_load, default=0) <= 1:
            return True
    return False


def graph_exhaustion() -> dict[str, int]:
    complete = tuple(itertools.product(range(3), range(3)))
    histogram: Counter[str] = Counter()
    checked = 0
    for mask in range(1 << len(complete)):
        edges = tuple(edge for index, edge in enumerate(complete) if mask & (1 << index))
        pseudo = is_pseudoforest(3, 3, edges)
        oriented = has_indegree_one_orientation(3, 3, edges)
        require(pseudo == oriented, "pseudoforest/orientation equivalence failed")
        histogram["pseudoforest" if pseudo else "non_pseudoforest"] += 1
        checked += 1
    return {
        "subgraphs_checked": checked,
        "pseudoforest_subgraphs": histogram["pseudoforest"],
        "non_pseudoforest_subgraphs": histogram["non_pseudoforest"],
    }


def depth_two_target(marked_support: Sequence[int]) -> tuple[int, int]:
    return (
        sum(marked_support) % P,
        sum(left * right for left, right in itertools.combinations(marked_support, 2)) % P,
    )


def target_tagged_fixture_graph(rows: Sequence[Mapping[str, object]]) -> dict[str, object]:
    labeled_edges = []
    target_histogram: Counter[tuple[int, int]] = Counter()
    for row in rows:
        target = depth_two_target(row["S"])
        require(target == depth_two_target(row["T"]),
                "marked-pair depth-two target drift")
        target_histogram[target] += 1
        left = (target, row["G"], sparse(EVEN_LABELS[row["even_index"]]))
        right = (target, row["G"], sparse(ODD_LABELS[row["odd_index"]]))
        labeled_edges.append((left, right))
    require(len(set(labeled_edges)) == 9, "target-tagged fixture edge collision")
    left_labels = sorted({left for left, _ in labeled_edges}, key=repr)
    right_labels = sorted({right for _, right in labeled_edges}, key=repr)
    left_index = {label: index for index, label in enumerate(left_labels)}
    right_index = {label: index for index, label in enumerate(right_labels)}
    indexed_edges = tuple((left_index[left], right_index[right])
                          for left, right in labeled_edges)
    shapes = component_counts(len(left_labels), len(right_labels), indexed_edges)
    vertex_count = len(left_labels) + len(right_labels)
    component_count = len(shapes)
    left_degrees = Counter(left for left, _ in indexed_edges)
    right_degrees = Counter(right for _, right in indexed_edges)
    return {
        "target_histogram": {
            f"{target[0]},{target[1]}": count
            for target, count in sorted(target_histogram.items())
        },
        "left_vertices": len(left_labels),
        "right_vertices": len(right_labels),
        "edges": len(indexed_edges),
        "components": component_count,
        "component_shapes": [list(shape) for shape in shapes],
        "cycle_rank": len(indexed_edges) - vertex_count + component_count,
        "left_degree_histogram": {
            str(degree): sum(value == degree for value in left_degrees.values())
            for degree in sorted(set(left_degrees.values()))
        },
        "right_degree_histogram": {
            str(degree): sum(value == degree for value in right_degrees.values())
            for degree in sorted(set(right_degrees.values()))
        },
        "pseudoforest": is_pseudoforest(len(left_labels), len(right_labels), indexed_edges),
        "indegree_one_endpoint_assignment": has_indegree_one_orientation(
            len(left_labels), len(right_labels), indexed_edges),
        "digest": sha256_json([
            (row["even_index"], row["odd_index"], depth_two_target(row["S"]), left, right)
            for row, (left, right) in zip(rows, labeled_edges)
        ]),
    }


def summarize() -> dict[str, object]:
    rows = build_fixture()
    fixture_digest = sha256_json(rows)
    require(fixture_digest == EXPECTED_FIXTURE_SHA256, "fixture digest drift")
    graph_counts = graph_exhaustion()
    target_graph = target_tagged_fixture_graph(rows)
    require(target_graph["digest"] == EXPECTED_TARGET_TAGGED_GRAPH_SHA256,
            "target-tagged fixture digest drift")
    require(target_graph["target_histogram"] == {
        "6,0": 1, "6,2": 2, "6,5": 2, "6,7": 4,
    }, "target-tagged fixture histogram drift")
    require(target_graph["left_vertices"] == 6
            and target_graph["right_vertices"] == 6
            and target_graph["edges"] == 9
            and target_graph["components"] == 4
            and target_graph["component_shapes"]
            == [[2, 1], [3, 2], [3, 2], [4, 4]]
            and target_graph["cycle_rank"] == 1
            and target_graph["left_degree_histogram"] == {"1": 3, "2": 3}
            and target_graph["right_degree_histogram"] == {"1": 3, "2": 3}
            and target_graph["pseudoforest"] is True
            and target_graph["indegree_one_endpoint_assignment"] is True,
            "target-tagged fixture graph drift")
    complete = tuple(itertools.product(range(3), range(3)))
    require(not is_pseudoforest(3, 3, complete), "K3,3 became a pseudoforest")
    require(not has_indegree_one_orientation(3, 3, complete),
            "K3,3 acquired a multiplicity-one endpoint assignment")
    pre_extension_rows, retained_rows, extension_row = build_predecessor_rows()
    base_graph = derived_graph(retained_rows)
    pivot_left_graph = derived_graph(retained_rows, left_pivot=True)
    pivot_right_graph = derived_graph(retained_rows, right_pivot=True)
    pivot_both_graph = derived_graph(retained_rows, left_pivot=True, right_pivot=True)
    graph_variants = {
        "base": graph_certificate(base_graph),
        "pivot_left": graph_certificate(pivot_left_graph),
        "pivot_right": graph_certificate(pivot_right_graph),
        "pivot_both": graph_certificate(pivot_both_graph),
    }
    for name, graph in graph_variants.items():
        require(graph["digest"] == PUBLISHED_GRAPH_DIGESTS[name],
                f"predecessor {name} graph digest drift")
        require(graph["row_edges"] == 55 and graph["edges"] == 55
                and graph["duplicate_edges"] == 0 and graph["cycle_rank"] == 0,
                f"predecessor {name} graph census drift")
        require(graph["left_degree_histogram"] == {"1": 55},
                f"predecessor {name} left-degree drift")
    require(base_graph["left_vertices"] == 55
            and base_graph["right_vertices"] == 52
            and base_graph["components"] == 52
            and base_graph["right_degree_histogram"] == {"1": 51, "4": 1}
            and base_graph["component_shapes"].count((2, 1)) == 51
            and base_graph["component_shapes"].count((5, 4)) == 1,
            "predecessor base graph shape drift")
    require(pivot_left_graph["left_vertices"] == 55
            and pivot_left_graph["right_vertices"] == 52
            and pivot_left_graph["components"] == 52
            and pivot_left_graph["right_degree_histogram"] == {"1": 51, "4": 1},
            "predecessor pivot-left graph shape drift")
    for name, graph in (("pivot-right", pivot_right_graph),
                        ("pivot-both", pivot_both_graph)):
        require(graph["left_vertices"] == 55
                and graph["right_vertices"] == 53
                and graph["components"] == 53
                and graph["right_degree_histogram"] == {"1": 52, "3": 1}
                and graph["component_shapes"].count((2, 1)) == 52
                and graph["component_shapes"].count((4, 3)) == 1,
                f"predecessor {name} graph shape drift")

    pre_extension_graph = derived_graph(pre_extension_rows)
    require(pre_extension_graph["digest"] == PRE_EXTENSION_GRAPH_DIGEST,
            "predecessor pre-extension graph digest drift")
    require(pre_extension_graph["left_vertices"] == 56
            and pre_extension_graph["right_vertices"] == 53
            and pre_extension_graph["row_edges"] == 56
            and pre_extension_graph["edges"] == 56
            and pre_extension_graph["duplicate_edges"] == 0
            and pre_extension_graph["components"] == 53
            and pre_extension_graph["cycle_rank"] == 0
            and pre_extension_graph["left_degree_histogram"] == {"1": 56}
            and pre_extension_graph["right_degree_histogram"] == {"1": 52, "4": 1}
            and pre_extension_graph["component_shapes"].count((2, 1)) == 52
            and pre_extension_graph["component_shapes"].count((5, 4)) == 1,
            "predecessor pre-extension graph shape drift")
    require(extension_row["packet_index"] == 2
            and extension_row["G"] == (1,)
            and extension_row["A"] == (3, 6)
            and extension_row["R"] == (11, 21)
            and extension_row["U"] == (18, 14, 1)
            and extension_row["pivot"] == 2
            and extension_row["support"] == 8
            and extension_row["mu3"] == 0,
            "predecessor extension identity drift")
    isolated_extension = deleted_edge_is_isolated(
        pre_extension_rows, retained_rows, extension_row)
    require(isolated_extension, "predecessor extension edge not isolated")

    predecessor_graph = {
        "precursor_packets": 75,
        "fixed_H_comparisons": len(pre_extension_rows),
        "extension_deletions": len(pre_extension_rows) - len(retained_rows),
        "retained_rows": len(retained_rows),
        "precursor_rows_sha256": predecessor_rows_digest(retained_rows),
        "all_fold_rows_sha256": sha256_json(retained_rows),
        "base": graph_certificate(base_graph),
        "pivot_left": graph_certificate(pivot_left_graph),
        "pivot_right": graph_certificate(pivot_right_graph),
        "pivot_both": graph_certificate(pivot_both_graph),
        "pre_extension": graph_certificate(pre_extension_graph),
        "deleted_extension": {
            "packet_index": extension_row["packet_index"],
            "G": list(extension_row["G"]),
            "A": list(extension_row["A"]),
            "R": list(extension_row["R"]),
            "U": list(extension_row["U"]),
            "pivot": extension_row["pivot"],
            "support": extension_row["support"],
            "mu3": extension_row["mu3"],
            "edge_is_isolated": isolated_extension,
        },
        "pre_first_match_only": True,
        "owner_typed_payment": False,
    }
    return {
        "status": "COUNTEREXAMPLE",
        "theorems": [
            "MARKED_SQUARE_FOLD_EXACT_ALPHABET_RECONSTRUCTION",
            "PSEUDOFOREST_IFF_INDEGREE_ONE_ENDPOINT_ASSIGNMENT",
            "SQUARE_FOLD_TARGET_ERASURE_K33_NO_GO",
        ],
        "provenance": SOURCE_PINS,
        "parameters": {
            "field": "F_23", "domain": "F_23^*", "literal_G": list(G),
            "side_size_off_core": 8, "prefix_depth": 2,
        },
        "alphabet": {
            "pairs": [list(pair) for pair in EXPECTED_ALPHABET],
            "characterization": "u == sigma (mod 2) and |u|+|sigma| <= 2",
            "positive_coordinate": "mu(x_y)=(u_y+sigma_y)/2",
            "negative_coordinate": "mu(-x_y)=(u_y-sigma_y)/2",
            "equal_side_constraints": ["sum u=0", "sum (u^2+sigma^2)=4r"],
        },
        "moment_split": {
            "even": "mu_(2h)=sum_y u_y*y^h",
            "odd": "mu_(2h+1)=sum_y sigma_y*x_y*y^h",
            "deployed_printed_even_rows": 33735,
            "deployed_odd_rows": 33736,
        },
        "fixture": {
            "even_labels": len(EVEN_LABELS),
            "odd_labels": len(ODD_LABELS),
            "joint_parents": len(rows),
            "additive_label_total": len(EVEN_LABELS) + len(ODD_LABELS),
            "product_label_total": len(EVEN_LABELS) * len(ODD_LABELS),
            "target_erased_graph": "K_3,3",
            "components": 1,
            "cyclomatic_number": 4,
            "next_odd_moments": [8, 15, 15],
            "all_projectively_primitive": True,
            "fixture_sha256": fixture_digest,
            "target_tagged_graph": target_graph,
        },
        "graph_exhaustion": graph_counts,
        "pinned_predecessor_forest": predecessor_graph,
        "ownership": {
            "literal_common_core_preserved": True,
            "named_first_match_executor_available": False,
            "even_projection_routes_nonquotient_parent": False,
            "odd_projection_is_boolean_quotient_support": False,
            "actual_incidence_constructed": False,
            "actual_vanishing_pivot_constructed": False,
            "rank_drop_routes": 0,
            "unrouted_vanishing_pivot_families": 0,
            "target_erasure_counterexample": True,
            "fixed_target_additive_transfer_refuted": False,
            "fixed_target_graph_is_pseudoforest": True,
            "deployed_bound_refuted": False,
        },
    }


EXPECTED_CERTIFICATE_SHA256 = "0c7053c2e1bd9f70bf478a9361f0c04a8a34ed06f141ec18d6604bf2a10a0513"


def validate(certificate: Mapping[str, object]) -> None:
    require(sha256_json(certificate) == EXPECTED_CERTIFICATE_SHA256, "certificate digest differs from fail-closed expected object")


def leaf_paths(value: object, path: tuple[object, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from leaf_paths(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from leaf_paths(child, (*path, index))
    else:
        yield path


def mutate_leaf(value: object) -> object:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "!"
    raise CertificateError(f"unsupported leaf type {type(value).__name__}")


def tamper_selftest(certificate: dict[str, object]) -> int:
    paths = tuple(leaf_paths(certificate))
    caught = 0
    for path in paths:
        broken = copy.deepcopy(certificate)
        cursor: object = broken
        for key in path[:-1]:
            cursor = cursor[key]  # type: ignore[index]
        cursor[path[-1]] = mutate_leaf(cursor[path[-1]])  # type: ignore[index]
        try:
            validate(broken)
        except CertificateError:
            caught += 1
    for operation in ("extra", "missing"):
        broken = copy.deepcopy(certificate)
        if operation == "extra":
            broken["unexpected"] = True
        else:
            del broken["ownership"]
        try:
            validate(broken)
        except CertificateError:
            caught += 1
    require(caught == len(paths) + 2, "tamper suite failed open")
    return caught


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper", action="store_true")
    args = parser.parse_args()
    certificate = summarize()
    validate(certificate)
    if args.tamper:
        print(f"TAMPER: PASS ({tamper_selftest(certificate)} mutations rejected)")
    else:
        print(json.dumps(certificate, indent=2, sort_keys=True))
        print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
