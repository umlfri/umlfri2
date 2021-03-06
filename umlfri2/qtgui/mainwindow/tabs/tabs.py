from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTabWidget, QStyle, QShortcut, QMessageBox

from umlfri2.application import Application
from umlfri2.application.events.application import LanguageChangedEvent
from umlfri2.application.events.model import ObjectDataChangedEvent
from umlfri2.application.events.tabs import OpenTabEvent, ChangedCurrentTabEvent, ClosedTabEvent, TabLockStatusChangedEvent
from umlfri2.model import Diagram
from umlfri2.qtgui.base import image_loader
from umlfri2.qtgui.base.icon_combiner import combine_icons
from umlfri2.qtgui.base.resources import ICONS
from umlfri2.qtgui.canvas import ScrolledCanvasWidget, CanvasWidget
from .tabbar import MiddleClosableTabBar
from .startpage import StartPage
from .tabcontextmenu import TabContextMenu


class Tabs(QTabWidget):
    def __init__(self, main_window):
        super().__init__()
        
        self.setTabBar(MiddleClosableTabBar())
        
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
        Application().event_dispatcher.subscribe(TabLockStatusChangedEvent, self.__tab_lock_status_changed)
        
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
            tab = Application().tabs.get_tab_for(widget.diagram)
            if tab is None:
                return
            if tab.locked:
                message_box = QMessageBox(self)
                message_box.setWindowModality(Qt.WindowModal)
                message_box.setIcon(QMessageBox.Warning)
                message_box.setWindowTitle(_("Closing Locked Tab"))
                message_box.setText(_("The tab you have just requested to be closed is locked."))
                message_box.setInformativeText(_("Do you really want to close it?"))
                message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                message_box.setDefaultButton(QMessageBox.No)
                message_box.button(QMessageBox.Yes).setText(_("Yes"))
                message_box.button(QMessageBox.No).setText(_("No"))
                
                resp = message_box.exec_()
                if resp == QMessageBox.No:
                    return
            tab.close()
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
        icon = image_loader.load_icon(event.tab.icon)
        if event.tab.locked:
            icon = combine_icons(icon, ICONS.LOCKED, [self.iconSize()])
        self.addTab(canvas, icon, event.tab.name)
        self.__handle_last_tab()
    
    def __tab_lock_status_changed(self, event):
        widget_id = self.__get_tab_widget_id(event.tab)
        
        if widget_id is not None:
            icon = image_loader.load_icon(event.tab.icon)
            if event.tab.locked:
                icon = combine_icons(icon, ICONS.LOCKED, [self.iconSize()])
            self.setTabIcon(widget_id, icon)
    
    def __change_tab(self, event):
        if event.tab is None:
            return
        
        widget_id = self.__get_tab_widget_id(event.tab)
        if widget_id is not None:
            self.setCurrentIndex(widget_id)

    def __close_tab(self, event):
        widget_id = self.__get_tab_widget_id(event.tab)
        if widget_id is not None:
            self.__ignore_change_tab = True
            try:
                self.removeTab(widget_id)
            finally:
                self.__ignore_change_tab = False
            self.__handle_last_tab()

    def __object_changed(self, event):
        if not isinstance(event.object, Diagram):
            return
        
        widget_id = self.__get_tab_widget_id_by_diagram(event.object)
        if widget_id is not None:
            self.setTabText(widget_id, event.object.get_display_name())
    
    def __get_tab_widget_id(self, tab):
        return self.__get_tab_widget_id_by_diagram(tab.drawing_area.diagram)

    def __get_tab_widget_id_by_diagram(self, diagram):
        for widget_id in range(self.count()):
            widget = self.widget(widget_id)

            if isinstance(widget, (ScrolledCanvasWidget, CanvasWidget)) \
                    and widget.diagram is diagram:
                return widget_id
        return None
    
    def __language_changed(self, event):
        self.__reload_texts()

    def __reload_texts(self):
        for tabno in range(self.count()):
            if isinstance(self.widget(tabno), StartPage):
                self.setTabText(tabno, self.__get_start_page_text())

    def __get_start_page_text(self):
        return _("Start Page")
