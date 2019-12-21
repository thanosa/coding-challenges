'''

https://www.codingame.com/training/easy/happy-numbers

'''
import sys
import math


def happy(x):
    seen = set()
    
    while True:
        s = 0
        for c in str(x):
            s += int(c) * int(c)

        if s in seen:
            return False
        elif s == 1:
            return True
        else:
            seen.add(s)
        
        x = s


n = int(input())
for i in range(n):
    x = input()
    
    if happy(x):
        print(str(x), ':)')
    else:
        print(str(x), ':(')
        