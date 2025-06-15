from .graphical_object import AbstractGraphicalObject
from .point import Point
from .rectangle import Rectangle
from listeners.graphical_object.graphical_object_listener import GraphicalObjectListener


class CompositeShape(AbstractGraphicalObject, GraphicalObjectListener):
    def __init__(self, children):
        super().__init__([])
        self.children = children
        for child in children:
            child.add_graphical_object_listener(self)

    def get_children(self):
        return list(self.children)
    
    # -- delegate methods to children --
    def render(self, renderer):
        for child in self.children:
            child.render(renderer)

    def translate(self, dp):
        for child in self.children:
            child.translate(dp)
        # dont call notify_changed(), since every child will call it

    def get_bounding_box(self):
        if not self.children:
            return Rectangle(0, 0, 0, 0)
        
        bbox = self.children[0].get_bounding_box()
        min_x, min_y = bbox.x, bbox.y
        max_x, max_y = bbox.x + bbox.width, bbox.y + bbox.height

        for i in range(1, len(self.children)):
            child_bbox = self.children[i].get_bounding_box()
            min_x = min(min_x, child_bbox.x)
            min_y = min(min_y, child_bbox.y)
            max_x = max(max_x, child_bbox.x + child_bbox.width)
            max_y = max(max_y, child_bbox.y + child_bbox.height)

        return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)
    
    def get_shape_name(self):
        return 'Composite Shape'
    
    def duplicate(self):
        new_children = [child.duplicate() for child in self.children]
        new_shape = CompositeShape(new_children)
        return new_shape
    
    def graphical_object_changed(self, go):
        self.notify_changed()

    def graphical_object_selection_changed(self, go):
        self.notify_selection_changed()

    def selection_distance(self, mouse_point):
        return min(child.selection_distance(mouse_point) for child in self.children)
    
    def get_shape_id(self):
        return '@COMP'
    
    def save(self, rows):
        for child in self.children:
            child.save(rows)
        rows.append(f'{self.get_shape_id()} {len(self.children)}')

    def load(self, stack, data):
        num_children = int(data)
        children = []
        for _ in range(num_children):
            child_data = stack.pop()
            children.append(child_data)

        children.reverse()

        new_composite = CompositeShape(children)
        stack.append(new_composite)