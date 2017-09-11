from PyQt5.QtGui import QKeySequence

from umlfri2.application import Application
from ..startpage import StartPage
from ..base.contextmenu import ContextMenu


class TabContextMenu(ContextMenu):
    def __init__(self, tab_bar, tab_index, tab_widget):
        super().__init__()
        self.__tab_bar = tab_bar
        self.__tab_index = tab_index
        self.__tab_widget = tab_widget
        
        if tab_bar.count() == 1 and isinstance(tab_widget, StartPage):
            can_close = False
        else:
            can_close = True
        
        if can_close:
            self._add_menu_item(None, _("Close Tab"), QKeySequence.Close, self.__close_tab)
            self._add_menu_item(None, _("Close All Tabs"), None, self.__close_all_tabs)
        else:
            self._add_menu_item(None, _("Close Tab"), QKeySequence.Close)
            self._add_menu_item(None, _("Close All Tabs"), None)
    
    def __close_tab(self, checked=False):
        self.__tab_bar.tabCloseRequested.emit(self.__tab_index)
    
    def __close_all_tabs(self, checked=False):
        Application().tabs.close_all()
