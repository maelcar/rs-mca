#!/usr/bin/env python3
"""Replay the finite rank-16 zero-profile scalar-line route cut.

The verifier uses integer arithmetic and a deterministic integral max-flow
compiler for all 2,607 deployed delta cells. It does not claim a ledger
payment or enumerate the full unowned complement.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass


P = 2_130_706_433
N = 2_097_152
K = 1_048_576
M = 1_116_047
B = 32_768
BLOCKS = 64
LINE_SIZE = 15
T = 981_105
ELL = 67_472
KAPPA_ERROR = 913_633
DELTA_MAX = 2_606
SWITCH_DELTA = 1_758


class VerificationError(RuntimeError):
    """Raised when a replay obligation fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def ceil_div(numerator: int, denominator: int) -> int:
    require(denominator > 0, "nonpositive ceiling denominator")
    return -(-numerator // denominator)


@dataclass
class Edge:
    to: int
    reverse: int
    capacity: int


class Dinic:
    """Small deterministic integral max-flow implementation."""

    def __init__(self, nodes: int) -> None:
        self.graph: list[list[Edge]] = [[] for _ in range(nodes)]

    def add_edge(self, source: int, target: int, capacity: int) -> int:
        require(capacity >= 0, "negative edge capacity")
        forward_index = len(self.graph[source])
        self.graph[source].append(Edge(target, len(self.graph[target]), capacity))
        self.graph[target].append(Edge(source, forward_index, 0))
        return forward_index

    def maximum_flow(self, source: int, sink: int) -> int:
        total = 0
        nodes = len(self.graph)
        while True:
            level = [-1] * nodes
            level[source] = 0
            queue = deque([source])
            while queue:
                vertex = queue.popleft()
                for edge in self.graph[vertex]:
                    if edge.capacity and level[edge.to] < 0:
                        level[edge.to] = level[vertex] + 1
                        queue.append(edge.to)
            if level[sink] < 0:
                return total

            cursor = [0] * nodes

            def send(vertex: int, amount: int) -> int:
                if vertex == sink:
                    return amount
                while cursor[vertex] < len(self.graph[vertex]):
                    edge = self.graph[vertex][cursor[vertex]]
                    if edge.capacity and level[edge.to] == level[vertex] + 1:
                        pushed = send(edge.to, min(amount, edge.capacity))
                        if pushed:
                            edge.capacity -= pushed
                            self.graph[edge.to][edge.reverse].capacity += pushed
                            return pushed
                    cursor[vertex] += 1
                return 0

            while True:
                pushed = send(source, 1 << 60)
                if not pushed:
                    break
                total += pushed


def balanced(total: int, slots: int) -> list[int]:
    quotient, remainder = divmod(total, slots)
    return [quotient + int(index < remainder) for index in range(slots)]


def compile_transport(
    core: list[int],
    remainder: list[int],
    diagonal: list[int],
    petal_size: int,
    mutate_column: bool,
) -> list[list[int]]:
    source = 0
    row_offset = 1
    column_offset = row_offset + LINE_SIZE
    sink = column_offset + BLOCKS
    network = Dinic(sink + 1)
    edge_index: list[list[int | None]] = [
        [None] * BLOCKS for _ in range(LINE_SIZE)
    ]

    total_row_demand = 0
    for row in range(LINE_SIZE):
        demand = petal_size - diagonal[row]
        require(demand >= 0, "negative residual petal demand")
        network.add_edge(source, row_offset + row, demand)
        total_row_demand += demand
        literal_block = row + 1
        for column in range(BLOCKS):
            if column == literal_block:
                continue
            capacity = B - core[column] - 1
            edge_index[row][column] = network.add_edge(
                row_offset + row, column_offset + column, capacity
            )

    total_column_demand = 0
    for column in range(BLOCKS):
        reserved = diagonal[column - 1] if 1 <= column <= LINE_SIZE else 0
        demand = B - core[column] - remainder[column] - reserved
        if mutate_column and column == 0:
            demand += 1
        require(demand >= 0, "negative residual column demand")
        network.add_edge(column_offset + column, sink, demand)
        total_column_demand += demand

    require(total_row_demand == total_column_demand, "transport demand balance")
    require(
        network.maximum_flow(source, sink) == total_row_demand,
        "transport saturation",
    )

    transport = [[0] * BLOCKS for _ in range(LINE_SIZE)]
    for row in range(LINE_SIZE):
        for column in range(BLOCKS):
            index = edge_index[row][column]
            if index is None:
                continue
            edge = network.graph[row_offset + row][index]
            transport[row][column] = network.graph[edge.to][edge.reverse].capacity
        transport[row][row + 1] = diagonal[row]
    return transport


def replay(mutation: str = "none") -> dict[str, object]:
    p = P
    omega = pow(3, 1_016, p)
    if mutation == "field-generator":
        omega += 1
    require(p - 1 == 127 * (1 << 24), "Proth factorization")
    require(127 < 1 << 24, "Proth size condition")
    require(pow(3, (p - 1) // 2, p) == p - 1, "Proth certificate")
    require(omega == 1_213_133_211, "deployed omega")
    require(pow(omega, N, p) == 1, "omega^n")
    require(pow(omega, N // 2, p) == p - 1, "omega exact order")
    zeta = pow(omega, B, p)
    require(zeta == 1_548_376_985, "deployed zeta")
    require(pow(zeta, 64, p) == 1, "zeta^64")
    require(pow(zeta, 32, p) == p - 1, "zeta exact order")

    scalar_cap = (N - (K - 1)) // (M - (K - 1))
    if mutation == "scalar-cap":
        scalar_cap += 1
    require(scalar_cap == LINE_SIZE, "scalar-line cap")
    c15_min = ceil_div(LINE_SIZE * M - N, LINE_SIZE - 1)
    c16_min = ceil_div(16 * M - N, 15)
    require(c15_min == 1_045_969, "15-line core floor")
    require(c16_min == 1_050_640 > K - 1, "16-line contradiction")

    delta_max = DELTA_MAX + int(mutation == "delta-endpoint")
    switch_delta = SWITCH_DELTA - int(mutation == "regime-switch")
    kappa_error = KAPPA_ERROR - int(mutation == "owner-threshold")
    require(delta_max == 2_606, "delta endpoint")
    require(switch_delta == 1_758, "regime switch")
    require(kappa_error == 913_633, "deployed error threshold")

    global_line_min = B
    global_line_max = 0
    global_companion_min = B
    global_companion_max = 0
    global_petal_block_max = 0
    endpoint_fingerprints: list[str] = []

    for delta in range(delta_max + 1):
        core_size = K - 1 - delta
        petal_size = ELL + delta + int(mutation == "agreement-exactness" and delta == 0)
        remainder_size = 36_497 - 14 * delta
        if mutation == "remainder-total" and delta == 0:
            remainder_size += 1
        require(remainder_size >= 0, "nonnegative exact remainder")
        require(
            core_size + LINE_SIZE * petal_size + remainder_size == N,
            "exact partition size",
        )

        core = [16_383 - delta] + [16_384] * (BLOCKS - 1)
        require(sum(core) == core_size, "core block total")
        remainder = balanced(remainder_size, BLOCKS)
        require(sum(remainder) == remainder_size, "remainder block total")

        if delta < switch_delta:
            root_fibre_size = 4_096
            diagonal = [root_fibre_size] * LINE_SIZE
            companion_remainder_total = 10_128 + delta
        else:
            root_fibre_size = 8_192
            diagonal = balanced(75_664 + delta, LINE_SIZE)
            companion_remainder_total = 0
        if mutation == "diagonal-reservation" and delta == 0:
            diagonal[0] -= 1
        require(root_fibre_size <= core[0], "root fibre inside core block")
        require(
            core[1] + root_fibre_size < B,
            "nonzero root fibre reservation",
        )
        if delta < switch_delta:
            require(diagonal == [4_096] * LINE_SIZE, "low diagonal roots")
            require(
                remainder_size - companion_remainder_total == 26_369 - 15 * delta,
                "low-regime leftover",
            )
        else:
            require(sum(diagonal) == 75_664 + delta, "high selected roots")
            require(max(diagonal) <= 5_218, "high selected-root fibre cap")

        transport = compile_transport(
            core,
            remainder,
            diagonal,
            petal_size,
            mutation == "column-demand" and delta == 0,
        )
        for row in range(LINE_SIZE):
            require(sum(transport[row]) == petal_size, "petal row sum")
            require(
                transport[row][row + 1] == diagonal[row],
                "literal diagonal root intersection",
            )
        for column in range(BLOCKS):
            require(
                core[column]
                + remainder[column]
                + sum(transport[row][column] for row in range(LINE_SIZE))
                == B,
                "block partition",
            )

        companion_remainder = balanced(companion_remainder_total, BLOCKS)
        require(
            all(
                companion_remainder[column] <= remainder[column]
                for column in range(BLOCKS)
            ),
            "companion remainder allocation",
        )

        companion_blocks = [
            core[column]
            - (root_fibre_size if column == 0 else 0)
            + (diagonal[column - 1] if 1 <= column <= LINE_SIZE else 0)
            + companion_remainder[column]
            for column in range(BLOCKS)
        ]
        require(
            sum(companion_blocks) == M,
            "nonlinear companion exact agreement total",
        )
        require(min(companion_blocks) > 0, "companion no empty block")
        require(max(companion_blocks) < B, "companion no complete block")

        cell_line_min = B
        cell_line_max = 0
        for row in range(LINE_SIZE):
            line_blocks = [
                core[column] + transport[row][column]
                for column in range(BLOCKS)
            ]
            require(sum(line_blocks) == M, "line exact agreement total")
            require(min(line_blocks) > 0, "line no empty block")
            require(max(line_blocks) < B, "line no complete block")
            cell_line_min = min(cell_line_min, min(line_blocks))
            cell_line_max = max(cell_line_max, max(line_blocks))
            global_petal_block_max = max(global_petal_block_max, max(transport[row]))

        cell_companion_min = min(companion_blocks)
        cell_companion_max = max(companion_blocks)
        global_line_min = min(global_line_min, cell_line_min)
        global_line_max = max(global_line_max, cell_line_max)
        global_companion_min = min(global_companion_min, cell_companion_min)
        global_companion_max = max(global_companion_max, cell_companion_max)

        require(34 * 16_384 + petal_size < K, "line 34-block K cut")
        require(32 * 16_384 + petal_size < K, "line 32-block K cut")
        require(29 * (B - cell_line_min) <= kappa_error, "line 29-block error cut")
        companion_noncore = M - (core_size - root_fibre_size)
        require(companion_noncore <= 78_270, "companion noncore cap")
        require(34 * 16_384 + companion_noncore < K, "companion 34-block K cut")
        require(32 * 16_384 + companion_noncore < K, "companion 32-block K cut")
        require(
            29 * (B - cell_companion_min) <= kappa_error,
            "companion 29-block error cut",
        )

        if delta in (0, 1_757, 1_758, 2_606):
            endpoint_fingerprints.append(
                f"{delta}:{cell_line_min}-{cell_line_max}:"
                f"{cell_companion_min}-{cell_companion_max}"
            )

    missed_core_floor = ceil_div(30_975, 14)
    require(missed_core_floor == 2_213, "missed-core floor")

    return {
        "p": P,
        "n": N,
        "K": K,
        "m": M,
        "omega": omega,
        "zeta": zeta,
        "scalar_line_cap": scalar_cap,
        "c15_min": c15_min,
        "c16_min": c16_min,
        "delta_range": f"0..{delta_max}",
        "missed_core_floor": missed_core_floor,
        "all_delta_transports": f"{delta_max + 1}/{delta_max + 1}",
        "max_petal_block": global_petal_block_max,
        "line_block_range": f"{global_line_min}..{global_line_max}",
        "companion_block_range": f"{global_companion_min}..{global_companion_max}",
        "endpoint_fingerprints": ",".join(endpoint_fingerprints),
        "displayed_candidates": 16,
        "current_complete_block_resource_mask_deficit": 0,
        "finite_ledger_charge": 0,
        "official_score": "0/2",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mutation",
        default="none",
        choices=(
            "none",
            "field-generator",
            "scalar-cap",
            "delta-endpoint",
            "regime-switch",
            "owner-threshold",
            "agreement-exactness",
            "remainder-total",
            "diagonal-reservation",
            "column-demand",
        ),
    )
    parser.add_argument("--self-test-mutations", action="store_true")
    args = parser.parse_args()
    if args.self_test_mutations:
        mutations = (
            "field-generator",
            "scalar-cap",
            "delta-endpoint",
            "regime-switch",
            "owner-threshold",
            "agreement-exactness",
            "remainder-total",
            "diagonal-reservation",
            "column-demand",
        )
        for mutation in mutations:
            try:
                replay(mutation)
            except VerificationError:
                print(f"MUTATION_CAUGHT={mutation}")
            else:
                raise VerificationError(f"mutation survived: {mutation}")
        print("ALL_MUTATIONS_CAUGHT")
        return

    values = replay(args.mutation)
    print("RANK16_ZERO_PROFILE_SCALAR_LINE_ROUTE_CUT_REPLAY")
    for key, value in values.items():
        print(f"{key}={value}")
    print("ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
