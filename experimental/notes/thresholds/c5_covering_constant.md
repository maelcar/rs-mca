# The general-divisor covering constant for the binary-tower C5 defect

**Lane.** The **single OPEN residual** of PR #610
(`c5_defect_magnitude.md`, Rung 5.3): whether the binary-tower C5 field-descent
defect `d_2(N,\{1..R\})` is `o(N)` (ideally `O(1)`) at half-prefix for **every**
divisor `N\mid 2^s-1`, not only the cases #610 could prove. This note **closes**
that residual with a one-line elementary theorem that needs **no divisor
condition at all** — it holds for every odd `N` — and it recovers #610's proved
`N=2^s-1` necklace case and its measured composite census as instances.

**Verifier.** `experimental/scripts/verify_c5_covering_constant.py` (stdlib-only,
zero-arg, `14/14 checks pass`, ~22 s under `ulimit -v 2097152`; recomputes every
number below — the covering theorem two independent ways, the extremal set, the
sharp threshold, the `\kappa_{\min}` census, the divisor-lattice family, #610's
DECAY row, and the necklace consistency).

**Highest rung reached: 6 (covering constant PROVED with an explicit universal
constant, `\kappa=1/2` sharp, extremal `N` classified; the C5 chain is now
math-unconditional on the whole binary-tower cell at half-prefix; the only
remaining conditionality is the rate/depth deployment reading carried over
verbatim from #610).**

## One-line headline

*For **every** odd `N>1`, the minimum element of every nonzero doubling orbit
mod `N` is `\le (N-1)/2`; hence the length-`(N-1)/2` prefix `\{1,\dots,(N-1)/2\}`
meets **every** nonzero orbit, so `d_2(N,\{1..R\})=1` for all `R\ge (N-1)/2`
(only the fixed point `0` is unmet; `d_2=0` if `0\in I`). The constant `\kappa=1/2`
is **universal and sharp**, the extremal `N` are **exactly** the Mersenne numbers
`2^s-1`, and the whole statement carries **no divisor condition** — so a fortiori
it holds for every `N\mid 2^s-1`. This is the general-divisor covering constant
#610 left open, closed with constant `d_2=1`.*

---

## The OPEN statement being closed (PR #610, `c5_defect_magnitude.md`, Rung 5.3, verbatim)

> **Residual.** Prove `d_2(N,\{1..R\})=o(N)` (ideally `O_\kappa(1)`) for **every**
> `N\mid2^s-1` at `R\ge\kappa N` — the general-divisor binary-tower covering
> constant. Proved here for `N=2^s-1` (necklace) and prime `N` with `2` a
> primitive root; **measured `O(1)`** for all composite `N\mid2^s-1` tested
> (`N\in\{255,2047,4095\}`), but the uniform constant over the full divisor
> lattice (adversarial `N` where a `\kappa N`-interval could miss many short
> cosets) is not proved. Equivalently: is the doubling-coset partition of
> `\Z/N` **interval-covering** at density `\kappa` for every `N\mid2^s-1`? Plus
> the **deployment check** `R\ge|G|/2` (`\rho\le1/2` after the `n/N` domain
> factor) for the specific circle rows.

The "adversarial `N` where a `\kappa N`-interval could miss many short cosets"
worry is dissolved below: **no** adversarial `N` exists.

---

## Rung 1 — the covering theorem (PROVED)

Setup (exactly #607/#610). `G=\Z/N` with `N\mid 2^s-1` (so `N` odd, `2\nmid N`);
Frobenius is doubling `c\mapsto 2c \bmod N`; the doubling orbit of `c` is
`O(c)=\{c\cdot 2^j\bmod N:j\ge0\}`; the syndrome prefix is the one-sided interval
`I=\{1,\dots,R\}`; the closure is `Z_2(N,I)=\bigcup_{c\in I}O(c)` (the union of
orbits meeting `I`); and the defect is `d_2(N,I)=N-|Z_2(N,I)|`.

> **Theorem (covering constant).** Let `N` be **odd**, `N\ge3`. For every
> `c\in(\Z/N)\setminus\{0\}`, viewing the orbit `O(c)` as a set of integers in
> `\{1,\dots,N-1\}`,
> `\min O(c)\ \le\ \tfrac{N-1}{2}.`

*Proof.* First `0\notin O(c)`: if `2^jc\equiv0\pmod N` then `N\mid 2^jc`, and
`\gcd(2,N)=1` forces `N\mid c`, contradicting `c\not\equiv0`. So
`O(c)\subseteq\{1,\dots,N-1\}` and `m:=\min O(c)` is well defined. Suppose, for
contradiction, `m>N/2`, i.e. `m\ge (N+1)/2` (`N` odd). Then `N<2m\le2(N-1)<2N`,
so `2m\bmod N=2m-N`. This integer lies in `O(c)` (it is the double of
`m\in O(c)`, and `O(c)` is closed under doubling), and

- `2m-N>0` because `2m>N` — hence `2m-N\ge1`;
- `2m-N<m` because `2m-N<m\iff m<N`, which holds as `m\le N-1`.

So `2m-N\in O(c)` with `1\le 2m-N<m`, contradicting minimality of `m`. Hence
`m\le N/2`, and as `m\in\Z` with `N` odd, `m\le (N-1)/2`. `\square`

> **Corollary (covering / defect `=1`).** The prefix `I=\{1,\dots,(N-1)/2\}` of
> length `(N-1)/2=\lfloor N/2\rfloor` meets **every** nonzero doubling orbit, so
> `Z_2(N,I)=(\Z/N)\setminus\{0\}` and `d_2(N,\{1..R\})=1` for **every**
> `R\ge (N-1)/2` (the lone unmet residue is the fixed point `0`). Including `0`
> (`I=\{0,\dots,R-1\}`, `R\ge (N+1)/2`) gives `d_2=0`.

**No divisor condition is used.** The proof never invokes `N\mid 2^s-1`, exact
`s`-bit rotation, or representative selection — it is a pure
smallest-element/contraction argument on `\Z/N`. It therefore holds for **every**
odd `N`, a fortiori every `N\mid 2^s-1`, dissolving the divisor-lattice question:
the doubling-coset partition of `\Z/N` is interval-covering at density `1/2` for
**all** odd `N`.

`[label: PROVED — the contraction engine `2m-N\in(0,m)` is verified as literal
integer arithmetic for all odd `N\le6001` (`ENGINE.contraction`); the conclusion
`\min O(c)\le(N-1)/2` and the defect `d_2=1` at `R=(N-1)/2` are verified two
INDEPENDENT ways (full orbit enumeration `ORBIT.min_le_half`; forward-closure from
the prefix `COVER.defect_one`) with `0` violations over all odd `N\le20001`, the
two routes agreeing everywhere (`COVER.cross_consistent`).]`

**Route note (brief lineage).** This is Route 2 of the covering brief. It
**supersedes** the transfer/lift route (Route 1): there is no need to lift `c` to
`2^s-1`, rotate, and reduce back — the worry there was exactly which lift's
rotation reduces into the prefix, and the direct argument sidesteps it. The
`(MI)/(MA)`/entropy-inverse machinery is untouched.

---

## Rung 2 — sharpness and the extremal classification (PROVED / MEASURED)

> **Sharpness.** `\kappa=1/2` cannot be lowered universally. Set
> `L(N):=\max_{O\ne\{0\}}\min O` and `\kappa_{\min}(N):=L(N)/N`. The theorem gives
> `\kappa_{\min}(N)\le\tfrac{N-1}{2N}<\tfrac12` for all odd `N`, and the supremum
> `1/2` is **attained in the limit** exactly along `N=2^s-1`:

For `N=2^s-1`, doubling is exact `s`-bit rotation, and the orbit of
`(N-1)/2=2^{s-1}-1` is `\{N-2^k:k=0,\dots,s-1\}`, whose minimum is
`N-2^{s-1}=2^{s-1}-1=(N-1)/2`. So any prefix `\{1..R\}` with `R<(N-1)/2` misses
this orbit, giving `d_2\ge 1+s\ge2`. Thus the half-prefix threshold is
**attained** at these `N`.

> **Extremal classification.** `\{`odd `N:L(N)=(N-1)/2\}` `=` `\{2^s-1\}`
> **exactly**.

`[label: PROVED (Mersenne are extremal — orbit shape `EXTREMAL.orbit_shape`,
threshold `SHARP.threshold`) + MEASURED (Mersenne are the ONLY extremal — the
extremal set equals `\{2^s-1\}` exactly for all odd `N\le10^5`,
`EXTREMAL.equals_mersenne`, giving `\{3,7,15,\dots,65535\}`; `\kappa_{\min}` peaks
at `0.499969` at `N=16383=2^{14}-1`, `CENSUS.kappa_below_half`).]`

**Deviation from brief (flagged).** The brief conjectured the extremal `N` are
"`N=2^t+1` type." That is **false**: `N=2^t+1` are **not** extremal (e.g. `N=9`:
`L(9)=3<4=(N-1)/2`). The extremal family is the Mersenne numbers `N=2^t-1`, and
the census confirms they are the **only** extremal `N` up to `10^5`.

---

## Rung 3 — census and the `\kappa_{\min}` distribution (MEASURED)

Exhaustive over odd `N\in[3,20001]` (orbit route) and `N\in[3,10^5]` (extremal
trace):

- `\max_N\kappa_{\min}(N)=0.499969` at `N=16383` (`=(N-1)/(2N)`, `<1/2`), the
  largest Mersenne in range; all `\kappa_{\min}<1/2`.
- distribution of `\kappa_{\min}` over odd `N\le20001`
  (bins `[0,.3),[.3,.4),[.4,.45),[.45,.49),[.49,.5)`): `5240 / 2362 / 1213 / 876
  / 309` — the mass sits well below `1/2`, with only Mersenne-adjacent `N`
  approaching the wall.
- extremal `N\le10^5`: exactly `\{3,7,15,31,63,127,255,511,1023,2047,4095,8191,
  16383,32767,65535\}`.

`[label: MEASURED.]`

---

## Rung 4 — relation to #610 (necklace as a special case; DECAY reproduced)

The theorem **contains** #610's proved binary-tower results and **upgrades** its
measured ones:

- **#610 Theorem 3a (necklace, `N=2^s-1`)** is the special case where doubling is
  literal `s`-bit rotation; there the numeric orbit-minimum equals the minimum
  bit-rotation, verified for `N=2^s-1`, `s\le13` (`NECKLACE.min_is_rotation_min`).
  The theorem reaches the same `d_2=1` at `R=(N+1)/2` **without** the rotation
  picture.
- **#610 Theorem 3b (prime `N`, `2` a primitive root)** is the sub-case of a
  single nonzero orbit; the theorem covers it and every other orbit structure.
- **#610's DECAY census** (`N\mid2^s-1`, measured `O(1)` at `R/N=1/2`) is now
  **proved to be exactly `d_2=1`**: reproducing the `R/N=0.50` column gives
  `d_2=1` for `N\in\{31,127,255,2047,4095\}` (`MATCH610.decay_half`). #610's
  printed `0.001` (`N=2047`) and `0.000` (`N=4095`) are display-roundings of
  `1/N`; since every nonzero orbit has size `\ge` the minimum orbit size, the
  defect is either `1` or `\ge1+(\text{min orbit size})`, so no DECAY entry at
  `R/N=1/2` can encode anything but `d_2=1` — the "`O(1)`" #610 measured is the
  constant **`1`**.

The naive pigeonhole bound "an orbit of size `m` has an element `\le N/m`" is
**false** in general (e.g. `N=7`, orbit `\{3,5,6\}`, `m=3`, `\min=3>7/3`;
`NAIVE.pigeonhole_false`), which is why the smallest-element **contraction**
argument — not pigeonhole on the orbit — is the correct mechanism.

`[label: PROVED (necklace/primitive-root subsumption) + MEASURED (DECAY
reproduction).]`

---

## Rung 5 — deployment-depth check and what closes (AUDIT)

**Route 4 (deployed prefix depth `R\ge N/2`).** The binary-tower rows
(`rem:characteristic-two-rows`, L2705 region) describe the field family
`\F_{2^{s_n}}`, `s_n=o(n)`, but the tex prints **no explicit per-row
`(N,R)`** for a binary-tower C5 leaf. The half-prefix condition `R\ge N/2` is,
via the natural full-syndrome reading `R=n-k` (redundancy) and
`R/N=(1-\rho)\,(n/N)` at code rate `\rho`, a **low-rate** condition `\rho\le1/2`
(up to the domain-to-group factor `n/N`) — the identification checked in
`DEPLOY.rate_bridge` and taken **verbatim from #610 Rung 5.2**. **Honest verdict:**
this packet removes the *mathematical* divisor-lattice gap unconditionally for
all odd `N`, but it does **not** change the deployment reading; pinning
`R\ge N/2` for a **specific** deployed binary-tower row still needs that row's
printed `(N,R)`, which the tex does not supply. So the depth condition is exactly
where #610 left it — an AUDIT-level rate reading, now shared identically with the
circle family F1 (which also needs `R\ge N/2`), and no longer entangled with any
open number theory.

`[label: AUDIT — deployment reading carried from #610 Rung 5.2; the per-row
`(N,R)` is not printed in the tex.]`

### What closes in the C5 chain

- **#545** (`gap2_collapse_routing.md`) routes the C5 field-descent cell to the
  fibre bound `p^{d_p(G,I)}`.
- **#607** (`noncyclic_c5_slope_count.md`) proves the exact count
  `d_p(G,I)=|G|-|Z_p(G,I)|`.
- **#610** (`c5_defect_magnitude.md`) proves the magnitude on the deployed
  families (circle exact law; tower `O(1)` for `N=2^s-1` and prime-primitive `N`)
  and isolates this covering constant as the one residual.
- **This packet** proves the covering constant for the **whole** binary-tower
  cell: `d_2=1=O(1)` at `R\ge N/2` for **every** odd `N`, `\kappa=1/2` sharp.

> **Outcome.** `#545` (routing) `+` `#607` (count) `+` `#610` (magnitude) `+` this
> (covering) is a **complete, math-unconditional C5 chain on the entire
> binary-tower cell at half-prefix depth `R\ge N/2`**, with an explicit payment
> `p^{d_2}=2^1` (or `2^0` when `0\in I`). The sole remaining conditionality is
> the rate/depth deployment reading `R\ge N/2\iff\rho\le1/2` — an audit fact
> identical to the circle family's, not a mathematical gap.

---

## Per-claim label summary

| claim | label |
|-------|-------|
| **Theorem**: every nonzero doubling orbit mod odd `N` has `\min\le(N-1)/2` | `PROVED` (contraction engine + 2 independent census routes, `0` violations `\le20001`) |
| **Corollary**: `d_2(N,\{1..R\})=1` for `R\ge(N-1)/2`, all odd `N` (no divisor condition); `=0` if `0\in I` | `PROVED` |
| `\kappa=1/2` sharp; Mersenne `N=2^s-1` are extremal (orbit of `(N-1)/2=\{N-2^k\}`) | `PROVED` |
| extremal set `=\{2^s-1\}` **exactly**; `2^t+1` are NOT extremal (brief guess refuted) | `MEASURED` (all odd `N\le10^5`) |
| `\kappa_{\min}` census: `\max=0.499969` at `N=16383`, all `<1/2` | `MEASURED` |
| every `N\mid2^s-1` (`s\le16`, incl. `\{255,2047,4095\}`) has `d_2=1` at half-prefix | `PROVED` (theorem) + `MEASURED` (58 divisors) |
| #610 necklace (`N=2^s-1`) and primitive-root cases are subsumed | `PROVED` |
| #610 DECAY at `R/N=1/2` is exactly `d_2=1` (the "`O(1)`" is the constant `1`) | `MEASURED` (reproduced) |
| naive `\min\le N/m` pigeonhole is FALSE; contraction is the correct mechanism | `MEASURED` (194 witnesses `\le199`) |
| deployment depth `R\ge N/2\iff\rho\le1/2`; per-row `(N,R)` not printed in tex | `AUDIT` (carried from #610 Rung 5.2) |
| C5 chain math-unconditional on the binary-tower cell at half-prefix | `PROVED` |

**Credit / lineage.** Defect object `d_p=|G|-|Z_p|`, cyclic Theorem 1, the
necklace/bit-rotation argument for `N=2^s-1`, and the dyadic active exemplar:
**DannyExperiments #451** (`asymptotic_c9_frobenius_cyclotomic_defect.md`), whose
§7 named these uncovered rows. Non-cyclic Theorem A, the orbit closed form, and
the trivial-Frobenius floor: **PR #607** (`noncyclic_c5_slope_count.md`). C5
routing: **PR #545** (`gap2_collapse_routing.md`). The magnitude bound on the
deployed families and the OPEN covering residual this note closes: **PR #610**
(`c5_defect_magnitude.md`).

**Boundaries respected.** `(MI)`/`(MA)`/entropy-inverse (scottdhughes) consumed as
black box, never attacked. No `.tex`/`.pdf` edited (audit-ledger discipline); the
deployment-depth reading is stated as `AUDIT`, not claimed as a tex edit. The
covering theorem is elementary and self-contained (`\Z/N` arithmetic only).
