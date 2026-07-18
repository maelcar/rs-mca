/-!
# Map-smooth agreement arithmetic and collision-aware cap anchors

This package follows the actual map-smooth source labels and proves their
all-parameter agreement arithmetic together with fixed numerical cap anchors:

Source labels (active thresholds paper; identical in the frontiers draft):
- lem:map-smooth-fiber: ℓ=⌊k/a⌋+2, A=aℓ, if ℓ≤N−1 then a list of
  size ≥ binom(N,ℓ)/|B| codewords agrees on ≥ A positions; and
  k+a+1 ≤ A ≤ k+2a (equality A=k+2a if a∣k)
- prop:map-smooth-cap: with L=⌈binom(N,ℓ)/|B|⌉,
  B_MCA(m) ≥ ⌈ L(q−n) / (q−n + k(L−1)) ⌉ for k+1 ≤ m ≤ A

Explicit integer toy (a∣k so A equals k+2a):
- a=2, k=2, N=4 (so n=a·N=8 for complete a-fibers), ℓ=⌊2/2⌋+2=3
- ℓ≤N−1: 3≤3 OK
- A=a·ℓ=6
- k+a+1=5 ≤ A=6 ≤ k+2a=6, and A=k+2a since a∣k
- |B|=2: L=⌈C(4,3)/2⌉=⌈4/2⌉=2
- Cap: q−n=2, L=2, k=2 → L(q−n)/(q−n+k(L−1))=4/(2+2)=1 exact

No `sorry`. No mathlib. Fixed numerical anchors retain dual
`native_decide` / `decide` checks.
-/

namespace PetalFiber

def binom : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => binom n (k + 1) + binom n k

/-- Ceil division ⌈num/den⌉ for den > 0. -/
def ceilDiv (num den : Nat) : Nat := (num + den - 1) / den

/-! ## General arithmetic in `lem:map-smooth-fiber`.

The source has `a ≥ 1` because `a` is the positive degree of a map-smooth
polynomial.  This positivity is necessary only for the lower endpoint.  The
remainder identity, upper endpoint, and divisibility characterization are valid
for all natural `a`, including Lean's total-division case `a = 0`. -/

/-- Exact division-algorithm kernel for `A = a * (k / a + 2)`. -/
theorem map_smooth_agreement_remainder (k₀ a₀ : Nat) :
    a₀ * (k₀ / a₀ + 2) + k₀ % a₀ = k₀ + 2 * a₀ := by
  have hsplit : k₀ % a₀ + a₀ * (k₀ / a₀) = k₀ :=
    Nat.mod_add_div k₀ a₀
  rw [Nat.mul_add]
  omega

/-- Lower endpoint of the source agreement window.  Positivity is necessary. -/
theorem map_smooth_agreement_lower (k₀ a₀ : Nat) (ha : 0 < a₀) :
    k₀ + a₀ + 1 ≤ a₀ * (k₀ / a₀ + 2) := by
  have hmod : k₀ % a₀ < a₀ := Nat.mod_lt k₀ ha
  have hrem := map_smooth_agreement_remainder k₀ a₀
  omega

/-- Upper endpoint of the source agreement window; no positivity is needed. -/
theorem map_smooth_agreement_upper (k₀ a₀ : Nat) :
    a₀ * (k₀ / a₀ + 2) ≤ k₀ + 2 * a₀ := by
  have hrem := map_smooth_agreement_remainder k₀ a₀
  omega

/-- The full source agreement window, with the implicit positive-degree
    hypothesis made explicit. -/
theorem map_smooth_agreement_window (k₀ a₀ : Nat) (ha : 0 < a₀) :
    k₀ + a₀ + 1 ≤ a₀ * (k₀ / a₀ + 2) ∧
      a₀ * (k₀ / a₀ + 2) ≤ k₀ + 2 * a₀ :=
  ⟨map_smooth_agreement_lower k₀ a₀ ha,
    map_smooth_agreement_upper k₀ a₀⟩

/-- Source equality case: divisibility eliminates the remainder. -/
theorem map_smooth_agreement_eq_of_dvd (k₀ a₀ : Nat) (hdiv : a₀ ∣ k₀) :
    a₀ * (k₀ / a₀ + 2) = k₀ + 2 * a₀ := by
  rw [Nat.mul_add, Nat.mul_div_cancel' hdiv, Nat.mul_comm a₀ 2]

/-- Exact characterization of the top endpoint, including `a = 0`. -/
theorem map_smooth_agreement_eq_top_iff (k₀ a₀ : Nat) :
    a₀ * (k₀ / a₀ + 2) = k₀ + 2 * a₀ ↔ a₀ ∣ k₀ := by
  constructor
  · intro htop
    apply Nat.dvd_of_mod_eq_zero
    have hrem := map_smooth_agreement_remainder k₀ a₀
    omega
  · exact map_smooth_agreement_eq_of_dvd k₀ a₀

/-- The lower endpoint would be false without the source's positive degree:
    at `a = k = 0` it says `1 ≤ 0`. -/
theorem map_smooth_agreement_lower_false_at_zero :
    ¬ ((0 : Nat) + 0 + 1 ≤ 0 * (0 / 0 + 2)) := by
  native_decide

/-! ## Map-smooth parameters (lem:map-smooth-fiber) -/

def a : Nat := 2
def k : Nat := 2
def Nq : Nat := 4
def n : Nat := a * Nq
def Bsize : Nat := 2

def ell : Nat := k / a + 2
def Aagree : Nat := a * ell

theorem ell_value : ell = 3 := by native_decide
theorem n_value : n = 8 := by native_decide
theorem Aagree_value : Aagree = 6 := by native_decide

/-- Side condition ℓ ≤ N−1. -/
theorem ell_le_N_minus_1 : ell ≤ Nq - 1 := by native_decide

/-- Agreement window: k+a+1 ≤ A ≤ k+2a. -/
theorem A_lower : k + a + 1 ≤ Aagree := by
  simpa [Aagree, ell] using
    (map_smooth_agreement_lower k a (by decide))
theorem A_upper : Aagree ≤ k + 2 * a := by
  simpa [Aagree, ell] using map_smooth_agreement_upper k a

/-- Equality case a ∣ k ⇒ A = k+2a. -/
theorem a_divides_k : k % a = 0 := by native_decide
theorem A_eq_k_plus_2a : Aagree = k + 2 * a := by
  simpa [Aagree, ell] using
    (map_smooth_agreement_eq_of_dvd k a
      (Nat.dvd_of_mod_eq_zero a_divides_k))

/-! ## List size L = ⌈binom(N,ℓ)/|B|⌉ -/

def Llist : Nat := ceilDiv (binom Nq ell) Bsize

theorem binom_4_3 : binom 4 3 = 4 := by native_decide
theorem Llist_value : Llist = 2 := by native_decide
theorem Llist_exact_div : binom Nq ell / Bsize = 2 := by native_decide

/-- Lemma conclusion shape: list size lower bound is Llist. -/
theorem list_size_lower : Llist ≥ 1 := by native_decide

/-! ## prop:map-smooth-cap lower bound (exact integer) -/

def qMinusN : Nat := 2
def capNum : Nat := Llist * qMinusN
def capDen : Nat := qMinusN + k * (Llist - 1)
def capExact : Nat := capNum / capDen
def capCeil : Nat := ceilDiv capNum capDen

theorem capDen_value : capDen = 4 := by native_decide
theorem capNum_value : capNum = 4 := by native_decide
theorem cap_divides : capNum = capExact * capDen := by native_decide
theorem capExact_value : capExact = 1 := by native_decide
theorem capCeil_eq_exact : capCeil = capExact := by native_decide

/-- Numerical RHS/cap anchor equals `1`; no MCA object is encoded. -/
theorem map_smooth_cap_instance : capExact = 1 := by native_decide
theorem map_smooth_cap_pos : capExact ≥ 1 := by native_decide

/-- Threshold range nonempty: k+1 ≤ m ≤ A with m=k+1. -/
def mThresh : Nat := k + 1
theorem m_ge_k_plus_1 : k + 1 ≤ mThresh := by native_decide
theorem m_le_A : mThresh ≤ Aagree := by native_decide

/-! ## Dual via `decide` -/

theorem ell_value' : ell = 3 := by decide
theorem A_eq_k_plus_2a' : Aagree = k + 2 * a := by decide
theorem ell_le_N_minus_1' : ell ≤ Nq - 1 := by decide
theorem Llist_value' : Llist = 2 := by decide
theorem capExact_value' : capExact = 1 := by decide
theorem A_lower' : k + a + 1 ≤ Aagree := by decide
theorem A_upper' : Aagree ≤ k + 2 * a := by decide

end PetalFiber
