import AsymptoticSpine.Normalization

namespace AsymptoticSpine

/-!
# (A6) First-match add-back sufficiency — `lem:addback`, `def:profile-nondegen` (R1, R4)

Stdlib-only (no mathlib) formalization of the add-back profile-decomposition scope
of gap **A6** of `experimental/asymptotic_rs_mca.tex`, as shipped in **PR #441**
(`thresholds-addback-decomposition`; note
`experimental/notes/audits/asymptotic_addback_profile_decomposition.md`).  #441
scoped the uncited "profile decomposition" of `lem:addback` (L246–252) to a single
named geometric condition `def:profile-nondegen` and proved:

**R1 (add-back sufficiency).**  If the first-match leaves partition the primitive
residual, and leaf `j` carries mass `M_j`, image size `L_j`, and per-syndrome prefix
counts `N_j(s)`, with

* (a) **per-leaf Q, uniform** `max_s N_j(s)·L_j ≤ C·M_j`  (cleared `max_s N_j ≤ C·M_j/L_j`),
* (b) **image non-degeneracy** `L_j·C' ≥ Y`  (cleared `L_j ≥ Y/C'`, `Y = |𝒴|`),
* (c) **mass partition** `∑_j M_j ≤ Mtot`,

then  `max_s ∑_j N_j(s) · Y ≤ C·C'·Mtot`  (cleared `max_s N(s) ≤ C·C'·Mtot/Y`).  The
proof chain is: max-of-a-sum ≤ sum-of-maxes (`listMax_sum_le_sum_listMax`,
`globalMax_le_sum_leafMax`); the per-leaf clearing `N_j(s)·Y ≤ N_j(s)·L_j·C' ≤
C·M_j·C'` (`leaf_clear_chain`); and a telescope over the masses
(`addback_sum_bound`).  **No leaf-count bound is needed** — the mass partition alone
telescopes the sum.

**R4 (falsifier).**  Dropping image non-degeneracy (b) is *load-bearing*: there is a
leaf family with per-leaf Q (a) satisfied yet the global add-back violated by the
factor `Y`.  Following #441's witness (`addback_falsifier`): `Y` collapsed leaves
(each `L_j = 1`) all piled onto the same syndrome — per-leaf Q holds trivially, but
`max_s N(s) = Y·barN` blows up by `Y` over `barN_global`.  Spreading the images to
distinct syndromes (`addback_falsifier_repair`) restores the bound, confirming that
pile-up (violation of (b)), not per-leaf Q, is the failure.

## Modeling: cleared-`Nat` list style, per-syndrome counts as functions

Following this package's standing convention (clear the positive normalizations,
state the scale-free integer content — `Moment.lean`/`Normalization.lean` headers,
correspondence note §0/§8b), the `exp(o(n))` rates enter as `Nat` placeholders `C`,
`C'` (as `NoHighEnergy.lean`'s `K^C`), the cardinality `|𝒴|` is the `Nat` parameter
`Y`, and the tex's rational bound is the cleared integer inequality above.

A leaf's per-syndrome counts `N_j : 𝒴 → ℕ` are modelled as a **function**
`cnt : Nat → Nat` and the syndrome axis as a `List Nat` `S`, because the load-bearing
lemma is *max-over-`s` of a sum-over-`j`* and the function model handles the empty
family/empty-axis boundary correctly (`listMax [] = 0`, `listSum [] = 0`) with no
length bookkeeping — the point the R1 proof turns on.  This is the same data as a
`List Nat` indexed by syndromes (as `Moment.lean` counts fibers), and the max/sum are
identical; the choice is one of representation, not of content (flagged in the
correspondence note).  The multiplier `Y = |𝒴|` is kept as an abstract `Nat`
parameter, so R1 holds for any `Y` meeting (b); the honest instantiation is `Y =
S.length`.

Kernel-checked, stdlib-only, no mathlib.  Stacks on the L1–L5 spine (#438) and the
B1 image-normalization identities (#440); mechanizes #441's R1/R4 (the #435-A6 →
#441 lineage).
-/

/-! ## List maximum `listMax` (the `max_s` operator, computed)

The spine elsewhere parametrizes "max" by an attained upper-bound witness
(`Moment.lean`); the add-back core needs the *computed* max so its empty case is
pinned (`listMax [] = 0`), which is where the union bound's base case lives. -/

/-- Maximum of a `List Nat` (the discrete `max_s`), with `listMax [] = 0`. -/
def listMax : List Nat → Nat
  | [] => 0
  | a :: l => Nat.max a (listMax l)

@[simp] theorem listMax_nil : listMax [] = 0 := rfl
@[simp] theorem listMax_cons (a : Nat) (l : List Nat) :
    listMax (a :: l) = Nat.max a (listMax l) := rfl

/-- Every member is bounded by the max: `a ∈ l → a ≤ listMax l`. -/
theorem le_listMax_of_mem : ∀ {l : List Nat} {a : Nat}, a ∈ l → a ≤ listMax l := by
  intro l
  induction l with
  | nil => intro a ha; simp at ha
  | cons b t ih =>
    intro a ha
    rcases List.mem_cons.mp ha with h | h
    · subst h; rw [listMax_cons]; exact Nat.le_max_left _ _
    · rw [listMax_cons]; exact Nat.le_trans (ih h) (Nat.le_max_right _ _)

/-- The max is bounded by any common upper bound: `(∀ x ∈ l, x ≤ b) → listMax l ≤ b`.
The `nil` case (`0 ≤ b`) is the empty base of the union bound. -/
theorem listMax_le : ∀ {l : List Nat} {b : Nat}, (∀ x ∈ l, x ≤ b) → listMax l ≤ b := by
  intro l
  induction l with
  | nil => intro b _; exact Nat.zero_le b
  | cons a t ih =>
    intro b hb
    rw [listMax_cons]
    exact Nat.max_le.mpr
      ⟨hb a List.mem_cons_self, ih (fun x hx => hb x (List.mem_cons_of_mem _ hx))⟩

/-! ## Termwise-monotone list sum over `map` -/

/-- If `f x ≤ g x` pointwise on `l`, then `∑ (l.map f) ≤ ∑ (l.map g)`. -/
theorem listSum_map_le {α : Type} (f g : α → Nat) :
    ∀ l : List α, (∀ x ∈ l, f x ≤ g x) → listSum (l.map f) ≤ listSum (l.map g) := by
  intro l
  induction l with
  | nil => intro _; simp
  | cons a t ih =>
    intro h
    simp only [List.map_cons, listSum_cons]
    exact Nat.add_le_add (h a List.mem_cons_self)
      (ih (fun x hx => h x (List.mem_cons_of_mem _ hx)))

/-! ## Max-of-pointwise-sum ≤ sum-of-maxes (the union-bound core)

The real content of `lem:addback`'s upgrade line
`max_s ∑_j N_j(s) ≤ ∑_j max_s N_j(s)`.  Stated for a finite list of functions
`F : List (Nat → Nat)` over a shared index axis `S : List Nat`; the empty cases are
handled by `listMax`/`listSum` at `0`. -/

/-- **Union bound over leaves.**  For any index axis `S` and finite family `F` of
functions, the max over `s ∈ S` of the pointwise sum `∑_{g∈F} g s` is at most the sum
over `F` of the per-function maxes: `max_s ∑_j g_j(s) ≤ ∑_j max_s g_j(s)`. -/
theorem listMax_sum_le_sum_listMax (S : List Nat) (F : List (Nat → Nat)) :
    listMax (S.map (fun s => listSum (F.map (fun g => g s))))
      ≤ listSum (F.map (fun g => listMax (S.map g))) := by
  apply listMax_le
  intro x hx
  rw [List.mem_map] at hx
  obtain ⟨s, hsS, rfl⟩ := hx
  apply listSum_map_le
  intro gg _
  exact le_listMax_of_mem (List.mem_map.mpr ⟨s, hsS, rfl⟩)

/-! ## Leaf families -/

/-- A first-match **leaf** `Ω_j`: mass `M_j = |Ω_j|`, image size `L_j = |Φ(Ω_j)|`, and
per-syndrome prefix counts `N_j : 𝒴 → ℕ`. -/
structure Leaf where
  /-- `M_j = |Ω_j|`, the leaf mass. -/
  mass : Nat
  /-- `L_j = |Φ(Ω_j)|`, the leaf image size. -/
  img : Nat
  /-- `N_j(·)`, per-syndrome prefix counts. -/
  cnt : Nat → Nat

/-- Per-leaf max `max_s N_j(s)` over the syndrome axis `S`. -/
def leafMax (S : List Nat) (lf : Leaf) : Nat := listMax (S.map lf.cnt)

/-- Global prefix count at syndrome `s`: `N(s) = ∑_j N_j(s)` (the leaves partition the
residual, so this is a genuine sum). -/
def globalCount (fam : List Leaf) (s : Nat) : Nat :=
  listSum (fam.map (fun lf => lf.cnt s))

/-- Global max `max_s N(s) = max_s ∑_j N_j(s)`. -/
def globalMax (S : List Nat) (fam : List Leaf) : Nat :=
  listMax (S.map (globalCount fam))

/-- **Union bound, leaf-family form** (the family instance of
`listMax_sum_le_sum_listMax`): `max_s ∑_j N_j(s) ≤ ∑_j max_s N_j(s)`.  Proved directly
by the same two-step argument (max-`≤`-per-member, then termwise `listSum`
monotonicity) for a clean unfold path. -/
theorem globalMax_le_sum_leafMax (S : List Nat) (fam : List Leaf) :
    globalMax S fam ≤ listSum (fam.map (leafMax S)) := by
  unfold globalMax
  apply listMax_le
  intro x hx
  rw [List.mem_map] at hx
  obtain ⟨s, hsS, rfl⟩ := hx
  unfold globalCount
  apply listSum_map_le
  intro lf _
  exact le_listMax_of_mem (List.mem_map.mpr ⟨s, hsS, rfl⟩)

/-! ## The cleared per-leaf arithmetic chain and its telescope -/

/-- **Per-leaf clearing** `N_j(s)·Y ≤ N_j(s)·L_j·C' ≤ C·M_j·C'`.  From per-leaf Q
`mx·L ≤ C·M` (a) and image non-degeneracy `Y ≤ L·C'` (b): `mx·Y ≤ C·C'·M`. -/
theorem leaf_clear_chain (mx L M C C' Y : Nat)
    (hQ : mx * L ≤ C * M) (hND : Y ≤ L * C') :
    mx * Y ≤ C * C' * M :=
  calc mx * Y
      ≤ mx * (L * C') := Nat.mul_le_mul (Nat.le_refl mx) hND
    _ = mx * L * C' := by rw [← Nat.mul_assoc]
    _ ≤ (C * M) * C' := Nat.mul_le_mul hQ (Nat.le_refl C')
    _ = C * C' * M := by rw [Nat.mul_assoc, Nat.mul_comm M C', ← Nat.mul_assoc]

/-- **Telescope over masses.**  With per-leaf Q (a) and image non-degeneracy (b)
uniform over the family, the sum of per-leaf maxes, scaled by `Y`, is bounded by
`C·C'·∑_j M_j` — no leaf-count bound needed. -/
theorem addback_sum_bound (S : List Nat) (Y C C' : Nat) :
    ∀ fam : List Leaf,
      (∀ lf ∈ fam, leafMax S lf * lf.img ≤ C * lf.mass) →
      (∀ lf ∈ fam, Y ≤ lf.img * C') →
      listSum (fam.map (leafMax S)) * Y ≤ C * C' * listSum (fam.map Leaf.mass) := by
  intro fam
  induction fam with
  | nil => intro _ _; simp
  | cons lf t ih =>
    intro hQ hND
    have hhead : leafMax S lf * Y ≤ C * C' * lf.mass :=
      leaf_clear_chain (leafMax S lf) lf.img lf.mass C C' Y
        (hQ lf List.mem_cons_self) (hND lf List.mem_cons_self)
    have htail := ih (fun x hx => hQ x (List.mem_cons_of_mem _ hx))
      (fun x hx => hND x (List.mem_cons_of_mem _ hx))
    simp only [List.map_cons, listSum_cons, Nat.add_mul, Nat.mul_add]
    omega

/-! ## R1 — `def:profile-nondegen` and `lem:addback` add-back sufficiency -/

/-- **`def:profile-nondegen`** (cleared bundle).  The primitive residual is
*profile non-degenerate* if its covering leaves satisfy (a) per-leaf Q uniformly, (b)
image non-degeneracy, and (c) the mass partition — all in cleared `Nat` form. -/
def ProfileNonDegen (S : List Nat) (fam : List Leaf) (Y C C' Mtot : Nat) : Prop :=
  (∀ lf ∈ fam, leafMax S lf * lf.img ≤ C * lf.mass)      -- (a) per-leaf Q, cleared
  ∧ (∀ lf ∈ fam, Y ≤ lf.img * C')                        -- (b) image non-degeneracy, cleared
  ∧ listSum (fam.map Leaf.mass) ≤ Mtot                   -- (c) mass partition

/-- **(R1) `lem:addback`, add-back sufficiency.**  If the primitive residual is
profile non-degenerate (`def:profile-nondegen`), then the global first-match prefix
count obeys `max_s N(s)·Y ≤ C·C'·Mtot` (cleared `max_s N(s) ≤ C·C'·Mtot/Y =
exp(o(n))·barN_global`).  Union bound over leaves, per-leaf clearing, mass telescope;
no leaf-count bound. -/
theorem addback_sufficiency (S : List Nat) (fam : List Leaf) (Y C C' Mtot : Nat)
    (h : ProfileNonDegen S fam Y C C' Mtot) :
    globalMax S fam * Y ≤ C * C' * Mtot := by
  obtain ⟨hQ, hND, hmass⟩ := h
  calc globalMax S fam * Y
      ≤ listSum (fam.map (leafMax S)) * Y :=
        Nat.mul_le_mul (globalMax_le_sum_leafMax S fam) (Nat.le_refl Y)
    _ ≤ C * C' * listSum (fam.map Leaf.mass) := addback_sum_bound S Y C C' fam hQ hND
    _ ≤ C * C' * Mtot := Nat.mul_le_mul (Nat.le_refl (C * C')) hmass

/-! ## R4 — falsifier: image non-degeneracy (b) is load-bearing

Following #441's witness (note R4): `Y` collapsed leaves (`L_j = 1`), each of mass
`barN`, all piled onto one syndrome.  Per-leaf Q (a) holds, but the global add-back is
violated by the factor `Y`.  Here `Y = 3`, `barN = 1`, `S = [0,1,2]`: piled
`max_s N(s) = 3 = Y·barN`, a blow-up of `Y = 3` over `barN_global = Mtot/Y = 1`. -/

/-- The syndrome axis `𝒴 = {0,1,2}` (`|𝒴| = Y = 3`). -/
def falsS : List Nat := [0, 1, 2]

/-- A collapsed leaf: mass `1`, image `L_j = 1`, all count on syndrome `0`. -/
def piledLeaf : Leaf := ⟨1, 1, fun s => if s = 0 then 1 else 0⟩

/-- `Y = 3` collapsed leaves, all piled on syndrome `0`. -/
def falsFam : List Leaf := [piledLeaf, piledLeaf, piledLeaf]

/-- **(R4) Falsifier.**  Per-leaf Q (a) holds (`C = 1`), image non-degeneracy (b)
*fails* (`L_j·C' = 1 < 3 = Y` at `C' = 1`), and the add-back conclusion is violated:
`C·C'·Mtot = 3 < 9 = max_s N(s)·Y` (a blow-up of `Y = 3`).  So (b) is load-bearing. -/
theorem addback_falsifier :
    (∀ lf ∈ falsFam, leafMax falsS lf * lf.img ≤ 1 * lf.mass)          -- (a) per-leaf Q, C = 1
    ∧ (¬ ∀ lf ∈ falsFam, (3 : Nat) ≤ lf.img * 1)                       -- (b) fails, C' = 1, Y = 3
    ∧ 1 * 1 * listSum (falsFam.map Leaf.mass) < globalMax falsS falsFam * 3 := by
  decide

/-- The `spread` repair of the falsifier: the same three collapsed leaves, images
sent to *distinct* syndromes. -/
def spreadFam : List Leaf :=
  [⟨1, 1, fun s => if s = 0 then 1 else 0⟩,
   ⟨1, 1, fun s => if s = 1 then 1 else 0⟩,
   ⟨1, 1, fun s => if s = 2 then 1 else 0⟩]

/-- **(R4) Repair.**  Spreading the collapsed images to distinct syndromes keeps
per-leaf Q (a) and *restores* the add-back bound (`max_s N(s)·Y = 3 ≤ 3 = C·C'·Mtot`),
confirming that pile-up — the violation of (b) — is the failure, not per-leaf Q. -/
theorem addback_falsifier_repair :
    (∀ lf ∈ spreadFam, leafMax falsS lf * lf.img ≤ 1 * lf.mass)        -- (a) still holds
    ∧ globalMax falsS spreadFam * 3 ≤ 1 * 1 * listSum (spreadFam.map Leaf.mass) := by
  decide

/-! ## Corollary — B1 `ambient_image_max` feeds add-back's per-leaf Q (a)

The per-leaf Q hypothesis (a) consumed by `addback_sufficiency` is exactly the
*conclusion* produced by the B1 image-max transfer `ambient_image_max`
(`Normalization.lean`): identifying `mxImg := leafMax S lf`, `L := lf.img`,
`M := lf.mass`, an ambient max bound on a leaf's fibers yields its cleared per-leaf Q.
So the #440 image-normalization output composes into the #441 add-back input. -/

/-- **B1 → A6 composition.**  Given a leaf whose per-syndrome fiber list `S.map lf.cnt`
sits inside an ambient fiber list `amb` with ambient max bound `mxAmb·A ≤ C·M_j` and
`L_j ≤ A`, `ambient_image_max` yields the per-leaf Q `leafMax S lf · L_j ≤ C·M_j` —
precisely hypothesis (a) of `ProfileNonDegen`/`addback_sufficiency`.  (`hImgMem`
records that the per-leaf max is attained in the fiber list, i.e. `S ≠ []`.) -/
theorem perLeafQ_of_ambient_image_max
    (S : List Nat) (lf : Leaf) (amb : List Nat) (A C mxAmb : Nat)
    (hImgMem : leafMax S lf ∈ S.map lf.cnt)
    (hLA : lf.img ≤ A)
    (hsub : ∀ x ∈ S.map lf.cnt, x ∈ amb)
    (hAmbUB : ∀ x ∈ amb, x ≤ mxAmb)
    (hAmb : mxAmb * A ≤ C * lf.mass) :
    leafMax S lf * lf.img ≤ C * lf.mass :=
  ambient_image_max (S.map lf.cnt) amb A lf.img lf.mass C (leafMax S lf) mxAmb
    hLA hsub hImgMem hAmbUB hAmb

/-! ## Concrete sanity certificates (closed by kernel `decide`)

A non-degenerate family: syndrome axis `S = [0,1]` (`Y = 2`), two full-image leaves
(`L_j = 2 = Y`) with flat unit counts (mass `2`).  Then per-leaf Q (a) `1·2 ≤ 1·2`,
image non-degeneracy (b) `2 ≤ 2·1`, mass partition (c) `4 ≤ 4`, and the add-back
bound `max_s N(s)·Y = 2·2 = 4 ≤ 1·1·4 = C·C'·Mtot` all hold. -/

/-- Non-degenerate syndrome axis `𝒴 = {0,1}` (`Y = 2`). -/
def ndS : List Nat := [0, 1]

/-- Two full-image flat leaves (mass `2`, image `2`, unit counts). -/
def ndFam : List Leaf := [⟨2, 2, fun _ => 1⟩, ⟨2, 2, fun _ => 1⟩]

/-- The three `ProfileNonDegen` clauses (a)/(b)/(c) and the add-back conclusion all
hold on the non-degenerate family. -/
theorem addback_example :
    (∀ lf ∈ ndFam, leafMax ndS lf * lf.img ≤ 1 * lf.mass)             -- (a)
    ∧ (∀ lf ∈ ndFam, (2 : Nat) ≤ lf.img * 1)                          -- (b)
    ∧ listSum (ndFam.map Leaf.mass) ≤ 4                               -- (c)
    ∧ globalMax ndS ndFam * 2 ≤ 1 * 1 * 4 := by decide

/-- The same conclusion obtained end-to-end through `addback_sufficiency` (not
`decide`): the theorem is applicable and its output matches the certificate. -/
theorem addback_example_via_theorem :
    globalMax ndS ndFam * 2 ≤ 1 * 1 * 4 :=
  addback_sufficiency ndS ndFam 2 1 1 4 ⟨by decide, by decide, by decide⟩

end AsymptoticSpine
