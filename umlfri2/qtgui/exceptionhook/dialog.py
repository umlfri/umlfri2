import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QTextCursor
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QTextEdit

from umlfri2.types.exceptioninfo import ExceptionInfo


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

        self.__cursor = QTextCursor(self.__exception_text.document())

        self.__normal_format = self.__cursor.charFormat()

        self.__separator_format = self.__cursor.charFormat()
        self.__separator_format.setFontWeight(QFont.Bold)

        self.__bold_format = self.__cursor.charFormat()
        self.__bold_format.setFontWeight(QFont.Bold)

        self.__file_format = self.__cursor.charFormat()
        self.__file_format.setFontUnderline(True)
        self.__file_format.setForeground(QColor(Qt.blue))

        self.__lineno_format = self.__cursor.charFormat()
        self.__lineno_format.setForeground(QColor(Qt.darkGreen))

        self.__code_format = self.__cursor.charFormat()
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.__code_format.setFontFamily(font.family())

        self.__add_exception(exc)
    
    def __add_exception(self, exc):
        if isinstance(exc, Exception):
            exc = ExceptionInfo.from_exception(exc)
        
        if exc.cause is not None:
            self.__add_exception(exc.cause)
            self.__add_separator_line(traceback._cause_message.strip())
        elif exc.context is not None:
            self.__add_exception(exc.context)
            self.__add_separator_line(traceback._context_message.strip())
        
        for line in exc.traceback:
            if line.module is not None:
                self.__add_module_line(line.module, line.lineno, line.function)
            else:
                self.__add_file_line(line.filename, line.lineno, line.function)
            
            if line.text:
                self.__add_code_line(line.text)
            
            self.__cursor.insertText("\n")
        
        self.__add_exc_description_line(exc.type_name, exc.description)
    
    def __add_separator_line(self, text):
        self.__cursor.setCharFormat(self.__separator_format)
        self.__cursor.insertText("\n")
        self.__cursor.insertText(text)
        self.__cursor.insertText("\n")
    
    def __add_module_line(self, module, lineno, function):
        self.__cursor.setCharFormat(self.__bold_format)
        self.__cursor.insertText("Module ")
        self.__cursor.setCharFormat(self.__file_format)
        self.__cursor.insertText(module)
        self.__cursor.setCharFormat(self.__bold_format)
        self.__cursor.insertText(" line ")
        self.__cursor.setCharFormat(self.__lineno_format)
        self.__cursor.insertText(str(lineno))
        self.__cursor.setCharFormat(self.__bold_format)
        self.__cursor.insertText(" in ")
        self.__cursor.setCharFormat(self.__normal_format)
        self.__cursor.insertText(function)
        self.__cursor.insertText("\n")
    
    def __add_file_line(self, filename, lineno, function):
        self.__cursor.setCharFormat(self.__bold_format)
        self.__cursor.insertText("File ")
        self.__cursor.setCharFormat(self.__file_format)
        self.__cursor.insertText(filename)
        self.__cursor.setCharFormat(self.__bold_format)
        self.__cursor.insertText(" line ")
        self.__cursor.setCharFormat(self.__lineno_format)
        self.__cursor.insertText(str(lineno))
        self.__cursor.setCharFormat(self.__bold_format)
        self.__cursor.insertText(" in ")
        self.__cursor.setCharFormat(self.__normal_format)
        self.__cursor.insertText(function)
        self.__cursor.insertText("\n")
    
    def __add_code_line(self, code):
        self.__cursor.setCharFormat(self.__code_format)
        self.__cursor.insertText("  ")
        self.__cursor.insertText(code)
        self.__cursor.insertText("\n")
    
    def __add_exc_description_line(self, type, description):
        self.__cursor.setCharFormat(self.__bold_format)
        self.__cursor.insertText(type)
        self.__cursor.insertText(": ")
        self.__cursor.setCharFormat(self.__normal_format)
        self.__cursor.insertText(description)
        self.__cursor.insertText("\n")
