import os.path
from functools import partial

from PySide.QtGui import QMenuBar, QAction, QMenu, QKeySequence, QIcon, QFileDialog
from umlfri2.application import Application
from umlfri2.application.commands.diagram import HideElementsCommand, PasteSnippetCommand, DuplicateSnippetCommand
from umlfri2.application.events.application.languagechanged import LanguageChangedEvent
from umlfri2.constants.keys import FULL_SCREEN, ZOOM_ORIGINAL, PASTE_DUPLICATE, COPY_IMAGE
from umlfri2.constants.languages import AVAILABLE_LANGUAGES
from umlfri2.qtgui.fullscreen import FullScreenDiagram
from umlfri2.qtgui.rendering import ImageExport, ExportDialog


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
        
        edit_menu.addSeparator()
        
        self.__edit_cut = self.__add_menu_item(edit_menu, QKeySequence.Cut, "edit-cut", self.__edit_cut_action)
        self.__edit_copy = self.__add_menu_item(edit_menu, QKeySequence.Copy, "edit-copy", self.__edit_copy_action)
        self.__edit_copy_image = self.__add_menu_item(edit_menu, COPY_IMAGE, None, self.__edit_copy_image_action)
        self.__edit_paste = self.__add_menu_item(edit_menu, QKeySequence.Paste, "edit-paste", self.__edit_paste_action)
        self.__edit_duplicate = self.__add_menu_item(edit_menu, PASTE_DUPLICATE, "edit-paste",
                                                     self.__edit_duplicate_action)
        
        edit_menu.addSeparator()
        
        self.__edit_select_all = self.__add_menu_item(edit_menu, QKeySequence.SelectAll, "edit-select-all",
                                                      self.__edit_select_all_action)
        
        self.__diagram, diagram_menu = self.__add_menu()
        self.__diagram_export = self.__add_menu_item(diagram_menu, None, None, self.__diagram_export_action)
        self.__diagram_full_screen = self.__add_menu_item(diagram_menu, FULL_SCREEN, "view-fullscreen",
                                                          self.__diagram_full_screen_action)
        
        self.__tools, tools_menu = self.__add_menu()
        self.__tools_languages_menu = QMenu()
        self.__tools_languages_menu.aboutToShow.connect(self.__tools_languages_menu_populate)
        self.__tools_languages = self.__add_submenu_item(tools_menu, None, None, self.__tools_languages_menu)
        
        # VIEW MENU
        self.__view, view_menu = self.__add_menu()
        
        self.__view_zoom_in = self.__add_menu_item(view_menu, QKeySequence.ZoomIn, "zoom-in",
                                                   self.__view_zoom_in_action)
        self.__view_zoom_out = self.__add_menu_item(view_menu, QKeySequence.ZoomOut, "zoom-out",
                                                       self.__view_zoom_out_action)
        self.__view_zoom_original = self.__add_menu_item(view_menu, ZOOM_ORIGINAL, "zoom-original",
                                                            self.__view_zoom_original_action)
        
        view_menu.addSeparator()
        
        for action in main_window.get_dock_actions():
            view_menu.addAction(action)
        
        view_menu.addSeparator()
            
        for action in main_window.get_toolbar_actions():
            view_menu.addAction(action)
        
        Application().event_dispatcher.subscribe(None, lambda event: self.__refresh_enable())
        Application().event_dispatcher.subscribe(LanguageChangedEvent, lambda event: self.__reload_texts())
        
        self.__reload_texts()
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
    
    def __add_submenu_item(self, menu, shortcut, icon, submenu):
        ret = QAction(None)
        if shortcut is not None:
            ret.setShortcut(QKeySequence(shortcut))
        if icon is not None:
            ret.setIcon(QIcon.fromTheme(icon))
        ret.setMenu(submenu)
        menu.addAction(ret)
        return ret
    
    def __refresh_enable(self):
        tab = Application().tabs.current_tab
        
        self.__file_save.setEnabled(Application().can_save_solution)
        self.__file_save_as.setEnabled(Application().can_save_solution_as)
        
        self.__edit_undo.setEnabled(Application().commands.can_undo)
        self.__edit_redo.setEnabled(Application().commands.can_redo)
        self.__edit_select_all.setEnabled(tab is not None)
        
        self.__diagram.setEnabled(tab is not None)
        
        if tab is None:
            self.__edit_cut.setEnabled(False)
            self.__edit_copy.setEnabled(False)
            self.__edit_copy_image.setEnabled(False)
            self.__edit_paste.setEnabled(False)
            self.__edit_duplicate.setEnabled(False)
            
            self.__view_zoom_in.setEnabled(False)
            self.__view_zoom_out.setEnabled(False)
            self.__view_zoom_original.setEnabled(False)
        else:
            self.__edit_cut.setEnabled(tab.drawing_area.can_copy_snippet)
            self.__edit_copy.setEnabled(tab.drawing_area.can_copy_snippet)
            self.__edit_copy_image.setEnabled(tab.drawing_area.selection.is_element_selected)
            self.__edit_paste.setEnabled(tab.drawing_area.can_paste_snippet)
            self.__edit_duplicate.setEnabled(tab.drawing_area.can_paste_snippet_duplicate)
            
            self.__view_zoom_in.setEnabled(tab.drawing_area.can_zoom_in)
            self.__view_zoom_out.setEnabled(tab.drawing_area.can_zoom_out)
            self.__view_zoom_original.setEnabled(tab.drawing_area.can_zoom_original)
    
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
    
    def __edit_copy_action(self, checked=False):
        drawing_area = Application().tabs.current_tab.drawing_area
        
        drawing_area.copy_snippet()
    
    def __edit_copy_image_action(self, checked=False):
        dialog = ExportDialog(self.__main_window)
        
        if dialog.exec_() == ExportDialog.Rejected:
            return
        
        selection = Application().tabs.current_tab.drawing_area.selection
        exp = ImageExport(selection, dialog.zoom, dialog.padding, dialog.transparent)
        exp.export_to_clipboard()
    
    def __edit_cut_action(self, checked=False):
        drawing_area = Application().tabs.current_tab.drawing_area
        
        drawing_area.copy_snippet()
        
        command = HideElementsCommand(drawing_area.diagram, drawing_area.selection.selected_elements)
        Application().commands.execute(command)
    
    def __edit_paste_action(self, checked=False):
        drawing_area = Application().tabs.current_tab.drawing_area
        
        command = PasteSnippetCommand(drawing_area.diagram, Application().clipboard)
        Application().commands.execute(command)
        drawing_area.selection.select(command.element_visuals)
    
    def __edit_duplicate_action(self, checked=False):
        drawing_area = Application().tabs.current_tab.drawing_area
        
        command = DuplicateSnippetCommand(drawing_area.diagram, Application().clipboard)
        Application().commands.execute(command)
        drawing_area.selection.select(command.element_visuals)
    
    def __edit_select_all_action(self, checked=False):
        Application().tabs.current_tab.drawing_area.selection.select_all()
    
    def __diagram_export_action(self, checked=False):
        dialog = ExportDialog(self.__main_window)
        
        if dialog.exec_() == ExportDialog.Rejected:
            return
        
        diagram = Application().tabs.current_tab.drawing_area.diagram
        exp = ImageExport(diagram, dialog.zoom, dialog.padding, dialog.transparent)
        filters = []
        default = exp.default_format
        default_filter = None
        for formats in exp.supported_formats():
            file_names = " ".join("*.{0}".format(i) for i in formats)
            filter_text = _("{0} image").format(formats[0].upper()) + "({0})".format(file_names)
            filters.append((filter_text, formats[0]))
            if default in formats:
                default_filter = filter_text
        
        file_name, filter = QFileDialog.getSaveFileName(
            self,
            caption=_("Export Diagram"),
            filter=";;".join(text for text, format in filters),
            selectedFilter=default_filter
        )
        
        if file_name:
            for text, formats in filters:
                if text == filter:
                    break
            else:
                raise Exception
            
            if '.' not in os.path.basename(file_name):
                file_name = file_name + '.' + formats
            
            # TODO: export to python file?
            exp.export(file_name, formats)
    
    def __diagram_full_screen_action(self):
        window = FullScreenDiagram(self.__main_window, Application().tabs.current_tab.drawing_area)
        window.showFullScreen()
    
    def __tools_languages_menu_populate(self):
        selected_language = Application().selected_language
        
        self.__tools_languages_menu.clear()
        system_lang = self.__tools_languages_menu.addAction(_("System language"))
        system_lang.triggered.connect(partial(self.__tools_languages_menu_activate, None))
        system_lang.setCheckable(True)
        system_lang.setChecked(selected_language is None)
        
        self.__tools_languages_menu.addSeparator()
        
        for lang_id, label in AVAILABLE_LANGUAGES:
            language = self.__tools_languages_menu.addAction(label)
            language.triggered.connect(partial(self.__tools_languages_menu_activate, lang_id))
            language.setCheckable(True)
            language.setChecked(selected_language == lang_id)
    
    def __tools_languages_menu_activate(self, lang_id, checked=False):
        Application().change_language(lang_id)
    
    def __view_zoom_in_action(self, checked=False):
        Application().tabs.current_tab.drawing_area.zoom_in()
    
    def __view_zoom_out_action(self, checked=False):
        Application().tabs.current_tab.drawing_area.zoom_out()
    
    def __view_zoom_original_action(self, checked=False):
        Application().tabs.current_tab.drawing_area.zoom_original()
    
    def __reload_texts(self):
        self.__file.setText(_("&File"))
        self.__file_new.setText(_("&New"))
        self.__file_open.setText(_("&Open"))
        self.__file_save.setText(_("&Save"))
        self.__file_save_as.setText(_("Save &as"))
        self.__file_exit.setText(_("&Quit"))
        
        self.__edit.setText(_("&Edit"))
        self.__edit_undo.setText(_("&Undo"))
        self.__edit_redo.setText(_("&Redo"))
        self.__edit_cut.setText(_("C&ut"))
        self.__edit_copy.setText(_("&Copy"))
        self.__edit_copy_image.setText(_("&Copy as Image"))
        self.__edit_paste.setText(_("&Paste"))
        self.__edit_duplicate.setText(_("Paste &Duplicate"))
        self.__edit_select_all.setText(_("Select &All"))
        
        self.__diagram.setText(_("&Diagram"))
        self.__diagram_export.setText(_("Export as &Image"))
        self.__diagram_full_screen.setText(_("Show Full &Screen"))
        
        self.__tools.setText(_("&Tools"))
        self.__tools_languages.setText(_("Change &Language"))
        
        self.__view.setText(_("&View"))
        self.__view_zoom_in.setText(_("Zoom &In"))
        self.__view_zoom_out.setText(_("Zoom &Out"))
        self.__view_zoom_original.setText(_("O&riginal Zoom"))
