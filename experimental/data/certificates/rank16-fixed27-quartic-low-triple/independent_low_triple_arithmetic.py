#!/usr/bin/env python3
from math import ceil
B=32768
d=63601
w=28897
BASE_CAP=12997
DEFICIT=7319

def ceil_div(a,b): return -((-a)//b)
def q5(T):
    q,s=divmod(T,5)
    return s*(q+1)*q+(5-s)*q*(q-1)

states=feasible=interval_infeasible=capacity_infeasible=0
best=None
records=[]
for c in range(BASE_CAP+1):
    r=d-c; lam=w-c
    M=1
    while M<=8192:
        if r%M==0:
            states += 1
            lower=5*lam-DEFICIT
            nmin=M*ceil_div(lower,M)
            L0=lam//M
            T=nmin//M
            # necessary actual constraints: n3<=2r and sum of 5 cells <=5*M*L0
            if nmin>2*r:
                interval_infeasible+=1
            elif T>5*L0:
                capacity_infeasible+=1
            else:
                feasible+=1
                b=B//M
                Q=q5(T)
                cap=(b-1)*(2*L0-2)
                gap=Q-cap
                row=(gap,c,lam,r,M,b,nmin,T,L0,Q,cap)
                if best is None or row<best: best=row
        M*=2
print('states',states,'feasible',feasible,'interval_infeasible',interval_infeasible,'capacity_infeasible',capacity_infeasible)
print('best',best)
assert (states,feasible,interval_infeasible,capacity_infeasible)==(25996,19346,6647,3)
assert best==(28,12401,16496,51200,2048,16,75776,37,8,238,210)
# one more deficit (7320, assumption n3 >= 5lam-7320)
D2=7320
states2=feasible2=interval2=capinf2=0; best2=None
for c in range(BASE_CAP+1):
    r=d-c; lam=w-c
    M=1
    while M<=8192:
        if r%M==0:
            states2+=1
            nmin=M*ceil_div(5*lam-D2,M)
            L0=lam//M; T=nmin//M
            if nmin>2*r: interval2+=1
            elif T>5*L0: capinf2+=1
            else:
                feasible2+=1
                b=B//M; Q=q5(T); cap=(b-1)*(2*L0-2); gap=Q-cap
                row=(gap,c,lam,r,M,b,nmin,T,L0,Q,cap)
                if best2 is None or row<best2: best2=row
        M*=2
print('sharp states',states2,'feasible',feasible2,'interval_infeasible',interval2,'capacity_infeasible',capinf2)
print('sharp best',best2)
assert (states2,feasible2,interval2,capinf2)==(25996,19350,6643,3)
assert best2==(-6766,12997,15900,50604,1,32768,72180,72180,15900,1041918300,1041925066)
print('union', (7*d-5*w+7320)//2)
assert (7*d-5*w+7320)%2==0
assert (7*d-5*w+7320)//2==154021
