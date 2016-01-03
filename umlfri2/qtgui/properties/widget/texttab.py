from PySide.QtGui import QTextEdit

class TextTab(QTextEdit):
    def __init__(self, tab, dialog):
        super().__init__()
        
        self.setTabChangesFocus(True)
        
        self.setPlainText(tab.widget.value)
        
        self.__tab = tab
        self.__dialog = dialog
    
    @property
    def label(self):
        if self.__tab.name is None:
            return _("General")
        else:
            return self.__tab.name
    
    def reload_texts(self):
        pass
