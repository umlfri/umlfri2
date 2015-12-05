from PySide.QtGui import QToolBar, QAction, QKeySequence, QIcon, QMenu
from umlfri2.application import Application


UNDO_REDO_COUNT = 10


class MainToolBar(QToolBar):
    def __init__(self, main_window):
        super().__init__()
        self.__main_window = main_window
        
        self.__shortcuts = {}
        
        self.__new = self.__add_toolbar_item(QKeySequence.New, "document-new", self.__new_action)
        self.__open = self.__add_toolbar_item(QKeySequence.Open, "document-open", self.__open_action)
        self.__save = self.__add_toolbar_item(QKeySequence.Save, "document-save", self.__save_action)
        
        self.addSeparator()
        
        self.__undo_menu = QMenu()
        self.__redo_menu = QMenu()
        self.__undo_menu.aboutToShow.connect(self.__undo_menu_show)
        self.__redo_menu.aboutToShow.connect(self.__redo_menu_show)
        
        self.__undo = self.__add_toolbar_item(QKeySequence.Undo, "edit-undo", self.__undo_action, self.__undo_menu)
        self.__redo = self.__add_toolbar_item(QKeySequence.Redo, "edit-redo", self.__redo_action, self.__redo_menu)
        
        self.reload_texts()
        
        Application().event_dispatcher.register(None, lambda event: self.__refresh_enable())
        self.__refresh_enable()
    
    def __add_toolbar_item(self, shortcut, icon, action=None, menu=None):
        ret = QAction(None)
        if shortcut is not None:
            self.__shortcuts[ret] = QKeySequence(shortcut)
        if icon is not None:
            ret.setIcon(QIcon.fromTheme(icon))
        if action is not None:
            ret.triggered.connect(action)
        if menu is not None:
            ret.setMenu(menu)
        self.addAction(ret)
        return ret
    
    def __new_action(self, checked=False):
        self.__main_window.new_project()
    
    def __open_action(self, checked=False):
        self.__main_window.open_solution()
    
    def __save_action(self, checked=False):
        self.__main_window.save_solution()
    
    def __undo_action(self, checked=False):
        pass
    
    def __undo_menu_show(self):
        self.__undo_menu.clear()
        
        for cmd in Application().commands.get_undo_stack(UNDO_REDO_COUNT):
            self.__undo_menu.addAction(cmd.description)
    
    def __redo_action(self, checked=False):
        pass
    
    def __redo_menu_show(self):
        self.__redo_menu.clear()
        
        for cmd in Application().commands.get_redo_stack(UNDO_REDO_COUNT):
            self.__redo_menu.addAction(cmd.description)
    
    def __refresh_enable(self):
        self.__save.setEnabled(Application().can_save_solution)
        
        self.__undo.setEnabled(Application().commands.can_undo)
        self.__redo.setEnabled(Application().commands.can_redo)
    
    def reload_texts(self):
        self.setWindowTitle(_("Toolbar"))
        self.__set_toolbar_item_text(self.__new, _("New"))
        self.__set_toolbar_item_text(self.__open, _("Open"))
        self.__set_toolbar_item_text(self.__save, _("Save"))
    
    def __set_toolbar_item_text(self, item, text):
        item.setText(text)
        
        tooltip = text
        if item in self.__shortcuts:
            tooltip += " ({0})".format(self.__shortcuts[item].toString())
        
        item.setToolTip(tooltip)
