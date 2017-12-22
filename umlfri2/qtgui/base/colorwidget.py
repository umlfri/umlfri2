from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QColorDialog, QFrame, QSizePolicy

from umlfri2.types.color import Color, Colors


class ColorSelectionWidget(QWidget):
    color_changed = pyqtSignal(Color)
    
    def __init__(self, btn_class=QPushButton):
        super().__init__()
        self.__color = Colors.black
        
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.__selected_color_label = QLabel()
        self.__selected_color_label.setFrameShape(QFrame.StyledPanel)
        self.__selected_color_label.setFrameShadow(QFrame.Sunken)
        self.__selected_color_label.setMinimumWidth(50)
        
        layout.addWidget(self.__selected_color_label, 1)
        chooseButton = btn_class()
        chooseButton.setText("...")
        chooseButton.clicked.connect(self.__choose_color)
        layout.addWidget(chooseButton, 0)
        
        self.setLayout(layout)
        
        self.__refresh_label()
    
    @property
    def selected_color(self):
        return self.__color
    
    @selected_color.setter
    def selected_color(self, value):
        self.__color = value

        self.__refresh_label()
    
    def __choose_color(self):
        dialog = QColorDialog(self.window())
        dialog.setOption(QColorDialog.ShowAlphaChannel, True)
        dialog.setCurrentColor(QColor.fromRgba(self.__color.argb))
        if dialog.exec_() == QColorDialog.Accepted:
            self.__color = Color(dialog.currentColor().rgba())
            self.__refresh_label()
            self.color_changed.emit(self.__color)
    
    def __refresh_label(self):
        self.__selected_color_label.setStyleSheet('QLabel { background-color: %s }' % self.__color.to_rgb_str())
