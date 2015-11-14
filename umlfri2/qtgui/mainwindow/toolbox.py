import os.path

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QVBoxLayout, QIcon, QFrame, QPushButton

from umlfri2.application import Application
from umlfri2.application.events.tabs import ChangedCurrentTabEvent
from umlfri2.paths import GRAPHICS
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
            self.set_diagram_type(event.tab.diagram_type)
    
    def set_diagram_type(self, diagram_type):
        for widget in self.__widgets:
            self.__vbox.removeWidget(widget)
            widget.deleteLater()
        
        self.__widgets = []
        
        self.__add_button(self.__arrow, 'Select')
        if diagram_type is not None:
            self.__add_separator()
            has_elements = False
            for element_type in diagram_type.element_types:
                self.__add_button(image_loader.load_icon(element_type.icon), element_type.id)
                has_elements = True
            
            if has_elements:
                self.__add_separator()
            
            for connection_type in diagram_type.connection_types:
                self.__add_button(image_loader.load_icon(connection_type.icon), connection_type.id)
        self.__widgets[0].setChecked(True)
    
    def __add_button(self, icon, text):
        button = QPushButton(text)
        button.setIcon(icon)
        button.setCheckable(True)
        button.clicked.connect(lambda checked=False: self.__select(button))
        self.__vbox.addWidget(button)
        self.__widgets.append(button)
    
    def __add_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.__vbox.addWidget(line)
        self.__widgets.append(line)
    
    def __select(self, button):
        for widget in self.__widgets:
            if isinstance(widget, QPushButton):
                widget.setChecked(widget is button)
