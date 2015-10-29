from PySide.QtGui import QWidget, QPainter
from umlfri2.qtgui.canvas.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.canvas.qtruler import QTRuler
from umlfri2.types.geometry import Point


class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__ruler = QTRuler()
        self.__diagram = None
    
    def show_diagram(self, diagram):
        self.__diagram = diagram
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        canvas = QTPainterCanvas(painter)
        if self.__diagram:
            self.__diagram.draw(canvas)
        painter.end()
    
    def get_ruler(self):
        return self.__ruler
    
    def mousePressEvent(self, event):
        # TODO: for testing purposes only
        if self.__diagram:
            pos = event.pos()
            element = self.__diagram.get_element_at(self.__ruler, Point(pos.x(), pos.y()))
            if element is None:
                print('None at position {0}, {1}'.format(pos.x(), pos.y()))
            else:
                print('{0} at position {1}, {2}'.format(element.object.get_display_name(), pos.x(), pos.y()))
