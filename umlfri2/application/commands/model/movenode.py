from umlfri2.application.events.model import NodeMovedEvent
from ..base import Command


class MoveNodeCommand(Command):
    def __init__(self, node, new_parent, new_index):
        self.__node_name = node.get_display_name()
        self.__node = node
        self.__new_parent = new_parent
        self.__new_index = new_index
        self.__old_parent = None
        self.__old_index = None
    
    @property
    def description(self):
        return "Node {0} moved in the project".format(self.__node_name)

    def _do(self, ruler):
        self.__old_parent = self.__node.parent
        self.__old_index = self.__old_parent.get_child_index(self.__node)
        
        self.__node.change_parent(self.__new_parent, self.__new_index)

    def _redo(self, ruler):
        self.__node.change_parent(self.__new_parent, self.__new_index)
    
    def _undo(self, ruler):
        self.__node.change_parent(self.__old_parent, self.__old_index)
        
    
    def get_updates(self):
        yield NodeMovedEvent(self.__node, self.__old_parent, self.__old_index, self.__new_parent, self.__new_index)
