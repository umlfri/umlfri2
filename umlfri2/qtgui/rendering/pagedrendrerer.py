import math

from PyQt5.QtGui import QPainter

from umlfri2.types.geometry import Vector
from .qtruler import QTRuler
from .qtpaintercanvas import QTPainterCanvas


class PagedRenderer:
    def __init__(self, device):
        self.__device = device
        self.__page = self.__device.pageRect()
    
    def render_diagram(self, diagram):
        bounds = diagram.get_bounds(QTRuler())
        
        painter = QPainter()
        painter.begin(self.__device)
        
        pages_horizontal = int(math.ceil(bounds.width / painter.device().width()))
        pages_vertical = int(math.ceil(bounds.height / painter.device().height()))
        
        pages_left = pages_horizontal * pages_vertical
        
        for y in range(pages_vertical):
            for x in range(pages_horizontal):
                self.__render_page(painter, diagram, x, y)
                pages_left -= 1
                if pages_left > 0:
                    self.__device.newPage()
        
        painter.end()
    
    def __render_page(self, painter, diagram, x, y):
        painter.setClipRect(
            0, 0, painter.device().width(), painter.device().height()
        )
        canvas = QTPainterCanvas(painter)
        canvas.translate(Vector(-x*painter.device().width(), -y*painter.device().height()))
        diagram.draw(canvas)
