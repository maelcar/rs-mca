import AsymptoticSpine.Moment

namespace AsymptoticSpine

/-!
# (B1) Image-normalization identities — `lem:ambient-image-max`, `lem:moment-normalization`, `ass:image-normalized-sidon-input`

Stdlib-only (no mathlib) formalization of the two normalization identities and the
two direction statements introduced by the B1 image-scale repair of
`experimental/asymptotic_rs_mca.tex` (the `\Scal=\operatorname{im}\Phi`,
`L=|\Scal|`, `M=|\OmegaC|`, `\barN=M/L` bookkeeping of `def:primitive-leaf`).

This module **stacks on the L1–L5 spine of PR #438** and formalizes the follow-up
that PR #439 (avdeevvadim) explicitly invited — *"Lean formalization of the two
normalization identities is a natural follow-up, but this PR is TeX/audit/verifier
only."*  Lineage: the B1 mismatch was flagged in the round audit (#436), repaired at
TeX scale in #439, and is mechanized here.  It reuses `AsymptoticSpine.Moment`'s
`listSumPow` (the discrete moment numerator `∑_s x_s^q`) rather than a new framework.

## Modeling: cardinality identity over `Nat`, not a `Rat` equation

The two moments of `lem:moment-normalization` are

    Γ_img(q) = L⁻¹ ∑_{s∈𝒮} (|F_s|/N̄)^q ,   N̄ = M/L ,
    Γ_amb(q) = A⁻¹ ∑_{y∈G} (|Ω∘∩Φ⁻¹(y)|/(M/A))^q ,

and the identity is `Γ_amb(q) = (A/L)^{q-1} Γ_img(q)`.  Lean *core* (v4.31.0, no
mathlib) carries **no algebraic hierarchy at all** — `Monoid`, `Ring`, `Field`,
`mul_pow`, `Nat.cast_pow`, `div_pow`, `ring` are all mathlib-only, and stdlib `Rat`
exposes only `Rat.mul_comm`/`Rat.mul_assoc`-style bare facts (this is the same
constraint `SigmaDiagonal.lean` documents when it keeps `Rat` to `1/lvl` with `rfl`).
So, exactly as the task permits ("*as an exact identity over `Rat` **or** as a
cardinality identity*") and following this package's established "clear the positive
normalization, state the scale-free integer content" convention (`Moment.lean`
header; correspondence note §0), the identity is formalized as a **cardinality
identity over `Nat`**, clearing the strictly positive denominators `L`, `A`, `M^q`,
`N̄`.  Since `L, A, M > 0`, clearing/uncleaning is an exact equivalence, so the `Nat`
statements are equivalent to — not weaker than — the `Rat` ones; the sole divergence
is of **form** (no `Rat` object is built), flagged in the correspondence note.

Two cleared moment numerators carry the content (`P = listSumPow q f = ∑_s|F_s|^q`,
the shared raw power sum; both equal `M^q` times the corresponding Γ):

    momImgN q L f = L^{q-1} · P = M^q · Γ_img(q) ,
    momAmbN q A f = A^{q-1} · P = M^q · Γ_amb(q) ,

using the **same** `f` because the ambient terms over `y ∉ 𝒮` vanish (`0^q=0`,
`q≥1`) — the "average is over `𝒮`, not an ambient group" point.  Their cross-relation

    L^{q-1} · momAmbN = A^{q-1} · momImgN

is the `Γ_amb=(A/L)^{q-1}Γ_img` identity cleared (`moment_normalization_ratio`),
while the honest summation form `∑_s(|F_s|·L)^q = L^q·P` etc.
(`moment_normalization_identity`) carries the real content (scale pull-out +
zero-vanishing).

Kernel-checked, stdlib-only, no mathlib.
-/

/-! ## Scale pull-out, additivity, and vanishing of ambient zeros

The three `listSumPow` facts behind the normalization identity: normalizing every
fiber by a common scale `c` multiplies the moment numerator by `c^q` (this is the
`N̄`-normalization / counting-vs-normalized-measure mechanism); `listSumPow` is
additive over `++`; and a block of empty ambient fibers (`y ∉ 𝒮`) contributes `0`
for `q ≥ 1`. -/

/-- **Scale pull-out.**  Scaling every fiber count by a common `c` (the cleared
`N̄`-normalization, `c=L` at image scale / `c=A` at ambient scale) multiplies the
`q`-th moment numerator by `c^q`: `∑_s (c·x_s)^q = c^q ∑_s x_s^q`. -/
theorem listSumPow_map_mul (q c : Nat) :
    ∀ f : List Nat, listSumPow q (f.map (· * c)) = c ^ q * listSumPow q f := by
  intro f
  induction f with
  | nil => simp
  | cons a t ih =>
    simp only [List.map_cons, listSumPow_cons, ih]
    rw [Nat.mul_pow, Nat.mul_add, Nat.mul_comm (a ^ q) (c ^ q)]

/-- `listSumPow` is additive over concatenation (the ambient sum `∑_{y∈G}` splits
into the image block `∑_{s∈𝒮}` plus the `y∉𝒮` block). -/
theorem listSumPow_append (q : Nat) :
    ∀ a b : List Nat, listSumPow q (a ++ b) = listSumPow q a + listSumPow q b := by
  intro a b
  induction a with
  | nil => simp
  | cons x t ih => simp only [List.cons_append, listSumPow_cons, ih, Nat.add_assoc]

/-- **Vanishing of the ambient zero block.**  For `q ≥ 1` a block of empty fibers
`y ∉ 𝒮` (count `0`) contributes nothing to the moment (`0^q = 0`); this is why the
ambient average reduces to the image average over `𝒮`. -/
theorem listSumPow_replicate_zero (q : Nat) (hq : 1 ≤ q) :
    ∀ k : Nat, listSumPow q (List.replicate k 0) = 0 := by
  intro k
  induction k with
  | zero => simp
  | succ n ih =>
    rw [List.replicate_succ, listSumPow_cons, ih, Nat.zero_pow (by omega : 0 < q)]

/-- The ambient moment numerator over `G` reduces to `A^q · P` over `𝒮`: pull the
ambient scale `A` out (`listSumPow_map_mul`) and drop the `y∉𝒮` zero block
(`listSumPow_replicate_zero`), where `k = A - L = |G| - |𝒮|`. -/
theorem ambient_sum_reduces (q A k : Nat) (hq : 1 ≤ q) (f : List Nat) :
    listSumPow q ((f ++ List.replicate k 0).map (· * A)) = A ^ q * listSumPow q f := by
  have hrep : (List.replicate k 0).map (· * A) = List.replicate k 0 := by
    simp [List.map_replicate]
  rw [List.map_append, listSumPow_append, listSumPow_map_mul, hrep,
    listSumPow_replicate_zero q hq k, Nat.add_zero]

/-! ## (i) Max-fiber transfer — `lem:ambient-image-max` -/

/-- **Every image fiber is an ambient fiber** ⇒ the image max is ≤ the ambient max.
`𝒮 = im Φ ⊆ G`, so each `F_s` (`s∈𝒮`) is an ambient fiber; hence a maximal image
fiber `mxImg ∈ img` is bounded by any ambient upper bound `mxAmb`. -/
theorem image_max_le_ambient_max (img amb : List Nat) (mxImg mxAmb : Nat)
    (hsub : ∀ x ∈ img, x ∈ amb) (hImgMem : mxImg ∈ img)
    (hAmbUB : ∀ x ∈ amb, x ≤ mxAmb) : mxImg ≤ mxAmb :=
  hAmbUB mxImg (hsub mxImg hImgMem)

/-- **Scale bridge** (cleared).  With `L ≤ A` (`|𝒮| ≤ |G|`) and `mxImg ≤ mxAmb`, an
ambient max bound `mxAmb ≤ C·(M/A)` (cleared: `mxAmb·A ≤ C·M`, `C = exp(o(N))`)
gives the image max bound `mxImg ≤ C·(M/L)` (cleared: `mxImg·L ≤ C·M`).  The step
`M/A ≤ M/L` from `L ≤ A` is here the `Nat` step `mxImg·L ≤ mxAmb·A`. -/
theorem ambient_image_max_transfer (A L M C mxImg mxAmb : Nat)
    (hLA : L ≤ A) (hmx : mxImg ≤ mxAmb) (hAmb : mxAmb * A ≤ C * M) :
    mxImg * L ≤ C * M :=
  Nat.le_trans (Nat.mul_le_mul hmx hLA) hAmb

/-- **(B1) `lem:ambient-image-max`, packaged.**  If the ambient max fiber obeys
`max_{y∈G}|Ω∘∩Φ⁻¹(y)| ≤ exp(o(N))·(M/A)` (cleared `mxAmb·A ≤ C·M`), then the image
max fiber obeys `max_{s∈𝒮}|F_s| ≤ exp(o(N))·N̄` with `N̄ = M/L` (cleared
`mxImg·L ≤ C·M`).  The `exp(o(N))` factor is the `Nat` placeholder `C` (same
convention as `NoHighEnergy.lean`'s `K^C`); the reals bookkeeping stays in the tex. -/
theorem ambient_image_max (img amb : List Nat) (A L M C mxImg mxAmb : Nat)
    (hLA : L ≤ A) (hsub : ∀ x ∈ img, x ∈ amb) (hImgMem : mxImg ∈ img)
    (hAmbUB : ∀ x ∈ amb, x ≤ mxAmb) (hAmb : mxAmb * A ≤ C * M) :
    mxImg * L ≤ C * M :=
  ambient_image_max_transfer A L M C mxImg mxAmb hLA
    (image_max_le_ambient_max img amb mxImg mxAmb hsub hImgMem hAmbUB) hAmb

/-! ## (ii) Moment normalization identity — `lem:moment-normalization` -/

/-- Cleared image moment numerator `L^{q-1}·P = M^q·Γ_img(q)`
(`P = ∑_s|F_s|^q = listSumPow q f`). -/
def momImgN (q L : Nat) (f : List Nat) : Nat := L ^ (q - 1) * listSumPow q f

/-- Cleared ambient moment numerator `A^{q-1}·P = M^q·Γ_amb(q)`; the same `P` as the
image side, because the ambient `y∉𝒮` terms vanish (`ambient_sum_reduces`). -/
def momAmbN (q A : Nat) (f : List Nat) : Nat := A ^ (q - 1) * listSumPow q f

/-- The cleared image numerator faithfully models the tex `L⁻¹∑_s(|F_s|/N̄)^q`: it is
the honest per-fiber cleared summation `∑_s(|F_s|·L)^q` divided by the average
weight `L`, i.e. `L · momImgN = ∑_s(|F_s|·L)^q`.  (`|F_s|·L` is `(|F_s|/N̄)^q`'s
numerator cleared of `M^q`, since `N̄ = M/L`.) -/
theorem momImgN_scaled (q L : Nat) (f : List Nat) (hq : 1 ≤ q) :
    L * momImgN q L f = listSumPow q (f.map (· * L)) := by
  unfold momImgN
  rw [listSumPow_map_mul, ← Nat.mul_assoc]
  congr 1
  rw [Nat.mul_comm, ← Nat.pow_succ]
  congr 1
  omega

/-- The cleared ambient numerator faithfully models the tex `A⁻¹∑_y(|·|/(M/A))^q`:
`A · momAmbN = ∑_{y∈G}(|Ω∘∩Φ⁻¹(y)|·A)^q`, over the ambient list `f ++ 0…0`
(`k = A - L` empty fibers). -/
theorem momAmbN_scaled (q A L : Nat) (f : List Nat) (hq : 1 ≤ q) :
    A * momAmbN q A f = listSumPow q ((f ++ List.replicate (A - L) 0).map (· * A)) := by
  unfold momAmbN
  rw [ambient_sum_reduces q A (A - L) hq, ← Nat.mul_assoc]
  congr 1
  rw [Nat.mul_comm, ← Nat.pow_succ]
  congr 1
  omega

/-- **(B1) `lem:moment-normalization`, identity (summation form).**  The two moment
numerators, before the `1/L` and `1/A` averaging, in closed form:

* image side  `∑_{s∈𝒮}(|F_s|·L)^q = L^q·P`  (scale pull-out), giving
  `Γ_img(q) = L^{q-1}P/M^q`;
* ambient side `∑_{y∈G}(|Ω∘∩Φ⁻¹(y)|·A)^q = A^q·P` (pull-out **and** the `y∉𝒮` zeros
  vanish), giving `Γ_amb(q) = A^{q-1}P/M^q`.

Dividing the two closed forms yields `Γ_amb(q)/Γ_img(q) = (A/L)^{q-1}`.  The real
content — the `y∉𝒮` vanishing and the scale-to-the-`q` pull-out — lives here; the
resulting exact factor is `moment_normalization_ratio`. -/
theorem moment_normalization_identity (q A L : Nat) (f : List Nat) (hq : 1 ≤ q) :
    listSumPow q (f.map (· * L)) = L ^ q * listSumPow q f
    ∧ listSumPow q ((f ++ List.replicate (A - L) 0).map (· * A))
        = A ^ q * listSumPow q f :=
  ⟨listSumPow_map_mul q L f, ambient_sum_reduces q A (A - L) hq f⟩

/-- **(B1) `lem:moment-normalization`, the `(A/L)^{q-1}` factor (cleared).**  The
cross-multiplied exact identity `L^{q-1}·(M^q Γ_amb) = A^{q-1}·(M^q Γ_img)`, i.e.
`Γ_amb(q) = (A/L)^{q-1} Γ_img(q)` cleared of the positive `M^q`.  (Trivial once the
closed forms of `moment_normalization_identity` are in hand — which is the point:
after the counting-vs-normalized-measure bookkeeping, the factor is exactly
`(A/L)^{q-1}`.) -/
theorem moment_normalization_ratio (q A L : Nat) (f : List Nat) :
    L ^ (q - 1) * momAmbN q A f = A ^ (q - 1) * momImgN q L f := by
  unfold momAmbN momImgN
  rw [← Nat.mul_assoc, ← Nat.mul_assoc, Nat.mul_comm (L ^ (q - 1)) (A ^ (q - 1))]

/-! ## Direction statements — safe vs. `A/L`-bridged -/

/-- **Safe direction** (`lem:moment-normalization`, "an ambient upper bound is safe
to use as an image upper bound").  Since `L ≤ A`, `momImgN ≤ momAmbN`, i.e.
`Γ_img(q) = (L/A)^{q-1}Γ_amb(q) ≤ Γ_amb(q)` for `q ≥ 1`. -/
theorem momImg_le_momAmb (q A L : Nat) (f : List Nat) (hLA : L ≤ A) :
    momImgN q L f ≤ momAmbN q A f :=
  Nat.mul_le_mul_right _ (Nat.pow_le_pow_left hLA (q - 1))

/-- **Ambient moment upper bound ⇒ image moment upper bound** (the safe transfer):
any ceiling `B` on the ambient moment transfers to the image moment. -/
theorem image_upper_of_ambient_upper (q A L B : Nat) (f : List Nat) (hLA : L ≤ A)
    (hamb : momAmbN q A f ≤ B) : momImgN q L f ≤ B :=
  Nat.le_trans (momImg_le_momAmb q A L f hLA) hamb

/-- **Unsafe reverse direction** (`lem:moment-normalization`, "the reverse direction
is unsafe without a printed bound on `A/L`").  An image bound gives an ambient bound
`momAmbN ≤ D·momImgN` **only** with an explicit `A/L` bridge `D ≥ (A/L)^{q-1}`
(hypothesis `A^{q-1} ≤ D·L^{q-1}`).  With no such printed `D` the ambient moment is
unbounded — which is exactly why C9 is stated at image scale. -/
theorem momAmb_le_momImg_bridge (q A L D : Nat) (f : List Nat)
    (hbridge : A ^ (q - 1) ≤ D * L ^ (q - 1)) :
    momAmbN q A f ≤ D * momImgN q L f := by
  unfold momAmbN momImgN
  calc A ^ (q - 1) * listSumPow q f
      ≤ (D * L ^ (q - 1)) * listSumPow q f := Nat.mul_le_mul_right _ hbridge
    _ = D * (L ^ (q - 1) * listSumPow q f) := by rw [Nat.mul_assoc]

/-! ## `ass:image-normalized-sidon-input` — the C9 input, as a hypothesis

Following the spine's hypothesis-packaging pattern (BSG/quasicube in
`NoHighEnergy.lean`; the per-tolerance null rate `P` in `SigmaDiagonal.lean`), the
C9 Fourier/Sidon payment is packaged as a **predicate**, not proved: it is the
missing moduli-source theorem.  `heavy` lists the Sidon-heavy fiber counts
(`{s : Δ(F_s) ≤ e^{-σN}}`); `Budget = M^q·exp(o(Nq))` is the cleared subexponential
ceiling. -/

/-- **`ass:image-normalized-sidon-input`.**  The C9 input consumed downstream, stated
at image scale: the image-normalized Sidon-heavy moment `Γ^{sid}_{q,σ} =
L⁻¹∑_{Δ(F_s)≤e^{-σN}}(|F_s|/N̄)^q` is subexponential, in cleared form
`momImgN q L heavy ≤ Budget`. -/
def ImageNormalizedSidonPaid (q L : Nat) (heavy : List Nat) (Budget : Nat) : Prop :=
  momImgN q L heavy ≤ Budget

/-- Ambient-scale Sidon-heavy payment (normalized by `M/A` over `G`), cleared. -/
def AmbientSidonPaid (q A : Nat) (heavy : List Nat) (Budget : Nat) : Prop :=
  momAmbN q A heavy ≤ Budget

/-- **The only safe way to consume an ambient C9 estimate.**  An ambient
Fourier/Sidon bound yields the image-normalized C9 input `ass:image-normalized-sidon-input`
via the safe transfer (`momImg_le_momAmb`) — formalizing #439's "*ambient moment
estimates can be consumed here only through `lem:ambient-image-max`,
`lem:moment-normalization`*".  No reverse implication is provided: an ambient
estimate does **not** license the image statement in the other direction without an
`A/L` bridge (`momAmb_le_momImg_bridge`). -/
theorem imageSidon_of_ambient (q A L : Nat) (heavy : List Nat) (Budget : Nat)
    (hLA : L ≤ A) (hAmb : AmbientSidonPaid q A heavy Budget) :
    ImageNormalizedSidonPaid q L heavy Budget :=
  Nat.le_trans (momImg_le_momAmb q A L heavy hLA) hAmb

/-! ## Concrete sanity certificates (closed by kernel `decide`)

Image fibers `[2,1]` (`L=2`, `P=∑x_s²=5`) inside an ambient group of size `A=3`
(ambient list `[2,1]++[0] = [2,1,0]`), at `q=2`.  Then `momImgN = 2·5 = 10`,
`momAmbN = 3·5 = 15`, the closed forms are `∑(x·2)² = 20 = 2²·5` and
`∑(x·3)² = 45 = 3²·5`, the safe direction is `10 ≤ 15`, and the cleared
`(A/L)^{q-1}` factor is the exact `2·15 = 3·10` (`L·Γ_amb = A·Γ_img`, i.e.
`Γ_amb/Γ_img = 3/2 = (A/L)^{2-1}`). -/
theorem normalization_example :
    momImgN 2 2 [2, 1] = 10
    ∧ momAmbN 2 3 [2, 1] = 15
    ∧ listSumPow 2 ([2, 1].map (· * 2)) = 2 ^ 2 * listSumPow 2 [2, 1]
    ∧ listSumPow 2 (([2, 1] ++ List.replicate (3 - 2) 0).map (· * 3))
        = 3 ^ 2 * listSumPow 2 [2, 1]
    ∧ momImgN 2 2 [2, 1] ≤ momAmbN 2 3 [2, 1]
    ∧ 2 * momAmbN 2 3 [2, 1] = 3 * momImgN 2 2 [2, 1] := by decide

end AsymptoticSpine
