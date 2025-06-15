from .state import State
from geometry.point import Point
from geometry.composite_shape import CompositeShape


class SelectShapeState(State):
    def __init__(self, model):
        self.model = model
        self.dragged_oject = None
        self.dragged_hot_point_idx = -1

    def mouse_down(self, mouse_point, shift_down, ctrl_down):
        selected_objects = self.model.get_selected_objects()
        if len(selected_objects) == 1:
            obj = selected_objects[0]
            hot_point_idx = self.model.find_selected_hot_point(obj, mouse_point)
            if hot_point_idx != -1:
                self.dragged_oject = obj
                self.dragged_hot_point_idx = hot_point_idx
                return
            
        # if hot point is not selected, select the object
        obj = self.model.find_selected_graphical_object(mouse_point)

        if obj is None:
            if not ctrl_down:  # if nothing is pressed, and no object is selected -> deselect all
                for o in list(self.model.get_selected_objects()):
                    o.set_selected(False)
            return
        
        if ctrl_down:  # toggle selection
            obj.set_selected(not obj.is_selected())
        else:  # select only this object, deselect others
            for o in list(self.model.get_selected_objects()):
                o.set_selected(False)
            obj.set_selected(True)

    def mouse_dragged(self, mouse_point):
        if self.dragged_oject is not None and self.dragged_hot_point_idx != -1:
            # move the dragged object
            self.dragged_oject.set_hot_point(self.dragged_hot_point_idx, mouse_point)

    def mouse_up(self, mouse_point, shift_down, ctrl_down):
        self.dragged_oject = None
        self.dragged_hot_point_idx = -1

    def key_pressed(self, key_code):
        selected = self.model.get_selected_objects()

        if key_code.lower() == 'g':
            if len(selected) > 1:
                new_group = CompositeShape(selected)
                
                for obj in selected:
                    self.model.remove_graphical_object(obj)
                
                self.model.add_graphical_object(new_group)
                new_group.set_selected(True)
            return

        if key_code.lower() == 'u':
            if len(selected) == 1 and isinstance(selected[0], CompositeShape):
                group_to_ungroup = selected[0]
                children = group_to_ungroup.get_children()
                
                self.model.remove_graphical_object(group_to_ungroup)
                
                for child in children:
                    self.model.add_graphical_object(child)
                    child.set_selected(True)
            return

        if not selected:
            return
        
        move_vectors = {
            'Up': Point(0, -1),
            'Down': Point(0, 1),
            'Left': Point(-1, 0),
            'Right': Point(1, 0)
        }

        if key_code in move_vectors:
            for obj in selected:
                obj.translate(move_vectors[key_code])
            return
        
        if key_code == 'plus':
            for obj in selected:
                self.model.increase_z(obj)
        elif key_code == 'minus':
            for obj in selected:
                self.model.decrease_z(obj)

    def after_draw(self, renderer, obj=None):
        if obj is None: return

        if obj.is_selected():
            bbox = obj.get_bounding_box()
            p1 = Point(bbox.x, bbox.y)
            p2 = Point(bbox.x + bbox.width, bbox.y)
            p3 = Point(bbox.x + bbox.width, bbox.y + bbox.height)
            p4 = Point(bbox.x, bbox.y + bbox.height)
            # Draw the bounding box in blue
            renderer.draw_line(p1, p2)
            renderer.draw_line(p2, p3)
            renderer.draw_line(p3, p4)
            renderer.draw_line(p4, p1)

            # if only one object is selected, draw the hot points
            if len(self.model.get_selected_objects()) == 1:
                for i in range(obj.get_number_of_hot_points()):
                    hp = obj.get_hot_point(i)
                    size = 3
                    p1_hp = Point(hp.x - size, hp.y - size)
                    p2_hp = Point(hp.x + size, hp.y - size)
                    p3_hp = Point(hp.x + size, hp.y + size)
                    p4_hp = Point(hp.x - size, hp.y + size)
                    renderer.fill_polygon([p1_hp, p2_hp, p3_hp, p4_hp])

    def on_leaving(self):
        for o in list(self.model.get_selected_objects()):
            o.set_selected(False)