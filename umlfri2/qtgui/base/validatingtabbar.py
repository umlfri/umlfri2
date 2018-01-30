from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QTabBar


class ValidateTabChangeEvent:
    def __init__(self, tab_index):
        self.__valid = True
        self.__tab_index = tab_index

    @property
    def is_valid(self):
        return self.__valid

    @property
    def tab_index(self):
        return self.__tab_index

    def invalidate(self):
        self.__valid = False


class ValidatingTabBar(QTabBar):
    validate_tab_change = pyqtSignal(ValidateTabChangeEvent)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return super().mousePressEvent(event)

        tab_index = self.tabAt(event.pos())
        if tab_index < 0 or tab_index == self.currentIndex():
            return super().mousePressEvent(event)

        evt = ValidateTabChangeEvent(tab_index)
        self.validate_tab_change.emit(evt)
        if evt.is_valid:
            return super().mousePressEvent(event)
        event.ignore()
