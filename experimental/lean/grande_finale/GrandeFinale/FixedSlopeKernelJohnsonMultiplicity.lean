import GrandeFinale.DirectionDistanceAllPairs
import GrandeFinale.SetSystemJohnson

/-!
# Fixed-slope kernel-Johnson multiplicity

This module proves the fixed-slope Johnson statement and the arithmetic
specialization used by the canonical A6 parameters.

For a fixed slope, two error words differ by a word in the kernel.  A kernel
distance lower bound therefore limits the intersection of their agreement
supports.  The target below packages the resulting Johnson double count; its
proof is obtained from the reusable finite set-system Johnson inequality.
-/

open scoped BigOperators Classical
noncomputable section

namespace GrandeFinale
namespace FixedSlopeKernelJohnsonMultiplicity

open DirectionDistanceAllPairs

set_option autoImplicit false

variable {D F W : Type*}
variable [Fintype D] [DecidableEq D]
variable [Field F] [DecidableEq F]
variable [AddCommGroup W] [Module F W]

/-- The pairs in P whose first coordinate is the prescribed slope. -/
def fixedSlopeFiber
    (P : Finset (SlopeErrorPair D F)) (gamma : F) :
    Finset (SlopeErrorPair D F) :=
  P.filter fun p => p.1 = gamma

/-- The denominator in the fixed-slope kernel-Johnson double count. -/
def kernelJohnsonDenominator (N t kappa : Nat) : Nat :=
  (N - t) ^ 2 - N * (kappa - 1)

/-- The numerator in the fixed-slope kernel-Johnson double count. -/
def kernelJohnsonNumerator (N t kappa : Nat) : Nat :=
  N * ((N - t) - (kappa - 1))

/-- Positivity of the fixed-slope kernel-Johnson denominator. -/
def KernelJohnsonPositive (N t kappa : Nat) : Prop :=
  N * (kappa - 1) < (N - t) ^ 2

/-- The multiplicative and quotient forms of the Johnson conclusion. -/
def FixedSlopeKernelJohnsonConclusion
    (P : Finset (SlopeErrorPair D F)) (gamma : F)
    (t kappa : Nat) : Prop :=
  let N := Fintype.card D
  let denominator := kernelJohnsonDenominator N t kappa
  let numerator := kernelJohnsonNumerator N t kappa
  (fixedSlopeFiber P gamma).card * denominator ≤ numerator ∧
    (KernelJohnsonPositive N t kappa →
      (fixedSlopeFiber P gamma).card ≤ numerator / denominator)

/-- A finite family of errors in one fixed syndrome class, all of weight at
most `t`. -/
def FixedSyndromeHypotheses
    (H : (D → F) →ₗ[F] W) (y : W) (E : Finset (D → F)) (t : Nat) : Prop :=
  ∀ e ∈ E, H e = y ∧ weight e ≤ t

/-- The unconditional multiplicative bound and positivity-gated quotient bound
for a fixed-syndrome error family. -/
def FixedSyndromeKernelJohnsonConclusion
    (E : Finset (D → F)) (t kappa : Nat) : Prop :=
  let N := Fintype.card D
  let denominator := kernelJohnsonDenominator N t kappa
  let numerator := kernelJohnsonNumerator N t kappa
  E.card * denominator ≤ numerator ∧
    (KernelJohnsonPositive N t kappa → E.card ≤ numerator / denominator)

/-- The proposition surface for the fixed-slope kernel-Johnson multiplicity
lemma, proved by `fixedSlopeKernelJohnsonMultiplicity` below. -/
def fixedSlopeKernelJohnsonMultiplicityTarget
    (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (P : Finset (SlopeErrorPair D F)) (gamma : F)
    (t kappa : Nat) : Prop :=
  let N := Fintype.card D
  BasicPairHypotheses H y₀ y₁ P t →
    KernelDistanceAtLeast H (N - kappa + 1) →
    0 < kappa →
    kappa ≤ N →
    t ≤ N →
    FixedSlopeKernelJohnsonConclusion P gamma t kappa

/-! ## Zero blocks and the fixed-slope kernel application -/

/-- The zero coordinates of a word. -/
def zeroSet (z : D → F) : Finset D :=
  Finset.univ.filter fun x => z x = 0

theorem zeroSet_eq_sdiff_wordSupport (z : D → F) :
    zeroSet z = Finset.univ \ wordSupport z := by
  ext x
  simp [zeroSet, wordSupport]

theorem zeroSet_card (z : D → F) :
    (zeroSet z).card = Fintype.card D - weight z := by
  rw [zeroSet_eq_sdiff_wordSupport, Finset.card_sdiff]
  simp [weight]

/-- A deterministic `a`-subset of `s`, empty if no such subset exists. -/
noncomputable def truncateTo (a : Nat) (s : Finset D) : Finset D :=
  if h : a ≤ s.card then Classical.choose (Finset.exists_subset_card_eq h) else ∅

omit [Fintype D] [DecidableEq D] in
theorem truncateTo_spec (a : Nat) (s : Finset D) (h : a ≤ s.card) :
    truncateTo a s ⊆ s ∧ (truncateTo a s).card = a := by
  rw [truncateTo, dif_pos h]
  exact Classical.choose_spec (Finset.exists_subset_card_eq h)

omit [DecidableEq D] in
theorem weight_le_length (z : D → F) :
    weight z ≤ Fintype.card D := by
  exact Finset.card_le_card (Finset.subset_univ (wordSupport z))

/-- The exact `(N-t)`-subset chosen from the zero coordinates of an error. -/
noncomputable def chosenZeroSet (t : Nat) (p : SlopeErrorPair D F) : Finset D :=
  truncateTo (Fintype.card D - t) (zeroSet p.2)

theorem chosenZeroSet_spec
    (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (P : Finset (SlopeErrorPair D F)) (gamma : F) (t : Nat)
    (hbasic : BasicPairHypotheses H y₀ y₁ P t)
    (ht : t ≤ Fintype.card D)
    {p : SlopeErrorPair D F} (hp : p ∈ fixedSlopeFiber P gamma) :
    chosenZeroSet t p ⊆ zeroSet p.2 ∧
      (chosenZeroSet t p).card = Fintype.card D - t := by
  have hpP : p ∈ P := (Finset.mem_filter.mp hp).1
  have hweight : weight p.2 ≤ t := hbasic.2.2 p hpP
  have hzero : Fintype.card D - t ≤ (zeroSet p.2).card := by
    rw [zeroSet_card]
    omega
  exact truncateTo_spec _ _ hzero

omit [DecidableEq D] in
theorem fixedSlope_sub_mem_kernel
    (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (P : Finset (SlopeErrorPair D F)) (gamma : F) (t : Nat)
    (hbasic : BasicPairHypotheses H y₀ y₁ P t)
    {p q : SlopeErrorPair D F}
    (hp : p ∈ fixedSlopeFiber P gamma)
    (hq : q ∈ fixedSlopeFiber P gamma) :
    H (p.2 - q.2) = 0 := by
  have hpP : p ∈ P := (Finset.mem_filter.mp hp).1
  have hqP : q ∈ P := (Finset.mem_filter.mp hq).1
  have hpgamma : p.1 = gamma := (Finset.mem_filter.mp hp).2
  have hqgamma : q.1 = gamma := (Finset.mem_filter.mp hq).2
  rw [map_sub, hbasic.2.1 p hpP, hbasic.2.1 q hqP, hpgamma, hqgamma]
  simp

omit [Fintype D] [DecidableEq D] in
theorem fixedSlope_sub_ne_zero
    (P : Finset (SlopeErrorPair D F)) (gamma : F)
    {p q : SlopeErrorPair D F}
    (hp : p ∈ fixedSlopeFiber P gamma)
    (hq : q ∈ fixedSlopeFiber P gamma)
    (hpq : p ≠ q) :
    p.2 - q.2 ≠ 0 := by
  apply sub_ne_zero.mpr
  intro herr
  apply hpq
  apply Prod.ext
  · exact (Finset.mem_filter.mp hp).2.trans (Finset.mem_filter.mp hq).2.symm
  · exact herr

theorem zeroSet_inter_subset_sub_zeroSet (p q : D → F) :
    zeroSet p ∩ zeroSet q ⊆ zeroSet (p - q) := by
  intro x hx
  simp only [Finset.mem_inter, zeroSet, Finset.mem_filter, Finset.mem_univ,
    true_and] at hx ⊢
  simp [hx.1, hx.2]

/-- The fixed-syndrome kernel-Johnson theorem in the direct error-family
interface of Theorem 1 in the companion note. The product inequality is
unconditional; only the quotient conclusion assumes denominator positivity. -/
theorem fixedSyndromeKernelJohnsonMultiplicity
    (H : (D → F) →ₗ[F] W) (y : W)
    (E : Finset (D → F)) (t kappa : Nat)
    (hfixed : FixedSyndromeHypotheses H y E t)
    (hkernel : KernelDistanceAtLeast H (Fintype.card D - kappa + 1))
    (hkappaPos : 0 < kappa)
    (hkappaN : kappa ≤ Fintype.card D)
    (ht : t ≤ Fintype.card D) :
    FixedSyndromeKernelJohnsonConclusion E t kappa := by
  let B : (D → F) → Finset D := fun e =>
    truncateTo (Fintype.card D - t) (zeroSet e)
  have hspec :
      ∀ e ∈ E, B e ⊆ zeroSet e ∧
        (B e).card = Fintype.card D - t := by
    intro e he
    have hweight : weight e ≤ t := (hfixed e he).2
    have hzero : Fintype.card D - t ≤ (zeroSet e).card := by
      rw [zeroSet_card]
      omega
    exact truncateTo_spec _ _ hzero
  have hcard :
      ∀ e ∈ E, (B e).card = Fintype.card D - t := by
    intro e he
    exact (hspec e he).2
  have hinter :
      ∀ e ∈ E, ∀ f ∈ E, e ≠ f → (B e ∩ B f).card ≤ kappa - 1 := by
    intro e he f hf hef
    have hsubset : B e ∩ B f ⊆ zeroSet (e - f) := by
      exact Finset.Subset.trans
        (Finset.inter_subset_inter (hspec e he).1 (hspec f hf).1)
        (zeroSet_inter_subset_sub_zeroSet e f)
    have hHzero : H (e - f) = 0 := by
      rw [map_sub, (hfixed e he).1, (hfixed f hf).1]
      simp
    have hdistance := hkernel (e - f) hHzero (sub_ne_zero.mpr hef)
    have hweightN := weight_le_length (e - f)
    calc
      (B e ∩ B f).card ≤ (zeroSet (e - f)).card :=
        Finset.card_le_card hsubset
      _ = Fintype.card D - weight (e - f) := zeroSet_card _
      _ ≤ kappa - 1 := by omega
  have hmultiplicative :=
    SetSystemJohnson.setSystemJohnson E B
      (Fintype.card D - t) (kappa - 1) hcard hinter
  dsimp [FixedSyndromeKernelJohnsonConclusion]
  refine ⟨?_, ?_⟩
  · simpa [kernelJohnsonDenominator, kernelJohnsonNumerator] using hmultiplicative
  · intro hpositive
    have hdenominator :
        0 < (Fintype.card D - t) ^ 2 - Fintype.card D * (kappa - 1) := by
      dsimp [KernelJohnsonPositive] at hpositive
      omega
    have hquotient :=
      SetSystemJohnson.setSystemJohnson_div E B
        (Fintype.card D - t) (kappa - 1) hcard hinter hdenominator
    simpa [kernelJohnsonDenominator, kernelJohnsonNumerator] using hquotient

#print axioms fixedSyndromeKernelJohnsonMultiplicity

theorem chosenZeroSet_inter_le
    (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (P : Finset (SlopeErrorPair D F)) (gamma : F) (t kappa : Nat)
    (hbasic : BasicPairHypotheses H y₀ y₁ P t)
    (hkernel : KernelDistanceAtLeast H (Fintype.card D - kappa + 1))
    (hkappaPos : 0 < kappa)
    (hkappaN : kappa ≤ Fintype.card D)
    (ht : t ≤ Fintype.card D)
    {p q : SlopeErrorPair D F}
    (hp : p ∈ fixedSlopeFiber P gamma)
    (hq : q ∈ fixedSlopeFiber P gamma)
    (hpq : p ≠ q) :
    (chosenZeroSet t p ∩ chosenZeroSet t q).card ≤ kappa - 1 := by
  have hpSpec := chosenZeroSet_spec H y₀ y₁ P gamma t hbasic ht hp
  have hqSpec := chosenZeroSet_spec H y₀ y₁ P gamma t hbasic ht hq
  have hsubset :
      chosenZeroSet t p ∩ chosenZeroSet t q ⊆ zeroSet (p.2 - q.2) := by
    exact Finset.Subset.trans
      (Finset.inter_subset_inter hpSpec.1 hqSpec.1)
      (zeroSet_inter_subset_sub_zeroSet p.2 q.2)
  have hHzero := fixedSlope_sub_mem_kernel H y₀ y₁ P gamma t hbasic hp hq
  have hdiffNe := fixedSlope_sub_ne_zero P gamma hp hq hpq
  have hdistance := hkernel (p.2 - q.2) hHzero hdiffNe
  have hweightN := weight_le_length (p.2 - q.2)
  calc
    (chosenZeroSet t p ∩ chosenZeroSet t q).card
        ≤ (zeroSet (p.2 - q.2)).card := Finset.card_le_card hsubset
    _ = Fintype.card D - weight (p.2 - q.2) := zeroSet_card _
    _ ≤ kappa - 1 := by omega

/-- The fixed-slope kernel-Johnson multiplicity theorem. -/
theorem fixedSlopeKernelJohnsonMultiplicity
    (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (P : Finset (SlopeErrorPair D F)) (gamma : F)
    (t kappa : Nat) :
    fixedSlopeKernelJohnsonMultiplicityTarget H y₀ y₁ P gamma t kappa := by
  dsimp [fixedSlopeKernelJohnsonMultiplicityTarget]
  intro hbasic hkernel hkappaPos hkappaN ht
  have hcard :
      ∀ p ∈ fixedSlopeFiber P gamma,
        (chosenZeroSet t p).card = Fintype.card D - t := by
    intro p hp
    exact (chosenZeroSet_spec H y₀ y₁ P gamma t hbasic ht hp).2
  have hinter :
      ∀ p ∈ fixedSlopeFiber P gamma,
        ∀ q ∈ fixedSlopeFiber P gamma, p ≠ q →
          (chosenZeroSet t p ∩ chosenZeroSet t q).card ≤ kappa - 1 := by
    intro p hp q hq hpq
    exact chosenZeroSet_inter_le H y₀ y₁ P gamma t kappa hbasic hkernel
      hkappaPos hkappaN ht hp hq hpq
  have hmultiplicative :=
    SetSystemJohnson.setSystemJohnson
      (fixedSlopeFiber P gamma) (chosenZeroSet t)
      (Fintype.card D - t) (kappa - 1) hcard hinter
  exact ⟨by
      simpa [kernelJohnsonDenominator, kernelJohnsonNumerator] using hmultiplicative,
    by
      intro hpositive
      have hdenominator :
          0 < (Fintype.card D - t) ^ 2 - Fintype.card D * (kappa - 1) := by
        dsimp [KernelJohnsonPositive] at hpositive
        omega
      have hquotient :=
        SetSystemJohnson.setSystemJohnson_div
          (fixedSlopeFiber P gamma) (chosenZeroSet t)
          (Fintype.card D - t) (kappa - 1) hcard hinter hdenominator
      simpa [kernelJohnsonDenominator, kernelJohnsonNumerator] using hquotient⟩

#print axioms fixedSlopeKernelJohnsonMultiplicity

/-! ## Canonical A6 arithmetic -/

def canonicalA6Length (r : Nat) : Nat := 500 * r

def canonicalA6KernelDimension (r : Nat) : Nat := 225 * r

def canonicalA6Radius (r : Nat) : Nat := 150 * r

def canonicalA6Agreement (r : Nat) : Nat :=
  canonicalA6Length r - canonicalA6Radius r

def canonicalA6Denominator (r : Nat) : Nat :=
  kernelJohnsonDenominator
    (canonicalA6Length r) (canonicalA6Radius r)
    (canonicalA6KernelDimension r)

def canonicalA6Numerator (r : Nat) : Nat :=
  kernelJohnsonNumerator
    (canonicalA6Length r) (canonicalA6Radius r)
    (canonicalA6KernelDimension r)

def canonicalA6KernelCap (r : Nat) : Nat :=
  canonicalA6Numerator r / canonicalA6Denominator r

theorem canonicalA6_agreement (r : Nat) :
    canonicalA6Agreement r = 350 * r := by
  simp [canonicalA6Agreement, canonicalA6Length, canonicalA6Radius]
  omega

theorem canonicalA6_denominator (r : Nat) (hr : 1 ≤ r) :
    canonicalA6Denominator r = 500 * r * (20 * r + 1) := by
  rw [canonicalA6Denominator, kernelJohnsonDenominator]
  change (500 * r - 150 * r) ^ 2 - 500 * r * (225 * r - 1) = _
  have hagree : 500 * r - 150 * r = 350 * r := by omega
  rw [hagree]
  have hsum : (225 * r - 1) + (20 * r + 1) = 245 * r := by omega
  have hid :
      (350 * r) ^ 2 =
        500 * r * (225 * r - 1) + 500 * r * (20 * r + 1) := by
    calc
      (350 * r) ^ 2 = 500 * r * (245 * r) := by ring
      _ = 500 * r * ((225 * r - 1) + (20 * r + 1)) := by rw [hsum]
      _ = 500 * r * (225 * r - 1) + 500 * r * (20 * r + 1) := by ring
  omega

theorem canonicalA6_numerator (r : Nat) (hr : 1 ≤ r) :
    canonicalA6Numerator r = 500 * r * (125 * r + 1) := by
  rw [canonicalA6Numerator, kernelJohnsonNumerator]
  change 500 * r * ((500 * r - 150 * r) - (225 * r - 1)) = _
  have hagree : 500 * r - 150 * r = 350 * r := by omega
  rw [hagree]
  have hinner : 350 * r - (225 * r - 1) = 125 * r + 1 := by omega
  rw [hinner]

theorem canonicalA6_denominator_pos (r : Nat) (hr : 1 ≤ r) :
    0 < canonicalA6Denominator r := by
  rw [canonicalA6_denominator r hr]
  positivity

theorem canonicalA6_kernel_cap (r : Nat) (hr : 1 ≤ r) :
    canonicalA6KernelCap r = 6 := by
  rw [canonicalA6KernelCap, canonicalA6_numerator r hr,
    canonicalA6_denominator r hr]
  have hden : 0 < 500 * r * (20 * r + 1) := by positivity
  have hlower :
      6 * (500 * r * (20 * r + 1)) ≤ 500 * r * (125 * r + 1) := by
    nlinarith
  have hupper :
      500 * r * (125 * r + 1) < 7 * (500 * r * (20 * r + 1)) := by
    nlinarith
  apply Nat.le_antisymm
  · have hlt :
        (500 * r * (125 * r + 1)) / (500 * r * (20 * r + 1)) < 7 :=
      (Nat.div_lt_iff_lt_mul hden).2 hupper
    omega
  · exact (Nat.le_div_iff_mul_le hden).2 hlower

theorem canonicalA6_multiplicity_le_six
    (r multiplicity : Nat) (hr : 1 ≤ r)
    (hcount : multiplicity * canonicalA6Denominator r ≤
      canonicalA6Numerator r) :
    multiplicity ≤ 6 := by
  have hden := canonicalA6_denominator_pos r hr
  have hdiv : multiplicity ≤ canonicalA6KernelCap r := by
    exact (Nat.le_div_iff_mul_le hden).2 hcount
  rwa [canonicalA6_kernel_cap r hr] at hdiv

/-! ## Composition with the fixed-direction slope bound -/

def fixedDirectionSlopeBound (D : Nat) : Nat :=
  1165 + 3744 * D ^ 6

def composedA6Bound (D : Nat) : Nat :=
  6 * fixedDirectionSlopeBound D

theorem composedA6Bound_eq (D : Nat) :
    composedA6Bound D = 6990 + 22464 * D ^ 6 := by
  simp [composedA6Bound, fixedDirectionSlopeBound]
  ring

theorem canonicalA6_compose_fixed_direction_bound
    (D slopeCount pairCount : Nat)
    (hslopes : slopeCount ≤ fixedDirectionSlopeBound D)
    (hpairs : pairCount ≤ 6 * slopeCount) :
    pairCount ≤ 6990 + 22464 * D ^ 6 := by
  calc
    pairCount ≤ 6 * slopeCount := hpairs
    _ ≤ 6 * fixedDirectionSlopeBound D := Nat.mul_le_mul_left 6 hslopes
    _ = composedA6Bound D := rfl
    _ = 6990 + 22464 * D ^ 6 := composedA6Bound_eq D

end FixedSlopeKernelJohnsonMultiplicity
end GrandeFinale
