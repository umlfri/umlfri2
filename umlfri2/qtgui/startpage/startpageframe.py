from html import escape

from PySide.QtCore import QSize, QRect
from PySide.QtGui import QWidget, QPainter, QBrush, QPen, QColor, QVBoxLayout, QLabel


class StartPageFrame(QWidget):
    WIDTH = 330
    HEIGHT = 150
    THICKNESS = 4
    
    def __init__(self):
        super().__init__()
        
        self.__layout = QVBoxLayout()
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
    
    def add_frame_action(self, callback):
        action_label = QLabel()
        action_label.linkActivated.connect(lambda url: callback())
        self.__layout.addWidget(action_label)
        
        return self.__layout.count() - 1
    
    def set_frame_action_label(self, no, text):
        widget = self.__layout.itemAt(no).widget()
        widget.setText('<a href="action" style="color: black">{0}</a>'.format(escape(text)))
    
    def clear(self):
        for no in range(self.__layout.count()):
            item = self.__layout.itemAt(no)
            self.__layout.removeWidget(item.widget())
            item.widget().deleteLater()
