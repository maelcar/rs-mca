import Std

namespace RouteDMarkedKeyGlobalAddbackNoGoV1

private def Fin.delete {m : Nat} (a y : Fin (m + 1)) (hne : y ≠ a) : Fin m :=
  if hlt : y.val < a.val then
    ⟨y.val, by omega⟩
  else
    ⟨y.val - 1, by omega⟩

private theorem Fin.delete_injective {m : Nat} (a : Fin (m + 1))
    {y₁ y₂ : Fin (m + 1)} (h₁ : y₁ ≠ a) (h₂ : y₂ ≠ a)
    (h : Fin.delete a y₁ h₁ = Fin.delete a y₂ h₂) : y₁ = y₂ := by
  simp only [Fin.delete] at h
  split at h <;> split at h <;> simp_all
  all_goals apply Fin.ext; omega

theorem fin_card_le_of_injective {n m : Nat} (f : Fin n → Fin m)
    (hinj : ∀ ⦃x y⦄, f x = f y → x = y) : n ≤ m := by
  induction n generalizing m with
  | zero => omega
  | succ n ih =>
      cases m with
      | zero => exact Fin.elim0 (f ⟨0, by omega⟩)
      | succ m =>
          let last : Fin (n + 1) := Fin.last n
          let omitted : Fin (m + 1) := f last
          have hne (i : Fin n) : f i.castSucc ≠ omitted := by
            intro heq
            have hs := hinj heq
            simp only [omitted, last] at hs
            have hv := congrArg Fin.val hs
            simp at hv
            have hi := i.isLt
            omega
          let g : Fin n → Fin m := fun i => Fin.delete omitted (f i.castSucc) (hne i)
          have hginj : ∀ ⦃i j⦄, g i = g j → i = j := by
            intro i j hij
            have hf : f i.castSucc = f j.castSucc :=
              Fin.delete_injective omitted (hne i) (hne j) hij
            have hc := hinj hf
            apply Fin.ext
            have hv := congrArg Fin.val hc
            exact hv
          have hnm := ih g hginj
          omega

private def Fin.pack {t b : Nat} (x : Fin t × Fin b) : Fin (t * b) :=
  ⟨b * x.1.val + x.2.val, by
    calc
      b * x.1.val + x.2.val < b * x.1.val + b :=
        Nat.add_lt_add_left x.2.isLt _
      _ = b * (x.1.val + 1) := by simp [Nat.mul_add]
      _ ≤ b * t := by
        apply Nat.mul_le_mul_left
        omega
      _ = t * b := Nat.mul_comm _ _⟩

private theorem Fin.pack_injective {t b : Nat} {x y : Fin t × Fin b}
    (h : Fin.pack x = Fin.pack y) : x = y := by
  have hb : 0 < b := by exact Nat.zero_lt_of_lt x.2.isLt
  have hv := congrArg Fin.val h
  have hfirst := congrArg (fun n => n / b) hv
  have hsecond := congrArg (fun n => n % b) hv
  simp only [Fin.pack, Nat.mul_add_div hb, Nat.div_eq_of_lt x.2.isLt,
    Nat.div_eq_of_lt y.2.isLt, Nat.add_zero] at hfirst
  simp only [Fin.pack, Nat.mul_add_mod, Nat.mod_eq_of_lt x.2.isLt,
    Nat.mod_eq_of_lt y.2.isLt] at hsecond
  apply Prod.ext
  · exact Fin.ext hfirst
  · exact Fin.ext hsecond

/-- An injective primitive encoder plus an injective `Fin t` slot map on every
admitted base fiber bounds the primitive cardinality by `t * baseCard`. -/
theorem card_prim_le_profile_cap_mul_card_base
    {Profile : Type} (primCard baseCard t : Nat)
    (encode : Fin primCard → Sigma fun _ : Fin baseCard => Profile)
    (hencode : ∀ ⦃x y⦄, encode x = encode y → x = y)
    (slot : Fin baseCard → Profile → Fin t)
    (hslot : ∀ (b : Fin baseCard) (p q : Profile),
      (∃ x, encode x = ⟨b, p⟩) →
      (∃ y, encode y = ⟨b, q⟩) →
      slot b p = slot b q → p = q) :
    primCard ≤ t * baseCard := by
  let code : Fin primCard → Fin (t * baseCard) := fun x =>
    Fin.pack (slot (encode x).1 (encode x).2, (encode x).1)
  apply fin_card_le_of_injective code
  intro x y hxy
  have hp := Fin.pack_injective hxy
  have hb : (encode x).1 = (encode y).1 := congrArg Prod.snd hp
  cases hbx : encode x with
  | mk bx px =>
      cases hby : encode y with
      | mk by0 py =>
          simp only [hbx, hby] at hb hp
          cases hb
          have hs : slot bx px = slot bx py := congrArg Prod.fst hp
          have hpx : px = py := hslot bx px py ⟨x, hbx⟩ ⟨y, hby⟩ hs
          apply hencode
          simp [hbx, hby, hpx]

theorem gen_add_prim_le_target_of_base_budget
    (genCard primCard baseCard t p : Nat)
    (hprim : primCard ≤ t * baseCard)
    (hbudget : genCard + t * baseCard ≤ t * p) :
    genCard + primCard ≤ t * p := by
  omega

private def Fin.split {g d : Nat} (i : Fin (g + d)) : Fin g ⊕ Fin d :=
  if h : i.val < g then
    Sum.inl ⟨i.val, h⟩
  else
    Sum.inr ⟨i.val - g, by omega⟩

private theorem Fin.split_injective {g d : Nat} {x y : Fin (g + d)}
    (h : Fin.split x = Fin.split y) : x = y := by
  simp only [Fin.split] at h
  split at h <;> split at h <;> simp_all
  all_goals apply Fin.ext; omega

theorem gen_sum_prim_le_target_of_direct_injection
    (genCard primCard t p : Nat)
    (code : Fin genCard ⊕ Fin primCard → Fin t × Fin p)
    (hinj : ∀ ⦃x y⦄, code x = code y → x = y) :
    genCard + primCard ≤ t * p := by
  let packed : Fin (genCard + primCard) → Fin (t * p) := fun x =>
    Fin.pack (code (Fin.split x))
  apply fin_card_le_of_injective packed
  intro x y hxy
  exact Fin.split_injective (hinj (Fin.pack_injective hxy))

private def sumCounts : List Nat → Nat
  | [] => 0
  | n :: ns => n + sumCounts ns

theorem per_key_caps_sum_to_key_multiple (counts : List Nat) (p : Nat)
    (hcap : ∀ n, n ∈ counts → n ≤ p) :
    sumCounts counts ≤ p * counts.length := by
  induction counts with
  | nil => simp [sumCounts]
  | cons n ns ih =>
      simp only [sumCounts, List.length_cons]
      have hn : n ≤ p := hcap n (by simp)
      have hns : ∀ q, q ∈ ns → q ≤ p := by
        intro q hq
        exact hcap q (by simp [hq])
      have hi := ih hns
      rw [Nat.mul_succ]
      omega

theorem two_key_caps_do_not_imply_global_cap (p : Nat) (hp : 0 < p) :
    (∀ n, n ∈ [p, p] → n ≤ p) ∧ ¬ sumCounts [p, p] ≤ p := by
  constructor
  · intro n hn
    simp at hn
    omega
  · simp [sumCounts]
    omega

end RouteDMarkedKeyGlobalAddbackNoGoV1
