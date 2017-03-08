from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFontDialog

from umlfri2.types.enums import FontStyle
from umlfri2.types.font import Font, Fonts


class FontSelectionWidget(QWidget):
    font_changed = pyqtSignal(Font)

    def __init__(self, btn_class=QPushButton):
        super().__init__()
        self.__font = Fonts.default

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.__selected_font_label = QLabel()

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
        fontPixelsPerPoint = self.__selected_font_label.physicalDpiY() / 72
        
        # TODO: change font dialog to custom dialog, QFontDialog does not work with pixelSize
        dialog = QFontDialog()
        qfont = QFont(self.__font.family)
        qfont.setPointSize(self.__font.size / fontPixelsPerPoint)
        qfont.setBold(FontStyle.bold in self.__font.style)
        qfont.setItalic(FontStyle.italic in self.__font.style)
        qfont.setStrikeOut(FontStyle.strike in self.__font.style)
        qfont.setUnderline(FontStyle.underline in self.__font.style)
        dialog.setCurrentFont(qfont)
        if dialog.exec_() == QFontDialog.Accepted:
            font = dialog.selectedFont()
            family = font.family()
            size = int(font.pointSize() * fontPixelsPerPoint)
            style = []
            if font.bold():
                style.append(FontStyle.bold)
            if font.italic():
                style.append(FontStyle.italic)
            if font.strikeOut():
                style.append(FontStyle.strike)
            if font.underline():
                style.append(FontStyle.underline)
            self.__font = Font(family, size, style)
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
