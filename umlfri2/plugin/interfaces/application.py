from .interface import Interface


class IApplication(Interface):
    def __init__(self, executor):
        self.__executor = executor

    @property
    def id(self):
        return 'app'

    @property
    def api_name(self):
        return 'Application'
    
    def __get_application(self):
        from umlfri2.application import Application
        return Application()

    def get_current_diagram(self) -> object:
        from .diagram import IDiagram
        
        tab = self.__get_application().tabs.current_tab
        
        if tab is None:
            return None
        else:
            return IDiagram(self.__executor, tab.drawing_area.diagram)

    def set_current_diagram(self, value: object):
        self.__get_application().tabs.select_tab(value.diagram)

    def get_solution(self):
        raise NotImplementedError
