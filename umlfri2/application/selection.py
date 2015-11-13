from umlfri2.model.connection import ConnectionVisual
from umlfri2.model.element import ElementVisual
from umlfri2.types.color import Colors
from umlfri2.types.geometry import Rectangle, Vector, Size


class SelectionPointPosition:
    First = 0
    Center = 1
    Last = 2


class Selection:
    SELECTION_COLOR = Colors.blue
    SELECTION_SIZE = 2
    
    SELECTION_POINT_COLOR = Colors.darkgray
    SELECTION_POINT_SIZE = 8
    
    def __init__(self):
        self.__selected = set()
    
    def select(self, visual):
        self.__selected.clear()
        if visual is not None:
            self.__selected.add(visual)
            
    def deselect_all(self):
        self.__selected.clear()
    
    def add_to_selection(self, visual):
        self.__selected.add(visual)
    
    def remove_from_selection(self, visual):
        self.__selected.remove(visual)
    
    def toggle_select(self, visual):
        if visual in self.__selected:
            self.__selected.remove(visual)
        else:
            self.__selected.add(visual)
    
    def draw_for(self, canvas, visual):
        if visual not in self.__selected:
            return
        
        if isinstance(visual, ElementVisual):
            bounds = visual.get_bounds(canvas.get_ruler())
            
            if len(self.__selected) == 1:
                resizable_x, resizable_y = visual.is_resizable(canvas.get_ruler())
                
                if resizable_x and resizable_y:
                    self.__draw_selection_point(canvas, bounds, SelectionPointPosition.First, SelectionPointPosition.First)
                    self.__draw_selection_point(canvas, bounds, SelectionPointPosition.First, SelectionPointPosition.Last)
                    self.__draw_selection_point(canvas, bounds, SelectionPointPosition.Last, SelectionPointPosition.First)
                    self.__draw_selection_point(canvas, bounds, SelectionPointPosition.Last, SelectionPointPosition.Last)
                
                if resizable_x:
                    self.__draw_selection_point(canvas, bounds, SelectionPointPosition.First, SelectionPointPosition.Center)
                    self.__draw_selection_point(canvas, bounds, SelectionPointPosition.Last, SelectionPointPosition.Center)
                
                if resizable_y:
                    self.__draw_selection_point(canvas, bounds, SelectionPointPosition.Center, SelectionPointPosition.First)
                    self.__draw_selection_point(canvas, bounds, SelectionPointPosition.Center, SelectionPointPosition.Last)
            
            canvas.draw_rectangle(bounds, fg=self.SELECTION_COLOR, line_width=self.SELECTION_SIZE)
        elif isinstance(visual, ConnectionVisual):
            if len(self.__selected) == 1:
                fg_color = None
                bg_color = self.SELECTION_POINT_COLOR
            else:
                fg_color = self.SELECTION_POINT_COLOR
                bg_color = None
            
            for point in visual.get_points(canvas.get_ruler()):
                canvas.draw_rectangle(
                    Rectangle.from_point_size(
                        point-Vector(self.SELECTION_POINT_SIZE//2, self.SELECTION_POINT_SIZE//2),
                        Size(self.SELECTION_POINT_SIZE, self.SELECTION_POINT_SIZE)
                    ),
                    fg=fg_color, bg=bg_color
                )
            
            for label in visual.get_labels():
                bounds = label.get_bounds(canvas.get_ruler())
                canvas.draw_rectangle(bounds, fg=self.SELECTION_POINT_COLOR, line_width=self.SELECTION_SIZE)
    
    def __draw_selection_point(self, canvas, bounds, pos_x, pos_y):
        x1, x2 = self.__compute_selection_point_position(pos_x, bounds.x1, bounds.width)
        y1, y2 = self.__compute_selection_point_position(pos_y, bounds.y1, bounds.height)
        
        canvas.draw_rectangle(Rectangle(x1, y1, x2 - x1, y2 - y1), bg=self.SELECTION_POINT_COLOR)

    def __compute_selection_point_position(self, pos, start, size):
        if pos == SelectionPointPosition.First:
            return start, start + self.SELECTION_POINT_SIZE
        elif pos == SelectionPointPosition.Center:
            return start + size // 2 - self.SELECTION_POINT_SIZE // 2, start + size // 2 + self.SELECTION_POINT_SIZE // 2
        elif pos == SelectionPointPosition.Last:
            return start + size - self.SELECTION_POINT_SIZE, start + size
        
