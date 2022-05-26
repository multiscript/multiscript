
import multiscript
from multiscript.config.base import Config
from multiscript.ui.app_config_general_panel import GeneralAppConfigPanel
from multiscript.ui.app_config_plugins_panel import PluginsAppConfigPanel
from multiscript.util import serialize


class AppConfigGroup(Config):
    '''Class that contains all the instances of AppConfig for the app as a whole.
    '''
    def __init__(self):
        self.general = GeneralAppConfig()
        self.sources = {}   # Dict of SourceAppConfigs, keyed by the long_id of the Source.
        self.outputs = {}   # Dict of OutputAppConfigs, keyed by the long_id of the Output.
        self.plugins = PluginsAppConfig()

        for source in multiscript.app().all_sources:
            source_app_config = source.new_source_app_config()
            if source_app_config is not None:
                self.sources[source.long_id] = source_app_config

        for output in multiscript.app().all_outputs:
            output_app_config = output.new_output_app_config()
            if output_app_config is not None:
                self.outputs[output.long_id] = output_app_config

    def save(self):
        serialize.save(self, multiscript.app().app_config_path)


def load_app_config_group(path):
    app_config_group = None
    try:
        app_config_group = serialize.load(path)
    except Exception as e:
        print(f"{e.__class__.__qualname__}: {e}")
        pass

    if app_config_group is None:
        # Loading failed
        return None

    # If in future any verification of the loaded app_config_group needs to be
    # performed, do so here.

    return app_config_group


class AppConfig(Config):
    '''A subclass of Config for all config stored on the app.
    '''
    pass


class GeneralAppConfig(AppConfig):
    '''Instance of AppConfig for storing general config settings for the app
    (i.e. config not related to a particular BibleSource or BibleOutput).
    '''
    def __init__(self):
        self.save_plans_before_execution = True
        self.keep_existing_template_files = True
        self.keep_existing_output_files = False

    def new_config_widget(self):
        return GeneralAppConfigPanel(None)


class PluginsAppConfig(AppConfig):
    '''Instance of AppConfig for storing plugins config settings for the app.
    '''
    def __init__(self):
        self.altPluginsPath = None

    def new_config_widget(self):
        return PluginsAppConfigPanel(None)


