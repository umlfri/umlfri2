from ..widgets import UflDialogChildWidget


class UflDialogTab:
    def __init__(self, id, name):
        self.__widgets = []
        self.__name = name
        self.__ufl_object = None
        self.__id = id
    
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def current_object(self):
        return self.__ufl_object
    
    def _set_current_object(self, ufl_object):
        self.__ufl_object = ufl_object
        
        if self.__ufl_object is not None:
            for widget in self.__widgets:
                if isinstance(widget, UflDialogChildWidget):
                    if widget.id is None:
                        widget.dialog.associate(self.__ufl_object)
                    else:
                        widget.dialog.associate(self.__ufl_object.get_value(widget.id))
    
    @property
    def widgets(self):
        yield from self.__widgets
    
    def add_widget(self, widget):
        self.__widgets.append(widget)
    
    def associate(self, ufl_object):
        raise NotImplementedError
    
    def get_value(self, id):
        raise NotImplementedError
