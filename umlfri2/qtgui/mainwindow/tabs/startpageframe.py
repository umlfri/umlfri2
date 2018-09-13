from PyQt5.QtCore import QSize, QRect, Qt
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from .startpageframeaction import StartPageFrameAction


class StartPageFrame(QWidget):
    WIDTH = 330
    HEIGHT = 150
    THICKNESS = 4
    
    def __init__(self):
        super().__init__()
        
        self.__layout = QVBoxLayout()
        self.__layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.__layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.__layout)
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBrush(QBrush(QColor(0, 0, 255, 32)))
        painter.setPen(QPen(QPen(QColor(0, 36, 62, 96), self.THICKNESS)))
        
        viewport = painter.viewport()
        
        rect = QRect(self.THICKNESS/2, self.THICKNESS/2, viewport.width() - self.THICKNESS,
                     viewport.height() - self.THICKNESS)
        
        painter.drawRoundedRect(rect, 15, 15)
        
        painter.end()
        
        super().paintEvent(event)
    
    def sizeHint(self):
        return QSize(self.WIDTH, self.HEIGHT)
    
    def add_frame_action(self):
        action = StartPageFrameAction()
        self.__layout.addWidget(action)
        
        return action
    
    def clear(self):
        for no in range(self.__layout.count()):
            widget = self.__layout.itemAt(0).widget()
            widget.setParent(None)
            self.__layout.removeWidget(widget)
