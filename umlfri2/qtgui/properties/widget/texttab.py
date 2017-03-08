from PyQt5.QtWidgets import QTextEdit


class TextTab(QTextEdit):
    def __init__(self, widget, tab):
        super().__init__()
        
        self.setTabChangesFocus(True)
        
        self.__timer = None
        
        self.textChanged.connect(self.__text_changed)
        
        self.__tab = tab
        self.__widget = widget
    
    def __text_changed(self):
        if self.__timer is not None:
            self.killTimer(self.__timer)
        self.__timer = self.startTimer(1000)
    
    def timerEvent(self, event):
        self.killTimer(self.__timer)
        self.__timer = None
        self.__tab.widget.value = self.toPlainText()
        self.__widget.apply()
    
    def focusOutEvent(self, event):
        if self.__timer is not None:
            self.killTimer(self.__timer)
        self.__timer = None
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
