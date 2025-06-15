from .state import State


class IdleState(State):

    def mouse_down(self, mouse_point, shift_down, ctrl_down):
        pass

    def mouse_up(self, mouse_point, shift_down, ctrl_down):
        pass

    def mouse_dragged(self, mouse_point):
        pass

    def key_pressed(self, key_code):
        pass

    def after_draw(self, renderer, go=None):
        pass

    def on_leaving(self):
        pass