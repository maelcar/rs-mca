I have the source structure I need: def:residue/thm:normalform (lines
1189–1207), prob:perfiber/conj:B/rem:aper (1227–1257),
thm:rigidcyclo/thm:exactcount (737, 1148), the aperiodic antipodal-rigidity
machinery, and the banked Cycle 1–6B reductions. Here is the attack.

---
Final classification: BANKABLE_LEMMA

Statement

  Setting (hypotheses, all source-grounded). B=\F_p, F=\F_{p^2}, \tau the
  nontrivialelementof\mathrm{Gal}(F/B),\alpha\in F\setminus Bwith
  \{1,\alpha\} a B-basis. D\subset B, |D|=n. Degree-t residue-line datum
(E,Bnum,w) of def:residue: E\in F[X]\setminus B[X],\deg E=t=\sigma,Enonzero
on D; \deg Bnum<t; w:D\to F. Balancedledger(Cycle4):

a=k+t=s_\delta=\lceil(1-\delta)n\rceil.Writew=w_0+\alphaw_1,w_i:D\toB;

forana-subsetSsetP_i^S=\mathrm{interp}_S(w_i)\inB_{<a}[X](baseLagrange

coefficients,bankedCycle1).\widehatE=\mathrm{lcm}(E,E^\tau)\inB[X].

Separationhypothesis(tangent+quotient-periodic,perrem:aperandCycle-2

caveat2):[Bnum]_E\neq0and\gcd(E,E^\tau)=1,so\deg\widehatE=2tandCRT

givesF[X]/\widehatE\congF[X]/E\timesF[X]/E^\tau.

  The slope of S (when defined) is the unique z\in F with
  [P_0^S]_E+\alpha[P_1^S]_E=z\,[Bnum]_EinF[X]/E.

  Part A — Slope is a base-linear-fractional functional of the readout;
  conjugateisco-determined.

TheslopemapfactorsasafixedB-linear-fractionalmapofthebasereadout
  \rho(S)=([P_0^S]_{\widehat E},[P_1^S]_{\widehat E})\in(B[X]/\widehat E)^2.
  Explicitly,withtheB-linear\varphi(\bar P_0,\bar P_1)=[\bar
  P_0]_E+\alpha[\bar P_1]_E\in F[X]/E, a support is on the bad line iff
\varphi(\rho(S))\in F\cdot[Bnum]_E, and thenz=\varphi(\rho(S))/[Bnum]_E.
Applying \tau to the slope equation yields,intheconjugatefactor

F[X]/E^\tau,

[P0^S]_{E^τ}+α^τ[P1^S]_{E^τ}=z^τ[Bnum^τ]_{E^τ},

[P0^S]_{E^τ}+α^τ[P1^S]_{E^τ}=z^τ[Bnum^τ]_{E^τ},
so the same base readout \rho(S) alsodetermines z^\tau.Consequentlythe
slopesetis\tau-stableand

#{distinctslopesz(S):Snoncontaineda-subsetonthebadline}

≤#{ρ(S):Snoncontaineda-subsetonthebadline}⊆B[X]/Ehat,

#{distinctslopesz(S):Snoncontaineda-subsetonthebadline}
       ≤  #{ ρ(S):  noncotained a-subset on he bad line}  ⊆B[X]/Ehat,

i.e.theF-valuedvalue-countisdominatedbythecardinalityofthebase
  readout image (a q_gen-coordinate object of B-dimension \le 2\deg\widehat E\le
  4t).

i.e.theF-valuedvalue-countisdominatedbythecardinalityofthebase
readout image (a q_gen-cordinate bjec of B-dimension \le 2\deg\widehat E\le
4t).

PartB—Exacttransferforbaseslopes(z\in B).Let\theta\in B[X]/\widehat
  E be the (\tau-fixed) CRT element with \theta\equiv\alpha\ (E),
  \theta\equiv\alpha^\tau\ (E^\tau),and\widehat b\in B[X]/\widehat Ethe
  \tau-fixed element with \widehat b\equiv[Bnum]_E\ (E), \widehat
b\equiv[Bnum^\tau]_{E^\tau}\ (E^\tau) (bothexistandarebaseby
\tau-invariance; if Bnum\in B[X] then\widehat b=[Bnum]_{\widehat E}).For

z\inB(z^\tau=z),thetwoCRTfactorscombineintoasinglebase-field

equation

[P0^S]_Ehat+θ·[P1^S]_Ehat=z·b̂inB[X]/Ehat,z∈B.(★)

[P0^S]_Ehat+θ·[P1^S]_Ehat=z·b̂inB[X]/Ehat,z∈B.(★)

Equation(★)isexactlyabase-fieldresidue-linereadoutforthebasedatum
  (\widehat E,\widehat b,\;w_0+\theta w_1) over (B,D,k) at prefix
  \le\deg\widehat E\le 2t.Hencethebase-slopesub-countisboundedbythebase
  packing number \Lambda^{\mathrm{NC}} of that datum
(def:residue/thm:normalform over B), and onsubgroup/monomialstratainthe
stable range it is governed exactly bythm:exactcount/thm:rigidcyclo:

base-slopecount=\Acl(N',\ell')=n^{\beta(\rho)/\ceff+o(1)}.

Equation(★)isexactlyabase-fieldresidue-linereadoutforthebasedatum
(\widehat E,\widehat b,\;w_0+\theta w_1) ovr (B,D,k) at prefix
\le\g\widehat E\le2t. Hence the base-slopesub-count is boundedbythebase
packing number \Lambda^{\mathrm{NC}} of that datum
(def:residue/thm:normlform over B),and on subgroup/monomialstratainthe
stable range it is governedexactly by thm:exactcount/thm:rigidcyclo:
base-slope count =\Acl(N',\ell')=n^{\bea(\rho)/\ceff+o(1)}.

Transferboundary(theanswerto"wheredoesthecyclotomiccounttransfer").
  The base-field count of thm:exactcount transfers to the z\in B slopes exactly
  (via(★))anddoesnottransfertoz\in F\setminus B:off-baseslopesarenot
  \tau-fixed, so they are not equivalent to any single base equation in
B[X]/\widehat E and instead require controllingthefullbase-readoutimageof
Part A. This is the precise residualcore(see"remainingwall").

  Why this is not the forbidden same-slope kernel

  The kernel statement \mathrm{interp}_S(w)-\mathrm{interp}_{S'}(w)\in E\cdot
  F_{<k}[X](Cycle6B)answers"whenisz(S)=z(S')."PartsAandBinstead
  answer "what controls \#\{z(S)\}": A exhibits the slope as a fixed
base-linear-fractional image of \rho(S) andboundsthecountbythe
base-readout image; B reduces the entirez\in Bstratumtoabase

\Lambda^{\mathrm{NC}}instanceandimportsthm:exactcountverbatim.Neitheris

akernel/descentrestatement.

Sourcedependencies

  def:residue (slackMCA_v3.tex:1189), thm:normalform (:1197), prob:perfiber
  (:1227),conj:B(:1231),rem:aper(:1255),thm:rigidcyclo(:737),
  thm:exactcount (:1148), prop:qfloor (:1273) for the \Acl form; banked Cycle 1
paired readout, Cycle 2 caveats (Ehat / unique-slope/a-subsetnoncontainment
loss), Cycle 3 noncontainment subsetlemma,Cycle4a=s_\delta.Galois

descent+CRTarestandard.Nouseofass:extension-mca-lift

(snarks_v4.tex:242),noq_chal,noline/list-decoding.

  Field ledger

  q_gen=p (B=\F_p: D, w_0,w_1, readouts \rho(S), \theta, \widehat b, \widehat E,
  andtheentirez\in Bstratum(★)livehere).q_line=p^2(F=\F_{p^2}:
  E,Bnum,\alpha,z and the off-base slopes). q_chal: unused. The lemma's content
is that the value-count is structurally a q_genobject(basereadoutimage),
with q_line re-entering only throughoff-baseslopes.

Parameterledger

  n=|D|; k=\rho n; t=\sigma=a-k; a=k+t=s_\delta=\lceil(1-\delta)n\rceil; reserve
  \eta=\sigma/n;radius\delta;extensiondegreee=2;\deg\widehat E=2t
  (quotient/lcm order), readout B-dimension 2\deg\widehat E\le 4t; first finite
test t=\sigma=2 (\deg\widehat E=4, readout dim\le 8).Nolistarityinvoked.

  Proof / audit notes

  A: E\mid\widehat E always, so \rho(S) determines [P_i^S]_E; \tau is a ring iso
  F[X]/E\to F[X]/E^\taufixingB[X],givingtheconjugateequation;B-linearity
  of \varphi and |\rho(S)\text{-image}| bounding \#\{z\} is immediate since
z=\varphi(\rho(S))/[Bnum]_E is a fixed functionof\rho(S).B:
(\alpha,\alpha^\tau) and ([Bnum]_E,[Bnum^\tau]_{E^\tau})are\tau-fixedunder

theCRTaction(u,v)\mapsto(v^\tau,u^\tau),hencebase;z=z^\taucollapses

(*)+(**)ontothefixedsubringB[X]/\widehatE,whichispreciselythebase

residue-lineformofdef:residue/thm:normalform.The\gcd(E,E^\tau)=1and

[Bnum]_E\neq0hypothesesareexactlythetangent/quotient-periodicseparations

thewallrequires;withoutthemCRTandunique-zfail(correctlyexcluded).

Consistencywiththe\sigma=1counterpacket:att=1,\deg\widehatE=2,readout

\le\F_p^4;thebound\#\{z\}\le\#\rho(S)permits\Theta(p^2)becausethe

base-readoutimageislargeatsub-reserve\eta\to0—Arelocates,anddoes

notclose,thatregime,asrequired.

  Remaining wall (not claimed proved)

  The off-base count \#\{z\in F\setminus B\} equals the number of distinct base
  readoutswhose\varphi-imagemeetsF\cdot[Bnum]_Eoffthebasesub-line
  B\cdot[Bnum]_E. Bounding this by n^{1+o(1)} above corrected reserve
\eta\ge(1+\epsilon)\taustar(\rho,q_{gen}) isexactlyabase-fieldinstanceof
prob:perfiber/conj:B for the fixed-anchorvarying-supportlocus—nowhonestly

inq_gencoordinates.Thisisthegenuinelyopencore;A+Breduceitfroman

F-counttothisbase-readout-imageincidencecountanddispatchthez\inB

stratumexactly.

  What Codex should bank / test next

  Bank: (A) the base-linear-fractional slope functional + #slopes ≤
  #base-readouts+conjugateco-determination;(B)theexactbase-slope
  reduction (★) to the base datum (\widehat E,\widehat b,w_0+\theta w_1) and the
thm:exactcount transfer for z\in B; and thetransferboundary(baseslopes
transfer, off-base do not).

  Test (t=\sigma=2 finite certificate, per P2): pick smallest p\equiv1\bmod n
  withD\le\F_p^\timesasubgroup,k=\rho n,a=k+2;pickE\in\F_{p^2}[X]degree
  2 with \gcd(E,E^\tau)=1 and E nonzero on D, Bnum\neq0 with [Bnum]_E\neq0; pick
base words w_0,w_1:D\to\F_p. Enumerate a-subsetsS,compute
\rho(S)\in(\F_p[X]/\widehat E)^2, theslopez(S)\in\F_{p^2}onthebadline,

andthenoncontainmentflag(Cycle3).Certifythreestatistics:(i)

\#\{z(S)\}\le\#\{\rho(S)\}(PartA);(ii)thez\in\F_psub-countequalsthe

base\Lambda^{\mathrm{NC}}of(\widehatE,\widehatb,w_0+\thetaw_1)computed

independentlyvia(★)(PartB);(iii)\{z(S)\}is\tau-stable.Adiscrepancy

in(i)–(iii)falsifiesthelemma;agreementplusanoff-baseexcess

\#\{z\in\F_{p^2}\setminus\F_p\}\ggn^{1+o(1)}atcorrectedreservewouldbe

thefirstabove-reservecounterpacketandshouldbepromotedtoa

COUNTERPACKETrun.Reusef1_extension_slope_sweep.py/mca_slope_scan.py

harnesseswiththereadouttakenover\widehatEratherthanE.
