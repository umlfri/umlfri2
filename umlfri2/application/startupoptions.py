from __future__ import annotations

import argparse
from typing import Iterator, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from umlfri2.application import Application


class StartupOptions:
    def __init__(self, application: Application, args: List[str]) -> None:
        self.__application = application
        self.__options = self.__build_argparse(application).parse_args(args)
        self.__open_solution_process: Optional[Iterator[str]] = None
    
    def __build_argparse(self, application: Application) -> argparse.ArgumentParser:
        arguments = argparse.ArgumentParser(description=application.about.description)
        arguments.add_argument('file', metavar="FILE", type=str, nargs='?', help="File to open")
        arguments.add_argument('-v', '--version', action="version", version="UML .FRI {}".format(application.about.version))
        
        return arguments
    
    def apply_at_start(self) -> None:
        if self.__options.file:
            self.__open_solution_process = self.__application.open_solution_in_steps(self.__options.file)
            
            # process all steps till the solution is opened, so tabs could be opened later
            for step in self.__open_solution_process:
                if step == "open":
                    break
    
    def apply_after_main_window(self) -> None:
        if self.__open_solution_process is not None:
            for _ in self.__open_solution_process:
                pass
            self.__open_solution_process = None
