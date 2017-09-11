import os.path
from functools import partial

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QPen, QPainterPath, QBrush
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from umlfri2.application import Application
from umlfri2.application.events.application import LanguageChangedEvent, RecentFilesChangedEvent
from umlfri2.constants.paths import GRAPHICS
from .startpageframe import StartPageFrame


class StartPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        
        self.__main_window = main_window
        
        self.__background = QPixmap()
        self.__background.load(os.path.join(GRAPHICS, "startpage", "startpage.png"))
        
        layout = QHBoxLayout()
        layout.setSpacing(50)
        layout.setContentsMargins(100, 250, 100, 0)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.__actions_frame = StartPageFrame()
        layout.addWidget(self.__actions_frame)
        
        self.__new_project = self.__actions_frame.add_frame_action(self.__main_window.new_project)
        self.__open_project = self.__actions_frame.add_frame_action(self.__main_window.open_solution)
        
        self.__recent_files_frame = StartPageFrame()
        layout.addWidget(self.__recent_files_frame)
        
        self.setLayout(layout)
        
        Application().event_dispatcher.subscribe(LanguageChangedEvent, self.__language_changed)
        Application().event_dispatcher.subscribe(RecentFilesChangedEvent, self.__recent_files_changed)
        self.__reload_texts()
        self.__reload_recent_files()
    
    def __language_changed(self, event):
        self.__reload_texts()
    
    def __recent_files_changed(self, event):
        self.__reload_recent_files()
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBackground(QColor(52, 170, 253))
        painter.eraseRect(painter.viewport())
        
        painter.drawPixmap(QPoint(0, 0), self.__background)
        
        qfont = QFont("Arial")
        qfont.setPixelSize(72)
        qfont.setBold(QFont.Bold)
        self.__paint_outlined_text(painter, QPoint(150, 110), qfont, "UML")
        
        qfont.setPixelSize(45)
        self.__paint_outlined_text(painter, QPoint(330, 110), qfont, ".FRI")
        
        self.__paint_outlined_text(painter, QPoint(450, 110), qfont, Application().about.version.major_minor_string)
        
        painter.end()
        
        super().paintEvent(event)
    
    def __paint_outlined_text(self, painter, position, font, text):
        path = QPainterPath()
        path.addText(position, font, text)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor(72, 124, 194), 1.5))
        painter.drawPath(path)
    
    def __reload_texts(self):
        self.__actions_frame.set_frame_action_label(self.__new_project, _("New Project"))
        self.__actions_frame.set_frame_action_label(self.__open_project, _("Open Project"))
    
    def __reload_recent_files(self):
        self.__recent_files_frame.clear()
        
        for file in reversed(list(Application().recent_files)[:5]):
            no = self.__recent_files_frame.add_frame_action(partial(self.__main_window.open_solution_from_file, file))
            self.__recent_files_frame.set_frame_action_label(no, os.path.basename(file), tooltip=file)
