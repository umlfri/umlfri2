from functools import partial

from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QFormLayout, QCheckBox, QPushButton, QComboBox, QTextEdit, QLabel

from umlfri2.qtgui.base.colorwidget import ColorSelectionWidget
from umlfri2.qtgui.base.fontwidget import FontSelectionWidget
from umlfri2.qtgui.base.multiselectcombobox import MultiSelectComboBox
from umlfri2.qtgui.base.selectalllineedit import SelectAllLineEdit
from umlfri2.qtgui.base.selectallspinbox import SelectAllSpinBox
from umlfri2.ufl.dialog import *


class PropertyTab(QWidget):
    def __init__(self, window, tab):
        super().__init__()
        self.__window = window
        self.__tab = tab
        self.__qt_widgets = {}
        self.__enabled = True
    
    @property
    def _tab(self):
        return self.__tab
    
    def _create_layout(self):
        self.__qt_widgets = {}
        ret = QFormLayout()
        
        for widget in self.__tab.widgets:
            if isinstance(widget, UflDialogCheckWidget):
                qt_widget = QCheckBox(widget.label)
                self.__qt_widgets[widget.id] = qt_widget
                qt_widget.stateChanged.connect(partial(self.__state_changed, widget))
                ret.addRow("", qt_widget)
            elif isinstance(widget, UflDialogChildWidget):
                qt_widget = QPushButton(_("Edit..."))
                self.__qt_widgets[widget.id] = qt_widget
                qt_widget.clicked.connect(partial(self.__show_dialog, widget))
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogColorWidget):
                qt_widget = ColorSelectionWidget()
                qt_widget.color_changed.connect(partial(self.__value_changed, widget))
                self.__qt_widgets[widget.id] = qt_widget
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogComboWidget):
                qt_widget = QComboBox()
                qt_widget.setEditable(True)
                for item in widget.possibilities:
                    qt_widget.addItem(item)
                self.__qt_widgets[widget.id] = qt_widget
                qt_widget.currentIndexChanged[str].connect(partial(self.__value_changed, widget))
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogFontWidget):
                qt_widget = FontSelectionWidget()
                qt_widget.font_changed.connect(partial(self.__value_changed, widget))
                self.__qt_widgets[widget.id] = qt_widget
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogIntegerWidget):
                qt_widget = SelectAllSpinBox()
                self.__qt_widgets[widget.id] = qt_widget
                qt_widget.valueChanged[int].connect(partial(self.__value_changed, widget))
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogMultiSelectWidget):
                qt_widget = MultiSelectComboBox()
                self.__qt_widgets[widget.id] = qt_widget
                for checked, item in widget.possibilities:
                    qt_widget.add_check_item(checked, item)
                qt_widget.check_changed.connect(partial(self.__multi_changed, widget))
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogSelectWidget):
                qt_widget = QComboBox()
                self.__qt_widgets[widget.id] = qt_widget
                for item in widget.possibilities:
                    qt_widget.addItem(item)
                qt_widget.currentIndexChanged[int].connect(partial(self.__index_changed, widget))
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogTextWidget):
                qt_widget = SelectAllLineEdit()
                self.__qt_widgets[widget.id] = qt_widget
                qt_widget.textChanged.connect(partial(self.__value_changed, widget))
                ret.addRow(widget.label, qt_widget)
            elif isinstance(widget, UflDialogTextAreaWidget):
                if widget.label is not None:
                    ret.addRow(QLabel(widget.label))
                qt_widget = QTextEdit()
                qt_widget.setTabChangesFocus(True)
                self.__qt_widgets[widget.id] = qt_widget
                qt_widget.textChanged.connect(partial(self.__text_changed, widget, qt_widget))
                ret.addRow(qt_widget)
        return ret
    
    def __show_dialog(self, widget, checked=False):
        from .dialog import PropertiesDialog
        
        PropertiesDialog(self.__window, widget.dialog, None).exec_()
        
    def __state_changed(self, widget, state):
        if not self.__enabled:
            return
        widget.value = state == Qt.Checked
    
    def __value_changed(self, widget, value):
        if not self.__enabled:
            return
        widget.value = value
    
    def __multi_changed(self, widget, index, checked):
        if not self.__enabled:
            return
        if checked:
            widget.check(index)
        else:
            widget.uncheck(index)
    
    def __index_changed(self, widget, index):
        if not self.__enabled:
            return
        widget.current_index = index
    
    def __text_changed(self, widget, qt_widget):
        if not self.__enabled:
            return
        widget.value = qt_widget.toPlainText()

    def _update_values(self):
        self.__enabled = False
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
                    elif isinstance(widget, UflDialogColorWidget):
                        qt_widget.selected_color = widget.value
                    elif isinstance(widget, UflDialogComboWidget):
                        qt_widget.setEditText(widget.value)
                    elif isinstance(widget, UflDialogFontWidget):
                        qt_widget.selected_color = widget.value
                    elif isinstance(widget, UflDialogIntegerWidget):
                        qt_widget.setValue(widget.value)
                    elif isinstance(widget, UflDialogMultiSelectWidget):
                        for index, (checked, item) in enumerate(widget.possibilities):
                            qt_widget.set_item_checked(index, checked)
                    elif isinstance(widget, UflDialogSelectWidget):
                        qt_widget.setCurrentIndex(widget.current_index)
                    elif isinstance(widget, UflDialogTextWidget):
                        qt_widget.setText(widget.value)
                    elif isinstance(widget, UflDialogTextAreaWidget):
                        qt_widget.setPlainText(widget.value)
        finally:
            self.__enabled = True
    
    def _focus_first(self):
        if self.__qt_widgets:
            self.__qt_widgets[self.__tab.first_widget.id].setFocus()
