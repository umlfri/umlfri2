import abc
from umlfri2.types.color import Color
from .ruler import Ruler


# TODO: replace with enum in Python 3.4.x
class LineStyle:
    solid = 1
    dot = 2
    dashdot = 3


class Canvas(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def draw_ellipse(self, rectangle, fg=None, bg=None, line_width=None, line_style=None):
        """
        Draws ellipse to canvas.
        
        :param pos: Position of the ellipse top left corner
        :type pos: (int, int)
        :param size: Size of the ellipse
        :type size: (int, int)
        :param fg: Foreground color
        :type fg: Color
        :param bg: Background color
        :type bg: Color
        :param line_width: Width of the arc outline
        :type line_width: int
        :param line_style: Line style used for arc outline
        :type line_style: int
        """
        pass
    
    @abc.abstractmethod
    def draw_line(self, start, end, fg, line_width=None, line_style=None):
        pass
    
    @abc.abstractmethod
    def draw_path(self, path, fg=None, bg=None, line_width=None, line_style=None):
        pass
    
    @abc.abstractmethod
    def draw_rectangle(self, rectangle, fg=None, bg=None, line_width=None, line_style=None):
        pass
    
    @abc.abstractmethod
    def draw_text(self, pos, text, font, fg):
        pass
    
    @abc.abstractmethod
    def draw_icon(self, pos, filename):
        pass
    
    @abc.abstractmethod
    def clear(self, color=None):
        pass
    
    @abc.abstractmethod
    def get_ruler(self):
        """
        Get ruler associated with current canvas.
        :return Ruler
        :rtype Ruler
        """
        pass
