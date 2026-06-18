# Cycle 16 Audit: Rank/Determinant Resonance Split Wall

Status: BANKABLE_LEMMA / EXACT_NEW_WALL / AUDIT.

Run:

- Run id: `2026-06-18T06-33-36-013Z-cycle16-rank-determinant-resonance-313a123d`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-18T06-33-36-013Z-cycle16-rank-determinant-resonance-313a123d`
- Lane: isolated RS-MCA VS Code credited terminal ads lane.
- Launcher: `/Users/danielcabezas/packy-fable-ui/.codex-vscode-launchers/rs-mca-current`
- App workaround: private no-xattr VS Code copy at
  `/Users/danielcabezas/packy-fable-ui/.vscode-app-sandbox/Visual Studio Code.app`.
- Harness result: `ok=false`, `classification=HARNESS_MALFORMED_VISIBLE_TERMINAL`,
  `answerSource=terminal_tui`, `terminalMalformedVisible=true`.
- Audited math artifact: clean recovered structured Claude JSONL copied to
  `../raw/20260618_CYCLE16_RANK_DETERMINANT_RESONANCE_RECOVERED_CLAUDE_JSONL.md`.
- Malformed visible-terminal text is preserved separately and is not banked as
  mathematics.

## Verdict

Cycle 16 gives one bankable safe-side lemma and one sharper exact wall.

Bank:

- Off `R0`, if the Cycle 15 determinant consistency polynomial
  `Q(z_0,z_1)` is not identically zero, then the slope set is contained in a
  nonzero degree-`<=4` plane curve over `B=F_p`; hence `C2<=4p=O(p)=O(n)`.
- The residual large-slope regime is no longer just "rank/determinant"; it is
  the split-distinct realisation inside `Q==0`.

Do not bank:

- a proof of slope collapse on `Ra/Rb`;
- a `Theta(q_line)` counterpacket;
- the raw claim that `Q==0` alone is a counterpacket;
- any result above corrected reserve;
- any `q_gen` collapse;
- any protocol, MCA, CA, list-decoding, line-decoding, or SNARK consequence.

## Field And Parameter Ledger

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `q_chal` unused.
- `D=F_p`, so `n=p`.
- `t=sigma=2`.
- `j=n-a=r-t=3`; hence `a=n-3`, `k=n-5`.
- `eta=sigma/n=2/n`, sub-reserve.
- Work is off `R0={ wedge([W]_E,[Bnum]_E)=0 }` unless explicitly stated.

## Harness And Source-Mount Audit

Cycle 16 exposed an operational bug: the mounted Packy source snapshot did not
include the Cycle 15 audit or certificate files. The worker reported that

```text
current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE15_SURFACE_SLOPE_FIBER_AUDIT.md
current_loop_20260618/2026-06-18-fable-loop/local_checks/20260618_cycle15_forced_ra_slope_scan_certificate.md
```

were absent from `FILE_INDEX_FOR_MODEL.md`. Local inspection confirmed that
Packy's `source_files/current_loop_20260618/2026-06-18-fable-loop` was stale
and stopped around Cycle 9. The worker reconstructed Cycle 15 from the route
ledgers, but the source mirror must be refreshed before Cycle 17.

This is an AUDIT issue, not a mathematical result.

## Banked Safe-Side Lemma

Off `R0`, `{[W]_E,b}` is an `F`-basis of `A=F[X]/E`, with `b=[Bnum]_E`.
Cycle 15 wrote

```text
L_z(tau)=iota(tau)-z mu(tau)=0 in A
```

as an affine `B`-linear system in `(tau_1,tau_2,tau_3)`.

With

```text
A0=p1[W]_E+p2 b,
B0=q1[W]_E+q2 b,
p_i=p_i^0+p_i^1 tau_1+p_i^2 tau_2,
q_i=q_i^0+q_i^1 tau_1+q_i^2 tau_2,
```

the columns are

```text
c1(z) = (p1^1 - z q1^1)[W]_E + (p2^1 - z q2^1)b,
c2(z) = (p1^2 - z q1^2)[W]_E + (p2^2 - z q2^2)b,
c3(z) = -[W]_E + z b,
c0(z) = (p1^0 - z q1^0)[W]_E + (p2^0 - z q2^0)b.
```

The consistency determinant is

```text
Q(z_0,z_1)=det_{4x4}[c1(z) | c2(z) | c3(z) | c0(z)],
z=z_0+alpha z_1.
```

Each column is `B`-linear in `(z_0,z_1)`, so `deg Q<=4`. Any landing slope
must satisfy `Q(z_0,z_1)=0`. Therefore, if `Q` is not identically zero,
Schwartz-Zippel gives

```text
C2 <= #{z in F : Q(z_0,z_1)=0} <= 4p = O(p)=O(n).
```

This is bankable in the restricted `D=F_p`, `t=sigma=2`, `j=3`, off-`R0`
regime.

## Audit-Only Algebra From The Answer

The recovered answer proposes a determinant-trace / Plucker identity and a
conjugate-skew Gram criterion for `Q==0`:

```text
delta^2 Q =
  Tr(m_12 Phi_0^tau)
  + Tr(Phi_1 m_24^tau)
  - Tr(m_14 Phi_2^tau),

Q==0 iff H_kl + H_lk^tau = 0 for all k,l in {0,1,2}.
```

This is plausible and useful as a scanner/proof target, but it should remain
AUDIT until checked against the actual coefficient formulas in a local
symbolic or finite verifier. Do not cite the trace/Gram criterion as proved
yet.

## Exact New Wall

The live wall is sharpened to:

```text
W-F1-AA-RES-T2J3-RANK-DET-SPLIT.
```

Question:

```text
When Q==0 identically on a source-valid Ra/Rb resonance surface, does the
slope map restricted to distinct D-split cubics T subset F_p realise
Theta(p^2)=Theta(q_line) distinct slopes, or does the split-distinct locus
collapse the image to O(p)?
```

This is still sub-reserve (`eta=2/n`) and cannot be used as a corrected-reserve
counterpacket without a separate reserve theorem or family.

## Next Checker Target

Implement a scanner/certificate for the `Q==0` branch:

- Input: `p`, separated `E`, `Bnum`, base anchors `w0,w1`, with
  `D=F_p`, `t=sigma=2`, `j=3`.
- Derive the Cycle 14 forms `A0,B0`, columns `c1,c2,c3,c0`, and `Q`.
- Filter to source-valid `Ra/Rb` resonance data.
- Record whether `Q` is identically zero.
- On the `Q==0` branch, enumerate distinct split co-supports
  `T subset F_p`, `|T|=3`, and count distinct slopes `C2`.
- Certificate fields:

```text
{
  p, q_gen, q_line, E, Bnum, seed,
  stratum,
  off_R0,
  Q_identically_zero,
  degQ,
  C2,
  split_triples_examined,
  fiber_sizes,
  status
}
```

Counterpacket trigger:

```text
Q==0 and C2/p^2 bounded below across a growing-p family.
```

Single-prime examples are EXPERIMENTAL only.
