from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTabBar


class MiddleClosableTabBar(QTabBar):
    def __init__(self):
        super().__init__()
        self.__middle_down_tab = None
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        
        if not self.tabsClosable():
            return
        
        if event.button() == Qt.MidButton:
            self.__middle_down_tab = self.tabAt(event.pos())
    
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        
        if not self.tabsClosable():
            return
        
        if event.button() == Qt.MidButton:
            if self.__middle_down_tab == self.tabAt(event.pos()):
                self.tabCloseRequested.emit(self.__middle_down_tab)
        
        self.__middle_down_tab = None
