from umlfri2.types.color import Colors
from .commands.diagram import MoveSelectionCommand, ResizeMoveElementCommand
from umlfri2.types.geometry import Rectangle
from .selection import Selection, ActionMoveSelection, ActionResizeElement, ActionSelectMany, SelectionPointPosition, \
    ActionMoveConnectionPoint, ActionMoveLabel


class DrawingAreaCursor:
    arrow = 0
    move = 1
    mainDiagonalResize = 2
    antiDiagonalResize = 3
    horizontalResize = 4
    verticalResize = 5


class DrawingArea:
    SELECTION_RECTANGLE_FILL = Colors.blue.add_alpha(5)
    SELECTION_RECTANGLE_BORDER = Colors.blue
    SELECTION_RECTANGLE_WIDTH = 3
    
    def __init__(self, application, diagram):
        self.__diagram = diagram
        self.__selection = Selection(self.__diagram)
        self.__application = application
        self.__postponed_action = None
        self.__current_action = None
        self.__current_action_point = None
        self.__current_action_bounds = None
        self.__cursor = DrawingAreaCursor.arrow
    
    @property
    def diagram(self):
        return self.__diagram
    
    @property
    def cursor(self):
        return self.__cursor
    
    def draw(self, canvas):
        self.__diagram.draw(canvas, self.__selection)
        if self.__current_action is not None:
            if self.__current_action_bounds is not None:
                canvas.draw_rectangle(
                    self.__current_action_bounds,
                    self.SELECTION_RECTANGLE_BORDER,
                    self.SELECTION_RECTANGLE_FILL,
                    self.SELECTION_RECTANGLE_WIDTH
                )
    
    def mouse_down(self, point, control_pressed):
        action = self.__selection.get_action_at(self.__application.ruler, point)
        
        if action is not None:
            self.__start_action(action, point)
        else:
            object = self.__diagram.get_visual_at(self.__application.ruler, point)
            
            if control_pressed:
                if object is not None:
                    self.__selection.toggle_select(object)
            else:
                self.__selection.select(object)
                action = self.__selection.get_action_at(self.__application.ruler, point)
                
                if action is None:
                    action = ActionSelectMany()
                self.__start_action(action, point)
                self.__postpone_action()
        
        self.__change_cursor(point)
    
    def mouse_move(self, point):
        if self.__is_in_action():
            self.__process_action(point)
        else:
            self.__change_cursor(point)
    
    def mouse_up(self):
        if self.__is_in_action():
            self.__finish_action()

    def __change_cursor(self, point):
        action = self.__selection.get_action_at(self.__application.ruler, point)
        if isinstance(action, ActionMoveSelection):
            self.__cursor = DrawingAreaCursor.move
        elif isinstance(action, ActionResizeElement):
            if action.horizontal == action.vertical:
                self.__cursor = DrawingAreaCursor.mainDiagonalResize
            elif action.horizontal == SelectionPointPosition.center:
                self.__cursor = DrawingAreaCursor.verticalResize
            elif action.vertical == SelectionPointPosition.center:
                self.__cursor = DrawingAreaCursor.horizontalResize
            elif action.horizontal != action.vertical:
                self.__cursor = DrawingAreaCursor.antiDiagonalResize
        elif isinstance(action, ActionMoveConnectionPoint):
            self.__cursor = DrawingAreaCursor.move
        elif isinstance(action, ActionMoveLabel):
            self.__cursor = DrawingAreaCursor.move
        else:
            self.__cursor = DrawingAreaCursor.arrow
    
    def __start_action(self, action, point):
        self.__current_action = action
        if isinstance(self.__current_action, ActionMoveSelection):
            self.__current_action_bounds = self.__selection.get_bounds(self.__application.ruler)
        elif isinstance(self.__current_action, ActionResizeElement):
            self.__current_action_bounds = self.__current_action.element.get_bounds(self.__application.ruler)
        elif isinstance(self.__current_action, ActionSelectMany):
            self.__current_action_bounds = Rectangle.from_point_point(point, point)
        
        self.__current_action_point = point
    
    def __is_in_action(self):
        return self.__current_action is not None or self.__postponed_action is not None
    
    def __postpone_action(self):
        self.__postponed_action = self.__current_action
        self.__current_action = None
    
    def __process_action(self, point):
        if self.__postponed_action is not None:
            self.__current_action = self.__postponed_action
            self.__postponed_action = None
        
        vector = point - self.__current_action_point
        
        if isinstance(self.__current_action, ActionMoveSelection):
            self.__current_action_bounds += vector
        elif isinstance(self.__current_action, ActionResizeElement):
            x1 = self.__current_action_bounds.x1
            y1 = self.__current_action_bounds.y1
            x2 = self.__current_action_bounds.x2
            y2 = self.__current_action_bounds.y2
            
            min_size = self.__current_action.element.get_minimal_size(self.__application.ruler)
            
            if self.__current_action.horizontal == SelectionPointPosition.first:
                x1 += vector.x
                if x2 - x1 < min_size.width:
                    x1 = x2 - min_size.width
            elif self.__current_action.horizontal == SelectionPointPosition.last:
                x2 += vector.x
                if x2 - x1 < min_size.width:
                    x2 = x1 + min_size.width
            
            if self.__current_action.vertical == SelectionPointPosition.first:
                y1 += vector.y
                if y2 - y1 < min_size.height:
                    y1 = y2 - min_size.height
            elif self.__current_action.vertical == SelectionPointPosition.last:
                y2 += vector.y
                if y2 - y1 < min_size.height:
                    y2 = y1 + min_size.height
            
            self.__current_action_bounds = Rectangle(x1, y1, x2 - x1, y2 - y1)
        elif isinstance(self.__current_action, ActionSelectMany):
            self.__current_action_bounds = Rectangle.from_point_point(self.__current_action_bounds.top_left, point)
        
        # TODO: don't move current point
        self.__current_action_point = point
    
    def __finish_action(self):
        if self.__postponed_action is not None:
            self.__postponed_action = None
        elif isinstance(self.__current_action, ActionMoveSelection):
            old_bounds = self.__selection.get_bounds(self.__application.ruler)
            command = MoveSelectionCommand(
                self.__selection,
                self.__current_action_bounds.top_left - old_bounds.top_left
            )
            self.__application.commands.execute(command)
        elif isinstance(self.__current_action, ActionResizeElement):
            command = ResizeMoveElementCommand(
                self.__current_action.element,
                self.__current_action_bounds
            )
            self.__application.commands.execute(command)
        elif isinstance(self.__current_action, ActionSelectMany):
            self.__selection.select_in_area(self.__application.ruler, self.__current_action_bounds.normalize())
        
        self.__current_action = None
        self.__current_action_bounds = None
