I have the required ledgers. Two files named in the prompt are not in this snapshot, which I record below, then I reconstruct the Cycle 15 setup from `ROUTE_BOARD_CURRENT.md`, `BANKED_LEMMAS.md`, `ACTIVE_WALLS.md`, and `NEXT_PROMPT_QUEUE.md` (which carry the columns verbatim) and attack the rank/determinant obstruction directly.

---

## Parameters (field ledgers kept separate)

```text
B = F_p        q_gen  = p          (generated/entropy/base field, D=F_p, n=p)
F = F_{p^2}    q_line = p^2        (extension/line field)
q_chal         unused
t = sigma = 2  j = n-a = r-t = 3   a = n-3, k = n-5
eta = sigma/n = 2/n                (sub-reserve; this whole wall is sub-reserve)
A = F[X]/E, dim_F A = 2, dim_B A = 4 ;  b = [Bnum]_E != 0 ;  ω := wedge([W]_E,b) ∈ F^*
Work off R0 = { ω = 0 }. {[W]_E, b} is then an F-basis of A.
```

## AUDIT 1 — two named source files are absent from this run snapshot

`current_loop_.../audits/20260618_CYCLE15_SURFACE_SLOPE_FIBER_AUDIT.md` and `.../local_checks/20260618_cycle15_forced_ra_slope_scan_certificate.md` are **not present** in `FILE_INDEX_FOR_MODEL.md`. The mounted local-checks stop at Cycle 9; `DIRECTOR_STATE.md` points the Cycle 15 artifacts at an external `/Users/danielcabezas/OpenClaw/...` path that is not in the read-only copy. I therefore reconstruct the Cycle 15 columns and the `Ra/Rb` reduction from the four banked ledgers, all of which transcribe them identically, and I flag every step that depends on the unavailable detailed `A0,B0` coefficients.

## AUDIT 2 — Cycle 15 columns are correct as stated (no index mismatch)

Substituting `A0=p1[W]_E+p2 b`, `B0=q1[W]_E+q2 b` (off `R0`) into `L_z=iota-z mu=(A0-tau_3[W]_E)-z(B0-tau_3 b)`:

```text
L_z = (p1 - z q1 - tau_3)[W]_E + (p2 - z q2 + z tau_3) b.
```

Collecting the `B`-affine structure `L_z = c0(z) + tau_1 c1(z) + tau_2 c2(z) + tau_3 c3(z)` with `p_i=p_i^0+p_i^1 tau_1+p_i^2 tau_2`, `q_i` likewise:

```text
c1(z) = (p1^1 - z q1^1)[W]_E + (p2^1 - z q2^1) b,
c2(z) = (p1^2 - z q1^2)[W]_E + (p2^2 - z q2^2) b,
c3(z) = -[W]_E + z b,
c0(z) = (p1^0 - z q1^0)[W]_E + (p2^0 - z q2^0) b.      (c0 made explicit)
```

`c1,c2,c3` match the prompt and the ledgers verbatim. The `[W]_E`-row of `c3` is `-1`, the `b`-row is `z` — consistent everywhere. No index mismatch found; I proceed with these.

---

## PROOF — realification identity, degree bound, and the safe side `Q != 0 => O(p)`

Write each column in the F-basis `{[W]_E,b}` as `c_i = f_i[W]_E + g_i b`, giving F-coordinates
`(f_1,g_1),(f_2,g_2),(f_3,g_3)=(-1,z),(f_0,g_0)`, each `f_i,g_i ∈ F` affine in `z`. Let `δ = α - α^τ ∈ F^*` (`τ` = the F/B-involution), so `δ^2 ∈ B^*`. Realifying `A ≅ B^4` in the B-basis `{[W]_E, α[W]_E, b, αb}`, the 4×4 B-determinant equals the conjugate-doubled F-determinant up to the basis discriminant:

```text
Q(z) = (1/δ^2) · det_F [ N ; N^τ ],     N = [ f_1 f_2 f_3 f_0 ; g_1 g_2 g_3 g_0 ].
```

(Verified on the `F=ℂ,B=ℝ` model: `det=−4`, `δ^2=−4`, `Q=1`.) Since `δ^2 ∈ B^*`, **`Q != 0 ⟺ det[N;N^τ] != 0`**.

**Degree.** Each `f_i,g_i` is degree `≤1` in `z`, so each 2×2 F-minor `m_{ij}(z)` is degree `≤2` in `z`. Treating `z = z_0+α z_1`, the conjugate factor `m_{kl}(z)^τ` is degree `≤2` in `(z_0,z_1)`; hence every Laplace term `m_{ij}(z)m_{kl}(z)^τ` and therefore `Q(z_0,z_1)` has **total degree `≤ 4`** in `(z_0,z_1) ∈ B^2`.

**Safe side.** If `Q ≢ 0`, then by Schwartz–Zippel a nonzero degree-`d` polynomial over `F_p` in `2` variables has `≤ d·p` zeros, so

```text
C2 ≤ #{ z ∈ F : Q(z_0,z_1)=0 } ≤ 4p = O(p) = O(n).
```

This is unconditional (given `R0`-complement, where `{[W]_E,b}` is a basis) and reproduces the Cycle 15 "`Q!=0 ⟹` curve-sized" side with an explicit constant `4p`. ∎

---

## BANKABLE_LEMMA — determinant–trace formula tying `Q` to the slope quadratic

Identify the column-3 minors with the Cycle 14 slope-quadratic coefficients. With `Φ_i(z) := q1^i z^2 - (p1^i - q2^i) z - p2^i` (so the landing quadratic is `Φ(z,tau)=Φ_0+Φ_1 tau_1+Φ_2 tau_2 = q1 z^2-(p1-q2)z-p2`):

```text
m_{13} = z f_1 + g_1 = -Φ_1(z),
m_{23} = z f_2 + g_2 = -Φ_2(z),
m_{34} = -(g_0 + z f_0) = Φ_0(z).
```

Laplace expansion of `det[N;N^τ]` along its first two rows, using `Tr(x)=x+x^τ`, gives the exact identity

```text
δ^2 · Q(z) = Tr( m_{12} Φ_0^τ ) + Tr( Φ_1 m_{24}^τ ) - Tr( m_{14} Φ_2^τ ),
```

where `m_{12},m_{14},m_{24}` are the (z-affine, degree `≤2`) minors of the `{tau_1,tau_2,const}` columns `{c1,c2,c0}`. The same minors obey the Grassmann–Plücker relation

```text
m_{12} Φ_0 + Φ_1 m_{24} - m_{14} Φ_2 = 0   (identically in z, over F).
```

Thus `Q` is precisely the **`τ`-twisted (trace) version of the Plücker combination whose untwisted version is identically zero.** This is exact and source-checkable from the Cycle 14 forms; it does not bound `C2` by itself.

---

## EXACT_NEW_WALL — `W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER-RANK-DET-SPLIT`

### (i) Closed criterion for `Q ≡ 0`

View `z,w` as independent (the change `(z_0,z_1) ↦ (z,z^τ)` is an F-linear isomorphism). Set
`U(z)=(m_{12},Φ_1,-m_{14})`, `V(z)=(Φ_0,m_{24},Φ_2)` with monomial-coefficient vectors `U_k,V_l ∈ F^3` (`k,l ∈ {0,1,2}`), and `H_{kl} := U_k · V_l^τ ∈ F` (ordinary dot product). Then

```text
δ^2 Q  =  Σ_{k,l} ( H_{kl} + H_{lk}^τ ) z^k w^l ,
so      Q ≡ 0   ⟺   H_{kl} + H_{lk}^τ = 0   for all k,l ∈ {0,1,2}.
```

This is a finite, exactly checkable **conjugate-skew Gram criterion** (9 entries; diagonal forces `Tr(U_k·V_k^τ)=0`). It is the requested symbolic classification of `Q==0`. The Plücker relation gives the companion *untwisted* identity `Σ_{k+l=m} U_k·V_l = 0`; `Q≡0` is the *independent* twisted condition, so generic data has `Q ≢ 0`.

### (ii) `Q ≡ 0 ⟺` the slope map is dominant on the resonance surface

On `Ra` (Cycle 13: `Delta ∈ F^*·\bar B[tau]`), `Ψ(tau) := (p1-tau_3)(q2-tau_3)-p2 q1 ∈ B[tau]`, so the landing locus `Sigma = {Ψ=0}` is one B-quadric **surface** (`~p^2` points), and the slope is the rational map `z = (p1-tau_3)/q1 : Sigma → F`. Because `Q` of degree `≤4 < p`, `Q≡0 ⟺` `z` is dominant (image cofinite, `Θ(p^2)`), and `Q≢0 ⟺` image `O(p)`.

### (iii) Correction (forbidden-overclaim guard): `Q ≡ 0` does NOT yield a counterpacket by itself

`Q` is pure B-linear algebra over all `tau ∈ B^3`; it ignores the split-cubic constraint. A dimension count *suggests* `Q ≡ 0` is the **generic** behaviour on `Ra` (on `Sigma`: 3 unknowns `tau`, landing `Ψ=0` is 1 B-equation, `slope=z` is 2 B-equations → `3=3`, solvable for a positive fraction of `z`). So the naive lemma "prove `Q != 0` on all `Ra/Rb`" is **likely false**, and a bare `Q≡0` example is **not** a counterpacket. The actual MCA count requires `tau` to be a genuine **`D`-split cubic with distinct roots** in `F_p`:

```text
RESIDUAL WALL: when Q ≡ 0 on a source-valid resonance surface Sigma,
does z restricted to split-distinct co-supports T ⊂ D=F_p realise
Θ(p^2)=Θ(q_line) distinct slopes, or does the split-distinct locus
collapse the image to O(p)?
```

This is exactly the old fixed-slope fiber-collapse problem, now isolated to the single case `{Q≡0} ∩ {split-distinct}`. The only mounted empirical datum (`forced_ra_slope_scan`, `p=7`, 12 seeds, `C2≤6`, EXPERIMENTAL) is *consistent with collapse* and in tension with the genericity heuristic — most plausibly a small-`p` effect or a real collapse; it cannot decide the scaling law. I therefore do **not** bank slope collapse, do **not** bank a `Θ(q_line)` counterpacket, and make no `q_gen`/protocol/list-decoding claim.

### (iv) Scanner spec (exact I/O / certificate) to resolve the residual wall

```text
INPUT : prime p; E (deg 2, separated, aperiodic, nonzero on F_p); Bnum (deg<2, b!=0);
        base anchors w0,w1: F_p->F_p ; n=p, a=n-3, k=n-5.
DERIVE: A0,B0 (Cycle 14) -> p_i^j,q_i^j ∈ F  -> columns c1,c2,c3,c0.
STEP A (resonance filter): compute Delta=Delta_0+α Delta_1; keep only data in
        Ra (Delta_0,Delta_1 B-proportional) or Rb (shared \bar B-linear factor).
STEP B (Q-test): evaluate H_{kl}=U_k·V_l^τ; flag Q≡0 iff H_{kl}+H_{lk}^τ=0 ∀k,l
        (cross-check: deg(Q)≤4, sample Q at 5p+1 points (z_0,z_1)).
STEP C (count, Q≡0 branch only): enumerate split-distinct T⊂F_p (|T|=3),
        record z(T)=(p1-tau_3)/q1; output C1, C2=#distinct z, fiber histogram of z,
        and max over seeds.
CERTIFICATE (per instance):
  { p, E, Bnum, w0, w1, stratum∈{Ra,Rb}, Q_identically_zero:bool,
    degQ, H_matrix, C1, C2, fiber_sizes:[...], split_triples_examined,
    status∈{PASS_Qnonzero_O(p), OPEN_Qzero_collapse?, COUNTERPACKET_C2~p^2} }
PASS  : Q!=0  (then C2≤4p proven).
TRIGGER (counterpacket, sub-reserve): a reproducible family with Q≡0 AND
        C2/p^2 bounded below across growing p. A single p is insufficient.
```

---

## What is and is not banked

- BANKABLE_LEMMA (new, exact): `δ^2 Q = Tr(m_{12}Φ_0^τ)+Tr(Φ_1 m_{24}^τ)-Tr(m_{14}Φ_2^τ)`, the minor↔slope-quadratic identities `m_{13}=-Φ_1, m_{23}=-Φ_2, m_{34}=Φ_0`, the Plücker relation, and `Q≢0 ⟹ C2≤4p=O(n)` off `R0`.
- EXACT_NEW_WALL (primary): `Q≡0 ⟺ H_{kl}+H_{lk}^τ=0 ∀k,l ⟺` slope map dominant on `Sigma`; and the corrected residual wall is the **split-distinct realisation** inside `{Q≡0}`, not `Q≡0` alone.
- NOT claimed: any proof of `conj:B`; slope collapse on `Ra/Rb`; a `Θ(q_line)` counterpacket; that rank 3 alone decides; any result above corrected reserve; any `q_gen` collapse; any protocol/MCA/CA/list-/line-decoding/SNARK consequence; no reuse of the generic complete-intersection lemma for `Ra/Rb`.

## Classification

```text
EXACT_NEW_WALL
```
