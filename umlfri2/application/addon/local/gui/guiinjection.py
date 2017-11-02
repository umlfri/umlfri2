class GuiInjection:
    def __init__(self, actions, toolbars):
        self.__actions = dict(actions)
        self.__toolbars = tuple(toolbars)
    
    def _set_addon(self, addon):
        for action in self.__actions.values():
            action._set_addon(addon)
        
        for toolbar in self.__toolbars:
            toolbar._set_addon(addon)
    
    def reset(self):
        for action in self.__actions.values():
            action.enabled = True
    
    @property
    def actions(self):
        yield from self.__actions.values()
    
    def get_action(self, id):
        return self.__actions[id]
    
    @property
    def toolbars(self):
        yield from self.__toolbars
