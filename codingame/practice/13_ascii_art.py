'''

https://www.codingame.com/training/easy/ascii-art

'''


l = int(input())
h = int(input())
t = input()
row = []
for i in range(h):
    row.append(input())

for i in range(h):
    ln = []
    
    for c in t:
        coef = ord(c.upper()) - 65
        if coef < 0 or coef > 26:
            coef = 26
            
        p1 = coef * l
        p2 = coef * l + (l - 1)
        
        for j in range(p1, p2 + 1):
            ln.append(row[i][j])
        
    print(''.join(ln))
