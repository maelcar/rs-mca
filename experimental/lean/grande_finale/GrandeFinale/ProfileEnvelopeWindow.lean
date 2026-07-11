import Mathlib

/-!
# Exact finite-family profile-envelope windows

This module formalizes the rational exponent comparison between the identity
profile and a finite family of complete-fiber foldings.  Its scope is only the
exponent algebra: it does not establish the ledger hypotheses A2/A4 or the
asymptotic bridge from exponent dominance to an envelope estimate.
-/

namespace GrandeFinale.ProfileEnvelopeWindow

/-! ## Exact algebra for one folding -/

/-- Exponent of the identity contribution. -/
def identityExponent (h s : ℚ) : ℚ := max 0 (h - s)

/-- Exponent of a single degree-`c`, field-ratio-`lambda` folding. -/
def foldingExponent (h s c lambda : ℚ) : ℚ := (h - lambda * s) / c

/-- Lower endpoint coefficient of the closed identity-dominance window. -/
def kappaLow (c lambda : ℚ) : ℚ := (c - 1) / (c - lambda)

/-- Upper endpoint coefficient of the closed identity-dominance window. -/
def kappaHigh (lambda : ℚ) : ℚ := 1 / lambda

/-- The identity exponent dominates one folding exponent. -/
def Dominates (h s c lambda : ℚ) : Prop :=
  foldingExponent h s c lambda ≤ identityExponent h s

/-- The open interval on which one folding strictly exceeds the identity exponent. -/
def FailureBand (h s c lambda : ℚ) : Prop :=
  kappaLow c lambda * h < s ∧ s < kappaHigh lambda * h

private theorem folding_le_linear_iff
    (h s c lambda : ℚ) (hc : 0 < c) (hclambda : 0 < c - lambda) :
    foldingExponent h s c lambda ≤ h - s ↔
      s ≤ kappaLow c lambda * h := by
  have hshape : kappaLow c lambda * h = ((c - 1) * h) / (c - lambda) := by
    simp only [kappaLow]
    ring
  rw [hshape]
  constructor
  · intro hfold
    have hcleared : h - lambda * s ≤ (h - s) * c :=
      (div_le_iff₀ hc).mp hfold
    apply (le_div_iff₀ hclambda).2
    nlinarith
  · intro hlow
    have hcleared : s * (c - lambda) ≤ (c - 1) * h :=
      (le_div_iff₀ hclambda).mp hlow
    apply (div_le_iff₀ hc).2
    nlinarith

private theorem folding_le_zero_iff
    (h s c lambda : ℚ) (hc : 0 < c) (hlambda : 0 < lambda) :
    foldingExponent h s c lambda ≤ 0 ↔ kappaHigh lambda * h ≤ s := by
  have hshape : kappaHigh lambda * h = h / lambda := by
    simp only [kappaHigh]
    ring
  rw [hshape]
  constructor
  · intro hfold
    have hcleared : h - lambda * s ≤ 0 := by
      have := (div_le_iff₀ hc).mp hfold
      simpa using this
    apply (div_le_iff₀ hlambda).2
    nlinarith
  · intro hhigh
    have hcleared : h ≤ s * lambda := (div_le_iff₀ hlambda).mp hhigh
    apply (div_le_iff₀ hc).2
    nlinarith

/--
Exact closed single-folding window under the standard profile hypotheses.
Equality at either endpoint is identity-dominant.
-/
theorem dominates_iff_windows
    (h s c lambda : ℚ) (_hh : 0 ≤ h) (hc : 2 ≤ c)
    (hlambda0 : 0 < lambda) (hlambda1 : lambda ≤ 1) :
    Dominates h s c lambda ↔
      s ≤ kappaLow c lambda * h ∨ kappaHigh lambda * h ≤ s := by
  have hc0 : 0 < c := by linarith
  have hclambda : 0 < c - lambda := by linarith
  constructor
  · intro hdom
    rcases le_total s h with hsh | hhs
    · left
      apply (folding_le_linear_iff h s c lambda hc0 hclambda).1
      simpa [Dominates, identityExponent, max_eq_right (sub_nonneg.mpr hsh)] using hdom
    · right
      apply (folding_le_zero_iff h s c lambda hc0 hlambda0).1
      simpa [Dominates, identityExponent, max_eq_left (sub_nonpos.mpr hhs)] using hdom
  · rintro (hlow | hhigh)
    · have hfold : foldingExponent h s c lambda ≤ h - s :=
        (folding_le_linear_iff h s c lambda hc0 hclambda).2 hlow
      exact hfold.trans (le_max_right 0 (h - s))
    · have hfold : foldingExponent h s c lambda ≤ 0 :=
        (folding_le_zero_iff h s c lambda hc0 hlambda0).2 hhigh
      exact hfold.trans (le_max_left 0 (h - s))

/-- Strict exponent excess is equivalent to membership in the open failure band. -/
theorem identity_lt_folding_iff_failureBand
    (h s c lambda : ℚ) (hh : 0 ≤ h) (hc : 2 ≤ c)
    (hlambda0 : 0 < lambda) (hlambda1 : lambda ≤ 1) :
    identityExponent h s < foldingExponent h s c lambda ↔
      FailureBand h s c lambda := by
  have hdom := not_congr
    (dominates_iff_windows h s c lambda hh hc hlambda0 hlambda1)
  simpa only [Dominates, FailureBand, not_le, not_or] using hdom

/-- At the zero-target crossing `s = h`, the exponent excess has this exact value. -/
theorem zeroTarget_excess_eq (h c lambda : ℚ) :
    foldingExponent h h c lambda - identityExponent h h =
      ((1 - lambda) / c) * h := by
  simp [foldingExponent, identityExponent]
  ring

/--
For positive entropy and a proper field drop, the zero-target crossing lies
strictly inside the failure band.
-/
theorem zeroTarget_mem_failureBand
    (h c lambda : ℚ) (hh : 0 < h) (hc : 2 ≤ c)
    (hlambda0 : 0 < lambda) (hlambda1 : lambda < 1) :
    FailureBand h h c lambda := by
  apply (identity_lt_folding_iff_failureBand h h c lambda (le_of_lt hh) hc
    hlambda0 (le_of_lt hlambda1)).1
  simp only [identityExponent, foldingExponent, sub_self, max_self]
  apply div_pos
  · nlinarith
  · linarith

/-! ## Concrete foldings and finite rows -/

/-- A complete-fiber folding with natural degree and rational field ratio. -/
structure CompleteFiberFolding where
  degree : ℕ
  fieldRatio : ℚ
  deriving DecidableEq

/-- The exponent contributed by a concrete complete-fiber folding. -/
def CompleteFiberFolding.exponent
    (f : CompleteFiberFolding) (h s : ℚ) : ℚ :=
  foldingExponent h s f.degree f.fieldRatio

/-- The identity exponent dominates this concrete folding. -/
def CompleteFiberFolding.IdentityDominant
    (f : CompleteFiberFolding) (h s : ℚ) : Prop :=
  f.exponent h s ≤ identityExponent h s

/-- Lower endpoint of this folding's closed safe window. -/
def CompleteFiberFolding.lowerEndpoint
    (f : CompleteFiberFolding) (h : ℚ) : ℚ :=
  kappaLow f.degree f.fieldRatio * h

/-- Upper endpoint of this folding's closed safe window. -/
def CompleteFiberFolding.upperEndpoint
    (f : CompleteFiberFolding) (h : ℚ) : ℚ :=
  kappaHigh f.fieldRatio * h

/-- The per-folding closed safe-window predicate. -/
def CompleteFiberFolding.InWindow
    (f : CompleteFiberFolding) (h s : ℚ) : Prop :=
  s ≤ f.lowerEndpoint h ∨ f.upperEndpoint h ≤ s

/-- The per-folding strict open failure-band predicate. -/
def CompleteFiberFolding.InFailureBand
    (f : CompleteFiberFolding) (h s : ℚ) : Prop :=
  f.lowerEndpoint h < s ∧ s < f.upperEndpoint h

/-- Exact closed-window theorem for a concrete complete-fiber folding. -/
theorem CompleteFiberFolding.identityDominant_iff_inWindow
    (f : CompleteFiberFolding) (h s : ℚ)
    (hh : 0 ≤ h) (hdegree : 2 ≤ f.degree)
    (hratio0 : 0 < f.fieldRatio) (hratio1 : f.fieldRatio ≤ 1) :
    f.IdentityDominant h s ↔ f.InWindow h s := by
  exact dominates_iff_windows h s f.degree f.fieldRatio hh
    (by exact_mod_cast hdegree) hratio0 hratio1

/-- Strict exponent excess for a concrete folding is exactly its open failure band. -/
theorem CompleteFiberFolding.identity_lt_exponent_iff_inFailureBand
    (f : CompleteFiberFolding) (h s : ℚ)
    (hh : 0 ≤ h) (hdegree : 2 ≤ f.degree)
    (hratio0 : 0 < f.fieldRatio) (hratio1 : f.fieldRatio ≤ 1) :
    identityExponent h s < f.exponent h s ↔ f.InFailureBand h s := by
  exact identity_lt_folding_iff_failureBand h s f.degree f.fieldRatio hh
    (by exact_mod_cast hdegree) hratio0 hratio1

/-- Closed-window membership is the complement of strict failure-band membership. -/
theorem CompleteFiberFolding.inWindow_iff_not_inFailureBand
    (f : CompleteFiberFolding) (h s : ℚ) :
    f.InWindow h s ↔ ¬ f.InFailureBand h s := by
  simp only [CompleteFiberFolding.InWindow, CompleteFiberFolding.InFailureBand,
    not_and_or, not_lt]

/-- Exponent-level identity dominance for every folding carried by a row. -/
def profileIdentityDominant
    (row : Finset CompleteFiberFolding) (h s : ℚ) : Prop :=
  ∀ f ∈ row, f.IdentityDominant h s

/-- Every folding carried by a row passes its own closed-window test. -/
def inEveryFoldingWindow
    (row : Finset CompleteFiberFolding) (h s : ℚ) : Prop :=
  ∀ f ∈ row, f.InWindow h s

/--
Exponent-level row dominance is exactly the intersection of the per-folding
closed windows. This theorem does not prove A2/A4 or an asymptotic envelope bridge.
-/
theorem profileIdentityDominant_iff_forall_folding
    (row : Finset CompleteFiberFolding) (h s : ℚ)
    (hh : 0 ≤ h)
    (hdegree : ∀ f ∈ row, 2 ≤ f.degree)
    (hratio0 : ∀ f ∈ row, 0 < f.fieldRatio)
    (hratio1 : ∀ f ∈ row, f.fieldRatio ≤ 1) :
    profileIdentityDominant row h s ↔ inEveryFoldingWindow row h s := by
  constructor
  · intro hdom f hf
    exact (f.identityDominant_iff_inWindow h s hh (hdegree f hf)
      (hratio0 f hf) (hratio1 f hf)).1 (hdom f hf)
  · intro hwindow f hf
    exact (f.identityDominant_iff_inWindow h s hh (hdegree f hf)
      (hratio0 f hf) (hratio1 f hf)).2 (hwindow f hf)

/-- The union of all strict failure bands carried by a finite row. -/
def failureBandUnion (row : Finset CompleteFiberFolding) (h : ℚ) : Set ℚ :=
  ⋃ f ∈ row, Set.Ioo (f.lowerEndpoint h) (f.upperEndpoint h)

/-- Membership in the row's failure union means failure for an actual row folding. -/
theorem mem_failureBandUnion_iff
    (row : Finset CompleteFiberFolding) (h s : ℚ) :
    s ∈ failureBandUnion row h ↔ ∃ f ∈ row, f.InFailureBand h s := by
  simp only [failureBandUnion, Set.mem_iUnion, Set.mem_Ioo,
    CompleteFiberFolding.InFailureBand, CompleteFiberFolding.lowerEndpoint,
    CompleteFiberFolding.upperEndpoint]
  aesop

/-- Every folding window holds exactly when the crossing avoids the failure union. -/
theorem inEveryFoldingWindow_iff_avoidsFailureBandUnion
    (row : Finset CompleteFiberFolding) (h s : ℚ) :
    inEveryFoldingWindow row h s ↔ s ∉ failureBandUnion row h := by
  constructor
  · intro hwindow hmem
    rcases (mem_failureBandUnion_iff row h s).1 hmem with ⟨f, hf, hfail⟩
    exact (f.inWindow_iff_not_inFailureBand h s).1 (hwindow f hf) hfail
  · intro havoid f hf
    apply (f.inWindow_iff_not_inFailureBand h s).2
    intro hfail
    exact havoid ((mem_failureBandUnion_iff row h s).2 ⟨f, hf, hfail⟩)

/--
Exponent-level identity dominance is equivalent to avoiding the union of all
strict folding-failure bands. This theorem does not prove A2/A4 or the
asymptotic envelope bridge.
-/
theorem profileIdentityDominant_iff_avoidsFailureBandUnion
    (row : Finset CompleteFiberFolding) (h s : ℚ)
    (hh : 0 ≤ h)
    (hdegree : ∀ f ∈ row, 2 ≤ f.degree)
    (hratio0 : ∀ f ∈ row, 0 < f.fieldRatio)
    (hratio1 : ∀ f ∈ row, f.fieldRatio ≤ 1) :
    profileIdentityDominant row h s ↔ s ∉ failureBandUnion row h := by
  rw [profileIdentityDominant_iff_forall_folding row h s hh hdegree hratio0 hratio1,
    inEveryFoldingWindow_iff_avoidsFailureBandUnion]

/-- A field-ratio-one folding is identity-dominant for every crossing. -/
theorem CompleteFiberFolding.identityDominant_of_fieldRatio_eq_one
    (f : CompleteFiberFolding) (h s : ℚ)
    (hh : 0 ≤ h) (_hs : 0 ≤ s) (hdegree : 2 ≤ f.degree)
    (hratio : f.fieldRatio = 1) :
    f.IdentityDominant h s := by
  rw [CompleteFiberFolding.IdentityDominant, CompleteFiberFolding.exponent, hratio]
  exact (dominates_iff_windows h s f.degree 1 hh (by exact_mod_cast hdegree)
    (by norm_num) (by norm_num)).2 (by
      simp [kappaLow, kappaHigh, show (f.degree : ℚ) - 1 ≠ 0 by
        have : (2 : ℚ) ≤ f.degree := by exact_mod_cast hdegree
        linarith]
      exact le_total s h)

/--
If every folding has field ratio one, then the entire finite row is globally
identity-dominant under the stated profile hypotheses.
-/
theorem profileIdentityDominant_of_all_fieldRatio_eq_one
    (row : Finset CompleteFiberFolding) (h s : ℚ)
    (hh : 0 ≤ h) (hs : 0 ≤ s)
    (hdegree : ∀ f ∈ row, 2 ≤ f.degree)
    (hratio : ∀ f ∈ row, f.fieldRatio = 1) :
    profileIdentityDominant row h s := by
  intro f hf
  exact f.identityDominant_of_fieldRatio_eq_one h s hh hs
    (hdegree f hf) (hratio f hf)

/-- Exact zero-target excess for a concrete folding. -/
theorem CompleteFiberFolding.zeroTarget_excess_eq
    (f : CompleteFiberFolding) (h : ℚ) :
    f.exponent h h - identityExponent h h =
      ((1 - f.fieldRatio) / f.degree) * h := by
  exact GrandeFinale.ProfileEnvelopeWindow.zeroTarget_excess_eq
    h f.degree f.fieldRatio

/-- A proper field-drop folding places a positive crossing in its strict failure band. -/
theorem CompleteFiberFolding.zeroTarget_mem_inFailureBand
    (f : CompleteFiberFolding) (h : ℚ)
    (hh : 0 < h) (hdegree : 2 ≤ f.degree)
    (hratio0 : 0 < f.fieldRatio) (hratio1 : f.fieldRatio < 1) :
    f.InFailureBand h h := by
  exact zeroTarget_mem_failureBand h f.degree f.fieldRatio hh
    (by exact_mod_cast hdegree) hratio0 hratio1

/--
At a positive zero-target crossing, a valid finite row is identity-dominant
exactly when every carried folding has field ratio one.
-/
theorem profileIdentityDominant_at_zeroTarget_iff_all_fieldRatio_eq_one
    (row : Finset CompleteFiberFolding) (h : ℚ)
    (hh : 0 < h)
    (hdegree : ∀ f ∈ row, 2 ≤ f.degree)
    (hratio0 : ∀ f ∈ row, 0 < f.fieldRatio)
    (hratio1 : ∀ f ∈ row, f.fieldRatio ≤ 1) :
    profileIdentityDominant row h h ↔
      ∀ f ∈ row, f.fieldRatio = 1 := by
  constructor
  · intro hdom f hf
    apply le_antisymm (hratio1 f hf)
    by_contra hnot
    have hlt : f.fieldRatio < 1 := lt_of_not_ge hnot
    have hfail : f.InFailureBand h h :=
      f.zeroTarget_mem_inFailureBand h hh (hdegree f hf) (hratio0 f hf) hlt
    have hexcess : identityExponent h h < f.exponent h h :=
      (f.identity_lt_exponent_iff_inFailureBand h h (le_of_lt hh)
        (hdegree f hf) (hratio0 f hf) (hratio1 f hf)).2 hfail
    exact (not_lt_of_ge (hdom f hf)) hexcess
  · intro hratio
    exact profileIdentityDominant_of_all_fieldRatio_eq_one row h h
      (le_of_lt hh) (le_of_lt hh) hdegree hratio

#print axioms dominates_iff_windows
#print axioms identity_lt_folding_iff_failureBand
#print axioms profileIdentityDominant_iff_avoidsFailureBandUnion
#print axioms profileIdentityDominant_of_all_fieldRatio_eq_one
#print axioms CompleteFiberFolding.zeroTarget_mem_inFailureBand
#print axioms profileIdentityDominant_at_zeroTarget_iff_all_fieldRatio_eq_one

end GrandeFinale.ProfileEnvelopeWindow
