import Mathlib

/-!
# Arithmetic kernels for the RF3'' global-degree bridge

The accompanying audit note proves the finite-field factor/Hensel theorem on
paper. This module records its full typed interface and certifies the
elementary integer identities that carry the corrected nonlinear weights,
the direct linear branch, the global factor-pair sum, RF3'' aggregation, the
top-incidence guard, and the chosen-support count.

GlobalDegreeRetainedFactorBridgeTarget is a proposition, not an axiom or a
theorem. The algebraic-function-field proof is not formalized here.
-/

namespace PavingRetainedFactorLift.GlobalDegreeBridge

open scoped BigOperators

set_option autoImplicit false

universe u

/-- Typed data for the paper-proved RF3'' bridge. rootIdentity is the
proposition that Q(X, P_gamma(X), gamma) is the zero polynomial; it remains
abstract until multivariate substitution and Hensel lifting are formalized. -/
structure BridgeInstance (F : Type u) [Field F] [Fintype F] where
  n : ℕ
  K : ℕ
  A : ℕ
  r : ℕ
  U : ℕ
  d : ℕ
  G : ℕ
  domain : Finset F
  Q : MvPolynomial (Fin 3) F
  slopes : Finset F
  P : F → Polynomial F
  chosenSupport : F → Finset F
  u0 : F → F
  u1 : F → F
  rootIdentity : F → Prop

/-- The exact monomial caps used by the integer core theorem. Coordinates
0, 1, 2 stand for X, Y, Z. -/
def DegreeCaps {F : Type u} [Field F] [Fintype F]
    (I : BridgeInstance F) : Prop :=
  I.Q ≠ 0 ∧
    ∀ e ∈ I.Q.support,
      e (0 : Fin 3) + I.K * e (1 : Fin 3) ≤ I.U - 1 ∧
      e (1 : Fin 3) ≤ I.d ∧
      e (1 : Fin 3) + e (2 : Fin 3) ≤ I.G

def SimultaneouslyExplained {F : Type u} [Field F] [Fintype F]
    (I : BridgeInstance F) : Prop :=
  ∃ gamma ∈ I.slopes, ∃ v0 v1 : Polynomial F,
    v0.natDegree < I.K ∧ v1.natDegree < I.K ∧
      (∀ x ∈ I.chosenSupport gamma, v0.eval x = I.u0 x) ∧
      (∀ x ∈ I.chosenSupport gamma, v1.eval x = I.u1 x)

/-- Full theorem-shaped interface proved in the companion note with the
integer threshold (1 + 2 U d^2) G + (r+1)d. This definition asserts
nothing by itself. -/
def GlobalDegreeRetainedFactorBridgeTarget : Prop :=
  ∀ (F : Type u) [Field F] [Fintype F] (I : BridgeInstance F),
    1 ≤ I.K →
    I.domain.card = I.n →
    I.A = I.n - I.r →
    I.K + 2 ≤ I.A →
    DegreeCaps I →
    ringChar F > I.d →
    Fintype.card F > 2 * I.U * I.d →
    (I.A - I.K) * (2 * I.U - 1) >
      (I.n - I.K) * (2 * I.K - 1) →
    (∀ gamma ∈ I.slopes,
      I.rootIdentity gamma ∧
      (I.P gamma).natDegree < I.K ∧
      I.chosenSupport gamma ⊆ I.domain ∧
      (I.chosenSupport gamma).card = I.A ∧
      ∀ x ∈ I.chosenSupport gamma,
        (I.P gamma).eval x = I.u0 x + gamma * I.u1 x) →
    I.slopes.card >
      (1 + 2 * I.U * I.d ^ 2) * I.G + (I.r + 1) * I.d →
    SimultaneouslyExplained I

/-- Corrected nonlinear slack: y = g-b+1-w. -/
def nonlinearY (b g w : ℤ) : ℤ := g - b + 1 - w

/-- Corrected derivative-numerator allowance. -/
def nonlinearChi (a b g w : ℤ) : ℤ :=
  a * g - 1 - (a - 1) * b - w

/-- Corrected numerator weight for positive Hensel index t. -/
def nonlinearL (a b g w t : ℤ) : ℤ :=
  nonlinearY b g w + (t + 1) * w +
    (2 * t - 1) * nonlinearChi a b g w

theorem nonlinear_chi_forms (a b g w : ℤ) :
    nonlinearChi a b g w =
      g - a + (a - 1) * nonlinearY b g w + (a - 2) * w := by
  unfold nonlinearChi nonlinearY
  ring

/-- Exact positive gap behind L_t < (2t+1)ag for t >= 1. -/
theorem nonlinear_weight_gap_identity (a b g w t : ℤ) :
    (2 * t + 1) * a * g - nonlinearL a b g w t =
      2 * a * g - g + b - 1 + (t - 1) * w +
        (2 * t - 1) * (1 + (a - 1) * b) := by
  unfold nonlinearL nonlinearChi nonlinearY
  ring

/-- Exact positive gap behind the nonlinear pole deletion. -/
theorem nonlinear_pole_gap_identity (a b g w : ℤ) :
    a * b * g - (w + b * nonlinearChi a b g w) =
      b + b ^ 2 * (a - 1) + (b - 1) * w := by
  unfold nonlinearChi
  ring

/-- The direct linear recurrence numerator has this exact coarse gap. -/
theorem linear_numerator_gap_identity (t g : ℤ) :
    (2 * t + 1) * g - ((t + 1) * g - t) = t * (g + 1) := by
  ring

/-- Every convolution term in the direct linear recurrence has the same
degree allowance. -/
theorem linear_recurrence_term_identity (t s g : ℤ) :
    (g - 1) + ((t - s + 1) * g - (t - s)) +
        (s - 1) * (g - 1) =
      (t + 1) * g - t := by
  ring

/-- The fixed-denominator affine numerator in the linear branch fits the
(2K-1)g coordinate charge. -/
theorem linear_affine_gap_identity (K g : ℤ) :
    (2 * K - 1) * g - (K * g - K + 1) =
      (K - 1) * (g + 1) := by
  ring

/-- Sum a_i^2 g_i using the global factor-degree budget. -/
theorem factorSquareCharge_le {ι : Type u} [DecidableEq ι]
    (s : Finset ι) (a g : ι → ℕ) (d G : ℕ)
    (ha : ∀ i ∈ s, a i ≤ d)
    (hG : ∑ i ∈ s, g i ≤ G) :
    ∑ i ∈ s, a i * a i * g i ≤ d * d * G := by
  calc
    ∑ i ∈ s, a i * a i * g i
        ≤ ∑ i ∈ s, d * d * g i := by
          apply Finset.sum_le_sum
          intro i hi
          exact Nat.mul_le_mul
            (Nat.mul_le_mul (ha i hi) (ha i hi))
            (Nat.le_refl (g i))
    _ = d * d * (∑ i ∈ s, g i) := by
          simp [Finset.mul_sum]
    _ ≤ d * d * G := Nat.mul_le_mul_left (d * d) hG

/-- Content, pair charge, and pair count combine to RF3''. -/
theorem rf3DoublePrimeAggregation
    (content pairCharge pairCount d G U r : ℕ)
    (hcontent : content ≤ G)
    (hcharge : pairCharge ≤ d ^ 2 * G)
    (hpairs : pairCount ≤ d) :
    content + 2 * U * pairCharge + (r + 1) * pairCount
      ≤ (1 + 2 * U * d ^ 2) * G + (r + 1) * d := by
  have hscaledCharge :
      2 * U * pairCharge ≤ 2 * U * (d ^ 2 * G) :=
    Nat.mul_le_mul_left (2 * U) hcharge
  have hscaledPairs :
      (r + 1) * pairCount ≤ (r + 1) * d :=
    Nat.mul_le_mul_left (r + 1) hpairs
  nlinarith

/-- Abstract form of the v9.2 top-guard strengthening. Put
p=A-K-1, s=n-K-1, L=2U-1, and M=2K-1. -/
theorem topGuard_strengthening (p s L M : ℤ)
    (hs : 0 < s) (hL : 0 ≤ L) (hps : p ≤ s)
    (hstrong : s * (M + 2) < p * L) :
    (s + 1) * M < (p + 1) * L := by
  have hpLle : p * L ≤ s * L :=
    mul_le_mul_of_nonneg_right hps hL
  have hsML : s * (M + 2) < s * L :=
    lt_of_lt_of_le hstrong hpLle
  have hML : M + 2 < L := by
    nlinarith
  nlinarith

/-- The chosen-support bad set has size at most r. -/
theorem chosenSupport_badSet_le (B T r : ℤ)
    (hr : 0 ≤ r)
    (hT : r + 1 < T)
    (hcount : B * (T - 1) ≤ r * T) :
    B ≤ r := by
  by_contra h
  have hB : r + 1 ≤ B := by omega
  have hTm : 0 ≤ T - 1 := by omega
  have hmul :
      (r + 1) * (T - 1) ≤ B * (T - 1) :=
    mul_le_mul_of_nonneg_right hB hTm
  have hstrict : r * T < (r + 1) * (T - 1) := by
    nlinarith
  nlinarith

#print axioms nonlinear_chi_forms
#print axioms nonlinear_weight_gap_identity
#print axioms nonlinear_pole_gap_identity
#print axioms linear_numerator_gap_identity
#print axioms linear_recurrence_term_identity
#print axioms linear_affine_gap_identity
#print axioms factorSquareCharge_le
#print axioms rf3DoublePrimeAggregation
#print axioms topGuard_strengthening
#print axioms chosenSupport_badSet_le

end PavingRetainedFactorLift.GlobalDegreeBridge
