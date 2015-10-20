class ElementVisual:
    def __init__(self, object):
        self.__object = object
        self.__old_visual = None
    
    @property
    def object(self):
        return self.__object
    
    def draw(self, canvas):
        if self.__old_visual is None:
            self.__old_visual = self.__object.create_visual_object(canvas.get_ruler())
        
        self.__old_visual.draw(canvas)
    
    def resize(self, ruler, new_size):
        if self.__old_visual is None:
            self.__old_visual = self.__object.create_visual_object(ruler)
        
        self.__old_visual.resize(new_size)
    
    def move(self, ruler, new_position):
        if self.__old_visual is None:
            self.__old_visual = self.__object.create_visual_object(ruler)
        
        self.__old_visual.move(new_position)
