Ihave the full chain. I could not execute code (the kernel tool was deniedin
this harness), so the coefficient derivations below are done by hand and
cross-checked against two independently banked diagnostics: the Cycle-12
leading coefficient [τ₃²]Δ = wedge([W]_E,[Bnum]_E), and the Codex
coeff_component_rank=2, zeros_all_B3=O(p) scan. They agree, which is the main
external check available to me.

  ⏵⏵ don't ask on (shift+tb to cycle)

  Setup and the one structural identity that drives everything

  Ledgers kept separate: B=F_p (q_gen=p), F=F_{p²}=B⊕αB with τ:α↦−α, q_chal
  unused.D=F_p,n=p,t=σ=2,j=n−a=3,co-supportT=D∖S,|T|=3,τ_i=e_i(T)∈B,
  L_T=X³−τ₁X²+τ₂X−τ₃, L_D=X^p−X=L_S·L_T.

  From W=L_S Q_S+I_S, multiply by L_T and use L_D=L_S L_T:

L_T·I_S=L_T·W−L_D·Q_S⟹[L_T]_E[I_S]_E=[W]_E[L_T]_E−[L_D]_E[Q_S]_E
  =: A.

  So with C := [Bnum]_E[L_T]_E, the route-board quadric is

Δ=A∧C=([L_T]_E[I_S]_E)∧([L_T]_E[Bnum]_E)=det(M_{L_T})·([I_S]_E∧
  [Bnum]_E),

  because for a 2×2 multiplication operator M on F[X]/E≅F²,
  (Mu)∧(Mv)=det(M)(u∧v).Heredet(M_{L_T})=Res(L_T,E)=∏_{E(ρ)=0}L_T(ρ).SinceE
  is nonzero on D its roots ρ∉D⊇T, so L_T(ρ)≠0 and Res(L_T,E)≠0 for every valid
co-support. Two consequences:

  - Δ=0 ⟺ [I_S]_E ∧ [Bnum]_E = 0 ⟺ landing. The resultant factor is a
  nonvanishingdecoration,soΔfaithfullydetectslandings(nospuriouszeros,
  no missed ones).

-Δ = Res(L_T,E)·δisanidentityofrationalfunctions(δ=[I_S]_E∧[Bnum]_E
  carries 1/Res because [I_S]_E=A·M_{L_T}^{-1}). It is not a polynomial
  factorization,sothereisno forced common factorsneakinginthroughthe
  resultant. This kills the most natural false-positive for a shared component.

  1. Explicit Δ₀, Δ₁ via the τ₃-quadratic form

  [L_T]_E and [Q_S]_E are affine-linear in τ (coordinates in basis {1,X},
  E=X²+e₁X+e₀):

[L_T]_E:const(e₁e₀,e₁²−e₀);∂τ₁(e₀,e₁);∂τ₂(0,1);∂τ₃(−1,0)

[Q_S]_E:const(W_{n-3}−W_{n-1}e₀,W_{n-2}−W_{n-1}e₁);∂τ₁
  (−W_{n-2},−W_{n-1});  ∂τ₂ (W_{n-1},0);  ∂τ₃ (0,0)

  [W]_E,[L_D]_E,[Bnum]_E∈F[X]/E are τ-independent. Hence A=M_V[L_T]_E−M_λ[Q_S]_E
  andC=M_β[L_T]_Eareaffine-linearinτ,soΔ=A∧Cisagenuinequadric.
  Crucially τ₃ enters only through the constant [L_T]_E-vector (−1,0), i.e.
through a⁽³⁾=−[W]_E, c⁽³⁾=−[Bnum]_E (the quotient Q_S is τ₃-free).So

Δ=κ·τ₃²+L(τ₁,τ₂)·τ₃+Q(τ₁,τ₂),κ=[W]_E∧[Bnum]_E∈F,

  with L affine-linear and Q a quadric in (τ₁,τ₂), both F-valued. The τ₃²
  coefficientκreproducesthebankedCycle-12valueexactly—myconsistency
  anchor. Representative mixed coefficient (hand-derived):

[τ₂τ₃]Δ=−[W]_E∧[X·Bnum]_E−[X·W]_E∧[Bnum]_E+W_{n-1}·[L_D]_E∧[Bnum]_E.

  Splitting each F-coefficient c=c₀+αc₁ over the B-basis {1,α} (legitimate
  becauseτ_i∈B):

Δ₀=κ₀τ₃²+L₀τ₃+Q₀,Δ₁=κ₁τ₃²+L₁τ₃+Q₁,κ₀,κ₁∈B,L_i,Q_i∈B[τ₁,τ₂].

  coeff_component_rank=2 (Codex) ⟺ Δ₁≢0 and Δ₁∝̸Δ₀: genuinely two base quadrics,
  asthecrackpredicted.

  2. Common factor ⟺ a classified resonance; generic coprimality

  A common nonconstant factor g∈\bar B[τ] of Δ₀,Δ₁ is linear or quadratic, and:

  - g divides both ⟹ g∣Δ=Δ₀+αΔ₁ over \bar F, with g defined over \bar B.

-Converselysucha\bar B-factorofΔproducesacommonfactorofΔ₀,Δ₁.

  So shared component ⟺ either (a) Δ is an F*-multiple of a quadric defined over
  \bar B, or (b) Δ has a linear factor defined over \bar B.

  Now use the τ₃-degree. Assume κ≠0 with both κ₀,κ₁≠0 (the generic leading
  configuration).Form

Φ:=κ₁Δ₀−κ₀Δ₁=(κ₁L₀−κ₀L₁)τ₃+(κ₁Q₀−κ₀Q₁),

  which has τ₃-degree ≤ 1 (the τ₃² terms cancel by construction).

  - Quadratic common factor (case a): then Δ₀,Δ₁∝g over \bar B, so Φ∝g too; but
  g∝Δ₀hasτ₃-degree2whileΦhasτ₃-degree≤1—impossibleunlessΦ≡0,i.e.
  κ₁Δ₀≡κ₀Δ₁, i.e. Δ₀,Δ₁ are B-proportional, i.e. Δ∈F*·B[τ]. That is exactly
stratum (a), and it forces a testable alignment: every coefficientratio
[τ_iτ_j]Δ / κ ∈ \bar B. E.g. ([τ₂τ₃]Δ)/([W]_E∧[Bnum]_E)∈BisoneF-into-B

condition(codimension≥1onsourcedata).Generic(W,E,Bnum)violateit.

-Linearcommonfactor(caseb):Δreduciblewitha\bar B-descendedfactor—
  the rank-≤2 condition on the 4×4 symmetric matrix of the projective quadric,
  plusadescentcondition.ProperZariski-closed.

  Therefore, outside the union of

  - R0 = {κ = [W]_E∧[Bnum]_E = 0} (the global/tangent endpoint already named in
  Cycles11–12),

-Ra = {Δ ∈ F*·\bar B[τ]}(full-coefficientF/Balignment),and

-Rb = {Δ reducible with a \bar B linear factor},

-R0 = {κ = [W]_E∧[Bnum]_E = 0}(theglobal/tangentendpointalreadynamedin
Cycles 11–12),
- Ra = {Δ ∈ F*·\bar B[τ]}(full-coefficientF/Balignment),and
breducilewith a \bar B linear factor},

Δ₀andΔ₁haveno common linear or quadratic factor.Thisprovestaskitem2
  in the conditional form the prompt allows ("outside classified strata"), and
  thestrataareexactlylow-degreeresonancescutoutbyexplicitinvariants.

  3. Finite-field point count off the strata

  With no common factor, V(Δ₀,Δ₁)⊂A³ is a complete intersection: by Krull's
  principal-idealtheoremeverycomponenthascodimension≤2(dim≥1),anddim
  ≤1 since a 2-dimensional component would be common to V(Δ₀) and V(Δ₁), i.e. a
common factor. So V is pure dimension ≤1. By Bézout in P³, twoquadric
surfaces with no common component meetinacurveofdegree≤4,so

#{τ∈B³:Δ(τ)=0}=#V(Δ₀,Δ₁)(F_p)≤4p+O(1)=O(p).

  Since each landing co-support T is a B-triple with Δ(τ)=0, and the slope z is
  uniqueperT(bankedCycle2,[Bnum]_E≠0),droppingthe"distinct-roots/
  D-split cubic" constraint over-counts upward:

C2≤#landings≤#{τ∈B³:Δ(τ)=0}=O(p)=O(n)(offR0∪Ra∪Rb).

  This recovers C2=O(n) without any fixed-slope fiber theorem, matching
  zeros_all_B3=O(p)anddominatingtheobservedmax_C2=5.

4. The shared-component strata: what they actually are

  Refuting the optimistic reading, the coprimality is not unconditional — Ra and
  Rbarerealandarepreciselythecandidate-counterpacketloci:

  - R0 (κ=0): [W]_E∥[Bnum]_E. This is the tangent/global endpoint; a ROUTE_CUT
  already coveredbythetangent/globalseparation.Notnew.

-Ra (Δ₁≡cΔ₀, single B-quadric)andRb (\bar B-linear factor):hereV(Δ₀,Δ₁)
  acquires a 2-dimensional B-component, so up to Θ(p²) split cubics can land and
  thebase-componentmethodgoessilent.Thesearenotautomaticallyharmless
  and not the tangent cut; they are a genuine new common-factor/resonance
invariant that only the fixed-slope fiber-collapse theorem (theP1wall)can
resolve. They are also thin (proper algebraicstratainsource-dataspace)and

sitatσ=2,i.e.sub-reserve—sotheycannotbepromotedtoa

corrected-reservecounterpackethere.

  So this run does not produce a counterpacket; it isolates the exact locus
  whereonewouldhavetolive.

Final classification

  BANKABLE_LEMMA (conditional / generic), with a sharpened EXACT_NEW_WALL
  attached—samepostureasCycles9and12.

  Bankable content (ledgers separate, q_gen=p, q_line=p², q_chal unused;
  sub-reserveatσ=2;noconj:B,noprotocol/MCA/CA/list-/line-decoding,no
  q_gen collapse):

  1. Faithfulness: Δ=Res(L_T,E)·([I_S]_E∧[Bnum]_E) with Res(L_T,E)≠0 on all
  validco-supports,soΔdetectslandingsexactlyandcarriesnoforced
  resultant factor.

2.Δ=κτ₃²+L(τ₁,τ₂)τ₃+Q(τ₁,τ₂),κ=[W]_E∧[Bnum]_E;Δ₀,Δ₁∈B[τ]aretwoquadrics,
  generically rank 2 (Δ₁≢0, Δ₁∝̸Δ₀).

3.OffthestrataR0∪Ra∪Rb,Δ₀,Δ₁arecoprime(τ₃-degreeargumenton
  Φ=κ₁Δ₀−κ₀Δ₁), hence V(Δ₀,Δ₁) is a curve of degree ≤4 and C2 ≤ #landings =
  O(p)=O(n).

  Residual wall left open (do not bank as resolved):

W-F1-AA-RES-T2J3-BASE-COMPONENT-RESONANCE:

onRa={Δ∈F*·\barB[τ]}andRb={Δhasa\barB-linearfactor},thebase

quadricsshareasurfacecomponent;boundorrefutetheslopecountthere

(thisisexactlywherefixed-slopefiber-collapse,
  W-F1-AA-RES-T2J3-FIBER-COLLAPSE,

isstillrequired).

  Caveat on rigor: the coefficient formulas (κ, [τ₂τ₃]Δ, the a⁽ⁱ⁾/c⁽ʲ⁾ tables)
  arehand-derivedbecausecodeexecutionwasunavailableinthisharness;they
  are consistent with the independently banked [τ₃²]Δ=wedge([W]_E,[Bnum]_E) and
with the Codex rank=2/O(p) scan, but a fresh symbolic recomputationofallsix
quadratic coefficients and an explicitdefining-idealcheckofRa/Rbisthe

naturalverificationstepbeforethisleavesAUDITstatus.
