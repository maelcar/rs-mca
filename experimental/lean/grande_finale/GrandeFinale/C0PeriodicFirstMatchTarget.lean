import Mathlib

/-!
# Deployed monomial periodic first-match payment

This theorem kernel-checks the exact finite-ledger union conclusion of Danny's
PR #796 packet.  The four input finsets are the already classified, post-deletion
cells: q64 `f=29` and `f=28`, followed by q128 `b=5` and `b=7`.  Their
component caps and first-match cover remain explicit hypotheses; the
proof does not claim a complete `c=0` parent bound.
-/

namespace GrandeFinale

theorem c0_periodic_first_match_payment_target
    {alpha : Type*} [DecidableEq alpha]
    (bad q64f29 q64f28 q128b5 q128b7 : Finset alpha)
    (hcover : bad ⊆ q64f29 ∪ q64f28 ∪ q128b5 ∪ q128b7)
    (h29 : q64f29.card ≤ 1619679744)
    (h28 : q64f28.card ≤ 83970774720)
    (h5h7 : (q128b5 ∪ q128b7).card ≤ 16501819170137728) :
    bad.card ≤ 16501904760592192 := by
  have hcover' :
      bad ⊆ (q64f29 ∪ q64f28) ∪ (q128b5 ∪ q128b7) := by
    simpa only [Finset.union_assoc] using hcover
  have hbad := Finset.card_le_card hcover'
  have hleft :
      (q64f29 ∪ q64f28).card ≤ q64f29.card + q64f28.card :=
    Finset.card_union_le q64f29 q64f28
  have houter :
      ((q64f29 ∪ q64f28) ∪ (q128b5 ∪ q128b7)).card ≤
        (q64f29 ∪ q64f28).card + (q128b5 ∪ q128b7).card :=
    Finset.card_union_le (q64f29 ∪ q64f28) (q128b5 ∪ q128b7)
  omega

#print axioms c0_periodic_first_match_payment_target

end GrandeFinale
