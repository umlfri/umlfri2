from umlfri2.application.events.model import DiagramDeletedEvent
from ..base import Command


class DeleteDiagramCommand(Command):
    def __init__(self, diagram):
        self.__parent = diagram.parent
        self.__diagram = diagram
    
    @property
    def description(self):
        return "Diagram deleted from the project"
    
    def _do(self, ruler):
        self._redo(ruler)
    
    def _redo(self, ruler):
        self.__parent.remove_child(self.__diagram)
    
    def _undo(self, ruler):
        self.__parent.add_child(self.__diagram)
    
    def get_updates(self):
        yield DiagramDeletedEvent(self.__diagram)
