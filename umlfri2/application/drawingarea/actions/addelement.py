from umlfri2.application.commands.diagram import AddDiagramElementCommand
from .action import Action


class AddElementAction(Action):
    def __init__(self, type):
        super().__init__()
        self.__type = type
        self.__point = None
    
    def mouse_down(self, drawing_area, application, point):
        self.__point = point
    
    def mouse_up(self, drawing_area, application):
        type = drawing_area.diagram.parent.project.metamodel.get_element_type(self.__type)
        command = AddDiagramElementCommand(
            drawing_area.diagram,
            type,
            self.__point
        )
        application.commands.execute(command)
        self._finish()
