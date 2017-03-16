from enum import Enum, unique

from umlfri2.application.events.diagram import ElementResizedMovedEvent
from ..base import Command, CommandNotDone


@unique
class ZOrderDirection(Enum):
    bellow = 1
    above = 2
    bottom = 3
    top = 4


class ChangeZOrderCommand(Command):
    def __init__(self, diagram, elements, direction):
        self.__diagram = diagram
        self.__elements = tuple(elements)
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
        
        for element in self.__elements:
            if self.__direction in (ZOrderDirection.above, ZOrderDirection.top):
                found = self.__diagram.get_visual_above(ruler, element, self.__elements)
            else:
                found = self.__diagram.get_visual_below(ruler, element, self.__elements)
            
            if found is not None:
                break
        else:
            raise CommandNotDone
        
        if self.__direction == ZOrderDirection.bottom:
            base = 0
        elif self.__direction == ZOrderDirection.top:
            base = self.__diagram.element_count - len(self.__elements)
        elif self.__direction == ZOrderDirection.above:
            # find the z-order of lowest element above the selection
            base = float('inf')
            for element in self.__elements:
                above_element = self.__diagram.get_visual_above(ruler, element, self.__elements)
                if above_element is not None:
                    above_z_order = self.__diagram.get_z_order(above_element)
                    if above_z_order < base:
                        base = above_z_order
            
            # is z-ordered elements are bellow found base, indices will be changed after their removal from a diagram
            delta = 0
            for element in self.__elements:
                z_order = self.__diagram.get_z_order(element)
                if z_order < base:
                    delta += 1
            
            base -= delta
            
            # new z-order should be above the found one
            base += 1
        elif self.__direction == ZOrderDirection.bellow:
            # find the z-order of topmost element below the selection
            base = -float('inf')
            for element in self.__elements:
                below_element = self.__diagram.get_visual_below(ruler, element, self.__elements)
                if below_element is not None:
                    below_z_order = self.__diagram.get_z_order(below_element)
                    if below_z_order > base:
                        base = below_z_order
        
        self.__new_z_indices = []
        for no, (z_order, element) in enumerate(self.__old_z_indices):
            self.__new_z_indices.append((no + base, element))
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        self.__diagram.change_z_order_many(self.__new_z_indices)
    
    def _undo(self, ruler):
        self.__diagram.change_z_order_many(self.__old_z_indices)
    
    def get_updates(self):
        for element in self.__elements:
            yield ElementResizedMovedEvent(element)
