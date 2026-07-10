import AsymptoticSpine.AddBack

namespace AsymptoticSpine

/-!
# Shared averaging / pigeonhole core (reroute #442 and window #443)

Stdlib-only (no mathlib) combinatorial engine shared by the two audit-corner
repairs of `experimental/asymptotic_rs_mca.tex` formalized in `Reroute.lean`
(PR #442 lower-side reroute) and `Window.lean` (PR #443 window uniformity).  Both
repairs turn on the *same* elementary fact — **a total distributed over a bounded
number of buckets forces some bucket to be large / some element to be small** — so
it is factored here once:

* `listSum_le_length_mul_listMax` — `∑ ≤ (#terms)·max`, the "log of a sum ≤ log
  count + log max" inequality cleared of logs; the pigeonhole floor and the
  bounded-complexity budget bound both reduce to it.
* `length_mul_le_listSum_map` — its dual `(#terms)·min-bound ≤ ∑`, the Markov /
  averaging direction.
* `partition_sum` / `pigeonhole_floor` — the exact fibre decomposition of a list
  under a key with `≤ P` values, and the resulting `total ≤ P·maxFibre` floor
  (the `lem:capff1-identity-prefix-floor` pigeonhole `M ↦ (e_j(M))_{j≤w}` into
  `|B|^w` prefix classes).
* `markov_count` / `exists_lt_of_listSum_lt` — Markov's inequality (few reservoir
  elements exceed a threshold) and the existence of a sub-threshold element when
  the total mass is subcritical (the `thm:A` reservoir-averaging over `Ω=F∖D`).
* `nodup_map_of_injective` — an injective image of a duplicate-free list is
  duplicate-free (the *collision-free* content: the identity-prefix map keeps the
  `binom(n,m)` codewords distinct, unlike the raw pole map which collapses them).

Kernel-checked, stdlib-only, no mathlib.  Reuses `AddBack.listMax` and the
`Util.listSum` list scaffolding.
-/

/-! ## `∑ ≤ (#terms)·max` and its Markov dual -/

/-- **Sum bounded by count times max.**  `∑_x l_x ≤ |l|·(max_x l_x)`.  Cleared of
logs this is "`log ∑ ≤ log(#terms) + log(max term)`", the inequality behind both
the pigeonhole floor (`total ≤ P·maxFibre`) and the bounded-complexity budget
bound (`log U ≤ log P + log max`). -/
theorem listSum_le_length_mul_listMax : ∀ l : List Nat, listSum l ≤ l.length * listMax l := by
  intro l
  induction l with
  | nil => simp
  | cons a t ih =>
    have hmax : listMax t ≤ listMax (a :: t) := by rw [listMax_cons]; exact Nat.le_max_right _ _
    have ha : a ≤ listMax (a :: t) := by rw [listMax_cons]; exact Nat.le_max_left _ _
    have ht : listSum t ≤ t.length * listMax (a :: t) :=
      Nat.le_trans ih (Nat.mul_le_mul (Nat.le_refl _) hmax)
    rw [listSum_cons, List.length_cons, Nat.add_mul, Nat.one_mul]
    omega

/-- **Count times lower-bound is at most the sum** (the averaging dual).  If every
member `f x` is at least `B`, then `|l|·B ≤ ∑_x f x`.  Contrapositive of "the
average is `≥ B`". -/
theorem length_mul_le_listSum_map {α : Type} (f : α → Nat) (B : Nat) :
    ∀ l : List α, (∀ x ∈ l, B ≤ f x) → l.length * B ≤ listSum (l.map f) := by
  intro l
  induction l with
  | nil => intro _; simp
  | cons a t ih =>
    intro h
    have ha : B ≤ f a := h a List.mem_cons_self
    have ht := ih (fun x hx => h x (List.mem_cons_of_mem _ hx))
    rw [List.map_cons, listSum_cons, List.length_cons, Nat.add_mul, Nat.one_mul]
    omega

/-! ## Indicator sums over a nodup key list -/

/-- The indicator sum of a value `c` **absent** from `ks` is `0`. -/
theorem indicator_sum_zero (c : Nat) :
    ∀ ks : List Nat, c ∉ ks → listSum (ks.map (fun v => if c = v then 1 else 0)) = 0 := by
  intro ks
  induction ks with
  | nil => intro _; simp
  | cons b rest ih =>
    intro h
    have hb : c ≠ b := fun hh => h (hh ▸ List.mem_cons_self)
    have hr : c ∉ rest := fun hh => h (List.mem_cons_of_mem _ hh)
    rw [List.map_cons, listSum_cons, if_neg hb, ih hr]

/-- The indicator sum of a value `c` **present once** in a duplicate-free `ks` is
`1`: `∑_{v∈ks} [c = v] = 1`.  (This is where `ks.Nodup` — the buckets are indexed
by *distinct* key values — enters the partition identity.) -/
theorem indicator_sum_one (c : Nat) :
    ∀ ks : List Nat, ks.Nodup → c ∈ ks →
      listSum (ks.map (fun v => if c = v then 1 else 0)) = 1 := by
  intro ks
  induction ks with
  | nil => intro _ h; simp at h
  | cons b rest ih =>
    intro hnd hmem
    have hbnr : b ∉ rest := (List.nodup_cons.mp hnd).1
    have hrest : rest.Nodup := (List.nodup_cons.mp hnd).2
    rw [List.map_cons, listSum_cons]
    rcases List.mem_cons.mp hmem with hcb | hcr
    · -- c = b: head contributes 1, tail all zero (c = b ∉ rest)
      subst hcb
      rw [if_pos rfl, indicator_sum_zero c rest hbnr]
    · -- c ∈ rest, so c ≠ b (else b ∈ rest)
      have hcb : c ≠ b := fun hh => hbnr (hh ▸ hcr)
      rw [if_neg hcb, ih hrest hcr]

/-- `listSum` distributes over a pointwise sum of two maps. -/
theorem listSum_map_add {α : Type} (X Y : α → Nat) :
    ∀ l : List α, listSum (l.map (fun v => X v + Y v))
      = listSum (l.map X) + listSum (l.map Y) := by
  intro l
  induction l with
  | nil => simp
  | cons a t ih =>
    simp only [List.map_cons, listSum_cons, ih]
    omega

/-- `listSum` of an all-zero map is `0`. -/
theorem listSum_map_zero {α : Type} (l : List α) :
    listSum (l.map (fun _ => (0 : Nat))) = 0 := by
  induction l with
  | nil => rfl
  | cons a t ih => rw [List.map_cons, listSum_cons, ih]

/-! ## Fibre partition and the pigeonhole floor -/

/-- **Partition identity.**  Let `key : α → ℕ` assign each element of `l` a bucket
value lying in a duplicate-free index list `ks` (every `key x ∈ ks`).  Then the
fibre sizes `|{x∈l : key x = v}|` sum, over `v∈ks`, to `|l|`: the buckets partition
`l`.  This is the counting content of the prefix decomposition
`M ↦ (e_j(M))_{1≤j≤w} ∈ B^w` in `lem:capff1-identity-prefix-floor`. -/
theorem partition_sum {α : Type} (key : α → Nat) (ks : List Nat) (hnd : ks.Nodup) :
    ∀ l : List α, (∀ x ∈ l, key x ∈ ks) →
      listSum (ks.map (fun v => (l.filter (fun x => decide (key x = v))).length)) = l.length := by
  intro l
  induction l with
  | nil =>
    intro _
    have hmap : (ks.map (fun v => (([] : List α).filter (fun x => decide (key x = v))).length))
        = ks.map (fun _ => 0) := by
      apply List.map_congr_left; intro v _; simp
    rw [hmap]; exact listSum_map_zero ks
  | cons a t ih =>
    intro hmem
    have hcov : ∀ x ∈ t, key x ∈ ks := fun x hx => hmem x (List.mem_cons_of_mem _ hx)
    have hka : key a ∈ ks := hmem a List.mem_cons_self
    -- each bucket splits: |{a::t : key=v}| = [key a = v] + |{t : key=v}|
    have hsplit : (ks.map (fun v => ((a :: t).filter (fun x => decide (key x = v))).length))
        = ks.map (fun v => (if key a = v then 1 else 0)
            + (t.filter (fun x => decide (key x = v))).length) := by
      apply List.map_congr_left
      intro v _
      rw [List.filter_cons]
      by_cases hv : key a = v
      · rw [if_pos (by simpa using hv), if_pos hv, List.length_cons]; omega
      · rw [if_neg (by simpa using hv), if_neg hv]; omega
    rw [hsplit,
      listSum_map_add (fun v => if key a = v then 1 else 0)
        (fun v => (t.filter (fun x => decide (key x = v))).length) ks,
      indicator_sum_one (key a) ks hnd hka, ih hcov, List.length_cons]
    omega

/-- **Pigeonhole floor (cleared).**  With the fibre buckets over a `≤ P`-value key,
`|l| ≤ P · maxFibre`, i.e. the largest fibre has `≥ ⌈|l|/P⌉` elements.  This is
`lem:capff1-identity-prefix-floor` at the abstract level: `binom(n,m)` items keyed
by their length-`w` prefix into `|B|^w = P` classes force a class of size
`≥ ⌈binom(n,m)/|B|^w⌉`. -/
theorem pigeonhole_floor {α : Type} (key : α → Nat) (ks : List Nat) (hnd : ks.Nodup)
    (P : Nat) (hP : ks.length ≤ P) (l : List α) (hmem : ∀ x ∈ l, key x ∈ ks) :
    l.length ≤ P *
      listMax (ks.map (fun v => (l.filter (fun x => decide (key x = v))).length)) := by
  have hsum := partition_sum key ks hnd l hmem
  have hbound := listSum_le_length_mul_listMax
    (ks.map (fun v => (l.filter (fun x => decide (key x = v))).length))
  rw [List.length_map] at hbound
  calc l.length
      = listSum (ks.map (fun v => (l.filter (fun x => decide (key x = v))).length)) := hsum.symm
    _ ≤ ks.length * listMax (ks.map (fun v => (l.filter (fun x => decide (key x = v))).length)) :=
        hbound
    _ ≤ P * listMax (ks.map (fun v => (l.filter (fun x => decide (key x = v))).length)) :=
        Nat.mul_le_mul hP (Nat.le_refl _)

/-! ## Reservoir averaging (Markov) -/

/-- **Markov's inequality (cleared).**  The number of reservoir elements whose mass
`f α` reaches the threshold `B`, times `B`, is at most the total mass:
`|{α : B ≤ f α}| · B ≤ ∑_α f α`.  "Most reservoir elements have bounded
collisions": at most `(∑ f)/B` of them exceed the threshold. -/
theorem markov_count {α : Type} (f : α → Nat) (B : Nat) :
    ∀ l : List α,
      (l.filter (fun x => decide (B ≤ f x))).length * B ≤ listSum (l.map f) := by
  intro l
  induction l with
  | nil => simp
  | cons a t ih =>
    rw [List.map_cons, listSum_cons, List.filter_cons]
    by_cases hc : B ≤ f a
    · rw [if_pos (by simpa using hc), List.length_cons, Nat.add_mul, Nat.one_mul]
      omega
    · rw [if_neg (by simpa using hc)]
      omega

/-- **Sub-threshold element exists.**  If the total reservoir mass is strictly
below `B` per element (`∑_α f α < B·|l|`), then some reservoir element carries mass
`< B`.  This is the averaging existence behind `thm:A`'s reservoir step: a pole
with few collisions exists once the total collision mass is subcritical. -/
theorem exists_lt_of_listSum_lt {α : Type} (f : α → Nat) (B : Nat) (l : List α)
    (h : listSum (l.map f) < B * l.length) : ∃ x ∈ l, f x < B := by
  rcases Classical.em (∃ x ∈ l, f x < B) with hyes | hno
  · exact hyes
  · exfalso
    have hall : ∀ x ∈ l, B ≤ f x := by
      intro x hx
      rcases Nat.lt_or_ge (f x) B with hlt | hge
      · exact absurd ⟨x, hx, hlt⟩ hno
      · exact hge
    have hml := length_mul_le_listSum_map f B l hall
    rw [Nat.mul_comm] at hml
    omega

/-! ## Collision-free content: injective image stays duplicate-free -/

/-- **Injective ⇒ duplicate-free image.**  An injective map sends a duplicate-free
list to a duplicate-free list.  This is the collision-free content of
`lem:capff1-identity-prefix-floor`: the identity-prefix map `M ↦ c_M` is injective
(locator identity), so the `binom(n,m)` codewords stay distinct — the raw pole map
`S ↦ ℓ_S(α)` is *not* injective and collapses them (contrast in `Reroute.lean`). -/
theorem nodup_map_of_injective {α β : Type} {f : α → β} (hf : Function.Injective f) :
    ∀ {l : List α}, l.Nodup → (l.map f).Nodup := by
  intro l h
  exact List.pairwise_map.2 (h.imp (fun hab habf => hab (hf habf)))

end AsymptoticSpine
