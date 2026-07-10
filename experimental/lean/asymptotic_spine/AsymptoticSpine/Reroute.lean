import AsymptoticSpine.Averaging

namespace AsymptoticSpine

/-!
# (R) Lower-side collision-free reroute — `lem:capff1-identity-prefix-floor` + `thm:A` (#442)

Stdlib-only (no mathlib) formalization of the two proved objects that PR #442
(`thresholds-lowerside-collision-free-reroute`; note
`experimental/notes/audits/asymptotic_lowerside_collision_free_reroute.md`) uses to
**reroute the lower side of `thm:frontier`** away from the unproved pole-collision
assertion.  Base `asymptotic_rs_mca.tex:283` justified
`B^{MCA}_C(m) ≥ exp(−o(n))·binom(n,m)·|B|^{−w}` by asserting the raw pole map
`S ↦ ℓ_S(α)=∏_{t∈S}(α−t)` has "subexponential collision loss in the standard
pole-reservoir regime" — a phrase that appears in **no source file** (audit r2 §A9,
ledger §B4 `FOUND-WEAKER`).  #442 replaces it with a *proved* two-step object:

1. the **collision-free identity-prefix floor** `lem:capff1-identity-prefix-floor`
   (`cap25_cap_v13_raw.tex:6909`): the map `M ↦ ((-1)^j e_j(M))_{1≤j≤w}` has codomain
   `B^w`, so **one prefix fibre holds `≥ ⌈binom(n,m)/|B|^w⌉` subsets**, and
   `M ↦ c_M := U_{z*} − Λ_M|_D` is **injective** (locator identity), so the fibre is
   `≥ ⌈binom(n,m)/|B|^w⌉` *distinct* codewords — no pole is evaluated, so there is no
   support collision;
2. the **reservoir averaging** of the deep-point conversion `thm:A`
   (`cap25_cap_v13_raw.tex:221`): `thm:A`'s own pole collisions live *among the `L`
   list codewords* (`P_i−P_j` has `≤ k` roots, so `≤ k·C(L,2)` collisions over the
   `q−n` reservoir poles `Ω=F∖D`), and **some reservoir pole realizes `L −` (its few
   collisions) distinct CA-bad slopes** — a *proved* lower bound replacing the
   asserted loss.

## Abstract content (what is and is not formalized)

The floor's numeric heart is the **pigeonhole** `Averaging.pigeonhole_floor`: the
prefix map into `|B|^w = P` classes forces a fibre of size `≥ ⌈binom(n,m)/|B|^w⌉`.
The collision-freeness is `Averaging.nodup_map_of_injective`: an injective codeword
map keeps the `binom(n,m)` subsets distinct (the raw pole map, being *non*-injective,
collapses them — the `462↦12` contrast of the note's Gate E, formalized in
`collision_contrast`).  The reservoir step is `Averaging.exists_lt_of_listSum_lt`:
bounded total collision mass ⇒ a low-collision pole exists ⇒ it realizes many
distinct slopes.

**Not formalized (honest boundary):** the RS/CA algebra that supplies the two
external facts — that `M ↦ c_M` *is* injective (the locator identity), and that the
distinct-slope count at a pole *is* `≥ L − coll(α)` (the `≤ k`-roots bound) — enters
as explicit hypotheses (`hinj`, and `hgood : ∀ α, L − coll α ≤ good α`), exactly as
`NoHighEnergy.lean` takes BSG/quasicube as hypotheses.  The `exp(o(n))` / ceiling and
`thm:A`'s `η`-slack bookkeeping stay over `Nat` in the package's cleared convention.

Stacks on the L1–L5 spine (#438), the B1 normalization (#440), and the A6 add-back
(#441 → this uses the shared `Averaging` core).  Kernel-checked, stdlib-only, no
mathlib.
-/

/-! ## Step 1 — the identity-prefix floor (pigeonhole over the prefix map) -/

/-- **(R1) `lem:capff1-identity-prefix-floor`, the floor.**  The `binom(n,m)` subsets
`M`, keyed by their length-`w` prefix `pfx M ∈ {0,…,P−1}` (`P = |B|^w`), have a prefix
fibre of size `≥ ⌈binom(n,m)/|B|^w⌉`, i.e. `binom(n,m) = |subsets| ≤ P · maxFibre`.
This is `pigeonhole_floor` at `ks = range P`; the count needs no injectivity (that is
Step 1b, distinctness of the resulting codewords). -/
theorem identity_prefix_floor {α : Type} (subsets : List α) (pfx : α → Nat) (P : Nat)
    (hpfx : ∀ M ∈ subsets, pfx M < P) :
    subsets.length ≤ P *
      listMax ((List.range P).map (fun z =>
        (subsets.filter (fun M => decide (pfx M = z))).length)) := by
  refine pigeonhole_floor pfx (List.range P) List.nodup_range P (by simp) subsets ?_
  intro M hM
  exact List.mem_range.mpr (hpfx M hM)

/-- **(R1b) collision-freeness.**  The identity-prefix codeword map `M ↦ c_M` is
injective (locator identity), so the `binom(n,m)` subsets yield `binom(n,m)` **distinct**
codewords: the map does not collide.  (Contrast `collision_contrast`: the raw pole map
is *not* injective and collapses the count.) -/
theorem identity_prefix_codewords_nodup {α β : Type} (subsets : List α) (code : α → β)
    (hinj : Function.Injective code) (hnd : subsets.Nodup) :
    (subsets.map code).Nodup :=
  nodup_map_of_injective hinj hnd

/-- Each prefix fibre is itself a duplicate-free list of codewords — a genuine
list-decoding list (`|Lst(…)| ≥ ⌈binom(n,m)/|B|^w⌉`), not a multiset. -/
theorem identity_prefix_fibre_nodup {α β : Type} (subsets : List α) (code : α → β)
    (pfx : α → Nat) (z : Nat) (hinj : Function.Injective code) (hnd : subsets.Nodup) :
    (((subsets.filter (fun M => decide (pfx M = z)))).map code).Nodup :=
  nodup_map_of_injective hinj (List.filter_sublist.nodup hnd)

/-! ## Step 2 — reservoir averaging (`thm:A`, over `Ω = F∖D`) -/

/-- **(R2a) Markov / "most poles have bounded collisions".**  Over the reservoir
`Ω=F∖D`, the number of poles whose collision count reaches a threshold `B`, times `B`,
is at most the total collision mass `T`.  So *at most `T/B`* reservoir poles are
high-collision — the averaging content of `thm:A`. -/
theorem reservoir_high_collision_few {γ : Type} (reservoir : List γ) (coll : γ → Nat)
    (T B : Nat) (hT : listSum (reservoir.map coll) ≤ T) :
    (reservoir.filter (fun α => decide (B ≤ coll α))).length * B ≤ T :=
  Nat.le_trans (markov_count coll B reservoir) hT

/-- **(R2b) `thm:A` reservoir distinct-slope floor.**  Model: a list-decoding list of
`L` codewords; at reservoir pole `α`, `coll α` codeword pairs collide and the distinct
CA-bad slope count is `good α ≥ L − coll α` (the `≤ k`-roots bound, taken as the
interface hypothesis `hgood`).  If the total collision mass is subcritical
(`∑_α coll α ≤ T < B·|Ω|`) with `B ≤ L`, then **some reservoir pole realizes more than
`L − B` distinct CA-bad slopes** — the proved replacement for the asserted
pole-collision loss. -/
theorem reservoir_distinct_slope_floor {γ : Type} (reservoir : List γ) (coll good : γ → Nat)
    (L T B : Nat)
    (hgood : ∀ α ∈ reservoir, L - coll α ≤ good α)
    (hmass : listSum (reservoir.map coll) ≤ T)
    (hsub : T < B * reservoir.length) (hBL : B ≤ L) :
    ∃ α ∈ reservoir, L - B < good α := by
  have hlt : listSum (reservoir.map coll) < B * reservoir.length := Nat.lt_of_le_of_lt hmass hsub
  obtain ⟨α, hα, hcoll⟩ := exists_lt_of_listSum_lt coll B reservoir hlt
  refine ⟨α, hα, ?_⟩
  have hg := hgood α hα
  omega

/-! ## The bridge — floor ∘ reservoir replaces the pole assertion -/

/-- **(R) The reroute bridge.**  Composition of Step 1 and Step 2, replacing
`asymptotic_rs_mca.tex:283`'s pole-collision assertion.  With
`L = maxFibre` the identity-prefix fibre size:

* (floor) `binom(n,m) = |subsets| ≤ P · L` — a fibre of `≥ ⌈binom(n,m)/|B|^w⌉` distinct
  codewords (`P = |B|^w`), **collision-free** (`hinj`);
* (reservoir) some pole `α ∈ Ω` realizes `> L − B` distinct CA-bad slopes,

so the CA-bad slope count is bounded **below** by an explicit floor with **no** bound on
the raw pole fibres `S ↦ ℓ_S(α)`.  `L` is threaded abstractly (its concrete value is the
`identity_prefix_floor` max fibre); the two external algebraic facts enter as `hinj`,
`hgood`. -/
theorem reroute_bridge {α β γ : Type}
    (subsets : List α) (code : α → β) (P : Nat)
    (reservoir : List γ) (coll good : γ → Nat) (L T B : Nat)
    (hinj : Function.Injective code) (hnd : subsets.Nodup)
    (hfloor : subsets.length ≤ P * L)
    (hgood : ∀ α ∈ reservoir, L - coll α ≤ good α)
    (hmass : listSum (reservoir.map coll) ≤ T)
    (hsub : T < B * reservoir.length) (hBL : B ≤ L) :
    (subsets.map code).Nodup ∧ subsets.length ≤ P * L ∧
      ∃ α ∈ reservoir, L - B < good α :=
  ⟨identity_prefix_codewords_nodup subsets code hinj hnd, hfloor,
    reservoir_distinct_slope_floor reservoir coll good L T B hgood hmass hsub hBL⟩

/-! ## Concrete certificates (closed by kernel `decide`)

### Gate E collision contrast (`462 ↦ 12`)

The note's Gate E (F_13, D={1..11}, K=3, m=5): the `binom(11,5)=462` subsets map to
`462` distinct codewords under the **injective** identity-prefix map, while the raw pole
map `S ↦ ℓ_S(0)` collapses them to `12` distinct values.  Compacted to a `decide`-sized
toy: an injective map keeps a duplicate-free image; a collapsing map does not. -/

/-- The six-element toy source (stand-in for the `462` subsets). -/
def toySrc : List Nat := [0, 1, 2, 3, 4, 5]

/-- **Collision contrast.**  An injective code (`M ↦ M+10`) keeps the toy source
duplicate-free (`Nodup`, the collision-free floor); a collapsing code (`M ↦ M mod 2`,
the raw-pole-map analogue) does **not** (`¬ Nodup`) — its image count crashes, exactly
the `462 ↦ 12` loss the reroute bypasses. -/
theorem collision_contrast :
    (toySrc.map (fun M => M + 10)).Nodup
    ∧ ¬ (toySrc.map (fun M => M % 2)).Nodup := by decide

/-- **Identity-prefix floor, worked.**  `total = 6` subsets keyed into `P = 2` prefix
classes by parity: fibres `[3,3]`, so `maxFibre = 3 ≥ ⌈6/2⌉` and the cleared floor
`6 ≤ 2·3` holds — via `identity_prefix_floor` (not `decide`). -/
theorem identity_prefix_floor_example :
    toySrc.length ≤ 2 *
      listMax ((List.range 2).map (fun z =>
        (toySrc.filter (fun M => decide (M % 2 = z))).length)) :=
  identity_prefix_floor toySrc (fun M => M % 2) 2 (by decide)

/-- The same fibre profile explicitly: parity buckets of `toySrc` are `[3,3]`, max `3`. -/
theorem identity_prefix_floor_fibres :
    (List.range 2).map (fun z => (toySrc.filter (fun M => decide (M % 2 = z))).length) = [3, 3] := by
  decide

/-! ### Reservoir distinct-slope floor, end-to-end -/

/-- A three-pole reservoir with collision counts `[0,1,0]` (total mass `1`), list size
`L = 4`, threshold `B = 2`.  Subcritical: `1 < 2·3`.  Distinct-slope counts
`good α = L − coll α = [4,3,4]`, all `≥ L − coll`. -/
def toyReservoir : List Nat := [0, 1, 2]
def toyColl : Nat → Nat := fun α => if α = 1 then 1 else 0
def toyGood : Nat → Nat := fun α => 4 - (if α = 1 then 1 else 0)

/-- **Reservoir floor, applied.**  `reservoir_distinct_slope_floor` fires on the toy:
some pole realizes `> L − B = 4 − 2 = 2` distinct CA-bad slopes (in fact `4`, at the two
collision-free poles). -/
theorem reservoir_floor_example :
    ∃ α ∈ toyReservoir, 4 - 2 < toyGood α :=
  reservoir_distinct_slope_floor toyReservoir toyColl toyGood 4 1 2
    (by decide) (by decide) (by decide) (by decide)

/-! ### Tamper witness — subcriticality is load-bearing

If the reservoir is **saturated** — every pole colliding at `≥ B` — no low-collision
pole exists and the distinct-slope floor is *false*.  This is the documented tamper:
weakening `hsub` (dropping subcriticality) makes the conclusion unprovable, witnessed
here by a saturated reservoir on which the conclusion literally fails. -/

/-- A saturated three-pole reservoir: every pole has `coll α = 2 = B`, so total mass
`6 = B·|Ω|` is **not** subcritical, and every distinct-slope count is `good α = L − B = 2`
— none exceeds `L − B`. -/
def satReservoir : List Nat := [0, 1, 2]
def satColl : Nat → Nat := fun _ => 2
def satGood : Nat → Nat := fun _ => 2

/-- **(Tamper) saturation kills the floor.**  The interface bound `good ≥ L − coll` holds
(`2 ≥ 4−2`) and the mass is exactly `B·|Ω|` (`6`, the non-strict boundary), yet **no** pole
realizes `> L − B` distinct slopes: `¬ ∃ α ∈ Ω, L − B < good α`.  So the strict
subcriticality `T < B·|Ω|` in `reservoir_distinct_slope_floor` is load-bearing. -/
theorem reservoir_saturated_falsifier :
    (∀ α ∈ satReservoir, 4 - satColl α ≤ satGood α)          -- interface bound holds
    ∧ listSum (satReservoir.map satColl) = 2 * satReservoir.length   -- mass = B·|Ω| (not subcritical)
    ∧ ¬ ∃ α ∈ satReservoir, 4 - 2 < satGood α := by decide

end AsymptoticSpine
