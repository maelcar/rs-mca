namespace AsymptoticSpine

/-!
# Shared stdlib-only list utilities

Lean core exposes no uniform `List.sum` at this toolchain pin, so the asymptotic
spine carries its own `listSum` over `List Nat`, together with the two length/sum
facts used by the first-match and moment lemmas.  Kernel-checked, stdlib-only,
no mathlib.
-/

/-- Sum of a `List Nat`. -/
def listSum : List Nat → Nat
  | [] => 0
  | a :: l => a + listSum l

@[simp] theorem listSum_nil : listSum [] = 0 := rfl
@[simp] theorem listSum_cons (a : Nat) (l : List Nat) :
    listSum (a :: l) = a + listSum l := rfl

/-- Length of a flattened list of lists is the sum of the block lengths. -/
theorem length_flatten (L : List (List Nat)) :
    L.flatten.length = listSum (L.map List.length) := by
  induction L with
  | nil => simp
  | cons c cs ih => simp [List.flatten_cons, List.length_append, ih]

/-- Monotonicity of `listSum` under a pointwise `≤` supplied via `List.zip`. -/
theorem listSum_le_of_zip :
    ∀ (a b : List Nat), a.length ≤ b.length →
      (∀ p ∈ a.zip b, p.1 ≤ p.2) → listSum a ≤ listSum b := by
  intro a
  induction a with
  | nil => intro b _ _; simp
  | cons x xs ih =>
    intro b hlen hpair
    cases b with
    | nil => simp at hlen
    | cons y ys =>
      have hx : x ≤ y := hpair (x, y) (by simp)
      have hpair' : ∀ p ∈ xs.zip ys, p.1 ≤ p.2 := by
        intro p hp; exact hpair p (by simp [List.zip_cons_cons]; exact Or.inr hp)
      have hlen' : xs.length ≤ ys.length := by
        simp only [List.length_cons] at hlen; omega
      have := ih ys hlen' hpair'
      simp only [listSum_cons]; omega

end AsymptoticSpine
