class Action:
    def get_cursor(self):
        raise NotImplementedError
    
    def mouse_down(self, point):
        raise NotImplementedError
    
    def mouse_move(self, point):
        raise NotImplementedError
    
    def mouse_up(self):
        raise NotImplementedError
