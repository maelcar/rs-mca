namespace AsymptoticSpine

/-!
# A natural-number kernel for two-block Boolean difference growth

This stdlib-only module isolates the arithmetic step behind combining two
Boolean coordinate blocks.  Four square bounds for the blockwise terms imply
one square bound for the combined family.  The proof is finite and exact: it
uses only monotonicity in `Nat` and reflection of order through squaring.
-/

/-- Squaring reflects the natural-number order. -/
theorem nat_le_of_square_le_square {m n : Nat}
    (h : m ^ 2 ≤ n ^ 2) : m ≤ n := by
  exact (Nat.pow_le_pow_iff_left (by decide : 2 ≠ 0)).mp h

/-- Exact two-block growth inequality over `Nat`.

The four hypotheses bound the off-diagonal block, the two competing diagonal
blocks, and the opposite off-diagonal block.  The shared bound `y` pays the
larger diagonal; the smaller diagonal is bounded by `x * z`. -/
theorem boolean_difference_growth_nat
    (a0 a1 b0 b1 x y z : Nat)
    (ha0b1 : a0 ^ 2 * b1 ≤ x ^ 2)
    (ha0b0 : a0 ^ 2 * b0 ≤ y ^ 2)
    (ha1b1 : a1 ^ 2 * b1 ≤ y ^ 2)
    (ha1b0 : a1 ^ 2 * b0 ≤ z ^ 2) :
    (a0 + a1) ^ 2 * (b0 + b1) ≤ (x + y + z) ^ 2 := by
  have hcross_b1_sq :
      (a0 * a1 * b1) ^ 2 ≤ (x * y) ^ 2 := by
    calc
      (a0 * a1 * b1) ^ 2
          = (a0 ^ 2 * b1) * (a1 ^ 2 * b1) := by
              simp [Nat.pow_two, Nat.mul_comm, Nat.mul_left_comm]
      _ ≤ x ^ 2 * y ^ 2 := Nat.mul_le_mul ha0b1 ha1b1
      _ = (x * y) ^ 2 := by
        simp [Nat.pow_two, Nat.mul_comm, Nat.mul_left_comm]
  have hcross_b1 : a0 * a1 * b1 ≤ x * y :=
    nat_le_of_square_le_square hcross_b1_sq
  have hcross_b0_sq :
      (a0 * a1 * b0) ^ 2 ≤ (y * z) ^ 2 := by
    calc
      (a0 * a1 * b0) ^ 2
          = (a0 ^ 2 * b0) * (a1 ^ 2 * b0) := by
              simp [Nat.pow_two, Nat.mul_comm, Nat.mul_left_comm]
      _ ≤ y ^ 2 * z ^ 2 := Nat.mul_le_mul ha0b0 ha1b0
      _ = (y * z) ^ 2 := by
        simp [Nat.pow_two, Nat.mul_comm, Nat.mul_left_comm]
  have hcross_b0 : a0 * a1 * b0 ≤ y * z :=
    nat_le_of_square_le_square hcross_b0_sq
  rcases Nat.le_total (a0 ^ 2 * b0) (a1 ^ 2 * b1) with hdiag | hdiag
  · have hsmall_sq :
        (a0 ^ 2 * b0) ^ 2 ≤ (x * z) ^ 2 := by
      calc
        (a0 ^ 2 * b0) ^ 2
            ≤ (a0 ^ 2 * b0) * (a1 ^ 2 * b1) := by
              rw [Nat.pow_two]
              exact Nat.mul_le_mul (Nat.le_refl _) hdiag
        _ = (a0 ^ 2 * b1) * (a1 ^ 2 * b0) := by
          simp [Nat.pow_two, Nat.mul_comm, Nat.mul_left_comm]
        _ ≤ x ^ 2 * z ^ 2 := Nat.mul_le_mul ha0b1 ha1b0
        _ = (x * z) ^ 2 := by
          simp [Nat.pow_two, Nat.mul_comm, Nat.mul_left_comm]
    have hsmall : a0 ^ 2 * b0 ≤ x * z :=
      nat_le_of_square_le_square hsmall_sq
    simp only [Nat.pow_two, Nat.mul_add, Nat.mul_comm, Nat.mul_left_comm] at *
    omega
  · have hsmall_sq :
        (a1 ^ 2 * b1) ^ 2 ≤ (x * z) ^ 2 := by
      calc
        (a1 ^ 2 * b1) ^ 2
            ≤ (a0 ^ 2 * b0) * (a1 ^ 2 * b1) := by
              rw [Nat.pow_two]
              exact Nat.mul_le_mul hdiag (Nat.le_refl _)
        _ = (a0 ^ 2 * b1) * (a1 ^ 2 * b0) := by
          simp [Nat.pow_two, Nat.mul_comm, Nat.mul_left_comm]
        _ ≤ x ^ 2 * z ^ 2 := Nat.mul_le_mul ha0b1 ha1b0
        _ = (x * z) ^ 2 := by
          simp [Nat.pow_two, Nat.mul_comm, Nat.mul_left_comm]
    have hsmall : a1 ^ 2 * b1 ≤ x * z :=
      nat_le_of_square_le_square hsmall_sq
    simp only [Nat.pow_two, Nat.mul_add, Nat.mul_comm, Nat.mul_left_comm] at *
    omega

#print axioms nat_le_of_square_le_square
#print axioms boolean_difference_growth_nat

end AsymptoticSpine
