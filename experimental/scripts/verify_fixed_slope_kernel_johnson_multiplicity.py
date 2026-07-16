#!/usr/bin/env python3
"""Verify the fixed-slope kernel/Johnson multiplicity compiler."""
from __future__ import annotations
import argparse, copy, hashlib, itertools, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

SCHEMA="rs-mca-fixed-slope-kernel-johnson-multiplicity-v1"
THEOREM_ID="fixed-slope-kernel-johnson-multiplicity"
STATUS="PROVED COMBINATORIAL COMPILER / EXPERIMENTAL CERTIFICATE"
REPO=Path(__file__).resolve().parents[2]
SOURCE_NOTE=REPO/"experimental/notes/thresholds/a6_all_witness_line_section_compiler.md"
CERTIFICATE=REPO/"experimental/data/certificates/fixed-slope-kernel-johnson-multiplicity/fixed_slope_kernel_johnson_multiplicity.json"
SOURCE_MARKERS=(
    "|Z| <= 1165 + 3744 D_r^6,",
    "D_r=floor((489950r-1372)/350)+1.                       (1a)",
    "|Z_a(r)| <= 3744D_r^6+47700r+688",
    "(gamma,S,h) -> (gamma,h) -> gamma.",
    "- a multiplicity bound for witnesses sharing one slope;",
)
class VerificationError(RuntimeError): pass
def require(c:bool,m:str)->None:
    if not c: raise VerificationError(m)
def canonical_bytes(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()
def payload_sha256(v:dict[str,Any])->str:
    u=copy.deepcopy(v);u.pop("payload_sha256",None);return hashlib.sha256(canonical_bytes(u)).hexdigest()
def file_sha256(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def source_binding()->dict[str,Any]:
    text=SOURCE_NOTE.read_text(); lines=text.splitlines(); pins=[]
    for marker in SOURCE_MARKERS:
        matches=[(i,line) for i,line in enumerate(lines,1) if marker in line]
        require(len(matches)==1,f"source marker is not unique: {marker}")
        i,line=matches[0];pins.append({"line":i,"marker":marker,"line_sha256":hashlib.sha256(line.encode()).hexdigest()})
    return {"path":str(SOURCE_NOTE.relative_to(REPO)),"sha256":file_sha256(SOURCE_NOTE),"pins":pins}

# Sparse polynomials in variables (R,kappa,t,M), for exact symbolic checks.
Poly=dict[tuple[int,int,int,int],int]
def pc(v:int)->Poly:return {} if v==0 else {(0,0,0,0):v}
def pv(i:int)->Poly:
    e=[0,0,0,0];e[i]=1;return {tuple(e):1}
def pa(a:Poly,b:Poly)->Poly:
    z=dict(a)
    for m,c in b.items():z[m]=z.get(m,0)+c
    return {m:c for m,c in z.items() if c}
def pn(a:Poly)->Poly:return {m:-c for m,c in a.items()}
def ps(a:Poly,b:Poly)->Poly:return pa(a,pn(b))
def pm(a:Poly,b:Poly)->Poly:
    z:Poly={}
    for x,c in a.items():
        for y,d in b.items():
            m=tuple(x[i]+y[i] for i in range(4));z[m]=z.get(m,0)+c*d
    return {m:c for m,c in z.items() if c}
def pp(a:Poly,e:int)->Poly:
    require(e>=0,"negative exponent");z=pc(1);b=dict(a)
    while e:
        if e&1:z=pm(z,b)
        b=pm(b,b);e//=2
    return z
def terms(p:Poly)->list[dict[str,Any]]:
    names=("R","kappa","t","M");return [{"coefficient":c,"powers":{names[i]:e for i,e in enumerate(m) if e}} for m,c in sorted(p.items(),reverse=True)]
def symbolic()->dict[str,Any]:
    R,K,T,M=pv(0),pv(1),pv(2),pv(3);one=pc(1);N=pa(R,K);a=ps(N,T);b=ps(K,one);J=ps(pp(a,2),pm(N,b));num=pm(N,ps(pa(R,one),T))
    require(ps(a,b)==ps(pa(R,one),T),"a-(kappa-1) identity")
    lhs=ps(pa(pm(N,a),pm(pm(N,ps(M,one)),b)),pm(M,pp(a,2)))
    rhs=ps(num,pm(M,J));require(lhs==rhs,"degree-square compiler identity")
    expected={(2,0,0,0):1,(1,1,0,0):1,(1,0,1,0):-2,(1,0,0,0):1,(0,1,1,0):-2,(0,1,0,0):1,(0,0,2,0):1}
    require(J==expected,"J expansion")
    return {"variables":["R","kappa","t","M"],"definitions":{"N":"R+kappa","a":"N-t","J_K":"a^2-N(kappa-1)","numerator":"N(R+1-t)"},"identities":["a-(kappa-1)=R+1-t","N*a+N*(M-1)*(kappa-1)-M*a^2=N*(R+1-t)-M*J_K"],"J_K_expansion":terms(J),"numerator_expansion":terms(num),"compiled_slack_expansion":terms(rhs)}

def params(N:int,R:int,K:int,t:int)->dict[str,int]:
    require(N==R+K,"N != R+kappa");require(0<=t<R,"0<=t<R failed");a=N-t;J=a*a-N*(K-1);num=N*(R+1-t);require(J>0,"J_K<=0")
    return {"N":N,"R":R,"kappa":K,"t":t,"a":a,"J_K":J,"numerator":num,"cap":num//J,"remainder":num%J}
def a6row(r:int)->dict[str,Any]:
    require(r>=1,"r<1");row=params(500*r,275*r,225*r,150*r);J=500*r*(20*r+1);num=500*r*(125*r+1)
    require(row["J_K"]==J and row["numerator"]==num,"A6 identities");require(row["cap"]==6,"A6 cap")
    require(num-6*J==2500*r*(r-1),"A6 lower floor");require(7*J-num==500*r*(15*r+6),"A6 upper floor")
    D=((489950*r-1372)//350)+1;slope=1165+3744*D**6;pair=6*slope;require(pair==6990+22464*D**6,"composition")
    global_slope=3744*D**6+47700*r+688;global_pair=6*global_slope
    require(global_pair==22464*D**6+286200*r+4128,"global composition")
    return {"r":r,**row,"D_r":D,"source_distinct_slope_bound":slope,"distinct_gamma_error_pair_bound":pair,"composed_formula_value":6990+22464*D**6,"source_global_distinct_slope_bound":global_slope,"global_distinct_gamma_error_pair_bound":global_pair,"global_composed_formula_value":22464*D**6+286200*r+4128}
def a6ledger()->dict[str,Any]:
    return {"parameters":"N=500r,R=275r,kappa=225r,t=150r,a=350r","J_K_identity":"500r(20r+1)","numerator_identity":"500r(125r+1)","floor_proof":{"numerator_minus_6J":"2500r(r-1)>=0 for r>=1","7J_minus_numerator":"500r(15r+6)>0 for r>=1","exact_cap":6},"source_distinct_slope_bound":"1165+3744*D_r^6","D_r":"floor((489950r-1372)/350)+1","composition":"6*(1165+3744*D_r^6)=6990+22464*D_r^6","composed_distinct_gamma_error_pair_bound":"6990+22464*D_r^6","source_global_distinct_slope_bound":"3744D_r^6+47700r+688","global_composition":"6*(3744D_r^6+47700r+688)=22464D_r^6+286200r+4128","global_composed_distinct_gamma_error_pair_bound":"22464D_r^6+286200r+4128","sample_rows":[a6row(r) for r in (1,2,3,7,64)]}

def detmod(A:list[list[int]],p:int)->int:
    require(len(A)==len(A[0]),"nonsquare minor");A=[[x%p for x in r] for r in A];d=1;n=len(A)
    for c in range(n):
        q=next((i for i in range(c,n) if A[i][c]),None)
        if q is None:return 0
        if q!=c:A[q],A[c]=A[c],A[q];d=-d
        v=A[c][c]%p;d=d*v%p;iv=pow(v,-1,p)
        for i in range(c+1,n):
            f=A[i][c]*iv%p
            if f:A[i]=[(A[i][j]-f*A[c][j])%p for j in range(n)]
    return d%p
def mv(A:list[list[int]],v:tuple[int,...],p:int)->tuple[int,...]:return tuple(sum(r[i]*v[i] for i in range(len(v)))%p for r in A)
def grs(points:tuple[int,...],weights:tuple[int,...],R:int,p:int)->list[list[int]]:
    require(len(points)==len(weights),"point/weight mismatch");require(len({x%p for x in points})==len(points),"points repeat");require(all(w%p for w in weights),"zero weight")
    return [[weights[i]*pow(points[i],d,p)%p for i in range(len(points))] for d in range(R)]
def nullbasis(A:list[list[int]],p:int)->list[tuple[int,...]]:
    m=len(A);n=len(A[0]);B=[[x%p for x in r] for r in A];piv=[];row=0
    for c in range(n):
        q=next((i for i in range(row,m) if B[i][c]),None)
        if q is None:continue
        B[row],B[q]=B[q],B[row];iv=pow(B[row][c],-1,p);B[row]=[x*iv%p for x in B[row]]
        for i in range(m):
            if i!=row and B[i][c]:
                f=B[i][c];B[i]=[(B[i][j]-f*B[row][j])%p for j in range(n)]
        piv.append(c);row+=1
        if row==m:break
    free=[c for c in range(n) if c not in piv];out=[]
    for f in free:
        v=[0]*n;v[f]=1
        for i,c in enumerate(piv):v[c]=-B[i][f]%p
        out.append(tuple(v))
    return out
def wt(v:Iterable[int])->int:return sum(x!=0 for x in v)
def kernelcheck(A:list[list[int]],p:int,K:int)->dict[str,int]:
    basis=nullbasis(A,p);require(len(basis)==K,"kernel dimension")
    for v in basis:require(mv(A,v,p)==(0,)*len(A),"bad null basis")
    minimum=None;nonzero=0
    for co in itertools.product(range(p),repeat=K):
        v=tuple(sum(co[i]*basis[i][j] for i in range(K))%p for j in range(len(A[0])))
        if any(v):nonzero+=1;minimum=wt(v) if minimum is None else min(minimum,wt(v))
    require(nonzero==p**K-1 and minimum is not None,"kernel census")
    return {"dimension":K,"vectors_checked":p**K,"nonzero_vectors_checked":nonzero,"minimum_distance":minimum}
def errors(p:int,N:int,t:int)->Iterable[tuple[int,...]]:
    yield (0,)*N
    for w in range(1,t+1):
        for S in itertools.combinations(range(N),w):
            for vals in itertools.product(range(1,p),repeat=w):
                v=[0]*N
                for i,x in zip(S,vals):v[i]=x
                yield tuple(v)
def zeroset(e:tuple[int,...],a:int)->tuple[int,...]:
    z=tuple(i for i,x in enumerate(e) if x==0);require(len(z)>=a,"too few zeros");return z[:a]

def setfixture(name:str,N:int,K:int,t:int,blocks:list[tuple[int,...]],kind:str)->dict[str,Any]:
    P=params(N,N-K,K,t);a=P["a"];B=[tuple(sorted(x)) for x in blocks];require(len(set(B))==len(B),f"{name}: duplicate");require(all(len(x)==a and len(set(x))==a for x in B),f"{name}: size");require(all(0<=y<N for x in B for y in x),f"{name}: range")
    hist=Counter();mx=0
    for x,y in itertools.combinations(B,2):
        q=len(set(x)&set(y));hist[q]+=1;mx=max(mx,q);require(q<=K-1,f"{name}: intersection")
    deg=[sum(i in x for x in B) for i in range(N)];M=len(B);s=sum(deg);ss=sum(x*x for x in deg)
    require(s==M*a,f"{name}: degree sum");require(N*ss>=s*s,f"{name}: Cauchy");require(ss<=M*a+M*(M-1)*(K-1),f"{name}: pair bound");require(M*P["J_K"]<=P["numerator"] and M<=P["cap"],f"{name}: compiler")
    return {"name":name,"kind":kind,"parameters":P,"blocks":[list(x) for x in B],"multiplicity":M,"cap_gap":P["cap"]-M,"maximum_pair_intersection":mx,"intersection_histogram":{str(k):v for k,v in sorted(hist.items())},"degrees":deg,"degree_sum":s,"degree_square_sum":ss,"cauchy_cross_product":{"left_N_sum_d2":N*ss,"right_sum_d_squared":s*s}}
def fixtures()->list[dict[str,Any]]:
    fano=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    rows=[setfixture("F5_same_slope_zero_sets_sharp",5,2,2,[(0,3,4),(0,1,2)],"sharp"),setfixture("Fano_plane_sharp",7,2,4,fano,"sharp_degree_square_equality"),setfixture("Fano_plane_one_block_removed_near_sharp",7,2,4,fano[:-1],"near_sharp_cap_minus_one")]
    require(rows[0]["multiplicity"]==rows[0]["parameters"]["cap"]==2,"F5 sharpness");require(rows[1]["multiplicity"]==rows[1]["parameters"]["cap"]==7,"Fano sharpness");require(rows[2]["cap_gap"]==1,"near sharpness");return rows

def syndrome_case(c:dict[str,Any])->dict[str,Any]:
    p=int(c["p"]);points=tuple(c["points"]);weights=tuple(c["weights"]);R=int(c["R"]);t=int(c["t"]);N=len(points);K=N-R;P=params(N,R,K,t);H=grs(points,weights,R,p)
    minors=0
    for C in itertools.combinations(range(N),R):
        require(detmod([[H[i][j] for j in C] for i in range(R)],p)!=0,f"{c['name']}: minor");minors+=1
    require(minors==math.comb(N,R),"minor census");kernel=kernelcheck(H,p,K);require(kernel["minimum_distance"]==R+1,f"{c['name']}: distance")
    F:dict[tuple[int,...],list[tuple[int,...]]]=defaultdict(list);checked=0
    for e in errors(p,N,t):F[mv(H,e,p)].append(e);checked+=1
    require(checked==sum(math.comb(N,w)*(p-1)**w for w in range(t+1)),f"{c['name']}: errors")
    hist=Counter();observed=0;sharp=[]
    for syn in sorted(F):
        E=sorted(F[syn]);M=len(E);hist[M]+=1
        if M>observed:observed=M;sharp=[list(syn)]
        elif M==observed:sharp.append(list(syn))
        B=[zeroset(e,P["a"]) for e in E];require(len(set(E))==M,"duplicate error")
        for i,j in itertools.combinations(range(M),2):
            d=tuple((E[i][q]-E[j][q])%p for q in range(N));require(mv(H,d,p)==(0,)*R,"difference outside kernel");require(wt(d)>=R+1,"distance in fiber");require(len(set(B[i])&set(B[j]))<=K-1,"zero intersection")
        deg=[sum(q in b for b in B) for q in range(N)];s=sum(deg);ss=sum(x*x for x in deg)
        require(s==M*P["a"],"fiber degree sum");require(N*ss>=s*s,"fiber Cauchy");require(ss<=M*P["a"]+M*(M-1)*(K-1),"fiber pair bound");require(M*P["J_K"]<=P["numerator"],"fiber compiler")
    require(observed<=P["cap"] and observed==int(c["expected"]),f"{c['name']}: max")
    special=None
    if c["name"]=="F5_unweighted_sharp":
        e=(0,4,3,0,0);f=(0,0,0,3,4);syn=(2,0,1);require(mv(H,e,p)==syn and mv(H,f,p)==syn,"F5 syndrome");require(sorted(F[syn])==sorted([e,f]),"F5 exact fiber")
        special={"syndrome":list(syn),"errors":[list(e),list(f)],"zero_sets":[list(zeroset(e,3)),list(zeroset(f,3))],"attains_cap":True}
    return {"name":c["name"],"field":{"p":p},"points":list(points),"column_weights":list(weights),"parameters":P,"matrix":H,"GRS_MDS":{"minors_checked":minors,**kernel},"low_weight_errors_checked":checked,"syndromes_observed":len(F),"fiber_size_histogram":{str(k):v for k,v in sorted(hist.items())},"observed_maximum_multiplicity":observed,"syndromes_attaining_observed_maximum":sharp,"special_sharp_fixture":special}
def fieldledger()->list[dict[str,Any]]:
    cases=[{"name":"F5_unweighted_sharp","p":5,"points":[0,1,2,3,4],"weights":[1,1,1,1,1],"R":3,"t":2,"expected":2},{"name":"F7_weighted_nontrivial","p":7,"points":[0,1,2,3,4,5],"weights":[1,2,3,4,5,6],"R":3,"t":2,"expected":3},{"name":"F11_weighted_injective_radius","p":11,"points":[0,1,2,3,4,5],"weights":[1,3,4,5,9,10],"R":4,"t":2,"expected":1}]
    return [syndrome_case(c) for c in cases]

def build()->dict[str,Any]:
    out={"schema":SCHEMA,"theorem_id":THEOREM_ID,"status":STATUS,"scope":{"counted_object":"distinct errors/completed codewords h at one fixed syndrome and slope gamma","not_counted":"multiple raw support labels S attached to the same error h","source_projection":"(gamma,S,h)->(gamma,h)->gamma","hypotheses":["N=R+kappa","0<=t<R","K=ker(H) has minimum distance R+1","all counted distinct errors e satisfy H e=y_gamma and wt(e)<=t","J_K=(N-t)^2-N(kappa-1)>0"],"conclusion":"M*J_K<=N(R+1-t), hence M<=floor(N(R+1-t)/J_K)"},"proof_ledger":{"zero_set_selection":"choose one a=N-t subset from the zero set of each distinct error","intersection_bound":"same-syndrome differences lie in K, so pairwise selected intersections are at most kappa-1","degree_identities":["sum_x d_x=M*a","sum_x d_x^2=M*a+2*sum_{i<j}|A_i intersect A_j|","N*sum_x d_x^2>=(M*a)^2","sum_x d_x^2<=M*a+M(M-1)(kappa-1)"],"compiled_inequality":"M*(a^2-N(kappa-1))<=N*(a-kappa+1)=N(R+1-t)","symbolic_checks":symbolic()},"canonical_A6":a6ledger(),"finite_field_exhaustion":fieldledger(),"set_system_fixtures":fixtures(),"source_binding":source_binding(),"nonclaims":["No multiplicity bound for multiple raw support labels sharing one slope and one completed error.","No claim when J_K<=0 or t>=R.","The factor six composes only with the pinned source distinct-slope bound.","No witness-exhaustive atlas, deployed-row crossing, Grand MCA, Grand List, or prize closure."]}
    out["payload_sha256"]=payload_sha256(out);return out

def validate_semantics(x:dict[str,Any])->None:
    require(x.get("schema")==SCHEMA,"schema");require(x.get("theorem_id")==THEOREM_ID,"id");require(x.get("status")==STATUS,"status");require(x.get("payload_sha256")==payload_sha256(x),"hash")
    s=x.get("scope",{});require("distinct errors" in s.get("counted_object",""),"scope");require("raw support labels" in s.get("not_counted",""),"raw scope");require(s.get("source_projection")=="(gamma,S,h)->(gamma,h)->gamma","projection")
    a=x.get("canonical_A6",{});require(a.get("floor_proof",{}).get("exact_cap")==6,"A6 cap");require(a.get("composed_distinct_gamma_error_pair_bound")=="6990+22464*D_r^6","composition");require(a.get("global_composed_distinct_gamma_error_pair_bound")=="22464D_r^6+286200r+4128","global composition")
    rows=x.get("finite_field_exhaustion",[]);require(len(rows)==3,"field rows");f5=next((r for r in rows if r.get("name")=="F5_unweighted_sharp"),None);require(f5 is not None and f5.get("observed_maximum_multiplicity")==2,"F5 row");require(f5.get("special_sharp_fixture",{}).get("attains_cap") is True,"F5 sharp")
    f=x.get("set_system_fixtures",[]);require(len(f)==3,"fixtures");require(f[1].get("cap_gap")==0,"Fano sharp");require(f[2].get("cap_gap")==1,"near sharp")
    b=x.get("source_binding",{});require(b.get("sha256")==file_sha256(SOURCE_NOTE),"source digest");require(len(b.get("pins",[]))==len(SOURCE_MARKERS),"pins");require(len(x.get("nonclaims",[]))>=4,"nonclaims")
def validate(actual:dict[str,Any],expected:dict[str,Any])->None:validate_semantics(actual);require(actual==expected,"deterministic recomputation mismatch")
def rehash(x:dict[str,Any])->None:x["payload_sha256"]=payload_sha256(x)
def tampers(expected:dict[str,Any])->int:
    M=[]
    x=copy.deepcopy(expected);x["canonical_A6"]["floor_proof"]["exact_cap"]=5;rehash(x);M.append(x)
    x=copy.deepcopy(expected);x["canonical_A6"]["parameters"]="N=499r,R=275r,kappa=224r,t=150r,a=349r";rehash(x);M.append(x)
    x=copy.deepcopy(expected);x["canonical_A6"]["composed_distinct_gamma_error_pair_bound"]="1165+3744*D_r^6";rehash(x);M.append(x)
    x=copy.deepcopy(expected);x["canonical_A6"]["global_composed_distinct_gamma_error_pair_bound"]="3744D_r^6+47700r+688";rehash(x);M.append(x)
    x=copy.deepcopy(expected);x["scope"]["not_counted"]="nothing";rehash(x);M.append(x)
    x=copy.deepcopy(expected);next(r for r in x["finite_field_exhaustion"] if r["name"]=="F5_unweighted_sharp")["observed_maximum_multiplicity"]=1;rehash(x);M.append(x)
    x=copy.deepcopy(expected);x["set_system_fixtures"][1]["cap_gap"]=1;rehash(x);M.append(x)
    x=copy.deepcopy(expected);x["set_system_fixtures"][2]["cap_gap"]=0;rehash(x);M.append(x)
    x=copy.deepcopy(expected);x["source_binding"]["sha256"]="0"*64;rehash(x);M.append(x)
    x=copy.deepcopy(expected);x["payload_sha256"]="f"*64;M.append(x)
    rejected=0
    for x in M:
        try:validate(x,expected)
        except VerificationError:rejected+=1
    require(rejected==len(M),"tamper accepted");return rejected
def check(expected:dict[str,Any])->None:
    require(CERTIFICATE.is_file(),f"missing {CERTIFICATE.relative_to(REPO)}")
    try:actual=json.loads(CERTIFICATE.read_text())
    except json.JSONDecodeError as e:raise VerificationError(f"JSON: {e}") from e
    require(isinstance(actual,dict),"root object");validate(actual,expected)
def summary(x:dict[str,Any],tamper:int|None=None)->None:
    print(f"{THEOREM_ID}: PASS");print("A6_cap=6 fixed_composed=6990+22464*D_r^6 global_composed=22464D_r^6+286200r+4128");print("finite_field_maxima="+",".join(f"{r['name']}:{r['observed_maximum_multiplicity']}/{r['parameters']['cap']}" for r in x["finite_field_exhaustion"]));print("set_system_caps=F5:2/2,Fano:7/7,Fano-minus-one:6/7");print(f"payload_sha256={x['payload_sha256']}")
    if tamper is not None:print(f"tamper_mutations_rejected={tamper}")
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group();g.add_argument("--emit",action="store_true",help="emit deterministic JSON to stdout");g.add_argument("--check",action="store_true");g.add_argument("--tamper-selftest",action="store_true");a=p.parse_args();x=build()
    if a.emit:print(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=True));return 0
    if a.tamper_selftest:summary(x,tampers(x));return 0
    check(x);summary(x);return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except (OSError,VerificationError,ValueError) as e:print(f"{THEOREM_ID}: FAIL: {e}",file=sys.stderr);raise SystemExit(1)
