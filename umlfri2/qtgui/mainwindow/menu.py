from PySide.QtGui import QMenuBar, QAction, QMenu, QKeySequence, QIcon


class MainWindowMenu(QMenuBar):
    def __init__(self, main_window): 
        super().__init__()
        
        self.__main_window = main_window
        
        # FILE MENU
        self.__file = QAction(None)
        self.addAction(self.__file)
        file_menu = QMenu()
        self.__file.setMenu(file_menu)

        self.__file_new = self.__add_menu_item(file_menu, "Ctrl+N", "document-new")
        self.__file_open = self.__add_menu_item(file_menu, "Ctrl+O", "document-open")
        self.__file_save = self.__add_menu_item(file_menu, "Ctrl+S", "document-save")
        self.__file_save_as = self.__add_menu_item(file_menu, None, "document-save-as")
        file_menu.addSeparator()
        self.__file_exit = self.__add_menu_item(file_menu, "Ctrl+Q", "application-exit")
        
        # VIEW MENU
        self.__view = QAction(None)
        self.addAction(self.__view)
        view_menu = QMenu()
        self.__view.setMenu(view_menu)
        
        for action in main_window.get_dock_actions():
            view_menu.addAction(action)
        
        self.reload_texts()

    def __add_menu_item(self, menu, shortcut, icon):
        ret = QAction(None)
        if shortcut is not None:
            ret.setShortcut(QKeySequence(shortcut))
        if icon is not None:
            ret.setIcon(QIcon.fromTheme(icon))
        menu.addAction(ret)
        return ret

    def reload_texts(self):
        self.__file.setText(_("&File"))
        self.__file_new.setText(_("&New"))
        self.__file_open.setText(_("&Open"))
        self.__file_save.setText(_("&Save"))
        self.__file_save_as.setText(_("Save &as"))
        self.__file_exit.setText(_("&Quit"))
        
        self.__view.setText(_("&View"))
