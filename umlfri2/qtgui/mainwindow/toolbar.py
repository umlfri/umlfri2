from PySide.QtGui import QToolBar, QAction, QKeySequence, QIcon


class MainToolBar(QToolBar):
    def __init__(self, main_window):
        super().__init__()
        self.__main_window = main_window
        
        self.__shortcuts = {}
        
        self.__new = self.__add_toolbar_item(QKeySequence.New, "document-new", self.__new_action)
        self.__open = self.__add_toolbar_item(QKeySequence.Open, "document-open", self.__open_action)
        self.__save = self.__add_toolbar_item(QKeySequence.Save, "document-save", self.__save_action)
        
        self.reload_texts()
    
    def __add_toolbar_item(self, shortcut, icon, action=None):
        ret = QAction(None)
        if shortcut is not None:
            self.__shortcuts[ret] = QKeySequence(shortcut)
        if icon is not None:
            ret.setIcon(QIcon.fromTheme(icon))
        if action is not None:
            ret.triggered.connect(action)
        self.addAction(ret)
        return ret
    
    def __new_action(self, checked=False):
        self.__main_window.new_project()
    
    def __open_action(self, checked=False):
        self.__main_window.open_solution()
    
    def __save_action(self, checked=False):
        self.__main_window.save_solution()
    
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
