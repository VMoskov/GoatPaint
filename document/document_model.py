# document_model.py
from geometry.graphical_object import AbstractGraphicalObject
from listeners.graphical_object.graphical_object_listener import GraphicalObjectListener
from listeners.document_model.document_model_listener import DocumentModelListener
from geometry.point import Point

class DocumentModel(GraphicalObjectListener):
    SELECTION_PROXIMITY: float = 10.0

    def __init__(self):
        self.objects = []
        self.selected_objects = []
        self.listeners = []

    # -- Observer methods --
    def graphical_object_changed(self, go):
        self.notify_listeners()

    def graphical_object_selection_changed(self, go):
        if go.is_selected() and go not in self.selected_objects:
            self.selected_objects.append(go)
        elif not go.is_selected() and go in self.selected_objects:
            self.selected_objects.remove(go)
        
        self.notify_listeners()

    def add_document_model_listener(self, l):
        if l not in self.listeners:
            self.listeners.append(l)

    def remove_document_model_listener(self, l):
        if l in self.listeners:
            self.listeners.remove(l)

    def notify_listeners(self):
        for l in self.listeners:
            l.document_change()

    # --- Object management methods ---
    def clear(self):
        for obj in self.objects:
            obj.remove_graphical_object_listener(self)

        self.objects.clear()
        self.selected_objects.clear()
        self.notify_listeners()

    def add_graphical_object(self, obj):
        self.objects.append(obj)
        obj.add_graphical_object_listener(self)
        if obj.is_selected() and obj not in self.selected_objects:
            self.selected_objects.append(obj)
        self.notify_listeners()

    def remove_graphical_object(self, obj: AbstractGraphicalObject):
        if obj in self.objects:
            obj.remove_graphical_object_listener(self)
            self.objects.remove(obj)
            if obj in self.selected_objects:
                self.selected_objects.remove(obj)
            self.notify_listeners()

    def list(self):
        return list(self.objects)

    # -- Selection methods --
    def get_selected_objects(self):
        return list(self.selected_objects)

    def find_selected_graphical_object(self, mouse_point):
        min_dist = float('inf')
        selected_obj = None
        for obj in self.objects:
            dist = obj.selection_distance(mouse_point)
            if dist < self.SELECTION_PROXIMITY and dist < min_dist:
                min_dist = dist
                selected_obj = obj
        return selected_obj

    def find_selected_hot_point(self, obj, mouse_point):
        min_dist = float('inf')
        selected_hp_index = -1
        for i in range(obj.get_number_of_hot_points()):
            dist = obj.get_hot_point_distance(i, mouse_point)
            if dist < self.SELECTION_PROXIMITY and dist < min_dist:
                min_dist = dist
                selected_hp_index = i
        return selected_hp_index

    # ---  Z-order methods ---
    def increase_z(self, go):
        if go in self.objects:
            index = self.objects.index(go)
            if index < len(self.objects) - 1:
                self.objects.pop(index)
                self.objects.insert(index + 1, go)
                self.notify_listeners()

    def decrease_z(self, go):
        if go in self.objects:
            index = self.objects.index(go)
            if index > 0:
                self.objects.pop(index)
                self.objects.insert(index - 1, go)
                self.notify_listeners()