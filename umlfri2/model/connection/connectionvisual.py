from weakref import ref

from ..cache import ModelTemporaryDataCache
from .connectionlabel import ConnectionLabel
from umlfri2.types.geometry import Line, Rectangle, Point


class ConnectionVisual:
    MAXIMAL_CLICKABLE_DISTANCE = 5
    
    def __init__(self, diagram, object, source, destination):
        self.__cache = ModelTemporaryDataCache(self.__create_appearance_object)
        self.__cache.depend_on(source.cache)
        self.__cache.depend_on(destination.cache)
        self.__cache.depend_on(object.cache)
        
        self.__diagram = ref(diagram)
        self.__object = object
        self.__source = ref(source)
        self.__destination = ref(destination)
        self.__cached_appearance = None
        self.__points = []
        self.__cached_points = ()
        self.__labels = [ConnectionLabel(self, label.id) for label in object.type.labels]
    
    @property
    def cache(self):
        return self.__cache
    
    @property
    def object(self):
        return self.__object
    
    @property
    def source(self):
        return self.__source()
    
    @property
    def destination(self):
        return self.__destination()
    
    def _reverse(self):
        self.__source, self.__destination = self.__destination, self.__source
        self.__cache.invalidate()
    
    def get_other_end(self, one_end):
        if self.__source() is one_end:
            return self.__destination()
        elif self.__destination() is one_end:
            return self.__source()
        else:
            return None
    
    @property
    def diagram(self):
        return self.__diagram()
    
    def get_points(self, ruler, source_and_end=True, element_centers=False):
        self.__cache.ensure_valid(ruler=ruler)
        
        if element_centers:
            yield self.__source().get_bounds(ruler).center
            yield from self.__points
            yield self.__destination().get_bounds(ruler).center
        elif source_and_end:
            yield from self.__cached_points
        else:
            yield from self.__points
    
    @property
    def number_of_points_on_line(self):
        return len(self.__points)
    
    @property
    def is_identity(self):
        return self.__source() is self.__destination()
    
    def get_labels(self):
        yield from self.__labels
    
    def get_label(self, id):
        for label in self.__labels:
            if label.id == id:
                return label
    
    def add_point(self, ruler, index, point):
        if index is None:
            index = len(self.__points) + 1
        elif index < 1 or index > len(self.__points) + 1:
            raise Exception("Point index out of range")
        
        self.__points.insert(index - 1, point)
        
        self.__cache.refresh(ruler=ruler)
        
        line1_length = (self.__cached_points[index] - self.__cached_points[index - 1]).length
        line2_length = (self.__cached_points[index + 1] - self.__cached_points[index]).length
        
        for label in self.__labels:
            label._adding_point(index - 1, line1_length, line2_length)
    
    def move_point(self, ruler, index, point):
        if index < 1 or index > len(self.__points):
            raise Exception("Point index out of range")
        
        self.__points[index - 1] = point
        
        self.__cache.invalidate()
    
    def remove_point(self, ruler, index):
        if index < 1 or index > len(self.__points):
            raise Exception("Point index out of range")
        
        self.__cache.ensure_valid(ruler=ruler)
        
        line1_length = (self.__cached_points[index] - self.__cached_points[index - 1]).length
        line2_length = (self.__cached_points[index + 1] - self.__cached_points[index]).length
        
        del self.__points[index - 1]
        
        for label in self.__labels:
            label._removing_point(index - 1, line1_length, line2_length)
        
        self.__cache.invalidate()
    
    def draw(self, canvas):
        self.__cache.ensure_valid(ruler=canvas.get_ruler())
        
        self.__cached_appearance.draw(canvas)
        
        for label in self.__labels:
            label.draw(canvas)
    
    def is_at_position(self, ruler, position):
        self.__cache.ensure_valid(ruler=ruler)
        
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
        self.__cache.ensure_valid(ruler=ruler)
        
        return self.__cached_points[id]
    
    def __create_appearance_object(self, ruler):
        self.__cached_appearance = self.__object.create_appearance_object(ruler)

        source_bounds = self.__source().get_bounds(ruler)
        destination_bounds = self.__destination().get_bounds(ruler)
        
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
        points.append(self.__get_common_point(line1, source_bounds, line1.second))
        points.extend(self.__points)
        points.append(self.__get_common_point(line2, destination_bounds, line2.first))
        
        self.__cached_appearance.assign_points(points)
        
        self.__cached_points = tuple(points)

    def __get_common_point(self, line_component, object_bounds, point):
        for point in object_bounds.intersect(line_component):
            return point
        
        return object_bounds.get_nearest_point_to(point)

    def get_bounds(self, ruler):
        self.__cache.ensure_valid(ruler=ruler)
        
        x1 = y1 = float('inf')
        x2 = y2 = -float('inf')
        
        for point in self.__cached_points:
            if point.x < x1:
                x1 = point.x
            if point.x > x2:
                x2 = point.x
            if point.y < y1:
                y1 = point.y
            if point.y > y2:
                y2 = point.y
        
        for label in self.__labels:
            bounds = label.get_bounds(ruler)
            
            if bounds.x1 < x1:
                x1 = bounds.x1
            if bounds.x2 > x2:
                x2 = bounds.x2
            if bounds.y1 < y1:
                y1 = bounds.y1
            if bounds.y2 > y2:
                y2 = bounds.y2
        
        return Rectangle.from_point_point(Point(x1, y1), Point(x2, y2))
