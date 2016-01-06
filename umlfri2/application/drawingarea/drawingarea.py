from umlfri2.application.events.application import ZoomChangedEvent
from umlfri2.application.snippet import SnippetBuilder
from umlfri2.types.geometry import Point
from .drawingareacursor import DrawingAreaCursor
from umlfri2.types.color import Colors
from .actions import SelectManyAction
from .selection import Selection


class DrawingArea:
    SELECTION_RECTANGLE_FILL = Colors.blue.add_alpha(5)
    SELECTION_RECTANGLE_BORDER = Colors.blue
    SELECTION_RECTANGLE_WIDTH = 3
    
    ZOOM_FACTOR = 1.25
    ZOOM_MIN = -3
    ZOOM_MAX = 6
    
    def __init__(self, application, diagram):
        self.__diagram = diagram
        self.__selection = Selection(application, self.__diagram)
        self.__application = application
        self.__postponed_action = None
        self.__current_action = None
        self.__cursor = DrawingAreaCursor.arrow
        self.__zoom = 0
    
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
        canvas.set_zoom(self.ZOOM_FACTOR**self.__zoom)
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
        point = self.__transform_position(point)
        
        if self.__current_action is not None:
            self.__current_action.mouse_down(point)
            self.__postprocess_action(point, shift_pressed)
        else:
            action = self.__selection.get_action_at(point, shift_pressed)
            
            if action is not None:
                self.set_action(action)
                self.__current_action.mouse_down(point)
                self.__postprocess_action(point, shift_pressed)
            else:
                object = self.__diagram.get_visual_at(self.__application.ruler, point)
                
                if control_pressed:
                    if object is not None:
                        self.__selection.toggle_select(object)
                else:
                    self.__selection.select(object)
                    action = self.__selection.get_action_at(point, shift_pressed)
                    
                    if action is None:
                        action = SelectManyAction()
                    self.__postponed_action = action, point
            
            self.__change_cursor(point, shift_pressed)

    def mouse_move(self, point, control_pressed, shift_pressed):
        point = self.__transform_position(point)
        
        if self.__postponed_action is not None:
            action, postponed_point = self.__postponed_action
            self.set_action(action)
            self.__current_action.mouse_down(postponed_point)
            self.__postponed_action = None
        
        if self.__current_action is not None:
            self.__current_action.mouse_move(point)
            self.__postprocess_action(point, shift_pressed)
        else:
            self.__change_cursor(point, shift_pressed)
    
    def mouse_up(self, point, control_pressed, shift_pressed):
        point = self.__transform_position(point)
        
        if self.__postponed_action is not None:
            self.__postponed_action = None
        elif self.__current_action is not None:
            self.__current_action.mouse_up()
            self.__postprocess_action(point, shift_pressed)
    
    def get_object_at(self, point):
        point = self.__transform_position(point)
        
        visual = self.__diagram.get_visual_at(self.__application.ruler, point)
        if visual is None:
            return None
        else:
            return visual.object
    
    def __postprocess_action(self, point, shift_pressed):
        if self.__current_action is not None and self.__current_action.finished:
            self.set_action(None)
            self.__change_cursor(point, shift_pressed)

    def __change_cursor(self, point, shift_pressed):
        action = self.__selection.get_action_at(point, shift_pressed)
        if action is None:
            self.__cursor = DrawingAreaCursor.arrow
        else:
            self.__cursor = action.cursor
    
    def set_action(self, action):
        self.__current_action = action
        if action is None:
            self.__cursor = DrawingAreaCursor.arrow
        else:
            action.associate(self.__application, self)
            self.__cursor = action.cursor
    
    @property
    def current_action(self):
        return self.__current_action
    
    @property
    def action_active(self):
        return self.__current_action is not None
    
    def get_size(self, ruler):
        zoom = self.ZOOM_FACTOR**self.__zoom
        return self.__diagram.get_size(ruler) * zoom
    
    def __transform_position(self, position):
        zoom = self.ZOOM_FACTOR**self.__zoom
        return Point(int(round(position.x / zoom)), int(round(position.y / zoom)))
    
    @property
    def can_zoom_in(self):
        return self.__zoom < self.ZOOM_MAX
    
    def zoom_in(self):
        self.__zoom += 1
        if self.__zoom > self.ZOOM_MAX:
            self.__zoom = self.ZOOM_MAX
        
        self.__application.event_dispatcher.dispatch(ZoomChangedEvent(self))
    
    @property
    def can_zoom_out(self):
        return self.__zoom > self.ZOOM_MIN
    
    def zoom_out(self):
        self.__zoom -= 1
        if self.__zoom < self.ZOOM_MIN:
            self.__zoom = self.ZOOM_MIN
        
        self.__application.event_dispatcher.dispatch(ZoomChangedEvent(self))
    
    @property
    def can_zoom_original(self):
        return self.__zoom != 0
    
    def zoom_original(self):
        self.__zoom = 0
        self.__application.event_dispatcher.dispatch(ZoomChangedEvent(self))
    
    @property
    def can_copy_snippet(self):
        return self.__selection.is_element_selected
    
    def copy_snippet(self):
        builder = SnippetBuilder(self.__diagram.project)
        
        for element in self.__selection.selected_elements:
            builder.add_element(self.__application.ruler, element)
        
        self.__application.clipboard = builder.build()
    
    @property
    def can_paste_snippet(self):
        if self.__application.clipboard_empty:
            return False
        
        return self.__application.clipboard.can_be_pasted_to(self.__diagram)
