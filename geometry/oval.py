import math
from .graphical_object import AbstractGraphicalObject
from .point import Point
from .rectangle import Rectangle


class Oval(AbstractGraphicalObject):
    NUM_SEGMENTS = 36  # Number of segments to approximate the ellipse

    def __init__(self, hot_point1=Point(0, 10), hot_point2=Point(10, 0)):
        super().__init__([hot_point1, hot_point2])
        self.hot_point1 = hot_point1
        self.hot_point2 = hot_point2

    def get_bounding_box(self):
        p1 = self.get_hot_point(0)
        p2 = self.get_hot_point(1)

        x = min(p1.x, p2.x)
        y = min(p1.y, p2.y)
        width = abs(p2.x - p1.x)
        height = abs(p2.y - p1.y)
        return Rectangle(x, y, width, height)
    
    def selection_distance(self, mouse_point):
        bbox = self.get_bounding_box()

        # ellipse center
        center_x = bbox.x + bbox.width / 2
        center_y = bbox.y + bbox.height / 2
        # ellipse radius
        radius_x = bbox.width / 2
        radius_y = bbox.height / 2

        if radius_x == 0 or radius_y == 0:
            # If the bounding box is a point, return distance to that point
            return math.sqrt((mouse_point.x - center_x) ** 2 + (mouse_point.y - center_y) ** 2)
        
        dx = mouse_point.x - center_x
        dy = mouse_point.y - center_y

        value = (dx / radius_x) ** 2 + (dy / radius_y) ** 2
        if value <= 1:  # inside the ellipse
            return 0
        else:  # outside the ellipse
            return math.sqrt(dx**2 + dy**2) - (radius_x * radius_y) / (math.sqrt((radius_y * dx) ** 2 + (radius_x * dy) ** 2))
        
    def get_shape_name(self):
        return 'Oval'
    
    def duplicate(self):
        # Create new object with the same hot points
        # NOTICE: listeners are not copied
        hot_point1 = self.get_hot_point(0)
        hot_point2 = self.get_hot_point(1)

        new_hot_point1 = Point(hot_point1.x, hot_point1.y)
        new_hot_point2 = Point(hot_point2.x, hot_point2.y)
        return Oval(new_hot_point1, new_hot_point2)
    
    def render(self, renderer):
        bbox = self.get_bounding_box()

        # Calculate the center and radii
        center_x = bbox.x + bbox.width / 2
        center_y = bbox.y + bbox.height / 2
        radius_x = bbox.width / 2
        radius_y = bbox.height / 2

        polygon_points = []
        
        for i in range(self.NUM_SEGMENTS):
            angle = 2 * math.pi * i / self.NUM_SEGMENTS
            x = center_x + radius_x * math.cos(angle)
            y = center_y + radius_y * math.sin(angle)
            polygon_points.append(Point(x, y))

        renderer.fill_polygon(polygon_points)

    def get_shape_id(self):
        return '@OVAL'
    
    def save(self, rows):
        p1 = self.get_hot_point(0)
        p2 = self.get_hot_point(1)
        rows.append(f'{self.get_shape_id()} {p1.x} {p1.y} {p2.x} {p2.y}')

    def load(self, stack, data):
        parts = data.split()
        if len(parts) != 4:
            raise ValueError(f'Invalid oval data: {data}')
        
        x1, y1, x2, y2 = map(float, parts)
        hot_point1 = Point(x1, y1)
        hot_point2 = Point(x2, y2)
        new_oval = Oval(hot_point1, hot_point2)
        stack.append(new_oval)