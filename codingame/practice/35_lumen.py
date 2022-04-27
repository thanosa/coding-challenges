'''

https://www.codingame.com/ide/puzzle/lumen

'''


def spot_is_free(spot, candles, light):
    """
    A spot is NOT free if the horizontal and vertical distance between
    that and the light is less than the light strength
    """
    for candle in candles:
        x_dist = abs(candle[0] - spot[0])
        y_dist = abs(candle[1] - spot[1])
        if x_dist < light and y_dist < light:
            return False
    else:
        return True

# Read the meta
n = int(input())
light = int(input())

# Read the candle positions
candles = []
for y in range(n):
    for x, cell in enumerate(input().split()):
        if cell == "C":
            candles.append((x, y))

# Create the spots
spots = [(x, y) for x in range(n) for y in range(n)]

# Discard spots if they are close to any of the lights
free_spots = [s for s in spots if spot_is_free(s, candles, light)]

# Output the number of free spots
print(len(free_spots))
