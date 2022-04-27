'''

https://www.codingame.com/training/easy/container-terminal

'''


n = int(input())
for i in range(n):
    stack = []
    for track in input():
        for i, top in enumerate(stack):
            if ord(track) <= ord(top):
                stack[i] = track
                break
        else:
            stack.append(track)
    print(len(stack))
