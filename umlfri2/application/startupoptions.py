import argparse

class StartupOptions:
    def __init__(self, application, args):
        self.__application = application
        self.__options = self.__build_argparse(application).parse_args(args)
        self.__open_solution_process = None
    
    def __build_argparse(self, application):
        arguments = argparse.ArgumentParser(description=application.about.description)
        arguments.add_argument('file', metavar="FILE", type=str, nargs='?', help="File to open")
        arguments.add_argument('-v', '--version', action="version", version="UML .FRI {}".format(application.about.version))
        
        return arguments
    
    def apply_at_start(self):
        if self.__options.file:
            self.__open_solution_process = self.__application.open_solution_in_steps(self.__options.file)
            
            # process all steps till the solution is opened, so tabs could be opened later
            for step in self.__open_solution_process:
                if step == "open":
                    break
    
    def apply_after_main_window(self):
        if self.__open_solution_process is not None:
            for _ in self.__open_solution_process:
                pass
            self.__open_solution_process = None
