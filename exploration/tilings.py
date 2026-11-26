from itertools import combinations
Q=40
def tilings():
 masks=[sum(1<<((a+j)%Q) for j in (0,4,5,9)) for a in range(Q)]
 full=(1<<Q)-1
 def go(used,selected):
  if used==full:
   yield selected
   return
  hole=(~used & (used+1)).bit_length()-1
  for j in (0,4,5,9):
   a=(hole-j)%Q
   if not used&masks[a]:
    yield from go(used|masks[a],selected|(1<<a))
 return list(go(0,0))
def br(mask):
 return ''.join('#' if mask>>i&1 else '.' for i in range(Q))
def norm(s):
 return min(w[i:]+w[:i] for w in (s,s[::-1]) for i in range(Q))
T=tilings()
U=sorted(set(norm(br(a|b)) for a,b in combinations(T,2) if not a&b))
print(len(T),len(U),sum(not a&b for a,b in combinations(T,2)))
for s in U:
 p=next(k for k in range(1,Q+1) if Q%k==0 and s[:k]*(Q//k)==s)
 print(p,s[:p])
