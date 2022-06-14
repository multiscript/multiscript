from collections import Counter
from pathlib import Path, PurePosixPath
import logging
import os
import site
import shutil
import sys
import traceback
import zipfile

import pluginlib
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt, QStandardPaths

import multiscript
from multiscript import plan
from multiscript.ui.main_window import MainWindow
from multiscript.util.exception_catcher import catch_unhandled_exceptions

# Plugins we import to ensure pyinstaller includes them in the distribution
from multiscript.plugins.base import Plugin
from multiscript.plugins.builtin import BuiltinPlugin


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
_logger.addHandler(logging.StreamHandler())

PLUGIN_FILE_EXTENSION = ".mplugin"
PLUGIN_FILE_FILTER = "*" + PLUGIN_FILE_EXTENSION
DEFAULT_TEMPLATE_NAMES = ["Default Template.docx", "Default Template.txt"]

# TODO: Extract other plugin functionality into a plugin manager, but still expose
#       key plugins through the application object.


class MultiscriptBaseApplication:
    '''Application base class.
    
    It contains most of the application-specific code, but omits most of the
    Qt-related functionality.
    '''
    def __init__(self):
        self._app_config_group = None
        self._attribution_contents = None
        self.replace_missing_templates()

        self._known_plugins = {}    # Needed by plugin-loading architecture
        self._plugins = []          # Current set of loaded plugins
        self._plugins_by_id = {}

        self._sources = []
        self._sources_by_long_id = {}

        self._outputs = []
        self._outputs_by_long_id = {}

    def replace_missing_templates(self):
        for template_name in DEFAULT_TEMPLATE_NAMES:
            template_path = self.templates_dir_path / template_name
            if not template_path.exists():
                internal_template_path = Path(__file__).parent / "templates" / template_name
                # TODO: Handle any exception raised by attempting to copy the template.
                # Programmatically create a fresh template?
                shutil.copyfile(internal_template_path, template_path)

    @property
    def all_plugins(self):
        return self._plugins

    def plugin(self, id):
        return self._plugins_by_id[id]

    @property
    def all_sources(self):
        '''A collated list of all BibleSources from all loaded plugins.'''
        return self._sources
    
    def source(self, long_id):
        '''Returns a particular BibleSource using its long_id (without needing a reference to its plugin).
        '''
        return self._sources_by_long_id[long_id]
    
    @property
    def all_outputs(self):
        '''A collated list of all BibleOutputs from all loaded plugins.'''
        return self._outputs
    
    def outputs_for_ext(self, template_file_ext):
        '''Returns a collated list of all BibleOutputs that accept the given template file
        extension (e.g. '.docx').
        '''
        return [output for output in self.all_outputs if template_file_ext in output.accepted_template_exts]

    def output(self, long_id):
        '''Returns a particular BibleOutput using its long_id (without needing a reference to its plugin).
        '''
        return self._outputs_by_long_id[long_id]

    @property
    def all_accepted_template_exts(self):
        '''A collated list of all the template file extensions from all available BibleOutputs.'''
        all_exts = set()
        for output in self.all_outputs:
            all_exts.update(output.accepted_template_exts)
        return sorted(list(all_exts))

    def load_plugins(self):
        '''Load all available plugins, including the built-in plugin. Must be called at least
        once at application startup, to ensure the built-in plugin is loaded.

        Can be safely called multiple times to discover any newly added plugins.
        '''
        if len(self._plugins) == 0:
            # Load builtin plugin
            self._update_plugin_collections(BuiltinPlugin())

            # Merely importing the BuiltinPlugin causes it be detected by the PluginLoader.
            # We therefore call _get_new_plugin_list once first, so the BuiltinPlugin is not
            # accidentally associated with later plugin folders.
            self._get_new_plugin_list(Plugin, prefix_package='multiscript')

        # Load plugins from base plugin folders
        plugin_base_paths = []
        plugin_base_paths.append(self.app_plugin_dir_path)
        alt_plugins_path = self.app_config_group.plugins.altPluginsPath
        if alt_plugins_path is not None and alt_plugins_path.is_dir():
            plugin_base_paths.append(alt_plugins_path)
        
        for base_path in plugin_base_paths:
            _logger.debug(f"Searching for plugins in base path {base_path}")
            for sub_path in base_path.iterdir():
                self._load_plugin_at_path(sub_path)

    def _load_plugin_at_path(self, path):
        '''Load any available plugin at the specified path. Returns the plugin instance if successful,
        otherwise returns None.

        Can be safely called multiple times to discover any newly added plugins at the path.
        '''
        # Ignore the path if it's not a directory, or it's hidden
        if not path.is_dir() or path.name[0] == '.':
            return None
        # Make sure we have the required directory structure
        plugin_id = path.name
        if not (path / "plugin/").is_dir() or not (path / "plugin" / plugin_id).is_dir():
            return None

        # Include any site-packages directory in the plugin
        site_packages_path = path / "site-packages/"
        if site_packages_path.is_dir():
        # This code doesn't seem to work when frozen with pyinstaller.
        #     site.addsitedir(site_packages_path)
        # So we just try this instead:
            sys.path.append(str(site_packages_path))

        # We will only search within the 'plugin' subdir
        search_path = path / "plugin"

        _logger.debug(f"\tSearching for plugins in {search_path}")
        search_path_in_syspath = search_path in sys.path
        if not search_path_in_syspath:
            sys.path.append(str(search_path))
        new_plugins = self._get_new_plugin_list(Plugin, paths=[str(search_path)], prefix_package='multiscript')
        if not search_path_in_syspath:
            sys.path.remove(str(search_path))
        num_new_plugins = len(new_plugins)
        if num_new_plugins == 0:
            _logger.debug(f"\t\tNo new plugins found in {search_path.name}")
            return None
        elif num_new_plugins > 1:
            _logger.debug(f"\t\tToo many plugin classes ({num_new_plugins}) found in {search_path.name}. Ignoring path")
            return None
        else:
            _logger.debug("\t\tFound: " + str(new_plugins))
            # Exactly one plugin in the sub_path, so we instantiate it
            plugin_instance = None
            try:
                plugin_instance = new_plugins[0]()
                plugin_instance.id = plugin_id
                plugin_instance.base_path = search_path.parent
                self._update_plugin_collections(plugin_instance)
            except Exception as exception:
                _logger.debug(f"\t\tThe plugin {plugin_id} could not be instantiated.")
                _logger.exception(exception)
            return plugin_instance

    def _update_plugin_collections(self, plugin_instance):
        '''For a new plugin_instance, update the internal collections of plugins, sources, outputs etc.
        '''
        self._plugins.append(plugin_instance)
        self._plugins_by_id[plugin_instance.id] = plugin_instance

        plugin_sources = plugin_instance.all_sources
        self._sources.extend(plugin_sources)
        self._sources_by_long_id.update({source.long_id: source for source in plugin_sources})

        plugin_outputs = plugin_instance.all_outputs
        self._outputs.extend(plugin_outputs)
        self._outputs_by_long_id.update({output.long_id: output for output in plugin_outputs})

        # _logger.debug(f"plugins={[type(plugin) for plugin in self._plugins]}\n")
        # _logger.debug(f"plugins_by_id={ {id:type(plugin) for id, plugin in self._plugins_by_id.items()} }\n")
        # _logger.debug(f"sources={[type(source) for source in self._sources]}\n")
        # _logger.debug(f"sources_by_long_id={ {id:type(source) for id, source in self._sources_by_long_id.items()} }\n")
        # _logger.debug(f"outputs={[type(output) for output in self._outputs]}\n")
        # _logger.debug(f"outputs_by_long_id={ {id:type(output) for id, output in self._outputs_by_long_id.items()} }\n")

    def _get_new_plugin_list(self, plugin_class, **plugin_loader_args):
        '''Returns a simple list of newly loaded plugins which are subclasses of plugin_class
        
        plugin_loader_args is a dict of any arguments to be supplied to the PluginLoader.
        '''
        new_plugin_items = self._get_new_plugin_items(**plugin_loader_args)
        new_plugin_list = list(new_plugin_items.get(plugin_class.__name__, {}).values())
        return new_plugin_list

    def _get_new_plugin_items(self, **plugin_loader_args):
        '''Returns newly loaded plugins, in the same format as pluginlib.PluginLoader().plugins.items()
        
        plugin_loader_args is a dict of any arguments to be supplied to the PluginLoader.
        '''
        new_plugins = {}

        # Note that pluginglib.PluginLoader always includes previously loaded plugins when asked to load
        # new plugins. We therefore use the existing collection of (previously loaded) plugins, to determine
        # which plugins are genuinely new.
        try:
            loader = pluginlib.PluginLoader(**plugin_loader_args)
            all_plugins = loader.plugins.items() # All old and new plugins together

            for plugin_type, plugins_by_name in all_plugins:
                if not plugin_type in self._known_plugins:
                    # A new root-level plugin type has been discovered
                    self._known_plugins[plugin_type] = {}
                    new_plugins[plugin_type] = {}
                
                for plugin_name, plugin_class in plugins_by_name.items():
                    if not plugin_name in self._known_plugins[plugin_type]:
                        # A new plugin has been discovered
                        if not plugin_type in new_plugins:
                            # We need to create a root-level entry for the new plugin
                            new_plugins[plugin_type] = {}
                
                        self._known_plugins[plugin_type][plugin_name] = plugin_class
                        new_plugins[plugin_type][plugin_name] = plugin_class
        except Exception as exception:
            _logger.debug(f"\t\tThe was a problem trying to load plugins using these args: {plugin_loader_args}")
            _logger.exception(exception)

        return new_plugins  # Return only the newly loaded plugins

    @property
    def user_app_data_path(self):
        path = Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
        return path

    @property
    def user_docs_path(self):
        path = Path(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation))
        return path

    @property
    def app_docs_path(self):
        path = self.user_docs_path / "Multiscript"
        path.mkdir(parents=True, exist_ok=True) # Ensure directory exists
        return path

    @property
    def templates_dir_path(self):
        path = self.app_docs_path / "Templates"
        path.mkdir(parents=True, exist_ok=True) # Ensure directory exists
        return path

    @property
    def default_template_path(self):
        self.replace_missing_templates()
        path = self.templates_dir_path / DEFAULT_TEMPLATE_NAMES[0]
        return path

    @property
    def output_dir_path(self):
        path = self.app_docs_path / "Output"
        path.mkdir(parents=True, exist_ok=True) # Ensure directory exists
        return path

    @property
    def app_config_path(self):
        return self.user_app_data_path / "Config" / "app_config.json"

    @property
    def app_plugin_dir_path(self):
        path = self.user_app_data_path / "Plugins"
        path.mkdir(parents=True, exist_ok=True) # Ensure directory exists
        return path

    @property
    def icon(self):
        return QtGui.QIcon(str(Path(__file__).parent / "icons" / "multiscript.svg"))

    @property
    def app_config_group(self):
        if self._app_config_group is None:
            # Load app config from file
            self._app_config_group = multiscript.config.app.load_app_config_group(self.app_config_path)

            # If loading from file didn't work, create a new default app config
            if self._app_config_group is None:
                self._app_config_group = multiscript.config.app.AppConfigGroup()
                self._app_config_group.save()
            
        return self._app_config_group

    @property
    def attribution_contents(self):
        if self._attribution_contents is not None:
            return self._attribution_contents

        attribution_path = Path(__file__).parent.parent / Path("Attribution.html")
        try:
            with open(attribution_path) as file:
                self._attribution_contents = file.read()
        except:
            self._attribution_contents = ""

        return self._attribution_contents


class MultiscriptApplication(QtWidgets.QApplication, MultiscriptBaseApplication):
    '''Application class that adds in most of the Qt-related functionality.

    Note that we inherit from QApplication first, so that calling super().__init__() calls
    QApplication.__init__. This is necessary to ensure the QApplication is constructed before
    any of our QWidgets. Otherwise, we will crash.
    '''

    _restart_request = QtCore.Signal(list) # Internal signal to allowed queued restart requests

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        MultiscriptBaseApplication.__init__(self) # Necessary because QApplication doesn't call super().__init__
        
        self.restart_requested = False # True if a restart should occur after the event loop ends

        # We use a Qt.QueuedConnection to ensure that restarts requested before the event loop starts
        # are not forgotten, and restarts requested from within a dialog still allow the dialog
        # to close cleanly before all other windows close and the restart occurs.
        self._restart_request.connect(self._on_restart_request, type=Qt.QueuedConnection)
        self._restart_arg_list = None # Command-line arguments to be passed to the restart
        
        self.main_window = None
        self.received_first_file_open_event = False

        self.setApplicationName("Multiscript")
        self.setWindowIcon(self.icon)

    def ui_init(self):
        # Note that we can't include this code in the __init__ method, as the QApplication
        # needs to have *finished* initialising before we start creating QWidgets like windows.

        self.main_window = MainWindow()
        # There may be multiple command-line arguments, but we only use the first plan file and first
        # plugin file we find.
        plan_path = None
        plugin_path = None
        for arg in sys.argv[1:]:
            path = Path(arg)
            if plan_path is None and path.suffix == plan.PLAN_FILE_EXTENSION:
                # First argument that is a plan file
                plan_path = path
            elif plugin_path is None and path.suffix == PLUGIN_FILE_EXTENSION:
                plugin_path = path
            
            if plan_path is not None and plugin_path is not None:
                # Ignore any remaining command-line arguments
                break
        
        print("Plan:", plan_path)
        print("Plugin:", plugin_path)
        # Load any plugin first, in case the plan depends on it
        if plugin_path is not None:
            print("Adding plugin")
            self.add_plugin(plugin_path)
            print("Added plugin")
        if plan_path is not None:
            self.main_window.load_plan(plan_path)

        self.main_window.show()

    def exec_(self):
        '''If we're not running as a 'frozen' pyinstaller bundle, this calls exec_() in our superclass
        as normal.

        If we *are* running as a 'frozen' pyinstaller bundle, we still call exec_() in the superclass,
        but we ensure that any unhandled exceptions are caught raised to the caller.
        '''
        if not self.is_frozen():
            return super().exec_()
        else:
            result = 0
            with catch_unhandled_exceptions(self):
                result = super().exec_()                  
            return result

    def exec_catches_exceptions(self):
        '''Same as exec_(), but rather than reraising unhandled exceptions, we catch them here
        and display them in a dialog.

        If we're not running as a 'frozen' pyinstaller bundle, this calls exec_() in our superclass
        as normal.

        If we *are* running as a 'frozen' pyinstaller bundle, we still call exec_() in the superclass,
        but we ensure that any unhandled exceptions are caught and displayed in a dialog.
        '''
        result = 0
        try:
            result = self.exec_()
        except BaseException as exception:
            detail_text = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            self.msg_box(self.tr("We're sorry, but an unexpected error has occurred and Multiscript needs to close."),
                         self.tr("Unexpected Error"),detail_text=detail_text)
        
        return result

    def event(self, e):
        # On Mac only, files are opened via AppleEvents, which Qt exposes as a (Mac-only) FileOpen
        # Qt event. However, we package our app using pyinstaller, which can optionally enable
        # argv-emulation. When this is turned on:
        #   1. pyinstaller catches the first open AppleEvent and supplies the same info as a
        #      command-line arg. The advantage of this is that we can immediately open
        #      the file at startup, rather than waiting for the first event.
        #   2. The event pyinstaller catches is still received here as our first Qt FileOpen event.
        #      This means that on Mac with argv-emulation enabled, we potentially receive twice
        #      the same file to open: once via the command-line and once as a FileOpen event.
        # To prevent opening the same file twice, we only process this FileOpen event if:
        #   - We've already created the main window, and
        #   - We've already received our first FileOpen event. If instead this *is* our first
        #         FileOpen event, we only process it if it's different from the command-line arg
        #         (which would suggest we've been packaged with something other than pyinstaller).
        #
        if e.type() == QtCore.QEvent.FileOpen:
            path = Path(e.file())
            this_is_first_file_open_event = not self.received_first_file_open_event

            if multiscript.ARGV_EMULATION:
                if this_is_first_file_open_event and \
                    (len(sys.argv) == 1 or (path == Path(sys.argv[1]))):
                    self.received_first_file_open_event = True
                    # We ignore this first event            
                    return super().event(e) 

            if path.suffix == plan.PLAN_FILE_EXTENSION:
                self.main_window.load_plan(path)
                return True
            elif path.suffix == PLUGIN_FILE_EXTENSION:
                self.add_plugin(path)
                return True
        
        return super().event(e)

    def add_plugin(self, path=None):
        '''Installs a plugin, given the path to the .mplugin file. If path is None,
        the user will be prompted for the .mplugin file.
        
        If the plugin is succesfully installed, returns the plugin instance. Otherwise returns None.
        '''
        if path is None:
            # Prompt for plugin to add
            # TODO: Set the default loading directory for the dialog to something like the documents folder
            path_str, selected_filter = QtWidgets.QFileDialog.getOpenFileName(None, self.tr("Select Plugin"),
                                                                                None, PLUGIN_FILE_FILTER)
            if len(path_str) == 0:
                # Cancel
                return None
            path = Path(path_str)
        
        if not zipfile.is_zipfile(path):
            self.msg_box(self.tr('This file is not a valid plugin.'), self.tr("Plugin Error"))
            return None
        
        try:
            file = zipfile.ZipFile(path)
        except BaseException as e:
            self.msg_box(self.tr('There was an error loading this plugin.'), self.tr("Plugin Error"))
            return None

        with file:
            # It would be great to use the Path interface to zip files, but instead we use the older
            # ZipInfo interface, so we can still run under Python 3.7. It's a lot more work
            # to verify the structure of the zip file is correct.
            # ZipInfo doesn't allow custom attributes, so we wrap it an a custom _ExtraZipInfo class
            # to hold some extra useful metadata.
            extra_infos = [_ExtraZipInfo(info) for info in file.infolist()]

            # Filter out root folders or filenames to ignore
            root_names_to_ignore = ['__MACOSX']
            final_names_to_ignore = ['.DS_Store']
            extra_infos = [info for info in extra_infos if (info.root_name not in root_names_to_ignore and \
                                                            info.final_name not in final_names_to_ignore)]

            # Get the names of the root elements in the zip, and how many times they're referenced
            root_names_count = Counter([info.root_name for info in extra_infos])

            if len(root_names_count) != 1:
                self.msg_box(self.tr('The plugin was not loaded as it contains more than one top-level file/folder.'),
                                      self.tr("Plugin Error"))
                return None

            plugin_id = list(root_names_count)[0]
            
            # There should be an entry for the top-level folder and at least one file/folder under it.
            if root_names_count[plugin_id] < 2:
                self.msg_box(self.tr('The plugin was not loaded as it appears to be empty.'),
                                      self.tr("Plugin Error"))
                return None
            
            new_plugin_path = self.app_plugin_dir_path / plugin_id
            if new_plugin_path.exists():
                # A plugin with the same id exists. Try to find its name.
                existing_plugin_name = "Unknown Name"
                for existing_plugin in self.all_plugins:
                    if existing_plugin.base_path == new_plugin_path:
                        existing_plugin_name = existing_plugin.name
                result = self.msg_box(self.tr(f"There is an existing plugin with id '{plugin_id}' named '{existing_plugin_name}'. ") + 
                                               self.tr("Do you wish to replace it?\n\n") + 
                                               self.tr("This will require restarting Multiscript."),
                                               self.tr("Replace Plugin?"),
                                               QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok)
                if result == QtWidgets.QMessageBox.Cancel:
                    return None
                else:
                    # Remove the existing plugin. We therefore need to restart, and we'll
                    # save installing the plugin for the restart.
                    shutil.rmtree(new_plugin_path)
                    # TODO: On restart, reopen the current plan file, rather than the default plan.
                    self.request_restart([path]) # Pass the plugin zip file as an argument to the restart.
                    return None

            for extra_info in extra_infos:
                dest_path = file.extract(extra_info.info, path=self.app_plugin_dir_path)
                # _logger.debug(f'Extracted {dest_path}')
            
            # Now we've extracted the plugin, try to import it.
            new_plugin_instance = self._load_plugin_at_path(new_plugin_path)
            if new_plugin_instance is None:
                self.msg_box(self.tr(f"The plugin with '{plugin_id}' id could not be loaded."),
                                      self.tr("Plugin Error"))
                shutil.rmtree(new_plugin_path)
                return None

            self.msg_box(self.tr(f"The plugin '{new_plugin_instance.name}' was successfully installed"),
                                  self.tr("Plugin Installed"))
            return new_plugin_instance

    def remove_plugin(self, plugin_id):
        '''Deletes the plugin on disk with the given id. If there is no plugin with the given id, this
        method does nothing.
        
        Returns True if the plugin was deleted, otherwise False. This method requests a restart, which
        is necessary to completely remove the plugin from memory.
        '''
        try:
            plugin = self.plugin(plugin_id)
        except KeyError:
            return False
        
        id = plugin.id
        name = plugin.name
        path = plugin.base_path
        result = self.msg_box(self.tr(f"Are you sure you want to remove the plugin '{name}' with id '{id}' and restart Multiscript?"),
                                       self.tr("Remove Plugin?"),
                                       QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok,
                                       QtWidgets.QMessageBox.Cancel, self.tr(f"This will delete the folder {path}"))
        if result == QtWidgets.QMessageBox.Cancel:
            return False

        try:
            shutil.rmtree(path)
        except FileNotFoundError as e:
            pass
        # TODO: On restart, reopen the current plan file, rather than the default plan.
        self.request_restart()
        return True

    def msg_box(self, message_text, window_title=None, standard_buttons=None, default_button=None,
                         inform_text=None, detail_text=None):
        if window_title is None:
            window_title = self.tr("Multiscript")
        if standard_buttons is None:
            standard_buttons = QtWidgets.QMessageBox.Ok
        if default_button is None:
            default_button = QtWidgets.QMessageBox.Ok
        box = QtWidgets.QMessageBox()
        box.setWindowTitle(window_title)
        box.setText(message_text)
        if inform_text is not None:
            box.setInformativeText(inform_text)
        if detail_text is not None:
            box.setDetailedText(detail_text)
        box.setIconPixmap(self.windowIcon().pixmap(64, 64))
        box.setStandardButtons(standard_buttons)
        box.setDefaultButton(default_button)
        return box.exec_()

    def request_restart(self, restart_arg_list=None):
        '''Request the app to restart. Note that the restart will only occur once the main event loop
        completes.
        '''
        self.restart_requested = True
        # We use a signal with a queued connection to ensure that restarts requested before the event
        # loop starts are not forgotten, and restarts requested from within a dialog still allow the
        # dialog to close cleanly before all other windows close and the restart occurs.
        self._restart_request.emit(restart_arg_list)

    def _on_restart_request(self, restart_arg_list=None):
        self._restart_arg_list = restart_arg_list
        self.closeAllWindows() # After closing all windows this will end the event loop.

    def execute_restart(self):
        '''This will execute a hard restart of the application. It should only be called from
        the top-level function/script of the app, once the event loop has completed, and only if
        self.restart_requested is True
        '''
        # It seems we need to manually add the current directory to the python path
        env = os.environ
        if 'PYTHONPATH' not in env:
            env['PYTHONPATH'] = './'
        else:
            env['PYTHONPATH'] = './:' + env['PYTHONPATH']
        if self._restart_arg_list is None:
            self._restart_arg_list = []
        args = ['-m', 'multiscript', *self._restart_arg_list]
        os.execvpe(sys.executable, args, env)

    def is_frozen(self):
        '''Return True if we are running as a 'frozen' pyinstaller bundle.
        '''
        # pyinstaller sets the following 2 attributes on the sys module
        return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


class _ExtraZipInfo:
    def __init__(self, zip_info):
        self.info = zip_info
        self.filename = zip_info.filename
        self.path = PurePosixPath(self.filename)
        self.root_name = self.path.parts[0]
        self.final_name = self.path.parts[-1]
