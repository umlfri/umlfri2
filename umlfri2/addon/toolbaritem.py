class ToolBarItem:
    def __init__(self, action, icon, label):
        self.__action = action
        self.__icon = icon
        self.__label = label
    
    @property
    def icon(self):
        return self.__icon
    
    @property
    def label(self):
        return self.__label
    
    @property
    def action(self):
        return self.__action
