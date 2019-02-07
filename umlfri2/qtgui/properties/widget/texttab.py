from .editorwidget import EditorWidget


class TextTab(EditorWidget):
    def __init__(self, widget, tab):
        super().__init__()
        
        self.setTabChangesFocus(True)
        
        self.text_update.connect(self.__text_changed)
        
        self.__tab = tab
        self.__widget = widget
    
    def __text_changed(self):
        self.__tab.widget.value = self.toPlainText()
        self.__widget.apply()
    
    @property
    def label(self):
        if self.__tab.name is None:
            return _("General")
        else:
            return self.__tab.name
    
    def reload_data(self):
        if self.toPlainText() != self.__tab.widget.value:
            self.setPlainText(self.__tab.widget.value)
    
    def reload_texts(self):
        pass
