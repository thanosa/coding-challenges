import time


def calc_recipes(recipes_cnt):

    recipes = ['3', '7']
    pos1 = 0
    pos2 = 1
    while True:
        score = int(recipes[pos1]) + int(recipes[pos2])
        for digit in str(score):
            recipes.append(digit)

        pos1 = (pos1 + int(recipes[pos1]) + 1) % len(recipes)
        pos2 = (pos2 + int(recipes[pos2]) + 1) % len(recipes)

        if len(recipes) >= recipes_cnt + 10:
            return ''.join(recipes[recipes_cnt:recipes_cnt + 10])


def calc_left_recipes(recipes_seq):

    recipes = ['3', '7']
    pos1 = 0
    pos2 = 1
    while True:
        score = int(recipes[pos1]) + int(recipes[pos2])
        for digit in str(score):
            recipes.append(digit)

        pos1 = (pos1 + int(recipes[pos1]) + 1) % len(recipes)
        pos2 = (pos2 + int(recipes[pos2]) + 1) % len(recipes)

        # We add one more since in each round the recipe scores can have one or two digits
        l = len(str(recipes_seq))
        sub = ''.join(recipes[-l-1:])
        for i in range(2):
            check1 = sub[i:l+i]
            check2 = str(recipes_seq)
            # print(check1, check2)
            if check1 == check2:
                return len(recipes) - len(str(recipes_seq)) - 1 + i


start = time.time()

assert calc_recipes(5) == "0124515891"
assert calc_recipes(18) == "9251071085"
assert calc_recipes(2018) == "5941429882"
print(calc_recipes(190221))

assert(calc_left_recipes("51589")) == 9
assert(calc_left_recipes("01245")) == 5
assert(calc_left_recipes("92510")) == 18
assert(calc_left_recipes("59414")) == 2018
print(calc_left_recipes(190221))


print("Seconds spent: ", round(time.time() - start, 5))
