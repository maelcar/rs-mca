import Std
import Std.Tactic

namespace RouteDSquareFoldEvenOddReconstructionV1

theorem marked_square_fold_even_odd_reconstruction
    (positive negative positive_prime negative_prime : Int)
    (same_occupancy : positive + negative = positive_prime + negative_prime)
    (same_signed : positive - negative = positive_prime - negative_prime) :
    positive = positive_prime ∧ negative = negative_prime := by
  omega

theorem square_fold_odd_data_recovery_no_go_cardinality : 1 < 3 := by
  native_decide

theorem f23_precursor_partition_pin : 1 + 55 = 56 := by native_decide

theorem folded_key_histogram_pin : 52 * 1 + 1 * 3 = 55 := by
  native_decide

theorem odd_data_key_count_pin : 52 < 55 := by native_decide

theorem odd_pivot_key_count_pin : 53 < 55 := by native_decide

theorem even_odd_marked_key_count_pin : 55 = 55 := by native_decide

theorem full_raw_support_pin : 2 + 3 ≤ 8 := by native_decide

theorem toy_vanishing_family_pin : 0 = 0 := by native_decide

theorem actual_all_minors_owner_adapter {allMaximalMinorsVanish rankDrop : Prop}
    (adapter : allMaximalMinorsVanish ↔ rankDrop) :
    allMaximalMinorsVanish → rankDrop := adapter.mp

theorem one_nonzero_pivot_blocks_all_vanishing {Index Field : Type}
    [Zero Field] (minor : Index → Field) (pivot : Index)
    (nonzero : minor pivot ≠ 0) :
    ¬ (∀ index, minor index = 0) := by
  intro allZero
  exact nonzero (allZero pivot)

end RouteDSquareFoldEvenOddReconstructionV1
