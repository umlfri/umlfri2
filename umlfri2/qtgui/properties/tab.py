from PySide.QtGui import QWidget, QFormLayout, QCheckBox, QPushButton, QComboBox, QSpinBox, QLineEdit, QGroupBox, \
    QVBoxLayout, QTextEdit, QLabel, QSizePolicy
from umlfri2.ufl.dialog import *


class ShowDialogAction:
    def __init__(self, window, dialog):
        self.__dialog = dialog
        self.__window = window
    
    def set_enabled(self, enabled):
        pass
    
    def action(self, checked=False):
        from .dialog import PropertiesDialog
        
        PropertiesDialog(self.__window, self.__dialog, None).exec_()


class WidgetChanged:
    def __init__(self, qt_widget, widget):
        self.__qt_widget = qt_widget
        self.__widget = widget
        self.__enabled = True
    
    def set_enabled(self, enabled):
        self.__enabled = enabled
    
    def action(self, *args):
        if not self.__enabled:
            return
        if isinstance(self.__widget, UflDialogCheckWidget):
            self.__widget.value = self.__qt_widget.isChecked()
        elif isinstance(self.__widget, UflDialogComboWidget):
            self.__widget.value = self.__qt_widget.currentText()
        elif isinstance(self.__widget, UflDialogIntegerWidget):
            self.__widget.value = self.__qt_widget.value()
        elif isinstance(self.__widget, UflDialogSelectWidget):
            self.__widget.value = self.__widget.get_value(self.__qt_widget.currentText())
        elif isinstance(self.__widget, UflDialogTextWidget):
            self.__widget.value = self.__qt_widget.text()
        elif isinstance(self.__widget, UflDialogTextAreaWidget):
            self.__widget.value = self.__qt_widget.toPlainText()


class PropertyTab(QWidget):
    def __init__(self, window, tab):
        super().__init__()
        self.__window = window
        self.__tab = tab
        self.__actions = []
        self.__qt_widgets = {}
    
    @property
    def _tab(self):
        return self.__tab
    
    def _create_layout(self):
        self.__qt_widgets = {}
        self.__actions = []
        ret = QFormLayout()
        
        for widget in self.__tab.widgets:
            if isinstance(widget, UflDialogCheckWidget):
                qt_widget = QCheckBox(widget.label)
                self.__qt_widgets[widget.id] = qt_widget
                self.__connect_action(qt_widget.stateChanged, WidgetChanged(qt_widget, widget))
                ret.addRow("", qt_widget)
            elif isinstance(widget, UflDialogChildWidget):
                qt_widget = QPushButton("Edit...")
                self.__qt_widgets[widget.id] = qt_widget
                self.__connect_action(qt_widget.clicked, ShowDialogAction(self.__window, widget.dialog))
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogColorWidget):
                qt_widget = QPushButton() # TODO: color selection widget
                self.__qt_widgets[widget.id] = qt_widget
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogComboWidget):
                qt_widget = QComboBox()
                qt_widget.setEditable(True)
                for item in widget.possibilities:
                    qt_widget.addItem(item)
                self.__qt_widgets[widget.id] = qt_widget
                self.__connect_action(qt_widget.editTextChanged, WidgetChanged(qt_widget, widget))
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogFontWidget):
                qt_widget = QPushButton() # TODO: font selection widget
                self.__qt_widgets[widget.id] = qt_widget
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogIntegerWidget):
                qt_widget = QSpinBox()
                self.__qt_widgets[widget.id] = qt_widget
                self.__connect_action(qt_widget.valueChanged, WidgetChanged(qt_widget, widget))
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogSelectWidget):
                qt_widget = QComboBox()
                self.__qt_widgets[widget.id] = qt_widget
                for item in widget.possibilities:
                    qt_widget.addItem(item)
                self.__connect_action(qt_widget.currentIndexChanged, WidgetChanged(qt_widget, widget))
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogTextWidget):
                qt_widget = QLineEdit()
                self.__qt_widgets[widget.id] = qt_widget
                self.__connect_action(qt_widget.textChanged, WidgetChanged(qt_widget, widget))
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogTextAreaWidget):
                if widget.label is not None:
                    ret.addRow(QLabel(widget.label))
                qt_widget = QTextEdit()
                qt_widget.setTabChangesFocus(True)
                self.__qt_widgets[widget.id] = qt_widget
                self.__connect_action(qt_widget.textChanged, WidgetChanged(qt_widget, widget))
                ret.addRow(qt_widget)
        return ret

    def __connect_action(self, signal, change_action):
        signal.connect(change_action.action)
        self.__actions.append(change_action)

    def _update_values(self):
        for action in self.__actions:
            action.set_enabled(False)
        try:
            if self.__tab.current_object is None:
                for qt_widget in self.__qt_widgets.values():
                    qt_widget.setEnabled(False)
            else:
                for widget in self.__tab.widgets:
                    qt_widget = self.__qt_widgets[widget.id]
                    qt_widget.setEnabled(True)
                    if isinstance(widget, UflDialogCheckWidget):
                        qt_widget.setChecked(widget.value)
                    elif isinstance(widget, UflDialogComboWidget):
                        qt_widget.setEditText(widget.value)
                    elif isinstance(widget, UflDialogIntegerWidget):
                        qt_widget.setValue(widget.value)
                    elif isinstance(widget, UflDialogSelectWidget):
                        qt_widget.setCurrentIndex(qt_widget.findText(widget.value))
                    elif isinstance(widget, UflDialogTextWidget):
                        qt_widget.setText(widget.value)
                    elif isinstance(widget, UflDialogTextAreaWidget):
                        qt_widget.setPlainText(widget.value)
        finally:
            for action in self.__actions:
                action.set_enabled(True)
