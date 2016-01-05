from PySide.QtCore import QSize, QRect
from PySide.QtGui import QPixmap, QPainter, QPrinter

try:
    from PySide.QtSvg import QSvgGenerator
except ImportError:
    QSvgGenerator = None

from .qtpaintercanvas import QTPainterCanvas
from .qtruler import QTRuler


class ImageExport:
    def __init__(self, diagram):
        self.__diagram = diagram
    
    def supported_formats(self):
        yield 'bmp',
        yield 'jpg', 'jpeg'
        yield 'pdf',
        yield 'png',
        yield 'ppm',
        if QSvgGenerator is not None:
            yield 'svg',
        yield 'tiff',
        yield 'xbm', 'xpm'
    
    def export(self, file, format):
        size = self.__diagram.get_size(QTRuler())
        
        if format == 'svg':
            output = QSvgGenerator()
            output.setFileName(file)
            
            output.setSize(QSize(size.width, size.height))
            output.setViewBox(QRect(0, 0, size.width, size.height))
            output.setTitle(self.__diagram.get_display_name() or "")
        elif format == 'pdf':
            output = QPrinter()
            output.setOutputFormat(QPrinter.PdfFormat)
            output.setPaperSize(QSize(size.width, size.height), QPrinter.DevicePixel)
            output.setPageMargins(0, 0, 0, 0, QPrinter.DevicePixel)
            output.setOutputFileName(file)
        else:
            output = QPixmap(size.width, size.height)
        
        painter = QPainter()
        painter.begin(output)
        
        canvas = QTPainterCanvas(painter)
        self.__diagram.draw(canvas)
        
        painter.end()
        
        if format not in ('svg', 'pdf'):
            output.save(file, format)
