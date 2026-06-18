Ihave he fullledger, the source efinitins (df:rsidue, thm:normalform,
prob:perfiber,conj:B, rem:aper), the Cycle 9 locator‑quotient reduction, and
the Cycle 11 j=2closd form. One onstraint: code xecutionis disbledin
this environment (te Jupyter tool ws denied and there is o hell), s I
derive everything alytically and ship thscanner as aspc rather thn
running it. I fag the numercsas pending.

---

  Classification: EXACT_NEW_WALL

Classification:EXACT_NEW_WALL

(carryinganembeddedBANKABLE_LEMMA:thet=2,j=3quotientclosedformandthe
  bad‑locus quadric with its leading coefficient. The slope bound itself is not
  reachablebytheCycle‑11methodandreducestooneprecisely‑namedmissing
  invariant.)

---

Exactstatement

Exactstatement

Bankablestructuralpart(rigorous).Intheregime

B=F_p,F=F_{p^2},D⊆B,w=w0+αw1withw0,w1:D→B,E∈F[X]separated/aperiodic
  with deg E=t=2 nonzero on D, deg Bnum<2, [Bnum]_E≠0, balanced a=k+t, σ=t=2,
  andj=n−a=r−t=3(soa=n−3,k=n−5,degQ_S≤2),writeW=interp_D(w)=ΣW_mX^m,
  top coefficients W_{n-1},W_{n-2},W_{n-3}∈F, and co-support T=D\S with
τ_i=e_i(T), E_i=e_i(D). Then the locator quotient W=L_S Q_S+I_S hastheclosed
form

Q_S=W_{n-1}·X^2

+(W_{n-2}+W_{n-1}E_1)·X

+(W_{n-3}+W_{n-2}E_1+W_{n-1}(E_1^2-E_2))

−τ1·(W_{n-1}X+W_{n-2}+W_{n-1}E_1)

+τ2·(W_{n-1}).

  For D=F_p (E_1=E_2=0) this collapses to

Q_S=W_{n-1}(X^2−τ1X+τ2)+W_{n-2}(X−τ1)+W_{n-3}.

  So Q_S is affine in (τ1,τ2)=(e1(T),e2(T)) and independent of τ3=e3(T). This is
  theexactj=3analogueofCycle11'sQ_S=C(X−s_T)+C1:thequotientseesone
  more co-support parameter (τ2) but still not the top one (τ3).

  Bad-line incidence equation (rigorous). Set A=F[X]/E (dim_F A=2), wedge
  ∧:A×A→Fthe2×2determinant,W_E=[W]_E,B_E=[Bnum]_E,L_{D,E}=[L_D]_E,
  μ=[Q_S]_E, λ=[L_T]_E. Since E is nonzero on D, λ is a unit with
N_{A/F}(λ)=∏_{d∈T}E(d)≠0. A slope z exists for T iff

Δ(T):=(W_E·λ−L_{D,E}·μ)∧(B_E·λ)=0,

  and then z is unique (Cycle 2). Using N(λ)=det(M_λ) and λ=λ0−τ3 with
  λ0=ξ3−τ1ξ2+τ2ξ(ξ=[X]_Eetc.):

Δ=(W_E∧B_E)·(τ3^2−Tr(λ0)τ3+N(λ0))−⟨μ,λ0⟩+τ3·⟨μ,1⟩,

⟨x,y⟩:=(L_{D,E}x)∧(B_Ey).

  Δ is a quadric surface in (τ1,τ2,τ3)∈A^3, and

[τ3^2]Δ=W_E∧B_E=[W]_E∧[Bnum]_E.

  So, exactly as in Cycle 11, the coefficient of the free top co-support
  parametersquaredis∧([W]_E,[Bnum]_E);Δ≡0forcestheglobal/tangent
  endpoint.

  Wall part (the new obstruction). Cycle 11's bound C2=O(n) came only from
  solution-counting:atj=2,thebadlocusisaconicin2-dimco-supportspace,
  meeting ≈ C(n,2)/p = O(n) subsets for n≈p, so trivially C2=O(n). At j=3 the
bad locus is the quadric Δ=0 in 3-dim co-support space, meeting

#{T:Δ(T)=0}≈C(n,3)/p≈n^2/6(n=p),

  which for D=F_p (n=p) is Θ(n^2)=Θ(q_line) — the solution-counting bound is
  vacuous.Hencethet=2line-incidencelawhasitsfirstgenuinewallexactly
  at j=3, and any nontrivial C2 bound must come from slope collapse, not
solution-counting.

---

  Proof / counterpacket data

Proof/counterpacketdata

DerivationofQ_S(rigorous):degI_S<a=n−3,sothethreetopcoefficients
  X^{n-1},X^{n-2},X^{n-3} of W come entirely from L_S Q_S. Matching them with
  L_S=Σ(−1)^me_m(S)X^{a−m}givesq_2=W_{n-1},q_1=W_{n-2}+W_{n-1}e_1(S),
  q_0=W_{n-3}+W_{n-2}e_1(S)+W_{n-1}(e_1(S)^2−e_2(S)). Substituting
e_1(S)=E_1−τ1, e_2(S)=E_2−E_1τ1+τ1^2−τ2 (disjoint-union symmetricidentities)
yields he boxed form; heW_{n-1}-coefficientofq_0simplifiesto

E_1^2−E_2−E_1τ1+τ2.Independencefromτ3isstructural:onlye_1(S),e_2(S)

enter,whichdependonτ1,τ2(andconstantsE_i)butneverτ3.∎

  Incidence/Δ: [I_S]_E∈F·B_E ⇔ [I_S]_E∧B_E=0 (true line characterization since
  B_E≠0indim2).FromL_T·I_S=L_TW−L_DQ_SreducedmodE:
  λ[I_S]_E=λW_E−L_{D,E}μ, so [I_S]_E∧B_E scaled by the unit λ gives Δ above. The
norm expansion det(M_{λ0−τ3})=τ3^2−Tr(λ0)τ3+N(λ0) and bilinearityof⟨·,·⟩
give thedisplayed quadricand [τ3^2]Δ=W_E∧B_E.∎

  Why it is a wall, not a proof or a counterpacket:

  - Not PROOF/BANKABLE of a C2 bound — the only available bound is
  C2≤#{Δ=0}=O(n^2)=Θ(q_line),vacuousforn≈p.TheCycle-11collapsemechanism
  (slope factors through one co-support parameter) fails: z(T) genuinely depends
on τ1,τ2,τ3 (via μ(τ1,τ2) and λ(τ1,τ2,τ3)), so the fibersarenotforced
small bytheclosed orm alone.

-NotCOUNTERPACKET—thisregimeissub-reserve(η=σ/n=2/n→0),andlargeC2
  sub-reserve is expected and is forbidden as a refutation of corrected-reserve
  conj:B.Ialsocannotexhibitexplicitexcess-slopedatawithoutrunningthe
  scanner (disabled here).

-NotPROOF/BANKABLEofaC2bound—theonlyavailableboundis
C2≤#{Δ=0}=O(n^2)=Θ(q_line), vacous for n≈p. The Cycle-11 collapsemechanism
(slope factors through one co-spport parameter)fais: z(T) genuinely depends
on τ1,τ2,τ3 (via μ(τ1,τ2) and λ(τ1,τ2,τ3)), so the fibers are not force
small by the closed form alone.
- NotCOUNTERPACKET— this regimeissub-reserve(η=σ/n=2/n→0),andlargeC2
sub-reserve is expected and is forbidden as a rfutation of corrected-eserve
conj:B. I alsocanno exhibit explicit excess-slope datawithut running the
scanner(disabled here).

Theexactmissinginvariant.Theslopemapz|_{{Δ=0}}sendsthe≈n^2/6
  solution subsets to its image. For fixed z, the locus is a line ℓ_z=ker M(z)
  in(τ1,τ2,τ3)-space(M(z)isthe2×4matrixofthetwoA-components,entries
  affine in z). Thus

C2=#{z:ℓ_zmeetsthecubic-splittinglocusofD},

=(#solution-T)/(avgfibersize),fiber=#{3-subsetsofDonℓ_z}.

  The wall is precisely: the generic fiber size of z on {Δ=0} = the typical
  numberofdistinct-rootcubicsX^3−τ1X^2+τ2X−τ3splitoverDalongalineℓ_z.
  If generic lines ℓ_z carry Θ(n) split cubics, then C2=Θ(n)=n^{1+o(1)}
(collapse holds, law survives). If the relevant ℓ_z are thespecial"fixed
(τ1,τ2),vary τ3" drecions (wher Δ=0isaquadraticinτ3with≤2roots,

contributingO(1)per(τ1,τ2)),thenC2canreachΘ(n^2)=Θ(q_line)andthelaw

failssub-reserve.Thissplit—genericvs.axis-aligneddirectionofℓ_z

againstthecubic-splittinglocus—isthesinglenewinvariantthatreplaces

theCycle11conic.

  ---

  Field ledger

Fieldledger

q_gen=pB=F_p:D,w0,w1,baselocatorsL_S,L_D,L_T,τ_i=e_i(T)

q_line=p^2F=F_{p^2}:α,E,Bnum,residuesinA=F[X]/E,slopesz,∧,
  N_{A/F}

q_chal=unused(noprotocol/challengeobjectinvoked)

B,Fkeptstrictlyseparate;noq_gencollapseclaimed.

  Parameter ledger

n=|D|(startD=F_p,n=p)t=σ=degE=2j=n−a=r−t=3

a=k+t=n−3k=n−5r=n−k=5

degQ_S≤j−1=2degBnum<2,[Bnum]_E≠0

co-support|T|=3,paramse1(T),e2(T),e3(T);Q_Sindep.ofe3(T)

badlineF[Bnum]_E⊂A:codimt−1=1reserveη=σ/n=2/n(sub-reserve)

Δ:totaldegree2in(τ1,τ2,τ3);[τ3^2]Δ=[W]_E∧[Bnum]_E

  Source dependencies (by label)

  - slackMCA_v3.tex:def:residue (≈L1189) — slope/witness Q_z≡zB mod E,
  noncontainment.

-slackMCA_v3.tex:thm:normalform(≈L1197)—emca=(1/q)·max_tΛ^{NC};slopes
  are the object, not raw residues.

-slackMCA_v3.tex:prob:perfiber(≈L1227),conj:B(≈L1231)—corrected-reserve
  n^{1+o(1)} is above-reserve; this regime is sub-reserve.

-slackMCA_v3.tex:rem:aper(≈L1255)—quotient-periodicdenominatorsstay
  separated; E aperiodic.

-Cycle9locator-quotientW=L_SQ_S+I_S,[I_S]_E=[W]_E−[L_SQ_S]_E;Cycle11
  j=2 conic and [free^2]Δ=∧([W]_E,[Bnum]_E); Cycle 2 slope-uniqueness; Cycle 3
  auto-noncontainmentfor|S|≥a,Bnum≠0.

  ---

  What Codex should bank

WhatCodexshouldbank

1.F1t=2,j=3quotientclosedform(BANKABLE_LEMMA):theboxedQ_S(generalD
  and D=F_p); Q_S is affine in (e1(T),e2(T)) and independent of e3(T).

2.F1t=2,j=3bad-locusquadric(BANKABLE_LEMMA):Δ(τ1,τ2,τ3)isadegree-2
  surface with [e3(T)^2]Δ=[W]_E∧[Bnum]_E; Δ≡0 ⇔ tangent/global endpoint (same
  resonancesignatureasCycle 11).

3.F1j=3solution-countingvacuity(EXACT_NEW_WALL):forn≈p,#{Δ=0}≈C(n,j)/p
  is O(n) at j=2 but Θ(n^2)=Θ(q_line) at j=3; Cycle 11's method dies exactly
  here.

4.W-F1-AA-RES-T2J3missinginvariant:genericfibersizeofz|_{{Δ=0}}=
  typical count of D-split cubics along the line ℓ_z=ker M(z); collapse ⇒
  C2=Θ(n),nocollapse⇒C2uptoΘ(q_line).

  What Codex must NOT bank

  - Any C2 bound (upper or lower) as proved — it is open pending the fiber
  invariant+scanner.

-RawresiduecardinalityC1astheMCAobject.

-Anyrefutationofconj:B:thisregimeissub-reserve(η=2/n);largeC2here
  is not an above-reserve counterpacket.

-Anyq_gencollapse;anyprotocol/MCA/CA/list-/line-decoding/SNARK
  consequence; any extension to j≥4, t≥3.
  -Cycle11beyondt=2,j=2.

---

  Suggested verifier/checker (spec — not executed here)

Suggestedverifier/checker(spec—notexecutedhere)

Extend20260618_cycle11_t2_j2_line_incidence_verify.py.Pseudocode:

forpin{7,11,13,17,19}(n=p,D=F_p):

picknonresiduenr->F=F_{p^2};choosealpha=(0,1)
    for trials:

E=randommonicdeg-2inF[X],separatedgcd(E,E^tau)=1,aperiodic,
  nonzero on D

Bnum:deg<2,[Bnum]_E!=0(sweeprandomANDadversarial:Bnum∥leading
  data)

w0,w1:D->Brandom;w=w0+alpha*w1;W=interp_D(w)
      a=n-3 (t=2,j=3)
   #(A)verifyclosedform

forSinC(D,a):

T=D\S;(t1,t2,t3)=e1,e2,e3(T)

Q_S=pdivmod(W,L_S).q

assertQ_S==W_{n-1}(X^2-t1X+t2)+W_{n-2}(X-t1)+W_{n-3}#D=F_p

assertcoeffofQ_ShasNOdependenceont3#varyTwithsame(t1,t2)
      # (B) incidence + slope
   I_S=W-L_SQ_S

RE=[I_S]_E

z=line_scalar(RE,[Bnum]_E)#NoneifREnot∥[Bnum]_E

assert(zisnotNone)==(Delta(t1,t2,t3)==0)#cross-checkquadric

ifz:recordz,and(t1,t2,t3)

report:C1=#distinctRE,C2=#distinctz,#solution-T,

[tau3^2]Delta==wedge([W]_E,[Bnum]_E),

histogramoffibersizes#{T->givenz}#<--thewall
  invariant

EMITcounterpacketbundleifC2grows~n^2(note:sub-reserve,notaconj:B
  refutation)

  Targets to read off: (i) confirm [τ3^2]Δ=[W]_E∧[Bnum]_E; (ii) the fiber-size
  histogramofz—itsmeanisthedecidinginvariant(Θ(n)⇒C2=Θ(n);O(1)⇒
  C2=Θ(n^2)); (iii) keep q_gen=p, q_line=p^2 columns separate; (iv) optionally
run t=3,j=2 (P2) for the codimension-2 comparison.

  Verification status: closed form and Δ/leading-coefficient are proved by hand
  above;thefiber-collapsenumericsarepending(noexecutionavailableinthis
  environment).
