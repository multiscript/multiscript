from collections import Counter
from pathlib import Path, PurePosixPath
import logging
import os
import shutil
import subprocess
import sys
import traceback
import zipfile

import pluginlib
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QStandardPaths

import multiscript
from multiscript import plan
from multiscript.qt_custom.concurrency import call_main_thread_later
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
        self._plugins = []          # Current list of loaded plugins
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
        '''Returns the plugin instance with the given id, or None if there is no loaded
        plugin with that id.
        '''
        if id in self._plugins_by_id:
            return self._plugins_by_id[id]
        else:
            return None

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
        if self.app_plugin_dir_path is not None and self.app_plugin_dir_path.is_dir():
            plugin_base_paths.append(self.app_plugin_dir_path)
        alt_plugins_path = self.app_config_group.plugins.altPluginsPath
        if alt_plugins_path is not None and alt_plugins_path.is_dir():
            plugin_base_paths.append(alt_plugins_path)
        
        for base_path in plugin_base_paths:
            self._load_plugins_at_base_path(base_path)

    def _load_plugins_at_base_path(self, base_path):
        _logger.debug(f"Searching for plugins in base path {base_path}")
        for sub_path in Path(base_path).iterdir():
            self._load_plugin_at_path(sub_path)

    def _load_plugin_at_path(self, path):
        '''Load any available plugin at the specified path. Returns the plugin instance if successful,
        otherwise returns None.

        Can be safely called multiple times to discover any newly added plugins at the path.
        '''
        path = Path(path) # Ensure we have a path object, and not just a str
        # Ignore the path if it's not a directory, or it's hidden
        if not path.is_dir() or path.name[0] == '.':
            return None
        # Ignore any source code for test plugin in the alt plugins directory
        if path.name == 'app_multiscript_test_plugin' and \
           path.parent == self.app_config_group.plugins.altPluginsPath:
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
            _logger.debug(f"\t\tNo new plugins found in directory: {search_path.name}")
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        MultiscriptBaseApplication.__init__(self) # Necessary because QApplication doesn't call super().__init__
        
        # Cmd-line arguments we also expect to receive as FileOpen events. See self.event() below.
        self._expected_open_file_event_args = set(sys.argv[1:])

        self.restart_requested = False # True if a restart should occur after the event loop ends
        self._restart_arg_list = [] # Command-line arguments to be passed to any restart
        
        self.main_window = None
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
        
        # Load any plugin first, in case the plan depends on it
        if plugin_path is not None:
            # Before loading the plugin, save any command-line plan arg in the restart
            # args, so that if adding the plugin causes a restart, we don't forget the plan
            if plan_path is not None:
                self._restart_arg_list = [plan_path]
            self.add_plugin(plugin_path) # Note this could result in a restart request
            # If no restart is needed, remove any plan from the restart arg list.
            if not self.restart_requested:
                self._restart_arg_list = []

        if not self.restart_requested:
            if plan_path is not None:
                self.main_window.load_plan(plan_path)
            else:
                # Load default plan
                self.main_window.load_plan(plan.get_default_plan_path())

            self.main_window.show()

    def exec(self):
        '''If we're not running as a 'frozen' pyinstaller bundle, this calls exec() in our superclass
        as normal.

        If we *are* running as a 'frozen' pyinstaller bundle, we still call exec() in the superclass,
        but we ensure that any unhandled exceptions are caught raised to the caller.
        '''
        if self.restart_requested:
            # Since a restart has already been requested, just exit straightaway.
            return 0

        if not self.is_frozen():
            return super().exec()
        else:
            result = 0
            with catch_unhandled_exceptions(self):
                result = super().exec()                  
            return result

    def exec_catches_exceptions(self):
        '''Same as exec(), but rather than reraising unhandled exceptions, we catch them here
        and display them in a dialog.
       '''
        if self.restart_requested:
            # Since a restart has already been requested, just exit straightaway.
            return 0

        result = 0
        try:
            result = self.exec()
        except BaseException as exception:
            detail_text = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            self.msg_box(self.tr("We're sorry, but an unexpected error has occurred and Multiscript needs to close."),
                         self.tr("Unexpected Error"),detail_text=detail_text)
        
        return result

    def event(self, e):
        #
        # On Mac only, files are opened via AppleEvents, which Qt exposes as a (Mac-only) FileOpen
        # Qt event. However, it's possible that some of these FileOpen events are duplicates
        # of the files passed to the app as commmand line arguments. This can happen:
        #   1. When running from the command-line with command-line arguments (either unfrozen or
        #      frozen).
        #   2. When launched from the Finder when frozen with pyinstaller if pyinstaller's
        #      argv-emulation is turned on. In this case, pyinstaller catches the initial open
        #      event and supplies the same info as a command-line argument. One advantage of this
        #      is that we can immediately open the file at startup, rather than waiting for our
        #      code to process an event.
        #
        # All of this means that it's possible be notified twice about opening a file: once on the
        # command-line, and once as a FileOpen event. Therefore, at startup, we create a set of
        # the command-line args in self._expected_open_file_event_args. When we receive a FileOpen
        # event, if the path is already in this set, we ignore the event, and remove the path
        # from the set. Otherwise we process the event as normal.
        #
        if e.type() == QtCore.QEvent.FileOpen:
            path_str = e.file()
            if path_str in self._expected_open_file_event_args:
                # Duplicate file open notification
                self._expected_open_file_event_args.remove(path_str)
                return super().event(e)

            path = Path(path_str)
            if path.suffix == plan.PLAN_FILE_EXTENSION:
                self.main_window.load_plan(path)
                return True
            elif path.suffix == PLUGIN_FILE_EXTENSION:
                # If the user launches the app by double-clicking on a file, it seems
                # we can receive a FileOpenEvent even before we've completed showing
                # our main_window. If they double-clicked on a plugin, and there's no argv
                # emulation in place, we can end up here trying to add a plugin before
                # the main window is ready. This can result in a crash, especially if the
                # user agrees to reload the plan after the plugin is added.
                #
                # To avoid this potential crash, we wrap the call to add_plugin()
                # using call_main_thread_later(). This posts the add_plugin() call
                # onto the event loop, to be executed once any other pending events
                # have been handled. This allows the main window to finish showing
                # before the execution of add_plugin().
                call_main_thread_later(self.add_plugin, path, offer_plan_reload=True)
                return True
        
        return super().event(e)

    def add_plugin(self, path=None, show_ui=True, offer_plan_reload=False):
        '''Installs a plugin, given the path to the .mplugin file. If path is None,
        the user will be prompted for the .mplugin file.

        If show_ui is True, prompts and dialogs will be shown. Set to false for a silent install.
        If show_ui is False, path must not be None.
        If show_ui is True and offer_plan_reload is True, then after the plugin is successfully
        installed, the main window will offer for the open plan to be reloaded (provided the main
        window exists.) 
        
        If the plugin is succesfully installed, returns the plugin instance. Otherwise returns None.
        '''
        if path is None:
            # Prompt for plugin to add
            if not show_ui:
                return None

            # TODO: Set the default loading directory for the dialog to something like the documents folder
            path_str, selected_filter = QtWidgets.QFileDialog.getOpenFileName(None, self.tr("Select Plugin"),
                                                                                None, PLUGIN_FILE_FILTER)
            if len(path_str) == 0:
                # Cancel
                return None
            path = Path(path_str)
        
        if not zipfile.is_zipfile(path):
            if show_ui:
                self.msg_box(self.tr('This file is not a valid plugin.'), self.tr("Plugin Error"))
            return None
        
        try:
            file = zipfile.ZipFile(path)
        except BaseException as e:
            if show_ui:
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
                if show_ui:
                    self.msg_box(self.tr('The plugin was not loaded as it contains more than one top-level file/folder.'),
                                 self.tr("Plugin Error"))
                return None

            plugin_id = list(root_names_count)[0]
            
            # There should be an entry for the top-level folder and at least one file/folder under it.
            if root_names_count[plugin_id] < 2:
                if show_ui:
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
                if show_ui:
                    result = self.msg_box(self.tr(f"There is an existing plugin with id '{plugin_id}' named '{existing_plugin_name}'. ") + 
                                          self.tr("Do you wish to replace it?\n\n") + 
                                          self.tr("This will require restarting Multiscript."),
                                          self.tr("Replace Plugin?"),
                                          QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok)
                else:
                    # For silent install, just go ahead and overwrite the plugin
                    result = QtWidgets.QMessageBox.Ok

                if result == QtWidgets.QMessageBox.Cancel:
                    return None
                else:
                    # Remove the existing plugin. We therefore need to restart, and we'll
                    # save installing the plugin for the restart.
                    shutil.rmtree(new_plugin_path)
                    self.request_restart([path]) # Pass the plugin zip file as an argument to the restart.
                    return None

            if show_ui:
                # Using Python to extract a zip file can be quite slow, so we show a progress dialog.
                progress_dialog = QtWidgets.QProgressDialog(self.activeWindow())
                progress_dialog.setWindowTitle(self.tr('Installing Plugin'))
                progress_dialog.setMinimumWidth(300)
                progress_dialog.setLabelText(self.tr(f"Installing plugin '{plugin_id}'..."))
                progress_dialog.setMinimum(0)
                progress_dialog.setMaximum(len(extra_infos))
                progress_dialog.setMinimumDuration(0)
                progress_dialog.setCancelButton(None)
                progress_dialog.open()
            for i in range(len(extra_infos)):
                extra_info = extra_infos[i]
                dest_path = file.extract(extra_info.info, path=self.app_plugin_dir_path)
                if show_ui:
                    progress_dialog.setValue(i)
            if show_ui:
                progress_dialog.close()

            # Now we've extracted the plugin, try to import it.
            new_plugin_instance = self._load_plugin_at_path(new_plugin_path)
            if new_plugin_instance is None:
                if show_ui:
                    self.msg_box(self.tr(f"The plugin with '{plugin_id}' id could not be loaded."),
                                 self.tr("Plugin Error"))
                shutil.rmtree(new_plugin_path)
                return None

            if show_ui:
                self.msg_box(self.tr(f"The plugin '{new_plugin_instance.name}' was successfully installed."),
                             self.tr("Plugin Installed"))
                if offer_plan_reload and self.main_window is not None:
                    self.main_window.offer_plan_reload()

            return new_plugin_instance

    def remove_plugin(self, plugin_id, show_ui=True):
        '''Deletes the plugin on disk with the given id. If there is no plugin with the given id, this
        method does nothing.
        
        If show_ui is True, prompts and dialogs will be shown. Set to false for a silent removal.

        Returns True if the plugin was deleted, otherwise False. This method requests a restart, which
        is necessary to completely remove the plugin from memory.
        '''
        plugin = self.plugin(plugin_id)
        if plugin is None:
            return False
        
        id = plugin.id
        name = plugin.name
        path = plugin.base_path
        if show_ui:
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
        '''Convenience method for showing a message box.
       '''
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
        return box.exec()

    def request_restart(self, restart_arg_list=None):
        '''Request the app to restart. Note that the restart will only occur once the main event loop
        completes.
        '''
        self.restart_requested = True

        if restart_arg_list is None:
            restart_arg_list = []
        # Note that the restart arg list may already contain the path to a yet-to-be-opened plan.
        self._restart_arg_list.extend(restart_arg_list)

        # If instead there is an open plan, add it's path to the restart args, so we'll reopen it upon
        # restart.
        if self.main_window is not None and self.main_window.plan is not None:
            plan = self.main_window.plan
            if not plan.new: # If plan isn't new, it must have a path
                path = plan.path
                if plan._orig_path is not None:
                    # Plan was modified due to missing plugins and not yet saved. Use orig path instead
                    path = plan._orig_path
                self._restart_arg_list.append(path)

        # Closing all windows will end the event loop, which in turn allows the restart to occur.
        # We use call_main_thread_later() to post the call to closeAllWindows() to the event loop.
        # This ensures restarts requested before the event loop begins re not forgotten, and that
        # restarts requested from within a dialog still allow the dialog to close cleanly before
        # all other windows close and the restart occurs.
        call_main_thread_later(self.closeAllWindows)

    def execute_restart(self):
        '''This will execute a hard restart of the application. It should only be called from
        the top-level function/script of the app, once the event loop has completed, and only if
        self.restart_requested is True
        '''
        # It seems we need to manually add the current directory to the python path
        env = os.environ
        current_dir_path = str(Path('.'))
        path_sep = ";" if multiscript.on_windows() else ":"
        if 'PYTHONPATH' not in env:
            env['PYTHONPATH'] = current_dir_path
        else:
            env['PYTHONPATH'] = current_dir_path + path_sep + env['PYTHONPATH']
        
        if self._restart_arg_list is None:
            self._restart_arg_list = []
        self._restart_arg_list = [str(arg) for arg in self._restart_arg_list] # Ensure all args are strings
        if multiscript.on_windows():
            # On Windows, the os.exec* functions seem to require us to further escape cmd-line arguments, in case
            # they have any spaces etc. The simplest way to do this is to use an undocumented function in
            # the subprocess module named list2cmdline. It returns all the arguments as one giant escaped string.
            self._restart_arg_list = [subprocess.list2cmdline(self._restart_arg_list)]
        
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
