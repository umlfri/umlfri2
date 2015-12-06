from umlfri2.application.events.diagram import ElementResizedMovedEvent
from ..base import Command


class ResizeMoveElementCommand(Command):
    def __init__(self, element, new_bounds):
        self.__element_name = element.object.get_display_name()
        self.__element = element
        self.__old_bounds = None
        self.__new_bounds = new_bounds
    
    @property
    def description(self):
        return "Element '{0}' resized".format(self.__element_name)
    
    def _do(self, ruler):
        self.__old_bounds = self.__element.get_bounds(ruler)
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        self.__element.move(ruler, self.__new_bounds.top_left)
        self.__element.resize(ruler, self.__new_bounds.size)
    
    def _undo(self, ruler):
        self.__element.move(ruler, self.__old_bounds.top_left)
        self.__element.resize(ruler, self.__old_bounds.size)
    
    def get_updates(self):
        yield ElementResizedMovedEvent(self.__element)
