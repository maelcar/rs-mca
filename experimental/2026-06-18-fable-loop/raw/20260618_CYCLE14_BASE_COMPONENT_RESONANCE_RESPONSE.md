I've read the wall ledger, banked lemmas, and cut routes. Note: code execution is disabled in this harness (the Jupyter tool was denied and no shell tool is exposed), and the Cycle 12/13 scanner scripts live outside this snapshot, so this is an analytic-only run. I worked the algebra directly from the banked Cycle 12/13 identities. Here is the result.

---

## W-F1-AA-RES-T2J3-BASE-COMPONENT-RESONANCE — analysis

Ledgers kept separate throughout: `B=F_p` (`q_gen=p`), `F=F_{p^2}` (`q_line=p^2`), `q_chal` unused, `D=F_p` so `n=|D|=p`, `t=σ=2`, `j=3`, `a=n-3`, `k=n-5`.

### 1. Reduction of `Delta` to two affine‑linear `A`-valued forms

Work in `A=F[X]/E`, `dim_F A=2`, with the `F`-valued wedge `u∧v=det` in basis `{1,X}`. Set `b:=[Bnum]_E≠0`, `m:=[L_T]_E`. From the Cycle 12 determinant form,

```text
Delta = Psi ∧ (m·b),   Psi := [W]_E·m − [L_D]_E·[Q_S]_E.
```

Using the Cycle 12 quotient (for `D=F_p`)
`Q_S = W_{n-1}(X^2−τ1 X+τ2)+W_{n-2}(X−τ1)+W_{n-3}`,
`Q_S` is affine‑linear in `(τ1,τ2)` and independent of `τ3`, while `m=[L_T]_E` is affine‑linear in `(τ1,τ2,τ3)` with `∂m/∂τ3=−1`. Hence define the two **`A`-valued affine‑linear** forms

```text
ι(τ) := m·[I_S]_E = Psi(τ)      (landing numerator),
μ(τ) := m·b      = [L_T]_E·b.
```

Both are linear in `τ`, and isolating `τ3` (since `∂m/∂τ3=−1`):

```text
ι(τ) = A0(τ1,τ2) − τ3·[W]_E,
μ(τ) = B0(τ1,τ2) − τ3·b.
```

Landing `[I_S]_E∈F·b ⇔ ι∈F·μ ⇔ Delta:=ι∧μ=0`. Expanding reproduces the banked leading coefficient exactly:

```text
Delta = (A0∧B0) − τ3·(A0∧b + [W]_E∧B0) + τ3^2·([W]_E∧b),
[τ3^2]Delta = [W]_E∧b = c2.
```

`c2≠0` off `R0={[W]_E∧[Bnum]_E=0}`; there `{[W]_E,b}` is an `F`-basis of `A`.

### 2. The slope as an explicit ratio, and the base‑rationality coupling

On landing, `[I_S]_E=z·b` with `z∈F` (unique since `b≠0`, per the Cycle 2 caveat), equivalently `ι=z·μ`. Expanding `A0,B0` in the basis `{[W]_E,b}` as `A0=p1[W]_E+p2 b`, `B0=q1[W]_E+q2 b` (with `p_i,q_i∈F` affine‑linear in `(τ1,τ2)`) and matching components of `ι=zμ` gives the **slope quadratic**

```text
q1·z^2 − (p1−q2)·z − p2 = 0,     τ3 = p1 − z·q1.
```

The second identity is the decisive one: `τ3=e_3(T)∈B`, while `p1,q1∈F`. So every realized slope must satisfy

```text
(base-rationality)   p1(τ1,τ2) − z·q1(τ1,τ2) ∈ B,   (τ1,τ2)∈B^2.
```

Equivalently `z=ι/μ=(A0∧b − τ3 c2)/(B0∧b)`, a ratio of `F`-valued forms.

### 3. `Ra` and `Rb` analyzed directly

`Ra` (`Delta∈F^*·\bar B[τ]`): `Delta=c2·g`, `g=τ3^2−(c1/c2)τ3+c0/c2∈B[τ]` monic in `τ3`. The landing set `Σ={g=0}` is a **quadric surface** in `B^3`: for each `(τ1,τ2)∈B^2` at most two `B`-roots `τ3`, so `#Σ_B=Θ(p^2)`.

`Rb` (`Delta` has a `\bar B`-linear factor common to `Delta_0,Delta_1`): the common zero contains a **plane**, again `Θ(p^2)` split candidates.

In both cases the landing locus is genuinely 2‑dimensional, so the Cycle 13 complete‑intersection bound `#landings=O(p)` fails on the locus. The remaining question is purely about the **slope image**, `C2=#{z}`.

Decisive structural point: `z∈F` is **two** `B`-coordinates `(z_0,z_1)`, so the map `Z:(τ1,τ2)↦z` from a 2‑dimensional base set need not have 1‑dimensional fibers — there is **no dimension reason** forcing `C2=O(p)`. The only candidate collapse mechanism is the base‑rationality constraint `p1−z q1∈B`. That constraint pins the `α`-part of `z` to a `B`-line per `(τ1,τ2)`, but `z` is already pinned to one point by `ι/μ`, so it is an automatic consistency relation, **not** an extra cut on the image. I therefore find **no proof of collapse**, and equally **no obstruction** to `z` filling up to `Θ(p^2)=Θ(q_line)` values on a resonance surface.

### 4. Do source hypotheses exclude the resonance?

No exclusion is provable here. `E` separated forces `E∉B[X]` (`E^σ≠E`), so its coefficients are genuinely in `F`; this makes `c2,A0∧b,B0∧b∈F\B` generically, which is exactly what permits a 2‑dimensional slope image. The resonance conditions `Ra,Rb` are positive‑codimension *closed* conditions on `(E,Bnum,w0,w1)`; the source hypotheses (separated/aperiodic/`deg E=2`/nonzero on `D`; `[Bnum]_E≠0`; arbitrary base anchors) are *open* and do not contradict them. The earlier Codex scans (`max_C2=5`, `coeff_component_rank=2`, `zeros_all_B3=O(p)` at `p=7,11,17`) are off‑resonance generic samples and carry no information about the measure‑zero resonance locus. So this is **not a ROUTE_CUT**.

### 5. Why not the other classifications

- Not **BANKABLE_LEMMA**: I could not prove slope collapse; the base‑rationality coupling is consistency, not a fiber bound, and the slope map has enough `B`-coordinates to be generically finite on a surface.
- Not **COUNTERPACKET**: exhibiting a source‑valid `Ra`/`Rb` family with `Θ(q_line)` distinct slopes requires a finite search/symbolic construction I cannot execute in this harness; asserting one would violate the "no result above corrected reserve unless verified" guard.
- Not **PROOF**: nothing here touches `conj:B`, `q_gen`, or any protocol/MCA/CA/list-/line-decoding consequence.

---

## Classification: EXACT_NEW_WALL

The resonance strata `Ra`/`Rb` are reduced to a single sharper, checkable invariant that replaces the coarse "common surface component" description. The whole `C2` question on the resonance surface collapses to a **slope‑fiber dimension** statement for an explicit map:

```text
W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER

Off R0, on a resonance surface Σ ⊂ B^3 (Ra: Σ={g=0} a B-quadric;
Rb: Σ ⊇ a B-plane), with the explicit forms
    ι(τ)=A0(τ1,τ2)−τ3[W]_E,   μ(τ)=B0(τ1,τ2)−τ3·b,
    z = ι/μ ∈ F  determined by   q1 z^2 −(p1−q2) z − p2 = 0,  τ3 = p1 − z q1 ∈ B,
bound  C2 = #{ z : (τ1,τ2,τ3)∈Σ, X^3−τ1X^2+τ2X−τ3 splits with distinct roots in D }.

C2 = O(p)=O(n)  iff the map  Z:(τ1,τ2) ↦ z  has 1-dimensional fibers on Σ
(equivalently the base-rationality constraint p1 − z q1 ∈ B forces a
1-dimensional z-image); otherwise C2 can reach Θ(p^2)=Θ(q_line).
```

New banked facts from this run (all `D=F_p`, `t=σ=2`, `j=3`, off `R0`):

1. `Delta=ι∧μ` with `ι,μ` `A`-valued **affine‑linear** in `τ`, `ι=A0−τ3[W]_E`, `μ=B0−τ3 b`; recovers `[τ3^2]Delta=[W]_E∧b`.
2. Explicit slope: `z=(A0∧b−τ3·([W]_E∧b))/(B0∧b)`, with slope quadratic `q1 z^2−(p1−q2)z−p2=0` and the **base‑rationality coupling** `τ3=p1−z q1∈B`.
3. On `Ra`/`Rb` the landing locus is a 2‑dim surface, so the Cycle 13 complete‑intersection count does **not** apply, and there is **no dimension‑theoretic collapse** of the slope image — `z` carries two `B`-coordinates and can be generically finite on a surface.
4. The only remaining collapse mechanism is the base‑rationality slope‑fiber law in `W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER`; this, not "common surface component," is the exact live obstruction.

Caveats / non‑claims: this is analytic only (no scanner run available); the resonance surface is not shown source‑empty, slope collapse is not proven, and no `Θ(q_line)` counterpacket is constructed. Nothing here proves `conj:B`, asserts a result above corrected reserve, claims a `q_gen` collapse, or yields any protocol/MCA/CA/list-/line-decoding consequence. The `sub‑reserve η=2/n` status is unchanged.
