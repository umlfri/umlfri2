import os

from PySide.QtCore import QPoint
from PySide.QtGui import QWidget, QPixmap, QPainter, QColor, QFont, QPen, QPainterPath, QBrush

from umlfri2.application import Application
from umlfri2.constants.paths import GRAPHICS


class StartPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.__background = QPixmap()
        self.__background.load(os.path.join(GRAPHICS, "startpage", "startpage.png"))
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBackground(QColor(52, 170, 253))
        painter.eraseRect(painter.viewport())
        
        painter.drawPixmap(QPoint(0, 0), self.__background)
        
        self.__paint_outlined_text(
            painter,
            QPoint(150, 110),
            QFont("Arial", 40, QFont.Bold, False),
            "UML"
        )
        
        self.__paint_outlined_text(
            painter,
            QPoint(330, 110),
            QFont("Arial", 25, QFont.Bold, False),
            ".FRI"
        )
        
        self.__paint_outlined_text(
            painter,
            QPoint(450, 110),
            QFont("Arial", 25, QFont.Bold, False),
            Application().VERSION.major_minor_string
        )
        
        painter.end()
        
        super().paintEvent(event)
    
    def __paint_outlined_text(self, painter, position, font, text):
        path = QPainterPath()
        path.addText(position, font, text)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor(72, 124, 194), 1.5))
        painter.drawPath(path)
