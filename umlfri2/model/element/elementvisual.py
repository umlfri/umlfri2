class ElementVisual:
    def __init__(self, object):
        self.__object = object
        self.__cached_visual = None
        self.__position = (0, 0)
        self.__size = None
    
    @property
    def object(self):
        return self.__object
    
    @property
    def position(self):
        return self.__position
    
    @property
    def size(self):
        return self.__size
    
    def draw(self, canvas):
        self.__ensure_visual_object_exists(canvas.get_ruler())
        
        self.__cached_visual.draw(canvas)

    def resize(self, ruler, new_size):
        self.__ensure_visual_object_exists(ruler)
        
        w_min, h_min = self.__cached_visual.get_minimal_size()
        w_new, h_new = new_size
        
        if w_new < w_min:
            w_new = w_min
        
        if h_new < h_min:
            h_new = h_min
        
        new_size = w_new, h_new
        
        self.__cached_visual.resize(new_size)
        self.__size = new_size
    
    def move(self, ruler, new_position):
        self.__ensure_visual_object_exists(ruler)
        
        self.__cached_visual.move(new_position)
        self.__position = new_position

    def __ensure_visual_object_exists(self, ruler):
        if self.__cached_visual is None:
            self.__cached_visual = self.__object.create_visual_object(ruler)
            self.__cached_visual.move(self.__position)
            if self.__size is None:
                self.__size = self.__cached_visual.get_minimal_size()
            else:
                self.__cached_visual.resize(self.__size)
