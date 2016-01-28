import os.path

from PySide.QtGui import QToolBar, QAction, QIcon, QPixmap

from umlfri2.application import Application
from umlfri2.application.events.application import LanguageChangedEvent
from umlfri2.application.events.diagram import SelectionChangedEvent
from umlfri2.application.events.tabs import ChangedCurrentTabEvent
from umlfri2.constants.paths import GRAPHICS


class AlignToolBar(QToolBar):
    def __init__(self):
        super().__init__()
        
        self.__align_left = self.__add_toolbar_item("align-left")
        self.__align_center_horizontally = self.__add_toolbar_item("align-hcenter")
        self.__align_right = self.__add_toolbar_item("align-right")
        
        self.addSeparator()
        
        self.__align_top = self.__add_toolbar_item("align-top")
        self.__align_center_vertically = self.__add_toolbar_item("align-vcenter")
        self.__align_bottom = self.__add_toolbar_item("align-bottom")
        
        self.__alignments = [self.__align_left, self.__align_center_horizontally, self.__align_right,
                             self.__align_top, self.__align_center_vertically, self.__align_bottom]
        
        self.addSeparator()
        
        self.__enable_snapping = self.__add_toolbar_item("enable-snapping", self.__enable_snapping_action, toggle=True)
        
        Application().event_dispatcher.subscribe(LanguageChangedEvent, lambda event: self.__reload_texts())
        
        self.__reload_texts()
        
        self.__refresh_enable()
        
        Application().event_dispatcher.subscribe(SelectionChangedEvent, self.__changed_selection)
        Application().event_dispatcher.subscribe(ChangedCurrentTabEvent, self.__changed_tab)
    
    def __add_toolbar_item(self, icon, action=None, toggle=False):
        ret = QAction(None)
        if icon is not None:
            pix = QPixmap()
            pix.load(os.path.join(GRAPHICS, "actions", icon + ".png"))
            ret.setIcon(QIcon(pix))
        if action is not None:
            ret.triggered.connect(action)
        if toggle:
            ret.setCheckable(True)
        self.addAction(ret)
        return ret
    
    def __changed_selection(self, event):
        tab = Application().tabs.current_tab
        if tab is not None:
            if event.diagram is tab.drawing_area.diagram:
                self.__refresh_enable()
    
    def __changed_tab(self, event):
        self.__refresh_enable()
        if event.tab is not None:
            self.__enable_snapping.setChecked(event.tab.drawing_area.enable_snapping)
        else:
            self.__enable_snapping.setChecked(False)
    
    def __enable_snapping_action(self, checked=False):
        tab = Application().tabs.current_tab
        if tab is not None:
            tab.drawing_area.enable_snapping = self.__enable_snapping.isChecked()
    
    def __refresh_enable(self):
        tab = Application().tabs.current_tab
        if tab is None:
            for action in self.__alignments:
                action.setEnabled(False)
            self.__enable_snapping.setEnabled(False)
        else:
            align_enabled = len(tuple(tab.drawing_area.selection.selected_elements)) >= 2
            for action in self.__alignments:
                action.setEnabled(align_enabled)
            self.__enable_snapping.setEnabled(True)
    
    def __reload_texts(self):
        self.setWindowTitle(_("Snapping"))
        self.__set_toolbar_item_text(self.__align_left, _("Align Left"))
        self.__set_toolbar_item_text(self.__align_center_horizontally, _("Center Horizontally"))
        self.__set_toolbar_item_text(self.__align_right, _("Align Right"))
        
        self.__set_toolbar_item_text(self.__align_top, _("Align Top"))
        self.__set_toolbar_item_text(self.__align_center_vertically, _("Center Vertically"))
        self.__set_toolbar_item_text(self.__align_bottom, _("Align Bottom"))
        
        self.__set_toolbar_item_text(self.__enable_snapping, _("Snap to Other Objects"))
    
    def __set_toolbar_item_text(self, item, text):
        item.setText(text)
        item.setToolTip(text)
