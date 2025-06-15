from .graphical_object import AbstractGraphicalObject
from .point import Point
from .rectangle import Rectangle
from .utils import distance_from_line_segment


class LineSegment(AbstractGraphicalObject):
    def __init__(self, start=Point(0, 0), end=Point(10, 0)):
        super().__init__([start, end])
        self.start = start
        self.end = end

    def selection_distance(self, mouse_point):
        start = self.get_hot_point(0)
        end = self.get_hot_point(1)
        return distance_from_line_segment(start, end, mouse_point)
    
    def get_bounding_box(self):
        start = self.get_hot_point(0)
        end = self.get_hot_point(1)
        
        x = min(start.x, end.x)
        y = min(start.y, end.y)
        width = abs(end.x - start.x)
        height = abs(end.y - start.y)
        return Rectangle(x, y, width, height)
    
    def get_shape_name(self):
        return 'Line'
    
    def duplicate(self):
        # crate new object with the same point
        # NOTICE: listeners are not copied
        start_point = self.get_hot_point(0)
        end_point = self.get_hot_point(1)

        new_start_point = Point(start_point.x, start_point.y)
        new_end_point = Point(end_point.x, end_point.y)
        return LineSegment(new_start_point, new_end_point)
    
    def render(self, renderer):
        start = self.get_hot_point(0)
        end = self.get_hot_point(1)
        renderer.draw_line(start, end)

    def get_shape_id(self):
        return '@LINE'
    
    def save(self, rows):
        start = self.get_hot_point(0)
        end = self.get_hot_point(1)
        rows.append(f'{self.get_shape_id()} {start.x} {start.y} {end.x} {end.y}')

    def load(self, stack, data):
        parts = data.split()
        if len(parts) != 4:
            raise ValueError(f'Invalid line data: {data}')
        
        x1, y1, x2, y2 = map(float, parts)
        start = Point(x1, y1)
        end = Point(x2, y2)
        new_line = LineSegment(start, end)
        stack.append(new_line)