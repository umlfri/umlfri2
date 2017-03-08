from PyQt5.QtCore import QSize, QSizeF, QRect, Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication

try:
    from PyQt5.QtPrintSupport import QPrinter
except ImportError:
    QPrinter = None

try:
    from PyQt5.QtSvg import QSvgGenerator
except ImportError:
    QSvgGenerator = None

from umlfri2.model import Diagram
from umlfri2.types.geometry import Vector
from .qtpaintercanvas import QTPainterCanvas
from .qtruler import QTRuler


class ImageExport:
    def __init__(self, diagram_or_selection, zoom, padding, transparent):
        self.__diagram_or_selection = diagram_or_selection
        self.__zoom = zoom
        self.__padding = padding
        self.__transparent = transparent
    
    def supported_formats(self):
        if not self.__transparent:
            yield 'bmp',
            yield 'jpg', 'jpeg'
        if QPrinter is not None:
            yield 'pdf',
        yield 'png',
        if QSvgGenerator is not None:
            yield 'svg',
        yield 'xpm',
    
    @property
    def default_format(self):
        return 'png'
    
    def export(self, file, format):
        bounds = self.__get_bounds()
        size = self.get_size(bounds)
        
        if format == 'svg':
            output = QSvgGenerator()
            output.setFileName(file)
            
            output.setSize(size)
            output.setViewBox(QRect(QPoint(0, 0), size))
            if isinstance(self.__diagram_or_selection, Diagram):
                output.setTitle(self.__diagram_or_selection.get_display_name() or "")
        elif format == 'pdf':
            output = QPrinter()
            output.setOutputFormat(QPrinter.PdfFormat)
            output.setPaperSize(QSizeF(size), QPrinter.DevicePixel)
            output.setPageMargins(0, 0, 0, 0, QPrinter.DevicePixel)
            output.setOutputFileName(file)
        else:
            output = QPixmap(size)
            output.fill(Qt.transparent)

        self.__draw(bounds, output)
        
        if format not in ('svg', 'pdf'):
            output.save(file, format)
    
    def export_to_clipboard(self):
        bounds = self.__get_bounds()
        size = self.get_size(bounds)
        
        output = QPixmap(size)
        output.fill(Qt.transparent)

        self.__draw(bounds, output)

        QApplication.clipboard().setPixmap(output)
    
    def __get_bounds(self):
        if isinstance(self.__diagram_or_selection, Diagram):
            return self.__diagram_or_selection.get_bounds(QTRuler())
        else:
            return self.__diagram_or_selection.get_bounds()
    
    def get_size(self, bounds):
        return QSize(
            (bounds.width + 2 * self.__padding) * self.__zoom,
            (bounds.height + 2 * self.__padding) * self.__zoom
        )
    
    def __draw(self, bounds, output):
        painter = QPainter()
        painter.begin(output)
        painter.setRenderHint(QPainter.Antialiasing)
        canvas = QTPainterCanvas(painter)
        canvas.zoom(self.__zoom)
        canvas.translate(Vector(-bounds.x1 + self.__padding, -bounds.y1 + self.__padding))
        if isinstance(self.__diagram_or_selection, Diagram):
            self.__diagram_or_selection.draw(canvas, transparent=self.__transparent)
        else:
            self.__diagram_or_selection.draw_selected(canvas, transparent=self.__transparent)
        painter.end()
