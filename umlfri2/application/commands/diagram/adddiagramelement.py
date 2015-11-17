from umlfri2.application.events.diagram import ElementShownEvent
from umlfri2.application.events.model import ElementCreatedEvent
from ..base import Command


class AddDiagramElementCommand(Command):
    def __init__(self, diagram, element_type, point):
        self.__diagram_name = diagram.get_display_name()
        self.__diagram = diagram
        self.__element_type = element_type
        self.__point = point
        self.__element_visual = None
        self.__element_object = None
    
    @property
    def description(self):
        return "Adding element '{0}' to diagram '{1}'".format(self.__element_type.id, self.__diagram_name)
    
    def _do(self, ruler):
        self.__element_object = self.__diagram.parent.create_child_element(self.__element_type)
        self.__element_visual = self.__diagram.show(self.__element_object)
        self.__element_visual.move(ruler, self.__point)
    
    def _redo(self, ruler):
        pass # TODO
    
    def _undo(self, ruler):
        pass # TODO
    
    @property
    def element_visual(self):
        return self.__element_visual
    
    @property
    def element_object(self):
        return self.__element_object
    
    def get_updates(self):
        yield ElementCreatedEvent(self.__element_object)
        yield ElementShownEvent(self.__element_visual)
