from enum import Enum, unique

from umlfri2.application.events.diagram import ElementResizedMovedEvent
from umlfri2.types.geometry import Vector
from ..base import Command


@unique
class AlignType(Enum):
    minimum = 1
    center = 2
    maximum = 3


class AlignSelectionCommand(Command):
    def __init__(self, selection, vertical=None, horizontal=None):
        if vertical is not None and horizontal is not None:
            raise Exception
        if vertical is None and horizontal is None:
            raise Exception
        
        self.__diagram = selection.diagram.get_display_name()
        self.__elements = list(selection.selected_elements)
        self.__vertical = vertical
        self.__horizontal = horizontal
        self.__align_to = selection.get_bounds(include_connections=False)
        
        self.__element_positions = []
    
    @property
    def description(self):
        if self.__horizontal == AlignType.minimum:
            return "Selection in diagram {0} aligned left".format(self.__diagram)
        elif self.__horizontal == AlignType.center:
            return "Selection in diagram {0} centered horizontally".format(self.__diagram)
        elif self.__horizontal == AlignType.center:
            return "Selection in diagram {0} aligned right".format(self.__diagram)
        elif self.__vertical == AlignType.minimum:
            return "Selection in diagram {0} aligned top".format(self.__diagram)
        elif self.__vertical == AlignType.center:
            return "Selection in diagram {0} centered vertically".format(self.__diagram)
        elif self.__vertical == AlignType.center:
            return "Selection in diagram {0} aligned bottom".format(self.__diagram)
    
    def __align(self, align_type, v1, v2):
        if align_type == AlignType.minimum:
            return v1
        elif align_type == AlignType.center:
            return (v1 + v2) // 2
        elif align_type == AlignType.maximum:
            return v2
        else:
            return None
            
    
    def _do(self, ruler):
        aligned_x = self.__align(self.__horizontal, self.__align_to.x1, self.__align_to.x2)
        aligned_y = self.__align(self.__vertical, self.__align_to.y1, self.__align_to.y2)
        
        for element in self.__elements:
            bounds = element.get_bounds(ruler)
            
            if self.__horizontal is None:
                vector_x = 0
            else:
                vector_x = aligned_x - self.__align(self.__horizontal, bounds.x1, bounds.x2)
            
            if self.__vertical is None:
                vector_y = 0
            else:
                vector_y = aligned_y - self.__align(self.__vertical, bounds.y1, bounds.y2)
            
            old_position = element.get_position(ruler)
            new_position = old_position + Vector(vector_x, vector_y)
            
            self.__element_positions.append((element, old_position, new_position))
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        for element, old_position, new_position in self.__element_positions:
            element.move(ruler, new_position)
    
    def _undo(self, ruler):
        for element, old_position, new_position in self.__element_positions:
            element.move(ruler, old_position)
    
    def get_updates(self):
        for element in self.__elements:
            yield ElementResizedMovedEvent(element)
