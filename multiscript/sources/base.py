
from pprint import pformat

from multiscript.bible.version import BibleVersion
from multiscript.config.app import AppConfig
from multiscript.config.plan import PlanConfig


class BibleSource:
    def __init__(self, plugin):
        self.plugin = plugin                # The plugin that created this BibleSource
        self.id = None
        self.name = None
        self.allow_manual_versions = True   # True if the user can add a version from this source manually

    @property
    def long_id(self):
        '''Returns the long id of this object, which is globally unique in the app.
        For a BibleSource this is a combination of its plugin long_id and the BibleSource's (short) id.'''
        return self.plugin.long_id + "/" + self.id

    def new_bible_version(self, version_id=None, name=None, lang=None, abbrev=None):
        '''Construct a new BibleVersion for this BibleSource. This should be overridden by subclasses
        to return an appropriate subclass of BibleVersion.
        '''
        return BibleVersion(self, version_id, name, lang, abbrev)

    def new_source_app_config(self):
        '''If this source stores app config, this method must return an instance
        of a subclass of SourceAppConfig. Returns None if the source stores no 
        app config.
        '''
        return None

    def new_source_plan_config(self):
        '''If this source stores plan config, this method must return an instance
        of a subclass of SourcePlanConfig. Returns None if the source stores no 
        plan config.
        '''
        return None

    def get_all_versions(self):
        '''Return all of the BibleVersions available for this BibleSource.
        '''
        return []

    def bible_content_loading(self, runner):
        '''When a plan contains versions from this Bible source, this method is called when the plan
        run is beginning to load Bible content.

        Subclasses may override to load any resources that may need to be shared amongst versions
        from this source during the plan run.
        '''
        pass

    def bible_content_loaded(self, runner):
        '''Called when a plan run has finished loading content from all its Bible versions.

        Subclasses may override to clean up any resources that were allocated during bible_content_loading().
        '''
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})" + "\n" + \
        pformat(self.__dict__)


class SourceAppConfig(AppConfig):
    '''A subclass of AppConfig for storing app-related config for
    a particular BibleSource.
    '''
    def __init__(self, bible_source):
        '''Subclasses should call this __init__() method to ensure the BibleSource
        that this SourceAppConfig belongs to is set.
        '''
        self.bible_source = bible_source

    def __repr__(self):
        return f"{self.__class__.__name__}" + "\n" + \
        pformat(self.__dict__)


class SourcePlanConfig(PlanConfig):
    '''A subclass of PlanConfig for storing plan-related config for
    a particular BibleSource.
    '''
    def __init__(self, bible_source):
        '''Subclasses should call this __init__() method to ensure the BibleSource
        that this SourcePlanConfig belongs to is set.
        '''
        self.bible_source = bible_source

    def __repr__(self):
        return f"{self.__class__.__name__}" + "\n" + \
        pformat(self.__dict__)

