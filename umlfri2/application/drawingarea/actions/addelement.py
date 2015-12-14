from umlfri2.application.commands.diagram import AddDiagramElementCommand
from .action import Action


class AddElementAction(Action):
    def __init__(self, type):
        super().__init__()
        self.__type = type
        self.__point = None
    
    def mouse_down(self, point):
        self.__point = point
    
    def mouse_up(self):
        type = self.drawing_area.diagram.parent.project.metamodel.get_element_type(self.__type)
        command = AddDiagramElementCommand(
            self.drawing_area.diagram,
            type,
            self.__point
        )
        self.application.commands.execute(command)
        self.drawing_area.selection.select(command.element_visual)
        self._finish()
