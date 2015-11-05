from weakref import ref
import math
from umlfri2.types.geometry import Point, Vector, Rectangle


class ConnectionLabel:
    def __init__(self, connection, id):
        self.__connection = ref(connection)
        self.__id = id
        self.__cached_appearance = None
        self.__line_index = 0
        self.__line_position = connection.object.type.get_label(id).position
        self.__angle = math.pi/2
        self.__distance = 0
    
    @property
    def connection(self):
        return self.__connection
    
    @property
    def id(self):
        return self.__id
    
    @property
    def line_index(self):
        return self.__line_index
    
    def _adding_point(self, line_index, line1_length, line2_length):
        if line_index > self.__line_index:
            self.__line_index += 1
            self.__cached_appearance = None
        elif line_index == self.__line_index:
            proportions = line1_length / (line1_length + line2_length)
            new_position = self.__line_position / proportions
            
            if new_position < 1:
                self.__line_position = new_position
            else:
                self.__line_index += 1
                self.__line_position = new_position - 1
            self.__cached_appearance = None
    
    def get_bounds(self, ruler):
        self.__ensure_appearance_object_exists(ruler)
        
        return Rectangle.from_point_size(self.__cached_appearance.position, self.__cached_appearance.size)
    
    def is_at_position(self, ruler, position):
        return self.get_bounds(ruler).contains(position)
    
    def draw(self, canvas):
        self.__ensure_appearance_object_exists(canvas.get_ruler())
        
        self.__cached_appearance.draw(canvas)

    def __ensure_appearance_object_exists(self, ruler):
        if self.__cached_appearance is None:
            self.__cached_appearance = self.__connection().object.create_label_object(self.__id, ruler)
            first_point = self.__connection().get_point(ruler, self.__line_index)
            second_point = self.__connection().get_point(ruler, self.__line_index + 1)
            
            line_vector = second_point - first_point
            
            vector_to_label = Vector.from_angle_length(line_vector.angle + self.__angle, self.__distance)
            
            position = first_point\
                       + line_vector * self.__line_position\
                       + vector_to_label\
                       - self.__cached_appearance.size.as_vector() / 2
            
            self.__cached_appearance.move(position)
