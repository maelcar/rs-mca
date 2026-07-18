import PowersumRigidity.VandermondeRank

/-!
# Exact rank of a weighted moment matrix

This module formalizes the weighted Vandermonde factorization in “Exact rank
factorization” of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at source snapshot
`168e9ba0`.  For a finite set `E` of field elements and nonzero weights on `E`,
it proves that the matrix

`M a b = ∑ x : E, w x * x ^ (a + b)`

has rank `min t E.card` whenever `E.card ≤ m`.

This is only the standalone weighted moment-matrix rank identity.  It consumes
an already supplied distinct support and nonzero weights; it neither extracts
these data from a Route-D/RIM packet nor identifies `rim_rank_drop_pivot` with
the ambient MCA Hankel rank-drop branch.  It proves no bad-incidence,
first-match, deep-MCA owner, support-count, or Route-D payment statement.

The source's natural-number corollary needs an edge repair: without `0 < t`,
`rank M < t ↔ E.card ≤ t - 1` fails for `t = 0` and `E = ∅`.  The all-`t`
theorem below is `rank M < t ↔ E.card < t`; the truncated-subtraction form is
provided both with its missing positivity hypothesis and as an all-`t`
conjunction.
-/

open Matrix
open scoped Classical

noncomputable section

namespace PowersumRigidity.WeightedMomentRank

variable {F : Type*} [Field F]

/-- The rectangular Vandermonde evaluation matrix with rows indexed by `E`
and columns indexed by exponents `0, ..., r - 1`.

Source: “Exact rank factorization” in
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
def rectangularVandermonde (E : Finset F) (r : ℕ) : Matrix E (Fin r) F :=
  fun x a ↦ (x : F) ^ (a : ℕ)

/-- The weighted moment matrix from the rank-drop source statement.

Source: “Statement audited” and “Exact rank factorization” in
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
def weightedMomentMatrix (E : Finset F) (w : F → F) (t m : ℕ) :
    Matrix (Fin t) (Fin m) F :=
  fun a b ↦ ∑ x : E, w x * (x : F) ^ ((a : ℕ) + (b : ℕ))

/-- The rows of a rectangular Vandermonde matrix are independent when there
are at least as many columns as nodes.

Source: the full-row-rank Vandermonde step supporting equations (1)--(2) in
“Exact rank factorization” of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem rectangularVandermonde_rows_linearIndependent
    (E : Finset F) (r : ℕ) (hcard : E.card ≤ r) :
    LinearIndependent F (rectangularVandermonde E r).row := by
  let e := (Fintype.equivFin E).symm
  have hy : Function.Injective
      (fun i : Fin (Fintype.card E) ↦ ((e i : E) : F)) := by
    intro i j hij
    apply e.injective
    exact Subtype.ext hij
  apply (linearIndependent_equiv e).mp
  change LinearIndependent F
    (fun i : Fin (Fintype.card E) ↦
      fun j : Fin r ↦ ((e i : E) : F) ^ (j : ℕ))
  simpa only [one_mul] using
    (VandermondeRank.columns_linearIndependent (by simpa using hcard)
      (fun i : Fin (Fintype.card E) ↦ ((e i : E) : F)) hy
      (fun _ ↦ (1 : F)) (by simp))

/-- A rectangular Vandermonde matrix on a finite set has the expected rank.

Source: the left-Vandermonde rank assertion supporting equation (2) in “Exact
rank factorization” of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem rectangularVandermonde_rank (E : Finset F) (r : ℕ) :
    (rectangularVandermonde E r).rank = min E.card r := by
  classical
  by_cases hcard : E.card ≤ r
  · rw [(rectangularVandermonde_rows_linearIndependent E r hcard).rank_matrix]
    simp [Nat.min_eq_left hcard]
  · have hrE : r ≤ Fintype.card E := by
      simpa using Nat.le_of_not_ge hcard
    have hrEfin : Fintype.card (Fin r) ≤ Fintype.card E := by
      simpa using hrE
    let e : Fin r ↪ E :=
      Classical.choice (Function.Embedding.nonempty_of_card_le hrEfin)
    let V := rectangularVandermonde E r
    let S : Matrix (Fin r) (Fin r) F :=
      V.submatrix e (Equiv.refl (Fin r))
    have hnodes : Function.Injective
        (fun i : Fin r ↦ ((e i : E) : F)) := by
      intro i j hij
      apply e.injective
      exact Subtype.ext hij
    have hS : S = Matrix.vandermonde
        (fun i : Fin r ↦ ((e i : E) : F)) := by
      ext i j
      rfl
    have hdet : S.det ≠ 0 := by
      rw [hS]
      exact Matrix.det_vandermonde_ne_zero_iff.mpr hnodes
    have hSrank : S.rank = r := by
      have hSli : LinearIndependent F S.row :=
        Matrix.linearIndependent_rows_of_det_ne_zero hdet
      simpa using hSli.rank_matrix
    have hle : S.rank ≤ V.rank :=
      Matrix.rank_submatrix_le V e (Equiv.refl (Fin r))
    have hVrank : V.rank = r := by
      apply le_antisymm
      · simpa using Matrix.rank_le_card_width V
      · simpa [hSrank] using hle
    have hrE' : r ≤ E.card := by simpa using hrE
    simpa [V, Nat.min_eq_right hrE'] using hVrank

/-- With at least as many columns as nodes, rectangular Vandermonde evaluation
is onto the space of functions on the nodes.

Source: the right-Vandermonde surjectivity assertion supporting equation (2)
in “Exact rank factorization” of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem rectangularVandermonde_mulVec_surjective
    (E : Finset F) (r : ℕ) (hcard : E.card ≤ r) :
    Function.Surjective (rectangularVandermonde E r).mulVecLin := by
  apply LinearMap.range_eq_top.mp
  apply Submodule.eq_top_of_finrank_eq
  rw [← Matrix.rank]
  rw [(rectangularVandermonde_rows_linearIndependent E r hcard).rank_matrix]
  simp

/-- A diagonal matrix with no zero diagonal entry acts surjectively.

Source: the invertible diagonal-map assertion supporting equation (2) in
“Exact rank factorization” of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem diagonal_mulVec_surjective
    (E : Finset F) (w : E → F) (hw : ∀ x, w x ≠ 0) :
    Function.Surjective (Matrix.diagonal w).mulVecLin := by
  intro y
  refine ⟨(fun x ↦ (w x)⁻¹ * y x), ?_⟩
  ext x
  change (Matrix.diagonal w *ᵥ (fun x ↦ (w x)⁻¹ * y x)) x = y x
  rw [Matrix.mulVec_diagonal]
  simp [hw x]

/-- The source factorization through two Vandermonde matrices and the diagonal
weight matrix.  The dimensions are `t × |E|`, `|E| × |E|`, and `|E| × m`.

Source: equation (1) in “Exact rank factorization” of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem weightedMomentMatrix_factorization
    (E : Finset F) (w : F → F) (t m : ℕ) :
    weightedMomentMatrix E w t m =
      ((rectangularVandermonde E t)ᵀ * Matrix.diagonal (fun x : E ↦ w x)) *
        rectangularVandermonde E m := by
  classical
  ext a b
  simp only [weightedMomentMatrix]
  rw [Matrix.mul_apply]
  simp_rw [Matrix.mul_diagonal]
  simp only [Matrix.transpose_apply, rectangularVandermonde]
  apply Finset.sum_congr rfl
  intro x _
  rw [pow_add]
  ring

/-- Right multiplication by a matrix whose `mulVec` map is surjective does
not change matrix rank.

Source: the surjective-factor rank step in the proof of equation (2), “Exact
rank factorization” of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem rank_mul_eq_left_of_mulVec_surjective
    {l n p : Type*} [Fintype n] [Fintype p]
    (A : Matrix l n F) (B : Matrix n p F)
    (hB : Function.Surjective B.mulVecLin) :
    (A * B).rank = A.rank := by
  rw [Matrix.rank, Matrix.rank, Matrix.mulVecLin_mul,
    LinearMap.range_comp_of_range_eq_top A.mulVecLin
      (LinearMap.range_eq_top.mpr hB)]

/-- **Exact weighted moment rank.**  Distinctness is carried by the `Finset`
index, `hcard` gives full row rank of the right Vandermonde factor, and
`hweight` makes the diagonal factor invertible.

Source: equation (2) in “Exact rank factorization” of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem weightedMomentMatrix_rank
    (E : Finset F) (w : F → F) (t m : ℕ)
    (hcard : E.card ≤ m) (hweight : ∀ x ∈ E, w x ≠ 0) :
    (weightedMomentMatrix E w t m).rank = min t E.card := by
  rw [weightedMomentMatrix_factorization]
  rw [rank_mul_eq_left_of_mulVec_surjective]
  · rw [rank_mul_eq_left_of_mulVec_surjective]
    · rw [Matrix.rank_transpose, rectangularVandermonde_rank, Nat.min_comm]
    · exact diagonal_mulVec_surjective E (fun x : E ↦ w x)
        (fun x ↦ hweight x x.property)
  · exact rectangularVandermonde_mulVec_surjective E m hcard

/-- The correct rank-drop equivalence for every natural `t`, including zero.

Source: repaired all-natural form of equation (3) in “Exact rank
factorization,” audited against “Edge cases and notation,” in
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem weightedMomentMatrix_rank_lt_iff_card_lt
    (E : Finset F) (w : F → F) (t m : ℕ)
    (hcard : E.card ≤ m) (hweight : ∀ x ∈ E, w x ≠ 0) :
    (weightedMomentMatrix E w t m).rank < t ↔ E.card < t := by
  rw [weightedMomentMatrix_rank E w t m hcard hweight, min_lt_iff]
  omega

/-- The all-`t` repair of the source's truncated-subtraction formulation.

Source: repaired conjunction form of equation (3) in “Exact rank
factorization,” audited against “Edge cases and notation,” in
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem weightedMomentMatrix_rank_lt_iff_pos_and_card_le_sub_one
    (E : Finset F) (w : F → F) (t m : ℕ)
    (hcard : E.card ≤ m) (hweight : ∀ x ∈ E, w x ≠ 0) :
    (weightedMomentMatrix E w t m).rank < t ↔
      0 < t ∧ E.card ≤ t - 1 := by
  rw [weightedMomentMatrix_rank_lt_iff_card_lt E w t m hcard hweight]
  omega

/-- The source's `≤ t - 1` corollary with its necessary positivity hypothesis
made explicit.  In the deployed packet, `t = 67,472`.

Source: equation (3) in “Exact rank factorization,” with the `t = 0` endpoint
repaired using “Edge cases and notation,” in
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem weightedMomentMatrix_rank_lt_iff_card_le_sub_one
    (E : Finset F) (w : F → F) (t m : ℕ)
    (hcard : E.card ≤ m) (hweight : ∀ x ∈ E, w x ≠ 0) (ht : 0 < t) :
    (weightedMomentMatrix E w t m).rank < t ↔ E.card ≤ t - 1 := by
  rw [weightedMomentMatrix_rank_lt_iff_card_lt E w t m hcard hweight]
  omega

end PowersumRigidity.WeightedMomentRank
