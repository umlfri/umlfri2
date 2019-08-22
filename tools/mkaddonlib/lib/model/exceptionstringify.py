from .basecontainer import BaseContainer


class ExceptionStringify(BaseContainer):
    def __init__(self, exception):
        BaseContainer.__init__(self, None, exception)
    
    @property
    def exception(self):
        return self.parent
