Ihave read the active wall, banked lemmas, cuts, the Cycle 2/3/5 audits, and
the source def:residue, thm:normalform, prob:perfiber,conj:B,thm:rigidcyclo,
thm:exactcount.Hereistheresult.

  ---
Final classification:BANKABLE_LEMMA
  Object:

Paired-ReadoutSlopeRigidityLemma(W-F1-AA-RESrigidityhalf):exact
  explanation-gauge kernel E·F_{<k}[X], datum-conjugation bijection z↦z^p, and
  reductionoftheF-valuedslopecounttobase-readoutequidistribution.
  (Restricted regime: quadratic B=F_p, F=F_{p^2}, D⊂B, balanced a=k+t=s_delta,
E∈F[X]\B[X] of degree t=sigma, Bnum≠0. The asymptotic value-countisnot
proved and is left as the residual wall.)

  Short verdict:

TherigidityhalfofW-F1-AA-RESisprovableandsource-valid;thevalue-count
  (asymptotic) half is not, and remains a faithful prob:perfiber/conj:B
  instance.Concretely,fornonzeronumeratorthebadslopeattachedtoan
  a-subset S is exactly the residue [interp_S(w)]_E∈F[X]/(E), and two supports
give the same slope iff their interpolants differ by E·G withdeg G<k—i.e.
by a degree-<k explanation. So the same-slopekernelispreciselythe

def:residuecontainmentgaugeE·F_{<k}[X],theslopeinvariantcarriesno

extensiondatabeyond[interp_S(w)]_E,andtheentireF-valuedcountcollapses

ontotheimageofthebasereadoutrhomoduloEhat=lcm(E,E^τ)∈B[X].

Conjugationτisabijectionofbad-slopewitnessesfromthedatumtoits

conjugatedatum(notaself-symmetry,sinceE∉B[X]),whichfixesthe

q_gen/q_lineledger.Whatstaysopenisthesizeofthatimage,whichisthe

genuinewall.

  Proof / counterpacket / wall:

  Notation. τ = Frobenius of F/B, α a fixed B-basis element with {1,α} a B-basis
  ofF,ᾱ=α^p=τ(α).Anchorw=w0+α·w1,w0,w1:D→B.Datum(E,Bnum,w)per
  def:residue with deg E=t, deg Bnum<t, Bnum≠0, E nonzero on D. Balanced
a=k+t=s_delta (Cycle 4). b:=[Bnum]_E∈F[X]/(E), nonzero sincedeg Bnum<t=deg E
and Bnum≠0.

  Step 0 (slope = interpolant residue on an a-subset). For |S|=a a witness has
  deg Q_z<k+t=aandQ_z=wonS,soQ_zistheuniqueinterpolant:
  Q_z=interp_S(w). The slope equation Q_z≡z·Bnum (mod E) becomes

[interp_S(w)]_E=z·binF[X]/(E).(*)

[interp_S(w)]_E=z·binF[X]/(E).(*)

Sinceb≠0isnotassumedaunitbut[Bnum]_E≠0inthefield-of-fractionssense
  forces uniqueness of the scalar z whenever (*) is solvable (banked caveat 2):
  z=z(S)iswell-defined.Asupportis"onthebadline"exactlywhen
  [interp_S(w)]_E∈F·b.

Sinceb≠0isnotassumedaunitbut[Bnum]_E≠0inthefield-of-fractionssense
fors uniqueess of thescalarz whenever (*)ssolvable (banked caveat 2):
z=z(S)is well-defined. A supportis "on the bad line" exactly when
[interp_S(w)]_E∈F·b.

Step1(exactsame-slopekernel=explanationgauge).LetS,S'bea-subsets,
  both on-line. Then z(S)=z(S') iff, subtracting (*),

interp_S(w)≡interp_{S'}(w)(modE).

interp_S(w)≡interp_{S'}(w)(modE).
Boh interpolants lie in F_{<a}[X], sotheirdifferenceD(X)hasdeg D<aand
E|D.HenceD=E·Gwithdeg G<a-t=k,i.e.

z(S)=z(S')⟺interp_S(w)-interp_{S'}(w)∈E·F_{<k}[X].(Rigidity)

z(S)=z(S')⟺interp_S(w)-interp_{S'}(w)∈E·F_{<k}[X].(Rigidity)

ThekernelE·F_{<k}[X]isexactlythedegree-<kexplanationfreedomof
  def:residue (adding E·G, deg G<k, preserves ≡zB mod E and deg<k+t). This is
  thepreciseanalogueofthm:rigidcyclo's"p_1(A)=0 ⟺ antipodal rearrangement":
  here "equal slope ⟺ difference is a degree-<k multiple of E." Counting
dimensions: F_{<a}[X] has F-dim a; E·F_{<k}[X] has F-dim k;thequotienthas
F-dim t and the reduction map identifiesitwithF[X]/(E)(kernelof

F_{<a}[X]→F[X]/(E)isE·F_{<a-t}[X]=E·F_{<k}[X]).Sothecompleteslope

invariantis[interp_S(w)]_E,withnoresidualextension-onlydatum,

confirmingandsharpeningtheCycle1–2reduction.

ThekernelE·F_{<k}[X]isexactlythedegree-<kexplanationfreedomof
def:residue (adding E·G, deg G<k,prserves ≡zB mod E nd deg<k+t).Thisis
the preciseanalogue of thm:rigidcyclo's "p_1(A)=0 ⟺ antipodal rearrangement":
here "qualslope ⟺ diference is a degree-<k multiple of E." Counting
dimensions:F_{<a}[X] has F-dim a; E·F_{<k}[X] has F-dim k; the quotienthas
F-dim t andthe reductionmap identifies it wit F[X]/(E) (kernel f
_{<a}[X]→F[X]/(E) is E·F_{<a-t}[X]=E·F_{<k}[X]). So the complete slope
invariant is [interp_S(w)]_E, with no residual extension-only datum,
confirming and sharpening the Cycle 1–2 reduction.

Step2(basedescentthroughrho).InterpolationoverthebasesetD⊂Bhas
  base-field Lagrange weights, so interp_S(w)=interp_S(w0)+α·interp_S(w1) with
  interp_S(w_i)∈B[X].BecauseEhat∈B[X]andE|Ehat,[interp_S(w)]_Eisthe
  E-image of the Ehat-class interp_S(w0)+α·interp_S(w1), i.e. it is a fixed
F-affine function of

rho(S)=(interp_S(w0)modEhat,interp_S(w1)modEhat)∈(B[X]/Ehat)^2.

rho(S)=(interp_S(w0)modEhat,interp_S(w1)modEhat)∈(B[X]/Ehat)^2.

CombiningwithStep1:thebad-slopesetistheimageofthebasereadoutrho
  under the fixed map rho ↦ [interp_S(w0)+α interp_S(w1)]_E, intersected with
  thelineF·b.Theslope'stwoB-coordinates(z0,z1),z=z0+αz1,arelinear
  read-offs of rho(S) in the F-structure of F[X]/(E).

CombiningwithStep1:thebad-slopesetistheimageofthebasereadoutrho
under thefxed marho ↦ [interp_S(w0)+α interp_S(w1)]_E, intersecte with
the line F·b. The slope's two B-coordinates (z0,z1), z=z0+αz1, ar linear
read-offs of rho(S) in the F-structure of F[X]/(E).

Step3(datum-conjugationbijection;ledger).Applyτto(*).Since
  τ(interp_S(w))=interp_S(w0)+ᾱ interp_S(w1)=interp_S(w̄) with w̄:=w0+ᾱw1, and
  τ(z·Bnum)=z^p·Bnum^τ,τ(E)=E^τ:

[interp_S(w̄)]_{E^τ}=z^p·[Bnum^τ]_{E^τ}.(**)

[interp_S(w̄)]_{E^τ}=z^p·[Bnum^τ]_{E^τ}.(**)

Thuszbadfor(E,Bnum,w)witnessedbyS⟺z^pbadfortheconjugatedatum
  (E^τ,Bnum^τ,w̄) witnessed by the same S. Because E∈F[X]\B[X], E^τ is not a
  scalarmultipleofE,sothedatumisneverself-conjugate:conjugationisa
  bijection between distinct data, not a symmetry of one datum. Consequence for
the ledger: slopes need not come in {z,z^p} pairs within onedatum,sogenuine
q_line=p^2 behavior is admissible; onlywhentherelevantdenominator

projectionisbase-rational(theexcludedE∈B[X]case)doesthereadout

collapseandforceq_gen=p-controlled,conjugation-closedslopesets.Thisis

thegenerated-fieldcriterion:q_gengovernsthecountexactlywhenthe

E-projectionofthereadoutfactorsthroughB[X]/(Ehat∩B\text{-rational

part});otherwiseq_lineistheceiling.

Thuszbadfor(E,Bnum,w)witnessedbyS⟺z^pbadfortheconjugatedatum
(E^τ,Bnum^τ,w̄)witnessed by h ame S. Because E∈F[X]\B[X], E^τ is not a
scalar multiple of E, sothe datum is nevr self-conjugate: conjugatinisa
bijection between distinct data, not a symmetry of one datum. Consequece for
the ledger: slopes need not comein {z,z^p} pairs within one datum, so gnuine
q_line=p^2 behavior is admissible; only when the relevat dnominator
projectionis base-rational (the excluded E∈B[X]cas) does the readout
collapse and forc q_gen=p-controlled, conjugation-closed lopsts. Thisis
the genrted-field criterion: q_gen governs the count xactly whn the
E-projection o thereadout factors through B[X]/(Ehat∩B\text{-rational
part}); otherwise q_line isthe ceiling.

WhatisNOTproved(theresidualwall).Thesize#{[interp_S(w)]_E∈F·b : S an
  admissible a-subset} is exactly the equidistribution of the base statistic

χ_b(S):=slope-coordinateof[interp_S(w0)+αinterp_S(w1)]_Ealongb,

χ_b(S):=slope-coordinateof[interp_S(w0)+αinterp_S(w1)]_Ealongb,
over a-subets S. Boundingthis image by n^{1+o(1)} above correctedreserve
eta=sigma/nisafaithfulinstanceofprob:perfiber/conj:B(heretheprefix
  map Φ_σ is replaced by the arbitrary-anchor residue read-off, but the
  per-fibercollisioncontentisidentical),andisnotdeliveredhere.The
  sigma=1 fixed-rate counterpacket is sub-reserve (eta=sigma/n→0) and is not
used.

Fieldandstatusaudit:

  - q_gen=p (B=F_p): field of D, of w0,w1, and of rho's components and Ehat.
  GovernsthecountifftheE-projectionisbase-rational(excludeddenominator
  case).

-q_line=p^2(F=F_{p^2}):fieldwhereslopeszandE,Bnumlive;theadmissible
  ceiling for the count since E∉B[X].

-q_chal:untouched.Noprotocolchallenge-fieldsaving,nodivisionofabase
  MCA numerator by |F|, no ass:extension-mca-lift.

-Proved(source-valid,restrictedregimeabove):Step0
  slope=[interp_S(w)]_E; Step 1 exact same-slope kernel E·F_{<k}[X] =
  def:residueexplanationgauge;Step2basedescentofthefullcountthrough
  rho mod Ehat; Step 3 datum-conjugation bijection and the q_gen/q_line
dichotomy. Uses only interpolation, degree counting, and B-linearityoverthe
banked reduction; no coprimality of E,E^τisneededforSteps0–1.

-Notproved:theasymptoticvalue-count(n^{1+o(1)}abovereserve),conj:B,
  prob:perfiber, list/line decoding. These remain the wall.

-q_gen=p(B=F_p):fieldofD,ofw0,w1,andofrho'scomponentsandEhat.
Governs the count if the E-projection is base-rational (excluded denominator
cas).
- q_line=p^2(F=F_{p^2}):fieldwhereslopeszandE,Bnumlive;theadmissible
ceiling for the count since E∉B[X].
- q_chal: unouched. No protocol challenge-fieldsaving,nodivisionofabase
MCA numerator by |F|, no ass:extension-mca-lift.
- Proved (surce-valid, restricted regime above):Step0
slope=[interp_S(w)]_E; Stp 1 exact same-slope kernel E·F_{<k}[X]=
def:resdu explanation gauge; Step2 base descent ofthe full countthrough
rho mod Ehat; Step 3 datum-conjugation bijection and the q_gen/q_line
dichotomy. Uses onlyinerpolation, degree ounting,andB-linearity overthe
banked reduction; nocoprimaiy ofE,E^τ is needed for Steps 0–1.
- Not poved: theasymptotic value-count (n^{1+o(1)} above reserve),conj:B,
prob:perfiber, list/line deoding. Theseremain the wll.

Whattobank:

BanktherigidityhalfofW-F1-AA-RESasaBANKABLE_LEMMA:onbalanceda=k+t
  subsets with nonzero numerator, the bad slope equals the interpolant residue
  [interp_S(w)]_E,thesame-slopeequivalenceistranslationbytheexplanation
  gauge E·F_{<k}[X], so the complete slope invariant carries no extension-only
data and the F-valued count descends to the image of the basereadoutrho mod
Ehat; conjugation τ is a bijection totheconjugatedatum(nota

self-symmetry,sinceE∉B[X]),pinningtheq_gen-vs-q_lineledger.Thestrictly

residual,still-openinvariantissharpenedfrom"arigidity/value-countlaw

forrho"tothesinglebase-fieldstatistic:equidistributionof

χ_b(S)=[interp_S(w)]_EalongthelineF·bovera-subsets,abovecorrected

reserveeta=sigma/n—afaithfulprob:perfiber/conj:Binstance,notclosable

here.
