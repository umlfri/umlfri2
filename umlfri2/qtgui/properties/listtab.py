from PySide.QtGui import QVBoxLayout, QTreeWidget, QHBoxLayout, QPushButton, QIcon, QTreeWidgetItem
from ..base.hlinewidget import HLineWidget
from .tab import PropertyTab


class ListPropertyTab(PropertyTab):
    def __init__(self, window, tab): 
        super().__init__(window, tab)
        layout = QVBoxLayout()
        layout.addLayout(self._create_layout)
        
        layout.addWidget(HLineWidget())
        
        self.__list = QTreeWidget()
        self.__list.setHeaderLabels(list(tab.columns))
        
        buttons = QHBoxLayout()
        buttons.addWidget(QPushButton(QIcon.fromTheme("edit-delete"), "Delete"))
        buttons.addWidget(QPushButton(QIcon.fromTheme("document-save"), "Save"))
        buttons.addWidget(QPushButton(QIcon.fromTheme("document-new"), "New"))
        layout.addLayout(buttons)
        
        layout.addWidget(self.__list)
        self.setLayout(layout)
        self.__update_list()
        self._update_values()
    
    def __update_list(self):
        self.__list.clear()
        for row in self._tab.rows:
            self.__list.addTopLevelItem(QTreeWidgetItem(row))
        if self._tab.current_index is not None:
            item = self.__list.topLevelItem(self._tab.current_index)
            self.__list.setCurrentItem(item)
        else:
            self.__list.setCurrentItem(None)
