/-!
# Cylinder modulus arithmetic and finite renormalization anchors

This standalone module follows the corrected source packet
`experimental/notes/thresholds/cylinder_renormalization.md`.  It proves the
all-depth base-3 normalization behind U1/V1,

`2 * ((3^B + 1) / 2) = 3^B + 1`, hence `3^B = 2L - 1`,

and retains the existing finite arithmetic anchors for the degenerate U3
convolution, shifted Vandermonde checks, and class census.

The primary theorem is subtraction-free.  The analytic Parseval estimate,
trigonometric U2/U3 identities, subgroup cube-flatness, and the corrected
twisted-coset counterexample are not formalized here.  No mathlib and no
`sorry` are used.
-/

namespace CylinderRenormalization

/-- `binom n k = C(n,k)` via the running product. -/
def binom (n k : Nat) : Nat :=
  (List.range k).foldl (fun acc i => acc * (n - i) / (i + 1)) 1

/-- Full slice `M = C(2B,B)`. -/
def slice (B : Nat) : Nat := binom (2 * B) B

/-- Arithmetic image scale `L = (3^B+1)/2`; V1 verifies the realized-image
    interpretation at its displayed positive even depths. -/
def realizedImage (B : Nat) : Nat := (3 ^ B + 1) / 2

/-- Collision count `M2`. -/
def collisionMass (B : Nat) : Nat :=
  (List.range (B + 1)).foldl (fun acc s =>
    if s % 2 = B % 2 then
      acc + binom B s * 2 ^ s * (binom (B - s) ((B - s) / 2)) ^ 2
    else acc) 0

/-! ## 1. U1's exact modulus identity (base 3): `c = 2L - 1`. -/

/-- Every power of three is odd, expressed as its remainder modulo two. -/
private theorem three_pow_mod_two (B : Nat) : 3 ^ B % 2 = 1 := by
  induction B with
  | zero => decide
  | succ B ih =>
      rw [Nat.pow_succ, Nat.mul_mod, ih]

/-- Subtraction-free all-depth form of the base-3 image normalization. -/
theorem realizedImage_double (B : Nat) :
    2 * realizedImage B = 3 ^ B + 1 := by
  have hodd : 3 ^ B % 2 = 1 := three_pow_mod_two B
  have hsplit : 3 ^ B % 2 + 2 * (3 ^ B / 2) = 3 ^ B :=
    Nat.mod_add_div (3 ^ B) 2
  have hsum : 3 ^ B + 1 = 2 * (3 ^ B / 2 + 1) := by
    omega
  have hhalf : (3 ^ B + 1) / 2 = 3 ^ B / 2 + 1 := by
    rw [hsum]
    exact Nat.mul_div_cancel_left _ (by decide)
  unfold realizedImage
  rw [hhalf]
  omega

/-- Exact source normalization, valid at every natural depth. -/
theorem modulus_identity_all (B : Nat) :
    3 ^ B = 2 * realizedImage B - 1 := by
  calc
    3 ^ B = (3 ^ B + 1) - 1 :=
      (Nat.add_sub_cancel (3 ^ B) 1).symm
    _ = 2 * realizedImage B - 1 := by
      rw [realizedImage_double]

/-- The former finite API, now a direct wrapper around the all-depth theorem. -/
theorem modulus_identity :
    ∀ B ∈ [4, 6, 8, 16, 32, 64], 3 ^ B = 2 * realizedImage B - 1 := by
  intro B _
  exact modulus_identity_all B

/-! ## 2. U3's combinatorial half: the `(1+z)^{2k}` convolution.

The graded convolution `[z^B] (1+z)^{2k} q(z) = sum_j C(2k, B-j) q_j` is
pure polynomial algebra; `native_decide` checks it on pinned integer
vectors (binomial rows `q_j = C(2(B-k), j)`, the `m = 0` instance of
`p_{B-k, m}`, whose scale-B value must be `C(2B, B) = M` -- the
degenerate-cylinder consistency `hatf_B(0) = M`). -/

/-- `[z^B] (1+z)^{2k} (1+z)^{2(B-k)} = C(2B, B)`: the `m = 0` instance,
    computed through the graded sum. -/
theorem degenerate_cylinder_consistency :
    ∀ B ∈ [6, 8], ∀ k ∈ [1, 2, 3],
      (List.range (2 * (B - k) + 1)).foldl
        (fun acc j => if j ≤ B then
          acc + binom (2 * k) (B - j) * binom (2 * (B - k)) j else acc) 0
      = slice B := by native_decide

/-- Vandermonde consistency of the graded sum at shifted extraction
    degrees (the convolution algebra at `[z^{B-1}]` and `[z^{B+1}]`,
    pinned): `sum_j C(2k, d-j) C(2(B-k), j) = C(2B, d)`. -/
theorem graded_vandermonde :
    ∀ B ∈ [6, 8], ∀ k ∈ [1, 2, 3], ∀ d ∈ [5, 6, 7, 8, 9],
      (List.range (2 * (B - k) + 1)).foldl
        (fun acc j => if j ≤ d then
          acc + binom (2 * k) (d - j) * binom (2 * (B - k)) j else acc) 0
      = binom (2 * B) d := by native_decide

/-! ## 3. Shared class pins. -/

theorem class_pins :
    collisionMass 6 = 3584 ∧ collisionMass 8 = 97444 ∧
    slice 6 = 924 ∧ slice 8 = 12870 := by native_decide

end CylinderRenormalization
