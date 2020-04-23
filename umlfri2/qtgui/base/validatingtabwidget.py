from itertools import chain

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
            self.change_tab_in_direction(to_right=True)
        else:
            self.change_tab_in_direction(to_right=False)
        
        event.ignore()
    
    def change_tab_in_direction(self, to_right, continue_from_end=False):
        if to_right:
            tested_tabs = range(self.currentIndex() - 1, -1, -1)
            from_start = range(self.count() - 1, self.currentIndex(), -1)
        else:
            tested_tabs = range(self.currentIndex() + 1, self.count(), 1)
            from_start = range(0, self.currentIndex(), 1)
        
        if continue_from_end:
            tested_tabs = chain(tested_tabs, from_start)

        for tested_index in tested_tabs:
            if self.isTabEnabled(tested_index):
                if self.__do_test(tested_index):
                    self.setCurrentIndex(tested_index)
                break
    
    def __do_test(self, tab_index):
        evt = ValidateTabChangeEvent(tab_index)
        self.validate_tab_change.emit(evt)
        return evt.is_valid


class ValidatingTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabBar(ValidatingTabBar())
    
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Tab, Qt.Key_Backtab) and event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Backtab or event.modifiers() & Qt.ShiftModifier:
                self.tabBar().change_tab_in_direction(to_right=True, continue_from_end=True)
            else:
                self.tabBar().change_tab_in_direction(to_right=False, continue_from_end=True)
            event.ignore()
        else:
            super().keyPressEvent(event)
