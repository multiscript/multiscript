
from pprint import pformat


class Config:
    def __init__(self):
        pass

    def new_config_widget(self):
        '''If this Config uses a ConfigWidget (a subclass of Qt Widget)
        for displaying and editing its data, this method returns an instance
        of a the widget (i.e. an instance of ConfigWidget or a subclass
        instance). This method returns None if this Config doesn't use an
        accompanying widget.

        ConfigWidgets use a load/store mechanism.
        '''
        return None

    def new_config_subform(self):
        '''If this Config uses a ConfigSubform (a subclass of Qt Widget)
        for displaying and editing its data, this method returns an instance
        of a the subform (i.e. an instance of ConfigSubform or a subclass
        instance). This method returns None if this Config doesn't use an
        accompanying subform.

        ConfigSubforms use a form mechanism.
        '''
        return None

    def copyTo(self, other_config):
        other_config.__dict__.update(self.__dict__)

    def __repr__(self):
        return f"{self.__class__.__name__}" + "\n" + \
        pformat(self.__dict__)


