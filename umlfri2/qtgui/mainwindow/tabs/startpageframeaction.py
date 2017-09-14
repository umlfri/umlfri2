from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy

from html import escape
from functools import partial


class StartPageFrameAction(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setContentsMargins(0, 0, 0, 0)
        
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.__img_label = QLabel()
        self.__text_label = QLabel()

        self.__img_label.setContextMenuPolicy(Qt.NoContextMenu)
        self.__text_label.setContextMenuPolicy(Qt.NoContextMenu)
        
        self.__pixmap = None
        self.__text = ""
        
        layout.addWidget(self.__img_label, stretch=0)
        layout.addWidget(self.__text_label, stretch=0)
        
        self.setLayout(layout)
    
    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, value):
        self.__text = value
        self.__text_label.setText('<a href="action" style="color: black">{0}</a>'.format(escape(value)))
    
    @property
    def pixmap(self):
        return self.__pixmap
    
    @pixmap.setter
    def pixmap(self, value):
        self.__pixmap = value
        
        if value is None:
            self.__img_label.clear()
        else:
            self.__img_label.setPixmap(value)
    
    @property
    def tooltip(self):
        return self.__text_label.toolTip()
    
    @tooltip.setter
    def tooltip(self, value):
        self.__text_label.setToolTip(value)
    
    def set_action_callback(self, callback):
        self.__text_label.linkActivated.connect(lambda url: callback())
    
    def set_context_menu_builder(self, menu_builder):
        self.__text_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__text_label.customContextMenuRequested.connect(partial(self.__show_context_menu, menu_builder))

    def __show_context_menu(self, menu_builder, point):
        menu = menu_builder()
        menu.exec_(self.__text_label.mapToGlobal(point))
