from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFormLayout, QCheckBox, QPushButton, QComboBox, QLabel, QSizePolicy

from umlfri2.qtgui.base.colorwidget import ColorSelectionWidget
from umlfri2.qtgui.base.fontwidget import FontSelectionWidget
from umlfri2.qtgui.base.multiselectcombobox import MultiSelectComboBox
from umlfri2.qtgui.base.selectalldoublespinbox import SelectAllDoubleSpinBox
from umlfri2.qtgui.base.selectalllineedit import SelectAllLineEdit
from umlfri2.qtgui.base.selectallspinbox import SelectAllSpinBox
from umlfri2.ufl.dialog import *

from .smalltextedit import SmallTextEdit


class PropertyTab(QWidget):
    def __init__(self, window, tab):
        super().__init__()
        self.__window = window
        self.__tab = tab
        self.__qt_widgets = {}
        self.__qt_nullable_checkboxes = {}
        self.__enabled = True
    
    @property
    def _tab(self):
        return self.__tab
    
    def _create_layout(self):
        self.__qt_widgets = {}
        ret = QFormLayout()
        ret.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        for widget in self.__tab.widgets:
            self.__create_qt_widget(ret, widget, None)
        return ret
    
    def __create_qt_widget(self, layout, widget, nullable_widget):
        if isinstance(widget, UflDialogCheckWidget):
            qt_widget = QCheckBox(widget.label)
            self.__qt_widgets[widget.id] = qt_widget
            qt_widget.stateChanged.connect(partial(self.__state_changed, widget))
            self.__add_qt_widget(layout, None, qt_widget, False, nullable_widget)
        elif isinstance(widget, UflDialogChildWidget):
            qt_widget = QPushButton(_("Edit..."))
            self.__qt_widgets[widget.id] = qt_widget
            qt_widget.clicked.connect(partial(self.__show_dialog, widget))
            self.__add_qt_widget(layout, widget.label, qt_widget, False, nullable_widget)
        elif isinstance(widget, UflDialogColorWidget):
            qt_widget = ColorSelectionWidget()
            qt_widget.color_changed.connect(partial(self.__value_changed, widget))
            self.__qt_widgets[widget.id] = qt_widget
            self.__add_qt_widget(layout, widget.label, qt_widget, False, nullable_widget)
        elif isinstance(widget, UflDialogComboWidget):
            qt_widget = QComboBox()
            qt_widget.setEditable(True)
            for item in widget.possibilities:
                qt_widget.addItem(item)
            self.__qt_widgets[widget.id] = qt_widget
            qt_widget.editTextChanged.connect(partial(self.__value_changed, widget))
            self.__add_qt_widget(layout, widget.label, qt_widget, False, nullable_widget)
        elif isinstance(widget, UflDialogFontWidget):
            qt_widget = FontSelectionWidget()
            qt_widget.font_changed.connect(partial(self.__value_changed, widget))
            self.__qt_widgets[widget.id] = qt_widget
            self.__add_qt_widget(layout, widget.label, qt_widget, False, nullable_widget)
        elif isinstance(widget, UflDialogIntegerWidget):
            qt_widget = SelectAllSpinBox()
            self.__qt_widgets[widget.id] = qt_widget
            qt_widget.valueChanged[int].connect(partial(self.__value_changed, widget))
            self.__add_qt_widget(layout, widget.label, qt_widget, False, nullable_widget)
        elif isinstance(widget, UflDialogDecimalWidget):
            qt_widget = SelectAllDoubleSpinBox()
            self.__qt_widgets[widget.id] = qt_widget
            qt_widget.valueChanged[float].connect(partial(self.__value_changed, widget))
            self.__add_qt_widget(layout, widget.label, qt_widget, False, nullable_widget)
        elif isinstance(widget, UflDialogMultiSelectWidget):
            qt_widget = MultiSelectComboBox()
            self.__qt_widgets[widget.id] = qt_widget
            for checked, item in widget.possibilities:
                qt_widget.add_check_item(checked, item)
            qt_widget.check_changed.connect(partial(self.__multi_changed, widget))
            self.__add_qt_widget(layout, widget.label, qt_widget, False, nullable_widget)
        elif isinstance(widget, UflDialogSelectWidget):
            qt_widget = QComboBox()
            self.__qt_widgets[widget.id] = qt_widget
            for item in widget.possibilities:
                qt_widget.addItem(item)
            qt_widget.currentIndexChanged[int].connect(partial(self.__index_changed, widget))
            self.__add_qt_widget(layout, widget.label, qt_widget, False, nullable_widget)
        elif isinstance(widget, UflDialogTextWidget):
            qt_widget = SelectAllLineEdit()
            self.__qt_widgets[widget.id] = qt_widget
            qt_widget.textChanged.connect(partial(self.__value_changed, widget))
            self.__add_qt_widget(layout, widget.label, qt_widget, False, nullable_widget)
        elif isinstance(widget, UflDialogTextAreaWidget):
            qt_widget = SmallTextEdit()
            policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            policy.setVerticalStretch(1)
            qt_widget.setSizePolicy(policy)
            qt_widget.setTabChangesFocus(True)
            self.__qt_widgets[widget.id] = qt_widget
            qt_widget.textChanged.connect(partial(self.__text_changed, widget, qt_widget))
            self.__add_qt_widget(layout, widget.label, qt_widget, True, nullable_widget)
        elif isinstance(widget, UflDialogNullableWidget):
            self.__create_qt_widget(layout, widget.inner_widget, widget)
        else:
            raise Exception()
    
    def __add_qt_widget(self, layout, label, qt_widget, multi_row, nullable_widget):
        if nullable_widget is not None:
            qt_nullable_checkbox = QCheckBox(nullable_widget.label or "")
            qt_nullable_checkbox.stateChanged.connect(partial(self.__nullable_state_changed, nullable_widget, qt_widget))
            self.__qt_nullable_checkboxes[nullable_widget.id] = qt_nullable_checkbox
            if multi_row:
                layout.addRow(qt_nullable_checkbox)
                layout.addRow(qt_widget)
            else:
                layout.addRow(qt_nullable_checkbox, qt_widget)
        elif multi_row:
            if label is not None:
                layout.addRow(QLabel(label))
            layout.addRow(qt_widget)
        else:
            layout.addRow(label or "", qt_widget)
    
    def __show_dialog(self, widget, checked=False):
        from .dialog import PropertiesDialog
        
        PropertiesDialog(self.__window, widget.dialog, None).exec_()
    
    def __nullable_state_changed(self, widget, qt_widget, state):
        if not self.__enabled:
            return
        widget.is_null = state == Qt.Unchecked
        qt_widget.setEnabled(not widget.is_null)
    
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
                for qt_nullable_checkbox in self.__qt_nullable_checkboxes.values():
                    qt_nullable_checkbox.setEnabled(False)
            else:
                for widget in self.__tab.widgets:
                    if isinstance(widget, UflDialogNullableWidget):
                        qt_nullable_checkbox = self.__qt_nullable_checkboxes[widget.id]
                        qt_nullable_checkbox.setChecked(not widget.is_null)
                        self.__update_widget_value(widget.inner_widget, not widget.is_null)
                    else:
                        self.__update_widget_value(widget, True)
        finally:
            self.__enabled = True
    
    def __update_widget_value(self, widget, is_enabled):
        qt_widget = self.__qt_widgets[widget.id]
        qt_widget.setEnabled(is_enabled)
        if isinstance(widget, UflDialogCheckWidget):
            qt_widget.setChecked(widget.value)
        elif isinstance(widget, UflDialogColorWidget):
            qt_widget.selected_color = widget.value
        elif isinstance(widget, UflDialogComboWidget):
            qt_widget.setEditText(widget.value)
        elif isinstance(widget, UflDialogFontWidget):
            qt_widget.selected_font = widget.value
        elif isinstance(widget, UflDialogIntegerWidget):
            qt_widget.setValue(widget.value)
        elif isinstance(widget, UflDialogDecimalWidget):
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
    
    def _focus_first(self):
        if self.__qt_widgets:
            first_widget = self.__qt_widgets[self.__tab.first_widget.id]
            first_widget.setFocus()
            if isinstance(first_widget, (SelectAllLineEdit, SelectAllSpinBox)):
                first_widget.selectAll()
    
    def refresh(self):
        raise NotImplementedError
