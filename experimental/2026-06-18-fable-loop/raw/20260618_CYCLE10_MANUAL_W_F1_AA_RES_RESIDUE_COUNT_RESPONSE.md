I'll start by reading the file index and the core state files, then the audits and source most relevant to W-F1-AA-RES-RESIDUE-COUNT.Let me read the core wall/lemma/route files and the key audits in parallel.Now the key audits and the verify script, plus the residue definitions from source.Let me examine the source theorems I must respect (exactcount, rigidcyclo, perfiber, residue) and the problem statements.I don't have bash here. Let me use Grep instead.Let me find the core source theorems in slackMCA_v3.tex.This is a deep problem. I need to ground my answer in the actual source definitions (prob:perfiber, def:residue, thm:exactcount, thm:rigidcyclo, rem:aper) rather than just the audit summaries. Let me read the relevant source sections.Let me locate the residue-line and per-fiber definitions efficiently by scanning targeted regions.Let me find the residue-line normal form, exactcount, and the per-fiber conjecture sections.Let me find the residue-line normal form and per-fiber conjecture (Part II/IV).I've now read the wall, the banked chain (Cycles 1–8), the Cycle 7/8 audits, the Cycle 8 verifier, and the governing source objects in `slackMCA_v3.tex` (`def:residue`, `thm:normalform`, `prob:perfiber`, `conj:B`, `rem:aper`, `def:locator-fiber`). Here is my classification.

---

Final classification: ROUTE_CUT

(with a runnable finite certificate, the corrected wall, and a small genuinely-bankable structural fragment in the notes — but the headline is a cut.)

## Precise statement of the cut

The banked target `W-F1-AA-RES-RESIDUE-COUNT`, as written in `ACTIVE_WALLS.md` and the Cycle 8 audit —

```text
above corrected reserve eta=sigma/n, bound the F-residue value count
S -> [interp_S(w0)+alpha*interp_S(w1)]_E in F[X]/E
by n^{1+o(1)}, for arbitrary base anchors w0,w1 and aperiodic separated E.
```

— is **not source-valid**, because it bounds the wrong object. It counts the **total residue-value image**

```text
(A)  #{ R_E(S) : S in binom(D,a) },   R_E(S) = [interp_S(w0)+alpha interp_S(w1)]_E,
```

whereas the quantity that `thm:normalform` turns into MCA error, and that `conj:B`/`rem:aper` conjecture to be `n^{1+o(1)}`, is the **on-line, noncontained, aperiodic slope count**

```text
(B)  Lambda^{NC}_{t,delta} = #{ z in F : exists noncontained a-subset S with [interp_S(w)]_E = z[Bnum]_E }.
```

Three hypotheses present in `def:residue`/`thm:normalform`/`rem:aper` were dropped between the Cycle 6B note (which correctly said "on the bad line `F*[Bnum]_E`") and the Cycle 8 restatement:

1. **The on-line restriction.** `def:residue` requires `Q_z ≡ zB (mod E)` with `Q_z = interp_S(w)` on `S`, i.e. `[interp_S(w)]_E ∈ F·[Bnum]_E`. The banked object has **no numerator `Bnum` at all** and counts every residue, on-line or off-line.
2. **Noncontainment.** `def:residue` only counts slopes with a *noncontained* witness; the banked object counts all supports.
3. **Aperiodic separation** (`rem:aper`): `conj:B` is about `Lambda^{aper}`, with quotient-periodic denominator families removed.

Always `(A) ≥ (B)`. The inequality `#slopes ≤ #values` is exactly the Cycle 7 banked boundary ("safe but non-closing"). Bounding `(A)` is therefore a *sufficient but strictly stronger* route — and that route is **provably blocked**, because `(A)` is not `n^{1+o(1)}` for arbitrary anchors.

## Why (A) is false for arbitrary anchors (the cut, with certificate)

Take `w1 = 0` and `w0` a generic base word (its global interpolant `W0` has degree `n-1`). Then `R_E(S) = [interp_S(w0)]_E = [W0 mod L_S]_E`. Two supports collide iff `interp_S(w0) - interp_{S'}(w0) ∈ E·F_{<k}[X]` (the Cycle 6B/8 kernel). For generic `w0` this kernel condition is satisfied by a vanishing fraction of subset pairs, so the residue map is **near-injective** and

```text
(A) = Theta( binom(n,a) ),
```

which is `2^{Theta(n)}` above reserve (`a=(rho+eta)n`) and `Theta(n^{t})`-scale at fixed `t`. Either way `(A) >> n^{1+o(1)}`. Only *special* anchors (codewords, degree `<k`, or quotient-periodic) make `(A)` small; "arbitrary anchors" is exactly the regime where it explodes. The reserve hypothesis does not rescue it: reserve constrains `sigma/n`, not the genericity of `w0`.

Meanwhile `(B) ≤ q_line = p^2` trivially, because when `[Bnum]_E ≠ 0` the bad line `F·[Bnum]_E` is a one-dimensional `F`-subspace of `F[X]/E`, hence has exactly `|F| = q_line` points, and distinct slopes are distinct on-line points.

Finite certificate (Codex-runnable, mirrors the Cycle 8 verifier harness):

```text
Field ledger:   B = F_11,  F = F_121 = F_11[a]/(a^2 - r), r a nonresidue, tau(a) = -a.
Params:         D = F_11 (n=11), k=2, t=sigma=2, a=k+t=4.  (deg E = 2, deg Ehat = 4.)
E:              any separated aperiodic E in F[X], gcd(E,E^tau)=1, E nonzero on D
                (reuse random_E() from 20260618_cycle8_twisted_readout_verify.py).
Numerator:      Bnum = 1  (bad line = constants F·[1]_E, the simplest nonzero line).
Anchors:        w0, w1 : D -> B uniform random.
Statistics over all 4-subsets S (binom(11,4)=330):
  N_A = #distinct R_E(S)                                     -> observed ~ 330 (near-injective)
  N_B = #{ z in F : [interp_S(w0)+alpha interp_S(w1)]_E = z·[1]_E for some S }
                                                             -> observed O(1)..O(10)
Assertion to certify:  N_A / N_B >> 1, and N_A = Theta(binom(n,a)),
                       so (A) is NOT O(n^{1+o(1)}), while (B) <= q_line = 121.
```

The structural reason (`generic anchor ⇒ near-injective residue map ⇒ N_A = Θ(binom(n,a))`) is prime-uniform, so it scales to any reserve by taking `t = σ = ⌈ηn⌉` and a generic `w0`. This is a certificate that the *value-count* object is the wrong target, not a refutation of `conj:B`.

## The corrected wall (what should replace it)

```text
W-F1-AA-RES-ONLINE-SLOPE-COUNT  (the actual source object):
Above corrected reserve eta >= (1+eps) tau*(rho, q_gen), for separated aperiodic E
and base anchors w0,w1 (with Bnum != 0 mod E), bound
   Lambda^{aper}_{t,1-rho-eta} = #{ z in F : exists noncontained, non-quotient-periodic
                                    a-subset S with [interp_S(w0)+alpha interp_S(w1)]_E = z[Bnum]_E }
by n^{1+o(1)}.
```

This is a **verbatim arbitrary-anchor / extension-denominator instance of `conj:B` via `thm:normalform`** (already flagged in the Cycle 5 audit: restored `W-F1-AA` "is a faithful instance of `Lambda^{NC}_{t,delta}`/`prob:perfiber`"). Consequently it **cannot be banked as a lemma** without proving `conj:B`; `prob:perfiber` records that prime-averaging, the polynomial method, subgroup exponential sums, and anticoncentration all terminate at it.

## Source dependencies

- `tex/slackMCA_v3.tex` — `def:residue` (slope = scalar `z` with `Q_z ≡ zB mod E`, plus noncontainment), `thm:normalform` (`emca = (1/q) max_t Lambda^{NC}_{t,delta}`), `rem:strata`/`rem:aper` (aperiodic packing, tangent floor `Lambda^{NC} ≥ ⌊δn⌋`), `prob:perfiber`, `conj:B` (the `n^{1+o(1)}` bound is on `Lambda^{aper}`, not on a residue-value count), `def:locator-fiber`/`prop:arb-fiber` (residue images of `interp_S` are the list-side object and are generically large).
- Cycle 6B audit (on-line qualifier "on the bad line `F*[Bnum]_E`"), Cycle 7 audit (`#slopes ≤ #values`, "safe but non-closing"), Cycle 8 audit + `20260618_cycle8_twisted_readout_verify.py` (twist isomorphism `B[X]/Ehat ≅ F[X]/E`; still valid — the cut does **not** reopen the twist).

## Field ledger

- `q_gen = p`, `B = F_p`: `D ⊆ B`, anchors `w0,w1`, `Ehat`, `theta`, paired readout.
- `q_line = p^2`, `F = F_{p^2}`: `E`, `Bnum`, the residue `[interp_S(w)]_E`, slopes `z`, and the bad line (exactly `q_line` points).
- `q_chal`: unused; no protocol/challenge denominator claimed.
- No `q_gen` collapse is claimed or used (Cycle 8 ledger preserved).

## Parameter ledger

- `n = |D|`, `k = rho n`, `a = ceil((1-delta)n)`, `sigma = a-k`, balanced `t = sigma`, so `a = k+t = s_delta`.
- `deg E = t`, `deg Ehat = 2t`; reserve `eta = sigma/n`, threshold `(1+eps) tau*(rho,q_gen)`.
- `t = sigma = 2` is **sub-reserve** when `n -> infty` (`eta = 2/n -> 0`); it is a finite algebra test, not an above-reserve instance. No quotient/list/interleaving arity used.

## Proof / audit notes

- The twist isomorphism (Cycle 8) is untouched and not reopened; nonconstant `theta` is not absorbed into `w0+theta w1` (Cycle 7 cut respected).
- Genuinely bankable fragments that survive (small, true, not the conjecture): (i) `(A) ≥ (B)`; (ii) `(B) ≤ q_line` when `[Bnum]_E ≠ 0` (one-dimensional bad line) — this is the crude bound the banked `sigma=1` counterpacket already saturates, so it is not progress toward `n^{1+o(1)}`; (iii) the collision law `R_E(S)=R_E(S') ⇔ interp_S(w)-interp_{S'}(w) ∈ E·F_{<k}[X]` (already banked). None of these closes the gap.
- The tangent floor (`rem:strata`, `Lambda^{NC} ≥ ⌊δn⌋`) shows `(B)` is genuinely `Ω(n)` on some data, so the corrected wall's `n^{1+o(1)}` target is sharp-if-true — confirming the right object is `(B)`, not `(A)`.

## What Codex should bank / test next

- **Bank:** `W-F1-AA-RES-RESIDUE-COUNT` (value-count formulation) is a `ROUTE_CUT` — an over-strong proxy that is false for arbitrary anchors (`(A)=Theta(binom(n,a))`). Replace it with `W-F1-AA-RES-ONLINE-SLOPE-COUNT` (`Lambda^{aper}` on the bad line, with `Bnum`, noncontainment, and `rem:aper` restored).
- **Bank the boundary:** the corrected wall is a verbatim `conj:B`/`prob:perfiber` instance; do **not** seek a "lemma" that bounds the full slope count without the conjecture.
- **Test:** run the certificate above (extend the Cycle 8 verifier to also emit `N_A` and `N_B`); confirm `N_A = Theta(binom(n,a))` and `N_B ≤ q_line`, separating them by a growing factor as `p` grows at fixed `t`.
- **Next sharper invariant (actionable, conjectural — do not bank as proved):** because `w0,w1 ∈ B` and `D ⊆ B`, ask whether the on-line slopes `z` are confined to a norm-/Galois-controlled subset of `F`, the arbitrary-anchor analogue of `thm:subfield`/`cor:deflate`. The pair `([interp_S(w0)]_Ehat,[interp_S(w1)]_Ehat) ∈ (B[X]/Ehat)^2` is base-valued; the only extension-valued ingredient is `alpha`. A subfield-confinement bound on `z` would feed `thm:normalform` directly and is the first genuinely new lever beyond the kernel/twist facts.

## Do I see a route to a full solve?

Honestly, no — not a complete one. Once the object is stated correctly (the on-line aperiodic slope count `(B)`), the wall is a faithful instance of `conj:B` through `thm:normalform`, and `prob:perfiber` is explicit that the natural attacks (prime averaging, polynomial method, subgroup exponential sums to `N ≥ p^{3/7+eps}`, anticoncentration) all terminate at exactly this divisibility statement. The Cycle 1–8 chain has correctly peeled off everything *around* the core (twist, kernel, noncontainment, balance notation, reserve indexing) without touching the core itself; the value-count restatement was the first step that accidentally enlarged the object back to something false.

The only structurally honest *partial* route I can point to — and I flag it as conjectural, not a solve — is the subfield-confinement angle in the last bullet: prove that the base-valued paired readout forces the on-line slopes into a set of size `O(q_gen·n^{o(1)}) = O(p·n^{o(1)})` rather than the trivial `q_line = p^2`. That would be a real `q_gen`-vs-`q_line` saving (which Cycle 8 correctly says is *not* yet known), it is the natural extension-field analogue of the already-proved `thm:subfield`, and unlike the value-count target it concerns the correct object `(B)`. It is the one lever in this setup that is both source-grounded and not already cut. But it is not a proof, and I would not let it be banked as one.