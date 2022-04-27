'''

https://www.codingame.com/training/easy/brackets-extreme-edition

'''

e = input()
d = {')': '(', ']': '[', '}': '{'}

s = []

for c in e:
    if c in d.values():
        s.append(c)
    elif c in d.keys():
        if len(s) == 0:
            print("false")
            exit(0)
        else:
            if d[c] == s.pop():
                pass
            else:
                print("false")
                exit(0)


if len(s) == 0:
    print("true")
else:
    print("false")
