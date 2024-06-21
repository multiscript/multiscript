
import multiscript
from multiscript.config.base import Config
from multiscript.ui.plan_config_general_panel import GeneralPlanConfigPanel


class PlanConfigGroup(Config):
    '''Class that contains all the instances of PlanConfig for a particular Plan.
    '''
    def __init__(self):
        self.general = GeneralPlanConfig()
        self.sources = {}   # Dict of SourcePlanConfigs, keyed by the long_id of the Source.
        self.outputs = {}   # Dict of OutputPlanConfigs, keyed by the long_id of the Output.

        for source in multiscript.app().all_sources:
            source_plan_config = source.new_source_plan_config()
            if source_plan_config is not None:
                self.sources[source.long_id] = source_plan_config

        for output in multiscript.app().all_outputs:
            output_plan_config = output.new_output_plan_config()
            if output_plan_config is not None:
                self.outputs[output.long_id] = output_plan_config


class PlanConfig(Config):
    '''A subclass of Config for all config stored on a Plan.
    '''
    pass


class GeneralPlanConfig(PlanConfig):
    '''Instance of PlanConfig for storing general config settings for a Plan
    (i.e. config not related to a particular BibleSource or BibleOutput).
    '''
    def __init__(self):
        self.allow_confirmations = True
        self.confirm_after_template_expansion = False
        self.create_template_copies = True
        self.always_overwrite_output = False

    def new_config_widget(self):
        return GeneralPlanConfigPanel(None)


