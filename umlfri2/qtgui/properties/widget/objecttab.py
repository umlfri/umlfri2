from PySide.QtCore import Qt
from PySide.QtGui import QTableWidgetItem, QCheckBox, QPushButton, QComboBox, QSpinBox, QLineEdit

from umlfri2.ufl.dialog import *
from .tabletab import TableTab


class ObjectTab(TableTab):
    __tab = None
    
    def __init__(self, tab, dialog):
        super().__init__()
        
        self.setRowCount(tab.widget_count)
        self.itemChanged.connect(self.__item_changed)
        self.currentCellChanged.connect(self.__cell_changed)
        
        for no, widget in enumerate(tab.widgets):
            if isinstance(widget, UflDialogCheckWidget):
                qt_widget = QCheckBox()
                qt_widget.setChecked(widget.value)
            elif isinstance(widget, UflDialogChildWidget):
                qt_widget = QPushButton(_("Edit..."))
            elif isinstance(widget, UflDialogColorWidget):
                qt_widget = QPushButton() # TODO: color selection widget
            elif isinstance(widget, UflDialogComboWidget):
                qt_widget = QComboBox()
                qt_widget.setEditable(True)
                for item in widget.possibilities:
                    qt_widget.addItem(item)
                qt_widget.setEditText(widget.value)
            elif isinstance(widget, UflDialogFontWidget):
                qt_widget = QPushButton() # TODO: font selection widget
            elif isinstance(widget, UflDialogIntegerWidget):
                qt_widget = QSpinBox()
                qt_widget.setValue(widget.value)
            elif isinstance(widget, UflDialogSelectWidget):
                qt_widget = QComboBox()
                for item in widget.possibilities:
                    qt_widget.addItem(item)
                qt_widget.setCurrentIndex(widget.current_index)
            elif isinstance(widget, UflDialogTextWidget):
                qt_widget = QLineEdit()
                qt_widget.setText(widget.value)
            else:
                raise Exception()
            self.setCellWidget(no, 1, qt_widget)
        
        self.__tab = tab
        self.__dialog = dialog
    
    def __item_changed(self, item):
        pass
    
    def __cell_changed(self, row, column, prev_row, prev_column):
        widget = self.cellWidget(row, 1)
        if widget is not None:
            widget.setFocus()
    
    def reload_texts(self):
        super().reload_texts()
        
        for no, widget in enumerate(self.__tab.widgets):
            label = QTableWidgetItem(widget.label)
            label.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.setItem(no, 0, label)
    
    @property
    def label(self):
        if self.__tab.name is None:
            return _("General")
        else:
            return self.__tab.name
