'''

https://www.codingame.com/training/medium/escaping-the-cat

'''
import math

from typing import Tuple


def calc_angle(x: float, y: float) -> float:
    """Calculate the angle of a point from the center in degrees"""
    return math.degrees(math.atan2(float(y), float(x)))


def calc_distance(x1: float, y1: float, x2: float, y2:float) -> float:
    """Calculate the distance between two points"""
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def move_on_angle(x: float, y:float, angle: float, distance: float) -> Tuple[float, float]:
    """Move a distance towards an angle in radians"""
    return x + distance * math.cos(angle), y + distance * math.sin(angle)


def move_on_circle(x:float, y:float, radius:float, distance:float):
    """Move a distance on a circle with specific radius"""

    # Calculate the theta of the differential angle 
    a, b, c = radius, radius, distance
    theta = math.acos((a**2 + b**2 - c**2) / (2 * a * b))

    # The new angle is the old one plus the differential angle theta
    old_angle = math.atan2(float(y), float(x))
    new_angle = old_angle + theta

    # Calculate the new x and y and with the basic trigonometric calculation
    new_x = radius * math.cos(new_angle)
    new_y = radius * math.sin(new_angle)
    return new_x, new_y
    

def calc_sweet_spot_radius(radius: float, cat_speed: float, mouse_speed: float, percentage: float) -> float:
    """Calculate the sweet spot radius from which the mouse can dash to the edge, 
    provided it is positioned on about 180 degrees opposite from the cat"""

    # The max time available is the time it takes for the cat to run half the circle
    perimeter = 2 * math.pi * radius
    max_available_time = (perimeter / 2) / cat_speed

    # The mouse should be outside this circle to have enough time to dash.
    min_circle = max(radius - (mouse_speed * max_available_time), 0)

    # The mouse should be inside this circle so that it can rotate faster than the cat.
    # TODO: This calculation doesn't seem correct.
    max_circle = radius * (mouse_speed / cat_speed)

    # The target radius is in between the min and the max 
    # The percentage variable controls the proximity of the sweet spot towards the min or max limits
    sweet_spot_radius = (max_circle * percentage) + (min_circle * (1 - percentage))
    return sweet_spot_radius

#
# Parameters
#

# Main optimization parameter by which the exact location of the sweet spot is calculated.
# Towards 0% the sweet spot will be on the min circle and 100% will be on the max circle.
SWEET_SPOT_PERC = 0.67

# Minimum allowable distance from the center where the mouse is considered centered.
# Not an important parameter as the first phase is not critical.
CENTER_TOLERANCE = 3

# Minimum allowable distance from the target radius
RADIUS_TOLERANCE = 5

# Minimum allowable agnle from the target angle. 
# Lowering this value too much, will make the mouse rotate on the sweet spot for ever.
# Increasing this angle will allow the mouse to dash even though it is not opposite from the cat.
ANGLE_TOLERANCE = 5

#
# Constants
#
mouse_speed = 10
radius = 500
cat_speed = int(input())

# Phases:
#  1: Move to the center
#  2: Move to the sweet spot circle
#  3: Move on the sweet spot circle until the cat is opposite from the mouse
#  4: Dash to the edge

# Initialization
phase = 1
sweet_spot_radius = calc_sweet_spot_radius(radius, cat_speed, mouse_speed, SWEET_SPOT_PERC)
p2_cat_angle = None

while True:
    # Ingest the input string.
    mouse_x, mouse_y, cat_x, cat_y = [int(i) for i in input().split()]

    if phase == 1:
        # In phase one move the mouse to the center.
        distance = calc_distance(mouse_x, mouse_y, 0, 0)
        if abs(distance) < CENTER_TOLERANCE:
            phase += 1
        else:
            mouse_x, mouse_y = 0, 0

    if phase == 2:
        # In phase 2 move the mouse to the sweet spot radius, towards the cat.
        distance = sweet_spot_radius - calc_distance(mouse_x, mouse_y, 0, 0)
        if abs(distance) < RADIUS_TOLERANCE:
            phase += 1
        else:
            # Freeze the target to the current cat angle.
            if not p2_cat_angle:
                p2_cat_angle = calc_angle(cat_x, cat_y) + 180

            # Move towards the frozen cat angle.
            mouse_x, mouse_y = move_on_angle(
                mouse_x, mouse_y, 
                angle=math.radians(p2_cat_angle), 
                distance=min(distance, mouse_speed)
        )

    if phase == 3:
        # If the mouse is opposite from the cat, then it is time for phase 3.
        opponent_angle = abs(calc_angle(mouse_x, mouse_y) - calc_angle(cat_x, cat_y))
        if abs(opponent_angle - 180) < ANGLE_TOLERANCE:
            phase += 1

        # Move on the direction that will increase the angle between the mouse and the cat.
        mouse_x, mouse_y = move_on_circle(mouse_x, mouse_y, sweet_spot_radius, distance=mouse_speed)
    
    if phase == 4:
        # Dash the mouse to the edge
        mouse_angle = calc_angle(mouse_x, mouse_y)
        mouse_x, mouse_y = move_on_angle(mouse_x, mouse_y, math.radians(mouse_angle), mouse_speed)

    print(f"{round(mouse_x)} {round(mouse_y)} p{phase}")
