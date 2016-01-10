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
    
    @property
    def children(self):
        yield from self.__projects
    
    @property
    def save_id(self):
        return self.__save_id
