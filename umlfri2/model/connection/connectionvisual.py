from umlfri2.types.geometry.line import Line


class ConnectionVisual:
    def __init__(self, object, source, destination):
        self.__object = object
        self.__source = source
        self.__destination = destination
        self.__cached_appearance = None
        self.__points = []
    
    def add_point(self, point, index=None):
        if index is None:
            self.__points.append(point)
        else:
            self.__points.insert(index, point)
    
    def draw(self, canvas):
        self.__ensure_appearance_object_exists(canvas.get_ruler())
        
        self.__cached_appearance.draw(canvas)
    
    def __ensure_appearance_object_exists(self, ruler):
        if self.__cached_appearance is None:
            self.__cached_appearance = self.__object.create_appearance_object(ruler)

            source_bounds = self.__source.get_bounds(ruler)
            destination_bounds = self.__destination.get_bounds(ruler)
            
            if self.__points:
                line1 = Line(source_bounds.center, self.__points[0])
                line2 = Line(self.__points[-1], destination_bounds.center)
            else:
                line1 = Line(
                    source_bounds.center,
                    destination_bounds.center
                )
                line2 = line1
            
            
            points = []
            points.extend(source_bounds.intersect(line1))
            points.extend(self.__points)
            points.extend(destination_bounds.intersect(line2))
            
            self.__cached_appearance.assign_points(points)
