from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTabWidget, QStyle, QShortcut

from umlfri2.application import Application
from umlfri2.application.events.application import LanguageChangedEvent
from umlfri2.application.events.model import ObjectDataChangedEvent
from umlfri2.application.events.tabs import OpenTabEvent, ChangedCurrentTabEvent, ClosedTabEvent
from umlfri2.model import Diagram
from umlfri2.qtgui.base import image_loader
from umlfri2.qtgui.canvas import ScrolledCanvasWidget, CanvasWidget
from .startpage import StartPage
from .tabcontextmenu import TabContextMenu


class Tabs(QTabWidget):
    def __init__(self, main_window):
        super().__init__()
        
        self.__main_window = main_window
        
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setDocumentMode(True)
        self.currentChanged.connect(self.__tab_changed)
        self.tabCloseRequested.connect(self.__tab_close_requested)

        self.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabBar().customContextMenuRequested.connect(self.__tab_bar_menu_requested)
        
        self.__ignore_change_tab = False

        Application().event_dispatcher.subscribe(OpenTabEvent, self.__open_tab)
        Application().event_dispatcher.subscribe(ChangedCurrentTabEvent, self.__change_tab)
        Application().event_dispatcher.subscribe(ClosedTabEvent, self.__close_tab)
        Application().event_dispatcher.subscribe(ObjectDataChangedEvent, self.__object_changed)
        
        Application().event_dispatcher.subscribe(LanguageChangedEvent, self.__language_changed)
        
        QShortcut(QKeySequence(QKeySequence.Close), self).activated.connect(self.__close_tab_shortcut)
        
        self.__reload_texts()
        self.__handle_last_tab()

    def __handle_last_tab(self):
        if self.count() == 0:
            self.addTab(StartPage(self.__main_window), self.__get_start_page_text())

        if self.count() == 1 and isinstance(self.widget(0), StartPage):
            tab_close_enabled = False
        else:
            tab_close_enabled = True

        tabbar = self.tabBar()
        close_button_position = tabbar.style().styleHint(QStyle.SH_TabBar_CloseButtonPosition, None, tabbar)

        for no in range(self.count()):
            tabbar.tabButton(no, close_button_position).setEnabled(tab_close_enabled)

    def __tab_changed(self, index):
        if self.__ignore_change_tab:
            return

        if index >= 0:
            widget = self.widget(index)

            if isinstance(widget, (ScrolledCanvasWidget, CanvasWidget)):
                Application().tabs.select_tab(widget.diagram)
            else:
                Application().tabs.select_tab(None)

    def __tab_close_requested(self, index):
        widget = self.widget(index)
        if isinstance(widget, (ScrolledCanvasWidget, CanvasWidget)):
            Application().tabs.close_tab(widget.diagram)
        elif isinstance(widget, StartPage):
            self.removeTab(self.indexOf(widget))
            self.__handle_last_tab()

    def __tab_bar_menu_requested(self, point):
        tab_bar = self.tabBar()
        index = tab_bar.tabAt(point)

        if index < 0:
            return

        widget = self.widget(index)

        menu = TabContextMenu(tab_bar, index, widget)
        menu.exec(tab_bar.mapToGlobal(point))
    
    def __close_tab_shortcut(self):
        index = self.currentIndex()
        self.__tab_close_requested(index)
    
    def __open_tab(self, event):
        canvas = ScrolledCanvasWidget(self.__main_window, event.tab.drawing_area)
        self.addTab(canvas, image_loader.load_icon(event.tab.icon), event.tab.name)
        self.__handle_last_tab()

    def __change_tab(self, event):
        if event.tab is None:
            return

        for widget_id in range(self.count()):
            widget = self.widget(widget_id)

            if isinstance(widget, (ScrolledCanvasWidget, CanvasWidget)) \
                    and widget.diagram is event.tab.drawing_area.diagram:
                self.setCurrentWidget(widget)
                return

    def __close_tab(self, event):
        for widget_id in range(self.count()):
            widget = self.widget(widget_id)

            if isinstance(widget, (ScrolledCanvasWidget, CanvasWidget)) \
                    and widget.diagram is event.tab.drawing_area.diagram:
                self.__ignore_change_tab = True
                try:
                    self.removeTab(widget_id)
                finally:
                    self.__ignore_change_tab = False
                break
        self.__handle_last_tab()

    def __object_changed(self, event):
        if not isinstance(event.object, Diagram):
            return

        for widget_id in range(self.count()):
            widget = self.widget(widget_id)

            if isinstance(widget, (ScrolledCanvasWidget, CanvasWidget)) \
                    and widget.diagram is event.object:
                self.setTabText(widget_id, widget.diagram.get_display_name())
                return

    def __language_changed(self, event):
        self.__reload_texts()

    def __reload_texts(self):
        for tabno in range(self.count()):
            if isinstance(self.widget(tabno), StartPage):
                self.setTabText(tabno, self.__get_start_page_text())

    def __get_start_page_text(self):
        return _("Start Page")
