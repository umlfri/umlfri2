from umlfri2.ufl.dialog import UflDialog
from .drawingareacursor import DrawingAreaCursor
from umlfri2.types.color import Colors
from .actions import SelectManyAction
from .selection import Selection


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
        self.__cursor = DrawingAreaCursor.arrow
    
    @property
    def diagram(self):
        return self.__diagram
    
    @property
    def cursor(self):
        return self.__cursor
    
    @property
    def selection(self):
        return self.__selection
    
    def draw(self, canvas):
        self.__diagram.draw(canvas, self.__selection)
        if self.__current_action is not None:
            if self.__current_action.box is not None:
                canvas.draw_rectangle(
                    self.__current_action.box,
                    self.SELECTION_RECTANGLE_BORDER,
                    self.SELECTION_RECTANGLE_FILL,
                    self.SELECTION_RECTANGLE_WIDTH
                )
            if self.__current_action.path is not None:
                canvas.draw_path(
                    self.__current_action.path,
                    fg=self.SELECTION_RECTANGLE_BORDER,
                    line_width=self.SELECTION_RECTANGLE_WIDTH
                )
    
    def mouse_down(self, point, control_pressed, shift_pressed):
        if self.__current_action is not None:
            self.__current_action.mouse_down(self, self.__application, point)
            self.__postprocess_action(point, shift_pressed)
        else:
            action = self.__selection.get_action_at(self.__application.ruler, point, shift_pressed)
            
            if action is not None:
                self.__current_action = action
                self.__current_action.mouse_down(self, self.__application, point)
                self.__postprocess_action(point, shift_pressed)
            else:
                object = self.__diagram.get_visual_at(self.__application.ruler, point)
                
                if control_pressed:
                    if object is not None:
                        self.__selection.toggle_select(object)
                else:
                    self.__selection.select(object)
                    action = self.__selection.get_action_at(self.__application.ruler, point, shift_pressed)
                    
                    if action is None:
                        action = SelectManyAction()
                    self.__postponed_action = action, point
            
            self.__change_cursor(point, shift_pressed)

    def mouse_move(self, point, control_pressed, shift_pressed):
        if self.__postponed_action is not None:
            self.__current_action, postponed_point = self.__postponed_action
            self.__current_action.mouse_down(self, self.__application, postponed_point)
            self.__postponed_action = None
        
        if self.__current_action is not None:
            self.__current_action.mouse_move(self, self.__application, point)
            self.__postprocess_action(point, shift_pressed)
        else:
            self.__change_cursor(point, shift_pressed)
    
    def mouse_up(self, point, control_pressed, shift_pressed):
        if self.__postponed_action is not None:
            self.__postponed_action = None
        elif self.__current_action is not None:
            self.__current_action.mouse_up(self, self.__application)
            self.__postprocess_action(point, shift_pressed)
    
    def edit_attributes(self, point):
        visual = self.__diagram.get_visual_at(self.__application.ruler, point)
        if visual is None:
            return None
        else:
            self.__current_action = None
            dialog = UflDialog(visual.object.data.type)
            dialog.associate(visual.object.data.make_mutable())
            return dialog

    def __postprocess_action(self, point, shift_pressed):
        if self.__current_action is not None and self.__current_action.finished:
            self.__current_action = None
            self.__change_cursor(point, shift_pressed)

    def __change_cursor(self, point, shift_pressed):
        action = self.__selection.get_action_at(self.__application.ruler, point, shift_pressed)
        if action is None:
            self.__cursor = DrawingAreaCursor.arrow
        else:
            self.__cursor = action.cursor
    
    def set_action(self, action):
        self.__current_action = action
