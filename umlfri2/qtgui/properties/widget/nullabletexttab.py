from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QCheckBox, QVBoxLayout

from .editorwidget import EditorWidget


class NullableTextTab(QWidget):
    def __init__(self, widget, tab):
        super().__init__()
        
        self.__not_null_check = QCheckBox()
        self.__text_edit = EditorWidget()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.__not_null_check)
        layout.addWidget(self.__text_edit)
        
        self.setLayout(layout)
        
        self.__text_edit.setTabChangesFocus(True)
        
        self.__not_null_check.stateChanged.connect(self.__null_changed)
        
        self.__text_edit.text_update.connect(self.__text_update)
        
        self.__tab = tab
        self.__widget = widget
    
    def __text_update(self):
        if not self.__not_null_check.isChecked():
            return
        self.__tab.widget.value = self.__text_edit.toPlainText()
        self.__widget.apply()
    
    def __null_changed(self, not_null_state):
        self.__tab.is_null = not_null_state == Qt.Unchecked
        self.__text_edit.setEnabled(self.__tab.is_null)
        self.__text_edit.setPlainText("")
        self.__widget.apply()
    
    @property
    def label(self):
        if self.__tab.name is None:
            return _("General")
        else:
            return self.__tab.name
    
    def reload_data(self):
        if self.__tab.is_null:
            self.__not_null_check.setChecked(False)
            self.__text_edit.setPlainText("")
            self.__text_edit.setEnabled(False)
        else:
            self.__not_null_check.setChecked(True)
            if self.__text_edit.toPlainText() != self.__tab.widget.value:
                self.__text_edit.setPlainText(self.__tab.widget.value)
            self.__text_edit.setEnabled(True)
    
    def reload_texts(self):
        self.__not_null_check.setText(self.label)
