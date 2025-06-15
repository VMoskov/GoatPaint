import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, p):
        # return new Point(self.x - p.x, self.y - p.y)
        new_p = Point(self.x - p.x, self.y - p.y)
        return new_p
    
    def translate(self, dp):
        # return new Point(self.x + dp.x, self.y + dp.y)
        new_p = Point(self.x + dp.x, self.y + dp.y)
        return new_p
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'
