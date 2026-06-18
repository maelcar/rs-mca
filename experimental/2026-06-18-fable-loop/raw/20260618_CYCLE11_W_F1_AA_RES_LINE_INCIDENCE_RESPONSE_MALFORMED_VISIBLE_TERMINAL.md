I've hit a tooling limit: code execution (mcp__ide__executeCode) is denied and
Write is disabled in this harness, so I cannot run a fresh verifier
in-session. I derived the result by hand and cross-checked it against the
existing Cycle 9 numerical receipts (which already tabulate this exact regime:
t=2, n=7, C2 ∈ {0,2}). I'll provide a runnable verifier as a listing for
Codex. The mathematics below is complete and self-contained.

---

Finalclassification:BANKABLE_LEMMA

Finalclassification:BANKABLE_LEMMA

1. Precise statement

  Setup exactly as the prompt: B=F_p, F=F_{p^2}, D ⊆ B, |D|=n; w=w0+α·w1 with
  w0,w1:D→B;W=interp_D(w),deg W ≤ n-1;E∈F[X]separatedaperiodic,deg
  E=t=σ=2, gcd(E,E^τ)=1, E nonzero on D; numerator Bnum, deg Bnum<2, [Bnum]_E≠0.
Balanced ledger a=k+t, with the first finite incidence regime j=n-a=r-t=2,
i.e. a=n-2, k=n-4. Co-support T=D\S,|T|=j=2,T={d1,d2},s_T=d1+d2,p_T=d1d2.

  Write R:=F[X]/E ≅ F^2 and ε:=[X]_E. Let wedge(u,v) be the F-determinant on
  R≅F^2,andκ:=wedge([W]_E,[Bnum]_E).LetC:=[W]_{n-1}(leadingcoeffofW,
  =Σ_{d∈D} w(d)/L_D'(d)) and C_1:=[W]_{n-2}+C·σ_1(D), σ_1(D)=Σ_{d∈D}d.

  Lemma (Cycle 11 — t=2, j=2 bad-line incidence).

  (a) Locator-quotient rigidity. For every a-subset S with co-support T,

Q_S=C·(X-s_T)+C_1,degQ_S≤1,

Q_S=C·(X-s_T)+C_1,degQ_S≤1,

soQ_SdependsonTonlythroughthesums_T,neverthroughtheproductp_T.

soQ_SdependsonTonlythroughthesums_T,neverthroughtheproductp_T.

(b)Incidence = a single conic.DefineP := [W]_E·[L_T]_E − [L_D]_E·[Q_S]_E ∈
  R and B'' := [Bnum]_E·[L_T]_E ∈ R; both are affine-linear in (s_T,p_T). Set

det(s,p):=wedge(P,B'')∈F[s,p],deg≤2.

det(s,p):=wedge(P,B'')∈F[s,p],deg≤2.

ThenSlandsonthebadline([I_S]_E = z[Bnum]_Eforsomez∈F)iff
  det(s_T,p_T)=0, and the slope z is then unique.

ThenSlandsonthebadline([I_S]_E = z[Bnum]_Eforsomez∈F)iff
det(s_T,p_T)=0,andtheslope z is then unique.

(c)Leading coefficient is κ.det = κ·N([L_T]_E) − wedge([L_D]_E·[Q_S]_E,
  [Bnum]_E·[L_T]_E), and the coefficient of p^2 in det equals κ. Hence det≡0 ⟹
  κ=0,i.e.[W]_E∈F[Bnum]_E(theglobal-codeword/tangentendpointof
  rem:strata).

  (d) Linear incidence bound. Define the online slope / bad-line incidence count

C2=#{z∈F:∃noncontaineda-subsetSwith[interp_S(w0)+αinterp_S(w1)]_E=
  z[Bnum]_E }.

C2=#{z∈F:∃noncontaineda-subsetSwith[interp_S(w0)+αinterp_S(w1)]_E=
z[Bnum]_E }.
If det≢0 thenC2 = O(n);concretelyC2 ≤ 6n,andC2 ≤ 4inthenon-resonant
casewherethetwoF_p-componentsofdet(inanyF_p-basisofF)shareno
  common factor (Bézout). The resonant case det≡0 cannot occur whenever D
  containstwo2-subsetswithequalsums≠-e_1anddistinctproductsandC≠0—
  in particular for D=F_p, p≥7, with deg W=n-1. Therefore, for D=F_p, p≥7,

C2≤6n=O(n)unconditionally,andC2≤4generically.

C2≤6n=O(n)unconditionally,andC2≤4generically.

Everylandinga-subsetisautomaticallyanoncontainedwitness(Cycle3lemma,
  Bnum≠0), so C2 is exactly the noncontained slope count contributed by
  support-size-awitnessesofthisdatum—thegenuinedef:residue/
  thm:normalform object, not the raw residue cardinality C1.

2. Proof

  (a) Euclidean division W=L_S Q_S+I_S with deg I_S<a=n-2, deg L_S=a, gives deg
  Q_S≤(n-1)-a=1=j-1.MatchtopcoefficientsofW=L_S Q_S+I_S(recallI_Shas
  degree ≤n-3, so it is invisible at X^{n-1},X^{n-2}): the X^{n-1} coefficient
gives q_1=[W]_{n-1}=C; the X^{n-2} coefficient gives
[W]_{n-2}=q_1·[L_S]_{n-3}+q_0=C·(−e_1(S))+q_0,where

e_1(S)=Σ_{d∈S}d=σ_1(D)−s_T.Henceq_0=[W]_{n-2}+C·σ_1(D)−C·s_T=C_1−C·s_T,i.e.

Q_S=C·X+(C_1−C·s_T)=C(X−s_T)+C_1.∎

  (b) L_D=L_S·L_T, and since E is nonzero on D, [L_D]_E,[L_T]_E∈R^×, so
  [L_S]_E=[L_D]_E[L_T]_E^{-1}.Thus

[I_S]_E=[W]_E−[L_D]_E[L_T]_E^{-1}[Q_S]_E,and[I_S]_E[L_T]_E=P.Landing
  [I_S]_E=zB' (B':=[Bnum]_E) ⟺ P=z·B'[L_T]_E=z·B''. In R≅F^2 this single-unknown
  systemissolvableforz∈FiffP∥B''iffwedge(P,B'')=0;sinceB'≠0and
  [L_T]_E∈R^×, B''≠0, so z is unique (this is the banked Cycle 2 uniqueness).
[L_T]_E=(p−e_0)−(e_1+s)ε and [Q_S]_E=(C_1−Cs)+Cε areaffine-linear in (s,p),
so P,B'' are affine-linear and det=wedge(P,B'')hastotaldegree≤2.∎

  (c) For u,x,y∈R, wedge(xu,yu)=det(M_u)·wedge(x,y)=N(u)·wedge(x,y)
  (multiplicationM_uscalestheareaformbyitsdeterminant=N(u)).With
  u=[L_T]_E, v=[Q_S]_E:

det=wedge([W]_E·u−[L_D]_E·v,B'·u)

=N(u)·wedge([W]_E,B')−wedge([L_D]_E·v,B'·u)

=κ·N(u)−wedge([L_D]_E·v,B'·u).

det=wedge([W]_E·u−[L_D]_E·v,B'·u)
   N(u)·wedge([W]_E,B') − wedge([L_D]_E·v,B'·u)
κ·N(u) − wedge([L_D]_E·v, B'·u).

N(u)isaquadraticformin(s,p)whosep^2-coefficientis1;visp-free,so
  the second term is degree ≤1 in p. Hence [p^2]det=κ. So det≡0 ⟹ κ=0. ∎

N(u)isaquadraticformin(s,p)whosep^2-coefficientis1;visp-free,so
the second term is degee ≤1 in p. Hence [p^2]det=κ. Sodet≡0 ⟹ κ=0. ∎

(d)Substitution / Bézout.ChooseanF_p-basis{1,α}ofF.Then
  det=det_0+α·det_1 with det_0,det_1∈F_p[s,p], deg≤2. Realizable points
  (s_T,p_T)=(d1+d2,d1d2)∈F_p^2;landingrequiresdet_0=det_1=0.Ifdet_0,det_1
  share no common factor, Bézout over F_p gives ≤4 common points, hence ≤4
co-supports and C2≤4. If they share a component: alineαs+βp=γ meets
{(d1+d2,d1d2)} in O(n) points (for eachd1∈D,(α+βd1)d2=γ−αd1has≤1solution

unlessα+βd1=0,ofwhichthereis≤1);asharedconicΓ(s,p)=0pullsbacktoa

symmetricΔ(d1,d2),deg≤2ind2,giving≤2rootsperd1(with≤O(1)

exceptionald1contributing≤neach)—O(n)eitherway.Addingthefinitely

manypointsofthenon-sharedfactor,C2≤6n.

  Exclusion of det≡0. Suppose det≡0. By (c), κ=0. det≡0 ⟺ [I_S]_E∈F·B' for all
  (s,p)(Zariski-dense),i.e.g(s,p):=[L_D]_E[L_T]_E^{-1}[Q_S]_E∈F·B'
  identically. Take two realizable co-supports with equal sum s (so [Q_S]_E=v(s)
coincides) and distinct products p≠p'. Proportionalityforces
wedge(v(s)·u(s,p'),\,v(s)·u(s,p))=N(v(s))·wedge(u(s,p'),u(s,p))=N(v(s))·\big(-

(e_1+s)(p'-p)\big)=0.IfC≠0thenv(s)=(C_1−Cs)+Cεhasnonzeroε-coordinate;

choosingswithN(v(s))≠0(avoidable:N(v(·))isanonzeroquadratic,≤2bad

s)ands≠−e_1,weget(e_1+s)(p−p')=0,acontradiction.ForD=F_p,p≥7,

repeated-sumpairswiths≠−e_1anddistinctproductsexistinabundance,so

det≢0.∎

3.Sourcedependencies

  - slackMCA_v3.tex:1189 def:residue — slopes/noncontained witnesses are the
  countedobject;C2isbuiltfromwitnesses(Q_z=I_S, S)withdeg I_S<k+t=a,
  |S|=a=s_δ, I_S≡z·Bnum (mod E), I_S=w on S.

-slackMCA_v3.tex:1197thm:normalform—emca = (1/q)·max_t Λ^{NC}_{t,δ};the
  lemma bounds the t=2, support-size-a contribution to Λ^{NC}.

-slackMCA_v3.tex:1227/1231prob:perfiber/conj:B—theconjecturalobjectisa
  slope/packing count; the lemma is a one-t, low-reserve instance, not a proof
  oftheconjecture.

-slackMCA_v3.tex:1255rem:aper—quotient-periodicEseparated;thelemma
  uses generic separated aperiodic E (gcd(E,E^τ)=1).

-rem:strata(slackMCA_v3.tex:1209)—theκ=0(det≡0)endpointisthe
  global-explanation/tangent stratum, consistent with the floor.

-Banked:Cycle9locator-quotientdecomposition;Cycle3
  noncontainment-subset lemma (Bnum≠0 ⟹ every a-subset noncontained); Cycle 2
  slope-uniqueness;Cycle8twist↔extension-residueisomorphism(letsuswork
  with [interp_S(w0)+α interp_S(w1)]_E directly).

-thm:exactcount/thm:rigidcycloarenotimported(onlyelementaryEuclid,the
  norm-form identity wedge(xu,yu)=N(u)wedge(x,y), and Bézout).

  4. Field ledger

  - q_gen=p, B=F_p: D, w0, w1, locators L_S,L_T,L_D, the parameters s_T,p_T
  (base-fieldpoints).

-q_line=p^2,F=F_{p^2}:E,Bnum,residuesinR=F[X]/E,slopesz,theform
  det∈F[s,p].

-q_chal:unused.Noq_gencollapseisclaimed:theboundisO(n)(inthe
  number of supports), stated without asserting whether it is governed by q_gen
  vsq_line.

  5. Parameter ledger

  n=|D|; k=ρn=n-4; a=⌈(1-δ)n⌉=s_δ=k+t=n-2; σ=a-k=2; t=σ=2; r=n-k=4; j=n-a=r-t=2;
  deg E=t=2;deg Bnum<2,[Bnum]_E≠0;deg Q_S≤j-1=1;bad-linecodimensioninR
  is t-1=1; reserve η=σ/n=2/n (low-reserve corner). No quotient order,
interleaving/list arity, or protocol parameter is used.

  6. Proof/audit notes

  - The whole mechanism is the codimension-1 jump flagged in Cycle 9: at t=1 the
  badlineisallofRandC2=C1=Θ(q_line)(thebankedσ=1packet);att=2the
  line is codimension 1, landing becomes the conic det=0, and the count
collapses to O(n) (generically ≤4 by Bézout). Thisisconsistent with, and
explains, the Cycle 9 receipts seed=0: t=2 C2=0,seed=1: t=2 C2=2—both≤4,

nevernearq_line=49.

-TherigidityQ_S=C(X-s_T)+C_1(dependenceonthesumonly)iswhatmakesdet
  a genuine degree-≤2 conic rather than something higher; it is the source of
  the≤4genericbound.

-Honestyboundary:withj=2thereareonly\binom{n}{2}=O(n^2)supports,so
  C2=O(n^2) is trivial; the content is the conic/Bézout sharpening to O(n) (and
  O(1)generic)plustheexclusionoftheresonantdet≡0endpoint.Thisdecides
  t=2,j=2 affirmatively but is not progress on the deep regime σ=Θ(n/log n) of
conj:B, where the support count is \binom{n}{a} andreserve is bounded below.

-Forbiddenmovesavoided:notrawC1;twistnotreopened;θnotabsorbed;
  exactcount/rigidcyclo not imported; not the same-slope kernel; no unrestricted
  ass:extension-mca-lift;norawlocatorfibers;σ=1endpointnotused;no
  q_gen collapse; no protocol/MCA/CA/list-/line-decoding claim.

  7. Verifier (for Codex; I could not execute it in-harness)

  Build on 20260618_cycle9_locator_quotient_incidence_check.py. Over B=F_7,
  F=F_7[a]/(a^2-3),D=F_7,t=2,a=5,k=3,j=2,formanyrandomseparated
  aperiodic E and random Bnum (deg<2, [Bnum]_E≠0) and arbitrary base anchors
w0,w1, check for every co-support T:

  1. closed form Q_S = C(X − s_T) + C_1 with C=[W]_{n-1}, C_1=[W]_{n-2}+C·σ_1(D)
  (assertequalstheEuclideanquotient);

2.landingpredicateviadet(s_T,p_T)=wedge(P,B'')agreeswiththedirecttest
  wedge([I_S]_E,[Bnum]_E)=0;

3.[p^2]det == κ = wedge([W]_E,[Bnum]_E);andwheneverdet≡0(allco-supports
  land) assert κ=0;

4.tabulateC2;assertC2 ≤ 6nalwaysandrecordhowoftenC2 ≤ 4(predicted:
  always, unless a shared-component/resonant E,Bnum,w).

  Decision rule for a counterpacket vs confirmation: a reproducible instance
  withC2 > 6n,orwithdet≡0andκ≠0,wouldrefutethelemma.Expectedoutput:
  PASS with C2∈{0,…,4} on essentially all trials (matching the Cycle 9 data),
occasional O(n) only on engineered shared-componentE,Bnum,w.

  Expected finite data (from the Cycle 9 receipts already in-repo, same regime):
  n=7,2n=14,observedC2∈{0,2};bothconsistentwiththegenericC2≤4branch.

  8. What Codex should bank / test next

  Bank: the t=2,j=2 line-incidence lemma (rigidity Q_S=C(X-s_T)+C_1; landing =
  conicdet=0;[p^2]det=κ;det≡0 ⟹ κ=0=global-codewordendpoint;C2≤6n,≤4
  generic; resonance excluded for D=F_p, p≥7, C≠0). Mark it as deciding the
first finite incidence regime affirmatively, explicitlynot a proof of conj:B.

  Do not bank: any extension to j≥3 or t≥3; any n^{1+o(1)} claim in the
  bounded-reserveregime;anyq_gencollapse;any
  protocol/MCA/list-/line-decoding consequence.

  Test next (sharper missing invariant): t=2, j=3 and t=3, j=2. For j=3, deg
  Q_S≤2,soQ_Sacquiresdependenceonp_Taswellass_T—theincidenceobject
  becomes a degree-≤3 curve and the rigidity that gives ≤4 breaks; that is the
next wall. For t=3, the bad line is codimension 2 ina3-dim R, so landing is
two simultaneous conditions and the rightobjectisahigher-codimension

incidencecount.Eitheristhenaturalsuccessorto

W-F1-AA-RES-LINE-INCIDENCE.
