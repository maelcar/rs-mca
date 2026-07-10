# CAP25 v13 raw: KB signed-e_m inverse — primitive Fourier participation factors through twist orbits; a w=2, avg>>1 scaled toy is mixed-orbit led

Status: `PARTIAL / AUDIT`. Per claim:

- `REFERENCE`: the exact KoalaBear MCA `a_+=1116048` signed-`e_m` target and
  first-match constants already integrated in
  `cap25_v13_q_em_inverse_participation_ratio.md` (was #414);
- `PROVED`: the Fourier-side twist-orbit corollary
  `PR(Rhat_prim)=n*PR(orbit amplitudes)`, a quantitative specialization of the
  existing twist-orbit machinery;
- `MEASURED`: the exact-fiber / floating-spectrum row
  `(p,n,m,w)=(193,64,30,2)`, the first shipped multiplicative-domain toy with
  both `w>=2` and `avg>>1` at deployment-scaled density and prefix depth;
- `OPEN`: the deployed raw or masked signed-`e_m` inverse, and hence the
  row-sharp Q atom and `U(1116048)<=B*`.

**Verifier:**
`experimental/scripts/verify_kb_signed_em_scaled_toy_audit.py`
(zero argument, stdlib only, self-capped by `RLIMIT_AS` at 2 GiB,
`KB_SIGNED_EM_AS_CAP_GB` / `KB_SIGNED_EM_DATA_DIR` knobs, about 21 seconds,
`RESULT: PASS (52/52 checks)`, exit 0). Data:
`experimental/data/cap25_v13_kb_signed_em_scaled_toy_audit.json`.

## What this is / is not

The integrated participation-ratio packet already contains the KB-MCA
signed-`e_m` formulation, exact `Krem`, structural lemmas L1--L3, dead-route
cuts, and small toys. This is therefore **not** a KB analogue of the M31 packet
and does not restate #414 as new work.

The new theorem-level content is narrower: the existing twist action on the
multiplicative KB domain gives an exact Fourier-orbit factorization of the
primitive participation ratio. At the `Gamma2-1=1` reference, it converts the
KB primitive target from about `2^44.392` modes to about `2^23.392` twist-orbit
amplitudes. The new experiment then instruments those amplitudes on a
`w=2, avg>>1` density/prefix-depth scaled row. It finds strong spectral
concentration, but the heavy mass is **mixed primitive**, not monomial, on this
toy.

The toy has subgroup index `3`, while deployment has index `1016`. Its entire
nonzero frequency space has only `37248` modes, already below the deployed
reference budget `23088082660036`. Thus the toy tests spectral shape and closes
#414's explicit `w>=2, avg>>1` instrumentation gap; it cannot certify or
falsify the deployed inverse.

---

## 1. Exact deployed KB statement and constants  `REFERENCE`

For the active KoalaBear MCA row:

```text
p = 2^31 - 2^24 + 1 = 2130706433
n = 2^21 = 2097152
k = 2^20 = 1048576
a_+ = 1116048
m = n-a_+ = 981104
w = a_+-(k+1) = 67471
B* = 274980728111395087
```

Writing `C=binom(n,m)` and `P=p^w`, the verifier independently derives:

```text
floor(C/P) = 57198030365
ceil(C/P)  = 57198030366
t*p reservation = 143763024447376
Brem = B* - t*p = 274836965086947711
floor(B* P/C)    = Kraw = 4807520
floor(Brem P/C)  = Krem = 4805007
floor(Krem C/P)  = target_floor = 274836936291722953
Kraw-Krem = 2513
```

For `D=alpha*mu_n`, define the moment-prefix fiber count

```text
N(z) = #{M subset D: |M|=m, Phi_w(M)=z},
Phi_w(M) = (sum_{x in M} x, ..., sum_{x in M} x^w),
```

and its nonzero Fourier spectrum

```text
E(t) = sum_{|M|=m} e_p(t.Phi_w(M))
     = e_m((e_p(f_t(x)))_{x in D}),
f_t(x) = sum_{i=1}^w t_i x^i.
```

The raw sufficient certificate from #414 is

```text
(STAR)  sum_{t!=0} |E(t)| <= (Krem-1) C.
```

With

```text
Gamma2 = p^w sum_z N(z)^2/C^2,
PR(Rhat) = ||E||_1^2/||E||_2^2,
||E||_2^2 = C^2(Gamma2-1),
```

this is exactly

```text
PR(Rhat) <= (Krem-1)^2/(Gamma2-1).
```

At `Gamma2-1=1`,

```text
nu_ref = (Krem-1)^2 = 4805006^2 = 23088082660036 = 2^44.392214.
```

As #413/#414 already emphasize, `(STAR)` is sufficient and possibly
overstrong. The theorem-facing first-match object is a masked residual. No
raw-to-masked equivalence is claimed here.

## 2. Fourier-side twist-orbit participation corollary  `PROVED`

Let `H=mu_n`. For `h in H`, act on a frequency by

```text
h.t = (h t_1, h^2 t_2, ..., h^w t_w).
```

Then

```text
f_{h.t}(x) = f_t(hx).
```

Multiplication by `h` permutes `D=alpha H`, so the two value multisets are
identical and therefore

```text
E(h.t) = E(t).
```

If `I(t)={i:t_i!=0}`, the stabilizer has size
`gcd(n,I(t))`. Primitive modes have `gcd(n,I(t))=1`, hence full orbit size `n`.
For primitive twist orbits `O`, put `a_O=|E(t_O)|`. Then

```text
||E_prim||_1   = n sum_O a_O,
||E_prim||_2^2 = n sum_O a_O^2,
PR(E_prim)     = n (sum_O a_O)^2/(sum_O a_O^2)
               = n PR_orbit(a).
```

This is the Fourier-side participation-ratio corollary of the already-known
twist-orbit constancy / moment amplification (`prop:twist-orbit`,
`prop:q-orbit-moment`; #412). The symmetry is not new; the exact PR
factorization and its deployed orbit-amplitude calibration are recorded here.

## 3. Deployed primitive reference becomes an orbit-amplitude target  `REDUCED`

If quotient frequencies are separately routed and the primitive raw spectrum
is assigned the `Gamma2-1=1` reference budget, then

```text
PR_orbit(a) <= nu_ref/n
            = 23088082660036/2097152
            = 5772020665009/524288
            = 11009255.723970413
            = 2^23.392214.
```

Thus the primitive side of #431 node `O414` can be stated as an effective
support bound on about eleven million **orbit amplitudes**, rather than on
individual modes. This does not close the node:

1. the true budget contains the actual `Gamma2-1`, not its reference value;
2. raw quotient `L1` mass needs an explicit compatible allocation;
3. participation ratios of primitive and quotient pieces do not add;
4. a masked residual inherits the factorization only if its mask is stable
   under `M -> hM` (or an equivalent orbit-closure theorem is proved).

## 4. The scaled toy and its exact scope  `AUDIT`

The row

```text
p=193, n=64, m=30, w=2, D=mu_64, [F_p^*:D]=3
```

was chosen because

```text
w/n = 0.03125          vs deployment 0.03217268  (within 3%)
m/n = 0.46875          vs deployment 0.46782684  (within 0.3%)
avg = binom(64,30)/193^2 = 2^45.306 >> 1.
```

This directly removes the `w>=2` / `avg<<1` confound in #414's shipped
`w>=2` toys. It does **not** preserve the multiplicative-coset index:

```text
toy index = 3, deployment index = (p_KB-1)/2^21 = 1016.
```

The correct label is therefore **density/prefix-depth scaled**, not
geometry-faithful.

## 5. Exact prefix-fiber computation  `PROVED` arithmetic

The verifier computes all `193^2=37249` fibers by an exact slice/group-ring DP.
After processing a root `x`, it updates

```text
F_j(z_1+x, z_2+x^2) += F_{j-1}(z_1,z_2)
```

in descending `j`. Since

```text
C=binom(64,30)=1620288010530347424 < 2^64,
```

unsigned 64-bit cells are exact. The replay gives:

```text
sum_z N(z) = C
all 37249 fibers nonempty
min_z N(z) = 43498831840209
max_z N(z) = 43498834049408
Rmax = 193^2 max_z N(z)/C = 1.000000036398
Gamma2-1 = 1.92055067611e-17.
```

So this row is extremely flat by direct exact enumeration.

## 6. Orbit-compressed signed-e_m spectrum  `MEASURED`

The dual twist action partitions the `37248` nonzero modes into

```text
579 primitive orbits of size 64
6 pure-quadratic quotient orbits of size 32
585 total orbits.
```

The verifier evaluates one signed-`e_m` coefficient per orbit, expands with the
proved multiplicity, and obtains:

```text
L1/C                         = 0.000000059246
PR(all nonzero modes)        = 182.765769449915
PR/(p^w-1)                   = 0.004906727058
PR(primitive modes)          = 169.819296027248
PR(primitive orbit amplitudes)= 2.653426500426
primitive L1 share           = 0.961949273138
Fourier triangle / true max  = 1.000000022848.
```

The numerical spectrum is independently guarded by:

- exact-fiber Parseval, relative error `3.4e-15`;
- forward/reverse coefficient-DP aggregate agreement below `5e-16`;
- multiplicative-coset offset agreement below `1.5e-15`;
- a worst individual order drift below `2.3e-10` at tiny coefficients;
- JSON replay plus live parameter/fiber/orbit/status tamper rejection.

The mode split is:

| mode class | L1 share | L2 share |
|---|---:|---:|
| linear (`t_1!=0,t_2=0`) | `0.000002278292` | about `1e-11` |
| mixed primitive (`t_1 t_2!=0`) | `0.961946994846` | `0.995891818575` |
| quadratic quotient (`t_1=0,t_2!=0`) | `0.038050726862` | `0.004108181415` |

Two mixed primitive twist orbits carry `0.993360183338` of all `L2` energy.
The concentration profile is:

| mass level | L1 orbits / modes | L2 orbits / modes |
|---|---:|---:|
| 50% | `2 / 128` | `2 / 128` |
| 90% | `6 / 352` | `2 / 128` |
| 99% | `52 / 3232` | `2 / 128` |

Therefore this toy is spectrally sparse, but it is **not monomial-led**. That
statement is local to `(193,64,30,2)` and does not refute #414's L3 monomial
collapse lemma: L3 identifies monomial value distributions; it does not claim
monomial directions dominate every row.

## 7. Falsification guard and the next atomic statement  `OPEN`

The automatic checks

```text
PR <= nu_ref/(Gamma2-1),
L1/C <= Krem-1
```

are not evidence here: the whole toy frequency space has only `37248` modes,
already much smaller than `nu_ref`. They are retained only as algebraic sanity
guards.

The nontrivial observation is the orbit-amplitude concentration. The next
atomic statement for the raw primitive route is:

> After quotient routing, bound the number and total weight of heavy **mixed
> primitive twist orbits** so that the orbit-amplitude participation ratio fits
> `5772020665009/524288` at the `Gamma2-1=1` reference, with the actual energy
> and quotient budget printed.

An equivalent threshold/tail formulation would bound, uniformly in `lambda`,

```text
#{O primitive mixed: a_O >= lambda C}
and
sum_{O: a_O < lambda C} a_O,
```

at the deployed row. If the theorem-facing object is the masked residual, a
twist-stable mask or an explicit orbit-closure payment is a prerequisite.
Without that, the raw orbit corollary cannot simply be transferred to `E_Q`.

No faithful-to-scope counterexample was found. The deployed inverse remains a
proof-method wall, not a theorem established by this experiment.

## 8. Weave  `AUDIT`

- **#414 / integrated participation-ratio packet.** This packet extends it; it
  does not duplicate its KB formulation, L1--L3, toys, or dead-route table.
- **#412 / concentration floor.** The equal-mass twist-orbit machinery is
  existing input. The new item is its exact Fourier PR specialization and the
  deployed orbit-amplitude calibration.
- **#431 barrier map, `O414 -> A397`.** This narrows the Fourier side to heavy
  primitive mixed orbit amplitudes. It does not identify or prove #397's primal
  full-rank signed-defect certificate and does not move the edge.
- **#434 M31 signed-`e_m` packet.** M31 uses a Chebyshev/twin-coset domain. The
  present multiplicative twist action is KB-specific and is not transferred to
  M31.
- **#413/#416/#417 masked lineage.** Raw `(STAR)` remains possibly overstrong.
  Masked participation is the tighter target, but lift-class removal is not a
  free payment and mask invariance is not assumed here.
- **`def:q-row-atom` / `prob:row-sharp-q`.** Both remain open at the deployed
  row.

## 9. Nonclaims

This packet does **not** prove:

```text
U(1116048) <= B* or any deployed adjacent safe row;
the raw signed-e_m inverse at KB-MCA;
the masked signed-e_m / participation bound;
def:q-row-atom or prob:row-sharp-q;
transfer from toy subgroup index 3 to deployed index 1016;
twist-orbit invariance for a first-match mask not proved twist-stable.
```

## 10. Reproduce

```bash
ulimit -v 2097152
python3 experimental/scripts/verify_kb_signed_em_scaled_toy_audit.py
# RESULT: PASS (52/52 checks), exit 0, about 21 seconds
```
