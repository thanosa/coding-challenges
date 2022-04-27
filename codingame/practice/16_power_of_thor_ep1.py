'''

https://www.codingame.com/training/easy/power-of-thor-episode-1

'''


light_x, light_y, initial_tx, initial_ty = [int(i) for i in input().split()]

pos_x = initial_tx
pos_y = initial_ty

while True:
    remaining_turns = int(input()) 

    x_dis = pos_x - light_x
    y_dis = pos_y - light_y

    if y_dis > 0:
        vertical = "N"
        pos_y -= 1
    elif y_dis < 0:
        vertical = "S"
        pos_y += 1
    else:
        vertical = ""
        
    if x_dis > 0:
        horizontal = "W"
        pos_x -= 1
    elif x_dis < 0:
        horizontal = "E"
        pos_x += 1
    else:
        horizontal = ""
    
    print(vertical + horizontal)
   