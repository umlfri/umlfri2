import json
from threading import Thread
from urllib.request import urlopen

from umlfri2.types.exceptioninfo import ExceptionInfo
from umlfri2.types.version import Version

from .events.application import UpdateCheckStartedEvent, UpdateCheckFinishedEvent


class UmlFriUpdate:
    def __init__(self, application, version, url):
        self.__application = application
        
        self.__url = url
        self.__version = version
    
    @property
    def url(self):
        return self.__url
    
    @property
    def version(self):
        return self.__version

    @property
    def is_newer(self):
        return self.__version > self.__application.about.version
    
    @property
    def is_ignored(self):
        return self.__version in self.__application.config.ignored_versions
    
    def ignore_update(self):
        if not self.is_ignored:
            self.__application.config.ignore_version(self.__version)


class UmlFriUpdates:
    __GITHUB_RELEASES = "https://api.github.com/repos/umlfri/umlfri2/releases"
    
    def __init__(self, about, application):
        self.__about = about
        self.__application = application
        self.__latest_version = None
        self.__latest_prerelease = None
        self.__check_error = None
        self.__checking_update = False
        
        if not __debug__ and application.config.auto_check_updates:
            self.recheck_update()
    
    @property
    def checking_update(self):
        return self.__checking_update
    
    @property
    def latest_version(self):
        return self.__latest_version
    
    @property
    def latest_prerelease(self):
        return self.__latest_prerelease
    
    @property
    def has_error(self):
        return self.__check_error is not None

    @property
    def error(self):
        return self.__check_error
    
    def recheck_update(self):
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
    
    def __update_check_thread(self):
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
