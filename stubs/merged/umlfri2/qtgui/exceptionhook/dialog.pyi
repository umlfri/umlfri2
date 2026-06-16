from PyQt5.QtWidgets import QDialog
from umlfri2.types.exceptioninfo import ExceptionInfo as ExceptionInfo

class ExceptionDialog(QDialog):
    def __init__(self, exc) -> None: ...
