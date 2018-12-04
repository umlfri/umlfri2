class UflDialogTab:
    def __init__(self, attr):
        self.__widgets = []
        self.__name = None
        self.__ufl_object = None
        self.__attr = attr
        self.__index = None
    
    @property
    def id(self):
        if self.__attr is None:
            return None
        else:
            return self.__attr.name
    
    @property
    def tab_index(self):
        return self.__index
    
    def _associate_tab_index(self, tab_index):
        if self.__index is not None:
            raise Exception
        self.__index = tab_index
    
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
    def first_widget(self):
        return self.__widgets[0]
    
    @property
    def widgets(self):
        yield from self.__widgets
    
    def add_widget(self, widget):
        self.__widgets.append(widget)
    
    def associate(self, ufl_object):
        raise NotImplementedError
    
    def finish(self):
        raise NotImplementedError
    
    @property
    def has_changes(self):
        for widget in self.__widgets:
            if widget.changed:
                return True
        return False
    
    def translate(self, translation):
        if self.__attr is not None:
            self.__name = translation.translate(self.__attr)
        
        for widget in self.__widgets:
            widget.translate(translation)
