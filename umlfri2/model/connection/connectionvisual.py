from umlfri2.types.geometry.line import Line


class ConnectionVisual:
    MAXIMAL_CLICKABLE_DISTANCE = 3
    
    def __init__(self, object, source, destination):
        self.__object = object
        self.__source = source
        self.__destination = destination
        self.__cached_appearance = None
        self.__points = []
        self.__cached_points = []
    
    @property
    def object(self):
        return self.__object
    
    def add_point(self, point, index=None):
        if index is None:
            self.__points.append(point)
        else:
            self.__points.insert(index, point)
    
    def draw(self, canvas):
        self.__ensure_appearance_object_exists(canvas.get_ruler())
        
        self.__cached_appearance.draw(canvas)
    
    def is_at_position(self, ruler, position):
        self.__ensure_appearance_object_exists(ruler)
        
        old_point = None
        for point in self.__cached_points:
            if old_point is not None:
                if Line(old_point, point).get_distance_to(position) <= self.MAXIMAL_CLICKABLE_DISTANCE:
                    return True
            old_point = point
        
        return False
    
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
            
            self.__cached_points = points
