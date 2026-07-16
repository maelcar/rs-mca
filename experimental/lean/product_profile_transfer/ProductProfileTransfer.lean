/-!
# The product-profile transfer certificate: decidable counting shadow

Maps to **hard input 2**: eleventh packet of the arc.  The note proves
the dense-band indicator transform is an IFS cocycle in the balanced
digit scan (C1), class data is computed exactly by a carry DP whose
transition is closed on {-1,0,1} with every final carry accepted (C2),
a Chebyshev function-valued DP evaluates it in O(B^2 K^2) with
geometric measured convergence (C3, computed), and the machinery covers
every symmetric product profile (C4).

Note:     `experimental/notes/thresholds/product_profile_transfer_certificate.md`.
Verifier: `experimental/scripts/verify_product_profile_transfer.py`
          (11/11, tamper 5/5).

Analytic results (PROVED in note + Python verifier; NOT in Lean): the
trig content lives in the scans.  This module is the DECIDABLE
arithmetic shadow (stdlib-only `native_decide`, no mathlib, no
`sorry`): the carry automaton's closure and reconstruction identities,
and the digit facts.
-/

namespace ProductProfileTransfer

/-- Balanced carry step: `v = e - g + ci`, digit `d = ((v+1) mod 3) - 1`
    (as Int arithmetic), carry `co = (v - d)/3`. -/
def step (e g ci : Int) : Int × Int :=
  let v := e - g + ci
  let d := (v + 1) % 3 - 1 + (if (v + 1) % 3 < 0 then 3 else 0)
  (d, (v - d) / 3)

/-- The 27-case closure: digits and carries stay in {-1,0,1} and the
    reconstruction `v = d + 3 co` holds. -/
theorem carry_closure :
    ∀ e ∈ [(-1 : Int), 0, 1], ∀ g ∈ [(-1 : Int), 0, 1],
      ∀ ci ∈ [(-1 : Int), 0, 1],
        (step e g ci).1 ≥ -1 ∧ (step e g ci).1 ≤ 1 ∧
        (step e g ci).2 ≥ -1 ∧ (step e g ci).2 ≤ 1 ∧
        e - g + ci = (step e g ci).1 + 3 * (step e g ci).2 := by
  native_decide

/-- Nonzero canonical balanced-ternary digits of `y mod 3^ndig`. -/
def s3 (y ndig : Nat) : Nat :=
  match ndig with
  | 0 => 0
  | n + 1 =>
    let d := y % 3
    if d = 0 then s3 (y / 3) n
    else if d = 1 then 1 + s3 (y / 3) n
    else 1 + s3 (y / 3 + 1) n

/-- `binom n k = C(n,k)` via the running product. -/
def binom (n k : Nat) : Nat :=
  (List.range k).foldl (fun acc i => acc * (n - i) / (i + 1)) 1

/-! ## Digit facts reused by the DP's terminal weights. -/

theorem dense_shell_counts :
    ∀ B ∈ [4, 6, 8],
      ((List.range (3 ^ B)).filter (fun a => s3 a B = B)).length
        = 2 ^ B := by
  native_decide

theorem class_pins :
    binom 12 6 = 924 ∧ binom 16 8 = 12870 ∧
    (∀ s ∈ [0, 2, 4, 6],
      (if s ≤ 6 ∧ s % 2 = 0 then binom (6 - s) ((6 - s) / 2) else 0)
        = [20, 6, 2, 1].getD (s / 2) 0) := by
  native_decide

end ProductProfileTransfer
