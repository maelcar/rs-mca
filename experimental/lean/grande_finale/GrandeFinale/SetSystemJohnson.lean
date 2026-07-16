import Mathlib.Algebra.Order.Chebyshev
import Mathlib.Tactic

/-!
# A finite set-system Johnson inequality

This module isolates the elementary incidence double count used by the
fixed-slope kernel--Johnson argument.  A family of constant-size blocks on a
finite ground type, with uniformly bounded pairwise intersections, satisfies
the usual Johnson multiplicity inequality.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale.SetSystemJohnson

variable {D I : Type*} [Fintype D] [DecidableEq D]

/-- The number of selected blocks containing a ground point. -/
def pointDegree (A : Finset I) (B : I → Finset D) (x : D) : Nat :=
  (A.filter fun i => x ∈ B i).card

/-- Incidence double count: the sum of point degrees is the sum of block sizes. -/
theorem sum_pointDegree (A : Finset I) (B : I → Finset D) :
    ∑ x : D, pointDegree A B x = ∑ i ∈ A, (B i).card := by
  classical
  simp only [pointDegree, Finset.card_filter]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [← Finset.card_filter]
  simp

/-- Second-moment double count: squared point degrees count ordered pairs of
blocks through a point. -/
theorem sum_pointDegree_sq (A : Finset I) (B : I → Finset D) :
    ∑ x : D, pointDegree A B x ^ 2 =
      ∑ i ∈ A, ∑ j ∈ A, (B i ∩ B j).card := by
  classical
  have hsquare (x : D) :
      pointDegree A B x ^ 2 =
        ∑ i ∈ A, ∑ j ∈ A, if x ∈ B i ∩ B j then 1 else 0 := by
    simp only [pointDegree, Finset.card_filter, pow_two]
    rw [Finset.sum_mul]
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl fun j _ => ?_
    by_cases hxi : x ∈ B i <;> by_cases hxj : x ∈ B j <;>
      simp [hxi, hxj]
  calc
    ∑ x : D, pointDegree A B x ^ 2 =
        ∑ x : D, ∑ i ∈ A, ∑ j ∈ A,
          if x ∈ B i ∩ B j then 1 else 0 := by
            refine Finset.sum_congr rfl fun x _ => hsquare x
    _ = ∑ i ∈ A, ∑ j ∈ A, ∑ x : D,
          if x ∈ B i ∩ B j then 1 else 0 := by
            rw [Finset.sum_comm]
            refine Finset.sum_congr rfl fun i _ => ?_
            rw [Finset.sum_comm]
    _ = ∑ i ∈ A, ∑ j ∈ A, (B i ∩ B j).card := by
            refine Finset.sum_congr rfl fun i _ => ?_
            refine Finset.sum_congr rfl fun j _ => ?_
            rw [← Finset.card_filter]
            congr 1
            ext x
            simp

/-- The abstract finite set-system Johnson inequality.

The finite set A contains the block labels, B i is the block with label i,
all selected blocks have size s, and two differently labelled blocks meet
in at most w points.  No injectivity hypothesis on B is needed: when
w is smaller than s, the overlap hypothesis itself rules out duplicate blocks. -/
theorem setSystemJohnson
    (A : Finset I) (B : I → Finset D) (s w : Nat)
    (hcard : ∀ i ∈ A, (B i).card = s)
    (hinter : ∀ i ∈ A, ∀ j ∈ A, i ≠ j → (B i ∩ B j).card ≤ w) :
    A.card * (s ^ 2 - Fintype.card D * w) ≤
      Fintype.card D * (s - w) := by
  classical
  let M := A.card
  let N := Fintype.card D
  have hpair :
      ∑ i ∈ A, ∑ j ∈ A, (B i ∩ B j).card ≤
        M * (s + (M - 1) * w) := by
    calc
      ∑ i ∈ A, ∑ j ∈ A, (B i ∩ B j).card ≤
          ∑ i ∈ A, ∑ j ∈ A, if i = j then s else w := by
            refine Finset.sum_le_sum fun i hi => ?_
            refine Finset.sum_le_sum fun j hj => ?_
            by_cases hij : i = j
            · subst j
              simp [hcard i hi]
            · simpa [hij] using hinter i hi j hj hij
      _ = M * (s + (M - 1) * w) := by
            have hinner (i : I) (hi : i ∈ A) :
                (∑ j ∈ A, if i = j then s else w) =
                  s + (M - 1) * w := by
              rw [← Finset.sum_erase_add A
                (fun j => if i = j then s else w) hi]
              have herase :
                  (∑ j ∈ A.erase i, if i = j then s else w) =
                    (A.erase i).card * w := by
                calc
                  (∑ j ∈ A.erase i, if i = j then s else w) =
                      ∑ _j ∈ A.erase i, w := by
                        refine Finset.sum_congr rfl fun j hj => ?_
                        have hji : j ≠ i := (Finset.mem_erase.mp hj).1
                        simp [Ne.symm hji]
                  _ = (A.erase i).card * w := by simp
              rw [herase, Finset.card_erase_of_mem hi]
              simp [M, Nat.add_comm]
            rw [Finset.sum_congr rfl hinner, Finset.sum_const,
              Nat.nsmul_eq_mul]
  have hincidence :
      ∑ x : D, pointDegree A B x = M * s := by
    rw [sum_pointDegree]
    calc
      ∑ i ∈ A, (B i).card = ∑ _i ∈ A, s :=
        Finset.sum_congr rfl hcard
      _ = M * s := by simp [M]
  have hcauchy :
      (M * s) ^ 2 ≤ N * (M * (s + (M - 1) * w)) := by
    calc
      (M * s) ^ 2 =
          (∑ x : D, pointDegree A B x) ^ 2 := by rw [hincidence]
      _ ≤ Fintype.card D * ∑ x : D, pointDegree A B x ^ 2 := by
        simpa using
          (sq_sum_le_card_mul_sum_sq
            (s := (Finset.univ : Finset D))
            (f := pointDegree A B))
      _ = N * ∑ i ∈ A, ∑ j ∈ A, (B i ∩ B j).card := by
        rw [sum_pointDegree_sq]
      _ ≤ N * (M * (s + (M - 1) * w)) :=
        Nat.mul_le_mul_left N hpair
  by_cases hM : M = 0
  · have hAcard : A.card = 0 := by simpa [M] using hM
    simp [hAcard]
  have hMpos : 0 < M := Nat.pos_of_ne_zero hM
  have hAnonempty : A.Nonempty := by
    apply Finset.card_pos.mp
    simpa [M] using hMpos
  have hsN : s ≤ N := by
    obtain ⟨i, hi⟩ := hAnonempty
    rw [← hcard i hi]
    exact Finset.card_le_card (Finset.subset_univ (B i))
  have hcancel :
      M * s ^ 2 ≤ N * s + N * (M - 1) * w := by
    have hfactor :
        M * (M * s ^ 2) ≤ M * (N * (s + (M - 1) * w)) := by
      simpa [pow_two, Nat.mul_add, Nat.add_mul, mul_assoc, mul_left_comm,
        mul_comm] using hcauchy
    have hfactored := le_of_mul_le_mul_left hfactor hMpos
    simpa [Nat.mul_add, Nat.add_mul, mul_assoc, mul_left_comm, mul_comm] using
      hfactored
  by_cases hws : w ≤ s
  · by_cases hdenom : N * w ≤ s ^ 2
    · have hNws : N * w ≤ N * s := Nat.mul_le_mul_left N hws
      have hMsplit : M - 1 + 1 = M := Nat.sub_add_cancel hMpos
      have hrhs :
          N * (s - w) + M * (N * w) =
            N * s + N * (M - 1) * w := by
        rw [Nat.mul_sub_left_distrib, ← hMsplit, Nat.add_mul, one_mul]
        calc
          (N * s - N * w) + ((M - 1) * (N * w) + N * w) =
              ((N * s - N * w) + N * w) + (M - 1) * (N * w) := by
                omega
          _ = N * s + (M - 1) * (N * w) := by
                rw [Nat.sub_add_cancel hNws]
          _ = N * s + N * (M - 1) * w := by ring
      apply Nat.add_le_add_iff_right.mp
      calc
        A.card * (s ^ 2 - Fintype.card D * w) + M * (N * w) =
            M * s ^ 2 := by
              simp only [M, N]
              rw [← Nat.mul_add, Nat.sub_add_cancel hdenom]
        _ ≤ N * s + N * (M - 1) * w := hcancel
        _ = Fintype.card D * (s - w) + M * (N * w) := by
              simpa [N] using hrhs.symm
    · have hzero : s ^ 2 - N * w = 0 :=
        Nat.sub_eq_zero_of_le (Nat.le_of_not_ge hdenom)
      simp [N, hzero]
  · have hsw : s < w := Nat.lt_of_not_ge hws
    have hsquare_le : s ^ 2 ≤ N * w := by
      calc
        s ^ 2 = s * s := by rw [pow_two]
        _ ≤ N * s := Nat.mul_le_mul_right s hsN
        _ ≤ N * w := Nat.mul_le_mul_left N (Nat.le_of_lt hsw)
    have hzero : s ^ 2 - N * w = 0 :=
      Nat.sub_eq_zero_of_le hsquare_le
    simp [N, hzero]

/-- Quotient form of setSystemJohnson, valid when the Johnson denominator is
positive. -/
theorem setSystemJohnson_div
    (A : Finset I) (B : I → Finset D) (s w : Nat)
    (hcard : ∀ i ∈ A, (B i).card = s)
    (hinter : ∀ i ∈ A, ∀ j ∈ A, i ≠ j → (B i ∩ B j).card ≤ w)
    (hpositive : 0 < s ^ 2 - Fintype.card D * w) :
    A.card ≤
      (Fintype.card D * (s - w)) /
        (s ^ 2 - Fintype.card D * w) := by
  rw [Nat.le_div_iff_mul_le hpositive]
  simpa [Nat.mul_comm] using setSystemJohnson A B s w hcard hinter

#print axioms setSystemJohnson
#print axioms setSystemJohnson_div

end GrandeFinale.SetSystemJohnson
