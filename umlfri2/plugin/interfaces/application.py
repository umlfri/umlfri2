from .interface import Interface


class IApplication(Interface):
    def __init__(self, executor):
        super().__init__(executor)

    @property
    def id(self):
        return 'app'

    @property
    def api_name(self):
        return 'Application'

    def get_action(self, id: str):
        raise NotImplementedError

    def get_actions(self):
        raise NotImplementedError

    def get_current_diagram(self):
        from .diagram import IDiagram
        
        tab = self._application.tabs.current_tab
        
        if tab is None:
            return None
        else:
            return IDiagram(self._executor, tab.drawing_area.diagram)

    def set_current_diagram(self, value: object):
        self._application.tabs.select_tab(value.diagram)

    def get_solution(self):
        from .solution import ISolution
        
        solution = self._application.solution
        
        if solution is None:
            return None
        else:
            return ISolution(self._executor, solution)
