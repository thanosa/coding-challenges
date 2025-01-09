'''

https://www.codingame.com/training/easy/the-descent

'''


while True:
    a = []
    for i in range(8):
        a.append(int(input()))
    
    m = -1
    s = -1
    for j, e in enumerate(a):        
        if e > m:
            m = e
            s = j
            
    print(s)
