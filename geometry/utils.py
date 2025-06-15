import math
from .point import Point


def distance_from_point(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def distance_from_line_segment(start, end, p):
    segment_dx = end.x - start.x
    segment_dy = end.y - start.y
    segment_length_squared = segment_dx ** 2 + segment_dy ** 2

    if segment_length_squared == 0:
        return distance_from_point(start, p)
    
    t = ((p.x - start.x) * segment_dx + (p.y - start.y) * segment_dy) / segment_length_squared  # projection factor

    if t < 0:  # point is before the start of the segment
        closest_point = start
    elif t > 1:   # point is after the end of the segment
        closest_point = end
    else:  # point is on the segment
        closest_x = start.x + t * segment_dx
        closest_y = start.y + t * segment_dy
        closest_point = Point(closest_x, closest_y)

    return distance_from_point(closest_point, p)