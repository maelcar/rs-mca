import GrandeFinale

/-!
# Finite Q correspondence tables

This module records the four finite tables printed in
`prop:q-exact-target` and `prop:q-moment-order-floor` of
`experimental/grande_finale.tex`.

The exact integer fields (`w`, average-fiber ceilings, budgets, and truncated
budget ratios) are checked by machine-evaluated `native_decide` arithmetic.
The bit margins and moment-order floors are correspondence data from the
audited real-average calculation: this module pins their values and the
real-average versus ceiling-average convention split, but does not claim to
formalize the transcendental logarithm or the enormous binomial evaluation
that produced them.

In particular, these tables do not prove the row-sharp Q atom, a finite upper
ledger, or any deployed adjacent safe row.
-/

namespace GrandeFinale.QFiniteTables

/-- The four active finite rows in the order used by the manuscript tables. -/
inductive RowName
  | koalaBearMCA
  | koalaBearList
  | mersenne31MCA
  | mersenne31List
  deriving DecidableEq, Repr

/-- Audited finite-Q data for one active row. -/
structure Row where
  name : RowName
  base : ℕ
  width : ℕ
  averageCeil : ℕ
  budget : ℕ
  /-- `⌊10^4 * budget / averageCeil⌋`. -/
  ratioFloorTenThousand : ℕ
  /-- The real-average bit margin, recorded to twelve decimal places. -/
  marginPicobits : ℕ
  /-- The manuscript's four-decimal rendering of the bit margin. -/
  printedMarginTenThousand : ℕ
  /-- `prop:q-moment-order-floor`, using the real-average convention. -/
  momentOrderFloor : ℕ
  /-- The comparison value obtained from the ceiling-average convention. -/
  ceilingAverageMomentOrderFloor : ℕ
  deriving DecidableEq, Repr

/-- The four rows of `prop:q-exact-target` / `prop:q-moment-order-floor`. -/
def rows : List Row :=
  [ { name := .koalaBearMCA
      base := Certificates.pKB
      width := 67471
      averageCeil := 57198030366
      budget := Certificates.BstarKB
      ratioFloorTenThousand := 48075209295
      marginPicobits := 22196861707683
      printedMarginTenThousand := 221969
      momentOrderFloor := 94196
      ceilingAverageMomentOrderFloor := 94196 }
  , { name := .koalaBearList
      base := Certificates.pKB
      width := 67471
      averageCeil := 65065153468
      budget := Certificates.BstarKB
      ratioFloorTenThousand := 42262365253
      marginPicobits := 22010942080645
      printedMarginTenThousand := 220109
      momentOrderFloor := 94991
      ceilingAverageMomentOrderFloor := 94991 }
  , { name := .mersenne31MCA
      base := Certificates.pM31
      width := 67447
      averageCeil := 1752700
      budget := Certificates.BstarM31
      ratioFloorTenThousand := 95722
      marginPicobits := 3258852879362
      printedMarginTenThousand := 32589
      momentOrderFloor := 641593
      ceilingAverageMomentOrderFloor := 641594 }
  , { name := .mersenne31List
      base := Certificates.pM31
      width := 67447
      averageCeil := 1993678
      budget := Certificates.BstarM31
      ratioFloorTenThousand := 84152
      marginPicobits := 3072999568105
      printedMarginTenThousand := 30730
      momentOrderFloor := 680397
      ceilingAverageMomentOrderFloor := 680397 } ]

/-- All four rows occur exactly once and in manuscript order. -/
theorem row_names : rows.map (fun row => row.name) =
    [ .koalaBearMCA, .koalaBearList, .mersenne31MCA, .mersenne31List ] := by
  native_decide

/-- Exact base-field assignment for the four rows. -/
theorem base_fields : rows.map (fun row => row.base) =
    [ 2130706433, 2130706433, 2147483647, 2147483647 ] := by
  native_decide

/-- Exact `(w, ceil average, B*)` inputs of `prop:q-exact-target`. -/
theorem exact_target_inputs : rows.map (fun row =>
    (row.width, row.averageCeil, row.budget)) =
    [ (67471, 57198030366, 274980728111395087)
    , (67471, 65065153468, 274980728111395087)
    , (67447, 1752700, 16777215)
    , (67447, 1993678, 16777215) ] := by
  native_decide

/-- The four displayed average-fiber ceilings fit below their full budgets. -/
theorem average_ceil_le_budget :
    ∀ row ∈ rows, row.averageCeil ≤ row.budget := by
  native_decide

/-- Exact four-decimal truncations of `B* / ceil(average)` in
`prop:q-exact-target`; this is integer arithmetic, not a floating check. -/
theorem exact_ratio_truncations :
    ∀ row ∈ rows,
      row.budget * 10000 / row.averageCeil = row.ratioFloorTenThousand := by
  native_decide

/-- The twelve-decimal audit values round to the four decimals printed in the
manuscript.  This checks the recorded decimal correspondence, not `Real.log`. -/
theorem printed_margin_rounding :
    ∀ row ∈ rows,
      (row.marginPicobits + 50000000) / 100000000 =
        row.printedMarginTenThousand := by
  native_decide

/-- The real-average moment-order floor table in
`prop:q-moment-order-floor`. -/
theorem moment_order_floors : rows.map (fun row => row.momentOrderFloor) =
    [ 94196, 94991, 641593, 680397 ] := by
  native_decide

/-- The ceiling-average comparison table.  Only the Mersenne-31 MCA row is
convention-sensitive, where the ceiling-average value is one larger. -/
theorem ceiling_average_moment_order_floors :
    rows.map (fun row => row.ceilingAverageMomentOrderFloor) =
      [ 94196, 94991, 641594, 680397 ] := by
  native_decide

theorem convention_sensitive_rows :
    (rows.filter fun row =>
      row.momentOrderFloor != row.ceilingAverageMomentOrderFloor).map
        (fun row => row.name) = [ .mersenne31MCA ] := by
  native_decide

end GrandeFinale.QFiniteTables
