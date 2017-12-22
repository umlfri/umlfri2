from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont, QIntValidator, QKeySequence
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QLineEdit, \
    QSlider, QPushButton, QSizePolicy

from umlfri2.constants.keys import STRIKE_OUT
from umlfri2.types.enums import FontStyle
from umlfri2.types.font import Fonts


class UpDownPassingLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.__dest_widget = None
    
    @property
    def destination_widget(self):
        return self.__dest_widget
    
    @destination_widget.setter
    def destination_widget(self, value):
        self.__dest_widget = value
    
    def keyPressEvent(self, event):
        if self.__dest_widget is not None and not event.modifiers() and event.key() in (Qt.Key_Up, Qt.Key_Down):
            self.__dest_widget.event(event)
        else:
            super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        if self.__dest_widget is not None and not event.modifiers() and event.key() in (Qt.Key_Up, Qt.Key_Down):
            self.__dest_widget.event(event)
        else:
            super().keyReleaseEvent(event)


class FontDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.__font_db = QFontDatabase()
        
        self.setWindowTitle(_("Select font"))

        layout = QVBoxLayout()
        
        content_layout = QHBoxLayout()
        
        font_list_layout = QVBoxLayout()
        
        font_list_layout.addWidget(QLabel(_("Font family:")))
        
        self.__font_search = UpDownPassingLineEdit()
        self.__font_search.textEdited.connect(self.__family_search_edited)
        
        font_list_layout.addWidget(self.__font_search)
        
        self.__font_list = QListWidget()
        self.__font_list.setFocusPolicy(Qt.NoFocus)
        
        for font in sorted(self.__font_db.families()):
            if self.__font_db.isSmoothlyScalable(font):
                self.__font_list.addItem(font)
        
        self.__font_list.currentTextChanged.connect(self.__family_changed)
        
        self.__font_search.destination_widget = self.__font_list
        
        font_list_layout.addWidget(self.__font_list)
        
        content_layout.addLayout(font_list_layout)
        
        style_layout = QVBoxLayout()
        style_layout.setAlignment(Qt.AlignCenter)
        
        self.__bold_widget = self.__create_style_button("B", _("Bold"), QKeySequence.Bold, FontStyle.bold)
        style_layout.addWidget(self.__bold_widget)

        self.__italic_widget = self.__create_style_button("I", _("Italic"), QKeySequence.Italic, FontStyle.italic)
        style_layout.addWidget(self.__italic_widget)

        self.__underline_widget = self.__create_style_button("U", _("Underline"), QKeySequence.Underline, FontStyle.underline)
        style_layout.addWidget(self.__underline_widget)
        
        self.__strike_widget = self.__create_style_button("S", _("Strike Out"), STRIKE_OUT, FontStyle.strike)
        style_layout.addWidget(self.__strike_widget)
        
        content_layout.addLayout(style_layout)
        
        size_layout = QVBoxLayout()
        size_layout.setAlignment(Qt.AlignHCenter)
        
        size_layout.addWidget(QLabel(_("Size (px):")))
        
        self.__size_edit = UpDownPassingLineEdit()
        self.__size_edit.textEdited.connect(self.__size_edited)
        self.__size_edit.setValidator(QIntValidator(5, 60))
        size_layout.addWidget(self.__size_edit)
        self.__size_edit.setSizePolicy(QSizePolicy.Preferred, self.__size_edit.sizePolicy().verticalPolicy())
        
        self.__size_slider = QSlider(Qt.Vertical)
        self.__size_slider.setFocusPolicy(Qt.NoFocus)
        self.__size_slider.setRange(5, 60)
        self.__size_slider.setTickInterval(5)
        self.__size_slider.setTickPosition(QSlider.TicksRight)
        self.__size_slider.valueChanged.connect(self.__size_changed)
        
        self.__size_edit.destination_widget = self.__size_slider
        
        size_layout.addWidget(self.__size_slider)
        
        content_layout.addLayout(size_layout)
        
        layout.addLayout(content_layout)
        
        self.__example = QLineEdit("AaBbYyZz")
        self.__example.setFixedHeight(80)
        layout.addWidget(self.__example)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
        button_box.button(QDialogButtonBox.Cancel).setText(_("Cancel"))
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        
        self.__font = Fonts.default
    
    def __create_style_button(self, text, tooltip, keys, font_style):
        def toggled(value):
            self.__font = self.__font.change(font_style, value)
            self.__refresh_example_font()
        
        shortcut = QKeySequence(keys)
        widget = QPushButton(text)
        widget.setShortcut(shortcut)
        widget.setToolTip("{0} ({1})".format(tooltip, shortcut.toString()))
        font = widget.font()
        if font_style == FontStyle.bold:
            font.setBold(True)
        elif font_style == FontStyle.italic:
            font.setItalic(True)
        elif font_style == FontStyle.underline:
            font.setUnderline(True)
        elif font_style == FontStyle.strike:
            font.setStrikeOut(True)
        widget.setFont(font)
        widget.setCheckable(True)
        widget.toggled.connect(toggled)
        return widget
    
    @property
    def ufl_font(self):
        return self.__font
    
    @ufl_font.setter
    def ufl_font(self, value):
        self.__font = value
        
        for item in self.__font_list.findItems(value.family, Qt.MatchExactly):
            self.__font_list.setCurrentItem(item)
            break
        else:
            self.__font_list.clearSelection()
        
        self.__font_search.setText(value.family)
        
        self.__bold_widget.setChecked(FontStyle.bold in value.style)
        self.__italic_widget.setChecked(FontStyle.italic in value.style)
        self.__underline_widget.setChecked(FontStyle.underline in value.style)
        self.__strike_widget.setChecked(FontStyle.strike in value.style)
        
        self.__size_slider.setValue(value.size)
        self.__size_edit.setText(str(value.size))
        
        self.__refresh_example_font()
    
    def __refresh_example_font(self):
        qfont = QFont(self.__font.family)
        qfont.setPixelSize(self.__font.size)
        qfont.setBold(FontStyle.bold in self.__font.style)
        qfont.setItalic(FontStyle.italic in self.__font.style)
        qfont.setStrikeOut(FontStyle.strike in self.__font.style)
        qfont.setUnderline(FontStyle.underline in self.__font.style)
        
        self.__example.setFont(qfont)
    
    def __family_search_edited(self, name):
        selected_text = self.__font_list.currentItem().text()
        if selected_text.startswith(name):
            return
        
        for item in self.__font_list.findItems(name, Qt.MatchStartsWith):
            self.__font_list.setCurrentItem(item)
            break

    def __family_changed(self, value):
        if self.__font.family != value:
            if not self.__font_search.hasFocus():
                self.__font_search.setText(value)
            self.__font = self.__font.change_family(value)
            self.__refresh_example_font()
    
    def __size_edited(self, value):
        if not value or int(value) < 5:
            return
        int_value = int(value)
        if self.__font.size != int_value:
            self.__font = self.__font.change_size(int_value)
            
            self.__size_slider.setValue(int_value)
            
            self.__refresh_example_font()
    
    def __size_changed(self, value):
        if self.__font.size != value:
            if self.__size_edit.text() != str(value):
                self.__size_edit.setText(str(value))
                self.__size_edit.selectAll()
            self.__font = self.__font.change_size(value)
            self.__refresh_example_font()
