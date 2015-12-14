from umlfri2.application.commands.diagram.adddiagramconnection import AddDiagramConnectionCommand
from umlfri2.model.element import ElementVisual
from umlfri2.types.geometry import PathBuilder
from .action import Action


class AddConnectionAction(Action):
    def __init__(self, type):
        super().__init__()
        self.__type = type
        self.__path = None
        self.__source_element = None
        self.__points = []
        self.__first_point = None
        self.__last_point = None
    
    @property
    def path(self):
        return self.__path
    
    def mouse_down(self, point):
        if self.__source_element is None:
            element = self.drawing_area.diagram.get_visual_at(self.application.ruler, point)
            if isinstance(element, ElementVisual):
                self.__first_point = element.get_bounds(self.application.ruler).center
                self.__build_path()
                self.__source_element = element
            else:
                self._finish()
        else:
            element = self.drawing_area.diagram.get_visual_at(self.application.ruler, point)
            if self.__source_element is not element or self.__points: 
                if isinstance(element, ElementVisual):
                    type = self.drawing_area.diagram.parent.project.metamodel.get_connection_type(self.__type)
                    command = AddDiagramConnectionCommand(
                        self.drawing_area.diagram,
                        type,
                        self.__source_element,
                        element,
                        self.__points
                    )
                    self.application.commands.execute(command)
                    self.drawing_area.selection.select(command.connection_visual)
                    self._finish()
                else:
                    self.__points.append(point)
                    self.__last_point = None
                    self.__build_path()
    
    def mouse_move(self, point):
        if self.__source_element is not None:
            self.__last_point = point
            self.__build_path()
    
    def mouse_up(self):
        pass
    
    def __build_path(self):
        path = PathBuilder()
        
        path.move_to(self.__first_point)
        
        for point in self.__points:
            path.line_to(point)
        
        if self.__last_point is not None:
            path.line_to(self.__last_point)
        
        self.__path = path.build()
