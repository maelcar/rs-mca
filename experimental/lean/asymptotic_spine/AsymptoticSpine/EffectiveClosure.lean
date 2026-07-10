import AsymptoticSpine.ProfileEnvelope

namespace AsymptoticSpine

/-!
# Effective prefix fibers and the shallow-closure ray bridge

This stdlib-only module formalizes two exact finite statements used by
`experimental/asymptotic_rs_mca_frontiers.tex`:

1. the full depth-`w` locator-prefix class is an effective-syndrome fiber after
   the verified Newton/affine reindexing; a first-match or balanced-core
   residual is only a subfamily of that full class;
2. the support injection in `(SE2)` bounds distinct slopes by support mass, and
   the elementary `L ≤ A_eff` arithmetic turns that bound into the direct branch
   of `(RC)`, which can supply condition `(A6)`.

The field-specific Newton coordinate map, its affine translation by the based
syndrome, and the RS fact that one noncommon support carries at most one slope
are explicit certificate inputs.  The module does not claim those semantic
facts for arbitrary weighted/rational charts.  It also does not prove
`log A_eff = o(|T|)`, MI, MA, a profile-envelope comparison, or any unrestricted
deep-prefix/high-kappa statement.

All cardinalities use the package's established duplicate-free `List` model.
-/

/-! ## Full fibers, prefix charts, and the affine reindexing guard -/

/-- The fiber of `key` over `z`, restricted to the displayed finite slice. -/
def mapFiber {Item Key : Type} [DecidableEq Key]
    (slice : List Item) (key : Item → Key) (z : Key) : List Item :=
  slice.filter (fun x => decide (key x = z))

/-- A depth-labelled locator-prefix map.  The depth is recorded for source
correspondence; the combinatorial fiber theorem uses only the key map. -/
structure DepthPrefix (Support Raw : Type) where
  depth : Nat
  key : Support → Raw

/-- The exact interface between the effective syndrome coordinate and the raw
locator prefix on one full fixed-weight slice.

`toPrefix` includes both the triangular Newton change of coordinates and the
affine basepoint translation in `(EF2)`.  Injectivity is load-bearing: without
it, two distinct syndrome fibers could collapse to one prefix class. -/
structure PrefixFiberBridge (Support Eff Raw : Type) where
  fullSlice : List Support
  fullSlice_nodup : fullSlice.Nodup
  syndrome : Support → Eff
  rawPrefix : DepthPrefix Support Raw
  toPrefix : Eff → Raw
  toPrefix_injective : Function.Injective toPrefix
  compatible : ∀ x ∈ fullSlice, toPrefix (syndrome x) = rawPrefix.key x

/-- The effective-syndrome fiber `N_g(z)` on the full fixed-weight slice. -/
def PrefixFiberBridge.syndromeFiber {Support Eff Raw : Type}
    [DecidableEq Eff] (b : PrefixFiberBridge Support Eff Raw) (z : Eff) : List Support :=
  mapFiber b.fullSlice b.syndrome z

/-- The full raw depth-prefix class at key `ξ`.  This deliberately says
`PrefixChart`, not `BalancedCoreChart`: a routed balanced-core residual need not
equal the whole prefix class. -/
def PrefixFiberBridge.depthPrefixChart {Support Eff Raw : Type}
    [DecidableEq Raw] (b : PrefixFiberBridge Support Eff Raw) (ξ : Raw) : List Support :=
  mapFiber b.fullSlice b.rawPrefix.key ξ

/-- **Fiber = chart, with the required reindexing.**  The effective syndrome
fiber at `z` is exactly the full raw prefix class at `toPrefix z`. -/
theorem syndromeFiber_eq_depthPrefixChart {Support Eff Raw : Type}
    [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff) :
    b.syndromeFiber z = b.depthPrefixChart (b.toPrefix z) := by
  apply List.filter_congr
  intro x hx
  apply decide_eq_decide.mpr
  constructor
  · intro h
    calc b.rawPrefix.key x
        = b.toPrefix (b.syndrome x) := (b.compatible x hx).symm
      _ = b.toPrefix z := congrArg b.toPrefix h
  · intro h
    apply b.toPrefix_injective
    exact (b.compatible x hx).trans h

/-- Filtering a first-match residual preserves the syndrome-fiber inclusion. -/
theorem residualSyndromeFiber_sublist {Support Eff Raw : Type}
    [DecidableEq Eff]
    (b : PrefixFiberBridge Support Eff Raw) (residual : List Support)
    (hres : List.Sublist residual b.fullSlice) (z : Eff) :
    List.Sublist (mapFiber residual b.syndrome z) (b.syndromeFiber z) := by
  exact hres.filter (fun x => decide (b.syndrome x = z))

/-- **Residual monotonicity, exact cardinality form.**  Deleting supports cannot
make a fixed syndrome fiber larger. -/
theorem residualSyndromeFiber_length_le {Support Eff Raw : Type}
    [DecidableEq Eff]
    (b : PrefixFiberBridge Support Eff Raw) (residual : List Support)
    (hres : List.Sublist residual b.fullSlice) (z : Eff) :
    (mapFiber residual b.syndrome z).length ≤ (b.syndromeFiber z).length :=
  (residualSyndromeFiber_sublist b residual hres z).length_le

/-- Any routed chart explicitly certified as a subfamily of the full prefix
class has cardinality at most the corresponding full syndrome fiber. -/
theorem residualChart_length_le_syndromeFiber {Support Eff Raw : Type}
    [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff) (residualChart : List Support)
    (hchart : List.Sublist residualChart (b.depthPrefixChart (b.toPrefix z))) :
    residualChart.length ≤ (b.syndromeFiber z).length := by
  rw [syndromeFiber_eq_depthPrefixChart b z]
  exact hchart.length_le

/-- A full syndrome fiber is itself a sublist of the full slice. -/
theorem syndromeFiber_sublist_fullSlice {Support Eff Raw : Type}
    [DecidableEq Eff] (b : PrefixFiberBridge Support Eff Raw) (z : Eff) :
    List.Sublist (b.syndromeFiber z) b.fullSlice :=
  List.filter_sublist

/-- The full syndrome fiber is a genuine set enumeration when the full slice is. -/
theorem syndromeFiber_nodup {Support Eff Raw : Type}
    [DecidableEq Eff] (b : PrefixFiberBridge Support Eff Raw) (z : Eff) :
    (b.syndromeFiber z).Nodup :=
  (syndromeFiber_sublist_fullSlice b z).nodup b.fullSlice_nodup

/-- Hence every full syndrome fiber is bounded by the full-slice mass. -/
theorem syndromeFiber_length_le_fullSlice {Support Eff Raw : Type}
    [DecidableEq Eff] (b : PrefixFiberBridge Support Eff Raw) (z : Eff) :
    (b.syndromeFiber z).length ≤ b.fullSlice.length :=
  (syndromeFiber_sublist_fullSlice b z).length_le

/-! ## `(SE2)`: one distinct noncommon support per distinct slope -/

/-- A finite `(SE2)` certificate.

`supports` and `slopes` enumerate sets without repetition.  `supportOf` chooses
one noncommon exact-agreement support for every slope.  The chosen supports are
certified as a sublist of a suitable enumeration of the support projection; this
is the finite injection asserted by "one fixed noncommon support carries at most
one slope." -/
structure SE2Certificate (Support Slope : Type) where
  supports : List Support
  slopes : List Slope
  supportOf : Slope → Support
  supports_nodup : supports.Nodup
  slopes_nodup : slopes.Nodup
  chosen_sublist : List.Sublist (slopes.map supportOf) supports

/-- The chosen noncommon supports are duplicate-free. -/
theorem SE2Certificate.chosen_nodup {Support Slope : Type}
    (c : SE2Certificate Support Slope) :
    (c.slopes.map c.supportOf).Nodup :=
  c.chosen_sublist.nodup c.supports_nodup

/-- **`(SE2)` support injection.**  Distinct first-match slopes are bounded by
the cardinality of their support projection. -/
theorem se2_support_injection {Support Slope : Type}
    (c : SE2Certificate Support Slope) :
    c.slopes.length ≤ c.supports.length := by
  simpa using c.chosen_sublist.length_le

/-- The `(SE2)` support bound followed by any printed support budget. -/
theorem se2_to_paidBudget {Support Slope : Type}
    (c : SE2Certificate Support Slope) (paidBudget : Nat)
    (hpaid : c.supports.length ≤ paidBudget) :
    c.slopes.length ≤ paidBudget :=
  Nat.le_trans (se2_support_injection c) hpaid

/-- Combining `(SE2)` with the honest residual/full-fiber relation: a slope cell
supported inside a routed prefix chart is no larger than the corresponding full
syndrome fiber. -/
theorem se2_residualChart_le_syndromeFiber {Support Slope Eff Raw : Type}
    [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff)
    (c : SE2Certificate Support Slope)
    (hchart : List.Sublist c.supports (b.depthPrefixChart (b.toPrefix z))) :
    c.slopes.length ≤ (b.syndromeFiber z).length :=
  Nat.le_trans (se2_support_injection c)
    (residualChart_length_le_syndromeFiber b z c.supports hchart)

/-- End-to-end exact mass bound: a residual prefix-chart slope cell has at most
the number of supports in the ambient full slice. -/
theorem se2_residualChart_le_fullSlice {Support Slope Eff Raw : Type}
    [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff)
    (c : SE2Certificate Support Slope)
    (hchart : List.Sublist c.supports (b.depthPrefixChart (b.toPrefix z))) :
    c.slopes.length ≤ b.fullSlice.length :=
  Nat.le_trans (se2_residualChart_le_syndromeFiber b z c hchart)
    (syndromeFiber_length_le_fullSlice b z)

/-! ## Exact finite route from `(SE2)` to direct `(RC)` and `(A6)` -/

/-- The finite direct branch of `(RC)`: `bad ≤ loss * (1 + average)`.
`average` is any printed integral ceiling for the image-normalized profile
average `M/L`; `loss` is the printed finite substitute for `e^{o(n)}`. -/
def DirectRC (bad loss average : Nat) : Prop :=
  bad ≤ loss * (1 + average)

/-- **Closure `(SE2)` supplies direct `(RC)`.**  If `bad ≤ M`, the printed
average covers the mass (`M ≤ L*average`), the realized image satisfies `L ≤ A`,
and the loss covers the effective span (`A ≤ loss`), then the direct ray bound
holds.  This is the exact finite arithmetic behind the shallow-prefix routing. -/
theorem se2_to_directRC {bad mass imageSize effectiveSize average loss : Nat}
    (hSE2 : bad ≤ mass)
    (haverage : mass ≤ imageSize * average)
    (himage : imageSize ≤ effectiveSize)
    (hloss : effectiveSize ≤ loss) :
    DirectRC bad loss average := by
  unfold DirectRC
  calc bad
      ≤ mass := hSE2
    _ ≤ imageSize * average := haverage
    _ ≤ effectiveSize * average := Nat.mul_le_mul_right average himage
    _ ≤ loss * average := Nat.mul_le_mul_right average hloss
    _ ≤ loss * (1 + average) :=
      Nat.mul_le_mul (Nat.le_refl loss) (by omega)

/-- A compact bundle of the exact finite closure inputs.  The asymptotic statement
that `effectiveSize`/`loss` is subexponential is intentionally not encoded here. -/
structure LowBoundaryClosureBounds where
  slopeCount : Nat
  mass : Nat
  imageSize : Nat
  effectiveSize : Nat
  average : Nat
  loss : Nat
  se2 : slopeCount ≤ mass
  average_covers : mass ≤ imageSize * average
  image_le_effective : imageSize ≤ effectiveSize
  effective_le_loss : effectiveSize ≤ loss

/-- Bundled form of the direct `(RC)` conclusion. -/
theorem lowBoundaryClosure_to_directRC (b : LowBoundaryClosureBounds) :
    DirectRC b.slopeCount b.loss b.average :=
  se2_to_directRC b.se2 b.average_covers b.image_le_effective b.effective_le_loss

/-- The two alternatives in current admissibility condition `(A6)`: either the
profile satisfies `(RC)`, or it has a separately proved direct profile-budget
bound. -/
def A6RayCondition (rayCompiler directProfileBound : Prop) : Prop :=
  rayCompiler ∨ directProfileBound

/-- End-to-end exact shallow-closure route.  The support injection is proved
from `c`; the routed chart is bounded by its full reindexed syndrome fiber and
then by the full-slice mass; the printed image/effective/loss inequalities close
the direct branch of `(RC)`. -/
theorem prefixResidualClosure_to_directRC {Support Slope Eff Raw : Type}
    [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff)
    (c : SE2Certificate Support Slope)
    (hchart : List.Sublist c.supports (b.depthPrefixChart (b.toPrefix z)))
    (imageSize effectiveSize average loss : Nat)
    (haverage : b.fullSlice.length ≤ imageSize * average)
    (himage : imageSize ≤ effectiveSize)
    (hloss : effectiveSize ≤ loss) :
    DirectRC c.slopes.length loss average :=
  se2_to_directRC (se2_residualChart_le_fullSlice b z c hchart)
    haverage himage hloss

/-- The composed prefix/residual closure reaches current `(A6)` through its
`(RC)` disjunct.  The other disjunct remains an arbitrary separately proved
profile-envelope bound. -/
theorem prefixResidualClosure_to_A6_via_RC {Support Slope Eff Raw : Type}
    [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff)
    (c : SE2Certificate Support Slope)
    (hchart : List.Sublist c.supports (b.depthPrefixChart (b.toPrefix z)))
    (imageSize effectiveSize average loss : Nat)
    (haverage : b.fullSlice.length ≤ imageSize * average)
    (himage : imageSize ≤ effectiveSize)
    (hloss : effectiveSize ≤ loss) (directProfileBound : Prop) :
    A6RayCondition (DirectRC c.slopes.length loss average) directProfileBound :=
  Or.inl (prefixResidualClosure_to_directRC b z c hchart imageSize effectiveSize
    average loss haverage himage hloss)

/-- **Concrete downstream wiring.**  Build the integrated
`ProfileCompilerInputs` record with its `rayCompiler` field supplied by the
reindexed prefix-residual closure theorem.  Every other compiler obligation is
still an explicit argument; in particular this constructor does not assert
atlas coverage, Sidon payment, envelope dominance, or the target inequality. -/
theorem profileCompilerInputs_of_prefixResidualClosure
    {Support Slope Eff Raw : Type} [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff)
    (c : SE2Certificate Support Slope)
    (hchart : List.Sublist c.supports (b.depthPrefixChart (b.toPrefix z)))
    (imageSize effectiveSize average closureLoss : Nat)
    (haverage : b.fullSlice.length ≤ imageSize * average)
    (himage : imageSize ≤ effectiveSize)
    (hloss : effectiveSize ≤ closureLoss)
    (badUpper nonprimitive nonprimitiveBudget sidonBudget profileEnvelope
      compilerLoss identityLoss identityBudget target : Nat)
    (hclosed : badUpper ≤ nonprimitive + c.slopes.length)
    (hnatural : nonprimitive ≤ compilerLoss * nonprimitiveBudget)
    (hclosurePaid : closureLoss * (1 + average) ≤ compilerLoss * sidonBudget)
    (henvelope : nonprimitiveBudget + sidonBudget ≤ profileEnvelope)
    (hidentity : profileEnvelope ≤ identityLoss * identityBudget)
    (htarget : (compilerLoss * identityLoss) * identityBudget ≤ target) :
    ProfileCompilerInputs badUpper nonprimitive c.slopes.length
      (closureLoss * (1 + average)) nonprimitiveBudget sidonBudget
      profileEnvelope compilerLoss identityLoss identityBudget target where
  closedLedger := hclosed
  naturalProfilePayment := hnatural
  sidonPayment := hclosurePaid
  rayCompiler := prefixResidualClosure_to_directRC b z c hchart imageSize
    effectiveSize average closureLoss haverage himage hloss
  profileEnvelopeBudget := henvelope
  identityDominance := hidentity
  targetBudget := htarget

/-- The existing profile-envelope compiler can consume the closure-supplied ray
field without an additional ray hypothesis. -/
theorem profileCompilerUpper_of_prefixResidualClosure
    {Support Slope Eff Raw : Type} [DecidableEq Eff] [DecidableEq Raw]
    (b : PrefixFiberBridge Support Eff Raw) (z : Eff)
    (c : SE2Certificate Support Slope)
    (hchart : List.Sublist c.supports (b.depthPrefixChart (b.toPrefix z)))
    (imageSize effectiveSize average closureLoss : Nat)
    (haverage : b.fullSlice.length ≤ imageSize * average)
    (himage : imageSize ≤ effectiveSize) (hloss : effectiveSize ≤ closureLoss)
    (badUpper nonprimitive nonprimitiveBudget sidonBudget profileEnvelope
      compilerLoss identityLoss identityBudget target : Nat)
    (hclosed : badUpper ≤ nonprimitive + c.slopes.length)
    (hnatural : nonprimitive ≤ compilerLoss * nonprimitiveBudget)
    (hclosurePaid : closureLoss * (1 + average) ≤ compilerLoss * sidonBudget)
    (henvelope : nonprimitiveBudget + sidonBudget ≤ profileEnvelope)
    (hidentity : profileEnvelope ≤ identityLoss * identityBudget)
    (htarget : (compilerLoss * identityLoss) * identityBudget ≤ target) :
    badUpper ≤ target :=
  profile_compiler_upper badUpper nonprimitive c.slopes.length
    (closureLoss * (1 + average)) nonprimitiveBudget sidonBudget profileEnvelope
    compilerLoss identityLoss identityBudget target
    (profileCompilerInputs_of_prefixResidualClosure b z c hchart imageSize
      effectiveSize average closureLoss haverage himage hloss badUpper
      nonprimitive nonprimitiveBudget sidonBudget profileEnvelope compilerLoss
      identityLoss identityBudget target hclosed hnatural hclosurePaid henvelope
      hidentity htarget)

/-- The shallow closure reaches `(A6)` through its `(RC)` disjunct. -/
theorem lowBoundaryClosure_to_A6_via_RC (b : LowBoundaryClosureBounds)
    (directProfileBound : Prop) :
    A6RayCondition (DirectRC b.slopeCount b.loss b.average) directProfileBound :=
  Or.inl (lowBoundaryClosure_to_directRC b)

/-- Alternatively, a printed support budget supplies `(A6)`'s separate direct
profile-bound disjunct.  This theorem is distinct from the `(RC)` route above. -/
theorem se2_to_A6_directProfile {Support Slope : Type}
    (c : SE2Certificate Support Slope) (rayCompiler : Prop) (paidBudget : Nat)
    (hpaid : c.supports.length ≤ paidBudget) :
    A6RayCondition rayCompiler (c.slopes.length ≤ paidBudget) :=
  Or.inr (se2_to_paidBudget c paidBudget hpaid)

/-! ## Small exact smoke tests -/

def affineToyBridge : PrefixFiberBridge Nat Nat Nat where
  fullSlice := [0, 1, 2, 3, 4]
  fullSlice_nodup := by decide
  syndrome := fun x => x % 2
  rawPrefix := { depth := 1, key := fun x => 10 + x % 2 }
  toPrefix := fun z => 10 + z
  toPrefix_injective := by intro a b h; exact Nat.add_left_cancel h
  compatible := by intro x hx; rfl

/-- The odd syndrome fiber `[1,3]` is the raw prefix chart at translated key `11`. -/
theorem affineToy_fiber_eq_chart :
    affineToyBridge.syndromeFiber 1 = affineToyBridge.depthPrefixChart 11 := by
  decide

def se2Toy : SE2Certificate Nat Nat where
  supports := [10, 11, 12]
  slopes := [2, 4]
  supportOf := fun z => if z = 2 then 10 else 12
  supports_nodup := by decide
  slopes_nodup := by decide
  chosen_sublist := by decide

/-- The toy certificate records two distinct slopes charged to three supports. -/
theorem se2Toy_exact : se2Toy.slopes.length ≤ se2Toy.supports.length :=
  se2_support_injection se2Toy

/-- Exact arithmetic smoke test for the direct `(RC)` bridge. -/
theorem directRC_toy : DirectRC 2 4 2 :=
  se2_to_directRC (bad := 2) (mass := 3) (imageSize := 2)
    (effectiveSize := 4) (average := 2) (loss := 4)
    (by omega) (by omega) (by omega) (by omega)

#print axioms syndromeFiber_eq_depthPrefixChart
#print axioms residualSyndromeFiber_sublist
#print axioms residualSyndromeFiber_length_le
#print axioms residualChart_length_le_syndromeFiber
#print axioms syndromeFiber_sublist_fullSlice
#print axioms syndromeFiber_nodup
#print axioms syndromeFiber_length_le_fullSlice
#print axioms SE2Certificate.chosen_nodup
#print axioms se2_support_injection
#print axioms se2_to_paidBudget
#print axioms se2_residualChart_le_syndromeFiber
#print axioms se2_residualChart_le_fullSlice
#print axioms se2_to_directRC
#print axioms lowBoundaryClosure_to_directRC
#print axioms prefixResidualClosure_to_directRC
#print axioms prefixResidualClosure_to_A6_via_RC
#print axioms profileCompilerInputs_of_prefixResidualClosure
#print axioms profileCompilerUpper_of_prefixResidualClosure
#print axioms lowBoundaryClosure_to_A6_via_RC
#print axioms se2_to_A6_directProfile
#print axioms affineToy_fiber_eq_chart
#print axioms se2Toy_exact
#print axioms directRC_toy

end AsymptoticSpine
