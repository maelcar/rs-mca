import Std
import Std.Tactic

namespace RouteDF17GlobalMarkedContactPivotNoGoV1

theorem analog_target_pin : 2 * 17 = 34 := by native_decide

theorem typed_representative_defect_mass_exceeds_target :
    2 * 17 < 16 + 463 := by native_decide

theorem literal_full_defect_support_exceeds_target :
    2 * 17 < 407 := by native_decide

theorem nonempty_contact_support_exceeds_target :
    2 * 17 < 103 := by native_decide

theorem profile_pivot_labels_retain_multiplicity :
    30 < 103 ∧ 9 > 1 := by native_decide

theorem no_profile_pivot_cardinality_certificate
    (claimedInjectionCardinality : 103 ≤ 2 * 17) : False := by
  omega

theorem target_from_global_cardinality_owner
    (generated primitive t p : Nat)
    (owner : generated + primitive ≤ t * p) :
    generated + primitive ≤ t * p := owner

theorem actual_all_minors_owner_adapter {allMaximalMinorsVanish rankDrop : Prop}
    (adapter : allMaximalMinorsVanish ↔ rankDrop) :
    allMaximalMinorsVanish → rankDrop := adapter.mp

theorem one_nonzero_pivot_blocks_all_vanishing {Index Field : Type}
    [Zero Field] (minor : Index → Field) (pivot : Index)
    (nonzero : minor pivot ≠ 0) :
    ¬ (∀ index, minor index = 0) := by
  intro allZero
  exact nonzero (allZero pivot)

theorem f17_filter_partition_pin :
    13 + 20 + 0 + 4 + 0 + 463 = 500 := by native_decide

theorem f17_contact_partition_pin :
    348 + 115 = 463 := by native_decide

theorem f17_contact_support_profile_pin :
    46 + 57 = 103 := by native_decide

end RouteDF17GlobalMarkedContactPivotNoGoV1
