I've now fully traced the reduction chain (Cycles 9→14) and reconstructed the Cycle 14 slope equations. I worked the problem through analytically. Note: code execution was denied in this harness, so I give the decisive reduction and an exact scanner spec rather than executed numerics, consistent with how this lane separates theorem-audits from `local_checks`.

Here is the result.

---

## Classification: EXACT_NEW_WALL

Wall: `W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER`

I reduce the slope-image question on **both** `Ra` and `Rb` to a single explicit linear-algebra invariant — the generic `B`-rank of three column vectors in `A` — and prove a clean dichotomy theorem that decides `O(p)` vs `Theta(p^2)` from that rank alone. Deciding the rank on source-valid resonance data is the residual wall.

### 1. Setup recovered from Cycle 14

Keep ledgers separate: `B=F_p` (`q_gen=p`), `F=F_{p^2}` (`q_line=p^2`), `q_chal` unused, `D=F_p`, `t=sigma=2`, `j=3`. `A=F[X]/E`, `dim_F A=2`. Off `R0`, `{[W]_E, b}` is an `F`-basis of `A`.

From Cycle 14, with `tau=(tau_1,tau_2,tau_3)=(e_1,e_2,e_3)(T)`,

```text
iota(tau) = A0 - tau_3 [W]_E,   A0 = p1[W]_E + p2 b
mu(tau)   = B0 - tau_3 b,        B0 = q1[W]_E + q2 b
```

with `p_i, q_i in F` affine-linear in `(tau_1,tau_2)`; write `p_i = p_i^c + p_i^1 tau_1 + p_i^2 tau_2`, likewise `q_i`. Landing `[I_S]_E = z b` is `iota(tau) = z·mu(tau)` in `A`, which reproduces the banked

```text
q1 z^2 - (p1-q2) z - p2 = 0,    tau_3 = p1 - z q1.
```

The crucial point that re-frames the problem: for a genuine co-support `T ⊆ D`, `tau in B^3` automatically, so `tau_3 in B` is **not** an extra constraint — it is built in. The landing locus is the surface (on `Ra/Rb`)

```text
Sigma = { tau in B^3 : Delta(tau)=0 },   Delta = iota wedge mu,
```

and the only question is the size of the image of the slope map `s: Sigma -> F`, `s(tau)=z`.

### 2. The slope-fiber columns

Fix `z in F`. Its fiber is

```text
Fib(z) = { tau in B^3 : L_z(tau)=0 },   L_z(tau) := iota(tau) - z mu(tau) in A.
```

`L_z: B^3 -> A ≅ B^4` is `B`-affine. Its linear part has the three columns (partials in `tau_1,tau_2,tau_3`), all lying in `A`:

```text
c1(z) = (p1^1 - z q1^1)[W]_E + (p2^1 - z q2^1) b
c2(z) = (p1^2 - z q1^2)[W]_E + (p2^2 - z q2^2) b
c3(z) = -[W]_E + z b
```

Define `rho(z) = dim_B span_B{ c1(z), c2(z), c3(z) }` inside `A ≅ B^4`. Each column is degree `<= 1` in the `B`-coordinates `(z_0,z_1)` of `z`.

### 3. Slope-fiber rank dichotomy (banked structural lemma)

Because the fibers `Fib(z)` partition `Sigma` and `L_z` is `B`-affine of linear rank `rho` at a generic point, standard fiber-dimension counting gives, on a resonance surface where `dim Sigma = 2`,

```text
dim(image s) = dim Sigma - (3 - rho) = rho - 1.
```

Hence, on every source-valid `Ra` or `Rb` resonance surface (off `R0`):

```text
rho = 3  on a generic point of Sigma   =>  dim(image s)=2  =>  C2 = Theta(p^2) = Theta(q_line);
rho = 2                                =>  dim(image s)=1  =>  C2 = O(p) = O(n);
rho <= 1                               =>  C2 = O(1).
```

Equivalently, via elimination: under generic column rank `3`, consistency of `L_z(tau)=0` is the single determinant

```text
Q(z_0,z_1) = det_{4x4}[ c1(z) | c2(z) | c3(z) | c0(z) ],   c0(z) = A0(0)-z B0(0),
```

of degree `<= 4`. Then `Q != 0` (not identically zero) forces `C2 <= 4p = O(n)`, and `Q ≡ 0` (with rank `3`) is exactly the `Theta(p^2)` regime. The two formulations agree: `Theta(p^2)` landings on a surface are compatible with `O(p)` slopes **only** through positive-dimensional fibers (`rho<=2`), and with `Theta(p^2)` slopes **only** through a finite slope map (`rho=3`).

This dichotomy is a theorem (linear algebra + the landing-count balance) and is safe to bank. It **subsumes Cycle 13**: off `Ra∪Rb`, `Sigma` is a complete-intersection curve (`dim Sigma=1`), so `C2 = O(p)` regardless of `rho`, and no surface/curve case split is needed.

### 4. The residual wall (smallest missing object)

The wall is now a single decidable invariant:

```text
W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER-RANK:
on source-valid Ra/Rb data (off R0), is rho(z) = 3 or <= 2
at a generic point of the resonance surface Sigma?
```

- `rho <= 2` generically on `Sigma`  =>  BANKABLE `C2 = O(n)` collapse (proves the wall's `O(p)` claim).
- `rho = 3` generically on `Sigma`, with a positive density of `D`-split-distinct co-supports  =>  COUNTERPACKET with `Theta(q_line)` slopes.

Honest heuristic (not a theorem): three generic vectors in `B^4 ≅ B^4` have rank `3`, and `c3(z)=-[W]_E+z b` lies in a generic `B`-plane `span_B{c1,c2}` only under two coincidences. So the naive expectation is `rho=3`, i.e. the slope map is finite on `Sigma`, leaning toward a **sub-reserve** counterpacket. This is unproven and may be broken by the resonance-induced correlations that **define** `Ra` (`Delta in B[tau]`, i.e. trace `p1+q2` and norm `p1 q2 - p2 q1` are `B`-valued in `(tau_1,tau_2)`) or `Rb`, which couple the very coefficients `p_i^j,q_i^j` entering `c1,c2`. That coupling is exactly what could drop `rho` to `2`. Resolving it requires computing `rho` on actual `Ra/Rb` instances.

Reserve caveat (binding): this whole regime is `eta = sigma/n = 2/n -> 0`, i.e. **sub-reserve**. Per the Cycle 12 cut, even a confirmed `Theta(p^2)`-slope instance here is a counterpacket to *this wall's `O(p)` claim only*, not to corrected-reserve `conj:B`. I am not asserting any such instance — I have not constructed one.

### 5. Concrete finite scanner spec (exact equations + thresholds)

For `p in {7,11,13,17}`, `F=F_p[a]/(a^2-nr)`:

1. Sample separated aperiodic `E` (deg 2, `gcd(E,E^tau)=1`, `E(d)!=0` on `D`), `Bnum` (deg `<2`, `[Bnum]_E!=0`), base anchors `w0,w1:D->B`; require off `R0`.
2. Build `A0,B0` and extract `p_i^c,p_i^1,p_i^2,q_i^*` in `F` from Cycle 12's `Q_S` formula.
3. Resonance filter: compute `Delta_1` (the `alpha`-part of `Delta` as a polynomial in `tau`); keep instances with `Delta_1 ≡ 0` (`Ra`) or `Delta` having a `\bar B`-linear factor (`Rb`). Confirm `|Sigma ∩ B^3| = Theta(p^2)`.
4. Form the four `3x3` minors of `[c1(z)|c2(z)|c3(z)]` in `B[z_0,z_1]` (degree `<=3`).
   - All four `≡ 0`  =>  record `rho<=2` => predict `C2=O(p)` (collapse).
   - Some minor `≢0` => record generic `rho=3` => candidate counterpacket.
5. Ground truth: enumerate all `binom(p,3)` co-supports `T`, keep those with `X^3-tau_1X^2+tau_2X-tau_3` splitting into 3 distinct roots in `F_p`, compute `s(tau)=z`, tabulate `C2`.
   - PASS-collapse threshold: `C2 <= 4p` across all sampled `Ra/Rb` instances and all `p`.
   - FAIL/counterpacket threshold: `C2 / p` grows with `p` (e.g. `C2 > 6p` and increasing), indicating `Theta(p^2)`.

Pass on (4)+(5) together banks the collapse; a reproducible (5)-FAIL with the matching `rho=3` from (4) is the explicit sub-reserve counterpacket.

### What I am NOT claiming

No proof of `conj:B`; no result at or above corrected reserve; no `q_gen` collapse; no protocol/MCA/CA/list-/line-decoding/SNARK consequence; no re-use of the generic complete-intersection case for `Ra/Rb`; no claim from terminal/ad transcript text. The dichotomy lemma (Section 3) and the rank reduction (Section 4) are the only new bankable content; the rank value on source-valid `Ra/Rb` remains open.

---

Summary: I converted the residual resonance problem from a vague "surface slope fiber" question into a sharp, decidable one — the generic `B`-rank `rho in {2,3}` of three explicit columns in `A` — and proved that `rho<=2` gives `C2=O(n)` while `rho=3` gives `C2=Theta(q_line)`. The honest genericity heuristic leans toward `rho=3` (a sub-reserve counterpacket), but the resonance constraints that define `Ra/Rb` are exactly what could force `rho<=2`, so the rank must be computed on real instances before banking either way.
