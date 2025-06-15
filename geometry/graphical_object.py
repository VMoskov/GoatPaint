from abc import ABC, abstractmethod
from .point import Point
from .utils import distance_from_point, distance_from_line_segment


class AbstractGraphicalObject(ABC):
    def __init__(self, hot_points):
        self.hot_points = hot_points
        self.hot_points_selected = [False] * len(hot_points)
        self.selected = False
        self.listeners = []

    # -- Object edit methods --
    def is_selected(self):
        return self.selected

    def set_selected(self, selected: bool):
        self.selected = selected
        self.notify_selection_changed()

    def get_number_of_hot_points(self):
        return len(self.hot_points)

    def get_hot_point(self, index: int) -> Point:
        if 0 <= index < len(self.hot_points):
            return self.hot_points[index]
        raise IndexError('Hot point index out of range')

    def set_hot_point(self, index: int, p: Point):
        if 0 <= index < len(self.hot_points):
            self.hot_points[index] = p
            self.notify_changed()
        else:
            raise IndexError('Hot point index out of range')

    def is_hot_point_selected(self, index: int) -> bool:
        if 0 <= index < len(self.hot_points_selected):
            return self.hot_points_selected[index]
        raise IndexError('Hot point index out of range')

    def set_hot_point_selected(self, index: int, selected: bool):
        if 0 <= index < len(self.hot_points_selected):
            self.hot_points_selected[index] = selected
            self.notify_selection_changed()
        else:
            raise IndexError('Hot point index out of range')

    def get_hot_point_distance(self, index: int, mouse_point: Point) ->  float:
        if 0 <= index < len(self.hot_points):
            return distance_from_point(self.hot_points[index], mouse_point)
        raise IndexError('Hot point index out of range')

    # -- Geometric operations on shape --
    def translate(self, dp: Point):
        for i in range(len(self.hot_points)):
            self.hot_points[i] = self.hot_points[i].translate(dp)
        self.notify_changed()

    @abstractmethod
    def get_bounding_box(self):
        pass

    @abstractmethod
    def selection_distance(self, mouse_point: Point) -> float:
        pass

    # -- Drawing methods (bridge pattern) --
    @abstractmethod
    def render(self, renderer):
        pass

    # -- Observer --
    def add_graphical_object_listener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_graphical_object_listener(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def notify_changed(self):
        for listener in self.listeners:
            listener.graphical_object_changed(self)

    def notify_selection_changed(self):
        for listener in self.listeners:
            listener.graphical_object_selection_changed(self)

    # -- Prototype support --
    @abstractmethod
    def get_shape_name(self) -> str:
        pass

    @abstractmethod
    def duplicate(self):
        pass

    # -- Saving and loading --
    @abstractmethod
    def get_shape_id(self) -> str:
        pass

    @abstractmethod
    def load(self, stack, data):
        pass

    @abstractmethod
    def save(self, rows):
        pass