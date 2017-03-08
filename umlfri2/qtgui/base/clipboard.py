from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import QApplication

from umlfri2.application import Application
from umlfri2.application.events.application import ClipboardSnippetChangedEvent
from umlfri2.application.snippet import Snippet


class QtClipboardAdatper:
    UMLFRI_CLIPBOARD_FORMAT = 'application/umlfri-snippet'
    
    def __init__(self):
        self.__clipboard = QApplication.clipboard()
        self.__last_snippet = Application().clipboard
        self.__serialized = None
        
        self.__clipboard.changed.connect(self.__qt_clipboard_changed)
        Application().event_dispatcher.subscribe(ClipboardSnippetChangedEvent, self.__umlfri_clipboard_changed)
        
        self.__synchronize_from_qt()
    
    def __qt_clipboard_changed(self, mode):
        if mode == QClipboard.Clipboard:
            self.__synchronize_from_qt()
    
    def __synchronize_from_qt(self):
        mime_data = self.__clipboard.mimeData()
        if mime_data.hasFormat(self.UMLFRI_CLIPBOARD_FORMAT):
            serialized = mime_data.data(self.UMLFRI_CLIPBOARD_FORMAT).data()
            if serialized == self.__serialized:
                return False
            self.__serialized = serialized
            self.__last_snippet = Snippet.deserialize(serialized.decode('utf8'))
            
            Application().clipboard = self.__last_snippet
        else:
            Application().clipboard = None
    
    def __umlfri_clipboard_changed(self, event):
        if event.new_snippet is None:
            return
        
        if event.new_snippet is not self.__last_snippet:
            self.__last_snippet = event.new_snippet
            
            self.__mime_data = QMimeData() # keep reference
            self.__serialized = event.new_snippet.serialize().encode('utf8')
            self.__mime_data.setData(self.UMLFRI_CLIPBOARD_FORMAT, self.__serialized)
            self.__clipboard.setMimeData(self.__mime_data, QClipboard.Clipboard)
