from abc import ABC, abstractmethod


class GraphicalObjectListener(ABC):
    @abstractmethod
    def graphical_object_changed(self, go):
        pass

    @abstractmethod
    def graphical_object_selection_changed(self, go):
        pass