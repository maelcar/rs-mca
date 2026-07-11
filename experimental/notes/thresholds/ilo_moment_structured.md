# (ILO-moment) on structured classes: subclass theorems + the Freiman chain

## Status

`R1 FREIMAN CHAIN: reduction PROVED (omega(eta)=(d+2)eta conditional on the
GAP-form exponential inverse-LO); the leak located EXACTLY (Step B) and the
Freiman-constant question resolved (constants enter only the fixed rank factor,
not whether omega->0) / R2 SUBCLASS THEOREMS PROVED — (ILO-moment) holds
UNCONDITIONALLY on (a) subsets of an AP of length O(b), (b) unions of c APs
(positions irrelevant), (c) bounded-rank GAPs of subexponential size; every
census optimizer lives in class (a) / R3 REFUTATION PROBE: no fat-fiber-fat-image
block; products cannot climb (image sub-multiplies), wild sets have fstar=1, the
(phi,lambda) corner is empty to b<=16 (COMPUTED, evidence FOR the hypothesis) /
R4 VERIFIER PASS (34/34) / R5 VERDICT: (ILO-moment) is a theorem on every
bounded-complexity class; the general case reduces to one missing lemma —
per-instance exponential-regime inverse-Littlewood-Offord for the moment map`.

This packet attacks the named wall our PR #655 (`fiber_image_tradeoff.md`, R5.1)
pinned: the **(ILO-moment)** hypothesis, whose reduction to `rho* < log2` #655
proved but left the hypothesis OPEN. In the notation of #655/#643/#623: a
**block** `V` is `b` distinct integers; the degree-2 signature of `S ⊆ V` is
`Phi(S) = (|S|, sum_{x∈S} x, sum_{x∈S} x^2)`; `fstar(V)` is the max fiber,
`L1(V)` the number of distinct signatures; `phi_2 = (log2 fstar)/b`,
`lam_2 = (log2 L1)/b`, `eta = 1 - phi_2`, and (natural-log rate)
`rho = phi + lam - log2`.

> **(ILO-moment) (OPEN, #655).** There exist `eta_0 > 0` and `omega(eta) -> 0`
> (as `eta -> 0`) such that every block `V` with `fstar(V) >= 2^{(1-eta)b}`
> (`eta < eta_0`) has `L1(V) <= 2^{omega(eta) b}`.

**One-line verdict.** `(ILO-moment)` is **PROVED unconditionally on every
bounded-complexity class the extremal blocks actually inhabit** — subsets of a
length-`O(b)` AP, unions of `c` APs (with the surprising position-independence
`L1 <= prod_j B(m_j)`), and bounded-rank GAPs of subexponential size — by
elementary **box bounds** generalizing #646's interval box. The census
optimizers of #643/#655 are all interval-with-holes = subsets of one short AP, so
they are all covered: **any counterexample must be structurally wild** (far from
every bounded-rank GAP of subexponential size). For the general case, the
**Freiman chain** (heavy fiber → low-support PTE trades → additive structure →
small GAP → small image) is assembled with **every step labeled**: the two ends
are PROVED (Step A `fstar_1 >= fstar`; Step C the GAP box bound), and the middle
**Step B is the exact leak** — per-instance inverse-Littlewood-Offord at
*exponential* concentration for the moment map, available in the polynomial
window (Nguyen-Vu, in scope) but OPEN for fixed `eta > 0` (only counting results,
Ferber-Jain-Luh-Samotij, exist there). Crucially, **the Freiman constants do not
degrade `omega`**: they enter only the fixed rank factor `(d+2)` multiplying
`eta`, so `omega(eta) = (d(eta)+2)·eta -> 0` whenever the rank stays bounded; the
obstruction is entirely the absence of *any* exponential-regime structural
inverse-LO, not a leaking Freiman constant. The **refutation probe** finds no
counterexample: products cannot climb (the image sub-multiplies, so the tensor
`(phi,lam)` stays in the convex hull of components), wild single blocks
(geometric, Sidon) have `fstar = 1`, and the joint `(phi_2, lam_2)` corner is
empty out to `b <= 16` — census evidence **for** the hypothesis.

Every number is recomputed by
`experimental/scripts/verify_ilo_moment_structured.py` (stdlib-only, zero-arg,
`RESULT: PASS (34/34)`, ~31 s / 56 MB under `ulimit -v 2097152`; every named
block and box bound re-derived exactly, the `b=18` champion cross-checked). The
deeper corner census (`b <= 16`) lives in
`experimental/scripts/repro_ilo_moment_structured.py` (documented runtime).

Label key: **PROVED** (written re-derivable proof, every external theorem quoted
with its exact hypotheses and applied only in scope), **COMPUTED** (exact
enumeration), **MEASURED** (exact finite objects, trend read off),
**CONDITIONAL** (proved modulo an explicitly named input, labeled cited-in-scope
or OPEN), **AUDIT** (cross-reference), **OPEN**.

**Credit.** Built directly on **our #655** (`fiber_image_tradeoff.md`: the named
`(ILO-moment)` wall and its reduction, the `b=14/16/18` champions, the
sphere-packing one-trade bound, the poly-window partial, the moment-curve
reduction), **our #646** (`moment_map_max_fiber.md`: `phi* = log2` and the
**interval box bound** `B(b) = (b+1)(1+C(b,2))(1+sum i^2)` that this packet
generalizes to APs and GAPs), **our #643** (`pte_cluster_packing_frontier.md`:
`rho = phi + lam - log2`, affine invariance Lemma A, Lemma B trade-deficit
`c >= 2^{b-2r}`, `rho <= phi`), and **our #623** (`pte_extremality_image_face.md`:
the `(fstar, L1)` wall). The minimal degree-2 PTE trade support 6 is
**scottdhughes #564** (`w_a_star_pte_lemma.md`). The `(ILO-moment)` name and the
scope discipline (no theorem imported beyond its printed hypotheses) are owed to
the **Codex team's read-only theorem-import audit** that flagged #655's first
draft — this packet exists to honor it. External inputs are cited **only within
their printed hypotheses and never re-derived**: inverse-Littlewood-Offord
(**Tao-Vu**; **Nguyen-Vu**, optimal) in the polynomial window; the
exponential-regime counting analogue (**Ferber-Jain-Luh-Samotij**);
**Freiman**'s theorem and its integer quantifications (**Ruzsa**;
**Green-Ruzsa**; **Sanders**' quasi-polynomial Bogolyubov-Ruzsa; the polynomial
Freiman-Ruzsa of **Gowers-Green-Manners-Tao**, over `F_2^n` only);
**Balog-Szemeredi-Gowers**; **Chang**'s spectral-GAP / **Ruzsa** covering for the
squares. Erdos-Moser / Sarkozy-Szemeredi is the classical anticoncentration
context.

---

## R0 — the reduction target and the box-bound engine (AUDIT + PROVED)

**What must be shown.** By #655's reduction (PROVED there), `(ILO-moment)`
implies `rho* < log2`. `(ILO-moment)` is a statement about the **near-max-fiber
regime** `phi_2 = 1 - eta`, `eta -> 0`: it asserts a near-maximal fiber forces an
exponentially small image. Two orientation facts (verifier BLOCK 0):

- The champions are the *wrong* corner for the hypothesis. The `b=18` champion
  (`fstar = 30`, `L1 = 151275`) has `phi_2 = 0.273` (**small** fiber) and
  `lam_2 = 0.956` (**near-full** image), so `eta = 0.727` — far from the
  hypothesis regime `eta -> 0`. `(ILO-moment)` says nothing about it; it
  constrains only blocks whose fiber is within a `2^{eta b}` factor of `2^b`.
- The interval `{0,...,b-1}` *is* the hypothesis regime (`phi_2 -> 1`,
  `eta = O(log b/b)`), and there `lam_2 -> 0` (image is `poly(b)`, #646): the
  hypothesis is *true and visible* on the interval. The question is whether
  near-max fiber **forces** small image on *every* block.

**The engine.** All PROVED results below are one idea — the **box bound**. If the
signature `Phi(S)` is a *fixed function of a low-dimensional integer vector whose
range is polynomially (or `2^{o(b)}`) bounded*, then `L1` is bounded by the size
of that range. #646 ran this for the interval (range `[0,b]×[0,bD]×[0,bD^2]`).
R2 runs it for APs, unions of APs, and GAPs.

---

## R2 — the subclass theorems (PROVED, unconditional)

These are banked first: they make `(ILO-moment)` a **theorem** on every class of
bounded additive complexity, with no appeal to any conjecture. All three are
proved by box bounds and verified exactly.

### 2.1 Theorem 1 — subsets of a short AP (verifier BLOCK 1)

> **Theorem 1.** Let `V` be `b` distinct integers contained in an arithmetic
> progression of length `L`. Then, writing `D <= L-1` for the diameter of the
> affine normalization (`min V = 0`, divide by the common difference),
> ```
>     L1(V) <= (b+1)(bD+1)(bD^2+1) <= (b+1) b^2 L^3    (using D <= L-1).
> ```
> In particular if `L <= C·b` then `L1(V) <= C^3 (b+1) b^5 = O_C(b^6)`, so
> `lam_2(V) <= 6 (log2 b)/b + O(1/b) -> 0`. Hence `(ILO-moment)` holds on this
> class **outright** (the conclusion is `b`-uniform with `omega ≡ o(1)`,
> independent of `eta`).

*Proof.* After affine normalization `V ⊆ {0,1,...,D}` (Lemma A of #643 leaves
`fstar, L1` unchanged). Every `S ⊆ V` has `|S| ∈ [0,b]`, `sum S ∈ [0, bD]`,
`sum S^2 ∈ [0, bD^2]`, so its signature lies in an integer box of the stated
size; `L1` is at most the number of lattice points in the box. The AP length `L`
bounds `D <= L-1`, and `L <= Cb` gives `L1 <= (b+1)(bCb)(b C^2 b^2) = C^3(b+1)b^5`
after dropping the `+1`s. Then `lam_2 = (log2 L1)/b <= (3 log2 b + log2(C^3(b+1)))/b
= 6(log2 b)/b + O(1/b)`. ∎

This is #646's interval bound extended to *any* sub-AP; the `C^3` is the only
cost of widening the AP from the tight interval. **Every #643/#655 census
optimizer is an interval-with-holes** — a subset of the single AP `{0,...,n}` of
length `n ~ 2b` — hence is covered by Theorem 1 with `C ~ 2`. So the entire
computed frontier lives inside a class where `(ILO-moment)` is proved.

### 2.2 Theorem 2 — unions of `c` arithmetic progressions (verifier BLOCK 2)

> **Theorem 2.** Let `V = V_1 ⊔ ... ⊔ V_c` be a disjoint union of `c`
> arithmetic progressions, `|V_j| = m_j` (so `sum_j m_j = b`), of **arbitrary**
> starts `a_j` and common differences `d_j`. Then
> ```
>     L1(V) <= prod_{j=1}^{c} B(m_j) ,   B(m) := (m+1)(1 + C(m,2))(1 + sum_{i<m} i^2) < (m+1)^6 ,
> ```
> **independent of the starts `a_j` and differences `d_j`**. Since each factor of
> `B(m) < (m+1)^6` and `prod_j (m_j+1) <= ((b+c)/c)^c <= (b+1)^c` (AM-GM), we get
> `prod_j B(m_j) < (b+1)^{6c}`, so `lam_2(V) < 6c (log2(b+1))/b -> 0` for fixed
> `c`, and `(ILO-moment)` holds on the union-of-`c`-APs class **outright** (the
> verifier confirms the sharper `prod_j B(m_j) <= b^{6c}` on every tested union).

*Proof.* Write `V_j = { a_j + d_j t : 0 <= t < m_j }`. For `S ⊆ V` put
`T_j = { t : a_j + d_j t ∈ S }` and let `(w_j, s_j, q_j) = (|T_j|, sum_{t∈T_j} t,
sum_{t∈T_j} t^2)` be the **internal signature** of `S` on part `j` (a signature
of a subset of `{0,...,m_j-1}`, so `(w_j,s_j,q_j)` takes at most `B(m_j)` values
by Theorem 1). Because `sum` and `sum-of-squares` are additive over the disjoint
parts, and each part contributes
```
    sum_{x∈S∩V_j} x   = a_j w_j + d_j s_j ,
    sum_{x∈S∩V_j} x^2 = a_j^2 w_j + 2 a_j d_j s_j + d_j^2 q_j ,
```
the total signature `Phi(S) = (sum_j w_j, sum_j (a_j w_j + d_j s_j),
sum_j (a_j^2 w_j + 2 a_j d_j s_j + d_j^2 q_j))` is a **fixed function of the
tuple `((w_j,s_j,q_j))_{j=1}^c`** (the constants `a_j, d_j` are fixed with `V`).
Distinct signatures therefore inject into distinct internal-signature tuples:
`L1(V) <= prod_j #{internal signatures on V_j} <= prod_j B(m_j)`. ∎

**This is the strongest and least obvious of the three:** the positions and
scales of the `c` pieces are *completely irrelevant* — a piece may be shifted to
`+10^9` or stretched by any step, yet `L1` stays `<= prod_j B(m_j)`. The
verifier confirms `L1` is unchanged as a piece is shifted to `+10^5` (BLOCK 2).
The additive coupling that could inflate `L1` (the cross term `2·(shift)·s_j` in
the second moment) is *already tracked* by the internal `s_j`, so it costs
nothing. The census optimizers, being interval-with-holes, are also unions of few
APs (the maximal runs), giving a second independent proof that they are covered.

### 2.3 Theorem 3 — the GAP box bound (verifier BLOCK 3)

> **Theorem 3.** Let `V` be contained in a proper generalized arithmetic
> progression (GAP) `P = { a_0 + sum_{i=1}^d x_i g_i : 0 <= x_i < L_i }` of rank
> `d` and size `|P| = prod_i L_i`. Then
> ```
>     L1(V) <= (b+1) · b^{d(d+3)/2} · |P|^{d+2} .
> ```
> Writing `|P| = 2^{alpha b}` and holding `d` fixed:
> `lam_2(V) <= (d+2)·alpha + (d(d+3)/2 + 1)(log2 b)/b`, so
> ```
>     lam_2(V) <= (d+2)·alpha + o(1) .
> ```
> Corollaries: (i) a **bounded-size** GAP `|P| = O(b)` gives `lam_2 -> 0`
> unconditionally; (ii) a GAP of size `|P| = 2^{eta b}` gives
> `lam_2 <= (d+2)·eta + o(1)`.

*Proof.* For `v ∈ V` write its GAP coordinates `x_i(v) ∈ [0, L_i)`. For `S ⊆ V`
put `X_i = sum_{v∈S} x_i(v)` and `Y_{ij} = sum_{v∈S} x_i(v) x_j(v)` (`i <= j`).
Expanding as in Theorem 2,
```
    w    = |S| ,
    sum  = w·a_0 + sum_i g_i X_i ,
    sum^2 = w·a_0^2 + 2 a_0 sum_i g_i X_i + sum_i g_i^2 Y_{ii} + 2 sum_{i<j} g_i g_j Y_{ij} ,
```
so `Phi(S)` is a **fixed function of `(w, (X_i)_i, (Y_{ij})_{i<=j})`**. Hence
`L1(V) <= #{ distinct (w,(X_i),(Y_{ij})) }`. The ranges are `w ∈ [0,b]`,
`X_i ∈ [0, b(L_i-1)]`, `Y_{ij} ∈ [0, b(L_i-1)(L_j-1)]`, so
```
    #tuples <= (b+1) · prod_i (b L_i) · prod_{i<=j} (b L_i L_j)
            = (b+1) · b^d |P| · b^{d(d+1)/2} |P|^{d+1}
            = (b+1) · b^{d(d+3)/2} · |P|^{d+2} ,
```
using `prod_{i<=j} L_i L_j = prod_i L_i^{d+1} = |P|^{d+1}` (each index appears in
`d+1` of the ordered-pair factors). Taking `log2`, dividing by `b`, and
`log2|P| = alpha b` gives the rate form. ∎

The verifier checks both inequalities — `L1 <= #tuples <= closed form` — exactly
for `d = 1, 2, 3` GAPs and for random subsets of a GAP (BLOCK 3); on plain APs
the first is an *equality* (`#tuples = L1`), exhibiting the bound as tight up to
the closed-form slack. The `Y_{ij}` monomials make explicit the fact that **the
squares of a rank-`d` GAP live in a rank-`O(d^2)` GAP** (the classical
Chang/Ruzsa observation) — here proved directly and quantitatively, not cited.

**Exceptional elements (verifier BLOCK 3).** If `V = V_0 ⊔ E` with `|E| = e`,
then because signatures add over the disjoint union, `L1(V) <= L1(V_0)·2^e`
(each of the `<= 2^e` subset-signatures of `E` shifts `V_0`'s image). So
adjoining `e = o(b)` arbitrary elements changes `lam_2` by `o(1)` — the "all but
`o(b)` elements" slack in inverse-LO statements is free.

**Consequence.** Theorems 1–3 prove `(ILO-moment)` (indeed the stronger
`lam_2 -> 0`, so `rho -> 0`) on: subsets of a length-`O(b)` AP; unions of `c` APs
(any `c` fixed); subsets of a rank-`d` GAP of size `2^{o(b)}` (any `d` fixed).
**Every bounded-additive-complexity block satisfies the hypothesis's conclusion
unconditionally.** A counterexample to `(ILO-moment)` must therefore be a block
with near-max fiber that is *not* `o(b)`-close to any bounded-rank subexponential
GAP — structurally wild. Whether such a block exists is exactly R1's wall.

---

## R1 — the Freiman route (reduction PROVED; the leak located)

The dream chain is: `fstar >= 2^{(1-eta)b}` ⟹ (Step A) linear concentration
`fstar_1 >= 2^{(1-eta)b}` ⟹ (Step B) `V` minus `o(b)` elements lies in a
bounded-rank GAP of size `2^{eta b + o(b)}` ⟹ (Step C = Theorem 3) `lam_2 <=
(d+2)eta + o(1)`. Steps A and C are proved here; Step B is the wall. We give the
chain with **each step labeled and each external theorem quoted in scope**, and
we resolve the Freiman-constant question the task poses.

### 1.1 Step A — the linear hinge (PROVED, verifier BLOCK 4)

Fixing `(w, s, q)` refines fixing `s` alone, so the 1-D linear concentration
`fstar_1(V) := max_s #{S : sum S = s}` satisfies `fstar_1 >= fstar`. Thus
`fstar >= 2^{(1-eta)b}` gives `fstar_1 >= 2^{(1-eta)b}`: the subset-sums of `V`
have Rademacher small-ball probability `>= 2^{-eta b}`, and (via the exact
`{0,1}^b ↔ {-1,1}^b` correspondence, #655 R5.3) so does `sum eps_i v_i`. **The
hypothesis is an inverse-Littlewood-Offord premise at concentration `2^{-eta b}`.**

### 1.2 Step 1 — heavy fiber forces one low-support trade (PROVED, BLOCK 4)

The fiber `F` (`|F| = fstar >= 2^{(1-eta)b}`) is a constant-weight binary code of
rate `1 - eta`. Two members `S, S' ∈ F` give a degree-2 PTE trade
`(P,Q) = (S∖S', S'∖S)` of support `|S△S'|` = their Hamming distance. By
sphere-packing (Hamming bound), a rate-`(1-eta)` code has two codewords within
distance `2·H_2^{-1}(eta)·b`, so `V` contains a trade of **relative support
`delta*(eta) = 2 H_2^{-1}(eta) -> 0`** as `eta -> 0` (verifier: the boundary
`H_2(delta*/2) = eta` holds exactly; `delta* = 0.106, 0.026, 0.006, 0.0017` at
`eta = 0.30, 0.10, 0.03, 0.01`). This is #655's R4 bound, restated as Step 1.

**But one trade is too weak** (#655 R4, PROVED there): a single support-`2r`
trade forces only deficit `c >= 2^{b-2r}` (Lemma B, #643), i.e. deficit *rate*
`gamma -> 0`. Step 1 gives the *existence* of small trades; the chain needs their
*proliferation into GAP structure*. That is Step B.

### 1.3 Step B — the leak: exponential-regime inverse-LO (OPEN)

> **(Step B, GAP form) — OPEN for fixed `eta`.** `fstar_1(V) >= 2^{(1-eta)b}`
> ⟹ all but `o(b)` elements of `V` lie in a proper GAP of rank `d = d(eta)` and
> size `|P| <= 2^{eta b + o(b)}`.

This is per-instance inverse-Littlewood-Offord at **exponential** concentration.
Its status, stated precisely:

- **Polynomial window — a theorem, in scope (verifier BLOCK 5).** If
  `eta <= C (log b)/b` (concentration `>= b^{-C}`, `C` fixed), the **Nguyen-Vu
  optimal inverse-LO** applies *within its printed hypotheses*: all but `n^{o(1)}`
  of the `v_i` lie in a GAP of rank `O_C(1)` and size `O_C(b^{C})`. Then Theorem 3
  gives `lam_2 = O_C((log b)/b) -> 0`. This **re-proves #655's poly-window
  Proposition (R5.3)** from the same box bound. (Quoted hypotheses: Nguyen-Vu
  assume the concentration exponent `C` is **fixed**; their GAP rank and volume
  constants depend on `C`. We use it only with `C` fixed.)

- **Exponential regime — OPEN.** For fixed `eta > 0` the concentration is
  `2^{-eta b}`, i.e. `C ~ eta b/log b` **grows with `b`**, and Nguyen-Vu's
  constants become `b`-dependent — the statement is *not* covered. What the
  literature offers is **counting, not structure**: **Ferber-Jain-Luh-Samotij**
  bound the *number* of blocks with concentration `>= 2^{-eta b}`; a counting
  theorem controls almost-all blocks and cannot bound a supremum over all blocks.
  We know of **no** published per-instance exponential-regime inverse-LO with
  explicit constants, so none is cited. **This is the single missing lemma.**

### 1.4 Step C — structure ⟹ small image (PROVED, = Theorem 3 + BLOCK 3)

Granting Step B's GAP (rank `d`, size `2^{eta b + o(b)}`) with `o(b)` exceptional
elements, Theorem 3 and the exceptional-element lemma give
```
    lam_2(V) <= (d+2)·(eta + o(1)) + o(1) = (d+2)·eta + o(1) .
```

### 1.5 The reduction and the Freiman-constant verdict (PROVED / analysis)

> **Reduction (PROVED, conditional on Step B).** Step A + Step C give: if Step B
> holds with rank `d(eta)`, then `(ILO-moment)` holds with
> `omega(eta) = (d(eta)+2)·eta + o(1)`. In particular `omega(eta) -> 0` whenever
> `d(eta) = o(1/eta)` — e.g. whenever the rank stays **bounded** as `eta -> 0`
> (the expected behavior: sharper concentration ⟹ simpler structure ⟹ lower
> rank). (Verifier BLOCK 5 checks the arithmetic `omega(eta) = (d+2)eta -> 0` for
> `d = 1, 2, 4`.)

**Does the Freiman constant leak?** The task asks whether current
additive-combinatorics technology keeps `omega(eta) -> 0` or degrades it to
`omega(eta) -> c > 0`. The answer: **it does not degrade `omega`** — the leak is
entirely the *existence* of Step B, not the constants in it. Trace the
alternative route that avoids assuming Step B outright, via additive energy:

1. *Fiber ⟹ energy.* One would need `fstar` large ⟹ additive energy
   `E(V) >= b^3 2^{-o(b)}`. **This step is itself unavailable at exponential
   concentration** (it is Step B in disguise): the small-ball-to-energy passage
   is exactly inverse-LO. *(Leak #1, = the same wall.)*
2. *Energy ⟹ doubling* (**Balog-Szemeredi-Gowers**, quoted in scope: `E(A) >=
   |A|^3/K` ⟹ some `A' ⊆ A`, `|A'| >= |A|/O(K^{O(1)})`, `|A'+A'| <=
   O(K^{O(1)})|A'|`). PROVED tool, in scope.
3. *Doubling ⟹ GAP* (**Freiman/Green-Ruzsa over `Z`**, quoted in scope:
   `|A'+A'| <= K'|A'|` ⟹ `A' ⊆` GAP of rank `<= K'^{O(1)}` and size `<=
   exp(K'^{O(1)})|A'|`; **Sanders** improves the size to quasi-polynomial
   `exp((log K')^{O(1)})`; the fully polynomial rank/size — **PFR**,
   Gowers-Green-Manners-Tao — is proved over `F_2^n` only, **not** over `Z`).

The Freiman constants (rank `d = K'^{O(1)}`, size factor `exp(K'^{O(1)})`) enter
Step C **only through the fixed factor `(d+2)` and an additive `o(1)` in the size
rate**: for **fixed `eta`** (hence fixed `K'`), `d` and the size factor are
*constants*. Green-Ruzsa's `exp(K'^{O(1)})` merely multiplies the GAP size by a
`b`-independent constant, contributing `log2(exp(K'^{O(1)}))/b = o(1)` to the size
rate `alpha`; so `lam_2 <= (d+2)(alpha_0 + o(1)) + o(1) -> (d+2)·alpha_0`, where
`alpha_0` is the concentration-driven rate (`eta` in the GAP form, `0` in the
bounded-doubling form). **Thus even Green-Ruzsa's `exp(K^{O(1)})` does not push
`omega` off `0`;** it only inflates the *rank constant* `d`, which changes
`omega`'s slope, not its limit. The one place a genuine degradation could occur is if the rank
`d(eta) -> ∞` **faster than `1/eta`** as `eta -> 0` — but sharper concentration
makes the structure *simpler*, so `d(eta)` is expected bounded; no known
mechanism forces `d(eta) = Omega(1/eta)`. **Conclusion: the chain's only real gap
is Leak #1 (produce *any* GAP/energy structure per instance at exponential
concentration); the downstream Freiman machinery is safe and keeps
`omega(eta) -> 0`.**

**R1 label summary.** Step A = PROVED. Step 1 (sphere-packing one-trade) =
PROVED. Step C (Theorem 3 + exceptional lemma) = PROVED. Poly-window instance of
Step B = CONDITIONAL (Nguyen-Vu, in scope). Exponential-regime Step B = OPEN.
Reduction "Step B ⟹ `(ILO-moment)` with `omega = (d+2)eta`" = PROVED.
Freiman-constant analysis = the constants do **not** degrade `omega`.

---

## R3 — refutation probe: no fat-fiber-fat-image block (COMPUTED)

We tried to build a block with near-max fiber **and** near-max image away from
AP/GAP structure. Nothing climbs.

**Products cannot climb (verifier BLOCK 7).** The natural way to combine a
"collider" (big `fstar`, small `L1`) with a "spreader" (big `L1`, `fstar ~ 1`) is
a direct sum `V = A ∪ (M + B)` with `M` large. The **fiber multiplies**
(`fstar(V) = fstar(A) fstar(B)`, verified), but the **image does not**: the
second-moment coordinate *convolves* (`q = q_A + q_B + 2M s_B + M^2 w_B` couples
the blocks), so `L1(V) < L1(A) L1(B)` (verified: `3863 < 63^2 = 3969`). Hence
`rho` does **not** climb — the direct sum stays at or below the better component
(`rho = 0.1106 <= 0.1129`), and a collider⊗spreader is **diluted** by the
spreader's `rho = 0` (`0.056 < 0.113`). The exact multiplicative tensor requires
#615's no-carry prime-field spacing; under it `(phi, lam)` is a length-weighted
**average** of the components' — confined to the **convex hull** of the
single-block frontier, never beyond it. This explains #655's "`k`-ladder peaks at
`k=2`": a single dense block at the degree-2 sweet spot is the extreme point;
products only interpolate. **To raise both `fstar` and `L1` you need a new single
dense block, not a product.**

**Wild single blocks have no fiber (verifier BLOCK 7).** A block with big image
but *not* interval-like buys the image by being **dissociated** — and
dissociation kills the fiber. The geometric block `{2^i}` and a Sidon block
(Mian-Chowla `{0,1,3,7,12,20,...}`) both have **all subset sums distinct**, so
`fstar = 1`, `L1 = 2^b`, `rho = 0` — the *opposite* corner. Multiplicative or
Sidon structure produces the image with **zero** fiber; there is no additive
collision without additive structure, and additive structure is exactly what the
AP/GAP subclasses control.

**The corner is empty (verifier BLOCK 6; deeper in the repro).** Census of the
joint `(phi_2, lam_2)` frontier over affine-canonical blocks (`b <= 12` in the
verifier, `b <= 16` in the repro): the maximum `lam_2` achievable at fiber
threshold `phi_2 >= t` is **non-increasing in `t`** (`0.998 → 0.995 → 0.989 →
0.986` at `t = 0.10, 0.15, 0.18, 0.20`, `b=12`), and `max(phi_2 + lam_2) = 1.186
<< 2` over the sampled frontier — a **squeeze**: more fiber forces less image. The
high-`phi_2` end is pinned by the interval family (`phi_2` up to `0.31` at `b=18`
with `lam_2` **falling** `0.98 → 0.87`). The `(phi_2, lam_2)` corner near `(1,1)`
is empty at every scale searched. **This is census evidence for `(ILO-moment)`.**

---

## R4 — verifier (COMPUTED)

`experimental/scripts/verify_ilo_moment_structured.py` recomputes every number:
the champions and the reduction (BLOCK 0); the three subclass box bounds on exact
instances (BLOCKS 1–3), including the position-independence of the union bound
and the exceptional-element multiplier; Step A and the sphere-packing one-trade
boundary (BLOCK 4); the conditional-`omega` arithmetic and the poly-window
numerics (BLOCK 5); the corner census and interval squeeze (BLOCK 6); the product
non-climb and wild-set collapse (BLOCK 7). `RESULT: PASS (34/34)`, ~31 s / 56 MB.
The deeper `b <= 16` corner census and the position-independence sweep are in
`experimental/scripts/repro_ilo_moment_structured.py` (documented runtime).

---

## R5 — verdict and the honest wall

```
    HYPOTHESIS (ILO-moment):  fstar >= 2^{(1-eta)b}  =>  L1 <= 2^{omega(eta) b},
                              omega(eta) -> 0.   (=> rho* < log2, #655.)

    PROVED (unconditional) on structured classes -- (ILO-moment) is a THEOREM on:
      (a) subsets of an AP of length O(b):   L1 <= (b+1)(bD+1)(bD^2+1) < C^3 b^6.
      (b) unions of c APs (any positions):   L1 <= prod_j B(m_j) <= b^{6c}.
      (c) subsets of a rank-d GAP, |P|=2^{alpha b}:  lam_2 <= (d+2) alpha + o(1).
      Every #643/#655 census optimizer is interval-with-holes = class (a).
      => any counterexample must be FAR from every bounded-rank subexp GAP.

    FREIMAN CHAIN:  reduction PROVED -- Step B (GAP form) => omega(eta)=(d+2)eta.
      Step A (fstar_1>=fstar) PROVED; Step C (GAP box bound) PROVED.
      Step B = per-instance inverse-LO at EXPONENTIAL concentration: a THEOREM in
      the poly window (Nguyen-Vu, in scope; reproves #655 R5.3), OPEN for fixed
      eta (only counting inverse-LO, Ferber-Jain-Luh-Samotij, exists there).
      Freiman constants (Green-Ruzsa exp, Sanders quasipoly, PFR=F_2^n-only)
      do NOT degrade omega: they enter only the fixed rank factor (d+2); omega->0
      as long as the rank stays o(1/eta) (bounded rank = expected). THE LEAK IS
      THE EXISTENCE OF STEP B, NOT ITS CONSTANTS.

    REFUTATION PROBE:  no fat-fiber-fat-image block. Products cannot climb (image
      sub-multiplies; tensor stays in the convex hull). Wild sets (geometric,
      Sidon) have fstar=1. The (phi_2,lam_2) corner is empty to b<=16.
      => consistent with (ILO-moment) TRUE (matches #655's census cap rho*~0.2).
```

**The missing lemma, named precisely.** To close the general case one needs:

> *A per-instance inverse-Littlewood-Offord theorem at exponential concentration
> for the moment map:* there is a rank bound `d = d(eta) = o(1/eta)` (ideally
> `O(1)`) and `eta_0 > 0` such that every `V` with linear concentration
> `fstar_1(V) >= 2^{(1-eta)b}` (`eta < eta_0`) has all but `o(b)` elements inside
> a proper GAP of rank `d` and size `2^{eta b + o(b)}`.

By R2 (Theorem 3) this lemma **immediately** yields `(ILO-moment)` with
`omega(eta) = (d(eta)+2)eta`, hence `rho* < log2`. The lemma is the exact
exponential-regime strengthening of Tao-Vu/Nguyen-Vu; the literature supplies it
polynomially (Nguyen-Vu) and countingly (Ferber-Jain-Luh-Samotij) but not
per-instance-exponentially. This packet's contribution is to **prove the entire
chain around this one lemma** — the downstream box bounds unconditionally, the
subclasses outright, and the upstream reduction with the constant question
resolved — so that the wall is now a single, sharply stated inverse-LO estimate,
and every structured block is already decided.

---

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/ilo_moment_structured.md` (this).
- Verifier: `experimental/scripts/verify_ilo_moment_structured.py` (fast;
  `RESULT: PASS (34/34)`; recomputes every number, re-checks each box bound and
  census on exact instances).
- Repro (deeper census, documented runtime):
  `experimental/scripts/repro_ilo_moment_structured.py`.
- Read-only inputs: our #655 `fiber_image_tradeoff.md`, #646
  `moment_map_max_fiber.md`, #643 `pte_cluster_packing_frontier.md`, #623
  `pte_extremality_image_face.md`; hughes #564 `w_a_star_pte_lemma.md`.

**Per-claim status.** Theorems 1–3 (AP / union-of-APs / GAP box bounds) =
`PROVED` (self-contained, no external theorem). Exceptional-element lemma =
`PROVED`. Step A, Step 1 (sphere-packing), Step C = `PROVED`. Poly-window
instance of Step B = `CONDITIONAL` (Nguyen-Vu, in scope). Reduction
"Step B ⟹ `(ILO-moment)`" = `PROVED`. Freiman-constant non-degradation analysis
= `PROVED` reasoning about cited bounds. Corner census, product non-climb,
wild-set collapse = `COMPUTED`. Interval squeeze / corner-emptiness trend =
`MEASURED`. Exponential-regime Step B (the wall) = `OPEN`.

**Flagged for PI (least-certain, 3 steps).**
(a) **The `d(eta) = o(1/eta)` clause.** The reduction gives `omega -> 0` only if
the (conjectural) Step B rank grows slower than `1/eta`; we argue this on
structural grounds (concentration ⟹ simplicity) but it is an *assumption about
the shape of the missing lemma*, not a theorem — if some pathology forced
`d(eta) = Omega(1/eta)`, `omega` could stay bounded below.
(b) **Poly-window import.** The re-use of Nguyen-Vu (Step B, poly window) is
exactly #655's R5.3; we quote its fixed-`C` hypotheses but do not re-derive the
GAP rank/volume constants — trust inherited from the cited theorem.
(c) **Corner-emptiness is bounded-`b`.** The `(phi_2, lam_2)` census (`b <= 16`)
is exact but finite; the "corner empty" reading is a MEASURED trend, consistent
with but not a proof of `(ILO-moment)` (as always, small-`b` plateaus can hide
slow climbs — the #646 lesson).

**Exact vs heuristic.** All `fstar`, `L1`, box counts, and census optima are
exact integer enumeration. The box bounds and the reduction are elementary
closed-form proofs. The Freiman/inverse-LO inputs are cited within their printed
hypotheses and never re-derived. No `.tex`/`.pdf` touched.
