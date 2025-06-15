from .state import State


class AddShapeState(State):
    def __init__(self, model, prototype):
        self.model = model
        self.prototype = prototype

    def mouse_down(self, mouse_point, shift_down, ctrl_down):
        new_object = self.prototype.duplicate()
        new_object.translate(mouse_point)
        self.model.add_graphical_object(new_object)

    def mouse_up(self, mouse_point, shift_down, ctrl_down):
        pass

    def mouse_dragged(self, mouse_point):
        pass

    def key_pressed(self, key_code):
        pass

    def after_draw(self, renderer, obj=None):
        pass

    def on_leaving(self):
        pass