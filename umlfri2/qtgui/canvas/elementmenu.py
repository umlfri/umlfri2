from functools import partial

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction

from umlfri2.application import Application
from umlfri2.application.commands.diagram import HideElementsCommand, ChangeZOrderCommand, ZOrderDirection, \
    PasteSnippetCommand, DuplicateSnippetCommand, ShowConnectionCommand
from umlfri2.application.commands.model import DeleteElementsCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT, Z_ORDER_RAISE, Z_ORDER_LOWER, Z_ORDER_TO_BOTTOM, Z_ORDER_TO_TOP, \
    PASTE_DUPLICATE
from umlfri2.metamodel import DefaultElementAction
from umlfri2.qtgui.base import image_loader
from ..base.contextmenu import ContextMenu
from ..properties import PropertiesDialog


class CanvasElementMenu(ContextMenu):
    def __init__(self, main_window, drawing_area, elements):
        super().__init__()
        
        self.__main_window = main_window
        self.__elements = tuple(elements)
        self.__drawing_area = drawing_area
        self.__diagram = drawing_area.diagram
        
        translation = self.__diagram.type.metamodel.get_translation(Application().language.current_language)
        
        something_above = False
        something_below = False
        for element in self.__elements:
            if self.__diagram.get_visual_above(Application().ruler, element) is not None:
                something_above = True
            if self.__diagram.get_visual_below(Application().ruler, element) is not None:
                something_below = True
        
        first_diagram_item = None
        
        if any(element.object.diagram_count > 0 for element in self.__elements):
            diagrams_menu = self._add_sub_menu_item(_("Show Diagram"))
            
            for element in self.__elements:
                for diagram in element.object.diagrams:
                    if diagram is not self.__diagram:
                        diagram_item = QAction(diagram.get_display_name(), diagrams_menu)
                        diagram_item.setIcon(image_loader.load_icon(diagram.type.icon))
                        diagram_item.triggered.connect(partial(self.__show_diagram, diagram))
                        diagrams_menu.addAction(diagram_item)
                        if first_diagram_item is None:
                            first_diagram_item = diagram_item
        else:
            self._add_sub_menu_item(_("Show Diagram"), enabled=False)

        self.addSeparator()
        
        if drawing_area.can_copy_snippet:
            self._add_menu_item("edit-cut", _("Cut"), QKeySequence.Cut, self.__cut_action)
        else:
            self._add_menu_item("edit-cut", _("Cut"), QKeySequence.Cut)
        
        if drawing_area.can_copy_snippet:
            self._add_menu_item("edit-copy", _("Copy"), QKeySequence.Copy, self.__copy_action)
        else:
            self._add_menu_item("edit-copy", _("Copy"), QKeySequence.Copy)
        
        if drawing_area.can_paste_snippet:
            self._add_menu_item("edit-paste", _("Paste"), QKeySequence.Paste, self.__paste_action)
        else:
            self._add_menu_item("edit-paste", _("Paste"), QKeySequence.Paste)
        
        if drawing_area.can_paste_snippet_duplicate:
            self._add_menu_item("edit-paste", _("Paste Duplicate"), PASTE_DUPLICATE, self.__duplicate_action)
        else:
            self._add_menu_item("edit-paste", _("Paste Duplicate"), PASTE_DUPLICATE)
        
        self.addSeparator()
        
        self._add_menu_item(None, _("Hide"), QKeySequence.Delete, self.__hide)
        self._add_menu_item("edit-delete", _("Delete"), DELETE_FROM_PROJECT, self.__delete)


        connections_to_show = []
        if len(self.__elements) == 1:
            for connection in self.__elements[0].object.connections:
                if not self.__diagram.contains(connection):
                    other = connection.get_other_end(self.__elements[0].object)
                    if self.__diagram.contains(other):
                        connections_to_show.append((connection, other))
        if connections_to_show:
            show_menu = self._add_sub_menu_item(_("Show Connection"))

            for connection, element in connections_to_show:
                self._add_menu_item(
                    None,
                    _("{0} to '{1}'").format(translation.translate(connection.type), element.get_display_name()),
                    None,
                    partial(self.__show_connection, connection),
                    show_menu
                )
        else:
            show_menu = self._add_sub_menu_item(_("Show Connection"), enabled=False)
        
        self.addSeparator()
        
        if len(self.__elements) == 1:
            self._add_menu_item(None, _("Find in the Project Tree"), None, self.__show_in_project)
        else:
            self._add_menu_item(None, _("Find in the Project Tree"), None)
        
        if something_above or something_below:
            z_order_menu = self._add_sub_menu_item(_("Z-Order"))
            
            if something_below:
                self._add_menu_item("go-down", _("Lower"), Z_ORDER_LOWER, self.__z_order_back, z_order_menu)
            else:
                self._add_menu_item("go-down", _("Lower"), Z_ORDER_LOWER, None, z_order_menu)
            
            if something_above:
                self._add_menu_item("go-up", _("Raise"), Z_ORDER_RAISE, self.__z_order_forward, z_order_menu)
            else:
                self._add_menu_item("go-up", _("Raise"), Z_ORDER_RAISE, None, z_order_menu)
            
            if something_below:
                self._add_menu_item("go-bottom", _("Lower to Bottom"), Z_ORDER_TO_BOTTOM, self.__z_order_bottom, z_order_menu)
            else:
                self._add_menu_item("go-bottom", _("Lower to Bottom"), Z_ORDER_TO_BOTTOM, None, z_order_menu)
            
            if something_above:
                self._add_menu_item("go-top", _("Raise to Top"), Z_ORDER_TO_TOP, self.__z_order_top, z_order_menu)
            else:
                self._add_menu_item("go-top", _("Raise to Top"), Z_ORDER_TO_TOP, None, z_order_menu)
        else:
            self._add_sub_menu_item(_("Z-order"), False)
        
        if len(self.__elements) == 1 and self.__elements[0].object.has_ufl_dialog:
            properties = self._add_menu_item(None, _("Properties..."), None, self.__edit_properties)
        else:
            properties = self._add_menu_item(None, _("Properties..."), None)
        
        if len(self.__elements) == 1:
            if self.__elements[0].object.type.default_action == DefaultElementAction.subdiagram:
                if first_diagram_item is not None:
                    diagrams_menu.setDefaultAction(first_diagram_item)
                else:
                    self.setDefaultAction(properties)
            else:
                self.setDefaultAction(properties)
    
    def __show_diagram(self, diagram, checked=False):
        Application().tabs.select_tab(diagram)
    
    def __cut_action(self, checked=False):
        self.__drawing_area.copy_snippet()
        
        command = HideElementsCommand(self.__diagram, self.__elements)
        Application().commands.execute(command)
    
    def __copy_action(self, checked=False):
        self.__drawing_area.copy_snippet()
    
    def __paste_action(self, checked=False):
        command = PasteSnippetCommand(self.__diagram, Application().clipboard)
        Application().commands.execute(command)
        self.__drawing_area.selection.select(command.element_visuals)
    
    def __duplicate_action(self, checked=False):
        command = DuplicateSnippetCommand(self.__diagram, Application().clipboard)
        Application().commands.execute(command)
        self.__drawing_area.selection.select(command.element_visuals)
    
    def __hide(self, checked=False):
        command = HideElementsCommand(self.__diagram, self.__elements)
        
        Application().commands.execute(command)
    
    def __delete(self, checked=False):
        command = DeleteElementsCommand(tuple(element.object for element in self.__elements))
        
        Application().commands.execute(command)
        
    def __show_connection(self, connection, checked):
        command = ShowConnectionCommand(self.__diagram, connection)

        Application().commands.execute(command)
    
    def __show_in_project(self, checked=False):
        Application().select_item(self.__elements[0].object)
    
    def __z_order_back(self, checked=False):
        command = ChangeZOrderCommand(self.__diagram, self.__elements, ZOrderDirection.bellow)
        
        Application().commands.execute(command)
    
    def __z_order_forward(self, checked=False):
        command = ChangeZOrderCommand(self.__diagram, self.__elements, ZOrderDirection.above)
        
        Application().commands.execute(command)
    
    def __z_order_bottom(self, checked=False):
        command = ChangeZOrderCommand(self.__diagram, self.__elements, ZOrderDirection.bottom)
        
        Application().commands.execute(command)
    
    def __z_order_top(self, checked=False):
        command = ChangeZOrderCommand(self.__diagram, self.__elements, ZOrderDirection.top)
        
        Application().commands.execute(command)
    
    def __edit_properties(self, checked=False):
        PropertiesDialog.open_for(self.__main_window, self.__elements[0].object)
