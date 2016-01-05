from PySide.QtCore import Qt, QPoint
from PySide.QtGui import QPainter, QPen, QBrush, QColor, QFont, QFontMetrics, QPainterPath

from umlfri2.components.visual.canvas import Canvas
from umlfri2.qtgui.base import image_loader
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.enums import LineStyle
from umlfri2.types.font import FontStyle
from umlfri2.types.geometry import PathLineTo, PathCubicTo


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
    
    def set_zoom(self, zoom):
        if zoom != 1:
            self.__painter.scale(zoom, zoom)
        
    def draw_ellipse(self, rectangle, fg=None, bg=None, line_width=None, line_style=None):
        self.__set_brush(bg)
        self.__set_pen(fg, line_width, line_style)
        self.__painter.drawEllipse(rectangle.x1, rectangle.y1, rectangle.width, rectangle.height)
    
    def draw_line(self, start, end, fg, line_width=None, line_style=None):
        self.__set_pen(fg, line_width, line_style)
        self.__painter.drawLine(start.x, start.y, end.x, end.y)
    
    def draw_path(self, path, fg=None, bg=None, line_width=None, line_style=None):
        qpath = QPainterPath()
        for segment in path.segments:
            qpath.moveTo(segment.starting_point.x, segment.starting_point.y)
            for command in segment.commands:
                if isinstance(command, PathLineTo):
                    qpath.lineTo(command.final_point.x, command.final_point.y)
                elif isinstance(command, PathCubicTo):
                    qpath.cubicTo(
                        command.control_point1.x, command.control_point1.y,
                        command.control_point2.x, command.control_point2.y,
                        command.final_point.x, command.final_point.y)
            if segment.closed:
                qpath.closeSubpath()
        
        self.__set_brush(bg)
        self.__set_pen(fg, line_width, line_style)
        self.__painter.drawPath(qpath)
    
    def draw_rectangle(self, rectangle, fg=None, bg=None, line_width=None, line_style=None):
        self.__set_brush(bg)
        self.__set_pen(fg, line_width, line_style)
        self.__painter.drawRect(rectangle.x1, rectangle.y1, rectangle.width, rectangle.height)
    
    def draw_text(self, pos, text, font, fg):
        if not text:
            return
        qfont = QFont(font.family)
        qfont.setPixelSize(font.size)
        qfont.setBold(FontStyle.bold in font.style)
        qfont.setItalic(FontStyle.italic in font.style)
        qfont.setStrikeOut(FontStyle.strike in font.style)
        qfont.setUnderline(FontStyle.underline in font.style)
        metrics = QFontMetrics(qfont)
        
        self.__painter.setFont(qfont)
        self.__set_pen(fg)
        x = pos.x
        y = pos.y + metrics.ascent()
        if '\n' in text:
            height = metrics.height()
            for line in text.split('\n'):
                self.__painter.drawText(QPoint(x, y), line)
                y += height
        else:
            self.__painter.drawText(QPoint(x, y), text)
    
    def draw_image(self, pos, image):
        pixmap = image_loader.load(image)
        self.__painter.drawPixmap(pos.x, pos.y, pixmap)
    
    def clear(self, color=None):
        if color is None:
            self.__painter.setBackground(QColor(255, 255, 255))
        else:
            self.__painter.setBackground(self.__convert_color(color))
        self.__painter.eraseRect(self.__painter.viewport())
    
    def get_ruler(self):
        return self.__ruler
