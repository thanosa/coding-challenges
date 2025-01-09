'''

https://www.codingame.com/training/easy/onboarding

'''


while 1:
    enemy_1 = input()  
    dist_1 = int(input())  
    enemy_2 = input() 
    dist_2 = int(input()) 

    if dist_1 < dist_2:
        print(enemy_1)
    else:
        print(enemy_2)
