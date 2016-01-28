from .initialized import InitializedSnapping


class Snapping:
    MAXIMAL_DISTANCE = 10
    
    def __init__(self, application, elements, connections, selected_elements):
        self.__application = application
        self.__elements = list(elements)
        self.__connections = list(connections)
        self.__selected_elements = set(selected_elements)
        self.__ignored_point = None
        self.__ignore_selection = False
    
    def ignore_point(self, connection, index):
        self.__ignored_point = connection, index
        return self
    
    def ignore_selection(self):
        self.__ignore_selection = True
        return self
    
    def build(self):
        rectangles = []
        points = []
        
        for element in self.__elements:
            if self.__ignore_selection:
                if element in self.__selected_elements:
                    continue
            rectangles.append(element.get_bounds(self.__application.ruler))
        
        for connection in self.__connections:
            for idx, point in enumerate(connection.get_points(self.__application.ruler, False, False)):
                if self.__ignored_point is not None:
                    if self.__ignored_point[1] - 1 == idx and self.__ignored_point[0] is connection:
                        continue
                points.append(point)
        
        return InitializedSnapping(rectangles, points)
