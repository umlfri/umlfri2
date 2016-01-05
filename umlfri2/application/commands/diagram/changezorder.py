from umlfri2.application.events.diagram import ElementResizedMovedEvent
from ..base import Command


class ZOrderDirection:
    bellow = 0
    above = 1
    bottom = 2
    top = 3


class ChangeZOrderCommand(Command):
    def __init__(self, diagram, elements, direction):
        self.__diagram = diagram
        self.__elements = elements
        self.__direction = direction
        self.__new_z_indices = None
        self.__old_z_indices = None
    
    @property
    def description(self):
        if self.__direction == ZOrderDirection.bellow:
            return "Elements sent back"
        elif self.__direction == ZOrderDirection.above:
            return "Elements brought forward"
        elif self.__direction == ZOrderDirection.bottom:
            return "Elements sent to bottom"
        else:
            return "Elements brought to top"
    
    def _do(self, ruler):
        self.__old_z_indices = []
        
        for element in self.__elements:
            self.__old_z_indices.append((self.__diagram.get_z_order(element), element))
        
        self.__old_z_indices.sort()
        
        if self.__direction == ZOrderDirection.bottom:
            base = 0
        elif self.__direction == ZOrderDirection.top:
            base = self.__diagram.element_count - len(self.__elements)
        elif self.__direction == ZOrderDirection.above:
            base = -float('inf')
            for element in self.__elements:
                above_element = self.__diagram.get_visual_above(ruler, element)
                above_z_order = self.__diagram.get_z_order(above_element)
                if above_z_order > base:
                    base = above_z_order
        elif self.__direction == ZOrderDirection.bellow:
            base = float('inf')
            for element in self.__elements:
                below_element = self.__diagram.get_visual_below(ruler, element)
                below_z_order = self.__diagram.get_z_order(below_element)
                if below_z_order < base:
                    base = below_z_order
        
        self.__new_z_indices = []
        for no, (z_order, element) in enumerate(self.__old_z_indices):
            self.__new_z_indices.append((no + base, element))
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        for z_order, element in self.__new_z_indices:
            self.__diagram.change_z_order(element, z_order)
    
    def _undo(self, ruler):
        for z_order, element in self.__old_z_indices:
            self.__diagram.change_z_order(element, z_order)
    
    def get_updates(self):
        for element in self.__elements:
            yield ElementResizedMovedEvent(element)
