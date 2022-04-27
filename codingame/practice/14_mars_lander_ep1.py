'''

https://www.codingame.com/training/easy/mars-lander-episode-1

'''


surface_n = int(input()) 
for i in range(surface_n):
    _, _ = [int(j) for j in input().split()]

while True:
    _, _, _, v_speed, _, _, _ = [int(i) for i in input().split()]

    print("0 4" if v_speed < -35 else "0 3")
