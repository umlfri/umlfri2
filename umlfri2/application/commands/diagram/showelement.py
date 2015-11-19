from umlfri2.application.events.diagram import ElementShownEvent
from ..base import Command, CommandNotDone


class ShowElementCommand(Command):
    def __init__(self, diagram, element_object, point):
        self.__diagram_name = diagram.get_display_name()
        self.__diagram = diagram
        self.__point = point
        self.__element_visual = None
        self.__element_object = element_object
    
    @property
    def description(self):
        return "Showing element on diagram '{0}'".format(self.__diagram_name)
    
    def _do(self, ruler):
        if self.__diagram.contains(self.__element_object):
            raise CommandNotDone
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
        yield ElementShownEvent(self.__element_visual)
