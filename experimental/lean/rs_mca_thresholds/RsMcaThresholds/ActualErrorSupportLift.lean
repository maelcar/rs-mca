import RsMcaThresholds.ExactSparsification

/-!
# Actual-error-support full-agreement lift

This module formalizes the support lift in the section `Lift to the deep
agreement` of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at source snapshot
`168e9ba0`.

Starting from an explicit explaining codeword and support-wise
noncontainment, the actual error support determines the full agreement set.
An error-support cap `|E| ≤ r` then makes the same slope MCA-bad at agreement
`|D| - r`.

The source prints `|D| - (t - 1) = |D| - t + 1`.  For natural-number
subtraction this needs both `0 < t` and `t ≤ |D|`.  The reusable theorem stays
at `|D| - r`; the source-facing wrapper derives both side conditions from the
exact-witness hypotheses.

Only this witness lift is proved.  The module consumes the actual-error cap;
it proves no exact-support reduction, rank-to-support bridge, identification
of an abstract moment matrix with the source matrix, RIM/Route-D adapter,
pivot/tangent/cyclotomic equivalence, deep-MCA count, owner charge, branch
closure, or KoalaBear row claim.

Field finiteness, Reed--Solomon structure, and an embedding of the coordinate
type into the field are unused by this support-only step, so they are not
assumed.
-/

open scoped Classical

noncomputable section

namespace RsMcaThresholds.ActualErrorSupportLift

set_option autoImplicit false

universe u v

variable {F : Type u} {D : Type v}
variable [Field F] [Fintype D] [DecidableEq D]

local notation "Word" => D → F

open ExactSparsification

/-- The source's full agreement set `S* = D \ E`, represented on the finite
domain type by the complement of the existing `wordSupport` definition.

Source: `Lift to the deep agreement` in
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
def fullAgreementSupport (f₀ f₁ c : Word) (γ : F) : Finset D :=
  Finset.univ \ wordSupport ((fun x => f₀ x + γ * f₁ x) - c)

/-- Membership in the full agreement support is exactly agreement with the
supplied explaining codeword.

Source: the definition `S* = D \ E` and the sentence following it in
`Lift to the deep agreement` of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem mem_fullAgreementSupport_iff
    (f₀ f₁ c : Word) (γ : F) (x : D) :
    x ∈ fullAgreementSupport f₀ f₁ c γ ↔
      c x = f₀ x + γ * f₁ x := by
  simp [fullAgreementSupport, wordSupport, sub_eq_zero, eq_comm]

/-- The full agreement set has cardinality `|D| - |E|`.

Source: the displayed identity `|S*| = n - |E|` in
`Lift to the deep agreement` of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem fullAgreementSupport_card
    (f₀ f₁ c : Word) (γ : F) :
    (fullAgreementSupport f₀ f₁ c γ).card =
      Fintype.card D -
        (wordSupport ((fun x => f₀ x + γ * f₁ x) - c)).card := by
  rw [fullAgreementSupport, Finset.card_sdiff]
  simp

/-- An explicit support witness lifts to the source's full agreement support.
The conclusion records the original-support inclusion, the `|D| - r` size
bound, explanation by the same codeword, and upward persistence of
noncontainment.

The source specializes `C` to a Reed--Solomon code.  No linear or
Reed--Solomon property is used by this support step, so the statement is
explicitly exported for an arbitrary code set.

Source: `Exact support and actual error support` and
`Lift to the deep agreement` in
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`;
the actual-error cap is equation (3). -/
theorem fullAgreementSupport_witness
    (C : Set Word) (f₀ f₁ c : Word) (γ : F) (S : Finset D) (r : ℕ)
    (hc : c ∈ C)
    (hagree : ∀ x ∈ S, c x = f₀ x + γ * f₁ x)
    (hnoncontained : ¬ GrandeFinale.ExplainedPair C f₀ f₁ S)
    (herror :
      (wordSupport ((fun x => f₀ x + γ * f₁ x) - c)).card ≤ r) :
    S ⊆ fullAgreementSupport f₀ f₁ c γ ∧
      Fintype.card D - r ≤ (fullAgreementSupport f₀ f₁ c γ).card ∧
      GrandeFinale.Explained C (fun x => f₀ x + γ * f₁ x)
        (fullAgreementSupport f₀ f₁ c γ) ∧
      ¬ GrandeFinale.ExplainedPair C f₀ f₁
        (fullAgreementSupport f₀ f₁ c γ) := by
  have hS : S ⊆ fullAgreementSupport f₀ f₁ c γ := by
    intro x hx
    exact (mem_fullAgreementSupport_iff f₀ f₁ c γ x).2 (hagree x hx)
  have hcard :
      Fintype.card D - r ≤ (fullAgreementSupport f₀ f₁ c γ).card := by
    rw [fullAgreementSupport_card]
    omega
  have hexplained :
      GrandeFinale.Explained C (fun x => f₀ x + γ * f₁ x)
        (fullAgreementSupport f₀ f₁ c γ) := by
    refine ⟨c, hc, ?_⟩
    intro x hx
    exact (mem_fullAgreementSupport_iff f₀ f₁ c γ x).1 hx
  have hnot :
      ¬ GrandeFinale.ExplainedPair C f₀ f₁
        (fullAgreementSupport f₀ f₁ c γ) := by
    intro hpair
    apply hnoncontained
    rcases hpair with ⟨c₀, hc₀, c₁, hc₁, h₀, h₁⟩
    exact ⟨c₀, hc₀, c₁, hc₁,
      fun x hx => h₀ x (hS hx), fun x hx => h₁ x (hS hx)⟩
  exact ⟨hS, hcard, hexplained, hnot⟩

/-- The consumer-facing core: an explicit support witness whose actual error
support has size at most `r` is MCA-bad at agreement `|D| - r`.

No hypothesis `r ≤ |D|` is needed; truncated natural subtraction is already
the correct all-`r` statement.

Source: the MCA-bad conclusion in `Lift to the deep agreement` of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`,
before the specialization `r = t - 1`. -/
theorem mcaBad_lift_of_wordSupport_card_le
    (C : Set Word) (f₀ f₁ c : Word) (γ : F) (S : Finset D) (r : ℕ)
    (hc : c ∈ C)
    (hagree : ∀ x ∈ S, c x = f₀ x + γ * f₁ x)
    (hnoncontained : ¬ GrandeFinale.ExplainedPair C f₀ f₁ S)
    (herror :
      (wordSupport ((fun x => f₀ x + γ * f₁ x) - c)).card ≤ r) :
    GrandeFinale.MCABad C f₀ f₁ (Fintype.card D - r) γ := by
  obtain ⟨_, hcard, hexplained, hnot⟩ :=
    fullAgreementSupport_witness C f₀ f₁ c γ S r hc hagree
      hnoncontained herror
  exact ⟨fullAgreementSupport f₀ f₁ c γ, hcard, hexplained, hnot⟩

/-- The explicitly repaired natural-subtraction identity used by the source.
Both hypotheses are necessary: it can fail at `t = 0` and at `t > n`.

Source: the printed equality `n - (t - 1) = n - t + 1` in
`Lift to the deep agreement` of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem nat_sub_pred_eq_sub_add_one
    (n t : ℕ) (ht : 0 < t) (htn : t ≤ n) :
    n - (t - 1) = n - t + 1 := by
  omega

/-- Source-facing exact-witness wrapper at rank depth `t = A - k`.

The source hypotheses `|S| = A`, `k + 1 ≤ A`, and `t = A - k` derive
`0 < t` and `t ≤ |D|`; hence the repaired endpoint is `|D| - t + 1`.
The domain set `D` is represented by the finite domain type, so `S ⊆ D` is
implicit in `S : Finset D`.

Source: `Exact support and actual error support`, equation (3), and
`Lift to the deep agreement` in
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`. -/
theorem rankDepth_mcaBad_lift_of_wordSupport_card_le
    (C : Set Word) (f₀ f₁ c : Word) (γ : F) (S : Finset D)
    (A k t : ℕ)
    (hScard : S.card = A)
    (hkA : k + 1 ≤ A)
    (ht : t = A - k)
    (hc : c ∈ C)
    (hagree : ∀ x ∈ S, c x = f₀ x + γ * f₁ x)
    (hnoncontained : ¬ GrandeFinale.ExplainedPair C f₀ f₁ S)
    (herror :
      (wordSupport ((fun x => f₀ x + γ * f₁ x) - c)).card ≤ t - 1) :
    GrandeFinale.MCABad C f₀ f₁ (Fintype.card D - t + 1) γ := by
  have htpos : 0 < t := by omega
  have hAcard : A ≤ Fintype.card D := by
    calc
      A = S.card := hScard.symm
      _ ≤ Finset.univ.card := Finset.card_le_card (Finset.subset_univ S)
      _ = Fintype.card D := Finset.card_univ
  have htcard : t ≤ Fintype.card D := by omega
  have hcore := mcaBad_lift_of_wordSupport_card_le C f₀ f₁ c γ S
    (t - 1) hc hagree hnoncontained herror
  rw [nat_sub_pred_eq_sub_add_one (Fintype.card D) t htpos htcard] at hcore
  exact hcore

end RsMcaThresholds.ActualErrorSupportLift
