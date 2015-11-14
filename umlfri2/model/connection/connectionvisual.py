from .connectionlabel import ConnectionLabel
from umlfri2.types.geometry.line import Line


class ConnectionVisual:
    MAXIMAL_CLICKABLE_DISTANCE = 5
    
    def __init__(self, object, source, destination):
        self.__object = object
        self.__source = source
        self.__destination = destination
        self.__cached_appearance = None
        self.__points = []
        self.__cached_points = ()
        self.__labels = [ConnectionLabel(self, label.id) for label in object.type.labels]
        
        self.__source_version = source.version
        self.__destination_version = destination.version
    
    @property
    def object(self):
        return self.__object
    
    def get_points(self, ruler):
        self.__ensure_appearance_object_exists(ruler)
        
        yield from self.__cached_points
    
    def get_labels(self):
        yield from self.__labels
    
    def add_point(self, ruler, point, index=None):
        if index is None:
            index = len(self.__points)
        
        self.__points.insert(index, point)
        
        self.__cached_appearance = None
        
        self.__ensure_appearance_object_exists(ruler)
        
        line1_length = (self.__cached_points[index + 1] - self.__cached_points[index]).length
        line2_length = (self.__cached_points[index + 2] - self.__cached_points[index + 1]).length
        
        for label in self.__labels:
            label._adding_point(index, line1_length, line2_length)
    
    def draw(self, canvas):
        self.__ensure_appearance_object_exists(canvas.get_ruler())
        
        self.__cached_appearance.draw(canvas)
        
        for label in self.__labels:
            label.draw(canvas)
    
    def is_at_position(self, ruler, position):
        self.__ensure_appearance_object_exists(ruler)
        
        old_point = None
        for point in self.__cached_points:
            if old_point is not None:
                distance = Line.from_point_point(old_point, point).get_distance_to(position)
                if distance <= self.MAXIMAL_CLICKABLE_DISTANCE:
                    return True
            old_point = point
        
        for label in self.__labels:
            if label.is_at_position(ruler, position):
                return True
        
        return False
    
    def get_point(self, ruler, id):
        self.__ensure_appearance_object_exists(ruler)
        
        return self.__cached_points[id]
    
    def invalidate(self):
        self.__cached_appearance = None
    
    def __ensure_appearance_object_exists(self, ruler):
        source_changed = self.__source_version != self.__source.version
        destination_changed = self.__destination.version != self.__destination_version
        
        if self.__cached_appearance is None or source_changed or destination_changed:
            self.__cached_appearance = self.__object.create_appearance_object(ruler)

            source_bounds = self.__source.get_bounds(ruler)
            destination_bounds = self.__destination.get_bounds(ruler)
            
            if self.__points:
                line1 = Line.from_point_point(source_bounds.center, self.__points[0])
                line2 = Line.from_point_point(self.__points[-1], destination_bounds.center)
            else:
                line1 = Line.from_point_point(
                    source_bounds.center,
                    destination_bounds.center
                )
                line2 = line1
            
            
            points = []
            points.extend(source_bounds.intersect(line1))
            points.extend(self.__points)
            points.extend(destination_bounds.intersect(line2))
            
            self.__cached_appearance.assign_points(points)
            
            self.__cached_points = tuple(points)
    
    def get_bounds(self, ruler):
        return None # TODO
