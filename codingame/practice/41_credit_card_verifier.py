'''

https://www.codingame.com/training/easy/order-of-succession

'''

n = int(input())
for i in range(n):
    sum = 0
    card = input()

    for i, d in enumerate(reversed(card.replace(" ", ""))):
        v = int(d)
        if i % 2 == 0:
            sum += v
        else:
            v *= 2
            if v > 9:
                v -= 9
            sum += v

    print("YES" if sum % 10 == 0 else "NO")
