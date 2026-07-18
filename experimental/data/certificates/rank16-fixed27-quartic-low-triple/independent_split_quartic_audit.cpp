#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <numeric>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using u32 = uint32_t;
using u64 = uint64_t;
using u128 = __uint128_t;
static constexpr u64 P = 2130706433ULL;
static constexpr u64 OMEGA = 1548376985ULL;

static inline u32 addm(u32 a, u32 b){ u64 s=(u64)a+b; if(s>=P) s-=P; return (u32)s; }
static inline u32 subm(u32 a, u32 b){ return a>=b ? a-b : (u32)((u64)a+P-b); }
static inline u32 mulm(u32 a, u32 b){ return (u32)(((u128)a*b)%P); }
static u32 powm(u32 a, u64 e){ u32 r=1; while(e){ if(e&1) r=mulm(r,a); a=mulm(a,a); e>>=1;} return r; }
static u64 rot64(u64 x, unsigned s){ s&=63; if(!s) return x; return (x<<s)|(x>>(64-s)); }

struct Arr3Hash { size_t operator()(std::array<u64,3> const& a) const noexcept {
    u64 h=1469598103934665603ULL; for(u64 x:a){ h^=x; h*=1099511628211ULL; h^=x>>32; h*=1099511628211ULL;} return (size_t)h;
}};
struct Arr6Hash { size_t operator()(std::array<u32,6> const& a) const noexcept {
    u64 h=1469598103934665603ULL; for(u32 x:a){ h^=x; h*=1099511628211ULL;} return (size_t)h;
}};

struct Cubic { u64 mask; std::array<u32,3> v; }; // coefficients x^2,x,1 (monic x^3)
struct DirRec { u32 k1,k2,id; uint8_t pivot; };
static bool dirless(DirRec const&a, DirRec const&b){
    if(a.pivot!=b.pivot) return a.pivot<b.pivot;
    if(a.k1!=b.k1) return a.k1<b.k1;
    if(a.k2!=b.k2) return a.k2<b.k2;
    return a.id<b.id;
}
static bool samekey(DirRec const&a, DirRec const&b){return a.pivot==b.pivot&&a.k1==b.k1&&a.k2==b.k2;}

struct Edge { std::array<u32,3> q; uint8_t common; };
static inline u64 pairkey(u32 a,u32 b){ if(a>b) std::swap(a,b); return ((u64)a<<32)|b; }

static std::array<u64,3> canon_triple(std::array<u64,3> a){
    std::array<u64,3> best{}; bool init=false;
    for(unsigned t=0;t<64;t++){
        std::array<u64,3> b={rot64(a[0],t),rot64(a[1],t),rot64(a[2],t)};
        std::sort(b.begin(),b.end());
        if(!init||b<best){best=b;init=true;}
    }
    return best;
}

int main(){
    // field/order checks
    if(powm((u32)OMEGA,64)!=1 || powm((u32)OMEGA,32)==1){ std::cerr<<"omega order fail\n"; return 2; }
    std::array<u32,64> root{}; root[0]=1; for(int i=1;i<64;i++) root[i]=mulm(root[i-1],(u32)OMEGA);
    {
        auto s=root; std::sort(s.begin(),s.end()); if(std::unique(s.begin(),s.end())!=s.end()){std::cerr<<"duplicate roots\n";return 2;}
    }

    std::vector<Cubic> cubics; cubics.reserve(41664);
    std::unordered_map<u64,u32> cubic_id; cubic_id.reserve(50000);
    for(int i=0;i<64;i++) for(int j=i+1;j<64;j++) for(int k=j+1;k<64;k++){
        u32 r1=root[i],r2=root[j],r3=root[k];
        u32 s1=addm(addm(r1,r2),r3);
        u32 s2=addm(addm(mulm(r1,r2),mulm(r1,r3)),mulm(r2,r3));
        u32 s3=mulm(mulm(r1,r2),r3);
        Cubic c{(1ULL<<i)|(1ULL<<j)|(1ULL<<k), {s1? (u32)(P-s1):0, s2, s3? (u32)(P-s3):0}};
        u32 id=(u32)cubics.size(); cubics.push_back(c); cubic_id[c.mask]=id;
    }
    if(cubics.size()!=41664){std::cerr<<"cubic count fail\n";return 2;}
    std::vector<u32> reps;
    for(u32 id=0;id<cubics.size();id++){
        u64 m=cubics[id].mask,best=m; for(int t=1;t<64;t++) best=std::min(best,rot64(m,t));
        if(m==best) reps.push_back(id);
    }
    std::cout<<"split_cubics="<<cubics.size()<<" translation_orbits="<<reps.size()<<std::endl;

    std::unordered_set<std::array<u64,3>,Arr3Hash> orbit_lines; orbit_lines.reserve(1000);
    std::vector<DirRec> recs; recs.reserve(cubics.size()-1);
    std::vector<u32> denoms; denoms.reserve(cubics.size()-1);
    std::vector<size_t> denom_pos; denom_pos.reserve(cubics.size()-1);
    std::vector<u32> pref, invs;

    for(size_t ai=0;ai<reps.size();ai++){
        u32 aid=reps[ai]; auto const&A=cubics[aid]; recs.clear(); denoms.clear(); denom_pos.clear();
        // First store raw differences in k1/k2 and denominator index encoded via pivot.
        for(u32 id=0;id<cubics.size();id++) if(id!=aid){
            u32 d0=subm(cubics[id].v[0],A.v[0]);
            u32 d1=subm(cubics[id].v[1],A.v[1]);
            u32 d2=subm(cubics[id].v[2],A.v[2]);
            DirRec r{}; r.id=id;
            if(d0){ r.pivot=0; r.k1=d1; r.k2=d2; denoms.push_back(d0); denom_pos.push_back(recs.size()); }
            else if(d1){ r.pivot=1; r.k1=d2; r.k2=0; denoms.push_back(d1); denom_pos.push_back(recs.size()); }
            else { r.pivot=2; r.k1=r.k2=0; }
            recs.push_back(r);
        }
        // batch invert all denominators
        pref.assign(denoms.size()+1,1);
        for(size_t i=0;i<denoms.size();i++) pref[i+1]=mulm(pref[i],denoms[i]);
        invs.resize(denoms.size());
        u32 acc=powm(pref.back(),P-2);
        for(size_t i=denoms.size();i-->0;){ invs[i]=mulm(acc,pref[i]); acc=mulm(acc,denoms[i]); }
        for(size_t di=0;di<denoms.size();di++){
            auto &r=recs[denom_pos[di]]; u32 inv=invs[di];
            if(r.pivot==0){r.k1=mulm(r.k1,inv);r.k2=mulm(r.k2,inv);} else {r.k1=mulm(r.k1,inv);}
        }
        std::sort(recs.begin(),recs.end(),dirless);
        size_t s=0;
        while(s<recs.size()){
            size_t e=s+1; while(e<recs.size()&&samekey(recs[s],recs[e])) e++;
            if(e-s>=2){
                for(size_t x=s;x<e;x++) for(size_t y=x+1;y<e;y++){
                    u64 m0=A.mask,m1=cubics[recs[x].id].mask,m2=cubics[recs[y].id].mask;
                    if((m0&m1)||(m0&m2)||(m1&m2)) continue;
                    orbit_lines.insert(canon_triple({m0,m1,m2}));
                }
            }
            s=e;
        }
    }
    std::cout<<"disjoint_cubic_line_orbits="<<orbit_lines.size()<<std::endl;

    std::unordered_set<std::array<u64,3>,Arr3Hash> actual_set; actual_set.reserve(30000);
    for(auto const&tr:orbit_lines) for(unsigned t=0;t<64;t++){
        std::array<u64,3> a={rot64(tr[0],t),rot64(tr[1],t),rot64(tr[2],t)}; std::sort(a.begin(),a.end()); actual_set.insert(a);
    }
    std::vector<std::array<u64,3>> actual_lines(actual_set.begin(),actual_set.end());
    std::sort(actual_lines.begin(),actual_lines.end());
    std::cout<<"actual_cubic_lines="<<actual_lines.size()<<std::endl;

    // all quartic masks and ids
    std::vector<u64> qmask; qmask.reserve(635376);
    std::unordered_map<u64,u32> qid; qid.reserve(800000);
    for(int i=0;i<64;i++) for(int j=i+1;j<64;j++) for(int k=j+1;k<64;k++) for(int l=k+1;l<64;l++){
        u64 m=(1ULL<<i)|(1ULL<<j)|(1ULL<<k)|(1ULL<<l); u32 id=(u32)qmask.size(); qmask.push_back(m); qid.emplace(m,id);
    }
    std::cout<<"split_quartics="<<qmask.size()<<std::endl;

    std::vector<Edge> edges; edges.reserve(actual_lines.size()*55ULL);
    for(auto const&tr:actual_lines){
        u64 uni=tr[0]|tr[1]|tr[2];
        if(__builtin_popcountll(uni)!=9){std::cerr<<"non-disjoint actual line\n";return 2;}
        for(int y=0;y<64;y++) if(!(uni&(1ULL<<y))){
            std::array<u32,3> q={qid.at(tr[0]|(1ULL<<y)),qid.at(tr[1]|(1ULL<<y)),qid.at(tr[2]|(1ULL<<y))};
            std::sort(q.begin(),q.end()); edges.push_back({q,(uint8_t)y});
        }
    }
    std::cout<<"concurrent_triples="<<edges.size()<<std::endl;

    struct FlatPairMap {
        std::vector<u64> keys; std::vector<u32> vals; u64 mask;
        explicit FlatPairMap(size_t min_capacity){
            size_t cap=1; while(cap<min_capacity*2) cap<<=1;
            keys.assign(cap,std::numeric_limits<u64>::max()); vals.resize(cap); mask=cap-1;
        }
        static u64 mix(u64 x){
            x += 0x9e3779b97f4a7c15ULL;
            x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
            x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
            return x ^ (x >> 31);
        }
        bool insert(u64 k,u32 v){
            u64 i=mix(k)&mask; while(keys[i]!=std::numeric_limits<u64>::max()){ if(keys[i]==k) return false; i=(i+1)&mask; }
            keys[i]=k; vals[i]=v; return true;
        }
        u32 get(u64 k) const {
            u64 i=mix(k)&mask; while(keys[i]!=std::numeric_limits<u64>::max()){ if(keys[i]==k) return vals[i]; i=(i+1)&mask; }
            return std::numeric_limits<u32>::max();
        }
    };

    std::vector<u32> deg(qmask.size(),0);
    FlatPairMap pairmap(edges.size()*3ULL);
    u64 pair_records=0;
    for(auto const&e:edges){
        auto q=e.q; for(u32 x:q) deg[x]++;
        if(!pairmap.insert(pairkey(q[0],q[1]),q[2]) ||
           !pairmap.insert(pairkey(q[0],q[2]),q[1]) ||
           !pairmap.insert(pairkey(q[1],q[2]),q[0])){
            std::cerr<<"nonlinear concurrent-triple hypergraph\n"; return 2;
        }
        pair_records += 3;
    }
    std::cout<<"pair_records="<<pair_records<<std::endl;
    std::vector<u64> off(qmask.size()+1,0); for(size_t i=0;i<deg.size();i++) off[i+1]=off[i]+deg[i];
    std::vector<u32> inc(off.back()); auto cur=off;
    for(u32 ei=0;ei<edges.size();ei++) for(u32 x:edges[ei].q) inc[cur[x]++]=ei;

    auto partial_target=[&](std::array<u32,5> ids){
        u64 ones=0,twos=0,fours=0;
        for(u32 id:ids){
            u64 x=qmask[id];
            u64 c1=ones&x; ones^=x;
            u64 c2=twos&c1; twos^=c1;
            fours^=c2;
        }
        u64 exact1=ones & ~twos & ~fours;
        u64 exact2=~ones & twos & ~fours;
        u64 exact3=ones & twos & ~fours;
        u64 fourplus=fours;
        return __builtin_popcountll(exact1)==6 && __builtin_popcountll(exact2)==4 &&
               __builtin_popcountll(exact3)==2 && fourplus==0;
    };

    std::unordered_set<std::array<u32,6>,Arr6Hash> pasch; pasch.reserve(20000);
    u64 incident_pairs=0, distinct_common_pairs=0, partial_profile_pairs=0, raw=0,target=0;
    std::unordered_map<u64,u64> profile_hist;
    for(u32 shared=0; shared<qmask.size(); shared++){
        for(u64 ix=off[shared]; ix<off[shared+1]; ix++){
            auto const&e0=edges[inc[ix]];
            u32 ab[2]; int na=0; for(u32 v:e0.q) if(v!=shared) ab[na++]=v; assert(na==2);
            for(u64 jx=ix+1; jx<off[shared+1]; jx++){
                auto const&e1=edges[inc[jx]]; incident_pairs++;
                if(e0.common==e1.common) continue;
                u32 de[2]; int nb=0; bool extra=false;
                for(u32 v:e1.q){ if(v==shared) continue; if(v==ab[0]||v==ab[1]) extra=true; de[nb++]=v; }
                if(extra || nb!=2) continue;
                distinct_common_pairs++;
                bool pp=partial_target({shared,ab[0],ab[1],de[0],de[1]});
                if(pp) partial_profile_pairs++;
                for(int pairing=0;pairing<2;pairing++){
                    u32 b=ab[0],c=ab[1],d=de[pairing],e=de[1-pairing];
                    u32 f1=pairmap.get(pairkey(b,d));
                    if(f1==std::numeric_limits<u32>::max()) continue;
                    u32 f2=pairmap.get(pairkey(c,e));
                    if(f1!=f2) continue;
                    u32 f=f1;
                    if(f==shared||f==b||f==c||f==d||f==e) continue;
                    raw++;
                    std::array<u32,6> six={shared,b,c,d,e,f}; std::sort(six.begin(),six.end());
                    pasch.insert(six);
                }
            }
        }
    }
    for(auto const&six:pasch){
        std::array<uint8_t,64> mult{};
        for(u32 id:six){u64 m=qmask[id]; while(m){unsigned bit=__builtin_ctzll(m);mult[bit]++;m&=m-1;}}
        int n1=0,n2=0,n3=0,n4p=0;
        for(auto x:mult){if(x==1)n1++;else if(x==2)n2++;else if(x==3)n3++;else if(x>=4)n4p++;}
        u64 key=((u64)n1<<48)|((u64)n2<<32)|((u64)n3<<16)|(u64)n4p; profile_hist[key]++;
        if(n1==6&&n2==3&&n3==4&&n4p==0) target++;
    }
    std::vector<std::pair<std::array<int,4>,u64>> hist;
    for(auto const&kv:profile_hist){
        u64 k=kv.first; hist.push_back({{(int)(k>>48),(int)((k>>32)&0xffff),(int)((k>>16)&0xffff),(int)(k&0xffff)},kv.second});
    }
    std::sort(hist.begin(),hist.end());
    std::cout<<"incident_edge_pairs="<<incident_pairs<<" distinct_common_pairs="<<distinct_common_pairs
             <<" partial_target_pairs="<<partial_profile_pairs<<std::endl;
    std::cout<<"pasch_unique="<<pasch.size()<<" raw_paths="<<raw<<" target_profiles="<<target<<std::endl;
    for(auto const&h:hist) std::cout<<"profile="<<h.first[0]<<","<<h.first[1]<<","<<h.first[2]<<","<<h.first[3]<<" count="<<h.second<<std::endl;
    if(reps.size()!=651 || orbit_lines.size()!=364 || actual_lines.size()!=23296 || qmask.size()!=635376 ||
       edges.size()!=1281280 || pair_records!=3843840 || pasch.size()!=11328 || raw!=67968 || target!=0){
        std::cerr<<"count mismatch\n"; return 3;
    }
    return 0;
}
