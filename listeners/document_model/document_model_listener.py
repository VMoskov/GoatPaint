from abc import ABC, abstractmethod

class DocumentModelListener(ABC):
    @abstractmethod
    def document_change(self):
        pass