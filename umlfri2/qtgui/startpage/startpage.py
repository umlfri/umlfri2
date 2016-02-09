import os

from PySide.QtCore import QPoint, Qt
from PySide.QtGui import QWidget, QPixmap, QPainter, QColor, QFont, QPen, QPainterPath, QBrush, QHBoxLayout
from umlfri2.application import Application
from umlfri2.constants.paths import GRAPHICS
from .startpageframe import StartPageFrame


class StartPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.__background = QPixmap()
        self.__background.load(os.path.join(GRAPHICS, "startpage", "startpage.png"))
        
        layout = QHBoxLayout()
        layout.setSpacing(40)
        layout.setContentsMargins(0, 300, 0, 0)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        
        actions_frame = StartPageFrame()
        layout.addWidget(actions_frame)
        
        recent_files_frame = StartPageFrame()
        layout.addWidget(recent_files_frame)
        
        self.setLayout(layout)
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBackground(QColor(52, 170, 253))
        painter.eraseRect(painter.viewport())
        
        painter.drawPixmap(QPoint(0, 0), self.__background)
        
        qfont = QFont("Arial")
        qfont.setPixelSize(72)
        qfont.setBold(QFont.Bold)
        self.__paint_outlined_text(painter, QPoint(150, 110), qfont, "UML")
        
        qfont.setPixelSize(45)
        self.__paint_outlined_text(painter, QPoint(330, 110), qfont, ".FRI")
        
        self.__paint_outlined_text(painter, QPoint(450, 110), qfont, Application().VERSION.major_minor_string)
        
        painter.end()
        
        super().paintEvent(event)
    
    def __paint_outlined_text(self, painter, position, font, text):
        path = QPainterPath()
        path.addText(position, font, text)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor(72, 124, 194), 1.5))
        painter.drawPath(path)
