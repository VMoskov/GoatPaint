from abc import ABC, abstractmethod


class Renderer(ABC):
    @abstractmethod
    def draw_line(start, end):
        pass

    @abstractmethod
    def fill_polygon(points):
        pass