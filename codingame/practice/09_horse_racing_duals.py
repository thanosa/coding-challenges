'''

https://www.codingame.com/training/easy/horse-racing-duals

'''

import math


n = int(input())
a = []
for i in range(n):
    a.append(int(input()))

a.sort()
m = math.inf
for i, e in enumerate(a):
   if i == len(a) - 1:
      break
   else:
      d = abs(a[i+1] - a[i])
      if d < m:
         m = d

print(m)
