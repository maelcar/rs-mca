# CAP25 Version 13.2 — revision notes

**Date:** July 19, 2026
**Base:** CAP25 v13.1, second-audit corrections integrated
**Release status:** candidate successor to v12; unsafe frontier results are presented as unconditional, while the four adjacent safe rows remain conditional on a fully instantiated certificate.

## 1. Executive status

Version 13.2 is a corrective integration release. It keeps the theorem-level advances introduced in v13/v13.1, repairs the discrete subfield-census normalization, synchronizes every headline table with the strongest exact unsafe endpoints, and removes claims that the present safe-side reductions already constitute a complete proof.

The active safe-side statement is now a **conditional certificate template**. It requires a proved exhaustive bucket compiler, explicit support-to-parameter coalescing, and one summed finite budget. No adjacent safe row is advertised as unconditional.

## 2. Active exact unsafe endpoints

All headline theorems, scanner tables, certificate tables, and introductory summaries now use the same four active endpoints:

| Row | Unsafe agreement parameter `m` | Exact unsafe proximity edge `δ=1-m/n` | Challenge target |
|---|---:|---:|---:|
| KoalaBear MCA | 1,116,047 | 981,105 / 2,097,152 | 2^-128 |
| KoalaBear list | 1,116,046 | 490,553 / 1,048,576 | 2^-128 |
| Mersenne-31 MCA | 1,116,023 | 981,129 / 2,097,152 | 2^-100 |
| Mersenne-31 list | 1,116,022 | 490,565 / 1,048,576 | 2^-100 |

The older scale-16/32 endpoints are retained only where they are explicitly labeled intermediate or superseded.

## 3. Mathematical corrections

### 3.1 Discrete subfield census

The central v13.1 error has been repaired. For

\[
A_{\mathbb B}(d_1)=\binom n{m'}|\mathbb B|^{-(d_1-1)},
\qquad m'=K-1+d_1,
\]

the manuscript now distinguishes the exact pigeonhole floor

\[
M_{\mathbb B}^{\rm disc}(d_1)
 =\binom{m'}m\left\lceil A_{\mathbb B}(d_1)\right\rceil
\]

from the soft mean-plus-one model

\[
M_{\mathbb B}^{\rm soft}(d_1)
 =\binom{m'}m\left(1+A_{\mathbb B}(d_1)\right).
\]

The ceiling is applied before multiplication by the support count. The active balanced-core input uses the soft upper model, while the exact census proposition records the discrete lower floor.

Corrected finite floor values, in bits, are:

| Offset | KoalaBear | Mersenne-31 |
|---:|---:|---:|
| d1 = w' + 1 | 67.0958 | 52.1129 |
| d1 = w' + 2 | 56.0111 | 41.0169 |
| d1 = w' + 3 | 43.9348 | 39.1799 |
| d1 = w' + 4 | 57.6849 | 57.6848 |

The boundary and interior maximal shifted-degree claims now include their missing degree contradiction instead of relying on an insufficient citation.

### 3.2 Safe-side logical status

The former closure proposition is recast as a conditional template. A valid finite certificate must prove:

- exhaustive assignment of every unpaid bad cell to a declared bucket under a fixed priority rule;
- a precise quotient/prefix bound with the necessary mean-plus-one floor;
- the corrected base-field-normalized balanced-core bound;
- the primitive local shift-pair bound;
- support-to-parameter coalescing for each bucket; and
- the single summed inequality

\[
U_{\rm paid}(a_0+1)+U_Q(a_0+1)+U_{\rm BC}(a_0+1)+U_{\rm sp}(a_0+1)
 \le B_*<L(a_0).
\]

The older `Q+A`, `Q+R1`, and split-pencil packages are now described only as intermediate proof reductions. They are not presented as independent closure theorems.

### 3.3 Loss and reserve condition

The manuscript no longer claims that every `e^{o(n)}` loss is absorbed by every reserve `R >> log n`. The active asymptotic regime requires

\[
R\to\infty,\qquad R=o(n),\qquad
\log L(n)=o\!\left(R(n)\log|\mathbb B|\right).
\]

### 3.4 Other proof and statement repairs

Version 13.2 also:

- adds the necessary `n-3w >= m` hypothesis to the near-rational reduction;
- states the moment inequality for finite `r` and gives the `r=∞` max-fiber endpoint separately;
- defines every multiplicative character at zero and makes the split-divisor indicator piecewise well-defined for nonsplit polynomials;
- repairs the moment-kernel injection by anchoring one member of a heavy fiber;
- qualifies the polynomial-degree heuristic by imposing coefficient normalization;
- gives every deployed row its correct challenge target;
- adds the `q < 2^256` envelope to the all-field circle corollary;
- keeps the original unnormalized band conjecture only as a historical, explicitly refuted proposal; and
- corrects the bibliography title of ePrint 2026/680.

## 4. Independent arithmetic verification

The bundled verifier uses exact integer arithmetic for the four deployed unsafe comparisons, their next-row failures, MCA admissibility, and the corrected discrete census. High-precision log-gamma evaluation is used only to cross-check the large bounded-prefix margins.

Verified frontier margins, in bits:

| Row | Active row | Next row |
|---|---:|---:|
| KoalaBear list | +9.163659 | -22.010942 |
| Mersenne-31 list | +28.112851 | -3.073000 |
| KoalaBear MCA | +8.977743 | -22.196862 |
| Mersenne-31 MCA | +27.927000 | -3.258853 |

Selected bounded-prefix checks:

- KoalaBear, `w=21`: +11,951.205743 bits;
- KoalaBear, `w=22`: -38,283.105400 bits;
- circle row, `w=10`: +60,240.540720 bits;
- circle row, `w=11`: -41,998.692549 bits.

## 5. Build and PDF audit

The release contains 10,276 TeX source lines and compiles to a 199-page PDF.

- 459 labels, all unique;
- 1,340 cross-reference keys, none missing;
- 80 citation keys used, none unresolved;
- no LaTeX errors, package warnings, undefined references, or overfull boxes;
- 31 cosmetic underfull-box notices;
- all fonts embedded;
- PDF preflight and Ghostscript parsing passed;
- all 199 pages rendered with `pdftoppm` and inspected in contact sheets;
- the principal corrected pages were additionally rendered at higher resolution and inspected.

The PDF metadata now includes title, author, subject, and keywords. The PDF remains untagged; that is an accessibility improvement left for a later publication-format pass, not a mathematical blocker.

## 6. Scope and remaining gap

This release does not claim a formal verification of every proof in the 199-page manuscript. The unconditional unsafe frontier survived the targeted second audit and independent arithmetic checks. The proposed adjacent safe rows remain open inside this manuscript until the conditional certificate template is instantiated with exact constants, proved coverage, and coalescing.

Relative to v13.1, the source changes comprise 299 insertions and 260 deletions. A unified patch is included in the release package.
