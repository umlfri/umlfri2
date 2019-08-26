from umlfri2.model.element import ElementVisual
from umlfri2.types.geometry import PathBuilder, Point
from .action import Action


class AddConnectionAction(Action):
    def __init__(self):
        super().__init__()
        self.__path = None
        self.__source_element = None
        self.__points = []
        self.__first_point = None
        self.__last_point = None
        self.__snapping = None
        self.__snapped = None
    
    @property
    def path(self):
        return self.__path
    
    @property
    def horizontal_snapping_indicators(self):
        if self.__snapped is not None:
            yield from self.__snapped.horizontal_indicators
    
    @property
    def vertical_snapping_indicators(self):
        if self.__snapped is not None:
            yield from self.__snapped.vertical_indicators
    
    def snap_to(self, snapping):
        self.__snapping = snapping.build()
    
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
                    self._create_connection(self.__source_element, element, self.__points)
                    self._finish()
                else:
                    if self.__snapping is not None:
                        self.__snapped = self.__snapping.snap_point(point)
                        point = self.__snapped.point
                        self.__snapping.add_point(point)
                    else:
                        self.__snapped = None
                    
                    self.__points.append(point)
                    self.__last_point = None
                    self.__build_path()
    
    def mouse_move(self, point):
        if self.__source_element is not None:
            x, y = point.x, point.y
            
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            
            point = Point(x, y)
            
            if self.__snapping is not None:
                self.__snapped = self.__snapping.snap_point(point)
                point = self.__snapped.point
            else:
                self.__snapped = None
            
            self.__last_point = point
            self.__build_path()
    
    def mouse_up(self):
        if self.__last_point is not None:
            element = self.drawing_area.diagram.get_visual_at(self.application.ruler, self.__last_point)
            if self.__source_element is not element and not self.__points and isinstance(element, ElementVisual):
                self._create_connection(self.__source_element, element, self.__points)
                self._finish()
    
    def _create_connection(self, source_element, destination_element, points):
        raise NotImplementedError
    
    def __build_path(self):
        path = PathBuilder()
        
        path.move_to(self.__first_point)
        
        for point in self.__points:
            path.line_to(point)
        
        if self.__last_point is not None:
            path.line_to(self.__last_point)
        
        self.__path = path.build()
