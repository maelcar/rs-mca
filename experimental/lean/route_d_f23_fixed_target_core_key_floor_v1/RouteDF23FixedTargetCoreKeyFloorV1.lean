import Std
import Std.Tactic

namespace RouteDF23FixedTargetCoreKeyFloorV1

theorem packet_count_pin : 75 = 75 := by native_decide

theorem exact_gcd_partition_pin : 56 + 5 + 5 + 4 + 4 = 74 := by
  native_decide

theorem extension_partition_pin : 1 + 55 = 56 := by native_decide

theorem support_histogram_pin : 1 + 5 + 21 + 28 = 55 := by
  native_decide

theorem contact_profile_histogram_pin : 43 + 6 + 6 = 55 := by
  native_decide

theorem complete_bases_exceed_field : 23 < 55 := by native_decide

theorem complete_bases_exceed_profile_times_field : 2 * 23 < 55 := by
  native_decide

theorem no_complete_base_cardinality_certificate
    (claimedInjectionCardinality : 55 ≤ 2 * 23) : False := by
  omega

theorem fixed_literal_core_one_scalar_cap
    (packetCount fieldCard : Nat)
    (constantTermInjection : packetCount ≤ fieldCard) :
    packetCount ≤ fieldCard := constantTermInjection

theorem global_addback_from_complete_owner
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

end RouteDF23FixedTargetCoreKeyFloorV1
