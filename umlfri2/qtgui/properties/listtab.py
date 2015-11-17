from PySide.QtGui import QVBoxLayout, QTreeWidget, QHBoxLayout, QPushButton, QIcon, QTreeWidgetItem
from ..base.hlinewidget import HLineWidget
from .tab import PropertyTab


class ListPropertyTab(PropertyTab):
    def __init__(self, window, tab): 
        super().__init__(window, tab)
        self.__disable_selection_handling = False
        
        layout = QVBoxLayout()
        layout.addLayout(self._create_layout)
        
        layout.addWidget(HLineWidget())
        
        self.__list = QTreeWidget()
        self.__list.setHeaderLabels(list(tab.columns))
        self.__list.itemSelectionChanged.connect(self.__item_changed)
        
        buttons = QHBoxLayout()
        self.__delete_button = QPushButton(QIcon.fromTheme("edit-delete"), "&Delete")
        self.__delete_button.clicked.connect(self.__delete)
        buttons.addWidget(self.__delete_button)
        self.__save_button = QPushButton(QIcon.fromTheme("document-save"), "&Save")
        self.__save_button.clicked.connect(self.__save)
        buttons.addWidget(self.__save_button)
        self.__new_button = QPushButton(QIcon.fromTheme("document-new"), "&New")
        self.__new_button.clicked.connect(self.__new)
        buttons.addWidget(self.__new_button)
        layout.addLayout(buttons)
        
        layout.addWidget(self.__list)
        self.setLayout(layout)
        self.__update_list()
        self._update_values()
        self.__update_buttons()
    
    def __update_list(self):
        self.__disable_selection_handling = True
        try:
            self.__list.clear()
            for row in self._tab.rows:
                self.__list.addTopLevelItem(QTreeWidgetItem(row))
            if self._tab.current_index is not None:
                item = self.__list.topLevelItem(self._tab.current_index)
                self.__list.setCurrentItem(item)
            else:
                self.__list.setCurrentItem(None)
        finally:
            self.__disable_selection_handling = False
    
    def __update_buttons(self):
        self.__new_button.setEnabled(self._tab.can_new)
        self.__save_button.setEnabled(self._tab.can_save)
        self.__delete_button.setEnabled(self._tab.can_delete)
    
    def __item_changed(self):
        if self.__disable_selection_handling:
            return
        items = self.__list.selectedItems()
        if items:
            index = self.__list.indexOfTopLevelItem(items[0])
            self._tab.current_index = index
        else:
            self._tab.current_index = None
        self._update_values()
        self.__update_buttons()
    
    def __new(self):
        self._tab.new()
        self._update_values()
        self.__update_buttons()
    
    def __save(self):
        self._tab.save()
        self.__update_list()
        self._update_values()
        self.__update_buttons()
    
    def __delete(self):
        self._tab.delete()
        self.__update_list()
        self._update_values()
        self.__update_buttons()
