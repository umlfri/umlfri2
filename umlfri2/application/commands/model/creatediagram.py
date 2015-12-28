from umlfri2.application.events.model import DiagramCreatedEvent
from ..base import Command


class CreateDiagramCommand(Command):
    def __init__(self, parent, diagram_type):
        self.__parent = parent
        self.__diagram_type = diagram_type
        self.__diagram = None
    
    @property
    def description(self):
        return "Creating diagram '{0}'".format(self.__diagram_type.id)
    
    def _do(self, ruler):
        self.__diagram = self.__parent.create_child_diagram(self.__diagram_type)
    
    def _redo(self, ruler):
        self.__parent.add_child(self.__diagram)
    
    def _undo(self, ruler):
        self.__parent.remove_child(self.__diagram)
    
    @property
    def diagram(self):
        return self.__diagram
    
    def get_updates(self):
        yield DiagramCreatedEvent(self.__diagram)
