'''

https://www.codingame.com/training/easy/bank-robbers

'''

r = int(input())
v = int(input())

robber_time = [0] * r
for i in range(v):
    c, n = [int(j) for j in input().split()]

    idx = robber_time.index(min(robber_time))
    robber_time[idx] += (10 ** n) * (5 ** (c-n))
        
print(max(robber_time))
