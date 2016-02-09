from PySide.QtCore import QSize, QRect
from PySide.QtGui import QWidget, QPainter, QBrush, QPen, QColor


class StartPageFrame(QWidget):
    WIDTH = 350
    HEIGHT = 200
    THICKNESS = 4
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBrush(QBrush(QColor(0, 0, 255, 32)))
        painter.setPen(QPen(QPen(QColor(0, 36, 62, 96), self.THICKNESS)))
        
        rect = QRect(self.THICKNESS/2, self.THICKNESS/2, self.WIDTH - self.THICKNESS, self.HEIGHT - self.THICKNESS)
        
        painter.drawRoundedRect(rect, 15, 15)
        
        painter.end()
        
        super().paintEvent(event)
    
    def sizeHint(self):
        return QSize(self.WIDTH, self.HEIGHT)
