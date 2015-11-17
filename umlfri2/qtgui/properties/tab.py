from PySide.QtGui import QWidget, QFormLayout, QCheckBox, QPushButton, QComboBox, QSpinBox, QLineEdit, QGroupBox, \
    QVBoxLayout, QTextEdit, QLabel, QSizePolicy
from umlfri2.ufl.dialog import *


class ShowDialogAction:
    def __init__(self, window, dialog):
        self.__dialog = dialog
        self.__window = window
    
    def action(self, checked=False):
        from .dialog import PropertiesDialog
        
        PropertiesDialog(self.__window, self.__dialog).exec_()


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
    
    @property
    def _create_layout(self):
        ret = QFormLayout()
        
        for widget in self.__tab.widgets:
            if isinstance(widget, UflDialogCheckWidget):
                qt_widget = QCheckBox(widget.label)
                self.__qt_widgets[widget.id] = qt_widget
                ret.addRow("", qt_widget)
            elif isinstance(widget, UflDialogChildWidget):
                qt_widget = QPushButton("Edit...")
                self.__qt_widgets[widget.id] = qt_widget
                action = ShowDialogAction(self.__window, widget.dialog)
                qt_widget.clicked.connect(action.action)
                self.__actions.append(action) # keep reference, qt doesn't
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
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogFontWidget):
                qt_widget = QPushButton() # TODO: font selection widget
                self.__qt_widgets[widget.id] = qt_widget
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogIntegerWidget):
                qt_widget = QSpinBox()
                self.__qt_widgets[widget.id] = qt_widget
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogSelectWidget):
                qt_widget = QComboBox()
                self.__qt_widgets[widget.id] = qt_widget
                for item in widget.possibilities:
                    qt_widget.addItem(item)
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogTextWidget):
                qt_widget = QLineEdit()
                self.__qt_widgets[widget.id] = qt_widget
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogTextAreaWidget):
                ret.addRow(QLabel(widget.label))
                qt_widget = QTextEdit()
                self.__qt_widgets[widget.id] = qt_widget
                ret.addRow(qt_widget)
        return ret
    
    def _update_values(self):
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
                    qt_widget.setCurrentIndex(qt_widget.findData(widget.value))
                elif isinstance(widget, UflDialogTextWidget):
                    qt_widget.setText(widget.value)
                elif isinstance(widget, UflDialogTextAreaWidget):
                    qt_widget.setText(widget.value)
