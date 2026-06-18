I've now read the wall history, the Cycle 6B/7/8 audits, the Cycle 8 checker,
and the governingsourcestatements(def:residue,thm:normalform,
prob:perfiber,conj:B,rem:aper,thm:rigidcyclo,thm:exactcount).Hereismy
 attack.

---
Finalclassification:EXACT_NEW_WALL

  Summary of the attack

Cycle 8 reduced the live object to the raw extensionresidue

R_E(S) = [interp_S(w0)+alpha interp_S(w1)]_E in F[X]/Eonbalanceda=k+t
  supports. The wall as currently written (ACTIVE_WALLS, Cycle 8 audit) asks to
  boundtheraw residue value count#{R_E(S)}byn^{1+o(1)}.Iclaimthattarget
  is the wrong invariant, and I can prove why with an exact structural
decomposition. The genuinely sharper missing invariant is a bad-line incidence
(landing) count, and the reserve eta=sigma/nentersexactlyasthe

codimensiont-1ofthatline.

  1. Bankable structural sub-result: locator–quotient decomposition

  Let W = interp_D(w) in F[X], deg W <= n-1, be the global interpolant of the
  arbitrarywordw=w0+alpha w1onallofD(itexistsbecauseD subset Bgives
  base-field Lagrange coefficients, so W = W0 + alpha W1 with Wi = interp_D(wi)
in B[X]). For an a-subset S, let L_S = prod_{d in S}(X-d), deg L_S = a,and
Q_S = floor(W / L_S). Then:

W=L_SQ_S+interp_S(w),deginterp_S(w)<a,degQ_S<=n-1-a=j-1,

  where j := n - a = r - t is the co-support size (r=n-k). Reducing mod E:

R_E(S)=[W]_E-[L_S]_E[Q_S]_EinF[X]/E.

  Twoconsequencesthatarebankablenow:

  - [W]_E is constant in S, so #{R_E(S)} = #{[L_S Q_S]_E}. This is the
  structuraldecompositionintermsofL_Sandthelow-degreequotientQ_S
  requested as Angle 1, with the degree of Q_S pinned to the co-support size
j-1, not to t.

-ParametrizingbytheomittedsetT=D\S(|T|=j,L_S = L_D L_T^{-1}in
  (F[X]/E)^*, all factors invertible since E(d)!=0), one gets the clean true
  upper bound

#{R_E(S)}<=C(n,n-a)=C(n,r-t).

  For fixed j=r-t this is <= n^{j}, i.e. polynomial but with exponent j. It
  equalsn^{1+o(1)}onlywhenj<=1(t>=r-1,thetrivialtopofreserve).Sothe
  raw-count bound n^{1+o(1)} is not delivered by this decomposition for any
j>=2.

2.Whytheraw-countreadingofthewallisthewrongobject(partial

route-cut)

  The MCA-relevant quantity in def:residue/thm:normalform/Lambda^{NC} is not
  #{R_E(S)}.Itisthenumberofdistinctslopesz in F,whereSis
  bad-with-slope-z iff

R_E(S)=z[Bnum]_E,zinF(ascalar).

  So a support contributes a slope only when its residue lands on the
  one-dimensional F-subspaceF[Bnum]_E subset F[X]/E.Thissubspacehas
  codimension t-1 over F (F[X]/E is t-dimensional over F; the bad line is
1-dimensional).

  This immediately separates two counts that the current wall conflates:

  - C1 (raw): #{R_E(S)} — generically Theta(C(n,j)) above reserve for arbitrary
  anchors(differentco-supportsgivedifferentresidues;thereisp^{2t} >>
  C(n,j) room when t is large). So C1 already exceeds n^{1+o(1)} once j>=2. A
raw counterpacket is therefore trivial and not MCA-meaningful — itrefutes
only the literal raw-count phrasing,nottheslopecount.

-C2(slope/MCA):#{ z in F : exists S, R_E(S) = z[Bnum]_E }—thebad-line
  landing count. This is Lambda^{NC}-relevant and is the real target.

  This is exactly why the banked sigma=1 packet is sub-reserve in a way I can
  nowmakeprecise:att=1,F[X]/E ~= Fisone-dimensional,thebadlineis
  codimension 0 (the whole space), so C1 = C2 and both reach Theta(q_line). For
t>=2 the bad line is a proper codim-(t-1) subspace and C2 << C1.Thereserve
mechanism is literally "raise t to thinthebadline."

  3. The EXACT_NEW_WALL (strictly sharper invariant)

W-F1-AA-RES-LINE-INCIDENCE:

ForB=F_p,F=F_{p^2},DsubsetB,separatedaperiodicE(degE=t=sigma,

gcd(E,E^tau)=1,EnonzeroonD),nonzeronumeratorBnum(deg<t),arbitrary
  base anchors w0,w1, and balanced a=k+t=s_delta, bound the bad-line incidence

count

N_line=#{zinF:existsa-subsetSwith[W]_E-[L_S]_E[Q_S]_E=
  z[Bnum]_E }

=#distinctslopes,

whereQ_S=floor(W/L_S),degQ_S<=j-1,j=n-a=r-t.

Equivalently:boundthenumberofco-supportsT(|T|=j)whoselocator-quotient

residue[L_SQ_S]_Elandsinthecodimension-(t-1)line[W]_E-F[Bnum]_E.

Thereserveeta=sigma/n=t/ncontrolsthecodimensiont-1ofthetargetline;

theconjecturaln^{1+o(1)}isanincidencebound,notacardinalitybound.

  ThisisstrictlysharperthanW-F1-AA-RES-RESIDUE-COUNTbecause:

  - it replaces a set-cardinality (#{R_E(S)}) with an incidence count between
  thelocator-quotientimageandafixedcodim-(t-1)line;

-itistheactualLambda^{NC}slopecount(thm:normalform),soaboundhere
  feeds MCA, whereas a raw-count bound does not;

-itisolatesthereserveasthecodimensionoftheline,explainingthet=1
  sub-reserve degeneration exactly and removing the temptation to refute via raw
  counts.

  It is theorem-sized and actionable: it is an incidence problem between a
  structuredcombinatorialfamily{(L_S, Q_S)}andalinearsubspace,withthe
  degree-(j-1) quotient as the only genuinely free low-degree datum.

Source dependencies

  - slackMCA_v3.tex:def:residue, thm:normalform — the MCA object is the
  noncontainedslopecountLambda^{NC},i.e.residuesonthebadline,notraw
  residues. This is what licenses the C1/C2 split.

-slackMCA_v3.tex:prob:perfiber,conj:B,rem:aper—then^{1+o(1)}targetand
  reserve/aperiodic framing; conj:B's q_{D,n} generated-field correction is
  consistentwiththecountstayingq_line-indexedofftheline.

-thm:rigidcyclo/thm:exactcount—usedonlytonotetheirrigidityisthe
  monomial/cyclotomic antipodal-pair structure (mu_N subgroup); arbitrary
  anchorshavenosuchsymmetry,sonoq_genrigiditytransfers(answeringthe
  prompt's Angle 3: no q_gen rigidity remains; honest counting is a q_line
per-fiber incidence problem). Not imported beyond their proved strata.

-Cycle6Bkernelinterp_S(w)-interp_S'(w) in E*F_{<k}[X]—recoveredasthe
  fiber of the incidence map, not reopened as the wall.

-Cycle8isomorphism—usedasthebridge;twistnotreopened.

-Cycle3nonzero-numeratornoncontainment—guaranteesevery|S|=asupportis
  noncontained, so landings are genuine slopes.

  Field ledger

  - q_gen = p, B = F_p: domain D, anchors w0,w1, components W0,W1, locators
  L_S,L_T(base-field,sinceD subset B).

-q_line = p^2,F = F_{p^2}:E,Bnum,residuesR_E(S),thebadlineF[Bnum]_E,
  slopes z. Residue space F[X]/E has p^{2t} elements; bad line has <= p^2. The
  countstaysq_line-governed;noautomaticcollapsetoq_gen(consistentwith
  Cycle 8).

-q_chal:unused.Noprotocol/denominator/list/line-decodingclaim.

  Parameter ledger

  - n=|D|, k=rho n, a=ceil((1-delta)n)=s_delta, sigma=a-k, balanced t=sigma,
  a=k+t.
  - r=n-k; co-support j=n-a=r-t; reserve eta=sigma/n=t/n.

-deg E=t,deg Bnum<t,deg Q_S<=j-1,deg(L_S Q_S)<=a+j-1=n-1.

-Badline:1-dimoverF;codimensiont-1inF[X]/E.

-Noquotientorder,interleaving,orlistarityused(separated/aperiodicE,
  rem:aper).

  Proof / audit notes

  - Decomposition (§1) is elementary Euclidean division plus mod-E reduction;
  fullyrigorous.Thedegreebounddeg Q_S<=j-1istheonlyquantitativeinput
  and is tight.

-#{R_E(S)} <= C(n,j)isrigorous(themapfactorsthroughthechoiceofT).

-TheC1/C2splitisdefinitionalfromdef:residue(slopezisascalar;
  badness needs R_E(S) in F[Bnum]_E). The claim "C1 generically Theta(C(n,j))"
  isstatedasageneric/heuristicseparation,notatheorem;thefinitecheck
  (below) is to confirm the mechanism (C1>>C2 for t>=2, C1=C2 for t=1), not the
asymptotic rate. Small-n finite data illustrates the mechanism only.

-Thisdoesnotproveprob:perfiber,conj:B,anyn^{1+o(1)}bound,anyq_gen
  saving, or any protocol/MCA/list/line claim.

  What Codex should bank / test next

  Bank:

  - the locator-quotient decomposition R_E(S)=[W]_E-[L_S]_E[Q_S]_E, deg
  Q_S<=n-a-1,with[W]_EconstantinS;

-therawupperbound#{R_E(S)} <= C(n,n-a);

-theC1(raw)vsC2(bad-lineslope)distinctionandthecodimension-(t-1)
  identification of reserve;

-thesharpenedwallW-F1-AA-RES-LINE-INCIDENCE.

-thelocator-quotientdecompositionR_E(S)=[W]_E-[L_S]_E[Q_S]_E,deg
Q_S<=n-a-1, with [W]_Econstant in S;
- the raw upper bound #{R_E(S)} <= C(n,n-a);
C1 (raw) vs C2 (bad-line slope) distinctionandthecodimension-(t-1)
identificationofreserve;
- the sharpened wall W-F1-AA-RES-LINE-INCIDENCE.

Donotbank:anyn^{1+o(1)}incidencebound,anyrefutationoftheslope-count
  wall, or a q_gen collapse.

  Test (extend the Cycle 8 checker, keeping fields separate):

  - B=F_7, F=F_49. Two regimes on D=F_7: (i) t=2,k=3,a=5,j=2 (separated
  aperiodicE,deg 2);(ii)t=1,k=4,a=5,j=2(ElinearoverF).

-Enumeratealla-subsetsS(equivalentlyco-supportsT,|T|=j).Forrandom
  base anchors w0,w1:D->B and nonzero Bnum:

a.verifythedecompositionR_E(S)==[W]_E-[L_S Q_S]_Eanddeg Q_S<=j-1;

b.tabulateC1 = #distinct R_E(S)andC2 = #distinct slopes z(thoseSwith
  R_E(S) in F*[Bnum]_E);

c.confirmregime(i)givesC2 << C1(badlinecodim 1)andregime(ii)
  gives C2 == C1 (bad line = whole space), reproducing the sigma=1 sub-reserve
  behaviorasthecodim-0endpoint.

-Thenscansmallgrowingp/natfixedj=2towatchwhetherC2stays
  n^{1+o(1)}-like while C1 tracks C(n,2); emit a certificate of the gap. This is
  theminimaldatathatdistinguishesthereal(incidence)wallfromthe
  trivial raw-count statement.

-B=F_7,F=F_49.TworegimesonD=F_7:(i)t=2,k=3,a=5,j=2(separated
aperiodic E, deg 2);(ii) t=1,k=4,a=5,j=2 (E linear over F).
- Enumerate all a-subsetsS (equivalentlyco-suppots T,|T|=j).Forrandom
base anchors w0,w1:D->B andnonzero Bnum:
  a.verify the decompositio R_E(S)==[W]_E-[L_S Q_S]_Eanddeg Q_S<=j-1;
btabulate C1 = #distinct R_E(S) and C2 = #distinct slopes z (those S with
R_E(S) in F*[Bnum]_E);
  c. confirm regime (i)givesC2 << C1(badlinecodim 1)andregime(ii)
gives C2 == C1 (badlne = whole space), reproducing the sigma=1 sub-reserve
behavior as the coim-0 endpoint.
- Then scnsmall growing p/n a fixedj=2towatchwhetherC2stays
n^{1+o(1)}-like while C1 tracks C(n,2); emi a certificat of the gap.Thisis
the minimal data thatdisinguishes thereal(incidence) wallfrom the
rivial rw-count statement.
