from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QTabBar, QTabWidget


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

        if self.__do_test(tab_index):
            return super().mousePressEvent(event)
        event.ignore()
    
    def wheelEvent(self, event):
        delta_point = event.angleDelta()
        if delta_point.x() == 0 and delta_point.y() != 0:
            delta = delta_point.y()
        elif delta_point.x() != 0 and delta_point.y() == 0:
            delta = delta_point.x()
        else:
            event.ignore()
            return
        
        if delta > 0:
            tested_tabs = range(self.currentIndex() - 1, -1, -1)
        else:
            tested_tabs = range(self.currentIndex() + 1, self.count(), 1)
        
        for tested_index in tested_tabs:
            if self.isTabEnabled(tested_index):
                if self.__do_test(tested_index):
                    self.setCurrentIndex(tested_index)
                break
        
        event.ignore()

    def __do_test(self, tab_index):
        evt = ValidateTabChangeEvent(tab_index)
        self.validate_tab_change.emit(evt)
        return evt.is_valid


class ValidatingTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabBar(ValidatingTabBar())
