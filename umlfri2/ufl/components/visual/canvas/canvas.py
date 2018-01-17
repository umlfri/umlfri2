class Canvas:
    def translate(self, delta):
        raise NotImplementedError
    
    def zoom(self, zoom):
        raise NotImplementedError
    
    def draw_ellipse(self, rectangle, fg=None, bg=None, line_width=None, line_style=None):
        raise NotImplementedError
    
    def draw_line(self, start, end, fg, line_width=None, line_style=None):
        raise NotImplementedError
    
    def draw_path(self, path, fg=None, bg=None, line_width=None, line_style=None):
        raise NotImplementedError
    
    def draw_rectangle(self, rectangle, fg=None, bg=None, line_width=None, line_style=None):
        raise NotImplementedError
    
    def draw_text(self, pos, text, font, fg):
        raise NotImplementedError
    
    def draw_image(self, pos, image):
        raise NotImplementedError
    
    def clear(self, color=None):
        raise NotImplementedError
    
    def get_ruler(self):
        raise NotImplementedError
