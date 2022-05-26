
import pluginlib


@pluginlib.Parent
class Plugin:
    '''The base class for Multiscript plugins. All plugins should subclass this class.
    '''
    def __init__(self):
        self.id = None          # String id of the plugin. Will be set to be the folder name of the plugin
        self.base_path = None   # Path to the top-level folder of the plugin
    
        self._sources = self.get_sources()
        self._sources_by_id = {}
        for source in self._sources:
            self._sources_by_id[source.id] = source

        self._outputs = self.get_outputs()
        self._outputs_by_id = {}
        for output in self._outputs:
            self._outputs_by_id[output.id] = output

    @property
    def long_id(self):
        '''Returns the long id of this object, which is globally unique in the app.
        For a plugin, the long_id is identical to the (short) id.'''
        return self.id

    # pluginlib already provides a "name" property. It would be nice to override it so we can expose it
    # here explicitly, rather than just through inheritance. However, I haven't figured out how to
    # override it while respecting pluginlib's metaclass mechanism. For now, we just provide
    # get_name() and set_name() methods to provide an explicit way of accessing the plugin's name.
    def get_name(self):
        return self.name        # Provided by pluginlib

    def set_name(self, name):
        # Note that in pluginlib you override the name by setting the _alias_ class attribute.
        self.__class__._alias_ = name

    @property
    def all_sources(self):
        return self._sources
    
    def source(self, id):
        return self._sources_by_id[id]
    
    @property
    def all_outputs(self):
        return self._outputs
    
    def output(self, id):
        return self._outputs_by_id[id]

    def get_sources(self):
        '''Returns a list of BibleSources that the plugin provides. Not to be called
        by external classes, but should be overridden by Plugin subclasses.
        '''
        return []               
    
    def get_outputs(self):
        '''Returns a list of BibleOutputs that the plugin provides. Not to be called
        by external classes, but should be overridden by Plugin subclasses.
        '''
        return []               

