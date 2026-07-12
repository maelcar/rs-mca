# A6 all-witness line-section compiler

**Status:** proved experimental theorem, conditional only on the cited
characteristic-free Noether-form theorem.

**Lane:** asymptotic A6 / hard input 3, canonical two-block stress family.

## Statement

Fix an integer `r>=1` and the canonical source parameters

```text
N=500r,  kappa=225r,  t=150r,  d=250r.
```

Work over any field containing the `N` distinct evaluation points. Fix one
received line and one active weighted-RS chart. Let `Z` be any set of slopes
which retain at least one actual completed witness of weight at most `t` on
that line. Then

```text
|Z| <= 1960 + 3744(1400r+5)^6.                         (1)
```

The bound is independent of the field size, of a witness selector, and of
the first-match order. In particular `|Z|=poly(r)=exp(o(N))`.

The theorem applies before partitioning by the punctured weight `e`.
Consequently it pays the entire fixed-line canonical A6 stress instance,
including the previously open strict central band `50r<e<100r`.

## Source interfaces

The canonical source construction supplies two facts used below.

1. Every actual completed witness has a polynomial representative `f` of
   degree less than `kappa` and a completed polynomial
   `C_gamma=f+Y+gamma V` with at least `N-t` evaluation-domain zeros.
2. Completed witnesses at two distinct slopes have at most `N-d` common
   evaluation-domain zeros. This follows from the literal minimum-lift
   distance `d`, not from an abstract mask-transversality assumption.

The source-valid nonvacuity and the equality `d=250r` are proved in
`completed_zero_mask_two_block.md`.

## One polynomial for every witness

Put

```text
w=kappa-1=225r-1,  m=4,  L=52,  D=1400r-1.
```

Let `Q` range over the span of the monomials

```text
X^alpha Z^beta W^c,
alpha+cw<=D,  beta+c<=L.                                (2)
```

At each evaluation point `x`, impose multiplicity four in the ideal

```text
I_x=(X-x, W+Y(x)+ZV(x)).                                (3)
```

Writing `A=X-x` and `T=W+Y(x)+ZV(x)`, reduction modulo `(A,T)^4`
shows that one coordinate imposes at most

```text
C=sum_(j=0)^3 (4-j)(52-j+1)=520                         (4)
```

linear conditions. The number of available monomials is

```text
U=sum_(c=0)^6 (53-c)((1400-225c)r+c)
 =260050r+1022,                                         (5)
```

where `floor(D/w)=6`. Since `NC=260000r`, the surplus is
`50r+1022>0`; hence a nonzero `Q` satisfying (3) exists.

Now take any actual witness at slope `gamma`. Substitution
`Z=gamma, W=f(X)` gives a polynomial of degree at most `D`. Every one
of the at least `N-t=350r` agreement points is a zero of multiplicity four,
so it has more than `D` zeros counted with multiplicity. Therefore

```text
Q(X,gamma,f(X))=0                                       (6)
```

identically. The same `Q` works for every actual witness; no selector was
used to construct it. This argument uses ideals rather than derivatives and
is valid in every characteristic.

## Specialization spectrum

Remove the `F[Z]`-content of `Q`. Its roots cost at most `L=52` slopes.
Over the algebraic closure of `F(Z)`, group the positive-`W`-degree factors
of the primitive polynomial into field-of-definition orbits. For orbit `i`,
let `q_i` be the degree, including inseparable degree, of its factor cover.
The orbit norms divide `Q`, so

```text
sum_i q_i <= q := deg_W Q <= 6.                         (7)
```

The coefficient map of `Q` has projective `Z`-degree at most `L`.
The projective multiplication identity `mu^*O(1)=O(1,1)` therefore bounds
the coefficient-map degree of the chosen factor on its cover by `q_i L`.

We import the characteristic-free integral Noether forms of Kaltofen,
Theorem 7, whose coefficient degree is at most `12 Delta^6` for a form of
degree `Delta`:

E. Kaltofen, *Effective Noether irreducibility forms and applications*,
J. Comput. Syst. Sci. 50 (1995), 274--295,
<https://doi.org/10.1006/jcss.1995.1023>.

Here every factor has total degree at most

```text
Delta <= D+q = 1400r+5.                                 (8)
```

Pulling back one generically nonzero Noether form charges at most
`12 q_i L Delta^6` reducible specializations on cover `i`.

There is one additional exceptional locus which reducibility forms do not
detect: the factor's `W`-degree can drop on specialization. A generically
nonzero leading-`W` coefficient is a section of degree at most `q_i L`, so
these fibers cost at most `q_i L`. This charge is necessary: for example,
`sW^2+W-X^2` remains irreducible at `s=0` while its `W`-degree drops.

After projecting exceptional cover points to slopes and summing (7), the
exceptional slope set `E` satisfies

```text
|E| <= L + qL(12 Delta^6+1)
     <= 52 + 3744(1400r+5)^6 + 312.                     (9)
```

Outside `E`, every graph factor `W-f(X)` in a specialized fiber comes from a
generic factor of `W`-degree one. Thus every nonexceptional actual witness
lies on one of finitely many integral factor covers, with total cover degree
at most six. This includes repeated, Galois, and purely inseparable factors.

## Moving-root count

On a `W`-linear factor cover write the factor as `A(X)W+B(X)` and form the
completed numerator

```text
P(X)=A(X)(Y(X)+pi V(X))-B(X).                            (10)
```

If the cover degree is `q_i`, the projective polynomial map defined by `P`
has degree at most

```text
delta_i <= q_i(L+1).                                    (11)
```

Assign each nonexceptional slope one representing cover point. On a cover
carrying at least two assigned slopes, the common fixed domain-root set has
size at most `N-d`; hence each assigned completed polynomial has at least
`d-t=100r` nonfixed roots. A nonfixed evaluation root cuts a hyperplane
section of degree at most `delta_i`. Double counting gives

```text
|Z_i|(d-t) <= N delta_i.                                (12)
```

The covers carrying at most one assigned slope contribute at most `q=6`.
Using (7) and (11),

```text
|Z\E| <= 6 + floor(N q(L+1)/(d-t))
      = 6 + 1590 = 1596.                               (13)
```

Adding (9) and (13) proves (1).

## Why this moves the board

Earlier A6 charges use a fixed witness selector, a nonnegative exponent
branch, or a bounded actual-core rank. The construction above is genuinely
all-witness: one interpolation polynomial contains every completed witness
on the fixed received line. The specialization and moving-root steps then
turn that universal containment into a polynomial distinct-slope bound.

This closes the canonical fixed-line hard-input-3 stress instance. It does
not sum the result over an unbounded collection of received lines, active
charts, or realized profiles; that still requires a witness-exhaustive
subexponential atlas.

## Audit correction record

The originating worker proposed an unsupported quartic Noether bound and did
not charge vertical-degree-drop fibers. Two independent hostile audits found
both defects. Equation (1) uses the published sixth-power Noether degree and
adds the missing `qL=312` charge. No quartic bound from that packet is used.

## Nonclaims

This note does not prove:

- the worker's quartic `O(r^4)` bound or its general `N^24` estimate;
- a theorem when `d<=t`;
- a multiplicity bound for witnesses sharing one slope;
- a witness-exhaustive atlas or a bound across different received lines,
  active charts, or realized profiles;
- the full all-parameter A6 theorem or the below-Johnson residual compiler;
- hard input 2, the unsafe/lower reserve, a deployed finite-row crossing,
  Grand MCA, Grand List, or either prize question.

The official score remains `0/2`. No stable-paper TeX is changed.
