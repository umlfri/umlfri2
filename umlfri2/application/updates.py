from __future__ import annotations

import json
from threading import Thread
from typing import Optional, TYPE_CHECKING, Union
from urllib.request import urlopen

from umlfri2.types.exceptioninfo import ExceptionInfo
from umlfri2.types.version import Version

from .events.application import UpdateCheckStartedEvent, UpdateCheckFinishedEvent

if TYPE_CHECKING:
    from umlfri2.application import Application
    from umlfri2.application.about import AboutUmlFri


class UmlFriUpdate:
    def __init__(self, application: Application, version: Version, url: str) -> None:
        self.__application = application
        
        self.__url = url
        self.__version = version
    
    @property
    def url(self) -> str:
        return self.__url
    
    @property
    def version(self) -> Version:
        return self.__version

    @property
    def is_newer(self) -> bool:
        return self.__version > self.__application.about.version
    
    @property
    def is_ignored(self) -> bool:
        return self.__version in self.__application.config.ignored_versions
    
    def ignore_update(self) -> None:
        if not self.is_ignored:
            self.__application.config.ignore_version(self.__version)


class UmlFriUpdates:
    __GITHUB_RELEASES = "https://api.github.com/repos/umlfri/umlfri2/releases"
    
    def __init__(self, about: AboutUmlFri, application: Application) -> None:
        self.__about = about
        self.__application = application
        self.__latest_version: Optional[UmlFriUpdate] = None
        self.__latest_prerelease: Optional[UmlFriUpdate] = None
        self.__check_error: Union[None, bool, ExceptionInfo] = None
        self.__checking_update: bool = False
        
        if not __debug__ and application.config.auto_check_updates:
            self.recheck_update()
    
    @property
    def checking_update(self) -> bool:
        return self.__checking_update
    
    @property
    def latest_version(self) -> Optional[UmlFriUpdate]:
        return self.__latest_version
    
    @property
    def latest_prerelease(self) -> Optional[UmlFriUpdate]:
        return self.__latest_prerelease
    
    @property
    def has_error(self) -> bool:
        return self.__check_error is not None

    @property
    def error(self) -> Union[None, bool, ExceptionInfo]:
        return self.__check_error
    
    def recheck_update(self) -> None:
        if self.__checking_update:
            raise Exception("Cannot check for updates while checking")
        
        self.__checking_update = True
        self.__check_error = None
        
        self.__application.event_dispatcher.dispatch(UpdateCheckStartedEvent())
        
        try:
            Thread(target=self.__update_check_thread).start()
        except:
            self.__check_error = True
            self.__checking_update = False
            raise
    
    def __update_check_thread(self) -> None:
        try:
            response = urlopen(self.__GITHUB_RELEASES)
            data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
            
            latest_prerelease = None
            latest_version = None
            
            for release in data:
                version = Version(release['name'] or release['tag_name'])
                
                if release.get('prerelease', False):
                    if latest_prerelease is None or version > latest_prerelease[0]:
                        latest_prerelease = version, release
                elif not release.get('draft', False):
                    if latest_version is None or version > latest_version[0]:
                        latest_version = version, release
            
            if latest_prerelease is not None and latest_version is not None and latest_prerelease[0] < latest_version[0]:
                latest_prerelease = None
            
            if latest_version is None:
                self.__latest_version = None
            else:
                self.__latest_version = UmlFriUpdate(self.__application, latest_version[0], latest_version[1]['html_url'])
            
            if latest_prerelease is None:
                self.__latest_prerelease = None
            else:
                self.__latest_prerelease = UmlFriUpdate(self.__application, latest_prerelease[0], latest_prerelease[1]['html_url'])
        except Exception as ex:
            self.__check_error = ExceptionInfo.from_exception(ex)
            if __debug__:
                raise
        finally:
            self.__checking_update = False
            self.__application.event_dispatcher.dispatch(UpdateCheckFinishedEvent(self))
