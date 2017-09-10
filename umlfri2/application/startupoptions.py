import argparse

class StartupOptions:
    def __init__(self, application, args):
        self.__application = application
        self.__options = self.__build_argparse(application).parse_args(args)
    
    def __build_argparse(self, application):
        arguments = argparse.ArgumentParser(description=application.about.description)
        arguments.add_argument('file', metavar="FILE", type=str, nargs='?', help="File to open")
        arguments.add_argument('-v', '--version', action="version", version="UML .FRI {}".format(application.about.version))
        
        return arguments
    
    def apply(self):
        if self.__options.file:
            self.__application.open_solution(self.__options.file)
