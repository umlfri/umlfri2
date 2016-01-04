class UflDialogTab:
    def __init__(self, attr):
        self.__widgets = []
        self.__name = None
        self.__ufl_object = None
        self.__attr = attr
    
    @property
    def id(self):
        if self.__attr is None:
            return None
        else:
            return self.__attr.name
    
    @property
    def name(self):
        return self.__name
    
    @property
    def current_object(self):
        return self.__ufl_object
    
    def _set_current_object(self, ufl_object):
        self.__ufl_object = ufl_object
        
        for widget in self.__widgets:
            widget.associate(ufl_object)
    
    @property
    def widget_count(self):
        return len(self.__widgets)
    
    @property
    def widgets(self):
        yield from self.__widgets
    
    def add_widget(self, widget):
        self.__widgets.append(widget)
    
    def associate(self, ufl_object):
        raise NotImplementedError
    
    def finish(self):
        raise NotImplementedError
    
    def translate(self, translation):
        if self.__attr is not None:
            self.__name = translation.translate(self.__attr)
        
        for widget in self.__widgets:
            widget.translate(translation)
