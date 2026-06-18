I'll start by reading the file index, then work through the required files in order.I'll read the mandatory files in order. Let me batch the independent reads.Now the two specified audit files.Now the upstream tex sections. Codex audit gives line anchors for slackMCA: def:residue ~1189, thm:normalform ~1197, prob:perfiber ~1227. Let me read those and locate conj:B and prob:F1.I have def:residue, thm:normalform, prob:perfiber, and conj:B. Now prob:F1 in the blueprint (around line 471).## Files read

I've read the file index and the seven mandated sources: `ACTIVE_WALLS.md`, `BANKED_LEMMAS.md`, `CUTS_AND_FALSE_ROUTES.md`, the two Cycle‑2 audits, `def:residue`/`thm:normalform`/`prob:perfiber`/`conj:B` in `slackMCA_v3.tex`, and `prob:F1` in `proximity_blueprint_v3.tex`. I did not re-derive the banked paired-readout factorization; I checked it and use it as given.

The decisive computation is in `def:residue`: a witness is *noncontained* iff no $A,G\in F_{<k}[X]$ satisfy $A=w/E$ and $G=-B/E$ on $S$. I traced what this predicate does at the two scales that matter (the $a$-subset used by the readout, $a=k+t$, versus the witness support $|S_z|\ge s_\delta=\lceil(1-\delta)n\rceil$). That trace forces the classification below.

---

```text
Final classification: EXACT_NEW_WALL

Object:
W-F1-AA-AGR — "agreement-rigidity invariant for the paired base readout."
The first missing invariant is NOT a slope-image bound; it is a high-agreement
collision classification for S |-> (interp_S(w0), interp_S(w1)) on a-subsets,
i.e. the arbitrary-base-anchor paired analogue of slackMCA_v3.tex:thm:rigidcyclo
that feeds prob:perfiber. Noncontainment is shown to be the wrong filter.

Short verdict:
After tangent/contained separation (i.e. [Bnum]_E != 0 and z != 0), def:residue
noncontainment is AUTOMATIC for every support of size >= a = k+t, so it filters
nothing among nondegenerate a-subset readouts; and it is UNCERTIFIABLE below size
k+1 (every support of size <= k is contained). Hence the certificate size is
Theta(n), not bounded, and the predicate the slope count must actually enforce is
not noncontainment but agreement-extendability nu(S) = |{x in D : interp_S(w)(x)
= w(x)}| >= s_delta. The bounded paired readout rho(S) in (B[X]/Ehat)^2
(B-dimension <= 4t) does not see nu. The first missing invariant is therefore a
rigidity statement linking rho (bounded) to nu (global), not a packing bound.
```

---

## Proof / wall (source-valid, with parameters)

Field separation kept throughout: `B = F_p` (generated/entropy field, `q_gen = p`); `F = F_{p^2}` (line/extension field, `q_line = p^2`); `q_chal` is **not** invoked (no protocol theorem); `D ⊂ B`; balanced `t = σ` with test case `t = 2`; `a = k+t`; radius `δ = 1-ρ-η`, so `s_δ = ⌈(1-δ)n⌉ = k + ⌈ηn⌉`. The datum is `(E, Bnum, w)` from `def:residue`, `β := [Bnum]_E ∈ F[X]/(E)`, `Ehat = lcm(E, E^τ) ∈ B[X]`, `deg Ehat ≤ 2t`.

### Lemma A (Certificate-size lemma — provable, banked support).

Fix a degree-`t` datum with `β ≠ 0` and a slope `z ≠ 0`.

**(A1) Automatic noncontainment at scale `a`.** Let `S` be any support with `|S| ≥ a = k+t` on which `w` restricts to a polynomial `Q_z := interp_S(w)` of degree `< a` with `Q_z ≡ zβ (mod E)`. Then the witness `(Q_z, S)` is noncontained.

*Proof.* Suppose the anchor were explained: `A ∈ F_{<k}[X]`, `AE = w = Q_z` on `S`. Both sides have degree `< k+t = a ≤ |S|`, so `AE = Q_z` identically, giving `E | Q_z`, i.e. `[Q_z]_E = zβ = 0`. Since `z` is a unit in `F` and `β ≠ 0` in `F[X]/(E)`, this is impossible. Suppose the direction were explained: `G ∈ F_{<k}[X]`, `GE = -Bnum` on `S`. Then `GE + Bnum` has degree `≤ a-1 < |S|` and vanishes on `S`, so `GE + Bnum = 0`, forcing `E | Bnum`; but `deg Bnum < t = deg E`, so `Bnum = 0`, contradicting `β ≠ 0`. Containment requires **both** explanations; both fail. ∎

**(A2) Forced containment below scale `k+1`.** For any `S'` with `|S'| ≤ k`, the restricted datum is contained: `w/E` and `-Bnum/E` are arbitrary `F`-valued functions on `≤ k` points, each interpolated by some degree-`< k` polynomial `A, G`. Hence the witness restricted to `S'` is contained.

**(A3) Certificate window.** Combining (A1)–(A2): the minimal support size at which noncontainment can be certified lies in `[k+1, k+t]`. It is `Θ(n)` (since `k = ρn`), never `o(k)`. In the window `[k+1, k+t-1]` certification is conditional on the top divided difference of `-Bnum/E` (equivalently `w/E`) being nonzero; at `|S| ≥ a` it is unconditional. ∎

**Consequence.** *Noncontainment cannot be certified by a bounded-size sub-support.* This answers the prompt's central decision in the **negative**, with an explicit obstruction (A2): every sub-support of size `≤ k` is contained.

### Why this re-targets the wall.

(A1) says that **after the tangent/contained separation the wall already presupposes** (`β ≠ 0`, `z ≠ 0`), noncontainment holds for *every* nondegenerate `a`-subset readout. So among the readouts `ρ(S)` with `S` an `a`-subset, the noncontainment predicate is constant (true). It removes **zero** slopes. The banked caveat 3 ("a subset of a noncontained support may become contained") is therefore correct only in the degenerate strata (`β` a genuine zero divisor in a reducible `E`, or `z = 0`, or quotient-periodic `E`); in the nondegenerate balanced quadratic case it is vacuous. The thing that is genuinely lost on shrinking is not noncontainment but the **agreement count**.

### The operative invariant the readout forgets.

A genuine MCA bad slope needs a witness with `|S_z| ≥ s_δ = k + ⌈ηn⌉`. Since `t = σ` is constant (test case `2`) and `η` is a positive constant scale, `s_δ = k + Θ(n) ≫ a = k + t`. For an `a`-subset `S ⊆ S_z`, `Q_z = interp_S(w)` is **forced** (degree `< a`, agrees with `w` on `S_z ⊇ S`), so `[interp_S(w)]_E = zβ ∈ Fβ`: the readout lands on the bad line and recovers `z` (uniquely, by banked caveat 2). Thus

```text
{genuine bad slopes}  ⊆  {z : ∃ a-subset S, ρ(S) ∈ Fβ}.        (overcount, safe)
```

But the converse fails exactly as the readout cannot measure agreement. Define

```text
nu(S) = |{x in D : interp_S(w)(x) = w(x)}|   (global agreement of the forced interpolant).
```

An `a`-subset `S` with `ρ(S) ∈ Fβ` gives a noncontained witness (by A1) and a slope `z`, but `z` is a *genuine* bad slope only if `nu(S) ≥ s_δ`. The map `S ↦ ρ(S)` lands in `(B[X]/Ehat)^2`, of `B`-dimension `2 deg Ehat ≤ 4t` (banked caveat 4); it is invariant under replacing `S` by any other `a`-subset of the same forced interpolant. **`nu` does not factor through `ρ`:** two `a`-subsets with identical readout (hence identical slope) can have forced interpolants of wildly different agreement, and a slope may be carried only by low-`nu` (spurious) readouts. Consequently the only slope bound the readout supplies on its own is the trivial `|Fβ| ≤ q_line = p^2` (or `≤ p^{4t}` from the readout image), which is `poly(p)` — useless against the target `n^{1+o(1)}` because `p` may be `2^{o(n)}`.

### Statement of the new wall.

```text
W-F1-AA-AGR (first missing invariant):
Provide a rigidity/collision classification for the paired base interpolation map
   S |-> (interp_S(w0) mod Ehat, interp_S(w1) mod Ehat)   on a-subsets of D,
that controls agreement, not just residue. Concretely: bound the number of
distinct z in F for which some a-subset S has
   [interp_S(w)]_E = z beta   AND   nu(S) >= s_delta,
after the quotient-periodic locus (rem:aper: E a pullback through x|->x^M,
M | gcd(n,k), M>1) is removed. Equivalently, classify the high-agreement
collisions: if a-subsets S, S' both satisfy nu >= s_delta and land on the common
line F*beta, show their slopes coincide unless interp_S(w) - interp_S'(w) is
forced into a controlled (quotient-periodic / antipodal-type) family, i.e.
Ehat | (interp_S(w) - interp_S'(w)) modulo an F-scalar with residual difference
in that family.
```

This is strictly sharper than "prove slope-image packing," and strictly inside the project's existing dependency structure: it is the **arbitrary-base-anchor paired analogue of `thm:rigidcyclo`** (which classifies prefix collisions of `e_1` as antipodal-pair rearrangements and is the engine behind the exact count `thm:exactcount` and the open core `prob:perfiber`). The monic-locator case is the special collapse where `interp_S(w)` reduces to the symmetric-function prefix `Φ_σ(S)=(e_1,…,e_σ)` and the needed rigidity is exactly `thm:rigidcyclo`; W-F1-AA-AGR asks for the version with two arbitrary base words `w0,w1` and modulus `Ehat`. No such rigidity is in the banked set, and `prob:perfiber` itself (its monomial special case) is the unproved open core, so this is the genuine first gap.

### Strict, useful conditional reduction (the bankable kernel).

W-F1-AA reduces to W-F1-AA-AGR **plus** `prob:perfiber`-type collision control, via:

```text
#{genuine bad slopes after separation}
   <= #{distinct z : exists a-subset S with rho(S) in F*beta and nu(S) >= s_delta}.
```

The right side is finite and well-posed; bounding it needs (i) Lemma A (done: noncontainment is automatic, so the only live filter is `nu ≥ s_δ`), and (ii) W-F1-AA-AGR (open: relate the bounded `ρ` to the global `nu`). Step (i) is a strict, source-valid simplification of the wall; step (ii) is the isolated missing object.

---

## Noncontainment audit

Exact statement on shrinking. For `β = [Bnum]_E ≠ 0` and `z ≠ 0` (the regime that survives tangent/contained separation), **noncontainment survives shrinking trivially and is therefore vacuous**: by Lemma A1 every support of size `≥ a` — in particular every `a`-subset of a genuine witness — is noncontained, and by Lemma A2 no support of size `≤ k` is. So noncontainment is a `Θ(n)`-scale property with certificate window `[k+1, k+t]`; it is neither preserved-and-meaningful nor lost on passing to an `a`-subset — it is automatically true at every size `≥ a` and hence carries no information about whether the `a`-subset extends to a genuine witness. The property that **is** lost on shrinking, and that the slope count must remember, is the global agreement `nu(S) ≥ s_δ`, which does not factor through the bounded readout `ρ(S)`. Therefore noncontainment cannot be certified by a bounded sub-support, and — more importantly — it is the wrong invariant: the slope-image count must remember larger supports through their agreement, not through noncontainment. This both confirms and sharpens banked caveat 3.

## What to bank

Bank Lemma A (certificate-size lemma) as `BANKABLE_LEMMA`: in the nondegenerate balanced quadratic datum (`β ≠ 0`, `z ≠ 0`), def:residue noncontainment is automatic at every support size `≥ a=k+t` and impossible to certify below size `k+1`, so the noncontainment certificate is `Θ(n)`-sized and vacuous as a slope filter. Bank `W-F1-AA-AGR` as the replacement `EXACT_NEW_WALL`: the first missing invariant is an agreement-rigidity/collision classification for the paired base interpolation map — the arbitrary-base-anchor paired analogue of `thm:rigidcyclo` feeding `prob:perfiber` — linking the bounded readout `ρ(S)` (B-dimension `≤ 4t`) to the global agreement `nu(S)`. Record that W-F1-AA reduces (strictly, via the safe overcount) to W-F1-AA-AGR plus prob:perfiber-style collision control, and that this is **not** `ass:extension-mca-lift`, a `q_chal` denominator saving, a list-decoding, or a line-decoding claim.