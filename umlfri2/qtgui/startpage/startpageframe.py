from PySide.QtCore import QSize
from PySide.QtGui import QWidget, QPainter, QBrush, QPen, QColor, QPainterPath


class StartPageFrame(QWidget):
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBrush(QBrush(QColor(0, 0, 255, 32)))
        painter.setPen(QPen(QPen(QColor(0, 36, 62, 128), 4)))
        
        painter.drawRect(painter.viewport())
        
        painter.end()
        
        super().paintEvent(event)
    
    def sizeHint(self):
        return QSize(350, 200)
