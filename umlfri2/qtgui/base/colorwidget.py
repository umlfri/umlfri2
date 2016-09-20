from PySide.QtCore import Signal
from PySide.QtGui import QWidget, QHBoxLayout, QLabel, QPushButton, QColor, QColorDialog

from umlfri2.types.color import Color, Colors


class ColorSelectionWidget(QWidget):
    color_changed = Signal(Color)
    
    def __init__(self, btn_class=QPushButton):
        super().__init__()
        self.__color = Colors.black
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.__selectedColorLabel = QLabel()
        
        layout.addWidget(self.__selectedColorLabel, 1)
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
        dialog = QColorDialog()
        dialog.setCurrentColor(QColor.fromRgba(self.__color.argb))
        if dialog.exec_() == QColorDialog.Accepted:
            self.__color = Color(dialog.currentColor().rgba())
            self.__refresh_label()
            self.color_changed.emit(self.__color)
    
    def __refresh_label(self):
        self.__selectedColorLabel.setStyleSheet('QLabel { background-color: %s }' % self.__color.to_rgb_str())
