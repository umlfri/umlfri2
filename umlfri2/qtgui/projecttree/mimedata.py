from PySide.QtCore import QMimeData


class ProjectMimeData(QMimeData):
    def __init__(self, model_object):
        super().__init__()
        self.__model_object = model_object
    
    @property
    def model_object(self):
        return self.__model_object
