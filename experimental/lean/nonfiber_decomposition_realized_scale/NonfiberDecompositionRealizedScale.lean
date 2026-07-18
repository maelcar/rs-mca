/-!
# Non-fiber-indexed decomposition at realized-image scale (arithmetic formalization)

Maps to **hard input 2**: the NON-fiber-indexed route to avdeevvadim's #716
charge-preserving semantic-or-signed decomposition -- the object left open after
the fiber-indexed route was cut on the Sidon-paired class (#739) and per-fiber
emission was closed (#735).  Reframed by the paper's `rem` PO5 (the correct
Fourier denominator is the realized-image group `|G_lambda|`, which "does not
assert that the realized image fills the affine group") and by the integrated
profile-envelope comparison audit: its exact finite full-codomain deficit for
the identity image is motivational only, not an asymptotic `(FI)` conclusion.

Note:     `experimental/notes/thresholds/nonfiber_decomposition_realized_scale.md`.
Verifier: `experimental/scripts/verify_nonfiber_decomposition_realized_scale.py`
          (90/90, tamper 3/3).

Class (#739 / #732 / #735 corrected Thm 2a / #717 Sec 7; DannyExperiments #749):
  `P` distinct-subset-sum, `|P|=B`, `c = 2 sum P + 1`, `T = P u (c-P)`, `a = B`,
  `Phi(S) = sum_{t in S} t` over `Z`; `M = C(2B,B)`, realized image
  `L = (3^B+1)/2`, unpaired-count `s` per support.

Analytic and census results (PROVED in note + Python verifier; over `Z`/`F_p`):
  RUNG (a)  #739 kills concentration at BOTH ambient and realized scale.  The
            realized image `L` is the SMALLEST admissible denominator
            (`L <= |G_lambda| <= ambient`), so `M/L` is the LARGEST mean and the
            concentration-FAVORABLE threshold; heavy counts obey
            `heavy_realized <= heavy_group <= heavy_ambient`, and the favorable
            `heavy_realized` is still exponential.  For base `5^i` an exponential
            effective-image collapse `c/L = (5/3)^B` (PR #759's phenomenon) IS
            present, yet the heaviest fiber exceeds the realized mean by an
            exponential factor -- the collapse benefit is insufficient.
  RUNG (c)  An image-class (`G_lambda`-coset) split is the fiber partition of the
            quotient chart `q_H o Phi`; #732 Thm A keeps (C1)-(C4) free for it.
            Over a PRIME field at depth 1 the additive image group has no proper
            subgroup, so the split degenerates to {fibers, one piece}.  Where a
            nontrivial split exists (modulus `3^B`), the count-vs-structure
            product is conserved: 0 semantic (single-unpaired-level) mass for
            every `#pieces < 3^{B-2}`.  VERDICT: hits the abundance identically.

This module is the DECIDABLE arithmetic shadow (stdlib-only, no mathlib, no
`sorry`) of the parts that are integer/combinatorial.  It formalizes the exact
finite normalization-order kernel `(ORD)` but not the exponential concentration
or decomposition conclusions.
-/

namespace NonfiberDecompositionRealizedScale

/-! ## 0. Exact binomial (multiplicative; exact partial quotients). -/

/-- `binom n k = C(n,k)` via the running product `prod_{i<k} (n-i)/(i+1)`. -/
def binom (n k : Nat) : Nat :=
  (List.range k).foldl (fun acc i => acc * (n - i) / (i + 1)) 1

/-- Realized image `L = (3^B+1)/2` (intrinsic, base-independent). -/
def realizedImage (B : Nat) : Nat := (3 ^ B + 1) / 2

/-- Full slice `M = C(2B,B)`. -/
def slice (B : Nat) : Nat := binom (2 * B) B

/-- Central (heaviest) fiber `C(B,B/2)`. -/
def maxFiber (B : Nat) : Nat := binom B (B / 2)

/-- Designed ambient modulus `c = 2*sum_{i<B} base^i + 1` (geometric sum). -/
def ambientMod (base B : Nat) : Nat := 2 * ((base ^ B - 1) / (base - 1)) + 1

/-! ## 1. RUNG (c) prime-field depth-1 degeneracy.
    `(F_p,+)` is cyclic of prime order, so its only subgroups are `{0}` and
    `F_p`; equivalently the only divisors of `p` are `1` and `p`.  Hence an
    additive image-class (coset) split at depth 1 over a prime field offers only
    the two useless extremes {fibers, one piece} -- no nontrivial candidate. -/

/-- Divisors of `n` in `[1,n]`. -/
def divisors (n : Nat) : List Nat :=
  (List.range (n + 1)).filter (fun d => d != 0 && n % d == 0)

theorem primeDivisors_7  : divisors 7  = [1, 7]  := by native_decide
theorem primeDivisors_11 : divisors 11 = [1, 11] := by native_decide
theorem primeDivisors_13 : divisors 13 = [1, 13] := by native_decide

/-- No proper nontrivial additive subgroup over the census prime fields. -/
theorem noProperSubgroup_7_11_13 :
    (divisors 7).filter (fun d => d != 1 && d != 7) = [] ∧
    (divisors 11).filter (fun d => d != 1 && d != 11) = [] ∧
    (divisors 13).filter (fun d => d != 1 && d != 13) = [] := by native_decide

/-- Contrast: the composite modulus `3^6 = 729` DOES carry proper nontrivial
    subgroups, so the degeneracy is specific to prime image groups (this is
    where a nontrivial coset split can even be posed -- and where RUNG (c)'s
    abundance argument then bites). -/
theorem compositeHasProperSubgroup :
    ((divisors 729).filter (fun d => d != 1 && d != 729)).length ≥ 4 := by
  native_decide

/-! ## 2. RUNG (a) scale decision: realized `L` is the minimal denominator, and
    the effective-image collapse (base `5^i`) is present but insufficient. -/

/-- Number of entries in one fixed finite fiber-size census satisfying the
    division-free heaviness test `K * M <= f * D`. -/
def heavyCount (fibers : List Nat) (K M D : Nat) : Nat :=
  (fibers.filter (fun f => K * M <= f * D)).length

/-- Increasing the cell scale can only increase the number of entries satisfying
    the same cross-multiplied heaviness test.  No relation between `M` and the
    sum of `fibers` is needed for this order kernel. -/
theorem heavyCount_mono_denominator (fibers : List Nat)
    (K M D₁ D₂ : Nat) (hD : D₁ <= D₂) :
    heavyCount fibers K M D₁ <= heavyCount fibers K M D₂ := by
  induction fibers with
  | nil => simp [heavyCount]
  | cons f fibers ih =>
      have ih' :
          (fibers.filter (fun f => K * M <= f * D₁)).length <=
            (fibers.filter (fun f => K * M <= f * D₂)).length := by
        simpa only [heavyCount] using ih
      have hmul : f * D₁ <= f * D₂ := Nat.mul_le_mul_left f hD
      by_cases h₁ : K * M <= f * D₁
      · have h₂ : K * M <= f * D₂ := Nat.le_trans h₁ hmul
        simpa [heavyCount, h₁, h₂] using Nat.succ_le_succ ih'
      · by_cases h₂ : K * M <= f * D₂
        · simp [heavyCount, h₁, h₂]
          exact Nat.le_succ_of_le ih'
        · simpa [heavyCount, h₁, h₂] using ih'

/-- Exact source ordering `(ORD)` for one fixed fiber-size census: if the
    realized-image cell count `L` is at most the generated-group count `G`, and
    `G` is at most the ambient count `A`, the corresponding heavy counts are
    ordered in the same direction. -/
theorem heavyCount_scale_chain (fibers : List Nat)
    (K M L G A : Nat) (hLG : L <= G) (hGA : G <= A) :
    heavyCount fibers K M L <= heavyCount fibers K M G ∧
      heavyCount fibers K M G <= heavyCount fibers K M A := by
  exact ⟨heavyCount_mono_denominator fibers K M L G hLG,
    heavyCount_mono_denominator fibers K M G A hGA⟩

/-- Realized image is strictly below the designed ambient modulus (both bases):
    the realized image does NOT fill the affine group (paper's PO5 warning). -/
theorem realized_below_ambient_base3 : realizedImage 8 < ambientMod 3 8 := by
  native_decide
theorem realized_below_ambient_base5 : realizedImage 8 < ambientMod 5 8 := by
  native_decide

/-- Base `3^i`: the collapse index `c/L -> 2` is BOUNDED (`c = 2L - 1`). -/
theorem collapse_bounded_base3 : ambientMod 3 8 = 2 * realizedImage 8 - 1 := by
  native_decide

/-- Base `5^i`: the collapse index `c/L = (5/3)^B` is EXPONENTIAL -- an
    effective-image collapse (PR #759's phenomenon) is genuinely present. -/
theorem collapse_exponential_base5 :
    ambientMod 5 8 ≥ 32 * realizedImage 8 := by native_decide

/-- ... yet INSUFFICIENT: at the concentration-favorable realized scale the
    heaviest fiber still exceeds twice the realized mean `M/L`
    (`maxFiber * L > 2 * M`), so realized-scale renormalization does not rescue
    concentration.  (`B = 8`, above the #739 small-`B` crossover.) -/
theorem collapse_insufficient_B8 : maxFiber 8 * realizedImage 8 > 2 * slice 8 := by
  native_decide

/-! ## 3. RUNG (c) abundance recurs.  The Python verifier establishes by exact
    enumeration that a mod-`3^j` coset coarsening of the Sidon-paired chart puts
    ZERO single-unpaired-level (semantic-candidate) mass in its classes for
    every `#pieces < 3^{B-2}`; the first semantic mass appears at modulus
    `3^{B-2}` and full resolution at `3^{B-1}`.  Both crossovers are
    super-polynomial, so no subexponential coset split carries semantic charge.
    Arithmetic shadow (the enumeration itself lives in Python, like #739). -/

/-- The first-semantic-mass crossover modulus `3^{B-2}` is super-polynomial:
    at `B = 60` it exceeds `60^12` (a degree-12 polynomial in `N = 2B = 120`). -/
theorem crossover_superpoly : (3 : Nat) ^ 58 > 60 ^ 12 := by native_decide

/-- Full-resolution modulus `3^{B-1}` dominates the first-semantic `3^{B-2}` and
    is likewise super-polynomial -- packaged with the crossover. -/
theorem abundance_recurs_B60 :
    (3 : Nat) ^ 58 > 60 ^ 12 ∧ (3 : Nat) ^ 59 > 3 ^ 58 := by native_decide

end NonfiberDecompositionRealizedScale
