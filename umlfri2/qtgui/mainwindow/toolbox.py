import os.path

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QVBoxLayout, QIcon, QFrame, QPushButton

from umlfri2.application import Application
from umlfri2.application.drawingarea.actions import AddElementAction, AddConnectionAction
from umlfri2.application.events.tabs import ChangedCurrentTabEvent
from umlfri2.paths import GRAPHICS
from ..base.hlinewidget import HLineWidget
from ..base import image_loader


class ToolBox(QWidget):
    def __init__(self): 
        super().__init__()
        self.__arrow = QIcon(os.path.join(GRAPHICS, 'arrow.png'))
        self.__vbox = QVBoxLayout()
        self.__vbox.setAlignment(Qt.AlignTop)
        self.setLayout(self.__vbox)
        
        self.__widgets = []
        self.set_diagram_type(None)
        
        Application().event_dispatcher.register(ChangedCurrentTabEvent, self.__current_tab_changed)
    
    def __current_tab_changed(self, event):
        if event.tab is None:
            self.set_diagram_type(None)
        else:
            self.set_diagram_type(event.tab.diagram_type, event.tab)
    
    def set_diagram_type(self, diagram_type, tab=None):
        for widget in self.__widgets:
            self.__vbox.removeWidget(widget)
            widget.deleteLater()
        
        self.__widgets = []
        
        self.__add_button(self.__arrow, _('Select'), None, tab)
        if diagram_type is not None:
            self.__add_separator()
            has_elements = False
            for element_type in diagram_type.element_types:
                # TODO: translation
                self.__add_button(image_loader.load_icon(element_type.icon), element_type.id,
                                  (AddElementAction, element_type.id),
                                  tab)
                has_elements = True
            
            if has_elements:
                self.__add_separator()
            
            for connection_type in diagram_type.connection_types:
                # TODO: translation
                self.__add_button(image_loader.load_icon(connection_type.icon), connection_type.id,
                                  (AddConnectionAction, connection_type.id),
                                  tab)
        
        self.__reset_selection()
    
    def __reset_selection(self):
        self.__widgets[0].setChecked(True)
        
        for widget in self.__widgets[1:]:
            if isinstance(widget, QPushButton):
                widget.setChecked(False)
    
    def __add_button(self, icon, text, action, tab):
        def on_clicked(checked=False):
            if action is not None:
                action_obj = action[0](action[1]).after_finish(self.__reset_selection)
            else:
                action_obj = None
            self.__select(button, action_obj, tab)
        button = QPushButton(text)
        button.setIcon(icon)
        button.setCheckable(True)
        button.clicked.connect(on_clicked)
        self.__vbox.addWidget(button)
        self.__widgets.append(button)
    
    def __add_separator(self):
        line = HLineWidget()
        self.__vbox.addWidget(line)
        self.__widgets.append(line)
    
    def __select(self, button, action, tab):
        for widget in self.__widgets:
            if isinstance(widget, QPushButton):
                widget.setChecked(widget is button)
        
        tab.drawing_area.set_action(action)
    
    def reload_texts(self):
        pass
