from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def mouse_down(self, mouse_point, shift_down, ctrl_down):
        pass

    @abstractmethod
    def mouse_up(self, mouse_point, shift_down, ctrl_down):
        pass

    @abstractmethod
    def mouse_dragged(self, mouse_point):
        pass

    @abstractmethod
    def key_pressed(self, key_code):
        pass

    @abstractmethod
    def after_draw(self, renderer, go):
        pass

    @abstractmethod
    def on_leaving(self):
        pass