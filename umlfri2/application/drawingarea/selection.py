from umlfri2.components.visual.canvas import LineStyle
from .selectionpointposition import SelectionPointPosition
from umlfri2.model.connection import ConnectionVisual
from umlfri2.model.element import ElementVisual
from umlfri2.types.color import Colors
from umlfri2.types.geometry import Rectangle, Vector, Size, Line
from .actions import MoveSelectionAction, ResizeElementAction, MoveConnectionPointAction, MoveConnectionLabelAction, \
    RemoveConnectionPointAction, AddConnectionPointAction


class Selection:
    SELECTION_COLOR = Colors.blue
    SELECTION_SIZE = 2
    
    SELECTION_POINT_COLOR = Colors.darkgray
    SELECTION_POINT_SIZE = 8
    
    LABEL_LINE_MINIMAL_DISTANCE = 10
    
    def __init__(self, diagram):
        self.__selected = set()
        self.__diagram = diagram
    
    @property
    def selected_visuals(self):
        yield from self.__selected
    
    @property
    def selected_elements(self):
        for visual in self.__selected:
            if isinstance(visual, ElementVisual):
                yield visual
    
    @property
    def selected_connections(self):
        for visual in self.__selected:
            if isinstance(visual, ConnectionVisual):
                yield visual
    
    @property
    def diagram(self):
        return self.__diagram
    
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
    
    def select_in_area(self, ruler, area):
        self.__selected.clear()
        for element in self.__diagram.elements:
            if element.get_bounds(ruler).is_overlapping(area):
                self.__selected.add(element)
    
    def draw_for(self, canvas, visual):
        if visual not in self.__selected:
            return
        
        if isinstance(visual, ElementVisual):
            bounds = visual.get_bounds(canvas.get_ruler())
            
            if len(self.__selected) == 1:
                for pos_x, pos_y in self.__get_selection_points_positions(canvas.get_ruler(), visual):
                    self.__draw_selection_point(canvas, bounds, pos_x, pos_y)
            
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
                        point - Vector(self.SELECTION_POINT_SIZE // 2, self.SELECTION_POINT_SIZE // 2),
                        Size(self.SELECTION_POINT_SIZE, self.SELECTION_POINT_SIZE)
                    ),
                    fg=fg_color, bg=bg_color
                )
            
            for label in visual.get_labels():
                bounds = label.get_bounds(canvas.get_ruler())
                if bounds.width and bounds.height:
                    canvas.draw_rectangle(bounds, fg=self.SELECTION_COLOR, line_width=self.SELECTION_SIZE)
                    line_to_connection = Line.from_point_point(
                        label.get_nearest_point(canvas.get_ruler()),
                        bounds.center
                    )
                    intersect = list(bounds.intersect(line_to_connection))
                    if intersect and (line_to_connection.first-intersect[0]).length > self.LABEL_LINE_MINIMAL_DISTANCE:
                        canvas.draw_line(line_to_connection.first, intersect[0], fg=self.SELECTION_COLOR,
                                         line_width=self.SELECTION_SIZE, line_style=LineStyle.dot)
    
    def __get_selection_points_positions(self, ruler, visual):
        resizable_x, resizable_y = visual.is_resizable(ruler)
        
        if resizable_x and resizable_y:
            yield SelectionPointPosition.first, SelectionPointPosition.first
            yield SelectionPointPosition.first, SelectionPointPosition.last
            yield SelectionPointPosition.last, SelectionPointPosition.first
            yield SelectionPointPosition.last, SelectionPointPosition.last
        
        if resizable_x:
            yield SelectionPointPosition.first, SelectionPointPosition.center
            yield SelectionPointPosition.last, SelectionPointPosition.center
        
        if resizable_y:
            yield SelectionPointPosition.center, SelectionPointPosition.first
            yield SelectionPointPosition.center, SelectionPointPosition.last
    
    def __draw_selection_point(self, canvas, bounds, pos_x, pos_y):
        canvas.draw_rectangle(self.__get_selection_point(bounds, pos_x, pos_y), bg=self.SELECTION_POINT_COLOR)

    def __get_selection_point(self, bounds, pos_x, pos_y):
        x1, x2 = self.__compute_selection_point_position(pos_x, bounds.x1, bounds.width)
        y1, y2 = self.__compute_selection_point_position(pos_y, bounds.y1, bounds.height)
        return Rectangle(x1, y1, x2 - x1, y2 - y1)

    def __compute_selection_point_position(self, pos, start, size):
        if pos == SelectionPointPosition.first:
            return start, start + self.SELECTION_POINT_SIZE
        elif pos == SelectionPointPosition.center:
            return start + size // 2 - self.SELECTION_POINT_SIZE // 2, start + size // 2 + self.SELECTION_POINT_SIZE // 2
        elif pos == SelectionPointPosition.last:
            return start + size - self.SELECTION_POINT_SIZE, start + size
    
    def get_action_at(self, ruler, position, shift_pressed):
        visual = self.__diagram.get_visual_at(ruler, position)
        
        if visual not in self.__selected:
            return None
        
        if len(self.__selected) > 1:
            if shift_pressed:
                return None
            else:
                return MoveSelectionAction()
        
        if isinstance(visual, ElementVisual):
            bounds = visual.get_bounds(ruler)
            for pos_x, pos_y in self.__get_selection_points_positions(ruler, visual):
                if self.__get_selection_point(bounds, pos_x, pos_y).contains(position):
                    if shift_pressed:
                        return None
                    else:
                        return ResizeElementAction(visual, pos_x, pos_y)
            if shift_pressed:
                return None
            else:
                return MoveSelectionAction()
        elif isinstance(visual, ConnectionVisual):
            found = None
            for idx, point in enumerate(visual.get_points(ruler)):
                if idx > 0: # don't return it for first point
                    if (position - point).length < ConnectionVisual.MAXIMAL_CLICKABLE_DISTANCE:
                        found = idx
                    elif found is not None: # don't return it for last point
                        if shift_pressed:
                            return RemoveConnectionPointAction(visual, found)
                        else:
                            return MoveConnectionPointAction(visual, found)
            
            for label in visual.get_labels():
                if label.get_bounds(ruler).contains(position):
                    if shift_pressed:
                        return None
                    else:
                        return MoveConnectionLabelAction(visual, label.id)
            
            if shift_pressed:
                last = None
                for idx, point in enumerate(visual.get_points(ruler)):
                    if last is not None:
                        distance = Line.from_point_point(last, point).get_distance_to(position)
                        if distance < ConnectionVisual.MAXIMAL_CLICKABLE_DISTANCE:
                            return AddConnectionPointAction(visual, idx)
                    last = point
        
        return None
    
    def get_bounds(self, ruler):
        x1 = float('inf')
        x2 = -float('inf')
        y1 = float('inf')
        y2 = -float('inf')
        
        for visual in self.__selected:
            if isinstance(visual, ElementVisual):
                bounds = visual.get_bounds(ruler)
                if bounds.x1 < x1:
                    x1 = bounds.x1
                if bounds.y1 < y1:
                    y1 = bounds.y1
                if bounds.x2 > x2:
                    x2 = bounds.x2
                if bounds.y2 > y2:
                    y2 = bounds.y2
        
        return Rectangle(x1, y1, x2 - x1, y2 - y1)