
from collections.abc import MutableMapping, MutableSequence, MutableSet
import functools
import json
import logging
import pathlib
from pprint import pformat
import traceback

import semver

import multiscript
from multiscript import outputs
from multiscript.bible.version import BibleVersion, BibleVersionLabels
from multiscript.config.app import AppConfigGroup, GeneralAppConfig, PluginsAppConfig
from multiscript.config.plan import PlanConfigGroup, GeneralPlanConfig
from multiscript.sources.base import BibleSource, SourceAppConfig, SourcePlanConfig
from multiscript.outputs.base import BibleOutput, OutputVersionConfig, OutputAppConfig, OutputPlanConfig
from multiscript.util.exception import MultiscriptException

_logger = logging.getLogger(__name__)

APP_VERSION_KEY         = "app_version"
BASE_OBJECT_KEY         = "__object__"
TYPE_KEY                = "__type__"
SUBTYPE_KEY             = "__subtype__"
GENERAL_ID_KEY          = "id"
GENERAL_NAME_KEY        = "name"
PLUGIN_NAME_KEY         = "__plugin_name__"
PLUGIN_ID_KEY           = "__plugin_id__"
BIBLESOURCE_NAME_KEY    = "__biblesource_name__"
BIBLESOURCE_ID_KEY      = "__biblesource_id__"
BIBLEOUTPUT_NAME_KEY    = "__bibleoutput_name__"
BIBLEOUTPUT_ID_KEY      = "__bibleoutput_id__"

MISSING_OBJ_SENTINEL = object() # Sentinel used to replace objects that could not be deserialized and are
                                # therefore missing.


def save(obj, path):
    version_str = str(multiscript.get_app_version())
    serialize_obj = {}
    serialize_obj[APP_VERSION_KEY] = version_str
    serialize_obj[BASE_OBJECT_KEY] = obj 

    # Ensure any parent directories exist, and create them if they don't.
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w') as file:
        json.dump(serialize_obj, file, indent=4, default=_serializer_handler)

def load(path, error_list=None, remove_sentinels=True):
    '''Load an object from a serialized file at the given path. Any errors that are non-failure (i.e.
    still allow loading to complete) are appended to the optional error_list.

    If remove_sentinels is true, remove_sentinels is called to remove any sentinels of missing objects
    prior to returning the deserialized object.
    '''
    with open(path, 'r') as file:
        file_content = file.read()

    # Do a basic load, just to capture the app_version that created the file
    serialize_obj = json.loads(file_content)
    file_app_version = semver.VersionInfo.parse(serialize_obj[APP_VERSION_KEY])

    # Now decode the file again, using our knowledge of the app_version that created the file
    serialize_obj = json.loads(file_content, object_hook=functools.partial(_deserialize_handler, file_app_version,
                                                                           error_list))
    if remove_sentinels:
        remove_obj_sentinels(serialize_obj)
    
    top_object = serialize_obj[BASE_OBJECT_KEY]
    return top_object

def remove_obj_sentinels(obj, cumulative_args=None):
    '''Tries to recursively examine obj and any sub-objects it contains, and remove any references to
    MISSING_OBJ_SENTINEL it finds. We assume that obj itself is not the MISSING_OBJ_SENTINEL.
    '''
    if cumulative_args is None:
        cumulative_args = set()
    else:
        if id(obj) in cumulative_args:
            # We've detected an object cycle
            # print("FOUND CYCLE")
            return
        cumulative_args.add(id(obj))

    if isinstance(obj, (int, float, bool, str)):
        # Basic types are not MISSING_OBJ_SENTINEL
        return
    if isinstance(obj, (MutableSequence, MutableSet)):
        # print("Seq/Set:", type(obj))
        # Remove any items that are the sentinel
        while MISSING_OBJ_SENTINEL in obj:
            _logger.debug("REMOVING SENTINEL")
            obj.remove(MISSING_OBJ_SENTINEL)

        # Remove any sentinels within the remaining items
        for item in obj:
            remove_obj_sentinels(item, cumulative_args)

    elif isinstance(obj, MutableMapping):
        # print("Mapping:", type(obj))
        # Remove any key-value pairs where the key is the sentinel
        while MISSING_OBJ_SENTINEL in obj:
            _logger.debug("REMOVING SENTINEL")
            del obj[MISSING_OBJ_SENTINEL]
        
        # To check the values, we iterate over the key-value pairs.
        # We can't change the dictionary while also iterating over it, so
        # instead we iterate over a copy, while deleting sentinels from
        # the original.
        for key, value in obj.copy().items():
            # Remove the key-value pairs if the value is the sentinel
            if value is MISSING_OBJ_SENTINEL:
                _logger.debug("REMOVING SENTINEL")
                del obj[key]
            else:
                # Remove any sentinels within the key or value
                remove_obj_sentinels(key, cumulative_args)
                remove_obj_sentinels(value, cumulative_args)
    else:
        # If obj has a __dict__ of attributes, remove any sentinels within it
        try:
            # print("Object:", type(obj))
            remove_obj_sentinels(obj.__dict__, cumulative_args)
        except AttributeError:
            pass 

def _serializer_handler(orig_obj):
    output_dict = {}
    # Set these keys to nothing now, so they appear first in the file (for better human readability)
    output_dict[TYPE_KEY] = None

    # Add in all the object's attributes
    try:
        output_dict.update(orig_obj.__dict__)
    except AttributeError:
        pass

    obj_type = _serialize(orig_obj, output_dict)
    
    # Now finally set these keys to their correct values
    output_dict[TYPE_KEY] = obj_type
    
    return output_dict

def _deserialize_handler(file_app_version, error_list, input_dict):
    if TYPE_KEY not in input_dict:
        return input_dict

    obj_type = input_dict.pop(TYPE_KEY)
    
    new_obj = None
    include_all_attributes = False

    try:
        if file_app_version < semver.VersionInfo.parse("0.6.0"):
            obj_subtype = input_dict.pop(SUBTYPE_KEY)
            new_obj, include_all_attributes = _deserialize_less_than_0_6_0(file_app_version, obj_type, obj_subtype, input_dict) 
        else:
            new_obj, include_all_attributes = _deserialize(file_app_version, error_list, obj_type, input_dict) 
        
        if new_obj is not None and include_all_attributes:
            # Load in all the object's attributes
            try:
                new_obj.__dict__.update(input_dict)
            except AttributeError:
                pass
    except ObjectNotFoundError as err:
        if error_list is not None:
            error_list.append(err)
        new_obj = MISSING_OBJ_SENTINEL

    return new_obj


def _serialize(orig_obj, output_dict):
    # Do this import here to avoid a circular dependancy between serialize.py and plan.py
    from multiscript.plan import Plan

    obj_type = None

    if isinstance(orig_obj, pathlib.Path):
        obj_type = "Path"
        output_dict["__path__"] = str(orig_obj)
    elif isinstance(orig_obj, Plan):
        obj_type = "Plan"
        del output_dict["path"]
        del output_dict["changed"]
        del output_dict["new"]
        del output_dict["_orig_path"]
    elif isinstance(orig_obj, BibleSource):
        obj_type = "BibleSource"
        # obj_subtype = orig_obj.id
        output_dict.clear()             # BibleSources don't persist state except through config classes.
        output_dict[TYPE_KEY] = None    # Temporarily set here so it appears at the top
        output_dict[PLUGIN_ID_KEY] = orig_obj.plugin.id
        output_dict[PLUGIN_NAME_KEY] = orig_obj.plugin.name
        output_dict["id"] = orig_obj.id
        output_dict["name"] = orig_obj.name
    elif isinstance(orig_obj, BibleVersion):
        obj_type = "BibleVersion"
        # obj_subtype = orig_obj.bible_source.id
        output_dict[PLUGIN_ID_KEY] = orig_obj.bible_source.plugin.id
        output_dict[PLUGIN_NAME_KEY] = orig_obj.bible_source.plugin.name
        output_dict[BIBLESOURCE_ID_KEY] = orig_obj.bible_source.id
        output_dict[BIBLESOURCE_NAME_KEY] = orig_obj.bible_source.name
    elif isinstance(orig_obj, BibleVersionLabels):
        obj_type = "BibleVersionLabels"
    elif isinstance(orig_obj, BibleOutput):
        obj_type = "BibleOutput"
        # obj_subtype = orig_obj.id
        output_dict.clear()             # BibleOutputs don't persist state except through config classes.
        output_dict[TYPE_KEY] = None    # Temporarily set here so it appears at the top
        output_dict[PLUGIN_ID_KEY] = orig_obj.plugin.id
        output_dict[PLUGIN_NAME_KEY] = orig_obj.plugin.name
        output_dict["id"] = orig_obj.id
        output_dict["name"] = orig_obj.name
    elif isinstance(orig_obj, OutputVersionConfig):
        obj_type = "OutputVersionConfig"
        # obj_subtype = orig_obj.output.id
        output_dict[PLUGIN_ID_KEY] = orig_obj.output.plugin.id
        output_dict[PLUGIN_NAME_KEY] = orig_obj.output.plugin.name
        output_dict[BIBLEOUTPUT_ID_KEY] = orig_obj.output.id
        output_dict[BIBLEOUTPUT_NAME_KEY] = orig_obj.output.name
    elif isinstance(orig_obj, AppConfigGroup):
        obj_type = "AppConfigGroup"
    elif isinstance(orig_obj, GeneralAppConfig):
        obj_type = "GeneralAppConfig"
    elif isinstance(orig_obj, SourceAppConfig):
        obj_type = "SourceAppConfig"
        # obj_subtype = orig_obj.bible_source.id
        output_dict[PLUGIN_ID_KEY] = orig_obj.bible_source.plugin.id
        output_dict[PLUGIN_NAME_KEY] = orig_obj.bible_source.plugin.name
        output_dict[BIBLESOURCE_ID_KEY] = orig_obj.bible_source.id
        output_dict[BIBLESOURCE_NAME_KEY] = orig_obj.bible_source.name
    elif isinstance(orig_obj, OutputAppConfig):
        obj_type = "OutputAppConfig"
        # obj_subtype = orig_obj.bible_output.id
        output_dict[PLUGIN_ID_KEY] = orig_obj.bible_output.plugin.id
        output_dict[PLUGIN_NAME_KEY] = orig_obj.bible_output.plugin.name
        output_dict[BIBLEOUTPUT_ID_KEY] = orig_obj.bible_output.id
        output_dict[BIBLEOUTPUT_NAME_KEY] = orig_obj.bible_output.name
    elif isinstance(orig_obj, PluginsAppConfig):
        obj_type = "PluginsAppConfig"
    elif isinstance(orig_obj, PlanConfigGroup):
        obj_type = "PlanConfigGroup"
    elif isinstance(orig_obj, GeneralPlanConfig):
        obj_type = "GeneralPlanConfig"
    elif isinstance(orig_obj, SourcePlanConfig):
        obj_type = "SourcePlanConfig"
        # obj_subtype = orig_obj.bible_source.id
        output_dict[PLUGIN_ID_KEY] = orig_obj.bible_source.plugin.id
        output_dict[PLUGIN_NAME_KEY] = orig_obj.bible_source.plugin.name
        output_dict[BIBLESOURCE_ID_KEY] = orig_obj.bible_source.id
        output_dict[BIBLESOURCE_NAME_KEY] = orig_obj.bible_source.name
    elif isinstance(orig_obj, OutputPlanConfig):
        obj_type = "OutputPlanConfig"
        # obj_subtype = orig_obj.bible_output.id
        output_dict[PLUGIN_ID_KEY] = orig_obj.bible_output.plugin.id
        output_dict[PLUGIN_NAME_KEY] = orig_obj.bible_output.plugin.name
        output_dict[BIBLEOUTPUT_ID_KEY] = orig_obj.bible_output.id
        output_dict[BIBLEOUTPUT_NAME_KEY] = orig_obj.bible_output.name
    else:
        raise UnimplementedSerializeError(type(orig_obj))

    return obj_type

def _deserialize(file_app_version, error_list, obj_type, input_dict):
    # Do this import here to avoid a circular dependancy between serialize.py and plan.py
    from multiscript.plan import Plan
    
    new_obj = None
    include_all_attributes = True

    if obj_type == "Path":
        new_obj = pathlib.Path(input_dict["__path__"])
        include_all_attributes = False

    elif obj_type == "Plan":
        new_obj = Plan()

    elif obj_type == "BibleSource":
        try:
            plugin = multiscript.app().plugin(input_dict[PLUGIN_ID_KEY])
            new_obj = plugin.source(input_dict[GENERAL_ID_KEY])
        except Exception as e:
            raise BibleSourceNotFoundError(input_dict[PLUGIN_ID_KEY], input_dict[PLUGIN_NAME_KEY],
                                           input_dict[GENERAL_ID_KEY], input_dict[GENERAL_NAME_KEY])
        for key in [PLUGIN_ID_KEY, PLUGIN_NAME_KEY, GENERAL_NAME_KEY]:
            del input_dict[key]

    elif obj_type == "BibleVersion":
        try:
            plugin = multiscript.app().plugin(input_dict[PLUGIN_ID_KEY])
            source = plugin.source(input_dict[BIBLESOURCE_ID_KEY])
            new_obj = source.new_bible_version()

            if file_app_version < semver.VersionInfo.parse("0.16.0"):
                try:
                    new_obj.font_family = input_dict["output_config"]["multiscript-builtin/word"].font_name
                    del input_dict["output_config"]["multiscript-builtin/word"].font_name
                except Exception:
                    _logger.info(f"Plan version < 0.16.0: Didn't find a font-family in version id {input_dict['id']}")

        except Exception as e:
            raise BibleVersionNotFoundError(input_dict[PLUGIN_ID_KEY], input_dict[PLUGIN_NAME_KEY],
                                            input_dict[BIBLESOURCE_ID_KEY], input_dict[BIBLESOURCE_NAME_KEY],
                                            input_dict[GENERAL_ID_KEY], input_dict.get(GENERAL_NAME_KEY, ""))
        for key in [PLUGIN_ID_KEY, PLUGIN_NAME_KEY, BIBLESOURCE_ID_KEY, BIBLESOURCE_NAME_KEY]:
            del input_dict[key]

    elif obj_type == "BibleVersionLabels":
        new_obj = BibleVersionLabels()
        if input_dict.get("name") is None:
            input_dict["name"] = ""
        if input_dict.get("lang") is None:
            input_dict["lang"] = ""
        if input_dict.get("abbrev") is None:
            input_dict["abbrev"] = ""    

    elif obj_type == "BibleOutput":
        try:
            plugin = multiscript.app().plugin(input_dict[PLUGIN_ID_KEY])
            new_obj = plugin.output(input_dict[GENERAL_ID_KEY])
        except Exception as e:
            raise BibleOutputNotFoundError(input_dict[PLUGIN_ID_KEY], input_dict[PLUGIN_NAME_KEY],
                                           input_dict[GENERAL_ID_KEY], input_dict[GENERAL_NAME_KEY])
        for key in [PLUGIN_ID_KEY, PLUGIN_NAME_KEY, GENERAL_NAME_KEY]:
            del input_dict[key]

    elif obj_type == "OutputVersionConfig":
        try:
            plugin = multiscript.app().plugin(input_dict[PLUGIN_ID_KEY])
            output = plugin.output(input_dict[BIBLEOUTPUT_ID_KEY])
        except Exception as e:
            raise BibleOutputNotFoundError(input_dict[PLUGIN_ID_KEY], input_dict[PLUGIN_NAME_KEY],
                                           input_dict[BIBLEOUTPUT_ID_KEY], input_dict[BIBLEOUTPUT_NAME_KEY])
        for key in [PLUGIN_ID_KEY, PLUGIN_NAME_KEY, BIBLEOUTPUT_ID_KEY, BIBLEOUTPUT_NAME_KEY]:
            del input_dict[key]
        new_obj = output.new_output_version_config()

    elif obj_type == "AppConfigGroup":
        new_obj = AppConfigGroup()
        include_all_attributes = False
        new_obj.general = input_dict["general"]
        new_obj.plugins = input_dict["plugins"]
        # To allow for new sources and outputs, we have to merge
        # these fields, rather than overwrite them
        new_obj.sources.update(input_dict["sources"])
        new_obj.outputs.update(input_dict["outputs"])

    elif obj_type == "GeneralAppConfig":
        new_obj = GeneralAppConfig()

    elif obj_type == "SourceAppConfig":
        try:
            plugin = multiscript.app().plugin(input_dict.pop(PLUGIN_ID_KEY))
            source = plugin.source(input_dict.pop(BIBLESOURCE_ID_KEY))
        except Exception as e:
            raise BibleSourceNotFoundError(input_dict[PLUGIN_ID_KEY], input_dict[PLUGIN_NAME_KEY],
                                           input_dict[BIBLESOURCE_ID_KEY], input_dict[BIBLESOURCE_NAME_KEY])
        for key in [PLUGIN_ID_KEY, PLUGIN_NAME_KEY, BIBLESOURCE_ID_KEY, BIBLESOURCE_NAME_KEY]:
            del input_dict[key]
        new_obj = source.new_source_app_config()

    elif obj_type == "OutputAppConfig":
        try:
            plugin = multiscript.app().plugin(input_dict[PLUGIN_ID_KEY])
            output = plugin.output(input_dict[BIBLEOUTPUT_ID_KEY])
        except Exception as e:
            raise BibleOutputNotFoundError(input_dict[PLUGIN_ID_KEY], input_dict[PLUGIN_NAME_KEY],
                                           input_dict[BIBLEOUTPUT_ID_KEY], input_dict[BIBLEOUTPUT_NAME_KEY])
        for key in [PLUGIN_ID_KEY, PLUGIN_NAME_KEY, BIBLEOUTPUT_ID_KEY, BIBLEOUTPUT_NAME_KEY]:
            del input_dict[key]
        new_obj = output.new_output_app_config()

    elif obj_type == "PluginsAppConfig":
        new_obj = PluginsAppConfig()
    
    elif obj_type == "PlanConfigGroup":
        new_obj = PlanConfigGroup()
        include_all_attributes = False
        new_obj.general = input_dict["general"]
        # To allow for new sources and outputs, we have to merge
        # these fields, rather than overwrite them
        new_obj.sources.update(input_dict["sources"])
        new_obj.outputs.update(input_dict["outputs"])

    elif obj_type == "GeneralPlanConfig":
        new_obj = GeneralPlanConfig()
        
    elif obj_type == "SourcePlanConfig":
        try:
            plugin = multiscript.app().plugin(input_dict[PLUGIN_ID_KEY])
            source = plugin.source(input_dict[BIBLESOURCE_ID_KEY])
        except Exception as e:
            raise BibleSourceNotFoundError(input_dict[PLUGIN_ID_KEY], input_dict[PLUGIN_NAME_KEY],
                                           input_dict[BIBLESOURCE_ID_KEY], input_dict[BIBLESOURCE_NAME_KEY])
        for key in [PLUGIN_ID_KEY, PLUGIN_NAME_KEY, BIBLESOURCE_ID_KEY, BIBLESOURCE_NAME_KEY]:
            del input_dict[key]
        new_obj = source.new_source_plan_config()

    elif obj_type == "OutputPlanConfig":
        try:
            plugin = multiscript.app().plugin(input_dict[PLUGIN_ID_KEY])
            output = plugin.output(input_dict[BIBLEOUTPUT_ID_KEY])
        except Exception as e:
            raise BibleOutputNotFoundError(input_dict[PLUGIN_ID_KEY], input_dict[PLUGIN_NAME_KEY],
                                           input_dict[BIBLEOUTPUT_ID_KEY], input_dict[BIBLEOUTPUT_NAME_KEY])
        for key in [PLUGIN_ID_KEY, PLUGIN_NAME_KEY, BIBLEOUTPUT_ID_KEY, BIBLEOUTPUT_NAME_KEY]:
            del input_dict[key]
        new_obj = output.new_output_plan_config()

    else:
        raise UnimplementedDeserializeError(file_app_version, obj_type, input_dict)

    return new_obj, include_all_attributes


def _deserialize_less_than_0_6_0(file_app_version, obj_type, obj_subtype, input_dict):
    # Do this import here to avoid a circular dependancy between serialize.py and plan.py
    from multiscript.plan import Plan
    
    new_obj = None
    include_all_attributes = True

    if obj_type == "Path":
        new_obj = pathlib.Path(input_dict["__path__"])
    elif obj_type == "Plan":
        new_obj = Plan()
    elif obj_type == "BibleSource":
        plugin = multiscript.app().plugin("multiscript-builtin")
        new_obj = plugin.source(obj_subtype)
    elif obj_type == "BibleVersion":
        plugin = multiscript.app().plugin("multiscript-builtin")
        source = plugin.source(obj_subtype)
        new_obj = source.new_bible_version()

        try:
            input_dict["output_config"]["multiscript-builtin/word"] = input_dict["output_config"]["word"]
            del input_dict["output_config"]["word"]
        except KeyError as e:
            traceback.print_exception(type(e), e, e.__traceback__)

    elif obj_type == "BibleVersionLabels":
        new_obj = BibleVersionLabels()
    elif obj_type == "BibleOutput":
        plugin = multiscript.app().plugin("multiscript-builtin")
        new_obj = plugin.output(obj_subtype)
    elif obj_type == "OutputVersionConfig":
        plugin = multiscript.app().plugin("multiscript-builtin")
        output = plugin.output(obj_subtype)
        new_obj = output.new_output_version_config()
    elif obj_type == "AppConfigGroup":
        new_obj = AppConfigGroup()
        include_all_attributes = False
        new_obj.general = input_dict["general"]
        new_obj.plugins = input_dict["plugins"]
        # To allow for new sources and outputs, we have to merge
        # these fields, rather than overwrite them
        new_obj.sources.update(input_dict["sources"])
        new_obj.outputs.update(input_dict["outputs"])
    elif obj_type == "GeneralAppConfig":
        new_obj = GeneralAppConfig()
    elif obj_type == "SourceAppConfig":
        plugin = multiscript.app().plugin("multiscript-builtin")
        source = plugin.source(obj_subtype)
        new_obj = source.new_source_app_config()
    elif obj_type == "OutputAppConfig":
        plugin = multiscript.app().plugin("multiscript-builtin")
        output = plugin.output(obj_subtype)
        new_obj = output.new_output_app_config()
    elif obj_type == "PluginsAppConfig":
        new_obj = PluginsAppConfig()
    elif obj_type == "PlanConfigGroup":
        new_obj = PlanConfigGroup()
        include_all_attributes = False
        new_obj.general = input_dict["general"]

        try:
            input_dict["outputs"]["multiscript-builtin/word"] = input_dict["outputs"]["word"]
            del input_dict["outputs"]["word"]
        except KeyError as e:
            traceback.print_exception(type(e), e, e.__traceback__)

        # To allow for new sources and outputs, we have to merge
        # these fields, rather than overwrite them
        new_obj.sources.update(input_dict["sources"])
        new_obj.outputs.update(input_dict["outputs"])
    elif obj_type == "GeneralPlanConfig":
        new_obj = GeneralPlanConfig()
    elif obj_type == "SourcePlanConfig":
        plugin = multiscript.app().plugin("multiscript-builtin")
        source = plugin.source(obj_subtype)
        new_obj = source.new_source_plan_config()
    elif obj_type == "OutputPlanConfig":
        plugin = multiscript.app().plugin("multiscript-builtin")
        output = plugin.output(obj_subtype)
        new_obj = output.new_output_plan_config()
        
        try:
            del input_dict["generatePDF"]
        except KeyError as e:
            traceback.print_exception(type(e), e, e.__traceback__)

    else:
        raise UnimplementedDeserializeError(file_app_version, obj_type, obj_subtype, input_dict)

    return new_obj, include_all_attributes


class ObjectNotFoundError(MultiscriptException):
    pass


class PluginNotFoundError(ObjectNotFoundError):
    def __init__(self, plugin_id, plugin_name):
        self.plugin_id = plugin_id
        self.plugin_name = plugin_name
    
    def __str__(self):
        return f"The plugin '{self.plugin_name}' ({self.plugin_id}) could not be found."


class BibleSourceNotFoundError(ObjectNotFoundError):
    def __init__(self, plugin_id, plugin_name, bible_source_id, bible_source_name):
        self.plugin_id = plugin_id
        self.plugin_name = plugin_name
        self.bible_source_id = bible_source_id
        self.bible_source_name = bible_source_name
    
    def __str__(self):
        return f"The Bible source '{self.bible_source_name}' ({self.bible_source_id}) " + \
               f"from plugin '{self.plugin_name}' ({self.plugin_id}) could not be found."


class BibleVersionNotFoundError(ObjectNotFoundError):
    def __init__(self, plugin_id, plugin_name, bible_source_id, bible_source_name, bible_version_id,
                 bible_version_name):
        self.plugin_id = plugin_id
        self.plugin_name = plugin_name
        self.bible_source_id = bible_source_id
        self.bible_source_name = bible_source_name
        self.bible_version_id = bible_version_id
        self.bible_version_name = bible_version_name
    
    def __str__(self):
        return f"The Bible version '{self.bible_version_name}' ({self.bible_version_id}) " + \
               f"from source '{self.bible_source_name}' ({self.bible_source_id}) " + \
               f"from plugin '{self.plugin_name}' ({self.plugin_id}) could not be found."


class BibleOutputNotFoundError(ObjectNotFoundError):
    def __init__(self, plugin_id, plugin_name, bible_output_id, bible_output_name):
        self.plugin_id = plugin_id
        self.plugin_name = plugin_name
        self.bible_output_id = bible_output_id
        self.bible_output_name = bible_output_name
    
    def __str__(self):
        return f"The output '{self.bible_output_name}' ({self.bible_output_id}) " + \
               f"from plugin '{self.plugin_name}' ({self.plugin_id}) could not be found."


class UnimplementedSerializeError(MultiscriptException):
    pass


class UnimplementedDeserializeError(MultiscriptException):
    pass


