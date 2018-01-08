import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
import sip

from umlfri2.application import Application
from umlfri2.application.drawingarea.actions import AddElementAction, AddConnectionAction
from umlfri2.application.events.application import LanguageChangedEvent
from umlfri2.constants.paths import GRAPHICS
from umlfri2.qtgui.base import image_loader
from umlfri2.qtgui.base.hlinewidget import HLineWidget


class ToolBox(QWidget):
    def __init__(self, drawing_area, show_names): 
        super().__init__()
        self.__arrow = QIcon(os.path.join(GRAPHICS, 'arrow.png'))
        self.__vbox = QVBoxLayout()
        self.__vbox.setAlignment(Qt.AlignTop)
        self.setLayout(self.__vbox)
        
        self.__show_names = show_names
        
        self.__widgets = []
        self.__current_tab = None
        self._fill(drawing_area)
        
        Application().event_dispatcher.subscribe(LanguageChangedEvent, self.__language_changed)
        
        self.__reload_texts()
    
    def __language_changed(self, event):
        self.__reload_texts()
    
    def _fill(self, drawing_area):
        for widget in self.__widgets:
            self.__vbox.removeWidget(widget)
            sip.delete(widget)
        
        self.__current_drawing_area = drawing_area
        self.__widgets = []
        
        if drawing_area is None:
            button = self.__add_button(self.__arrow, _('Select'), None, drawing_area, True)
            button.setEnabled(False)
            return
        
        current_connection = None
        current_element = None
        if isinstance(drawing_area.current_action, AddElementAction):
            current_element = drawing_area.current_action.element_type
        elif isinstance(drawing_area.current_action, AddConnectionAction):
            current_connection = drawing_area.current_action.connection_type
        
        self.__add_button(
            self.__arrow,
            _('Select'),
            None,
            drawing_area,
            current_connection is None and current_element is None
        )
        
        self.__add_separator()
        
        diagram_type = drawing_area.diagram.type
        
        translation = diagram_type.metamodel.get_translation(Application().language.current_language)
        
        has_elements = False
        for element_type in diagram_type.element_types:
            self.__add_button(image_loader.load_icon(element_type.icon), translation.translate(element_type),
                              (AddElementAction, element_type.id),
                              drawing_area,
                              current_element == element_type.id)
            has_elements = True
        
        if has_elements:
            self.__add_separator()
        
        for connection_type in diagram_type.connection_types:
            self.__add_button(image_loader.load_icon(connection_type.icon), translation.translate(connection_type),
                              (AddConnectionAction, connection_type.id),
                              drawing_area,
                              current_connection == connection_type.id)
    
    def __reset_selection(self):
        self.__widgets[0].setChecked(True)
        
        for widget in self.__widgets[1:]:
            if isinstance(widget, QPushButton):
                widget.setChecked(False)
    
    def __add_button(self, icon, text, action, drawing_area, checked):
        def on_clicked(checked=False):
            if action is not None:
                action_obj = action[0](action[1]).after_finish(self.__reset_selection)
            else:
                action_obj = None
            self.__select(button, action_obj, drawing_area)
        
        button = QPushButton()
        if self.__show_names:
            button.setText(text)
        else:
            button.setToolTip(text)
        button.setIcon(icon)
        button.setCheckable(True)
        button.setChecked(checked)
        button.clicked.connect(on_clicked)
        self.__vbox.addWidget(button)
        self.__widgets.append(button)
        
        return button
    
    def __add_separator(self):
        line = HLineWidget()
        self.__vbox.addWidget(line)
        self.__widgets.append(line)
    
    def __select(self, button, action, drawing_area):
        for widget in self.__widgets:
            if isinstance(widget, QPushButton):
                widget.setChecked(widget is button)
        
        drawing_area.set_action(action)
    
    def __reload_texts(self):
        self._fill(self.__current_drawing_area)
