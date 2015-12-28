from umlfri2.application.events.model import ElementCreatedEvent
from ..base import Command


class CreateElementCommand(Command):
    def __init__(self, parent, element_type):
        self.__parent = parent
        self.__element_type = element_type
        self.__element_object = None
    
    @property
    def description(self):
        return "Creating element '{0}'".format(self.__element_type.id)
    
    def _do(self, ruler):
        self.__element_object = self.__parent.create_child_element(self.__element_type)
    
    def _redo(self, ruler):
        self.__parent.add_child(self.__element_object)
    
    def _undo(self, ruler):
        self.__parent.remove_child(self.__element_object)
    
    @property
    def element_object(self):
        return self.__element_object
    
    def get_updates(self):
        yield ElementCreatedEvent(self.__element_object)
