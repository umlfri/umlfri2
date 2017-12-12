from .tab import PropertyTab


class ObjectPropertyTab(PropertyTab):
    def __init__(self, window, tab, lonely=False): 
        super().__init__(window, tab)
        layout = self._create_layout()
        if lonely:
            layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self._update_values()
    
    def refresh(self):
        self._update_values()
