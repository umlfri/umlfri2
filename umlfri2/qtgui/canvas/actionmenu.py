from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu, QApplication, QAction

from umlfri2.types.geometry import Point

from ..base import image_loader


class ActionMenu(QMenu):
    def __init__(self, drawing_area, menu):
        super().__init__()
        self.__menu = menu
        self.__drawing_area = drawing_area
        self.__menu_selected = False
    
    def do(self):
        for menu_item in self.__menu:
            qt_menu_item = QAction(menu_item.text, self)
            if menu_item.icon is not None:
                qt_menu_item.setIcon(image_loader.load_icon(menu_item.icon))
            qt_menu_item.triggered.connect(partial(self.__execute_menu_action, menu_item))
            self.addAction(qt_menu_item)
    
        qt_menu_pos = QCursor.pos()
        self.exec_(qt_menu_pos)
        if not self.__menu_selected:
            self.__drawing_area.set_action(None)

    def __execute_menu_action(self, menu_item):
        self.__menu_selected = True
        global_pos = QCursor.pos()
        pos = self.mapFromGlobal(global_pos)
        point = Point(pos.x(), pos.y())
        
        self.__drawing_area.execute_menu_action(
            menu_item,
            point,
            QApplication.keyboardModifiers() == Qt.ControlModifier,
            QApplication.keyboardModifiers() == Qt.ShiftModifier
        )
