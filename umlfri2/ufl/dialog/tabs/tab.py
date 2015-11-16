class UflDialogTab:
    def __init__(self, name):
        self.__widgets = []
        self.__name = name
    
    @property
    def name(self):
        return self.__name
    
    @property
    def widgets(self):
        yield from self.__widgets
    
    def add_widget(self, widget):
        self.__widgets.append(widget)
