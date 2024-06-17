
import logging
from pprint import pformat
from pathlib import Path
import traceback

import multiscript
from multiscript.config.plan import PlanConfigGroup
from multiscript.util import serialize, util


_logger = logging.getLogger(__name__)

PLAN_FILE_EXTENSION = ".mplan"
PLAN_FILE_FILTER = "*" + PLAN_FILE_EXTENSION
UNTITLED_PLAN_NAME = "Untitled Plan" + PLAN_FILE_EXTENSION
DEFAULT_PLAN_FILENAME = "Default Plan" + PLAN_FILE_EXTENSION


class Plan:
    def __init__(self):
        # Path this plan has been saved to or will be saved to.
        self._path: Path = multiscript.app().app_docs_path / UNTITLED_PLAN_NAME

        # True until the plan is saved or loaded for the first time.
        self.new: bool = True

        # Classes using Plan should set changed to True if this plan has been modified and not yet saved.
        self.changed: bool = False

        # If the path renamed due to missing plugins, store the original path here, but only until the plan
        # is saved, when _orig_path is reset to None.
        self._orig_path: Path = None

        # String data of plan notes
        self.notes: str = ""

        # Media-type of plan notes. Currently only "text/markdown" supported.
        self.notes_type: str = "text/markdown" 

        self.bible_passages: str = None
        
        # A list of all the BibleVersions in the plan.
        self.bible_versions: list[multiscript.bible.version.BibleVersion] = []

        # A list of lists of Boolean values. The top-level list represents the list of columns.
        # Each sub-list contains Boolean values to indicate whether the corresponding version in
        # self.bible_versions is selected for that column. By default we start with two empty version columns.
        self.version_selection: list[list[bool]] = [[], []]

        # TODO: Should there be a setting to specify the default template?
        self._template_path: Path = multiscript.app().default_template_path
        self._output_dir_path: Path = multiscript.app().output_dir_path
        self.config: PlanConfigGroup = PlanConfigGroup()

    @property
    def path(self) -> Path:
        '''Returns the path of this plan.'''
        return self._path

    @path.setter
    def path(self, path: Path):
        '''Sets the path of this plan. The path must be absolute.
        
        If the current template or output directory paths are now in the same parent directory of this plan
        (or a subdirectory), their values are converted to relative paths.'''
        self._path = path
        if self.template_path.is_absolute():
            # Set the property to its current value to give an opportunity to make it relative if necessary
            self.template_path = self.template_path
        if self.output_dir_path.is_absolute():
            # Set the property to its current value to give an opportunity to make it relative if necessary
            self.output_dir_path = self.output_dir_path

    @property
    def template_path(self) -> Path:
        '''Returns the path of the template. May be absolute or relative to the parent directory of this plan.'''
        return self._template_path

    @template_path.setter
    def template_path(self, template_path: Path):
        '''Sets the template path. May be absolute or relative to the parent directory of this plan.
        If the path is absolute but is in the parent directory of this plan or a subdirectory, the path
        is converted to a relative path.'''
        if template_path.is_absolute() and template_path.is_relative_to(self.path.parent):
            self._template_path = template_path.relative_to(self.path.parent)
        else:
            self._template_path = template_path

    @property
    def template_abspath(self) -> Path:
        '''Returns the path of the template, and will always be the absolute path.'''
        if not self._template_path.is_absolute():
            return Path(self.path.parent, self._template_path)
        else:
            return self._template_path

    @property
    def output_dir_path(self) -> Path:
        '''Returns the path of the output directory. May be absolute or relative to the parent directory of this
        plan.'''
        return self._output_dir_path

    @output_dir_path.setter
    def output_dir_path(self, output_dir_path: Path):
        '''Sets the outpur directory path. May be absolute or relative to the parent directory of this plan.
        If the path is absolute but is in the parent directory of this plan or a subdirectory, the path
        is converted to a relative path.'''
        if output_dir_path.is_absolute() and output_dir_path.is_relative_to(self.path.parent):
            self._output_dir_path = output_dir_path.relative_to(self.path.parent)
        else:
            self._output_dir_path = output_dir_path

    @property
    def output_dir_abspath(self) -> Path:
        '''Returns the path of the outpud directory, and will always be the absolute path.'''
        if not self._output_dir_path.is_absolute():
            return Path(self.path.parent, self._output_dir_path)
        else:
            return self._output_dir_path

    @property
    def is_default_plan(self) -> bool:
        return (self.path == get_default_plan_path())

    def save(self):
        serialize.save(self, self.path)
        self.changed = False
        self.new = False
        self._orig_path = None

    def __repr__(self): 
        return f"{self.__class__.__name__}" + "\n" + \
        pformat(self.__dict__)


def load(path, error_list=None):
    '''Load a saved Plan from the file at the given path. Any errors that are non-failure (i.e.
    still allow loading to complete) are appended to the optional error_list.
    '''
    plan = None
    if error_list is None:
        error_list = []

    try:
        # Load the plan. We don't remove sentinels of missing-objects yet, because if any versions are missing
        # from plan.bible_versions, we have to remove the corresponding boolean values from
        # plan.version_selection.
        plan = serialize.load(path, error_list, remove_sentinels=False)
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        error_list.append(e) # Include load-failure exception in the list of non-failure errors

    if plan is None:
        # Loading failed
        return None

    plan.path = path
    plan.new = False

    # Remove missing versions (now marked by sentinels) and their corresponding boolean selections.
    index = 0
    while index < len(plan.bible_versions):
        if plan.bible_versions[index] is serialize.MISSING_OBJ_SENTINEL:
            # print("Removing index ", index)
            del plan.bible_versions[index]
            for bool_list in plan.version_selection:
                del bool_list[index]
            # Having deleted the objects at this index, we don't need to increment index
            # because there are now new objects at the same index.
        else:
            index += 1
    # Remove any remaining sentinels
    serialize.remove_obj_sentinels(plan)

    if len(error_list) > 0:
        # Non-failure errors occurred, which may mean the resulting loaded plan is different
        # from the plan on disk. To avoid saving over the plan on disk, we modify the plan
        # path, and mark it as modified.
        plan.changed = True
        plan._orig_path = plan.path
        plan.path = plan.path.with_name(plan.path.stem + " copy" + plan.path.suffix)

    # Handle any paths parameters that don't exist.
    blank_plan = Plan() # Provides our default values
    if util.is_absolute_any_platform(plan.template_path) and not plan.template_path.exists():
        _logger.info(f"Template absolute path {path.template_path} not found, so replacing.")
        plan.template_path = blank_plan.template_path
    if util.is_absolute_any_platform(plan.output_dir_path) and not plan.output_dir_path.exists():
        _logger.info(f"Output dir absolute path {path.output_dir_path} not found, so replacing.")
        plan.output_dir_path = blank_plan.output_dir_path

    return plan

def get_default_plan_path():
    path = multiscript.app().app_docs_path / DEFAULT_PLAN_FILENAME
    if not path.exists():
        # Create a new default plan
        default_plan = Plan()
        default_plan.path = path

        default_plan_notes_path = Path(__file__).parent / "default_plan_notes.md"
        with open(default_plan_notes_path) as file:
            default_plan.notes = file.read()
 
        default_plan.save()
    return path



