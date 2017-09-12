from .tab import PropertyTab


class ObjectPropertyTab(PropertyTab):
    def __init__(self, window, tab): 
        super().__init__(window, tab)
        self.setLayout(self._create_layout())
        self._update_values()
    
    def refresh(self):
        self._update_values()
