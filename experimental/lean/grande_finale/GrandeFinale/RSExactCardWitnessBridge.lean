import GrandeFinale.FirstMatchWitnessBridge
import GrandeFinale.RSExactSupportUpper

/-!
# Finite exact-cardinality Reed--Solomon witness bridge

This module supplies a finite, literal `(slope, support, degree-<k explainer)`
catalogue for each received line.  "Exact" means that the chosen support has
cardinality exactly `a`; it does not mean that this support is the complete
agreement set of the explainer.  Semantic cells, their exhaustivity, their
budgets, and a uniform sum bound remain explicit hypotheses.
-/

open Polynomial
open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale.RSExactCardWitnessBridge

open GrandeFinale.CollisionAwarePole
open GrandeFinale.FirstMatchWitnessBridge
open GrandeFinale.RSExactSupportUpper

/-- A finite representation of `(gamma, S, h)` with `deg h < k`.
The coefficient vector is decoded by `explanation`. -/
structure RSExactCardWitness (D F : Type*) (k : Nat) where
  slope : F
  support : Finset D
  coeffs : Fin k -> F
deriving Fintype, DecidableEq

/-- The degree-`<k` polynomial encoded by a witness coefficient vector. -/
def RSExactCardWitness.explanation {D F : Type*} [Semiring F] {k : Nat}
    (w : RSExactCardWitness D F k) : F[X] :=
  ((Polynomial.degreeLTEquiv F k).symm w.coeffs : Polynomial.degreeLT F k)

theorem RSExactCardWitness.explanation_degree_lt
    {D F : Type*} [Semiring F] {k : Nat}
    (w : RSExactCardWitness D F k) :
    w.explanation.degree < (k : WithBot Nat) := by
  exact Polynomial.mem_degreeLT.mp
    ((Polynomial.degreeLTEquiv F k).symm w.coeffs).2

section Catalogue

variable {D F : Type*} [Field F] [Fintype F] [DecidableEq F]
variable [Fintype D] [DecidableEq D]

/-- A represented explainer agrees on an exact-`a` support and carries the
MCA non-pair condition.  Agreement outside the selected support is allowed. -/
def ValidRSExactCardWitness (ev : D -> F) (k a : Nat)
    (u0 u1 : D -> F) (w : RSExactCardWitness D F k) : Prop :=
  w.support.card = a ∧
    (∀ d ∈ w.support,
      w.explanation.eval (ev d) = u0 d + w.slope * u1 d) ∧
    ¬ GrandeFinale.ExplainedPair (rsEval ev k : Set (D -> F))
      u0 u1 w.support

/-- The finite catalogue of all exact-cardinality polynomial witnesses on one
received line. -/
noncomputable def rsExactCardWitnesses (ev : D -> F) (k a : Nat)
    (u0 u1 : D -> F) : Finset (RSExactCardWitness D F k) :=
  Finset.univ.filter (ValidRSExactCardWitness ev k a u0 u1)

omit [Fintype F] [DecidableEq F] [Fintype D] [DecidableEq D] in
/-- The explainer is unique given slope and support once the support contains
at least `k` evaluation points. -/
theorem explanation_eq_of_valid_of_slope_eq_support_eq
    (ev : D -> F) (hev : Function.Injective ev)
    (k a : Nat) (hka : k ≤ a) (u0 u1 : D -> F)
    {w w' : RSExactCardWitness D F k}
    (hw : ValidRSExactCardWitness ev k a u0 u1 w)
    (hw' : ValidRSExactCardWitness ev k a u0 u1 w')
    (hslope : w.slope = w'.slope)
    (hsupport : w.support = w'.support) :
    w.explanation = w'.explanation := by
  have hksupport : k ≤ w.support.card := by
    rw [hw.1]
    exact hka
  apply Polynomial.eq_of_degrees_lt_of_eval_index_eq
    (s := w.support) hev.injOn
  · exact w.explanation_degree_lt.trans_le
      (WithBot.coe_le_coe.mpr hksupport)
  · exact w'.explanation_degree_lt.trans_le
      (WithBot.coe_le_coe.mpr hksupport)
  · intro d hd
    have hd' : d ∈ w'.support := by
      rw [← hsupport]
      exact hd
    calc
      w.explanation.eval (ev d) = u0 d + w.slope * u1 d := hw.2.1 d hd
      _ = u0 d + w'.slope * u1 d := by rw [hslope]
      _ = w'.explanation.eval (ev d) := (hw'.2.1 d hd').symm

omit [Fintype F] [DecidableEq F] [Fintype D] [DecidableEq D] in
/-- Projection to `(slope, support)` is injective on valid exact-cardinality
witnesses; the polynomial field carries no hidden multiplicity. -/
theorem slope_support_projection_injOn_validRSExactCardWitness
    (ev : D -> F) (hev : Function.Injective ev)
    (k a : Nat) (hka : k ≤ a) (u0 u1 : D -> F) :
    Set.InjOn
      (fun w : RSExactCardWitness D F k => (w.slope, w.support))
      {w | ValidRSExactCardWitness ev k a u0 u1 w} := by
  intro w hw w' hw' hprojection
  have hslope : w.slope = w'.slope := congrArg Prod.fst hprojection
  have hsupport : w.support = w'.support := congrArg Prod.snd hprojection
  have hexplanation : w.explanation = w'.explanation :=
    explanation_eq_of_valid_of_slope_eq_support_eq
      ev hev k a hka u0 u1 hw hw' hslope hsupport
  have hcoeffs : w.coeffs = w'.coeffs := by
    apply (Polynomial.degreeLTEquiv F k).symm.injective
    apply Subtype.ext
    exact hexplanation
  cases w
  cases w'
  simp only at hslope hsupport hcoeffs
  cases hslope
  cases hsupport
  cases hcoeffs
  rfl

/-- Threshold-`a` bad slopes are exactly the slope image of the finite literal
witness catalogue. -/
theorem rsMcaBadSlopes_eq_exactCardWitnessSlopeImage
    (ev : D -> F) (hev : Function.Injective ev)
    (k a : Nat) (hka : k + 1 ≤ a) (u0 u1 : D -> F) :
    Finset.univ.filter (fun gamma : F =>
      GrandeFinale.MCABad (rsEval ev k : Set (D -> F)) u0 u1 a gamma) =
      (rsExactCardWitnesses ev k a u0 u1).image
        RSExactCardWitness.slope := by
  ext gamma
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]
  constructor
  · intro hbad
    obtain ⟨T, hTcard, hline, hpair⟩ :=
      mcaBad_has_exact_support ev hev k a hka u0 u1 gamma hbad
    obtain ⟨c, hc, hcT⟩ := hline
    obtain ⟨P, hPdeg, hcP⟩ := mem_rsEval.mp hc
    let pLT : Polynomial.degreeLT F k :=
      ⟨P, Polynomial.mem_degreeLT.mpr hPdeg⟩
    let w : RSExactCardWitness D F k :=
      ⟨gamma, T, Polynomial.degreeLTEquiv F k pLT⟩
    apply Finset.mem_image.mpr
    refine ⟨w, ?_, rfl⟩
    simp only [rsExactCardWitnesses, Finset.mem_filter,
      Finset.mem_univ, true_and]
    refine ⟨hTcard, ?_, hpair⟩
    intro d hd
    calc
      w.explanation.eval (ev d) = P.eval (ev d) := by
        simp [RSExactCardWitness.explanation, w, pLT]
      _ = c d := (hcP d).symm
      _ = u0 d + gamma * u1 d := hcT d hd
  · intro hgamma
    rcases Finset.mem_image.mp hgamma with ⟨w, hw, hsw⟩
    simp only [rsExactCardWitnesses, Finset.mem_filter,
      Finset.mem_univ, true_and] at hw
    rcases hw with ⟨hcard, hagree, hpair⟩
    subst gamma
    refine ⟨w.support, hcard.ge, ?_, hpair⟩
    refine ⟨fun d => w.explanation.eval (ev d), ?_, ?_⟩
    · exact mem_rsEval.mpr
        ⟨w.explanation, w.explanation_degree_lt, fun _ => rfl⟩
    · intro d hd
      exact hagree d hd

end Catalogue

section FirstMatchAdapter

variable {D F ι : Type*}
variable [Field F] [Fintype F] [DecidableEq F]
variable [Fintype D] [DecidableEq D] [LinearOrder ι]

/-- The generic witness-exhaustive first-match bridge specialized to the
finite exact-cardinality RS catalogue; the bad-slope image hypothesis is now a
theorem rather than a caller obligation. -/
theorem B_MCA_rsEval_le_sup_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets
    (ev : D -> F) (hev : Function.Injective ev)
    (k a : Nat) (hka : k + 1 ≤ a)
    (idx : ((D -> F) × (D -> F)) -> Finset ι)
    (cell : ((D -> F) × (D -> F)) -> ι ->
      Finset (RSExactCardWitness D F k))
    (U : ((D -> F) × (D -> F)) -> ι -> Nat)
    (hexhaust : ∀ p,
      (idx p).biUnion (cell p) = rsExactCardWitnesses ev k a p.1 p.2)
    (hcell : ∀ p i, i ∈ idx p ->
      (firstMatchSlopeCell (idx p) (cell p)
        RSExactCardWitness.slope i).card ≤ U p i) :
    GrandeFinale.B_MCA (rsEval ev k : Set (D -> F)) a ≤
      Finset.univ.sup (fun p : (D -> F) × (D -> F) =>
        ∑ i ∈ idx p, U p i) := by
  apply B_MCA_le_sup_of_witnessExhaustive_firstMatchSlopeBudgets
    (rsEval ev k : Set (D -> F)) a
    (fun p => rsExactCardWitnesses ev k a p.1 p.2)
    RSExactCardWitness.slope idx cell U
  · intro p
    exact rsMcaBadSlopes_eq_exactCardWitnessSlopeImage
      ev hev k a hka p.1 p.2
  · exact hexhaust
  · exact hcell

/-- A uniform bound on the line-dependent semantic-cell budget sums gives the
fixed-row Reed--Solomon MCA numerator bound. -/
theorem B_MCA_rsEval_le_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets
    (ev : D -> F) (hev : Function.Injective ev)
    (k a B : Nat) (hka : k + 1 ≤ a)
    (idx : ((D -> F) × (D -> F)) -> Finset ι)
    (cell : ((D -> F) × (D -> F)) -> ι ->
      Finset (RSExactCardWitness D F k))
    (U : ((D -> F) × (D -> F)) -> ι -> Nat)
    (hexhaust : ∀ p,
      (idx p).biUnion (cell p) = rsExactCardWitnesses ev k a p.1 p.2)
    (hcell : ∀ p i, i ∈ idx p ->
      (firstMatchSlopeCell (idx p) (cell p)
        RSExactCardWitness.slope i).card ≤ U p i)
    (hunif : ∀ p, ∑ i ∈ idx p, U p i ≤ B) :
    GrandeFinale.B_MCA (rsEval ev k : Set (D -> F)) a ≤ B := by
  apply B_MCA_le_of_witnessExhaustive_firstMatchSlopeBudgets
    (rsEval ev k : Set (D -> F)) a B
    (fun p => rsExactCardWitnesses ev k a p.1 p.2)
    RSExactCardWitness.slope idx cell U
  · intro p
    exact rsMcaBadSlopes_eq_exactCardWitnessSlopeImage
      ev hev k a hka p.1 p.2
  · exact hexhaust
  · exact hcell
  · exact hunif

end FirstMatchAdapter

#print axioms RSExactCardWitness.explanation_degree_lt
#print axioms explanation_eq_of_valid_of_slope_eq_support_eq
#print axioms slope_support_projection_injOn_validRSExactCardWitness
#print axioms rsMcaBadSlopes_eq_exactCardWitnessSlopeImage
#print axioms B_MCA_rsEval_le_sup_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets
#print axioms B_MCA_rsEval_le_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets

end GrandeFinale.RSExactCardWitnessBridge
