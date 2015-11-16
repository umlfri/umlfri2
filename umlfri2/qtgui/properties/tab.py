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
    
    @property
    def _create_layout(self):
        ret = QFormLayout()
        
        for widget in self.__tab.widgets:
            if isinstance(widget, UflDialogCheckWidget):
                ret.addRow("", QCheckBox(widget.label))
            elif isinstance(widget, UflDialogChildWidget):
                w = QPushButton("Edit...")
                action = ShowDialogAction(self.__window, widget.dialog)
                w.clicked.connect(action.action)
                self.__actions.append(action)
                ret.addRow(widget.label, w)
            elif isinstance(widget, UflDialogColorWidget):
                ret.addRow(widget.label, QPushButton()) # TODO: color selection widget
            elif isinstance(widget, UflDialogComboWidget):
                w = QComboBox()
                w.setEditable(True)
                for item in widget.possibilities:
                    w.addItem(item)
                ret.addRow(widget.label, w)
            elif isinstance(widget, UflDialogFontWidget):
                ret.addRow(widget.label, QPushButton()) # TODO: font selection widget
            elif isinstance(widget, UflDialogIntegerWidget):
                ret.addRow(widget.label, QSpinBox())
            elif isinstance(widget, UflDialogSelectWidget):
                w = QComboBox()
                for item in widget.possibilities:
                    w.addItem(item)
                ret.addRow(widget.label, w)
            elif isinstance(widget, UflDialogTextWidget):
                ret.addRow(widget.label, QLineEdit())
            elif isinstance(widget, UflDialogTextAreaWidget):
                ret.addRow(QLabel(widget.label))
                ret.addRow(QTextEdit())
        return ret
