from umlfri2.types.geometry import Point, Rectangle, Size


class ElementVisual:
    def __init__(self, object):
        self.__object = object
        self.__cached_appearance = None
        self.__position = Point(0, 0)
        self.__size = None
    
    @property
    def object(self):
        return self.__object
    
    def get_position(self, ruler):
        self.__ensure_appearance_object_exists(ruler)
        
        return self.__position
    
    def get_size(self, ruler):
        self.__ensure_appearance_object_exists(ruler)
        
        return self.__size
    
    def get_bounds(self, ruler):
        self.__ensure_appearance_object_exists(ruler)
        
        return Rectangle.from_point_size(self.__position, self.__size)
    
    def draw(self, canvas):
        self.__ensure_appearance_object_exists(canvas.get_ruler())
        
        self.__cached_appearance.draw(canvas)

    def resize(self, ruler, new_size):
        self.__ensure_appearance_object_exists(ruler)
        
        min_size = self.__cached_appearance.get_minimal_size()
        w_min = min_size.width
        h_min = min_size.height 
        w_new = new_size.width
        h_new = new_size.height
        
        if w_new < w_min:
            w_new = w_min
        
        if h_new < h_min:
            h_new = h_min
        
        new_size = Size(w_new, h_new)
        
        self.__cached_appearance.resize(new_size)
        self.__size = new_size
    
    def move(self, ruler, new_position):
        self.__ensure_appearance_object_exists(ruler)
        
        self.__cached_appearance.move(new_position)
        self.__position = new_position
    
    def is_at_position(self, ruler, position):
        return self.get_bounds(ruler).contains(position)
    
    def is_resizable(self, ruler):
        # TODO: 3-state resizable indication
        self.__ensure_appearance_object_exists(ruler)
        
        return self.__cached_appearance.is_resizable()

    def __ensure_appearance_object_exists(self, ruler):
        if self.__cached_appearance is None:
            self.__cached_appearance = self.__object.create_appearance_object(ruler)
            self.__cached_appearance.move(self.__position)
            if self.__size is None:
                self.__size = self.__cached_appearance.get_minimal_size()
            else:
                self.__cached_appearance.resize(self.__size)
