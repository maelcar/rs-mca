import GrandeFinale.C0PeriodicFirstMatchTarget
import GrandeFinale.FirstMatchAddBack

/-!
# Periodic `q = 128` singleton certificates

This module formalizes the two-odd-moment singleton packing step used by the
deployed monomial `c = 0` first-match packet.  It proves that a fixed first and
third moment admits at most `34,137` antipodal-free five-subsets, and at most
`12,598,400` antipodal-free seven-subsets, of a 128-point ambient set.

The final compiler combines those exact numerical singleton caps with supplied
local fixed-singleton cell caps.  The local Hahn bounds and the assertion that the
deployed cells furnish the required covers remain explicit certificate inputs;
no complete `c = 0` parent bound is claimed.
-/

open scoped BigOperators

namespace GrandeFinale.C0PeriodicSingletonCertificate

private theorem disjointUniformFamily_packing
    {D : Type*} [DecidableEq (Finset D)]
    (idx : Finset (Finset D)) (V : ℕ) (univ : Finset (Finset D))
    (ball : Finset D → Finset (Finset D))
    (hsub : ∀ M ∈ idx, ball M ⊆ univ)
    (hsize : ∀ M ∈ idx, (ball M).card = V)
    (hdisj : (idx : Set (Finset D)).PairwiseDisjoint ball) :
    idx.card * V ≤ univ.card := by
  have hunion : (idx.biUnion ball).card ≤ univ.card :=
    Finset.card_le_card (Finset.biUnion_subset.mpr hsub)
  convert hunion using 1
  rw [Finset.card_biUnion hdisj, Finset.sum_congr rfl hsize,
    Finset.sum_const, smul_eq_mul, mul_comm]

/-- A finite set contains no pair `x, -x`.  In particular it does not contain
zero. -/
def AntipodalFree {F : Type*} [Neg F] [DecidableEq F] (U : Finset F) : Prop :=
  ∀ x ∈ U, -x ∉ U

private theorem twoPoint_cubic_identity
    {F : Type*} [CommRing F] [DecidableEq F]
    (A : Finset F) (hA : A.card = 2) :
    3 * (∑ x ∈ A, x) * (∏ x ∈ A, x) =
      (∑ x ∈ A, x) ^ 3 - ∑ x ∈ A, x ^ 3 := by
  obtain ⟨x, y, hxy, rfl⟩ := Finset.card_eq_two.mp hA
  simp [hxy]
  ring

private theorem twoPoint_sum_ne_zero
    {F : Type*} [AddCommGroup F] [DecidableEq F]
    (A : Finset F) (hA : A.card = 2) (hfree : AntipodalFree A) :
    (∑ x ∈ A, x) ≠ 0 := by
  obtain ⟨x, y, hxy, rfl⟩ := Finset.card_eq_two.mp hA
  intro hsum
  have hsum' : x + y = 0 := by simpa [hxy] using hsum
  have hy : y = -x := by
    rw [eq_neg_iff_add_eq_zero]
    simpa [add_comm] using hsum'
  exact hfree x (by simp) (by simp [hy])

private theorem twoPoint_eq_of_sum_prod
    {F : Type*} [Field F] [DecidableEq F]
    (A B : Finset F) (hA : A.card = 2) (hB : B.card = 2)
    (hsum : (∑ x ∈ A, x) = ∑ x ∈ B, x)
    (hprod : (∏ x ∈ A, x) = ∏ x ∈ B, x) :
    A = B := by
  obtain ⟨x, y, hxy, rfl⟩ := Finset.card_eq_two.mp hA
  obtain ⟨u, v, huv, rfl⟩ := Finset.card_eq_two.mp hB
  have hsum' : x + y = u + v := by simpa [hxy, huv] using hsum
  have hprod' : x * y = u * v := by simpa [hxy, huv] using hprod
  have hxroot : (x - u) * (x - v) = 0 := by
    calc
      (x - u) * (x - v) = x ^ 2 - x * (u + v) + u * v := by ring
      _ = x ^ 2 - x * (x + y) + x * y := by rw [← hsum', ← hprod']
      _ = 0 := by ring
  rcases mul_eq_zero.mp hxroot with hxu | hxv
  · have hxu' : x = u := sub_eq_zero.mp hxu
    subst u
    have hyv : y = v := add_left_cancel hsum'
    subst v
    rfl
  · have hxv' : x = v := sub_eq_zero.mp hxv
    subst v
    have hyu : y = u := by
      apply add_right_cancel (b := x)
      calc
        y + x = x + y := add_comm _ _
        _ = u + x := hsum'
    subst u
    ext z
    simp [or_comm]

private theorem twoPoint_eq_of_moments
    {F : Type*} [Field F] [DecidableEq F]
    (hthree : (3 : F) ≠ 0)
    (A B : Finset F) (hA : A.card = 2) (hB : B.card = 2)
    (hfree : AntipodalFree A)
    (hsum : (∑ x ∈ A, x) = ∑ x ∈ B, x)
    (hcube : (∑ x ∈ A, x ^ 3) = ∑ x ∈ B, x ^ 3) :
    A = B := by
  have hsum0 := twoPoint_sum_ne_zero A hA hfree
  have hcoef : (3 : F) * (∑ x ∈ A, x) ≠ 0 := mul_ne_zero hthree hsum0
  have hprod : (∏ x ∈ A, x) = ∏ x ∈ B, x := by
    apply mul_left_cancel₀ hcoef
    calc
      ((3 : F) * ∑ x ∈ A, x) * ∏ x ∈ A, x =
          (∑ x ∈ A, x) ^ 3 - ∑ x ∈ A, x ^ 3 := by
            simpa [mul_assoc] using twoPoint_cubic_identity A hA
      _ = (∑ x ∈ B, x) ^ 3 - ∑ x ∈ B, x ^ 3 := by rw [hsum, hcube]
      _ = ((3 : F) * ∑ x ∈ B, x) * ∏ x ∈ B, x := by
            simpa [mul_assoc] using (twoPoint_cubic_identity B hB).symm
      _ = ((3 : F) * ∑ x ∈ A, x) * ∏ x ∈ B, x := by rw [hsum]
  exact twoPoint_eq_of_sum_prod A B hA hB hsum hprod

/-- A common `(b - 2)`-subset determines an antipodal-free `b`-subset from
its first and third moments. -/
theorem eq_of_common_omittedPair_certificate
    {F : Type*} [Field F] [DecidableEq F]
    (hthree : (3 : F) ≠ 0)
    (b : ℕ) (hb : 2 ≤ b) (U V W : Finset F)
    (hUcard : U.card = b) (hVcard : V.card = b)
    (hWcard : W.card = b - 2)
    (hWU : W ⊆ U) (hWV : W ⊆ V)
    (hfree : AntipodalFree U)
    (hsum : (∑ x ∈ U, x) = ∑ x ∈ V, x)
    (hcube : (∑ x ∈ U, x ^ 3) = ∑ x ∈ V, x ^ 3) :
    U = V := by
  have hUdiffCard : (U \ W).card = 2 := by
    rw [Finset.card_sdiff_of_subset hWU, hUcard, hWcard]
    omega
  have hVdiffCard : (V \ W).card = 2 := by
    rw [Finset.card_sdiff_of_subset hWV, hVcard, hWcard]
    omega
  have hdiffFree : AntipodalFree (U \ W) := by
    intro x hx hneg
    exact hfree x (Finset.mem_sdiff.mp hx).1 (Finset.mem_sdiff.mp hneg).1
  have hdiffSum : (∑ x ∈ U \ W, x) = ∑ x ∈ V \ W, x := by
    rw [← Finset.sum_sdiff hWU, ← Finset.sum_sdiff hWV] at hsum
    exact add_right_cancel hsum
  have hdiffCube : (∑ x ∈ U \ W, x ^ 3) = ∑ x ∈ V \ W, x ^ 3 := by
    rw [← Finset.sum_sdiff hWU, ← Finset.sum_sdiff hWV] at hcube
    exact add_right_cancel hcube
  have hdiff := twoPoint_eq_of_moments hthree
    (U \ W) (V \ W) hUdiffCard hVdiffCard hdiffFree hdiffSum hdiffCube
  calc
    U = (U \ W) ∪ W := (Finset.sdiff_union_of_subset hWU).symm
    _ = (V \ W) ∪ W := by rw [hdiff]
    _ = V := Finset.sdiff_union_of_subset hWV

/-! ## Fixed-moment singleton families -/

/-- The exact interface supplied by one fixed absolute-scalar cell: every
member is an antipodal-free `b`-subset of `ambient`, and all members have the
same first and third moments. -/
structure SingletonMomentFiber
    (F : Type*) [Field F] [DecidableEq F]
    (ambient : Finset F) (b : ℕ) where
  members : Finset (Finset F)
  firstMoment : F
  thirdMoment : F
  member_subset : ∀ U ∈ members, U ⊆ ambient
  member_card : ∀ U ∈ members, U.card = b
  antipodalFree : ∀ U ∈ members, AntipodalFree U
  first_moment : ∀ U ∈ members, (∑ x ∈ U, x) = firstMoment
  third_moment : ∀ U ∈ members, (∑ x ∈ U, x ^ 3) = thirdMoment

theorem SingletonMomentFiber.certificates_pairwiseDisjoint
    {F : Type*} [Field F] [DecidableEq F]
    {ambient : Finset F} {b : ℕ}
    (fiber : SingletonMomentFiber F ambient b)
    (hthree : (3 : F) ≠ 0) (hb : 2 ≤ b) :
    (fiber.members : Set (Finset F)).PairwiseDisjoint
      (fun U ↦ U.powersetCard (b - 2)) := by
  intro U hU V hV hUV
  change Disjoint (U.powersetCard (b - 2)) (V.powersetCard (b - 2))
  rw [Finset.disjoint_left]
  intro W hWU hWV
  apply hUV
  exact eq_of_common_omittedPair_certificate hthree b hb U V W
    (fiber.member_card U hU) (fiber.member_card V hV)
    (Finset.mem_powersetCard.mp hWU).2
    (Finset.mem_powersetCard.mp hWU).1
    (Finset.mem_powersetCard.mp hWV).1
    (fiber.antipodalFree U hU)
    (by rw [fiber.first_moment U hU, fiber.first_moment V hV])
    (by rw [fiber.third_moment U hU, fiber.third_moment V hV])

/-- Disjoint omitted-pair certificates pack inside all `(b - 2)`-subsets of
the ambient set. -/
theorem SingletonMomentFiber.card_mul_choose_le
    {F : Type*} [Field F] [DecidableEq F]
    {ambient : Finset F} {b : ℕ}
    (fiber : SingletonMomentFiber F ambient b)
    (hthree : (3 : F) ≠ 0) (hb : 2 ≤ b) :
    fiber.members.card * b.choose (b - 2) ≤ ambient.card.choose (b - 2) := by
  simpa only [Finset.card_powersetCard] using
    (disjointUniformFamily_packing fiber.members (b.choose (b - 2))
      (ambient.powersetCard (b - 2))
      (fun U ↦ U.powersetCard (b - 2))
      (by
        intro U hU W hW
        exact Finset.mem_powersetCard.mpr
          ⟨(Finset.mem_powersetCard.mp hW).1.trans
            (fiber.member_subset U hU),
           (Finset.mem_powersetCard.mp hW).2⟩)
      (by
        intro U hU
        simp only [Finset.card_powersetCard, fiber.member_card U hU])
      (fiber.certificates_pairwiseDisjoint hthree hb))

/-- Exact numerical packing cap `floor (choose 128 3 / choose 5 2) = 34,137`. -/
theorem SingletonMomentFiber.card_le_five
    {F : Type*} [Field F] [DecidableEq F]
    {ambient : Finset F}
    (fiber : SingletonMomentFiber F ambient 5)
    (hthree : (3 : F) ≠ 0) (hambient : ambient.card = 128) :
    fiber.members.card ≤ 34137 := by
  have hpack := fiber.card_mul_choose_le hthree (by norm_num : 2 ≤ 5)
  rw [hambient] at hpack
  norm_num [Nat.choose] at hpack
  omega

/-- Exact numerical packing cap `choose 128 5 / choose 7 2 = 12,598,400`. -/
theorem SingletonMomentFiber.card_le_seven
    {F : Type*} [Field F] [DecidableEq F]
    {ambient : Finset F}
    (fiber : SingletonMomentFiber F ambient 7)
    (hthree : (3 : F) ≠ 0) (hambient : ambient.card = 128) :
    fiber.members.card ≤ 12598400 := by
  have hpack := fiber.card_mul_choose_le hthree (by norm_num : 2 ≤ 7)
  rw [hambient] at hpack
  norm_num [Nat.choose] at hpack
  omega

/-! ## Fixed-singleton cell compiler -/

/-- A certificate interface for one `q = 128` singleton-occupancy cell.
There are 128 possible quotient constants; within each constant fiber the
singleton sets satisfy the moment interface, and every candidate lies in a
local fixed-singleton cell. -/
structure Q128OccupancyCertificate
    (α F : Type*) [DecidableEq α] [Field F] [DecidableEq F]
    (ambient : Finset F) (b localCap : ℕ) where
  target : Finset α
  fibers : Fin 128 → SingletonMomentFiber F ambient b
  cell : Fin 128 → Finset F → Finset α
  cover : target ⊆
    (Finset.univ : Finset (Fin 128)).biUnion fun c ↦
      (fibers c).members.biUnion (cell c)
  cell_card : ∀ c U, U ∈ (fibers c).members → (cell c U).card ≤ localCap

theorem Q128OccupancyCertificate.target_card_le_of_family_bound
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    {ambient : Finset F} {b localCap : ℕ}
    (cert : Q128OccupancyCertificate α F ambient b localCap)
    (familyCap : ℕ)
    (hfamily : ∀ c, (cert.fibers c).members.card ≤ familyCap) :
    cert.target.card ≤ 128 * familyCap * localCap := by
  have hinner : ∀ c : Fin 128,
      ((cert.fibers c).members.biUnion (cert.cell c)).card ≤
        familyCap * localCap := by
    intro c
    calc
      ((cert.fibers c).members.biUnion (cert.cell c)).card ≤
          (cert.fibers c).members.card * localCap :=
        FirstMatchAddBack.profileUnion_card_le_family_mul_budget
          (cert.fibers c).members (cert.cell c) localCap
          (fun U hU ↦ cert.cell_card c U hU)
      _ ≤ familyCap * localCap := Nat.mul_le_mul_right localCap (hfamily c)
  have houter :
      ((Finset.univ : Finset (Fin 128)).biUnion fun c ↦
        (cert.fibers c).members.biUnion (cert.cell c)).card ≤
          (Finset.univ : Finset (Fin 128)).card *
            (familyCap * localCap) :=
    FirstMatchAddBack.profileUnion_card_le_family_mul_budget
      (Finset.univ : Finset (Fin 128))
      (fun c ↦ (cert.fibers c).members.biUnion (cert.cell c))
      (familyCap * localCap) (fun c _hc ↦ hinner c)
  calc
    cert.target.card ≤
        ((Finset.univ : Finset (Fin 128)).biUnion fun c ↦
          (cert.fibers c).members.biUnion (cert.cell c)).card :=
      Finset.card_le_card cert.cover
    _ ≤ (Finset.univ : Finset (Fin 128)).card *
        (familyCap * localCap) := houter
    _ = 128 * familyCap * localCap := by simp [Nat.mul_assoc]

theorem Q128OccupancyCertificate.target_card_le_five
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    {ambient : Finset F}
    (cert : Q128OccupancyCertificate α F ambient 5 14641173)
    (hthree : (3 : F) ≠ 0) (hambient : ambient.card = 128) :
    cert.target.card ≤ 128 * 34137 * 14641173 :=
  cert.target_card_le_of_family_bound 34137
    (fun c ↦ (cert.fibers c).card_le_five hthree hambient)

theorem Q128OccupancyCertificate.target_card_le_seven
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    {ambient : Finset F}
    (cert : Q128OccupancyCertificate α F ambient 7 10193410)
    (hthree : (3 : F) ≠ 0) (hambient : ambient.card = 128) :
    cert.target.card ≤ 128 * 12598400 * 10193410 :=
  cert.target_card_le_of_family_bound 12598400
    (fun c ↦ (cert.fibers c).card_le_seven hthree hambient)

/-- The exact new `b = 5, 7` subtotal from the source packet. -/
theorem q128_b5_b7_card_le
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    {ambient : Finset F}
    (cert5 : Q128OccupancyCertificate α F ambient 5 14641173)
    (cert7 : Q128OccupancyCertificate α F ambient 7 10193410)
    (hthree : (3 : F) ≠ 0) (hambient : ambient.card = 128) :
    (cert5.target ∪ cert7.target).card ≤ 16501819170137728 := by
  calc
    (cert5.target ∪ cert7.target).card ≤
        cert5.target.card + cert7.target.card :=
      Finset.card_union_le cert5.target cert7.target
    _ ≤ 128 * 34137 * 14641173 + 128 * 12598400 * 10193410 :=
      Nat.add_le_add
        (cert5.target_card_le_five hthree hambient)
        (cert7.target_card_le_seven hthree hambient)
    _ = 16501819170137728 := by norm_num

/-- PR #819's first-match union theorem with its largest component hypothesis
replaced by the exact two-moment singleton-certificate interface. -/
theorem c0_periodic_first_match_payment_of_singleton_certificates
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    {ambient : Finset F}
    (bad q64f29 q64f28 : Finset α)
    (cert5 : Q128OccupancyCertificate α F ambient 5 14641173)
    (cert7 : Q128OccupancyCertificate α F ambient 7 10193410)
    (hthree : (3 : F) ≠ 0) (hambient : ambient.card = 128)
    (hcover : bad ⊆
      q64f29 ∪ q64f28 ∪ cert5.target ∪ cert7.target)
    (h29 : q64f29.card ≤ 1619679744)
    (h28 : q64f28.card ≤ 83970774720) :
    bad.card ≤ 16501904760592192 :=
  GrandeFinale.c0_periodic_first_match_payment_target
    bad q64f29 q64f28 cert5.target cert7.target
    hcover h29 h28 (q128_b5_b7_card_le cert5 cert7 hthree hambient)

#print axioms eq_of_common_omittedPair_certificate
#print axioms SingletonMomentFiber.card_mul_choose_le
#print axioms q128_b5_b7_card_le
#print axioms c0_periodic_first_match_payment_of_singleton_certificates

end GrandeFinale.C0PeriodicSingletonCertificate
