# b2 (mod-p giant extras) — scoping summary: object, regime, and status

- **Status:** SCOPING / understanding contribution. No new threshold or bound is proved. All computational
  claims are cross-checked on ≥2 engines and adversarially reviewed (Codex). Dated 2026-07-06.
- **Purpose:** a self-contained account of *what the b2 max-fiber bound actually is, why it is open, and
  how it relates to the L1 lane* — the durable output of a focused investigation. Detailed trail (with the
  dated corrections that produced this understanding) is in the sibling notes referenced below.

## The object (verified against `experimental/cap25_cap_v13_raw.tex`)

b2 concerns the **max-fiber of the identity prefix map** `Φ_{m,w}: (D choose m) → 𝔅^w,
M ↦ ((-1)^h e_h(M))_{h≤w}` (`:7251`, `prob:capfpr-Q`), with `|D|=n`, `K=ρn`, `m=K+w`, denominator `|𝔅|^w`.
Its zero-fiber = the "t-null blocks" (subsets `B⊆μ_n` with `p_1..p_w=0`, by Newton `⟺ e_1..e_w=0`, valid
for `w < char 𝔅` — satisfied by the deployed rows, `w≈67466 ≪ p≈2^31`, `:7663`/`:7755`). CAP25 defines
`Φ`/`(Q)` and separates quotient/paid from aperiodic scales (`:7251`, `:7258`); the **specific `≤ n^3`
(`16 n^3`) budget** is a *repo-side conditional* framing (QA22/QA25/b1 packets), NOT a CAP25 theorem: it
bounds **only the residual** — the moment-trade + primitive-non-coset columns — after the exactly-counted
coset-union main term (b1 char-0 giant-coset theorem) and boundary column (QA.25) are peeled off. The
structured alternative is a **quotient stabilizer / block structure** (`:7543`), an **open `n^C`
inverse-theorem target — not proved**, and `:7217` requires explicit `C` + constants inside the finite
margin (poly-loss is not a certificate).

## The regime (verified) — dense, band depth, OPEN at every deployed row

- **Deployed prefix depth** is `w ≈ 4096` (MCA, `:5149`) to `w = 67470/67446` (list frontier, `:6944`) —
  NOT the small `w` a naive reading suggests. So the deployed regime is **near-full-entropy / ultra-dense**
  (`C(n,m) ≈ p^w·2^192` ⟹ mean fiber `≈ 2^192`, `:8471`), not rare-event.
- **Proved head-depth bound is tiny:** `w_0 = 21–22` (KoalaBear) / `10–11` (Mersenne-31) — the proof
  "pays one Weil cost `√p` per power sum, and this is exactly what stops it at `w_0=21–22`" (`:7111`, `:8158`).
- **Therefore b2 is OPEN at every deployed row** (`w = 4096–67470 ≫ w_0`), and even a poly-loss bound does
  not decide the printed adjacent pairs (finite margins 22.2/22.0/3.3/3.1 bits — need the constant-factor
  `(1+o(1))`-of-mean form, `:7115`).

## What b2 really is (verified, `:8471`)

`(Q)` = **balanced subset-sum equidistribution on a moment curve** `v_ξ=(ξ, ξ²/2, …, ξ^w/w)` at near-full
entropy = the **function-field analogue of equidistribution of the divisors of a fixed polynomial in
residue classes / short intervals**, at effective modulus `(#divisors)^{1-o(1)}` (band depth). Closing it
needs **square-root cancellation twice** over the `p^w` frequencies — the per-power-sum layer (Weil/Parseval)
is provably insufficient (`:7367`), and the missing input is *horizontal (among-tuple)* cohomological
cancellation. The target is **open even over ℤ** (`:8471`; the corresponding ℤ divisor-in-residue-classes
exponent of distribution is far below near-full modulus — e.g. `θ_3 = 9/17` for the ternary divisor
function, Fouvry–Kowalski–Michel).

## b2 and L1: a shared barrier (not a proved equivalence)

The b2 giant-extras bound and the L1 `E₃ ≤ ℓ−2` max-fiber ceiling **share the same `√p` barrier and
inverse-theorem framing** (`:7367`, `:7543`, `:8471`): per-frequency Weil is insufficient in both, and b2
stops at head depth `w_0=21` for the same reason L1 route A hit the wall. This is a shared obstruction and
framing — **no equivalence or difficulty-class theorem is proved**; the two reductions are independent and
land on structurally analogous additive-combinatorics / cohomological cores.

## Routes found insufficient at toy scale (with evidence)

- **Geometric / Katz-equidistribution via the pencil monodromy: BLIND (toy ℓ=11,13).** The pencil
  `G = Gal(X^{ℓ-1}−t·γ / 𝔽_p(t))` is the *full symmetric group* for both extremal (`E₃=ℓ−2`) and random
  (`E₃=0`) Γ: for the **extremal** cases a rigorous GAP transitive-subgroup filter leaves only `S_10`/`S_12`,
  and the random cases are Chebotarev-consistent with the same — so monodromy does not distinguish the
  extremal structure (`b2_l1_pencil_monodromy_v2.sage`).
- **Per-character / Cauchy–Schwarz bounds:** insufficient at scale (per-character `|S_b(c)|` and the L²
  diagonal both overshoot the target).
- **Off-the-shelf BGK / Bourgain–Chang:** wrong regime (dense vs sparse subgroup) and/or wrong precision.

These are evidenced observations at toy/deployed scale, not impossibility theorems.

## Process contribution: the regime-first verification protocol

The investigation produced a durable checklist (`b2_verification_protocol.md`) after a wrong-regime toy
model passed every code-review (code-correct ≠ claim-valid). Its Step 0 — *pin the deployed object +
parameters from the primary source and check the claim's arithmetic there before trusting any toy* — is what
caught the regime error and is generally applicable to scaling/asymptotic claims.

## Reproducibility (Codex-green scripts)
`experimental/scripts/b2_regime_check.py` (the regime restriction), `b2_bound_mechanism.py` (the reduction
mechanism), `b2_l1_pencil_monodromy_v2.sage` (monodromy-blind, GAP-certified), `b2_prong1_fixed_b.py`,
`b2_charsum_crosscheck.py`, `b2_l1_saturator_structure.sage`. Detailed trail:
`b2_modp_giant_extras_first_move.md`, `b2_step0_object_pinned.md`, `b2_l1_shared_core.md`,
`b2_l1_lemma_draft.md`, `b2_verification_protocol.md`.

## Honest scope
No bound is proved. This is a **partial / complementary scoping contribution**: it pins the object and the
deployed regime, shows the bound is open at every deployed depth (divisor equidistribution, `√p` barrier),
identifies the b2≡L1 shared core, rules out three routes with evidence, and supplies a reusable
verification protocol.
