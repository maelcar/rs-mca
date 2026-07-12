# (ILO-moment) is closed — consumer reconciliation for the fiber-image chain

## Status

CONSUMER / RECONCILIATION note. Every mathematical claim here is either
(i) DannyExperiments' PR #668 theorem, consumed at head
`56128dbadf9c9b731f965cdf4f8a8178bec829df`
(`canonical_transversal_vc_compression.md` — the closer, full credit there),
re-verified independently by the verifier below, or (ii) arithmetic
consequences for our integrated chain #643/#646/#655/#657/#661/#663, each
labeled. No new mathematics beyond the composition.

## 1. What #668 proves (AUDIT, independently re-verified)

For any weights `a_1..a_b` in an abelian group, with `f` the maximum
subset-sum fiber, `L` the image size, and `d` the maximum subset-dissociated
set size:

```text
(668-1)   f <= 2^(b-d)          (fiber injects through the complement of a
                                 maximum dissociated set)
(668-2)   L <= sum_{j<=d} C(b,j) (minimum-binary-cost transversal shatters
                                 only dissociated sets + Sauer-Shelah)
(668-3)   f*L <= 3^b            (combine; tight direction at d/b = 1/3)
```

We re-derived all three steps by hand at gate (the binary cost `2^(i-1)`
makes all subset costs distinct, so the swap argument needs no tie-break;
the swapped set is disjoint from `R_0 minus B` because `R_0` meets the
shattered set in exactly `B`). BLOCK 1 of the verifier re-proves (668-1)-(668-3)
exhaustively on 4,096 exact instances independent of #668's own regression.

## 2. Consequences for the chain (each one line)

- **(ILO-moment) HOLDS** with `omega(eta) = H_2(eta)` (PROVED, = #668 (3)):
  `f >= 2^{(1-eta)b}` forces `d <= eta b` by (668-1), then (668-2) gives
  `L <= 2^{H_2(eta) b}`. This is SHARPER than the `(d+2)eta` form our #657
  conditioned on, and it needs no GAP structure at all.
- **#655's conditional cap is now UNCONDITIONAL** (PROVED): `rho* < log 2`,
  and explicitly `rho* <= log(3/2) = 0.405465` by (668-3), since
  `rho = (log f + log L)/b - log 2 <= log 3 - log 2` on every block.
- **The bracket, both ends unconditional (COMPUTED):**
  `rho* in [0.158411, 0.405465]` — lower end = #655's b=18 champion
  (verifier BLOCK 2 recomputes it from scratch), upper end = #668.
  #655's censused fit (~0.20-0.23) sits inside; the fit stays MEASURED.
- **#657's missing lemma: RESOLVED in image-size form** (AUDIT): the named
  per-instance exponential inverse-LO was only ever needed to bound `L1`;
  #668 bounds `L1` directly. The GAP-containment form of Step B remains a
  genuine open problem of independent interest, but it is no longer
  load-bearing for any consumer in this program. #657's structured-class
  theorems stand (they give rank/GAP structure #668 does not).
- **#661/#663 stand as structural results** (AUDIT, = #668's own framing):
  the Fourier atom bound, quadratic-Bohr trapping, dichotomy, det-G
  refutation, and the three bridge-route impossibilities are statements
  about GAP-structure recovery, untouched by the image-size shortcut.
  In particular #663's "L4 route is structure-blind" and #668's success are
  consistent: #668 is not a moment/energy argument — it is a compression
  argument, exactly the kind of input #663's route-cuts did not exclude.
- **The corridor closes (PROVED, one line):** #655's corridor corollary
  required any `rho -> log 2` family to satisfy
  `log b / b << 1 - phi/log2 << 1`; by #668 no family reaches past
  `log(3/2)`, so the corridor is empty above that rate — the packing
  frontier question is now the exact value of `rho*` inside
  `[0.158411, 0.405465]`.

## 3. Superseding ledger note (paste-ready, for the maintainer)

*The image-face chain #643 -> #646 -> #655 -> #657 -> #661 -> #663 posed
one named hypothesis, (ILO-moment). DannyExperiments #668 proves it
outright (canonical-transversal VC compression, `omega(eta) = H_2(eta)`),
making the packing-rate cap unconditional: `rho* <= log(3/2)`, with the
proved family lower bound `0.158411`. The remaining open content on this
face is the exact value of `rho*` and, separately, the GAP-form of the
inverse question (open, no longer load-bearing). All prior conditional
statements in the chain should be read with the condition discharged.*

## 4. Nonclaims

No improvement of either bracket end is claimed here; the exact `rho*` is
OPEN. The GAP-form Step B is OPEN (and unclaimed by us — #663 maps its
routes). No span-face content. No TeX edit.

## Reproducibility

`python3 experimental/scripts/verify_ilo_moment_closed_consumer.py`
(exits nonzero on any failure; prints a PASS count; runtime ~20s under
`ulimit -v 2097152`).
