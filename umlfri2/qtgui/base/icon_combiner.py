from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QIcon


def combine_icons(icon, overlay, sizes=None):
    if sizes is None:
        sizes = icon.availableSizes()
    
    ret = QIcon()
    for size in sizes:
        size_pixmap = QPixmap(size)
        size_pixmap.fill(Qt.transparent)

        painter = QPainter()
        painter.begin(size_pixmap)

        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawPixmap(0, 0, icon.pixmap(size))
        
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, overlay.scaled(size.width(), size.height()))
        
        painter.end()
        ret.addPixmap(size_pixmap)
    
    return ret
