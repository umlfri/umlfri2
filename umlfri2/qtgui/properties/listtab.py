from PySide.QtGui import QVBoxLayout, QTreeWidget, QHBoxLayout, QPushButton, QIcon

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
    
    def __get_icon(self, type):
        return 
