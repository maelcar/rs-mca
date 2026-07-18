import Std
import Std.Tactic

/-!
# Route-D Rule-2 WSP algebraic preflight v1

This standalone module exposes only correctly typed bridge interfaces:

* a left inverse makes an algebraic support transfer injective;
* preservation of a carried common-core mark is explicit;
* exact support transfer does not by itself provide a numerical payment;
* an upper bound of ten extension candidates among ninety-one emissions gives
  at least eighty-one nonextension candidates.

The exhaustive `F_31` enumeration belongs to the deterministic Python
verifier.  Lean kernel-checks the count arithmetic, source-orientation pins,
and the three auxiliary extension fixtures.

Exact provenance:

* source commit `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`;
* shipment commit `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`;
* top-seam note blob `dda538a9a36cd0c8e267c11600a49cdc5bf054d1`;
* top-seam verifier blob `dc4a7235b3274fbcc5ef0ed8bd8c96620b04a5a1`;
* barrier-map note blob `ea896eca8bf89038b76469e51b6dd70eb83d3c02`;
* barrier-map JSON blob `4d3d068cf80cd5912c998d86411e8baf33ece156`;
* barrier-map verifier blob `2243a8c987d0493cb5f48f52b6174f735312e54a`;
* rank-owner note blob `ddfce00907f34128b324a64041f4e0ec8957b7d3`;
* rank-owner verifier blob `1702842190da45806e5a52e932aa4b8dab951ffe`;
* shipment note/verifier/Lean blobs
  `f24ce928df7e7170c1b4f3228d5fe9b184be50b4`,
  `ace3e859b917ae87eeffb8c0e7c37155520e311e`, and
  `78e46c6ab97d97191c567041f81a6ca05e76cf41`.
-/

namespace RouteDRule2WspAlgebraicPreflightV1

def sourceCommit : String := "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
def shipmentCommit : String := "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0"
def topseamNoteBlob : String := "dda538a9a36cd0c8e267c11600a49cdc5bf054d1"
def topseamVerifierBlob : String := "dc4a7235b3274fbcc5ef0ed8bd8c96620b04a5a1"
def barrierNoteBlob : String := "ea896eca8bf89038b76469e51b6dd70eb83d3c02"
def barrierJsonBlob : String := "4d3d068cf80cd5912c998d86411e8baf33ece156"
def barrierVerifierBlob : String := "2243a8c987d0493cb5f48f52b6174f735312e54a"
def rankOwnerNoteBlob : String := "ddfce00907f34128b324a64041f4e0ec8957b7d3"
def rankOwnerVerifierBlob : String := "1702842190da45806e5a52e932aa4b8dab951ffe"
def shipmentNoteBlob : String := "f24ce928df7e7170c1b4f3228d5fe9b184be50b4"
def shipmentVerifierBlob : String := "ace3e859b917ae87eeffb8c0e7c37155520e311e"
def shipmentLeanBlob : String := "78e46c6ab97d97191c567041f81a6ca05e76cf41"

theorem exact_source_pins :
    sourceCommit = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e" ∧
    shipmentCommit = "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0" ∧
    topseamNoteBlob = "dda538a9a36cd0c8e267c11600a49cdc5bf054d1" ∧
    topseamVerifierBlob = "dc4a7235b3274fbcc5ef0ed8bd8c96620b04a5a1" ∧
    barrierNoteBlob = "ea896eca8bf89038b76469e51b6dd70eb83d3c02" ∧
    barrierJsonBlob = "4d3d068cf80cd5912c998d86411e8baf33ece156" ∧
    barrierVerifierBlob = "2243a8c987d0493cb5f48f52b6174f735312e54a" ∧
    rankOwnerNoteBlob = "ddfce00907f34128b324a64041f4e0ec8957b7d3" ∧
    rankOwnerVerifierBlob = "1702842190da45806e5a52e932aa4b8dab951ffe" ∧
    shipmentNoteBlob = "f24ce928df7e7170c1b4f3228d5fe9b184be50b4" ∧
    shipmentVerifierBlob = "ace3e859b917ae87eeffb8c0e7c37155520e311e" ∧
    shipmentLeanBlob = "78e46c6ab97d97191c567041f81a6ca05e76cf41" := by
  native_decide

/-! ## Correct bridge interfaces -/

structure MarkedPacket (Core Side Cell : Type) where
  core : Core
  removed : Side
  added : Side
  cell : Cell

/-- A recoverable algebraic emission is injective.  This is the exact logical
content of support cost one; no accepting owner or numerical bound occurs in
the statement. -/
theorem recoverable_emission_injective
    {Packet Certificate : Type}
    (emit : Packet → Certificate) (recover : Certificate → Packet)
    (leftInverse : ∀ packet, recover (emit packet) = packet) :
    ∀ ⦃left right⦄, emit left = emit right → left = right := by
  intro left right equality
  calc
    left = recover (emit left) := (leftInverse left).symm
    _ = recover (emit right) := congrArg recover equality
    _ = right := leftInverse right

/-- The mark-preservation hypothesis is returned explicitly; an algebraic
recovery theorem may not silently forget the common core. -/
theorem recoverable_emission_carries_core
    {Core Side Cell Certificate : Type}
    (emit : MarkedPacket Core Side Cell → Certificate)
    (coreOf : Certificate → Core)
    (preserves : ∀ packet, coreOf (emit packet) = packet.core)
    (packet : MarkedPacket Core Side Cell) :
    coreOf (emit packet) = packet.core := by
  exact preserves packet

def NumericallyPaid {Certificate : Type}
    (accepts : Certificate → Prop) (certificate : Certificate) : Prop :=
  accepts certificate

/-- Exact recovery and numerical payment remain separate inputs.  The theorem
only concludes payment after an accepting-owner hypothesis is supplied. -/
theorem payment_requires_acceptance
    {Packet Certificate : Type}
    (emit : Packet → Certificate) (recover : Certificate → Packet)
    (accepts : Certificate → Prop) (packet : Packet)
    (_leftInverse : ∀ value, recover (emit value) = value)
    (accepted : accepts (emit packet)) :
    NumericallyPaid accepts (emit packet) := by
  exact accepted

/-- The order-invariant arithmetic bridge used by the finite preflight. -/
theorem any_choice_has_at_least_81_candidates
    (emitted extensionCandidates nonextensionCandidates : Nat)
    (emittedCount : emitted = 91)
    (extensionBound : extensionCandidates ≤ 10)
    (partition : extensionCandidates + nonextensionCandidates = emitted) :
    81 ≤ nonextensionCandidates := by
  omega

/-! ## Exact finite pins -/

def cellSizeHistogram : List (Nat × Nat) :=
  [(1, 1), (2, 4), (3, 5), (4, 8), (5, 3), (6, 4), (7, 1), (8, 1), (9, 1)]

def histogramCells : Nat :=
  cellSizeHistogram.foldl (fun total pair => total + pair.2) 0

def histogramPackets : Nat :=
  cellSizeHistogram.foldl (fun total pair => total + pair.1 * pair.2) 0

def histogramEmissions : Nat :=
  cellSizeHistogram.foldl (fun total pair => total + (pair.1 - 1) * pair.2) 0

theorem f31_count_arithmetic_pin :
    histogramCells = 28 ∧
    histogramPackets = 119 ∧
    histogramEmissions = 91 ∧
    28 ≤ 30 ∧
    91 = 6 + 85 ∧
    91 = 3 + 88 ∧
    484 = 32 + 452 ∧
    91 - 10 = 81 ∧
    91 - 1 = 90 ∧
    32 + 40 + 19 = 91 ∧
    32 + 35 + 18 = 85 ∧
    40 + 30 + 21 = 91 := by
  native_decide

def sumPowMod (p degree : Nat) (values : List Nat) : Nat :=
  values.foldl (fun total value => (total + value ^ degree) % p) 0

def cubicLocatorConstant (p : Nat) (values : List Nat) : Nat :=
  (p - values.foldl (fun product value => (product * value) % p) 1) % p

def cellLabel (p : Nat) (removed added : List Nat) : Nat :=
  (cubicLocatorConstant p added + p - cubicLocatorConstant p removed) % p

def signedMoment (p degree : Nat) (positive negative : List Nat) : Nat :=
  (sumPowMod p degree positive + p - sumPowMod p degree negative) % p

def rule2Moment
    (p degree : Nat) (removed0 added0 removed added : List Nat) : Nat :=
  let positive := added0 ++ removed
  let negative := removed0 ++ added
  signedMoment p degree positive negative

def r0c5 : List Nat := [5, 11, 19]
def a0c5 : List Nat := [15, 24, 27]
def rc5 : List Nat := [12, 26, 28]
def ac5 : List Nat := [6, 14, 15]

def r0c26 : List Nat := [4, 7, 26]
def a0c26 : List Nat := [16, 22, 30]
def rc26 : List Nat := [5, 12, 20]
def ac26 : List Nat := [15, 23, 30]

def r0c28 : List Nat := [5, 7, 11]
def a0c28 : List Nat := [13, 14, 27]
def rc28 : List Nat := [7, 19, 28]
def ac28 : List Nat := [8, 17, 29]

theorem source_orientation_and_auxiliary_extension_pins :
    cellLabel 31 r0c5 a0c5 = 5 ∧
    cellLabel 31 rc5 ac5 = 5 ∧
    cellLabel 31 r0c26 a0c26 = 26 ∧
    cellLabel 31 rc26 ac26 = 26 ∧
    cellLabel 31 r0c28 a0c28 = 28 ∧
    cellLabel 31 rc28 ac28 = 28 ∧
    (cellLabel 31 r0c5 a0c5 +
      signedMoment 31 3 a0c5 r0c5 * 21) % 31 = 0 ∧
    (cellLabel 31 r0c26 a0c26 +
      signedMoment 31 3 a0c26 r0c26 * 21) % 31 = 0 ∧
    (cellLabel 31 r0c28 a0c28 +
      signedMoment 31 3 a0c28 r0c28 * 21) % 31 = 0 ∧
    rule2Moment 31 4 r0c5 a0c5 rc5 ac5 = 0 ∧
    rule2Moment 31 4 r0c26 a0c26 rc26 ac26 = 0 ∧
    rule2Moment 31 4 r0c28 a0c28 rc28 ac28 = 0 := by
  native_decide

end RouteDRule2WspAlgebraicPreflightV1
