from ..base import Command


class MoveSelectionCommand(Command):
    def __init__(self, selection, delta):
        self.__diagram_name = selection.diagram.get_display_name()
        self.__elements = list(selection.selected_elements)
        self.__delta = delta
        self.__element_positions = []
    
    @property
    def description(self):
        return "Selection in diagram '{0}' moved".format(self.__diagram_name)

    def _do(self, ruler):
        self.__element_positions = []
        for element in self.__elements:
            self.__element_positions.append((element, element.get_position(ruler))) 
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        for element, position in self.__element_positions:
            element.move(ruler, position + self.__delta)
    
    def _undo(self, ruler):
        for element, position in self.__element_positions:
            element.move(ruler, position)
