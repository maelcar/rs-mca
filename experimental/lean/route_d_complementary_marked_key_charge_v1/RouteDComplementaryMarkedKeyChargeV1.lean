import Std

namespace RouteDComplementaryMarkedKeyChargeV1

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
          let g : Fin n → Fin m := fun i =>
            Fin.delete omitted (f i.castSucc) (hne i)
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

private def Fin.pack {t p : Nat} (x : Fin t × Fin p) : Fin (t * p) :=
  ⟨p * x.1.val + x.2.val, by
    calc
      p * x.1.val + x.2.val < p * x.1.val + p :=
        Nat.add_lt_add_left x.2.isLt _
      _ = p * (x.1.val + 1) := by simp [Nat.mul_add]
      _ ≤ p * t := by
        apply Nat.mul_le_mul_left
        omega
      _ = t * p := Nat.mul_comm _ _⟩

private theorem Fin.pack_injective {t p : Nat} {x y : Fin t × Fin p}
    (h : Fin.pack x = Fin.pack y) : x = y := by
  have hp : 0 < p := Nat.zero_lt_of_lt x.2.isLt
  have hv := congrArg Fin.val h
  have hfirst := congrArg (fun n => n / p) hv
  have hsecond := congrArg (fun n => n % p) hv
  simp only [Fin.pack, Nat.mul_add_div hp, Nat.div_eq_of_lt x.2.isLt,
    Nat.div_eq_of_lt y.2.isLt, Nat.add_zero] at hfirst
  simp only [Fin.pack, Nat.mul_add_mod, Nat.mod_eq_of_lt x.2.isLt,
    Nat.mod_eq_of_lt y.2.isLt] at hsecond
  apply Prod.ext
  · exact Fin.ext hfirst
  · exact Fin.ext hsecond

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

theorem sum_card_le_target_of_direct_injection
    (generatedCard defectCard t p : Nat)
    (code : Fin generatedCard ⊕ Fin defectCard → Fin t × Fin p)
    (hinj : ∀ ⦃x y⦄, code x = code y → x = y) :
    generatedCard + defectCard ≤ t * p := by
  let packed : Fin (generatedCard + defectCard) → Fin (t * p) := fun x =>
    Fin.pack (code (Fin.split x))
  apply fin_card_le_of_injective packed
  intro x y equality
  exact Fin.split_injective (hinj (Fin.pack_injective equality))

def complementaryCharge
    {Generated Defect Row Scalar : Type}
    (generatedCharge : Generated → Row × Scalar)
    (defectCharge : Defect → Row × Scalar) :
    Generated ⊕ Defect → Row × Scalar
  | Sum.inl generated => generatedCharge generated
  | Sum.inr defect => defectCharge defect

theorem complementaryCellCharge_injective
    {Generated Defect Row Scalar : Type}
    (markedCell : Row × Scalar → Prop)
    (generatedCharge : Generated → Row × Scalar)
    (defectCharge : Defect → Row × Scalar)
    (generatedInjective :
      ∀ ⦃x y⦄, generatedCharge x = generatedCharge y → x = y)
    (defectInjective :
      ∀ ⦃x y⦄, defectCharge x = defectCharge y → x = y)
    (generatedInside :
      ∀ generated, markedCell (generatedCharge generated))
    (defectOutside :
      ∀ defect, ¬ markedCell (defectCharge defect)) :
    ∀ ⦃x y⦄,
      complementaryCharge generatedCharge defectCharge x =
        complementaryCharge generatedCharge defectCharge y →
      x = y := by
  intro left right equality
  cases left with
  | inl generatedLeft =>
      cases right with
      | inl generatedRight =>
          have chargeEquality :
              generatedCharge generatedLeft =
                generatedCharge generatedRight := by
            simpa [complementaryCharge] using equality
          exact congrArg Sum.inl (generatedInjective chargeEquality)
      | inr defectRight =>
          have chargeEquality :
              generatedCharge generatedLeft =
                defectCharge defectRight := by
            simpa [complementaryCharge] using equality
          have enteredMarked :
              markedCell (defectCharge defectRight) := by
            rw [← chargeEquality]
            exact generatedInside generatedLeft
          exact (defectOutside defectRight enteredMarked).elim
  | inr defectLeft =>
      cases right with
      | inl generatedRight =>
          have chargeEquality :
              defectCharge defectLeft =
                generatedCharge generatedRight := by
            simpa [complementaryCharge] using equality
          have enteredMarked :
              markedCell (defectCharge defectLeft) := by
            rw [chargeEquality]
            exact generatedInside generatedRight
          exact (defectOutside defectLeft enteredMarked).elim
      | inr defectRight =>
          have chargeEquality :
              defectCharge defectLeft =
                defectCharge defectRight := by
            simpa [complementaryCharge] using equality
          exact congrArg Sum.inr (defectInjective chargeEquality)

theorem complementaryCharge_injective
    {Generated Defect Row Scalar : Type}
    (marked : Scalar → Prop)
    (generatedCharge : Generated → Row × Scalar)
    (defectCharge : Defect → Row × Scalar)
    (generatedInjective :
      ∀ ⦃x y⦄, generatedCharge x = generatedCharge y → x = y)
    (defectInjective :
      ∀ ⦃x y⦄, defectCharge x = defectCharge y → x = y)
    (generatedMarked :
      ∀ generated, marked (generatedCharge generated).2)
    (defectUnmarked :
      ∀ defect, ¬ marked (defectCharge defect).2) :
    ∀ ⦃x y⦄,
      complementaryCharge generatedCharge defectCharge x =
        complementaryCharge generatedCharge defectCharge y →
      x = y := by
  intro left right equality
  cases left with
  | inl generatedLeft =>
      cases right with
      | inl generatedRight =>
          have chargeEquality :
              generatedCharge generatedLeft =
                generatedCharge generatedRight := by
            simpa [complementaryCharge] using equality
          exact congrArg Sum.inl (generatedInjective chargeEquality)
      | inr defectRight =>
          have scalarEquality :
              (generatedCharge generatedLeft).2 =
                (defectCharge defectRight).2 := by
            simpa [complementaryCharge] using congrArg Prod.snd equality
          have enteredMarked :
              marked (defectCharge defectRight).2 := by
            rw [← scalarEquality]
            exact generatedMarked generatedLeft
          exact (defectUnmarked defectRight enteredMarked).elim
  | inr defectLeft =>
      cases right with
      | inl generatedRight =>
          have scalarEquality :
              (defectCharge defectLeft).2 =
                (generatedCharge generatedRight).2 := by
            simpa [complementaryCharge] using congrArg Prod.snd equality
          have enteredMarked :
              marked (defectCharge defectLeft).2 := by
            rw [scalarEquality]
            exact generatedMarked generatedRight
          exact (defectUnmarked defectLeft enteredMarked).elim
      | inr defectRight =>
          have chargeEquality :
              defectCharge defectLeft =
                defectCharge defectRight := by
            simpa [complementaryCharge] using equality
          exact congrArg Sum.inr (defectInjective chargeEquality)


theorem route_d_complementary_cell_charge
    (generatedCard defectCard t p : Nat)
    (markedCell : Fin t × Fin p → Prop)
    (generatedCharge : Fin generatedCard → Fin t × Fin p)
    (defectCharge : Fin defectCard → Fin t × Fin p)
    (generatedInjective :
      ∀ ⦃x y⦄, generatedCharge x = generatedCharge y → x = y)
    (defectInjective :
      ∀ ⦃x y⦄, defectCharge x = defectCharge y → x = y)
    (generatedInside :
      ∀ generated, markedCell (generatedCharge generated))
    (defectOutside :
      ∀ defect, ¬ markedCell (defectCharge defect)) :
    generatedCard + defectCard ≤ t * p := by
  apply sum_card_le_target_of_direct_injection _ _ _ _
    (complementaryCharge generatedCharge defectCharge)
  exact complementaryCellCharge_injective markedCell generatedCharge
    defectCharge generatedInjective defectInjective generatedInside
    defectOutside

theorem route_d_complementary_marked_key_charge
    (generatedCard defectCard t p : Nat)
    (marked : Fin p → Prop)
    (generatedCharge : Fin generatedCard → Fin t × Fin p)
    (defectCharge : Fin defectCard → Fin t × Fin p)
    (generatedInjective :
      ∀ ⦃x y⦄, generatedCharge x = generatedCharge y → x = y)
    (defectInjective :
      ∀ ⦃x y⦄, defectCharge x = defectCharge y → x = y)
    (generatedMarked :
      ∀ generated, marked (generatedCharge generated).2)
    (defectUnmarked :
      ∀ defect, ¬ marked (defectCharge defect).2) :
    generatedCard + defectCard ≤ t * p := by
  exact route_d_complementary_cell_charge generatedCard defectCard t p
    (fun cell => marked cell.2) generatedCharge defectCharge
    generatedInjective defectInjective generatedMarked defectUnmarked

theorem complementary_complete_base_charge
    {Profile : Type}
    (generatedCard defectCard baseCard t p : Nat)
    (generatedCharge : Fin generatedCard → Fin t × Fin p)
    (generatedInjective :
      ∀ ⦃x y⦄, generatedCharge x = generatedCharge y → x = y)
    (encode : Fin defectCard → Sigma fun _ : Fin baseCard => Profile)
    (encodeInjective : ∀ ⦃x y⦄, encode x = encode y → x = y)
    (slot : Fin baseCard → Profile → Fin t)
    (slotInjectiveOnRealized :
      ∀ (base : Fin baseCard) (x y : Profile),
        (∃ defect, encode defect = ⟨base, x⟩) →
        (∃ defect, encode defect = ⟨base, y⟩) →
        slot base x = slot base y → x = y)
    (baseScalar : Fin baseCard → Fin p)
    (baseScalarInjective :
      ∀ ⦃x y⦄, baseScalar x = baseScalar y → x = y)
    (separate :
      ∀ generated base,
        (generatedCharge generated).2 ≠ baseScalar base) :
    generatedCard + defectCard ≤ t * p := by
  let defectCharge : Fin defectCard → Fin t × Fin p := fun defect =>
    (slot (encode defect).1 (encode defect).2, baseScalar (encode defect).1)
  have defectInjective :
      ∀ ⦃x y⦄, defectCharge x = defectCharge y → x = y := by
    intro x y equality
    have baseEquality :
        (encode x).1 = (encode y).1 :=
      baseScalarInjective (congrArg Prod.snd equality)
    cases hx : encode x with
    | mk bx px =>
        cases hy : encode y with
        | mk by0 py =>
            simp only [defectCharge, hx, hy] at baseEquality equality
            cases baseEquality
            have slotEquality : slot bx px = slot bx py :=
              congrArg Prod.fst equality
            have profileEquality : px = py :=
              slotInjectiveOnRealized bx px py
                ⟨x, hx⟩ ⟨y, hy⟩ slotEquality
            apply encodeInjective
            simp [hx, hy, profileEquality]
  let marked : Fin p → Prop := fun scalar =>
    ∀ base, scalar ≠ baseScalar base
  have generatedMarked :
      ∀ generated, marked (generatedCharge generated).2 := by
    intro generated base
    exact separate generated base
  have defectUnmarked :
      ∀ defect, ¬ marked (defectCharge defect).2 := by
    intro defect allSeparate
    exact allSeparate (encode defect).1 rfl
  exact route_d_complementary_marked_key_charge
    generatedCard defectCard t p marked generatedCharge defectCharge
    generatedInjective defectInjective generatedMarked defectUnmarked


def cellFixtureGeneratedCharge (scalar : Fin 3) : Fin 2 × Fin 3 :=
  (⟨0, by decide⟩, scalar)

def cellFixtureDefectCharge (scalar : Fin 3) : Fin 2 × Fin 3 :=
  (⟨1, by decide⟩, scalar)

def cellFixtureMarked (cell : Fin 2 × Fin 3) : Prop :=
  cell.1 = ⟨0, by decide⟩

theorem cellFixtureGeneratedInjective :
    ∀ ⦃x y⦄,
      cellFixtureGeneratedCharge x = cellFixtureGeneratedCharge y → x = y := by
  intro x y equality
  exact congrArg Prod.snd equality

theorem cellFixtureDefectInjective :
    ∀ ⦃x y⦄,
      cellFixtureDefectCharge x = cellFixtureDefectCharge y → x = y := by
  intro x y equality
  exact congrArg Prod.snd equality

theorem cellFixtureGeneratedInside :
    ∀ generated,
      cellFixtureMarked (cellFixtureGeneratedCharge generated) := by
  intro generated
  rfl

theorem cellFixtureDefectOutside :
    ∀ defect,
      ¬ cellFixtureMarked (cellFixtureDefectCharge defect) := by
  intro defect equality
  have valueEquality := congrArg Fin.val equality
  simp [cellFixtureMarked, cellFixtureDefectCharge] at valueEquality

theorem strict_cell_complement_fixture_bound :
    3 + 3 ≤ 2 * 3 :=
  route_d_complementary_cell_charge 3 3 2 3
    cellFixtureMarked cellFixtureGeneratedCharge cellFixtureDefectCharge
    cellFixtureGeneratedInjective cellFixtureDefectInjective
    cellFixtureGeneratedInside cellFixtureDefectOutside

theorem strict_cell_fixture_has_no_scalar_separator :
    ¬ ∃ marked : Fin 3 → Prop,
      (∀ generated, marked (cellFixtureGeneratedCharge generated).2) ∧
      (∀ defect, ¬ marked (cellFixtureDefectCharge defect).2) := by
  intro existsMarked
  obtain ⟨marked, generatedMarked, defectUnmarked⟩ := existsMarked
  let scalar : Fin 3 := ⟨0, by decide⟩
  exact defectUnmarked scalar (generatedMarked scalar)

theorem deployed_target_pin :
    67472 * 2130706433 = 143763024447376 := by
  native_decide

theorem image_only_countermodel_pin :
    2 * (2 * 5) > 2 * 5 := by
  native_decide

theorem local_one_scalar_sum_countermodel_pin :
    3 * 5 > 2 * 5 := by
  native_decide

theorem actual_all_minors_owner_adapter
    {allMaximalMinorsVanish rankDrop : Prop}
    (adapter : allMaximalMinorsVanish ↔ rankDrop) :
    allMaximalMinorsVanish → rankDrop :=
  adapter.mp

end RouteDComplementaryMarkedKeyChargeV1
