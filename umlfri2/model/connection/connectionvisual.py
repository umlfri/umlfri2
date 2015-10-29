class ConnectionVisual:
    def __init__(self, object, source, destination):
        self.__object = object
        self.__source = source
        self.__destination = destination
        self.__cached_appearance = None
        self.__points = []
    
    def draw(self, canvas):
        self.__ensure_appearance_object_exists(canvas.get_ruler())
        
        self.__cached_appearance.draw(canvas)
    
    def __ensure_appearance_object_exists(self, ruler):
        if self.__cached_appearance is None:
            self.__cached_appearance = self.__object.create_appearance_object(ruler)
            
            points = [self.__source.get_bounds(ruler).center]
            points.extend(self.__points)
            points.append(self.__destination.get_bounds(ruler).center)
            
            self.__cached_appearance.assign_points(points)
