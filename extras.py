from shapes import Rect, Circle
import math


def circle_rect_collision(circle: Circle, rect: Rect):
    cx = circle.position.x
    cy = circle.position.y
    radius = circle.radius.value
    rx = rect.position.x - rect.size.x / 2
    ry = rect.position.y - rect.size.y / 2
    rw = rect.size.x
    rh = rect.size.y

    testX = cx
    testY = cy

    # which edge is closest?
    if (cx < rx):
        testX = rx        # test left edge
    elif (cx > rx+rw):
        testX = rx + rw   # right edge
    if (cy < ry):
        testY = ry        # top edge
    elif (cy > ry + rh):
        testY = ry + rh   # bottom edge
    
    # get distance from closest edges
    distX = cx - testX
    distY = cy - testY
    distance = math.sqrt((distX * distX) + (distY * distY))

    # if the distance is less than the radius, collision!
    if (distance <= radius):
        return True
    return False
