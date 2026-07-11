# Frame image-completion: magnitude route vs phase supplement (J2 decided)

## Status

`R1 CIRCULAR (PROVED) / R2 IMPOSSIBILITY WITNESS (PROVED) / SUPPLEMENT ROUTED`.

This is a **research packet**, not an audit: it settles, as a theorem either
way, the J2 interface gap that our audit **PR #608**
(`thresholds-character-frame-audit`) exposed in avdeev's integrated
character-frame certificate (**PR #558**,
`asymptotic_primitive_profile_character_frame_v1.md`, integrated at `e190193`).

**Headline (the honest, non-manufactured answer).** J2 is a **genuine gap, not
a one-line ledger fix**. The frame's magnitude-side hypotheses `(CF1)+(CF2)`
**cannot** deliver the image half `L >= e^{-o(N)} A_eff` of
`def:effective-fourier-payment` (EFP). The witness is **avdeev's own
block-parabola separation family**: it satisfies `(CF1)+(CF2)` *exactly*
(`K_{A_k}=I`, `|A_k| = p^k = L`, `kappa_frame = 1`) while
`L / A_eff = p^{-k} = e^{-Theta(N)}`. So the frame's showcase family --- the one
avdeev uses to beat global `(MI)+(MA)` --- is simultaneously the family that
proves the frame is **magnitude-blind to the image size**. The character frame
is therefore a **half-interface**: a valid alternative for the max-fiber
multiplier (EF4/EF5) at image normalization *only*, never for the image clause.

Every number below is recomputed by
`experimental/scripts/verify_frame_image_completion.py`
(stdlib-only, `RESULT: PASS (66/66)`, ~0.48 s under `ulimit -v 2097152`).

Label key: **PROVED** (hand derivation, exact), **MEASURED** (exact finite toy,
asymptotic claim not proved from the toy), **OPEN**.

Credit. The block-parabola construction and the `(CF1)/(CF2)/(CF3)` identities
are **avdeev's** (PR #558). The J2 gap is our audit **PR #608**. **PR #539**
(`fi_full_image_primitive.md`) is the Gap-1 corollary
`EF4 => image >= A_eff/kappa` this packet contrasts against; scottdhughes's
ambient signed `(LS)` (#564) is named as the phase-sensitive supplement route.

---

## Rung 1 --- OBJECT EXTRACTION

### 1.1 The frame's hypothesis set (avdeev #558, exact, with anchors)

Notation (frame note L47-52): `M=|Omega|` full-slice size; `S={Phi(x)-s0}` the
realized image; `L=|S|`; `mu(z)=|F_z|/M`; `barN=M/L`. Frontiers application
(L54): `G=V_g`, `|G|=A_eff`.

| id | statement | anchor | proof-status |
|----|-----------|--------|--------------|
| CF1 | `\|F_z\| <= M\|\|K_A\|\|_op/\|A\| = (L\|\|K_A\|\|_op/\|A\|) barN` (max-fiber Bessel bound) | note L83-86 | PROVED (avdeev) |
| CF2 | source-specific packing input: `\|A\| >= exp(-o(N)) L` **and** `\|\|K_A\|\|_op <= exp(o(N))` | note L92-93 | OPEN (avdeev's crux) |
| CF3 | converse guardrail `\|\|K_A\|\|_op >= \|A\| mu(z)`, hence `L\|\|K_A\|\|_op/\|A\| >= L max_z mu(z)` (magnitude-only) | note L140-148 | PROVED (avdeev) |
| full-dual | `\|\|K_{G^}\|\|_op = \|G\| max_z mu(z)` | note L156 | PROVED (avdeev) |
| CF4 | greedy packing `\|A\| >= \|G^\|/\|Mfrak\|` | note L176 | PROVED (avdeev) |
| CF5/CF6 | `\|Mfrak\| <= exp(o(N))\|G^\|/L`; minor Gram row-sum `<= exp(o(N))` | note L182-189 | OPEN (avdeev) |
| kappa_frame | finite certified image multiplier `kappa_frame = L B_A/\|A\|`, `B_A >= \|\|K_A\|\|_op` | note L205 | PROVED (avdeev) |

**Certificate quantifier structure.** The frame is: *there exists* a nonempty
`A subset G^` such that (CF2) holds; *for all* fibers `F_z`, (CF1) bounds
`|F_z|`. The reported certificate is the pair `(|A|, ||K_A||_op)` (equivalently
`kappa_frame`); it is a pure **operator-norm / magnitude** object. CF3 makes the
magnitude-only nature explicit: the frame can never certify a multiplier below
`L max_z mu(z)`, and the full-dual identity shows the whole-dual norm is itself
`|G| max mu`, not an independent proof of Q.

### 1.2 The target J2 (frontiers tex, exact quotes with anchors)

`def:effective-fourier-payment` (EFP, tex L2930-2953) bundles **two** outputs
from one hypothesis:

- **EF4 (max-fiber, tex L2941-2942):** `max_z N_g(z) <= kappa binom(|T|,m)/A_eff`.
- **image clause (tex L2944-2945):** *"It also implies that the realized image
  contains at least `A_eff/kappa` points."*

The EFP definition flags itself (tex L2947): *"`(EFP)` is **phase-dependent**
and does not pay an ambient annihilator twice."* Its "Proof of the image-size
assertion" (tex L2951-2955) is the pigeonhole `M = sum_z N_g(z) <= L*F_max`,
`F_max <= kappa M/A_eff`, hence `L >= A_eff/kappa`.

The load-bearing consumer is the effective-prefix-flatness / primitive-Q proof
(tex L7181-7190, the block the audit indexed at line 7185):

> *"If `L` is the realized full-slice image size and `M=binom(N,m)`, then
> `L >= e^{-o(N)} A_eff`, while every residual fiber is at most
> `e^{o(N)} M/A_eff`. Relative to the image-normalized full-slice mean `M/L`,
> every residual fiber is therefore `e^{o(N)}`-bounded."*

So the image bound `L >= e^{-o(N)} A_eff` is used **precisely to convert the
`A_eff`-normalized fiber bound into the image (`M/L`)-normalized bound**. It is
the **target** of this packet.

**The target, exactly.** `L >= e^{-o(N)} A_eff`, where `L=|S|` = realized
full-slice image size, `A_eff=|V_g|` = effective span size. Equivalently
`(FI)`'s Gap-1 (tex L875, L4844; split by #539): `L >= e^{-o(n)} A_eff`.

---

## Rung 2 --- R1: MAGNITUDE DERIVATION ATTEMPT --- verdict **CIRCULAR (PROVED)**

### 2.1 The elementary pigeonhole and the exact inequality that reverses

The fibers partition `Omega`, so `M = sum_{z in S} |F_z|`, and there are exactly
`L` nonempty fibers. Feed (CF1) `|F_z| <= M||K_A||_op/|A|`:

```
M = sum_{z in S} |F_z|  <=  L * max_z |F_z|  <=  L * ( M ||K_A||_op / |A| ).
```

Cancel `M > 0`:

```
    L  >=  |A| / ||K_A||_op .                                 (P)
```

**(P) is the only image lower bound the max-fiber bound yields.** To reach the
target `L >= e^{-o(N)} A_eff` from (P) one needs
`|A|/||K_A||_op >= e^{-o(N)} A_eff`; with `||K_A||_op <= e^{o(N)}` (CF2b) this is

```
    |A|  >=  e^{-o(N)} A_eff .          (NEED : span-normalized packing)
```

But CF2a supplies only

```
    |A|  >=  e^{-o(N)} L .              (HAVE : image-normalized packing)
```

Since `S subseteq G` always gives `L <= A_eff`, **(NEED) is strictly stronger
than (HAVE) by the factor `A_eff/L`**. Substituting (HAVE) into (P):

```
    L  >=  |A|/||K_A||_op  >=  e^{-o(N)} L / e^{o(N)}  =  e^{-o(N)} L .   (TAUTOLOGY)
```

**The exact reversing point.** (HAVE) `|A| >= e^{-o}L` cannot be upgraded to
(NEED) `|A| >= e^{-o}A_eff` without already knowing `L >= e^{-o}A_eff` --- which
*is* the target. The deficit is exactly the factor `A_eff/L`. This is avdeev's
own note L393 ("noncircular: neither statement nor hypotheses refer to the
residual max-fiber size") read against the *image* target: CF2 is image-scale,
so it is silent on the span scale. **PROVED.**

Tex restatement. The frame delivers *image*-normalized flatness
(`max fiber <= e^{o} M/L = e^{o} barN^img`). `rem:flatness-certifies-image`
(tex L4903-4912) converts flatness into `(FI)` **only from `AMBIENT`/span
normalization** (`max fiber <= e^{o} M/A = e^{o} barN^amb`), and `def:primitive-q`
(tex L4914-4940) states outright: *"An ambient formulation is permitted only
when it is proved directly or when `(FI)` has already been certified."* The two
normalizations differ by `A_eff/L` = `(FI)` itself. R1 is circular in the tex's
own vocabulary.

### 2.2 The circularity is ROBUST: CF3 kills the span-normalized escape too

Could one instead *demand* the stronger (NEED) `|A| >= e^{-o}A_eff` as a new
packing hypothesis, closing (P) in one line? No: by CF3,
`||K_A||_op >= |A| max_z mu(z) >= |A|/L` (since `max mu >= 1/L`). With
`|A| >= e^{-o}A_eff` this forces `||K_A||_op >= e^{-o} A_eff/L`, which is
`<= e^{o(N)}` (CF2b) **iff** `A_eff/L <= e^{o(N)}`, i.e. iff `L >= e^{-o}A_eff`
--- the target again. The full-dual identity is the sharp instance: taking
`A=G^` gives `|A|=A_eff` but `||K_{G^}||_op = |G| max mu = A_eff/L * (L max mu)`,
exponential when the image collapses (verifier BLOCK 2:
`||K_{G^}|| = p` on the one-block parabola, so the full dual pays `p` per block).

**Conclusion (PROVED).** No magnitude / operator-norm hypothesis of the CF1--CF6
family implies the image bound. Every route reverses at the same inequality:
the frame certificate is `|A|(image)/L`-normalized, the target needs
`A_eff(span)`-normalization, and the gap is exactly `A_eff/L`.

**Numerical face (verifier BLOCK 2, MEASURED).** For the one-block parabola
(`p in {3,5,7}`) the pigeonhole `|A|/||K_A||_op` over `A in {singleton, packing
A_k, full dual G^}` equals `1, p, p` respectively; its maximum over all families
is `p = L`, **never** `A_eff = p^2`. The pigeonhole recovers `L` and stops.

---

## Rung 3 --- R2: IMPOSSIBILITY WITNESS --- verdict **PROVED**

### 3.1 The witness is avdeev's own block-parabola family

Take the frame's block-parabola separation family verbatim (note L247-354):
odd prime `p`, `k` blocks, `Omega_k=(F_p)^k`, `N_k=pk`,
`Phi_k(t_1,..,t_k)=((t_1,t_1^2),..,(t_k,t_k^2)) in G_k=(F_p^2)^k`. avdeev already
proved every identity we need:

- injective, so `M_k = L_k = p^k` (note L273); `barN=1`.
- effective span is all of `G_k` (note L280): `A_eff = |G_k| = p^{2k}`.
  (`(t,t^2)` at `t=1,-1` has determinant `2 != 0`; verifier confirms
  `rank_{F_p} V_g = 2k`.)
- packing `A_k = {((a_1,0),..,(a_k,0))}` (note L329): `|A_k| = p^k = L_k`, and
  `K_{A_k} = I`, `||K_{A_k}||_op = 1`, `kappa_frame = L_k/|A_k| = 1`
  (note L336-338) --- because every off-diagonal difference `((a,0),..)` has a
  block factor `phi(a,0)=0` (the vanishing `b=0, a!=0` Gauss coefficient).

### 3.2 The witness satisfies CF1+CF2 exactly and violates J2 exponentially

- **(CF1):** `F_max = 1 <= M||K_{A_k}||/|A_k| = p^k * 1 / p^k = 1`. Holds
  (with equality).
- **(CF2):** `|A_k| = p^k = L_k >= e^{-o(N)}L_k` (equality) and
  `||K_{A_k}||_op = 1 <= e^{o(N)}`. **Satisfied exactly.**
- **Target J2:** `L_k >= e^{-o(N)} A_eff` would read `p^k >= e^{-o(pk)} p^{2k}`,
  i.e. `p^{-k} >= e^{-o(pk)}` --- **false** by the honest exponential factor

  ```
     A_eff / L_k  =  p^{2k}/p^k  =  p^k  =  e^{(log p / p) * N_k}  =  e^{Theta(N)}.
  ```

**Theorem (PROVED).** The implication *"(CF1) + (CF2) => `L >= e^{-o(N)}A_eff`"*
is **false**. The block-parabola family is a counter-instance on which all frame
hypotheses hold exactly while `L/A_eff = p^{-k}` is exponentially small. Hence
the character frame **cannot** deliver the image half of `(EFP)`.

### 3.3 Why: the frame multiplier and the image multiplier are different objects

The frame reports `kappa_frame = L ||K_A||/|A|` (image-normalized). #539's Gap-1
pigeonhole reports `kappa* := A_eff * F_max / M` (span-normalized; #539
`A1.EFP.image_ge_Aeff_over_kappa`, note L159-167). They are related by

```
    kappa*  <=  (A_eff/L) * kappa_frame ,     with equality on the witness:
    kappa* = p^k ,   kappa_frame = 1 ,   kappa*/kappa_frame = p^k = A_eff/L .
```

The frame bounds `kappa_frame`; the target needs `kappa*` bounded; the
uncontrolled ratio between them is exactly `A_eff/L` = the image bound. On the
witness `kappa_frame=1` (perfect flatness certified) while `kappa*=p^k` (Gap-1
fails). **PROVED / MEASURED** (identity proved; numbers in verifier BLOCK 1 and
the summary table).

### 3.4 Indistinguishability, and why no fully-CF2 exponential *pair* exists

The parabola measure and the uniform-on-`G` measure give the **identical** Gram
`K_{A_k} = I` on the same packing `A_k` (verifier BLOCK 3): same `A`, same
`|A| = p^k`, same `||K|| = 1` --- yet `L = p` (parabola) vs `L = p^2` (full).
`kappa*` is `p` (Gap-1 FAILS) vs `1` (Gap-1 HOLDS). **Identical frame data,
opposite image verdict: the Gram matrix is `A_eff`-blind.**

Honest sub-finding (PROVED). A *pair* both satisfying CF2 with the *same* `|A|`
and `||K||` cannot have exponentially different `L`: (P) gives `L >= |A|/||K||`
and CF2a gives `L <= e^{o}|A|`, so both `L` are pinned to `|A|` up to
subexponential. Thus the impossibility is carried by a **single** CF2-satisfying
witness (the parabola); the "pair" is the indistinguishability illustration, not
a second CF2 instance. The frame *does* pin `L` to `|A|`; it does **not** pin `L`
to `A_eff`.

Sub-finding (phase, PROVED). A pure phase rotation of `hat_mu` (= a translation
of `mu`) preserves `L` exactly, so it can never collapse the image. The collapse
is realized by **spectral concentration on the `b != 0` band** that the packing
`A_k` dodges: there `|hat_mu| = p^{-1/2} > 0` (image-span mass) while the frame
sees only the `b = 0` band. The supplement must probe `V_g^ \ (A-A)`.

---

## Rung 4 --- R3: SUPPLEMENT ROUTING

The image half needs a **span (`A_eff`)-normalized** max-fiber bound, equivalently
a direct image lower bound, which is inherently **phase-dependent** (EFP is
phase-dependent, tex L2947; the frame is magnitude-only, CF3). Named sources:

1. **#539 Gap-1 corollary** `EF4 => L >= A_eff/kappa` (note L153-179). It
   consumes the **span-normalized** `EF4` (`F_max <= e^{o} M/A_eff`), which the
   frame does **not** deliver (frame gives `F_max <= e^{o} M/L`). So #539 bridges
   **from `(EFP)`, not from the frame**; using it requires retaining
   `(EFP)`/`(MI)+(MA)` on `V_g` --- the very payment the frame was to replace.
   *Not available to the frame.* (PROVED: kappa*/kappa_frame = A_eff/L uncontrolled.)

2. **`(FI)`/`(A4)`'s `L_N` clause** (tex L864-884, L912-923, L4844): assume
   `L >= e^{-o(N)}A` as a leaf hypothesis. Per #539 this splits as Gap-1 (image
   fills span) + Gap-2 (span fills ambient); the frame supplies **neither**. This
   is the honest external source: the consumer posits the image is large.

3. **Phase-sensitive / signed spectral input** --- scottdhughes's ambient
   `(LS)` large sieve (#564), or any input controlling `hat_mu` across all of
   `V_g^` (able to detect `|supp mu| = L`). This is the phase-sensitive
   supplement CF3 proves the frame lacks.

**Cheapest honest completion (the deliverable statement).**

> **Frame (max-fiber, image-normalized) + a Gap-1 source (span-normalized image
> bound) = the full `(EFP)` interface.** The frame alone is a proper
> half-interface. Any leaf using the frame in place of `(EFP)` must source
> `L >= e^{-o(N)}A_eff` separately, from `(A4)`'s span-normalized
> `(EFP)/(MI)+(MA)/Sidon` payment on `V_g` **or** a phase-sensitive input; it is
> **not** derivable from the frame's magnitude hypotheses (Rung 2, Rung 3).

This **sharpens** the audit's J2 verdict from `OPEN GAP` ("the large-image fact
is not a frame output") to a **theorem**: the large-image fact is *not
deliverable by any magnitude / operator-norm frame hypothesis*.

---

## Rung 5 --- CENSUS (exact toy verification)

`verify_frame_image_completion.py`, `RESULT: PASS (66/66)`, ~0.48 s under
`ulimit -v 2097152`. Blocks: (0) Gauss-sum identities `phi(0,0)=1`, `phi(a,0)=0`,
`|phi(a,b)|=p^{-1/2}`; (1) R2 witness on `(p,k) in {(3,1),(3,2),(5,1),(5,2),(7,1)}`
+ closed-form scalable rows `k=1..4`; (2) R1 circularity sweep + CF3 full-dual
identity; (3) indistinguishability pair.

Recomputed summary (MEASURED, exact):

| p | k | M | L | A_eff | kappa_frame | kappa*(#539) | L/A_eff |
|---|---|---|---|-------|-------------|--------------|---------|
| 3 | 1 | 3 | 3 | 9 | 1.0000 | 3 | 0.3333 |
| 3 | 2 | 9 | 9 | 81 | 1.0000 | 9 | 0.1111 |
| 5 | 1 | 5 | 5 | 25 | 1.0000 | 5 | 0.2000 |
| 5 | 2 | 25 | 25 | 625 | 1.0000 | 25 | 0.0400 |
| 7 | 1 | 7 | 7 | 49 | 1.0000 | 7 | 0.1429 |

Every row: CF1 holds, CF2 holds exactly (`|A_k|=L`, `||K||=1`), yet
`kappa*=p^k=A_eff/L` while `kappa_frame=1`. R1 sweep: `max_A |A|/||K_A|| = L`,
never `A_eff`; CF3 `||K_{G^}|| = p` confirmed.

---

## Verdict ledger and #558 promotion decision

| item | verdict | status |
|------|---------|--------|
| R1 magnitude derivation (pigeonhole) | **CIRCULAR** at `(HAVE) |A|>=e^{-o}L` vs `(NEED) |A|>=e^{-o}A_eff`, deficit `A_eff/L` | PROVED |
| R1 robustness (span-normalized escape via CF3) | **DEAD**: `|A|>=e^{-o}A_eff` forces `||K_A||>=e^{-o}A_eff/L`, subexp iff J2 | PROVED |
| R2 impossibility witness (block-parabola) | **(CF1)+(CF2) hold exactly, J2 fails by `p^k=e^{Theta(N)}`** | PROVED |
| kappa*/kappa_frame = A_eff/L | frame multiplier and Gap-1 multiplier differ by the image bound | PROVED / MEASURED |
| indistinguishability (K_{A_k}=I for L=p and L=p^2) | frame data is `A_eff`-blind | MEASURED |
| supplement (FI/A4 L_N clause, or phase-sensitive (LS)) | frame + Gap-1 source = full interface | routed |

**Promotion decision for #558: PARTIAL replacement + named supplement.**
Promote the character frame exactly as the audit's proposed ledger entry gated
it (G1/J2): an **alternative sufficient interface for the max-fiber multiplier
(EF5) of `prop:effective-mi-ma-flatness`, at image normalization only**. It
**cannot** replace the image clause of `(EFP)`. Every consumer (the
`thm:primitive-q` / prefix-flatness proof at tex L7185) that replaces `(EFP)` by
the frame must **separately** source `L >= e^{-o(N)}A_eff` from `(A4)`'s
span-normalized payment on `V_g` or a phase-sensitive input. **The frame is a
proper half-interface: max-fiber yes, image no --- provably, not merely
un-supplied.** Do not promote `(CF2)` (still OPEN, avdeev's crux).

### The 2-3 steps the PI should re-derive

1. **R1's reversing inequality (2.1).** Confirm `(P) L >= |A|/||K_A||` is the
   only image lower bound from CF1, and that CF2a `|A|>=e^{-o}L` -> tautology
   `L>=e^{-o}L`; the deficit is exactly `A_eff/L`. This is the whole verdict.
2. **R2's CF2-exactness on the parabola (3.2).** Confirm `K_{A_k}=I`,
   `|A_k|=p^k=L`, so CF2 holds *exactly*, while `A_eff=p^{2k}` gives
   `L/A_eff=p^{-k}`. This is avdeev's own family, so no new construction is
   trusted --- only the re-reading against the *image* target.
3. **The kappa*/kappa_frame = A_eff/L identity (3.3) and CF3 robustness (2.2).**
   Confirm the frame multiplier and #539's Gap-1 multiplier differ by exactly
   the image bound, and that CF3 forbids buying `|A|>=e^{-o}A_eff` cheaply.

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_frame_image_completion.py   # RESULT: PASS (66/66)
```
