
from multiscript.plugins import BUILTIN_PLUGIN_ID
from multiscript.plugins.base import Plugin

from multiscript.sources.getbible_dot_net import GetBibleDotNetSource
from multiscript.sources.accordance import AccordanceSource

from multiscript.outputs.word import WordOutput
from multiscript.outputs.plain_text import PlainTextOutput

class BuiltinPlugin(Plugin):
    '''Built-in plugin for built-in sources and outputs.
    '''
    _alias_ = "Builtin Plugin"

    def __init__(self):
        super().__init__()
        self.id = BUILTIN_PLUGIN_ID
   
    def get_sources(self):
        '''Returns a list of BibleSources that the plugin provides.
        '''
        return [GetBibleDotNetSource(self), AccordanceSource(self)]               
    
    def get_outputs(self):
        '''Returns a list of BibleOutputs that the plugin provides.
        '''
        return [WordOutput(self), PlainTextOutput(self)]               
