from PySide.QtGui import QPainter, QPen, QBrush, QColor, QFont, QFontMetrics
from PySide.QtCore import Qt, QPoint

from umlfri2.qtgui.canvas.qtruler import QTRuler
from umlfri2.components.visual.canvas import Canvas, LineStyle
from umlfri2.types.font import FontStyle


class QTPainterCanvas(Canvas):
    __line_styles = {
        LineStyle.solid: Qt.PenStyle.SolidLine,
        LineStyle.dot: Qt.PenStyle.DotLine,
        LineStyle.dashdot: Qt.PenStyle.DashDotLine
    }
    
    def __init__(self, painter):
        """
        Painter used by the canvas
        
        :type painter: QPainter
        """
        
        self.__painter = painter
        self.__ruler = QTRuler()

    def __convert_color(self, color):
        return QColor.fromRgba(color.argb)

    def __set_pen(self, color=None, width=None, style=None):
        if color:
            qcolor = self.__convert_color(color)
            if style:
                qstyle = self.__line_styles[style]
            else:
                qstyle = Qt.PenStyle.SolidLine
            self.__painter.setPen(QPen(self.__create_brush(color), width or 1, qstyle))
        else:
            self.__painter.setPen(Qt.PenStyle.NoPen)
    
    def __create_brush(self, color=None):
        if color:
            qcolor = self.__convert_color(color)
            return QBrush(qcolor)
        else:
            return Qt.BrushStyle.NoBrush
    
    def __set_brush(self, color=None):
        self.__painter.setBrush(self.__create_brush(color))
        
    def draw_ellipse(self, pos, size, angles=(0, 360), fg=None, bg=None, line_width=None, line_style=None):
        self.__set_brush(bg)
        self.__set_pen(fg, line_width, line_style)
        self.__painter.drawEllipse(pos[0], pos[1], size[0], size[1])
    
    def draw_line(self, start, end, fg, line_width=None, line_style=None):
        self.__set_pen(fg, line_width, line_style)
        self.__painter.drawLine(start[0], start[1], end[0], end[1])
    
    def draw_path(self, path, fg=None, bg=None, line_width=None, line_style=None):
        pass
    
    def draw_rectangle(self, pos, size, fg=None, bg=None, line_width=None, line_style=None):
        self.__set_brush(bg)
        self.__set_pen(fg, line_width, line_style)
        self.__painter.drawRect(pos[0], pos[1], size[0], size[1])
    
    def draw_text(self, pos, text, font, fg):
        qfont = QFont(font.family, font.size)
        qfont.setBold(FontStyle.bold in font.style)
        qfont.setItalic(FontStyle.italic in font.style)
        qfont.setStrikeOut(FontStyle.strike in font.style)
        qfont.setUnderline(FontStyle.underline in font.style)
        metrics = QFontMetrics(qfont)
        
        self.__painter.setFont(qfont)
        self.__set_pen(fg)
        x = pos[0]
        y = pos[1] + metrics.ascent()
        self.__painter.drawText(QPoint(x, y), text)
    
    def draw_icon(self, pos, filename):
        pass
    
    def clear(self, color=None):
        if color is None:
            self.__painter.setBackground(QColor(255, 255, 255))
        else:
            self.__painter.setBackground(self.__convert_color(color))
    
    def get_ruler(self):
        return self.__ruler
