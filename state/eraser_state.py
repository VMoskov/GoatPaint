from .state import State
from geometry.point import Point
from geometry.rectangle import Rectangle


class EraserState(State):
    def __init__(self, model):
        self.model = model
        self.path_points = []  # points for the eraser path

    def mouse_down(self, mouse_point, shift_down, ctrl_down):
        self.path_points.clear()
        self.path_points.append(mouse_point)
        self.model.notify_listeners()

    def mouse_dragged(self, mouse_point):
        self.path_points.append(mouse_point)
        self.model.notify_listeners()

    def mouse_up(self, mouse_point, shift_down, ctrl_down):
        self.path_points.append(mouse_point)

        objects_to_delete = []

        for obj in self.model.list():
            obj_bbox = obj.get_bounding_box()
            
            for i in range(len(self.path_points) - 1):
                p1 = self.path_points[i]
                p2 = self.path_points[i + 1]

                segment_bbox = Rectangle(
                    min(p1.x, p2.x), min(p1.y, p2.y),
                    abs(p2.x - p1.x), abs(p2.y - p1.y)
                )

                if self._do_bboxes_intersect(obj_bbox, segment_bbox):
                    objects_to_delete.append(obj)
                    break

        if objects_to_delete:
            for obj in objects_to_delete:
                self.model.remove_graphical_object(obj)

        self.path_points.clear()
        self.model.notify_listeners()

    def after_draw(self, renderer, go=None):
        if go is None and len(self.path_points) > 1:
            for i in range(len(self.path_points) - 1):
                p1 = self.path_points[i]
                p2 = self.path_points[i + 1]
                renderer.draw_line(p1, p2)

    def _do_bboxes_intersect(self, bbox1, bbox2):
        return not (bbox1.x + bbox1.width < bbox2.x or
                    bbox1.x > bbox2.x + bbox2.width or
                    bbox1.y + bbox1.height < bbox2.y or
                    bbox1.y > bbox2.y + bbox2.height)
    
    def key_pressed(self, key_code):
        pass

    def on_leaving(self):
        self.path_points.clear()