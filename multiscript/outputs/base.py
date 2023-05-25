
import logging
from pprint import pformat

from multiscript.bible.content import BibleStreamHandler
from multiscript.config.app import AppConfig
from multiscript.config.plan import PlanConfig
from multiscript.config.version import VersionConfig
from multiscript.plugins.base import Plugin


_logger = logging.getLogger(__name__)


class BibleOutput:
    '''A BibleOutput is responsible for generating a set of output items using
    the BibleContent and other information supplied in a PlanRunner.

    Different formats of output items need to be handled by different subclasses
    of BibleOutput. If the output items are a set of files, it is easier to subclass
    FileSetOutput instead (itself a subclass of BibleOutput). If the output items
    are a set of files based on standard Multiscript tags, it's easier to subclass
    TaggedOutput (itself a subclass of FileSetOutput).
    '''
    def __init__(self, plugin):
        self.plugin: Plugin = plugin    # The plugin that created this BibleOutput
        self.id: str = None
        self.name: str = None
        self._accepted_template_exts: list[str] = []

    @property
    def long_id(self) -> str:
        '''Returns the long id of this object, which is globally unique in the app.
        For a BibleOutput this is a combination of its plugin long_id and the BibleOutput's (short) id.'''
        return self.plugin.long_id + "/" + self.id

    @property
    def accepted_template_exts(self) -> list[str]:
        '''Returns a list of the template file extensions accepted by this BibleOutput (e.g. ['.txt','.docx'])
        '''
        return self._accepted_template_exts

    def get_total_progress_steps(self, runner):
        return len(runner.all_version_combos)

    def generate_all(self, runner):
        '''Generate all the output items for this module for the given PlanRunner.

        This is the main entry method for the BibleOutput, called by the PlanRunner.
        This default implementation first calls setup(), then iterates
        through runner.all_version_combos and calls generate_combo_item() for
        each combination. Finally it calls cleanup().

        Subclasses can override this method for more complex algorithms.
        '''
        self.setup(runner)
        for version_combo in runner.all_version_combos:
            try:
                template_obj = self.get_template_obj(runner, version_combo)
                self.generate_combo_item(runner, version_combo, template_obj)
            except Exception as exception:
                _logger.exception(exception)
                runner.monitors.request_confirmation(f"<b>There was an error creating an output " +
                                                     f"for these versions:<br>{version_combo}.</b>")
            runner.increment_progress_step_count()
        self.cleanup(runner)

    def get_template_obj(self, runner, version_combo):
        '''For the given runner and version combination, obtain the template object needed
        to generate the output item. This method uses the cache of template objects contained
        in the OutputPlanRun, and calls generate_combo_item() to create template objects
        where necessary.

        The base template object will be the Path stored in runner.base_template_path.
        Subsequent template objects will be whatever object is returned by generate_combo_item().
        Template objects are cached by version combination.
        '''
        template_combo = version_combo.template_combo
        template_cache = runner.output_runs[self.long_id].template_cache # Cache of template objects
        template_obj = None

        if template_combo is None:
            template_obj = runner.base_template_path
        elif tuple(template_combo) not in template_cache:
            # No template in the cache, so look for the prior template
            prior_template = self.get_template_obj(runner, template_combo)
            template_obj = self.generate_combo_item(runner, template_combo, prior_template, is_template=True)
            template_cache[tuple(template_combo)] = template_obj
        else:
            template_obj = template_cache[tuple(template_combo)]

        return template_obj

    def generate_combo_item(self, runner, version_combo, template_obj=None, is_template=False):
        '''Subclasses must either override this method, or override generate_all() to change the
        default algorithm.
        
        Create an individual output item (most often, a file) for the given runner and
        version combination. An optional template object can be provided (most often, a path to a
        template file). If is_template is True, the resulting output (e.g. filepath) is itself a
        template, to be used for creating later outputs, and an appropriate template object
        must be returned (e.g. the path of the newly created file).
        
        The default implementation does nothing except print a log message, and return the version_combo
        itself.
        '''
        base_log_message = "\t\tCreating "
        base_log_message += "template" if is_template else "file"
        _logger.info(base_log_message+  ": " + str(version_combo) + " using template: " + str(template_obj))
        return version_combo

    def new_output_app_config(self):
        '''If this output stores app config, subclasses must override to return a subclass instance of
        OutputAppConfig. Or return None if the output stores no app config.
        '''
        return None

    def new_output_plan_config(self):
        '''If this output stores plan config, subclasses must override to return a subclass instance of
        OutputPlanConfig. Or return None if the output stores no plan config.
        '''
        return None

    def new_output_version_config(self):
        '''If this output stores version config, subclasses must override to return a subclass instance of
        OutputVersionConfig. Or return None if the output stores no version config.
        '''
        return None

    def new_output_plan_run(self, plan):
        '''Every output needs to supply an instance of OutputPlanRun or a subclass. Ata minimum, the
        OutputPlanRun holds the cache of template objects. OutputPlanRuns may be subclassed to store
        other per-run information for the output as well.
        '''
        return OutputPlanRun(plan)

    def setup(self, runner):
        '''Abstract method subclasses may override if needed. Called prior to looping through the version
        combos.
        '''
        pass

    def cleanup(self, runner):
        '''Abstract method subclasses may override if needed. Called after looping through the version
        combos.
        '''
        pass


class OutputAppConfig(AppConfig):
    '''A subclass of AppConfig for storing app-related config for
    a particular BibleOutput.
    '''
    def __init__(self, bible_output):
        '''Subclasses should call this __init__() method to ensure the BibleOutput
        that this OutputAppConfig belongs to is set.
        '''
        self.bible_output = bible_output

    def __repr__(self):
        return f"{self.__class__.__name__}" + "\n" + \
        pformat(self.__dict__)


class OutputPlanConfig(PlanConfig):
    '''A subclass of PlanConfig for storing plan-related config for
    a particular BibleOutput.
    '''
    def __init__(self, bible_output):
        '''Subclasses should call this __init__() method to ensure the BibleOutput
        that this OutputPlanConfig belongs to is set.
        '''
        self.bible_output = bible_output

    def __repr__(self):
        return f"{self.__class__.__name__}" + "\n" + \
        pformat(self.__dict__)


class OutputVersionConfig(VersionConfig):
    def __init__(self, bible_output):
        self.output = bible_output

    def __repr__(self):
        return f"{self.__class__.__name__}" + "\n" + \
        pformat(self.__dict__)


class OutputPlanRun:
    def __init__(self, plan):
        self.template_cache = {}        # A cache of templates, keyed by the tuple of their BibleVersionCombo.
                                        # Typically, these will be Paths to a file.

    def __repr__(self):
        return f"{self.__class__.__name__}" + "\n" + \
        pformat(self.__dict__)


class OutputBibleStreamHandler(BibleStreamHandler):
    pass
