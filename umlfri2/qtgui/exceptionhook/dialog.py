import traceback
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor, QFont, QFontDatabase, QTextCursor
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QTextEdit

from umlfri2.constants.paths import ROOT_DIR


class ExceptionDialog(QDialog):
    def __init__(self, exc):
        super().__init__()
        
        self.setWindowTitle(_("Exception occured"))

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
        button_box.accepted.connect(self.accept)
        
        self.setMinimumSize(800, 100)

        layout = QVBoxLayout()
        
        self.__exception_text = QTextEdit(self)
        self.__exception_text.setReadOnly(True)
        self.__exception_text.setLineWrapMode(QTextEdit.NoWrap)
        
        layout.addWidget(self.__exception_text)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        
        self.__add_exception(exc)
    
    def __add_exception(self, exc):
        cursor = QTextCursor(self.__exception_text.document())
        
        normal_format = cursor.charFormat()
        
        bold_format = cursor.charFormat()
        bold_format.setFontWeight(QFont.Bold)

        file_format = cursor.charFormat()
        file_format.setFontUnderline(True)
        file_format.setForeground(QColor(Qt.blue))

        lineno_format = cursor.charFormat()
        lineno_format.setForeground(QColor(Qt.darkGreen))
        
        code_format = cursor.charFormat()
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        code_format.setFontFamily(font.family())
        
        for filename, lineno, function, text in traceback.extract_tb(exc.__traceback__):
            if filename.startswith(ROOT_DIR):
                filename = filename[len(ROOT_DIR) + 1:]
            
            cursor.setCharFormat(bold_format)
            cursor.insertText("File ")
            cursor.setCharFormat(file_format)
            cursor.insertText(filename)
            cursor.setCharFormat(bold_format)
            cursor.insertText(" line ")
            cursor.setCharFormat(lineno_format)
            cursor.insertText(str(lineno))
            cursor.setCharFormat(bold_format)
            cursor.insertText(" in ")
            cursor.setCharFormat(normal_format)
            cursor.insertText(function)
            if text:
                cursor.insertText(":\n")
                cursor.setCharFormat(code_format)
                cursor.insertText("  ")
                cursor.insertText(text)
                cursor.insertText("\n\n")
            else:
                cursor.insertText("\n")
        
        cursor.setCharFormat(bold_format)
        cursor.insertText(type(exc).__name__)
        cursor.insertText(": ")
        cursor.setCharFormat(normal_format)
        cursor.insertText(str(exc))
