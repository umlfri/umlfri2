from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QVBoxLayout, QTreeWidget, QHBoxLayout, QPushButton, QTreeWidgetItem, QMessageBox, QShortcut

from umlfri2.constants.keys import MOVE_DOWN, MOVE_UP
from umlfri2.qtgui.base.hlinewidget import HLineWidget
from .tab import PropertyTab


class ListPropertyTab(PropertyTab):
    def __init__(self, window, tab, lonely=False): 
        super().__init__(window, tab)
        self.__disable_selection_handling = False
        
        layout = QVBoxLayout()
        if lonely:
            layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self._create_layout())
        
        layout.addWidget(HLineWidget())
        
        self.__list = QTreeWidget()
        headers = []
        for column in tab.columns:
            headers.append(column or _('Value'))
        self.__list.setHeaderLabels(headers)
        self.__list.itemSelectionChanged.connect(self.__item_changed)
        
        buttons = QHBoxLayout()
        
        def add_icon_button(icon, alt_text, shortcut, fnc):
            icon_obj = QIcon.fromTheme(icon)
            if icon_obj.isNull():
                button = QPushButton(alt_text)
            else:
                button = QPushButton(icon_obj, "")
            button.setToolTip(alt_text + " (" + shortcut + ")")
            QShortcut(QKeySequence(shortcut), self).activated.connect(fnc)
            button.clicked.connect(fnc)
            buttons.addWidget(button)
            return button
        
        def add_text_button(icon, text, fnc):
            button = QPushButton(QIcon.fromTheme(icon), text)
            button.clicked.connect(fnc)
            buttons.addWidget(button)
            return button

        self.__move_up_button = add_icon_button("go-up", _("Move up"), MOVE_UP, self.__move_up)
        self.__move_down_button = add_icon_button("go-down", _("Move down"), MOVE_DOWN, self.__move_down)
        
        buttons.addStretch()
        
        self.__delete_button = add_text_button("edit-delete", _("&Delete"), self.__delete)
        self.__save_button = add_text_button("document-save", _("&Save"), self.__save)
        self.__new_button = add_text_button("document-new", _("&New"), self.__new)
        
        layout.addLayout(buttons)
        
        layout.addWidget(self.__list, stretch=1)
        self.setLayout(layout)
        self.refresh()
    
    def __update_list(self):
        self.__disable_selection_handling = True
        try:
            self.__list.clear()
            for row in self._tab.rows:
                self.__list.addTopLevelItem(QTreeWidgetItem(row))
            self.__update_list_current_index()
        finally:
            self.__disable_selection_handling = False

    def __update_list_current_index(self):
        if self._tab.current_index is not None:
            item = self.__list.topLevelItem(self._tab.current_index)
            self.__list.setCurrentItem(item)
        else:
            self.__list.setCurrentItem(None)

    def __update_buttons(self):
        self.__move_down_button.setEnabled(self._tab.can_move_down)
        self.__move_up_button.setEnabled(self._tab.can_move_up)
        self.__new_button.setEnabled(self._tab.can_new)
        self.__save_button.setEnabled(self._tab.can_save)
        self.__delete_button.setEnabled(self._tab.can_delete)
    
    def __item_changed(self):
        if self.__disable_selection_handling:
            return
        items = self.__list.selectedItems()
        if items:
            index = self.__list.indexOfTopLevelItem(items[0])
        else:
            index = None
        
        if index == self._tab.current_index:
            return
        
        if self._tab.should_save:
            if not self.handle_needed_save():
                if self._tab.current_index is None:
                    self.__list.setCurrentItem(None)
                else:
                    self.__list.setCurrentItem(self.__list.topLevelItem(self._tab.current_index))
                return
        
        self._tab.change_current_index(index)
        self._update_values()
        self.__update_buttons()
        self.__update_list_current_index()
        self._focus_first()
    
    def __new(self):
        if self._tab.should_save:
            if not self.handle_needed_save():
                return
        
        self._tab.new()
        self._update_values()
        self.__update_buttons()
        self.__update_list_current_index()
        self._focus_first()
    
    def __save(self, deselect=False):
        self._tab.save()
        if deselect:
            self._tab.change_current_index(None)
        self.refresh()
        if self._tab.current_index is None:
            self._focus_first()
    
    def __discard(self, deselect=False):
        self._tab.discard()
        if deselect:
            self._tab.change_current_index(None)
        self.refresh()
    
    def __delete(self):
        self._tab.delete()
        self.refresh()
    
    def __move_up(self):
        self._tab.move_up()
        self.refresh()
    
    def __move_down(self):
        self._tab.move_down()
        self.refresh()
    
    def handle_needed_save(self):
        message_box = QMessageBox(self)
        message_box.setWindowModality(Qt.WindowModal)
        message_box.setIcon(QMessageBox.Question)
        message_box.setWindowTitle(_("Data changed"))
        message_box.setText(_("The data on this tab has been modified."))
        message_box.setInformativeText(_("Do you want to save the data?"))
        message_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        message_box.setDefaultButton(QMessageBox.Save)
        message_box.button(QMessageBox.Save).setText(_("Save"))
        message_box.button(QMessageBox.Discard).setText(_("Discard"))
        message_box.button(QMessageBox.Cancel).setText(_("Cancel"))
        
        resp = message_box.exec_()
        
        if resp == QMessageBox.Cancel:
            return False
        
        if resp == QMessageBox.Save:
            self.__save(deselect=True)
        
        if resp == QMessageBox.Discard:
            self.__discard()
        
        return True
    
    def refresh(self):
        self.__update_list()
        self._update_values()
        self.__update_buttons()
