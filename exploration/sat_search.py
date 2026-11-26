from pysat.solvers import Solver
from itertools import combinations
import sys,time
def forbidden(k):
 return {((a+9*b)//2) for a in range(-k,k+1) for b in range(-k+abs(a),k-abs(a)+1) if (a+9*b)%2==0 and a+9*b>0}
templates=['####....','##.#..#.','#.','####.....']
def solve(t,m,k,budget):
 pat=templates[t]; n=len(pat)*m
 R=[x for x in range(n) if pat[x%len(pat)]=='.']
 def v(x,c):return (x*k)+c
 ss=Solver(name='cadical195')
 for x in R:ss.add_clause([v(x,c) for c in range(4,k+1)])
 for c in range(4,k+1):
  diffs={min(d%n,(-d)%n) for d in forbidden(c)}
  for x in R:
   if 0 in diffs:ss.add_clause([-v(x,c)]);continue
   for d in diffs:
    y=(x+d)%n
    if pat[y%len(pat)]=='.':ss.add_clause([-v(x,c),-v(y,c)])
 ss.conf_budget(budget)
 ans=ss.solve_limited()
 print(t,n,k,ans,flush=True)
 if ans:
  model=set(ss.get_model())
  word=[next((c for c in range(4,k+1) if v(x,c) in model),0) if x in R else 0 for x in range(n)]
  open(f'tmp/found_{t}_{n}_{k}.txt','w').write(str(word))
 ss.delete()
if __name__=='__main__':
 for m in (16,18,20,22,24,26,28,30,32,36,40,44,48,52,56,60,64,72,80,90,96,108,120):
  for t in (0,1,2,3):
   solve(t,m if t!=2 else m*4,16,int(sys.argv[1]))
