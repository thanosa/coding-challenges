'''

https://www.codingame.com/training/easy/mime-type

'''


n = int(input())
q = int(input())

d = {}
for i in range(n):
    ext, mt = input().split()
    d[ext.lower()] = mt

for i in range(q):
    fname = input()
    tokens = fname.split('.')
    
    if len(tokens) > 1:
        ext = tokens[-1].lower()

        if ext in d:
            mime = d[ext]
        else:
            mime = 'UNKNOWN'
    else:
        mime = 'UNKNOWN'
        
    print(mime)
