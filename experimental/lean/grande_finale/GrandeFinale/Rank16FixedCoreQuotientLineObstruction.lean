import Mathlib

/-!
# Rank-16 fixed-core quotient-line obstruction: statement target

This module is an **UNPROVED STATEMENT TARGET** for
`experimental/notes/l2/rank16_fixed_core_quotient_line_obstruction.md`.
It records the post-core fixed-syndrome equation, full-fiber factors,
root-free generator, splitting hypothesis, affine-line normalization, and
the exact conclusion `card <= 5`. It proves no affine-line ownership, cap
eight, parent saving, rank-16 closure, Grand List theorem, or score change.
-/

open scoped Classical
open Polynomial

noncomputable section

namespace GrandeFinale
namespace Rank16FixedCoreQuotientLineObstruction

set_option autoImplicit false

universe u v

variable {F : Type u} {I : Type v}
variable [Field F] [Fintype F] [DecidableEq F] [DecidableEq I]

def baseFieldPrime : Nat := 2130706433
def evaluationDomainSize : Nat := 2097152
def blockSize : Nat := 32768
def fixedCoreSize : Nat := 27
def generatorDegree : Nat := 67472
def postCoreLocatorDegree : Nat := 96369
def quotientDegreeCeiling : Nat := 28897

/-- `P` splits completely, with every root in the deployed subgroup. -/
def SplitsOver (H : Finset F) (P : F[X]) : Prop :=
  P.roots.card = P.natDegree ∧ ∀ x ∈ P.roots, x ∈ H

/-- The generator has no root on the deployed evaluation subgroup. -/
def RootFreeOn (H : Finset F) (g : F[X]) : Prop :=
  ∀ x ∈ H, g.eval x ≠ 0

/-- The complete `B`-fiber over `y` is present in the deployed subgroup. -/
def HasCompleteFiber (H : Finset F) (y : F) : Prop :=
  (H.filter fun x ↦ x ^ blockSize = y).card = blockSize

/-- The normalized Pade quotients indexed by `S` lie on one affine line. -/
def OnAffineLine (S : Finset I) (V : I → F[X]) : Prop :=
  ∃ V0 V1 : F[X], ∃ c : I → F,
    ∀ i ∈ S, V i = V0 + C (c i) * V1

/--
**UNPROVED STATEMENT TARGET.** Six distinct extra full-fiber labels cannot
occur in one normalized quotient affine line in the exact post-core source
cell.
-/
def fixedCoreQuotientLineObstructionTarget
    (H : Finset F) (S : Finset I) (A W V : I → F[X])
    (q y : I → F) (h g : F[X]) : Prop :=
  Fintype.card F = baseFieldPrime →
    H.card = evaluationDomainSize →
    g.natDegree = generatorDegree →
    RootFreeOn H g →
    h.natDegree < generatorDegree →
    (∀ i ∈ S, q i ≠ 0) →
    (∀ i ∈ S, A i ≠ 0) →
    (∀ i ∈ S, HasCompleteFiber H (y i)) →
    (∀ i ∈ S, (X ^ blockSize - C (y i)) ∣ A i) →
    (∀ i ∈ S, A i = C (q i) * h + g * W i) →
    (∀ i ∈ S, C (q i) * V i = W i) →
    (∀ i ∈ S, (A i).natDegree = postCoreLocatorDegree) →
    (∀ i ∈ S, (W i).natDegree ≤ quotientDegreeCeiling) →
    (∀ i ∈ S, SplitsOver H (A i)) →
    Set.InjOn y (S : Set I) →
    OnAffineLine S V →
    S.card ≤ 5

end Rank16FixedCoreQuotientLineObstruction
end GrandeFinale
