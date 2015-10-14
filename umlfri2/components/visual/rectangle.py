from umlfri2.types.color import Color
from .visualcomponent import VisualComponent, VisualObject


class RectangleObject(VisualObject):
    def __init__(self, child, fill, border):
        self.__child = child
        self.__fill = fill
        self.__border = border
        
        self.__child_size = child.get_minimal_size()
    
    def assign_bounds(self, bounds):
        self.__position = bounds[0], bounds[1]
        self.__size = bounds[2], bounds[3]
        
        self.__child.assign_bounds(bounds)
    
    def get_minimal_size(self):
        return self.__child_size
    
    def draw(self, canvas, shadow):
        if shadow:
            x, y = self.__position
            canvas.draw_rectangle(
                (x + shadow.shift, y + shadow.shift),
                self.__size,
                None,
                shadow.color
            )
        else:
            canvas.draw_rectangle(self.__position, self.__size, self.__border, self.__fill)
            self.__child.draw(canvas, None)


class Rectangle(VisualComponent):
    def __init__(self, children, fill: Color=None, border: Color=None):
        super().__init__(children)
        self.__fill = fill
        self.__border = border
    
    def _create_object(self, context, ruler):
        for local, child in self._get_children(context):
            return RectangleObject(
                child._create_object(local, ruler),
                self.__fill(local),
                self.__border(local)
            )
