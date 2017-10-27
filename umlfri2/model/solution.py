from uuid import uuid4


class Solution:
    def __init__(self, project=None, save_id=None):
        if project is None:
            self.__projects = []
        else:
            self.__projects = [project]
        if save_id is None:
            self.__save_id = uuid4()
        else:
            self.__save_id = save_id
    
    def add_project(self, project):
        self.__projects.append(project)
    
    def remove_project(self, project):
        self.__projects.remove(project)
    
    @property
    def children(self):
        yield from self.__projects
    
    @property
    def save_id(self):
        return self.__save_id
    
    def get_all_diagrams(self):
        for element in self.get_all_elements():
            yield from element.diagrams
    
    def get_all_elements(self):
        def recursion(obj):
            for child in obj.children:
                yield child
                yield from recursion(child)
        
        for project in self.__projects:
            yield from recursion(project)
