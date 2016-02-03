from umlfri2.application.events.diagram import ElementResizedMovedEvent
from umlfri2.types.geometry import Vector
from ..base import Command


class AlignType:
    Minimum = 0
    Center = 1
    Maximum = 2


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
        if self.__horizontal == AlignType.Minimum:
            return "Selection in diagram {0} aligned left".format(self.__diagram)
        elif self.__horizontal == AlignType.Center:
            return "Selection in diagram {0} centered horizontally".format(self.__diagram)
        elif self.__horizontal == AlignType.Center:
            return "Selection in diagram {0} aligned right".format(self.__diagram)
        elif self.__vertical == AlignType.Minimum:
            return "Selection in diagram {0} aligned top".format(self.__diagram)
        elif self.__vertical == AlignType.Center:
            return "Selection in diagram {0} centered vertically".format(self.__diagram)
        elif self.__vertical == AlignType.Center:
            return "Selection in diagram {0} aligned bottom".format(self.__diagram)
    
    def _do(self, ruler):
        if self.__horizontal is not None:
            aligned_x = (self.__align_to.x1 * (2 - self.__horizontal) + self.__align_to.x2 * self.__horizontal) // 2
        if self.__vertical is not None:
            aligned_y = (self.__align_to.y1 * (2 - self.__vertical) + self.__align_to.y2 * self.__vertical) // 2
        
        for element in self.__elements:
            bounds = element.get_bounds(ruler)
            
            if self.__horizontal is None:
                vector_x = 0
            else:
                aligned_bounds_x = (bounds.x1 * (2 - self.__horizontal) + bounds.x2 * self.__horizontal) // 2
                vector_x = aligned_x - aligned_bounds_x
            
            if self.__vertical is None:
                vector_y = 0
            else:
                aligned_bounds_y = (bounds.y1 * (2 - self.__vertical) + bounds.y2 * self.__vertical) // 2
                vector_y = aligned_y - aligned_bounds_y
            
            self.__element_positions.append((element, element.get_position(ruler), Vector(vector_x, vector_y)))
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        for element, position, vector in self.__element_positions:
            element.move(ruler, position + vector)
    
    def _undo(self, ruler):
        for element, position, vector in self.__element_positions:
            element.move(ruler, position)
    
    def get_updates(self):
        for element in self.__elements:
            yield ElementResizedMovedEvent(element)
