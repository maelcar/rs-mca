# CAP25 v13 Route-D shared barrier map v2

Status: `SYNTHESIS` / `REFERENCE` / `AUDIT`. This packet claims **no** new
mathematics. It composes the field's integrated Route-D / program-wide state at
tip `2b1a7e2` into a single obstruction map and **supersedes v1**
(`cap25_v13_route_d_barrier_map.md`, base `84b393e`), which is now stale by
roughly 25 packets and two maintainer papers. Every node, proved edge, and
dead route is a citation to an in-tree file; the one non-cited section
(SPECULATIVE EDGES) is fenced and labelled `ANALYSIS-CONJECTURAL`.

**Map + verifier.**
`experimental/data/cap25_v13_route_d_barrier_map_v2.json` (machine-readable
ledger) and `experimental/scripts/verify_route_d_barrier_map_v2.py` (zero-arg,
stdlib-only, `RDMAP2_AS_CAP_GB` / `RDMAP2_DATA_DIR` knobs; gates file-existence,
quote substrings, constant tokens, edge-DAG, count agreement, and the
proved/speculative fence, plus six tamper self-tests; `RESULT: PASS`, `< 30 s`).

## What this is / is not (merge framing)

This is **a provenance-gated map of the integrated Route-D / barrier state at tip
`2b1a7e2` — no closure claimed, no new bounds, no row-sharp Q claim.** Its value
is getting the implication structure exactly right and exhaustively sourced
across every contributor lineage as the day's packets landed. It:

- does **not** close `prob:row-sharp-q` (`grande_finale.tex` L2177) or
  `def:q-row-atom` (L2043);
- proves **no** deployed safe row — there is no `U(a_+) <= B^*` certificate here,
  and the maintainer promotes **no** deployed safe-row theorem;
- derives nothing new: every recorded status is a citation the verifier checks
  exists, and the only analytical content (four speculative edges) is fenced
  `ANALYSIS-CONJECTURAL`;
- records honest corrections where the field's shorthand had drifted ahead of the
  proofs — most sharply, the M31 degree-two LP is a **partial** cut (187 of
  3,254,885 pairs), **not** a saturation (see `AUD-LP-PARTIAL`); and the
  `(RC)/(MA)/(FI)/(PF)` tag system belongs to the entropy-frontiers draft, not
  to `asymptotic_rs_mca.tex` (see §7);
- reflects the tree at `2b1a7e2` and **decays as new work lands** — the node and
  edge set is a snapshot, not a standing theorem.

## Collaborative credit, by lineage

- **scottdhughes** — KB-MCA Route-D residual free-1 / A_SP card (#423), and the
  new **wall `|T| <= H2`** with its **`star3`** sub-wall pin/reduction/second-moment
  packets (#468/#479/#482/#484/#490), the **C9 major-arc value-set** (#465) and
  **Frobenius-closure Lean backing** (#466), and the **disjoint-PTE `D_d`** B1
  bridge (#448).
- **avdeevvadim** — singleton-heavy top-seam Route-D compiler (#425), and the
  **literal-C9 interface counterexample** + specification-repair floor (#444).
- **DannyExperiments** — M31 moment/Chebyshev floors (#424/#426), the **M31
  two-shell wall / integral-ratio lattice / degree-two LP / few-shell theorem**
  (#476/#480/#481/#495), and the **C9 restricted-payment / route-cut** family
  (#451/#463/#464/#485–#489).
- **holmbuar** — the row-sharp Q Fourier lineage (#407/#412/#414/#416/#417, the
  KB/M31 rung audits), the **KB mixed twist-orbit index ladder + L2 bound**
  (#467/#475/#477), the **M31 signed-`e_m` inverse `nu*_ref`** target, the
  **asymptotic Lean spine** (with LegaSage), and the **entropy-frontiers
  submission audit** (#494, in-flight).
- **LegaSage** — Lean asymptotic-spine co-formalization (with holmbuar).
- **AllenGrahamHart** (#405) — independent row-sharp Q calibration, cited as
  consistency context in #407.
- **maintainer** — the `grande_finale.tex` steering objects, the two asymptotic
  papers (`asymptotic_rs_mca.tex`, `rs_mca_entropy_frontiers.tex`), and the
  standing C9/split-pencil promotion gate.

## Deployed rows and steering objects (`grande_finale.tex`, quoted with lines)

- `def:q-row-atom` (L2043): `max_z |P_Q(z)| <= B*`. **The missing theorem.**
- `prob:row-sharp-q` (L2177): the row-overhead form; a moment proof must fit the
  finite margin.
- `prop:q-exact-target` (L2061): `B*_KB = 274980728111395087`,
  `B*_M31 = 16777215`; ratios `4807520.9295 / 4226236.5253 / 9.5722 / 8.4152` —
  **the binding Q problem is the Mersenne-31 list row** (~8.42x).
- Deployed rows: **KoalaBear MCA `a_+ = 1116048`** and **Mersenne-31 list
  `a_+ = 1116023`**. KB terminal-wall constant `H2 = 77291948627`, side `e = 67472`.

`TOTALS: nodes=59 proved_edges=28 speculative_edges=4 dead_routes=20`
(machine-checked against the JSON arrays by gate (e); `audit_nodes=12`,
`machine_checked_nodes=4`).

**Adjacent open PRs (post-tip, cited by number only; not in-tree at `2b1a7e2`).**
This map's genre now overlaps LegaSage's **#508** (`U_paid` partial per-cell
ledger + blocker map for `cor:capfr1-Q-R1-closing`) — that is a **Q-R1-cell paid
ledger**, distinct from this **program-wide Route-D / finite-wall obstruction
map**; #508 is a node-local companion of the avdeev top-seam paid-ledger genre
(`A0`..`A4`) and the `GF-ATOM` closing, not duplicated here. Live routes named
below have moved: the `star3` signed route is IN-FLIGHT (DannyExperiments
**#504**); the M31 two-shell modular F_p-nullity lever is a precise null
(holmbuar **#509**), leaving SDP/realizability last; and scottdhughes runs an
active entropy-inverse / Q1 reduction program (**#498/#501/#505**). See §7, §8b.

---

## 1. NODE LEDGER

IDs match the JSON. `SF` paths are repo-root-relative. Subsections 1a–1f are the
v1 nodes (carried over byte-identical, still valid at `2b1a7e2`); 1g–1n are the
day's new material.

### 1a. scottdhughes — KB-MCA Route-D residual free-1 / A_SP card (#423)

`H-DEPLOY` (deployed KB row, REFERENCE) · `H-V25` (free-1 disjoint, PROVED /
cross-high OPEN) · `H-V45` (residual card criteria, PROVED / gates OPEN) ·
`H-V46` (decomp PROVED / envelope REFUTED) · `H-V48` (e=2 CLOSED / e>=3 star
REFUTED) · `H-V49` (geometry PROVED) · `H-V51` (U2e PROVED / window OPEN) ·
`H-V53` (C_unique PROVED) · `H-V54` (terminal star PROVED; `|T|>>H2` for e>2) ·
**`H-WALL`** (STATUS: e>2 needs `|T| <= H2` — the standing wall; e=2 CLOSED;
alt-close `|R2| <= e·p`).

### 1b. avdeevvadim — singleton-heavy top-seam Route-D compiler (#425)

`A0` (conditional counting closure) · `A1`/`A2`/`A3`/`A4` (the four obligations) ·
`A397` (prefix-atom additive stratum, `|E_ret| <= 11440` imported-PROVED; the
open primitive full-rank certificate is the primal side of the holmbuar crux).

### 1c. DannyExperiments — M31 moment / Chebyshev floors (#424/#426)

`D-MOM` (mass-sensitive moment floor, PROVED / ROUTE-CUT) · `D-CHEB`
(`F_2048 = 6796405` exact floor) · `D-C1024` (m=67 even-defect wall, OPEN) ·
`D-RECON` (precision reconciliation, AUDIT).

### 1d. holmbuar — row-sharp Q Fourier lineage

`O407` (kappa <= 1.221 measured) · `O412` (`p^{w/2}` floor: every r=2 route dead
by 1,045,396.58 bits) · `O414` (`(STAR) <=> PR(Rhat) <= nu*`, `nu*_ref=2^44.39`;
L∞ dead) · `O416` (masked transfer, CONDITIONAL) · `O417` (lift-class model
REFUTED-DEAD) · `O-RUNGKB` (rung audit GREEN) · `O-RUNGM31` (rung audit NOT-GREEN).

### 1e. maintainer — grande_finale.tex steering objects

`GF-ATOM` (def:q-row-atom, OPEN target) · `GF-PROB` (prob:row-sharp-q, OPEN
target) · `GF-TARGET` (prop:q-exact-target budgets, REFERENCE).

### 1f. v1 audit / discrepancy-guard nodes

`AUD-TARGETFLOOR`, `AUD-384`, `AUD-M31MCA-CONV`, `AUD-RUNGROUND` (see §6).

### 1g. scottdhughes — wall `|T| <= H2` and its `star3` sub-wall (#468/#479/#482/#484/#490)

The v54 terminal star (`H-WALL`) is now pinned exactly, sliced to its smallest
honest sub-wall, and reduced to a signed-cancellation character-sum problem.

| id | source · section | statement | status | pins |
|---|---|---|---|---|
| `HW-WALL` | small_e · The wall pinned + witnesses | terminal `T` with distinct free-1 partner; open wall `\|T\| <= H2 = 77291948627` at e=67472; faithfulness pins F1–F4; **first deployed `T` members** (8 at e_s=3, `\|T(n',4)\|>=1972`); at e=67472 the exact load gate gives ~**1.34 million bits** of paucity margin | OPEN wall | 77291948627, 67472, 1972, 2000, 1344158 |
| `HW-STAR3` | star3 · The incidence reduction | smallest honest sub-wall `star3`: `\|T(n',3)\| <= H2`, trivial bound `C(n'-1,2)=700358019921` (admissible fraction `<= 0.110361`); a free-1 partner is a degree-2 PTE collision on the arc; **PROVED** `\|T(n',3)\| <= P`, recasting `star3` as the point-count `P <= H2` | OPEN sub-wall (reduction PROVED) | 77291948627, 700358019921, 8 |
| `HW-PC` | pointcount · Principal frequency IS the load | the `(0,0)` term equals exactly `floor 42623216888 = 0.551457·H2` — hughes's heuristic **`P_main = 0.5515·H2`** made an exact frequency — converting `P <= H2` into the explicit non-principal budget `P_err <= 0.448543·H2` | PROVED identity / bound OPEN | 42623216888, 0.551457, 700358019921, 0.448543 |
| `HW-L2` | star3_l2 · Second moment dead; signed route live | every absolute-value second-moment / large-sieve estimate on `P_err` is dead: T3/T2 Cauchy–Schwarz floor `5515.41·H2 = 12296x` the budget unconditionally (`sqrt=453080737874835`), large-sieve premise fails; the `psi(-u·zeta)` twist is load-bearing so `star3` needs **signed** cancellation (Weil/Kloosterman), not any absolute value — that signed route is now **IN-FLIGHT** (DannyExperiments #504, star3 torus Kloosterman reduction) | PROVED-DEAD (abs-value) / signed route IN-FLIGHT (#504) | 12296, 5515.41, 453080737874835 |

### 1h. DannyExperiments / holmbuar — M31 two-shell, LP, few-shell (#476/#480/#481/#495)

| id | source · section | statement | status | pins |
|---|---|---|---|---|
| `M31-FEWSHELL` | chebyshev_shells · few-shell lemma + one-shell cap | affine few-inner-product lemma ⇒ `\|F_z\| <= binom(n-w-1+s,s)`; deployed one-shell `max_z\|F_z\| <= n-w = 2029705 < B* = 16777215` (headroom 14747510); mass-aware `Gamma_l` bound; a faithful-toy **counterexample refutes the primitive-only-PR simplification** (quotient line carries `>98%` of L2 energy) | PROVED (lemma+cap) / primitive-PR REFUTED | 2029705, 16777215, 14747510 |
| `M31-2SHELL` | two_shell_wall · reduction + Seidel + lattice | a violation `L>B*` forces integral shell ratios; Seidel eigenvalue-multiplicity caps `2<=k<=774`; prefix rigidity leaves exactly **3254885** unresolved `(k,t)` pairs; the M31 prefix forces `dim_Fp ker(A+kI) >= 14747511` | PROVED (reduction+lattice) / deployed s=2 OPEN | 16777215, 2029705, 14747511, 774, 3254885 |
| `M31-LP` | integral_ratio_lp · degree-two spherical cut | a degree-two spherical-LP bound eliminates **exactly 187 of the 3,254,885** pairs; a genuine exact improvement but it **does not pay the whole two-shell cell** — **3254698 pairs OPEN**; the modular `-k` F_p-nullity lever is now a **precise null** (holmbuar #509), leaving **SDP/realizability** as the last lever | PROVED (partial cut) / OPEN | 187, 3254698, 3254885 |
| `M31-EMINV` | signed_em_inverse · nu*_ref from row constants | binding M31-list signed-`e_m` budget reduces to `PR(Rhat) <= nu*_ref = (K-1)^2 = 54.98531 = 2^5.781 ~ 55`, `K = 16777215/1993678 = 8.415208`; transfers to the Chebyshev domain, holds with room at toys; **the finite primitive effective-support theorem is the OPEN crux — the prize wall's binding instance** | REDUCED / crux OPEN | 54.98531, 8.415208, 16777215, 1993678 |

The modular **F_p-nullity certificate** on the 3,254,698 survivors is now a
**precise null** (holmbuar open PR #509), leaving **SDP/realizability** as the
only remaining lever on the two-shell cell. Both are cited by PR number; neither
is an integrated result at this tip, so neither carries a node here.

### 1i. holmbuar / scottdhughes — KB mixed twist-orbit + disjoint-PTE (#467/#475/#477/#448)

| id | source · section | statement | status | pins |
|---|---|---|---|---|
| `KB-LADDER` | index_ladder · coset-split bound + ceiling | the KB inverse narrowed to a mixed twist-orbit wall; **PROVED** the coset-split refinement beats plain Cauchy–Schwarz by at most `sqrt(index)`; at deployed `index = (p-1)/2^21 = 1016`, `sqrt(1016)=31.87x=4.994 bits` — a **sub-6-bit** polish that cannot cross the ~`1.045e6`-bit second-moment deficit | PROVED (ceiling) / deployed OPEN | 1016, 31.87, 4.994 |
| `KB-L2` | mixed_orbit_l2 · exact energy + open scope | exact mixed-axis Parseval identity + twist-orbit Cauchy–Schwarz give an upward-rational L2→L1 ceiling uniform over the index-3 coset family; **does not** transfer to index 1016 — the **remaining atomic input** is a deployed mixed collision-energy/tail bound beating the finite margin without the dead second moment | PROVED (toy) / deployed atom OPEN | 3, 1016 |
| `KB-PTE` | b1_bridge · the `d>w` tail | the **disjoint-PTE `D_d` law**: `D_d` = ordered disjoint `d`-subset pairs matching `p_1..p_w` (size-`d`, degree-`w` PTE trade); base `D_d=0` for `1<=d<=w` **machine-checked** (`pte_rigidity`); the named OPEN step is `D_d = C(N,d)C(N-d,d)Q^{-w}(1+o(1))` for every `d>w` — a second moment, strictly easier than the fourth-moment PR crux; the adjacent controller of the KB mixed-orbit atom | PROVED-anchor (base) / `d>w` tail OPEN | — |

### 1j. C9 / split-pencil corner

| id | source · section | statement | status | pins |
|---|---|---|---|---|
| `C9-CE` | c9_literal_counterexample (#444) | an explicit Boolean family meets every printed `def:primitive-leaf` hypothesis with **exponentially growing** image-normalized C9 moment — refuting the literal quantitative interface and setting a specification-repair floor; `C9 <=> primitive Q` on frontier leaves, so primitive Q is refuted too | COUNTEREXAMPLE / CONDITIONAL-BLOCKER | — |
| `C9-VALUESET` | c9_major_arc (#465) | signed-`e_m` major arcs concentrate on small value-set `c`; the cleanest family is `mu_d`-invariant and **`exp(Theta(n))`-large** (w=67471) — routing major arcs to C1–C8 must be structural, not a counting bound | MEASURED (structure) / not a C9 proof | 67471 |
| `C9-FROB` | c9_frobenius (#466) | **Lean, zero-sorry** (`powersum_rigidity`): `F_p`-coefficient polys are Frobenius-closed — the exact step PR #451 invokes — and the same primitive drives the Mersenne reciprocal-gap coset theorem and the disjoint-PTE base | PROVED (Lean) | — |
| `C9-PAY` | asymptotic_c9_frobenius_defect (#451) | pointwise Frobenius-orbit fiber bound; at `p=5, N=2^s` a constant image-normalized C9 cap depending only on `R/N` — pays C9 pointwise on that **strict char-5 dyadic subregime only**; representative of the #485–#489 payment family | RESTRICTED-PAYMENT (PROVED / strict subregime) | — |
| `C9-CUT` | asymptotic_c9_radial_route_cut (#485–#489) | a `p`-ary Delsarte/Krawtchouk radial-LP hierarchy (+ MDS-dual coset floor + shell caps) **cannot alone** prove `exp(o(N))` in the `kappa*N<=D<=N/2` regime — `exp(cN)`-large Johnson packings satisfy the whole radial package | ROUTE-CUT (in stated scope) | — |
| `C9-GATE` | asymptotic_rs_mca.md · Next action | **maintainer standing gate**: no C9/split-pencil residual is promoted to theorem status until the residual class is exhausted **and** the RC image bound is proved at the printed profile scale (restated in agents-log.md) | STANDING GATE / GUARD | — |

### 1k. asymptotic papers + entropy-frontiers audit

| id | source · section | statement | status | pins |
|---|---|---|---|---|
| `PAP-ASYMP` | asymptotic_rs_mca.tex · thm:frontier | the conditional profile-envelope frontier theorem: closed profile ledger + `def:ray-compiler` + Sidon residual payment + (identity-dominant case) explicit identity-dominance and target-adjusted-crossing hypotheses | CONDITIONAL | — |
| `PAP-FRONT` | entropy_frontiers.tex · admissible-sequence / ray-compiler | 5940-line submission draft; conditional compiler rests on `(A1)–(A7)`, side-conditions `(PF)/(MA)/(FI)`, and the sole formal hypothesis `(RC) = hyp:ray-compiler`; `(L1)–(L4)` are the `def:closed-asymptotic-ledger` items | SUBMISSION-DRAFT / CONDITIONAL | — |
| `AUD-FRONT` | entropy_frontiers.tex (audited by #494) | OPEN audit PR #494 (out-of-tree): theorem-by-theorem inventory of every conditional input; tally **33 NO-ISSUE / 2 FIXED / 1 exposition OPEN-GAP / 0 counterexample** across the 33 conditional-input instances | IN-FLIGHT / AUDIT | — |

### 1l. Lean coverage layer (machine-checked cores)

| id | source · section | statement | status | pins |
|---|---|---|---|---|
| `LEAN-SPINE` | lean_asymptotic_spine_note | `asymptotic_spine` (stdlib-only, v4.31.0) formalizes L1–L5 + B1 normalization + A6 add-back, **sorry-free** | MACHINE-CHECKED | — |
| `LEAN-M31` | lean_m31_few_shell | `m31_few_shell` formalizes the `M31-FEWSHELL` core incl. `2029705 < 16777215`, headroom `14747510`, mass-aware `Gamma_l`; no sorry/admit/custom axioms | MACHINE-CHECKED | 2029705, 16777215, 14747510 |
| `LEAN-GF` | lean_grande_finale_finite_q_tables | `grande_finale` finite-Q tables formalize the four row `(w, avg, B*)` triples and `thm:q-implies-sp`; proves **no** row-sharp Q max-fiber theorem and no safe row | MACHINE-CHECKED | 274980728111395087, 16777215 |

`C9-FROB` (`powersum_rigidity`) is the fourth machine-checked core; see §6b.

### 1m. new audit / boundary guards

`AUD-FIN-ASYMP` (finite-vs-asymptotic boundary), `AUD-LP-PARTIAL` (LP is a
partial cut, not a saturation), and `C9-GATE` (promotion gate) — see §6.

---

## 2. EDGE LEDGER — proved implications & preconditions

Each edge carries a verbatim quote (byte-checked by gate (b)) and its
file+section. **v1 edges (16), carried over:** `A1,A2,A3,A4 → A0`
(precondition); `H-V25 → H-V54`, `H-V53 → H-V54` (used-in-proof);
`H-V54 → H-WALL` (reduces-to), `H-V45 → H-WALL` (alternate-close);
`O412 → O414` (special-case-of), `O414 → O416` (transfers-to),
`O417 → O416` (resolves-condition-negatively); `O412 → A397`, `O414 → A397`
(same-object-dual-view, the shared cross-lineage sink); `D-CHEB → D-C1024`
(refines); `D-MOM → GF-PROB` (constrains); `GF-TARGET → GF-ATOM`
(provides-budget).

**New edges (12):**

- `HW-WALL → HW-STAR3` (names-subwall): *"named the **smallest honest sub-wall**"*.
- `HW-STAR3 → HW-PC` (reduces-to): *"recast `star3` as the point-count"*.
- `HW-PC → HW-L2` (reduces-to-tested-dead): *"reduced `star3` to a non-principal
  budget"* — where every absolute-value estimate then dies.
- `M31-FEWSHELL → M31-2SHELL` (paid-s1-left-s2): *"It paid `s=1` at M31 but left
  `s=2` open."*
- `M31-2SHELL → M31-LP` (partially-ruled-by): *"PR #480 reduces every first
  violating"* — the LP then eliminates 187 of the lattice.
- `KB-LADDER → KB-L2` (leaves-open-same-atom): *"the atomic input of `#475`"*.
- `KB-L2 → KB-PTE` (adjacent-to): *"The `d>w` tail of `E_mix` is the disjoint-PTE
  count"*.
- `C9-VALUESET → C9-CE` (structurally-explains): *"Why literal C9 is refuted
  (avdeevvadim #444)."*
- `C9-FROB → C9-PAY` (formalizes-step-of): *"This machine-checks the exact step
  PR #451 invokes"*.
- `C9-CE → C9-GATE` (motivates): *"a corrected theorem must exclude or pay the
  counterexample family"*.
- `C9-PAY → C9-GATE` (does-not-satisfy): *"No unrestricted C9 or primitive-Q
  theorem is proved."*
- `LEAN-M31 → M31-FEWSHELL` (formalizes): *"Checks `2029705 < 16777215` and
  headroom `14747510`"*.

The 28 proved edges form a DAG (gate (d)); `A397` remains the shared
cross-lineage Fourier/Route-D sink, and `C9-GATE` is the C9-corner sink.

## 2b. SPECULATIVE EDGES — `ANALYSIS-CONJECTURAL` (fenced; NOT proved)

> Plausible but not stated in any source; excluded from the proved graph by the
> verifier fence (gate (f)). Do not read them as established.

- `H-WALL ~ A0` (complementary-decomposition-of-same-A_SP-residual) — v1.
- `H-V25 ~ A2` (apparent-shift-pair-overlap) — v1.
- `D-C1024 ~ A2` (cross-row-planted-shift-pair-analogy) — v1.
- **`HW-L2 ~ O414` (signed-cancellation-vs-absolute-value analogy)** — NEW. Both
  walls collapse identically: on `star3` (`HW-L2`) every absolute-value second
  moment is proved dead and only signed (twisted Weil/Kloosterman) cancellation
  survives; on the Q atom (`O414`) the L∞ and r=2 routes are dead and only the
  signed-`e_m` inverse survives. The *"absolute-value dead, signed alive"*
  mechanism is structurally identical, but **no source identifies** the star3
  two-parameter twisted frequency object with the signed-`e_m` participation
  ratio — they live on different domains (KB terminal arc vs the Q max-fiber).

---

## 3. SINGLE-LEMMA FRONTIER (ranked)

Statements each of which, if proved, closes a **named** branch. **Global honest
ranking** (sharpest / closest to a branch closure first):

1. **[holmbuar] M31-list signed-`e_m` inverse** — `PR(Rhat) <= nu*_ref = 2^5.781
   ~ 55` (`M31-EMINV`). *Closes:* `def:q-row-atom` at **the binding row**
   (~8.42x) — the whole prize's binding instance. The sharpest, most concrete
   standalone finite target the program has. *Owner:* holmbuar.
2. **[scottdhughes] `star3` signed cancellation** — a Weil/Kloosterman-type bound
   for the two-parameter frequency family with the `psi(-u·zeta)` twist intact,
   giving `P_err <= 0.4485·H2` (`HW-L2`). *Closes:* the `star3` sub-wall — the
   smallest honest slice of the KB terminal wall. Uniquely well-isolated:
   **every** absolute-value / second-moment / large-sieve route is now *proved*
   dead, so the remaining obligation is pinned to exactly signed cancellation.
   **Now IN-FLIGHT** (DannyExperiments open PR #504, star3 torus Kloosterman
   reduction). *Owner:* scottdhughes analysis (#490) / DannyExperiments (#504).
3. **[holmbuar/DannyExperiments] M31 two-shell SDP / realizability cut** — after
   holmbuar #509 showed the modular F_p-nullity lever is a **precise null**, an
   SDP / realizability cut of the 3,254,698 LP-surviving `(k,t)` pairs is now the
   **only remaining lever** (`M31-2SHELL`, `M31-LP`; the mod-p nullity
   `dim_Fp ker(A+kI) >= 14747511` is exact but does not by itself cut the cell).
   *Closes:* the deployed `s=2` shell wall, completing the few-shell →
   deployed-fiber cap at M31. *Owner:* holmbuar / DannyExperiments.
4. **[scottdhughes] `|T| <= H2 = 77291948627`** — the KB terminal wall itself, as
   a **large-`e` paucity** theorem at `e=67472` (`HW-WALL`; `star3` is its `e_s=3`
   sub-wall). *Closes:* hughes's primary Route-D residual free-1 / A_SP card (via
   `H-V53`/`H-V54`, `|H_unt|=|T|`). *Alternate (same owner):* `|R2| <= e·p`.
5. **[holmbuar / avdeev-#397] KB max-fiber signed-`e_m` inverse** —
   `PR(Rhat) <= nu*_ref = 2^44.39` (`O414 → A397`). *Closes:* the **direct** KB-MCA
   row atom (`def:q-row-atom`) — the Fourier side of #397's primitive full-rank
   certificate. *Owner:* holmbuar (Fourier) / avdeevvadim (primal, #397).

Also live, per row: **[avdeevvadim]** each of `A1`/`A2`/`A3`/`A4` and
`weighted_primitive_sp_pade_bound` (the top-seam compiler's distinct KB Route-D
decomposition); **[holmbuar]** the KB mixed-orbit deployed collision-energy/tail
bound (`KB-L2`) and the disjoint-PTE `d>w` law (`KB-PTE`); **[DannyExperiments]**
the M31 `m=67` even-defect divisor count (`D-C1024`) and genuinely tighter M31-MCA
rung `L_1,L_2,L_3` (`O-RUNGM31`).

---

## 4. DEAD-ROUTE LEDGER

Everything proved dead / banked / refuted, with the killing citation (all quotes
byte-checked). **v1 dead routes (14), carried over:** `DR-O1` (any r=2 route,
1,045,396.58 bits) · `DR-O2` (uniform L∞, 2,090,815.35 bits) · `DR-O3` (lift-class
model REFUTED) · `DR-O4` (anticode fiber cap) · `DR-O5` (frequency-quotient mask
worsens) · `DR-D1` (moment-only below r-floor) · `DR-D2` (additive Chebyshev
stacking) · `DR-D3` (orbit amplification, L=1) · `DR-H1`..`DR-H6` (hughes v40–v54
false-envelope tourism).

**New dead routes (6):**

| id | route (owner) | status | killing citation |
|---|---|---|---|
| `DR-STAR3-L2` | absolute-value second-moment / large-sieve on the `star3` budget (scottdhughes #490) | PROVED-DEAD by `>=12296x` unconditionally | star3_l2 *"needs *signed* cancellation, not any absolute-value"* |
| `DR-STAR3-CS` | naive Cauchy–Schwarz / L2-energy (single-moment) in high-space (scottdhughes #484) | PROVED-DEAD by ~5862x | pointcount *"dead by `5862x`"* |
| `DR-KB-COSET` | coset-split refinement of Cauchy–Schwarz on the KB mixed-orbit L1 sum (holmbuar #477) | PROVED-CEILING at `sqrt(index)` (sub-6-bit at index 1016) | index_ladder *"sub-6-bit polish of Cauchy--Schwarz at the deployed index"* |
| `DR-M31-PRIMPR` | primitive-only participation ratio (delete every Chebyshev-fold direction) (DannyExperiments, #476 toy) | COUNTEREXAMPLE / ROUTE-CUT | chebyshev_shells *"delete every Chebyshev-fold direction, then prove PR_primitive <= nu*_ref"* — quotient line carries `>98%` of L2 energy |
| `DR-C9-LITERAL` | the literal quantitative C9 interface (avdeevvadim #444) | COUNTEREXAMPLE (new floor) | c9_literal *"COUNTEREXAMPLE_NEW_FLOOR for the literal quantitative interface."* |
| `DR-C9-RADIAL` | `p`-ary Delsarte/Krawtchouk radial-LP as a self-contained C9 route (DannyExperiments #485–#489) | ROUTE-CUT (in scope) | c9_radial *"nonnegative combinations of its inequalities cannot prove"* |

**Not a dead route (honest correction).** The M31 degree-two spherical **LP is
NOT saturated** — it is a *partial* cut (187 of 3,254,885 pairs), it is not stated
over Johnson harmonics, and the two-shell wall stays OPEN. Any "LP-over-Johnson
saturation" reading is unsupported by the source; recorded as `AUD-LP-PARTIAL`.

The task's named registry maps as: *unrestricted second moment* = `DR-O1`;
*dual-L∞* = `DR-O2`; *lift-class* = `DR-O3`; *coset-split sqrt(index) ceiling* =
`DR-KB-COSET`; *primitive-only PR* = `DR-M31-PRIMPR`; *absolute-value star3 second
moment* = `DR-STAR3-L2`; *naive single-moment cut* = `DR-STAR3-CS`;
*LP-over-Johnson-harmonics saturation* → **not established**, see `AUD-LP-PARTIAL`.

---

## 5. CROSS-ROW TABLE — KB row vs M31-list row

| object | KoalaBear MCA (`a_+=1116048`) | Mersenne-31 list (`a_+=1116023`) | transfers? |
|---|---|---|---|
| budget `B*` | `274980728111395087` (~22.20-bit margin) | `16777215` (~3.07-bit margin) | row-specific |
| binding ratio | `4807520.9295` | `8.4152` (**the binding row**) | row-specific |
| signed-`e_m` inverse target | `nu*_ref=2^44.39` (`O414`) | `nu*_ref=2^5.781~55` (`M31-EMINV`, binding) | transfers; `nu*` row-specific |
| terminal / shell wall | `\|T\| <= H2 = 77291948627` (`HW-WALL`); `star3` sub-wall | one-shell paid `2029705 < B*`; **s=2 wall** = 3,254,885-pair lattice (`M31-2SHELL`) | row-specific geometry (arc vs Chebyshev prefix) |
| best partial cut of the wall | star3 reduced to a point-count; abs-value dead (`HW-L2`) | degree-two LP cuts 187/3,254,885 (`M31-LP`); 3,254,698 OPEN | both leave a signed/nullity crux |
| coset method ceiling | `sqrt(index)`, sub-6-bit at index 1016 (`KB-LADDER`) | — | KB-specific |
| second-moment controller | disjoint-PTE `D_d` law (`KB-PTE`) | few-shell `Gamma_l` / integral-ratio lattice | analogous role, row-specific object |
| conj:Q rung audit | `1116048` **GREEN** (`O-RUNGKB`) | `1116024` **NOT-GREEN** (`O-RUNGM31`) | descent (D) PROVED both |

---

## 6. AUDIT / discrepancy nodes (conflation traps)

- **`AUD-TARGETFLOOR` (v1).** `target_floor = 274836936291722953 = K_rem·avg` is a
  **distinct object** from `B* = 274980728111395087`; the two Route-D lineages
  agree on `target_floor` to the digit — but must not be conflated with `B*`.
- **`AUD-384`, `AUD-M31MCA-CONV`, `AUD-RUNGROUND` (v1).** Resolved
  precision/convention pins; not open discrepancies.
- **`AUD-LP-PARTIAL` (NEW).** The M31 degree-two LP is a *partial* cut — 187 of
  3,254,885 pairs, 3,254,698 OPEN — **not** a saturation and **not** over Johnson
  harmonics. It *"does not pay the whole two-shell cell."* Guards against reading
  the LP ruleout as a closed wall.
- **`AUD-FIN-ASYMP` (NEW).** The **finite-vs-asymptotic boundary**: no deployed
  adjacent safe row is proved (only `def:q-row-atom` is the missing theorem), the
  asymptotic papers (`PAP-ASYMP`, `PAP-FRONT`) are CONDITIONAL, and the finite Q1
  wall (`def:q-row-atom` / `prob:row-sharp-q`, the signed-`e_m` inverses at KB
  `2^44.39` and M31 `~55`) remains **THE prize wall**, binding at the M31 list row.
  Guards against reading an asymptotic conditional result as a finite closure.
- **`C9-GATE` (NEW guard).** No C9/split-pencil residual is promoted until the
  residual class is exhausted **and** the RC image bound is proved at the printed
  profile scale.
- **Two-papers RC conflation (prose guard, no node).** `hyp:ray-compiler` and the
  `(RC)/(MA)/(FI)/(PF)` tag system are objects of
  `rs_mca_entropy_frontiers.tex`; `asymptotic_rs_mca.tex` uses `def:ray-compiler`
  (a *definition*) and unlabeled "major arcs" prose. The two RC objects are not
  the same and must not be cited interchangeably.

No source-vs-source contradiction on a constant or claimed implication was found.

## 6b. Machine-checked cores (Lean coverage)

Which map nodes have a machine-checked core (`experimental/lean/`):

- **`asymptotic_spine`** (`LEAN-SPINE`): L1–L5 + B1 normalization + A6 add-back,
  sorry-free — the asymptotic compiler spine (companion `Reroute`/`Window` modules
  have their own audit notes).
- **`m31_few_shell`** (`LEAN-M31` → `M31-FEWSHELL`): the few-shell lemma core and
  the deployed one-shell numeric cap `2029705 < 16777215`.
- **`grande_finale` finite-Q tables** (`LEAN-GF`): the four deployed-row budget
  triples and `thm:q-implies-sp`; proves **no** row-sharp Q theorem.
- **`powersum_rigidity`** (`C9-FROB`): power-sum rigidity + Frobenius closure +
  `pte_rigidity` — backs the C9 fiber bound (`C9-PAY`) **and** the disjoint-PTE
  base `D_d=0` (`KB-PTE`).

No machine-checked core touches a deployed *safe-row* theorem; the finite crux
(`def:q-row-atom`) and every OPEN wall above remain unformalized-because-unproved.

## 7. Finite-vs-asymptotic boundary (context)

The map spans two tracks joined at `AUD-FIN-ASYMP`. The **finite** track (KB /
M31 deployed rows) is where the prize wall lives: `def:q-row-atom` via the
signed-`e_m` inverses (`M31-EMINV`, `O414`), the hughes terminal wall / `star3`
(`HW-*`), the M31 shell walls (`M31-*`), and the KB mixed-orbit atom (`KB-*`). The
**asymptotic** track (`PAP-ASYMP`, `PAP-FRONT`, the C9 corner, the Lean spine) is
entirely CONDITIONAL: `thm:frontier` needs a closed profile ledger + `def:ray-
compiler` + Sidon payment; the submission draft needs `(A1)–(A7)`, `(RC)`, and the
numeric side-conditions; and the C9 residual is fenced by `C9-GATE`. The
`fp-span` entropy-inverse sibling arc
(`cap25_v13_entropy_inverse_fp_span_*`) is the asymptotic counterpart of the
holmbuar finite crux (context only; not re-derived here).

**scottdhughes entropy-inverse / Q1 reduction program (open, cited by PR
number).** The entropy-inverse corner of this boundary has an active reduction
lane: a Lean Li–Wan prefix-flatness power-sum core, the Li–Wan core of the
Fourier-flat payment (**#498**, zero-sorry); a zero-sorry Vandermonde-kills-
low-rank lemma plus an entropy-inverse Phase-0 reduction (**#501**); and a
referee-facing entropy-inverse crux roadmap (**#505**). These reduce the
asymptotic entropy-inverse crux that sits under `prob:entropy-inverse-q`; they
are post-tip and carry no in-tree node here.

## 8. Weave (sibling arcs this map does not re-derive)

Integrated files composed: scottdhughes v25–v54 + STATUS (#423), wall/`star3`
(#468/#479/#482/#484/#490), C9 major-arc/Frobenius (#465/#466), B1 bridge (#448);
avdeev topseam (#425), literal-C9 (#444); DannyExperiments moment/Chebyshev
(#424/#426), M31 two-shell/LP/few-shell (#476/#480/#481/#495), C9 payments
(#451/#463/#464/#485–#489); holmbuar #407/#412/#414/#416/#417, KB mixed-orbit
(#467/#475/#477), M31 signed-`e_m`, rung audits, Lean spine (with LegaSage),
entropy-frontiers audit (#494); the maintainer's two papers and steering objects.

## 8b. Adjacent open work (cited by PR number; not in-tree at `2b1a7e2`)

These PRs are open or post-tip; they carry **no** in-tree node/citation here (the
verifier only gates integrated files). They are recorded so lanes can see where
the named routes have moved:

- **#504** (DannyExperiments) — KoalaBear `star3` torus Kloosterman reduction: the
  signed-cancellation route named dead-only-for-absolute-value in `HW-L2`, now
  IN-FLIGHT (frontier #2).
- **#509** (holmbuar) — M31 modular nullity lever is a precise null; SDP is the
  last lever on the two-shell cell (updates `M31-LP` / frontier #3).
- **#508** (LegaSage) — `U_paid` partial per-cell ledger + blocker map for
  `cor:capfr1-Q-R1-closing`: a **Q-R1-cell paid ledger** (companion to the avdeev
  top-seam paid-ledger genre `A0`..`A4` and the `GF-ATOM` closing), **distinct**
  from this program-wide obstruction map — not duplicated here.
- **#498 / #501 / #505** (scottdhughes) — the active entropy-inverse / Q1
  reduction program (Li–Wan prefix-flatness core; Vandermonde-kills-low-rank +
  entropy-inverse Phase-0; entropy-inverse crux roadmap); see §7.

## 9. Reproduce

```bash
python3 experimental/scripts/verify_route_d_barrier_map_v2.py
#   RESULT: PASS  (< 30 s; six gates + six tamper self-tests)
```

## 10. Nonclaims (restated)

This packet does **not** prove `U(1116048) <= B*`, `U(1116023) <= B*`, any
deployed safe row, `prob:row-sharp-q`, `def:q-row-atom`, or any single node's open
lemma. It composes the integrated state at `2b1a7e2` into one provenance-gated
map, superseding v1. It claims no new mathematics; the four speculative edges are
`ANALYSIS-CONJECTURAL` and fenced out of the proved ledger. The M31 LP is a
partial cut, not a saturation; the F_p-nullity lever is in-flight; the asymptotic
papers are conditional. The map reflects the tree at `2b1a7e2` and decays as new
work lands.
