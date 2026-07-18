import Std

/-!
# KoalaBear row-sharp Route-D pivot obstruction

This standalone, Std-only module kernel-checks two facts used by the Route-D
guardrail:

* the deployed product `67472 * 2130706433`;
* the exact singular `6 x 6` RIM specialization over `F_17` and its displayed
  nonzero kernel witness.

The final support certificate is present only as an explicitly unproved adapter
target.  Nothing in this file proves the deployed row-sharp Q bound.
-/

namespace KbRowsharpRouteDPivotObstruction

def deployedP : Nat := 2130706433
def deployedT : Nat := 67472
def deployedSupportBudget : Nat := 143763024447376

theorem deployed_support_budget_exact :
    deployedT * deployedP = deployedSupportBudget := by
  native_decide

abbrev F17 := Fin 17

def rimMatrix : Fin 6 → Fin 6 → F17
  | 0, 0 => 1 | 0, 1 => 1  | 0, 2 => 1  | 0, 3 => 0  | 0, 4 => 0  | 0, 5 => 0
  | 1, 0 => 1 | 1, 1 => 2  | 1, 2 => 4  | 1, 3 => 0  | 1, 4 => 0  | 1, 5 => 0
  | 2, 0 => 0 | 2, 1 => 0  | 2, 2 => 0  | 2, 3 => 1  | 2, 4 => 4  | 2, 5 => 16
  | 3, 0 => 0 | 3, 1 => 0  | 3, 2 => 0  | 3, 3 => 1  | 3, 4 => 13 | 3, 5 => 16
  | 4, 0 => 1 | 4, 1 => 8  | 4, 2 => 13 | 4, 3 => 16 | 4, 4 => 9  | 4, 5 => 4
  | 5, 0 => 1 | 5, 1 => 16 | 5, 2 => 1  | 5, 3 => 16 | 5, 4 => 1  | 5, 5 => 16

def rimKernel : Fin 6 → F17
  | 0 => 2
  | 1 => 14
  | 2 => 1
  | 3 => 3
  | 4 => 0
  | 5 => 3

def rimProduct (i : Fin 6) : F17 :=
  rimMatrix i 0 * rimKernel 0 +
  rimMatrix i 1 * rimKernel 1 +
  rimMatrix i 2 * rimKernel 2 +
  rimMatrix i 3 * rimKernel 3 +
  rimMatrix i 4 * rimKernel 4 +
  rimMatrix i 5 * rimKernel 5

theorem rim_kernel_nonzero : rimKernel 0 ≠ 0 := by
  decide

theorem rim_matrix_times_kernel_zero :
    ∀ i : Fin 6, rimProduct i = 0 := by
  native_decide

theorem rim_specialization_is_singular :
    rimKernel ≠ (fun _ => 0) ∧ ∀ i : Fin 6, rimProduct i = 0 := by
  constructor
  · intro h
    have h0 := congrFun h 0
    exact rim_kernel_nonzero h0
  · exact rim_matrix_times_kernel_zero

/-!
The common core stays marked in the adapter data.  The propositions below are
abstract on purpose: this package does not pretend to formalize or discharge
the named first-match branches.
-/

structure NamedFirstMatchResidual (α : Type) where
  generatedPrefix : List α
  primitiveFullRank : List α
  commonCoreMarkPreserved : Prop
  generatedFieldDeleted : Prop
  quotientPlantedDeleted : Prop
  sparsePadeHankelDeleted : Prop
  m1WindowShadowDeleted : Prop
  rankDropPivotDeleted : Prop
  bcChartDeleted : Prop
  spShiftPairDeleted : Prop
  extensionSlopeDeleted : Prop

/--
UNPROVED ADAPTER TARGET.  This is the exact support inequality still required
after the named first-match deletions.  The singular RIM witness above explains
why `rankDropPivotDeleted` must be an explicit hypothesis; it does not prove
this target or any numerical row-sharp Q certificate.
-/
theorem rowSharpPrimitiveSupportCertificate_target_unproved
    {α : Type} (packet : NamedFirstMatchResidual α)
    (_hCommonCore : packet.commonCoreMarkPreserved)
    (_hGenerated : packet.generatedFieldDeleted)
    (_hQuotient : packet.quotientPlantedDeleted)
    (_hPade : packet.sparsePadeHankelDeleted)
    (_hWindow : packet.m1WindowShadowDeleted)
    (_hRankDrop : packet.rankDropPivotDeleted)
    (_hBC : packet.bcChartDeleted)
    (_hSP : packet.spShiftPairDeleted)
    (_hExtension : packet.extensionSlopeDeleted) :
    packet.generatedPrefix.length + packet.primitiveFullRank.length ≤
      deployedSupportBudget := by
  sorry

end KbRowsharpRouteDPivotObstruction
