from PySide.QtGui import QMenuBar, QAction, QMenu, QKeySequence, QIcon

from umlfri2.application import Application
from .newproject import NewProjectDialog


class MainWindowMenu(QMenuBar):
    def __init__(self, main_window): 
        super().__init__()
        
        self.__main_window = main_window
        
        # FILE MENU
        self.__file, file_menu = self.__add_menu()

        self.__file_new = self.__add_menu_item(file_menu, QKeySequence.New, "document-new", self.__file_new_action)
        self.__file_open = self.__add_menu_item(file_menu, QKeySequence.Open, "document-open", self.__file_open_action)
        self.__file_save = self.__add_menu_item(file_menu, QKeySequence.Save, "document-save", self.__file_save_action)
        self.__file_save_as = self.__add_menu_item(file_menu, QKeySequence.SaveAs, "document-save-as", self.__file_save_as_action)
        file_menu.addSeparator()
        self.__file_exit = self.__add_menu_item(file_menu, QKeySequence.Quit, "application-exit", self.__file_exit_action)
        
        # VIEW MENU
        self.__edit, edit_menu = self.__add_menu()
        self.__edit_undo = self.__add_menu_item(edit_menu, QKeySequence.Undo, "edit-undo", self.__edit_undo_action)
        self.__edit_redo = self.__add_menu_item(edit_menu, QKeySequence.Redo, "edit-redo", self.__edit_redo_action)
        
        # VIEW MENU
        self.__view, view_menu = self.__add_menu()
        
        for action in main_window.get_dock_actions():
            view_menu.addAction(action)
        
        view_menu.addSeparator()
            
        for action in main_window.get_toolbar_actions():
            view_menu.addAction(action)
        
        self.reload_texts()
        
        Application().event_dispatcher.register(None, lambda event: self.__refresh_enable())
        self.__refresh_enable()

    def __add_menu(self):
        menu_item = QAction(None)
        self.addAction(menu_item)
        menu = QMenu()
        menu_item.setMenu(menu)
        return menu_item, menu

    def __add_menu_item(self, menu, shortcut, icon, action=None):
        ret = QAction(None)
        if shortcut is not None:
            ret.setShortcut(QKeySequence(shortcut))
        if icon is not None:
            ret.setIcon(QIcon.fromTheme(icon))
        if action is not None:
            ret.triggered.connect(action)
        menu.addAction(ret)
        return ret
    
    def __refresh_enable(self):
        self.__file_save.setEnabled(Application().can_save_solution)
        self.__file_save_as.setEnabled(Application().can_save_solution_as)
        
        self.__edit_undo.setEnabled(Application().commands.can_undo)
        self.__edit_redo.setEnabled(Application().commands.can_redo)
    
    def __file_new_action(self, checked=False):
        self.__main_window.new_project()
    
    def __file_open_action(self, checked=False):
        self.__main_window.open_solution()
    
    def __file_save_action(self, checked=False):
        self.__main_window.save_solution()
    
    def __file_save_as_action(self, checked=False):
        self.__main_window.save_solution_as()
    
    def __file_exit_action(self, checked=False):
        self.__main_window.close()
    
    def __edit_undo_action(self, checked=False):
        Application().commands.undo()
    
    def __edit_redo_action(self, checked=False):
        Application().commands.redo()
    
    def reload_texts(self):
        self.__file.setText(_("&File"))
        self.__file_new.setText(_("&New"))
        self.__file_open.setText(_("&Open"))
        self.__file_save.setText(_("&Save"))
        self.__file_save_as.setText(_("Save &as"))
        self.__file_exit.setText(_("&Quit"))
        
        self.__edit.setText(_("&Edit"))
        self.__edit_undo.setText(_("&Undo"))
        self.__edit_redo.setText(_("&Redo"))
        
        self.__view.setText(_("&View"))
