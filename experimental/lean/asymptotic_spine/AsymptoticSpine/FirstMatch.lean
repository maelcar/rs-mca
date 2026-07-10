import AsymptoticSpine.Util

namespace AsymptoticSpine

/-!
# (L1) First-match disjointization — `lem:first-match` / `def:cells`

Stdlib-only (no mathlib) formalization of the centerpiece combinatorial lemma of
`experimental/asymptotic_rs_mca.tex`:

* `def:cells` (L77–79): ordered cells; a slope is assigned to the *first* cell
  containing one of its witnesses; the cell's first-match budget is the number of
  slopes so assigned.
* `lem:first-match` (L81–87): *"If ordered cells `C_1,…,C_J` cover a set of bad
  slopes and the `j`-th first-match cell has budget `U_j`, then the covered slopes
  contribute at most `∑_j U_j` to `B_C^{MCA}(a)`."*  Paper proof (L86): *"assign
  each bad slope to the least-indexed cell containing a witness.  These assigned
  slope classes are disjoint, and the `j`-th class is contained in the projection
  of `C_j` after earlier cells have been removed.  Summing the budgets and then
  maximizing over received lines proves the claim."*

Lean core has no `Finset`/`Fintype`, so — following the repo's stdlib-only
convention (`l1_threshold_ledger`, `staircase_logic`) — a fixed received line's
data is modelled as `cells : List (List Nat)`, where `cells[j]` lists the
slope-ids for which cell `j` contains a witness (its raw projection, possibly
overlapping other cells).  The set of covered bad slopes is `cells.flatten`.

The first-match assignment produces, for cell `j`, the *leaf*
`L_j = C_j \ (C_0 ∪ … ∪ C_{j-1})` — exactly the paper's "projection of `C_j`
after earlier cells have been removed".  We prove:

* `nodup_firstMatchLeaves` — the assigned classes are **disjoint** (the flattened
  leaves are duplicate-free): no slope is charged to two cells;
* `mem_firstMatchLeaves` — the assigned classes **cover** exactly the covered bad
  slopes (`x` is assigned iff `x` is witnessed by some cell);
* `firstMatch_le_sum_cellSizes` / `firstMatch_le_sum_budgets` — the **budget-sum
  bound**: the first-match count is at most `∑_j |C_j|`, and at most `∑_j U_j` for
  any per-cell caps `U_j ≥ |C_j|`.

Maximizing over received lines (the outer `max_{r_1,r_2}` of `B_C^{MCA}`) is the
finite `sup` left in the tex; the disjointization content is per-line and is what
is formalized here (matching how `GrandeFinale.first_match_ledger` keeps it).

Kernel-checked, stdlib-only, no mathlib.
-/

/-! ## First-match leaves `L_j = C_j \ (C_0 ∪ … ∪ C_{j-1})` -/

/-- Slopes of cell `c` **newly** paid given the already-paid set `paid`: the leaf
contribution `C_j \ paid` (paper: projection of `C_j` after earlier cells
removed). -/
def newPaid (paid c : List Nat) : List Nat :=
  c.filter (fun x => decide (x ∉ paid))

/-- The ordered list of first-match leaves `L_0, L_1, …`, threading the running
union `paid` of already-paid slopes. -/
def firstMatchLeaves : List Nat → List (List Nat) → List (List Nat)
  | _, [] => []
  | paid, c :: cs => newPaid paid c :: firstMatchLeaves (paid ++ newPaid paid c) cs

/-- The running paid (union) set after processing the cells from `paid`. -/
def paidUnion : List Nat → List (List Nat) → List Nat
  | paid, [] => paid
  | paid, c :: cs => paidUnion (paid ++ newPaid paid c) cs

/-- The paid union telescopes: it is `paid` prepended to the flattened leaves. -/
theorem paidUnion_eq_append_flatten :
    ∀ (cells : List (List Nat)) (paid : List Nat),
      paidUnion paid cells = paid ++ (firstMatchLeaves paid cells).flatten := by
  intro cells
  induction cells with
  | nil => intro paid; simp [paidUnion, firstMatchLeaves]
  | cons c cs ih =>
    intro paid
    simp only [paidUnion, firstMatchLeaves, List.flatten_cons]
    rw [ih (paid ++ newPaid paid c), List.append_assoc]

/-- Membership in the paid union telescopes to the union of `paid` and the cells. -/
theorem mem_paidUnion :
    ∀ (cells : List (List Nat)) (paid : List Nat) (x : Nat),
      x ∈ paidUnion paid cells ↔ x ∈ paid ∨ x ∈ cells.flatten := by
  intro cells
  induction cells with
  | nil => intro paid x; simp [paidUnion]
  | cons c cs ih =>
    intro paid x
    rw [paidUnion, ih (paid ++ newPaid paid c) x]
    simp only [newPaid, List.mem_append, List.mem_filter, List.flatten_cons,
      decide_eq_true_eq]
    by_cases hx : x ∈ paid <;> simp [hx]

/-- The paid union stays duplicate-free: with duplicate-free cells the accumulated
paid set is `Nodup` (disjointness-after-removal). -/
theorem nodup_paidUnion :
    ∀ (cells : List (List Nat)) (paid : List Nat),
      (∀ c ∈ cells, c.Nodup) → paid.Nodup → (paidUnion paid cells).Nodup := by
  intro cells
  induction cells with
  | nil => intro paid _ hp; simpa [paidUnion] using hp
  | cons c cs ih =>
    intro paid hcells hp
    have hc : c.Nodup := hcells c List.mem_cons_self
    have hfilt : (newPaid paid c).Nodup := List.filter_sublist.nodup hc
    have hdisj : ∀ a, a ∈ paid → ∀ b, b ∈ newPaid paid c → a ≠ b := by
      intro a ha b hb hab
      have hbnp : b ∉ paid := of_decide_eq_true (List.mem_filter.mp hb).2
      exact hbnp (hab ▸ ha)
    have hstep : (paid ++ newPaid paid c).Nodup :=
      List.nodup_append.mpr ⟨hp, hfilt, hdisj⟩
    exact ih (paid ++ newPaid paid c)
      (fun c' hc' => hcells c' (List.mem_cons_of_mem _ hc')) hstep

/-- The flattened leaves equal the paid union from `[]`. -/
theorem flatten_firstMatchLeaves (cells : List (List Nat)) :
    (firstMatchLeaves [] cells).flatten = paidUnion [] cells := by
  rw [paidUnion_eq_append_flatten]; simp

/-! ## The shipped first-match statement -/

/-- The first-match count for a received line: how many distinct bad slopes are
paid across the ordered cells. -/
def firstMatchCount (cells : List (List Nat)) : Nat :=
  (firstMatchLeaves [] cells).flatten.length

/-- **Disjointness of the assigned classes** (`lem:first-match`, "these assigned
slope classes are disjoint").  With duplicate-free cells the flattened first-match
leaves are duplicate-free: no bad slope is charged to two cells. -/
theorem nodup_firstMatchLeaves (cells : List (List Nat))
    (hcells : ∀ c ∈ cells, c.Nodup) :
    (firstMatchLeaves [] cells).flatten.Nodup := by
  rw [flatten_firstMatchLeaves]
  exact nodup_paidUnion cells [] hcells List.nodup_nil

/-- **Coverage of the assigned classes** (`lem:first-match`, the leaves cover the
bad slopes).  A slope is assigned to some cell iff it is witnessed by some cell. -/
theorem mem_firstMatchLeaves (cells : List (List Nat)) (x : Nat) :
    x ∈ (firstMatchLeaves [] cells).flatten ↔ x ∈ cells.flatten := by
  rw [flatten_firstMatchLeaves]
  simpa using mem_paidUnion cells [] x

/-- Each leaf's length is at most its cell's length: the leaf-length sum is
dominated by the cell-length sum (leaf `L_j ⊆ C_j`). -/
theorem firstMatchLeaves_sum_length_le :
    ∀ (cells : List (List Nat)) (paid : List Nat),
      listSum ((firstMatchLeaves paid cells).map List.length)
        ≤ listSum (cells.map List.length) := by
  intro cells
  induction cells with
  | nil => intro paid; simp [firstMatchLeaves]
  | cons c cs ih =>
    intro paid
    simp only [firstMatchLeaves, List.map_cons, listSum_cons]
    have hleaf : (newPaid paid c).length ≤ c.length := by
      simpa [newPaid] using List.length_filter_le (fun x => decide (x ∉ paid)) c
    have := ih (paid ++ newPaid paid c)
    omega

/-- **Budget-sum bound, raw form** (`lem:first-match`).  The first-match count is
at most the sum of the raw cell sizes `∑_j |C_j|` — the paper's `∑_j U_j` with the
natural budget `U_j = |C_j|`. -/
theorem firstMatch_le_sum_cellSizes (cells : List (List Nat)) :
    firstMatchCount cells ≤ listSum (cells.map List.length) := by
  unfold firstMatchCount
  rw [length_flatten]
  exact firstMatchLeaves_sum_length_le cells []

/-- **Budget-sum bound, printed-budget form** (`lem:first-match`, verbatim).  For
any per-cell caps `U` (one per cell, `|C_j| ≤ U_j`), the covered slopes contribute
at most `∑_j U_j`. -/
theorem firstMatch_le_sum_budgets (cells : List (List Nat)) (U : List Nat)
    (hlen : cells.length ≤ U.length)
    (hcap : ∀ p ∈ (cells.map List.length).zip U, p.1 ≤ p.2) :
    firstMatchCount cells ≤ listSum U := by
  refine Nat.le_trans (firstMatch_le_sum_cellSizes cells) ?_
  refine listSum_le_of_zip (cells.map List.length) U ?_ hcap
  simpa using hlen

/-! ## Concrete first-match census (closed by kernel `decide`)

The `prop:no-high-energy`-independent toy from the round-2 in-paper audit's A1
attack: five bad slopes `g1..g5` and three ordered cells with overlapping
witnesses `g2∈{C1,C2}`, `g3,g5∈{C1,C2,C3}`, `g4∈{C2,C3}`.  First-match budgets
`(3,1,1)` sum to `5` = the number of distinct covered slopes, while summing the
raw projection budgets `(3,3,3)` over-counts to `9`.  First-match never
double-counts. -/

/-- The first-match leaves of the A1 toy: `(3,1,1)`, summing to the `5` distinct
covered slopes — not the raw `3+3+3 = 9`. -/
theorem firstMatch_A1_example :
    firstMatchLeaves [] [[1, 2, 3, 5], [1, 2, 3, 4, 5], [3, 4, 5]]
      = [[1, 2, 3, 5], [4], []]
    ∧ firstMatchCount [[1, 2, 3, 5], [1, 2, 3, 4, 5], [3, 4, 5]] = 5
    ∧ listSum ([[1, 2, 3, 5], [1, 2, 3, 4, 5], [3, 4, 5]].map List.length) = 12 := by
  decide

end AsymptoticSpine
