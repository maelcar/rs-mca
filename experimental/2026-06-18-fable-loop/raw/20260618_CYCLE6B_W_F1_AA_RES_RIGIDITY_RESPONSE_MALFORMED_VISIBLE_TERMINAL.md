Ihave enough from the source and audit chain to classify. Key checks:
def:residue gives the slope condition [I_S]_E = z[Bnum]_E in F[X]/(E); the
banked Cycle 1 / Codex-local audits already contain the paired-readout
reduction; Cycle 3 isolates the agreement gap; Cycle 5 / ACTIVE_WALLS name the
missing invariant as a rigidity/value-count law analogous to thm:rigidcyclo /
thm:exactcount.

  ⏵⏵ don't ask on (shift+tb to cycle)

  Final classification: EXACT_NEW_WALL

  Object:

RestrictedW-F1-AA-RESrigidityhalf:same-slopekernelpluspairedbase
  readout.

  Verdict:

Bothpartsarecorrectandsource-valid,butneitherisanewadvance.

PartBisthealready-bankedCycle1/Codexpaired-readoutreductionverbatim.

PartAisaone-linecorollaryofbankedslope-uniquenessplusadegreecount.

Togethertheyrestatetheresidueequationasakernelandabase
  factorization.

Theydonotcountslopesorcontrolagreement,sotherigiditywallstands.

  Proof or cut:

  1. def:residue slope cond is [I_S]_E = z[Bnum]_E in F[X]/(E), z in F.

2.Bnum!=0,degBnum<t=degE,so[Bnum]_E!=0(noE-multiplehas
  deg<t).

3.Nonzeroz-z'inFisaunitinF[X]/(E);soz(S)isunique(banked
  Cycle 2).

4.Hencez(S)=z(S')iff[I_S]_E=[I_S']_EiffE|(I_S-I_S')inF[X].

5.degI_S,I_S'<a=k+tanddegE=t,sothequotienthasdegree<k.

6.ThusE|(I_S-I_S')iffI_S-I_S'inE*F_{<k}[X].PartAholds(withE,over
  F).

7.DsubsetBgivesB-valuedLagrangeweights:I_S=interp_S(w0)+alpha
  interp_S(w1).

8.Ehat=lcm(E,E^tau)inB[X],E|Ehat,so[I_S]_EisreadfromI_SmodEhat.

9.So[I_S]_Eisdeterminedbyrho(S)in(B[X]/Ehat)^2.PartBholds(banked).

10.Nofalsestep:notROUTE_CUT.Hypothesesareprecise:notimprecise.

11.ButPartAisonlythekerneloftheslopemap;itsayswhenslopes
  coincide.

12.Itdoesnotboundthenumberofdistinctcosets(slopes)onthebadline.

13.PartBfactorsresiduethroughbasedata;Cycle1warnsthisisnota
  count:

14.hugerho-fiberscancarryfewslopes,low-degreewimakeI_S
  S-independent.

15.Neitherpartseesagreementnu(S)=|{x:I_S(x)=w(x)}|>=s_delta(Cycle 3).

16.Sotheclaimed"rigidityhalf"isarestatementstoppingatthewall.

17.Thesharpermissinginvariantisnamedbelow;classificationis
  EXACT_NEW_WALL.

7. DsubsetBgivesB-valuedLagrangeweights:I_S=interp_S(w0)+alpha
interp_S(w1).
8. Ehat=lcm(E,E^tau)inB[X],E|Ehat,so[I_S]_EisreadfromI_SmodEhat.
9So [I_S]_ is determined by rho(S) in (BX]/Ehat)^2. Part B holds (banked).
10. No false step: not ROUTE_CUT. Hypotheses are precise: not imprecise.
1But PartA is olythe kernelof the lope ma; it says when slopes
coincide.
12. It doesnotboundthenumberofdistinctcosets(slopes)onthebadline.
3Part B facors residue through base data; Cycle1 warn this isnota
count:
14. hugerho-fiberscancarryfewslopes,low-degreewimakeI_S
S-indepndent.
15. Nither partseesagreementnu(S)=|{x:I_S(x)=w(x)}|>=s_delta(Cycle 3).
6So  climed "rigidity half" is a restatement stopping at thewall.
7The sharper missin invarint is nmed below; classifcation is
EXAC_NEW_WALL.

Fieldledger:

q_gen=p:baseB;rho(S)andinterp_S(w0),interp_S(w1)liveinB[X]/Ehat.

q_line=p^2:slopeszandbadlineF*[Bnum]E live in F = F{p^2}.

KernelE*F_{<k}[X]isoverF(I_SinF[X]);readoutdescendstoBviaEhat.

q_chal:unused;noprotocoldenominatorsavingclaimed.

Noconj:B,prob:perfiber,line/listdecoding,orass:extension-mca-liftclaim.

sigma=1counterpacketnotused;thestatementisareserve-agnostic
  restatement.

  What to bank:

Donotbankastherigidityhalf;itiskernel+bankedreductiononly.

Missinginvariant(nameit):aslopevalue-count/collision-rigiditylaw

boundingdistinctz(S)inFovera-subsetsthatareon-line,noncontained,

andhigh-agreement(nu(S)>=s_delta),viarhoonF*[Bnum]_E,reserve
  eta=sigma/n,

withaq_gen-vs-q_lineledger.ThisistheAAanalogueofthm:rigidcyclo+

thm:exactcount:counttheimageontheagreementlocus,notthekernel.
