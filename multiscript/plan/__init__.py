
from pprint import pformat
from pathlib import Path
import traceback

import multiscript
from multiscript.config.plan import PlanConfigGroup
from multiscript.util import serialize

PLAN_FILE_EXTENSION = ".mplan"
PLAN_FILE_FILTER = "*" + PLAN_FILE_EXTENSION
UNTITLED_PLAN_NAME = "Untitled Plan" + PLAN_FILE_EXTENSION
DEFAULT_PLAN_FILENAME = "Default Plan" + PLAN_FILE_EXTENSION


class Plan:
    def __init__(self):
        # Set the default path to the user's Documents directory, plus an untitled file name
        self.path = multiscript.app().app_docs_path / UNTITLED_PLAN_NAME
        self.changed = False    # Classes using Plan should set to True if plan has been modified and not yet saved.
        self.new = True         # True until the plan is saved or loaded for the first time.
        self._orig_path = None  # If the path renamed due to missing plugins, store the original path here, but only
                                # until the plan is saved, when _orig_path is reset to None.

        self.notes = ""                   # Markdown text of plan notes
        self.bible_passages = None
        self.bible_versions = []          # A list of all the BibleVersions in the plan.
        self.version_selection = [[], []] # A list of lists of Boolean values. The top-level list represents the list
                                          # of columns. Each sub-list contains Boolean values to indicate whether
                                          # the corresponding version in self.bible_versions is selected for that
                                          # column. By default we start with two empty version columns.

        # TODO: Do better than hard-coding to the word document. Specify in app settings?
        self.template_path = multiscript.app().default_template_path
        self.output_dir_path = multiscript.app().output_dir_path
        self.config = PlanConfigGroup()

    @property
    def is_default_plan(self):
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
    template_path = Path(plan.template_path) # In case we've somehow received a string, we convert it to a Path
    if not template_path.exists():
        plan.template_path = blank_plan.template_path

    output_dir_path = Path(plan.output_dir_path) # In case we've somehow received a string, we convert it to a Path
    if not output_dir_path.exists():
        plan.output_dir_path = blank_plan.output_dir_path

    return plan

def get_default_plan_path():
    path = multiscript.app().app_docs_path / DEFAULT_PLAN_FILENAME
    if not path.exists():
        # Create a new default plan
        default_plan = Plan()
        default_plan.path = path
        default_plan.save()
    return path



