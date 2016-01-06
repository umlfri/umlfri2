from functools import partial

from PySide.QtGui import QToolBar, QAction, QKeySequence, QIcon, QMenu
from umlfri2.application import Application
from umlfri2.application.commands.diagram import HideElementsCommand, PasteSnippetCommand
from umlfri2.application.events.application import LanguageChangedEvent

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
        
        self.__cut = self.__add_toolbar_item(QKeySequence.Cut, "edit-cut", self.__cut_action)
        self.__copy = self.__add_toolbar_item(QKeySequence.Copy, "edit-copy", self.__copy_action)
        self.__paste = self.__add_toolbar_item(QKeySequence.Paste, "edit-paste", self.__paste_action)
        
        self.addSeparator()
        
        self.__undo_menu = QMenu()
        self.__redo_menu = QMenu()
        self.__undo_menu.aboutToShow.connect(self.__undo_menu_show)
        self.__redo_menu.aboutToShow.connect(self.__redo_menu_show)
        
        self.__undo = self.__add_toolbar_item(QKeySequence.Undo, "edit-undo", partial(self.__undo_action, 1),
                                              self.__undo_menu)
        self.__redo = self.__add_toolbar_item(QKeySequence.Redo, "edit-redo", partial(self.__redo_action, 1),
                                              self.__redo_menu)
        
        self.addSeparator()
        
        self.__zoom_in = self.__add_toolbar_item(QKeySequence.ZoomIn, "zoom-in", self.__zoom_in_action)
        self.__zoom_out = self.__add_toolbar_item(QKeySequence.ZoomOut, "zoom-out", self.__zoom_out_action)
        
        Application().event_dispatcher.subscribe(LanguageChangedEvent, lambda event: self.__reload_texts())
        
        self.__reload_texts()
        
        Application().event_dispatcher.subscribe(None, lambda event: self.__refresh_enable())
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
    
    def __copy_action(self, checked=False):
        drawing_area = Application().tabs.current_tab.drawing_area
        
        drawing_area.copy_snippet()
    
    def __cut_action(self, checked=False):
        drawing_area = Application().tabs.current_tab.drawing_area
        
        drawing_area.copy_snippet()
        
        command = HideElementsCommand(drawing_area.diagram, drawing_area.selection.selected_elements)
        Application().commands.execute(command)
    
    def __paste_action(self, checked=False):
        drawing_area = Application().tabs.current_tab.drawing_area
        
        command = PasteSnippetCommand(drawing_area.diagram, Application().clipboard)
        Application().commands.execute(command)
    
    def __undo_action(self, count, checked=False):
        Application().commands.undo(count)
    
    def __undo_menu_show(self):
        self.__undo_menu.clear()
        
        for no, cmd in enumerate(Application().commands.get_undo_stack(UNDO_REDO_COUNT)):
            action = self.__undo_menu.addAction(cmd.description)
            action.triggered.connect(partial(self.__undo_action, no + 1))
        
        if Application().commands.undo_stack_size > UNDO_REDO_COUNT:
            self.__undo_menu.addAction("...").setEnabled(False)
    
    def __redo_action(self, count, checked=False):
        Application().commands.redo(count)
    
    def __redo_menu_show(self):
        self.__redo_menu.clear()
        
        for no, cmd in enumerate(Application().commands.get_redo_stack(UNDO_REDO_COUNT)):
            action = self.__redo_menu.addAction(cmd.description)
            action.triggered.connect(partial(self.__redo_action, no + 1))
        
        if Application().commands.redo_stack_size > UNDO_REDO_COUNT:
            self.__redo_menu.addAction("...").setEnabled(False)
    
    def __zoom_in_action(self, checked=False):
        Application().tabs.current_tab.drawing_area.zoom_in()
    
    def __zoom_out_action(self, checked=False):
        Application().tabs.current_tab.drawing_area.zoom_out()
    
    def __refresh_enable(self):
        self.__save.setEnabled(Application().can_save_solution)
        
        self.__undo.setEnabled(Application().commands.can_undo)
        self.__redo.setEnabled(Application().commands.can_redo)
        
        tab = Application().tabs.current_tab
        if tab is None:
            self.__cut.setEnabled(False)
            self.__copy.setEnabled(False)
            self.__paste.setEnabled(False)
            
            self.__zoom_in.setEnabled(False)
            self.__zoom_out.setEnabled(False)
        else:
            self.__cut.setEnabled(tab.drawing_area.can_copy_snippet)
            self.__copy.setEnabled(tab.drawing_area.can_copy_snippet)
            self.__paste.setEnabled(tab.drawing_area.can_paste_snippet)
            
            self.__zoom_in.setEnabled(tab.drawing_area.can_zoom_in)
            self.__zoom_out.setEnabled(tab.drawing_area.can_zoom_out)
    
    def __reload_texts(self):
        self.setWindowTitle(_("Toolbar"))
        self.__set_toolbar_item_text(self.__new, _("New"))
        self.__set_toolbar_item_text(self.__open, _("Open"))
        self.__set_toolbar_item_text(self.__save, _("Save"))
        
        self.__set_toolbar_item_text(self.__cut, _("Cut"))
        self.__set_toolbar_item_text(self.__copy, _("Copy"))
        self.__set_toolbar_item_text(self.__paste, _("Paste"))
        
        self.__set_toolbar_item_text(self.__undo, _("Undo"))
        self.__set_toolbar_item_text(self.__redo, _("Redo"))
        
        self.__set_toolbar_item_text(self.__zoom_in, _("Zoom In"))
        self.__set_toolbar_item_text(self.__zoom_out, _("Zoom Out"))
    
    def __set_toolbar_item_text(self, item, text):
        item.setText(text)
        
        tooltip = text
        if item in self.__shortcuts:
            tooltip += " ({0})".format(self.__shortcuts[item].toString())
        
        item.setToolTip(tooltip)
