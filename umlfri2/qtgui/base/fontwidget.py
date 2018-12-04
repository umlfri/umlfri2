from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFrame

from umlfri2.qtgui.appdialogs.fontdialog import FontDialog
from umlfri2.types.font import Font, Fonts


class FontSelectionWidget(QWidget):
    font_changed = pyqtSignal(Font)

    def __init__(self, btn_class=QPushButton):
        super().__init__()
        self.__font = Fonts.default

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.__selected_font_label = QLabel()
        self.__selected_font_label.setFrameShape(QFrame.StyledPanel)
        self.__selected_font_label.setFrameShadow(QFrame.Sunken)
        self.__selected_font_label.setMinimumWidth(50)
        
        layout.addWidget(self.__selected_font_label, 1)
        choose_button = btn_class()
        choose_button.setText("...")
        choose_button.clicked.connect(self.__choose_font)
        layout.addWidget(choose_button, 0)

        self.setLayout(layout)

        self.__refresh_label()

    @property
    def selected_font(self):
        return self.__font

    @selected_font.setter
    def selected_font(self, value):
        self.__font = value

        self.__refresh_label()

    def __choose_font(self):
        dialog = FontDialog(self.window())
        dialog.ufl_font = self.__font
        if dialog.exec() == FontDialog.Accepted:
            self.__font = dialog.ufl_font
            self.__refresh_label()
            self.font_changed.emit(self.__font)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.__refresh_label()

    def __refresh_label(self):
        text = str(self.__font)
        metrics = QFontMetrics(self.__selected_font_label.font())
        width = self.__selected_font_label.width() - 2
        text = metrics.elidedText(text, Qt.ElideRight, width)
        self.__selected_font_label.setText(text)
