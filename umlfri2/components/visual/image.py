from umlfri2.types.geometry import Rectangle
from umlfri2.ufl.types import UflImageType
from .visualcomponent import VisualComponent, VisualObject


class ImageObject(VisualObject):
    def __init__(self, size, image):
        self.__position = None
        self.__size = size
        self.__image = image
    
    def assign_bounds(self, bounds):
        self.__position = bounds.top_left
    
    def get_minimal_size(self):
        return self.__size
            
    def draw(self, canvas, shadow):
        if shadow:
            canvas.draw_rectangle(
                Rectangle.from_point_size(self.__position, self.__size),
                None,
                shadow.color
            )
        else:
            canvas.draw_image(self.__position, self.__image)
    
    def is_resizable(self):
        return False, False


class ImageComponent(VisualComponent):
    ATTRIBUTES = {
        'image': UflImageType(),
    }
    HAS_CHILDREN = False
    
    def __init__(self, image): 
        super().__init__(())
        self.__image = image
    
    def _create_object(self, context, ruler):
        image = self.__image(context)
        size = ruler.measure_image(image)
        return ImageObject(size, image)
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            image=self.__image
        )