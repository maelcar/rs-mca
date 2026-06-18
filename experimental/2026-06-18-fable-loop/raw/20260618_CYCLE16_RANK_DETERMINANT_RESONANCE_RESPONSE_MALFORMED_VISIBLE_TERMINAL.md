Ihave the requiredledgers.Two filsnamed i theprompt are not in his
snapshot, whichI record below, thnI recontruct the Cycle 15 setup from
ROUTE_BOARD_CURRENT.md, BANKED_LEMMAS.md, ACTIVE_WALLS.md, and
NEXT_PROMPT_QUEUE.md (which carry thecolumns verbatim) nd attack th
rank/determinant obstruction directly.

---

  Parameters (field ledgers kept separate)

Parameters(fieldledgerskeptseparate)

B=F_pq_gen=p(generated/entropy/basefield,D=F_p,n=p)

F=F_{p^2}q_line=p^2(extension/linefield)

q_chalunused

t=sigma=2j=n-a=r-t=3a=n-3,k=n-5

eta=sigma/n=2/n(sub-reserve;thiswholewallis
  sub-reserve)

A=F[X]/E,dim_FA=2,dim_BA=4;b=[Bnum]_E!=0;ω:=
  wedge([W]_E,b) ∈ F^*

WorkoffR0={ω=0}.{[W]_E,b}isthenanF-basisofA.

  AUDIT 1 — two named source files are absent from this run snapshot

  current_loop_.../audits/20260618_CYCLE15_SURFACE_SLOPE_FIBER_AUDIT.md and
  .../local_checks/20260618_cycle15_forced_ra_slope_scan_certificate.mdarenot
  present in FILE_INDEX_FOR_MODEL.md. The mounted local-checks stop at Cycle 9;
DIRECTOR_STATE.md points the Cycle 15 artifacts at an external
/Users/danielcabezas/OpenClaw/... paththatisnotintheread-onlycopy.I

thereforereconstructtheCycle15columnsandtheRa/Rbreductionfromthe

fourbankedledgers,allofwhichtranscribethemidentically,andIflag

everystepthatdependsontheunavailabledetailedA0,B0coefficients.

  AUDIT 2 — Cycle 15 columns are correct as stated (no index mismatch)

  Substituting A0=p1[W]_E+p2 b, B0=q1[W]_E+q2 b (off R0) into L_z=iota-z
  mu=(A0-tau_3[W]_E)-z(B0-tau_3b):

L_z=(p1-zq1-tau_3)[W]_E+(p2-zq2+ztau_3)b.

  Collecting the B-affine structure L_z = c0(z) + tau_1 c1(z) + tau_2 c2(z) +
  tau_3c3(z)withp_i=p_i^0+p_i^1tau_1+p_i^2tau_2,q_ilikewise:

c1(z)=(p1^1-zq1^1)[W]_E+(p2^1-zq2^1)b,

c2(z)=(p1^2-zq1^2)[W]_E+(p2^2-zq2^2)b,

c3(z)=-[W]_E+zb,

c0(z)=(p1^0-zq1^0)[W]_E+(p2^0-zq2^0)b.(c0madeexplicit)

  c1,c2,c3 match the prompt and the ledgers verbatim. The [W]_E-row of c3 is -1,
  theb-rowisz—consistenteverywhere.Noindexmismatchfound;Iproceed
  with these.

  ---

  PROOF — realification identity, degree bound, and the safe side Q != 0 => O(p)

PROOF—realificationidentity,degreebound,andthesafesideQ!=0=>O(p)

WriteeachcolumnintheF-basis{[W]_E,b}asc_i=f_i[W]_E+g_ib,giving
  F-coordinates

(f_1,g_1),(f_2,g_2),(f_3,g_3)=(-1,z),(f_0,g_0),eachf_i,g_i∈Faffineinz.
  Let δ = α - α^τ ∈ F^* (τ = the F/B-involution), so δ^2 ∈ B^*. Realifying A ≅
  B^4intheB-basis{[W]_E,α[W]_E,b,αb},the4×4B-determinantequalsthe
  conjugate-doubled F-determinant up to the basis discriminant:

Q(z)=(1/δ^2)·det_F[N;N^τ],N=[f_1f_2f_3f_0;g_1g_2g_3
  g_0 ].

  (Verified on the F=ℂ,B=ℝ model: det=−4, δ^2=−4, Q=1.) Since δ^2 ∈ B^*, Q != 0
  ⟺det[N;N^τ]!=0.

  Degree. Each f_i,g_i is degree ≤1 in z, so each 2×2 F-minor m_{ij}(z) is
  degree≤2inz.Treatingz=z_0+αz_1,theconjugatefactorm_{kl}(z)^τis
  degree ≤2 in (z_0,z_1); hence every Laplace term m_{ij}(z)m_{kl}(z)^τ and
therefore Q(z_0,z_1) has total degree ≤ 4 in (z_0,z_1) ∈ B^2.

  Safe side. If Q ≢ 0, then by Schwartz–Zippel a nonzero degree-d polynomial
  overF_pin2variableshas≤d·pzeros,so

C2≤#{z∈F:Q(z_0,z_1)=0}≤4p=O(p)=O(n).

  This is unconditional (given R0-complement, where {[W]_E,b} is a basis) and
  reproducestheCycle15"Q!=0⟹curve-sized"sidewithanexplicitconstant
  4p. ∎

---

  BANKABLE_LEMMA — determinant–trace formula tying Q to the slope quadratic

BANKABLE_LEMMA—determinant–traceformulatyingQtotheslopequadratic

Identifythecolumn-3minorswiththeCycle14slope-quadraticcoefficients.
  With Φ_i(z) := q1^i z^2 - (p1^i - q2^i) z - p2^i (so the landing quadratic is
  Φ(z,tau)=Φ_0+Φ_1tau_1+Φ_2tau_2=q1z^2-(p1-q2)z-p2):

m_{13}=zf_1+g_1=-Φ_1(z),

m_{23}=zf_2+g_2=-Φ_2(z),

m_{34}=-(g_0+zf_0)=Φ_0(z).

  Laplace expansion of det[N;N^τ] along its first two rows, using Tr(x)=x+x^τ,
  givestheexactidentity

δ^2·Q(z)=Tr(m_{12}Φ_0^τ)+Tr(Φ_1m_{24}^τ)-Tr(m_{14}Φ_2^τ),

  where m_{12},m_{14},m_{24} are the (z-affine, degree ≤2) minors of the
  {tau_1,tau_2,const}columns{c1,c2,c0}.Thesameminorsobeythe
  Grassmann–Plücker relation

m_{12}Φ_0+Φ_1m_{24}-m_{14}Φ_2=0(identicallyinz,overF).

  Thus Q is precisely the τ-twisted (trace) version of the Plücker combination
  whoseuntwistedversionisidenticallyzero.Thisisexactand
  source-checkable from the Cycle 14 forms; it does not bound C2 by itself.

---

  EXACT_NEW_WALL — W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER-RANK-DET-SPLIT

EXACT_NEW_WALL—W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER-RANK-DET-SPLIT

(i)ClosedcriterionforQ≡0

  View z,w as independent (the change (z_0,z_1) ↦ (z,z^τ) is an F-linear
  isomorphism).Set

U(z)=(m_{12},Φ_1,-m_{14}),V(z)=(Φ_0,m_{24},Φ_2)withmonomial-coefficient
  vectors U_k,V_l ∈ F^3 (k,l ∈ {0,1,2}), and H_{kl} := U_k · V_l^τ ∈ F (ordinary
  dotproduct).Then

δ^2Q=Σ_{k,l}(H_{kl}+H_{lk}^τ)z^kw^l,

soQ≡0⟺H_{kl}+H_{lk}^τ=0forallk,l∈{0,1,2}.

  This is a finite, exactly checkable conjugate-skew Gram criterion (9 entries;
  diagonalforcesTr(U_k·V_k^τ)=0).Itistherequestedsymbolicclassification
  of Q==0. The Plücker relation gives the companion untwisted identity Σ_{k+l=m}
U_k·V_l = 0; Q≡0 is the independent twisted condition, so genericdatahasQ
≢ 0.

  (ii) Q ≡ 0 ⟺ the slope map is dominant on the resonance surface

  On Ra (Cycle 13: Delta ∈ F^*·\bar B[tau]), Ψ(tau) := (p1-tau_3)(q2-tau_3)-p2
  q1∈B[tau],sothelandinglocusSigma={Ψ=0}isoneB-quadricsurface(~p^2
  points), and the slope is the rational map z = (p1-tau_3)/q1 : Sigma → F.
Because Q of degree ≤4 < p, Q≡0 ⟺ z is dominant (image cofinite,Θ(p^2)),and
Q≢0 ⟺ image O(p).

  (iii) Correction (forbidden-overclaim guard): Q ≡ 0 does NOT yield a
  counterpacketbyitself

  Q is pure B-linear algebra over all tau ∈ B^3; it ignores the split-cubic
  constraint.AdimensioncountsuggestsQ≡0isthegenericbehaviouronRa
  (on Sigma: 3 unknowns tau, landing Ψ=0 is 1 B-equation, slope=z is 2
B-equations → 3=3, solvable for a positive fraction of z). So thenaivelemma
"prove Q!= 0 on all Ra/R" is liklyfalse,andabareQ≡0exampleisnota

counterpacket.TheactualMCAcountrequirestautobeagenuineD-splitcubic

withdistinctrootsinF_p:

RESIDUALWALL:whenQ≡0onasource-validresonancesurfaceSigma,

doeszrestrictedtosplit-distinctco-supportsT⊂D=F_prealise

Θ(p^2)=Θ(q_line)distinctslopes,ordoesthesplit-distinctlocus

collapsetheimagetoO(p)?

  This is exactly the old fixed-slope fiber-collapse problem, now isolated to
  thesinglecase{Q≡0}∩{split-distinct}.Theonlymountedempiricaldatum
  (forced_ra_slope_scan, p=7, 12 seeds, C2≤6, EXPERIMENTAL) is consistent with
collapse and in tension with the genericity heuristic — most plausiblya
small-p effect or a real collapse; itcannotdecidethescalinglaw.I

thereforedonotbankslopecollapse,donotbankaΘ(q_line)counterpacket,

andmakenoq_gen/protocol/list-decodingclaim.

  (iv) Scanner spec (exact I/O / certificate) to resolve the residual wall

INPUT:primep;E(deg2,separated,aperiodic,nonzeroonF_p);Bnum(deg<2,
  b!=0);

baseanchorsw0,w1:F_p->F_p;n=p,a=n-3,k=n-5.

DERIVE:A0,B0(Cycle14)->p_i^j,q_i^j∈F->columnsc1,c2,c3,c0.

STEPA(resonancefilter):computeDelta=Delta_0+αDelta_1;keeponlydatain

Ra(Delta_0,Delta_1B-proportional)orRb(shared\barB-linear
  factor).

STEPB(Q-test):evaluateH_{kl}=U_k·V_l^τ;flagQ≡0iffH_{kl}+H_{lk}^τ=0
  ∀k,l

(cross-check:deg(Q)≤4,sampleQat5p+1points(z_0,z_1)).

STEPC(count,Q≡0branchonly):enumeratesplit-distinctT⊂F_p(|T|=3),

recordz(T)=(p1-tau_3)/q1;outputC1,C2=#distinctz,fiberhistogram
  of z,

andmaxoverseeds.

CERTIFICATE(perinstance):

{p,E,Bnum,w0,w1,stratum∈{Ra,Rb},Q_identically_zero:bool,

degQ,H_matrix,C1,C2,fiber_sizes:[...],split_triples_examined,

status∈{PASS_Qnonzero_O(p),OPEN_Qzero_collapse?,COUNTERPACKET_C2~p^2}}

PASS:Q!=0(thenC2≤4pproven).

TRIGGER(counterpacket,sub-reserve):areproduciblefamilywithQ≡0AND

C2/p^2boundedbelowacrossgrowingp.Asinglepisinsufficient.

  ---

  What is and is not banked

Whatisandisnotbanked

-BANKABLE_LEMMA(new,exact):δ^2Q=Tr(m_{12}Φ_0^τ)+Tr(Φ_1
  m_{24}^τ)-Tr(m_{14}Φ_2^τ), the minor↔slope-quadratic identities m_{13}=-Φ_1,
  m_{23}=-Φ_2,m_{34}=Φ_0,thePlückerrelation,andQ≢0⟹C2≤4p=O(n)offR0.

-EXACT_NEW_WALL(primary):Q≡0⟺H_{kl}+H_{lk}^τ=0∀k,l⟺slopemapdominant
  on Sigma; and the corrected residual wall is the split-distinct realisation
  inside{Q≡0},notQ≡0alone.

-NOTclaimed:anyproofofconj:B;slopecollapseonRa/Rb;aΘ(q_line)
  counterpacket; that rank 3 alone decides; any result above corrected reserve;
  anyq_gencollapse;anyprotocol/MCA/CA/list-/line-decoding/SNARKconsequence;
  no reuse of the generic complete-intersection lemma for Ra/Rb.

Classifiction

EXACT_NEW_WALL
