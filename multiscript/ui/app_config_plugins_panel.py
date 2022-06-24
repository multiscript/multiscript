
from pathlib import Path

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt

import multiscript
from multiscript.plugins import BUILTIN_PLUGIN_ID
from multiscript.qt_custom.models import ItemListTableModel
from multiscript.qt_custom.model_columns import ModelColumnType, AttributeColumn, BooleanColumn
from multiscript.qt_custom.widgets import ConfigWidget
from multiscript.ui.app_config_plugins_panel_generated import Ui_PluginsAppConfigPanel
from multiscript.util.util import launch_file

class PluginsAppConfigPanel(ConfigWidget, Ui_PluginsAppConfigPanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()

        self.altPluginsPath = None  # Local copy of the alternative plugins path
        
    def setupUi(self):
        super().setupUi(self)
        if multiscript.on_mac():
            self.verticalLayout.setSpacing(6)
        
        self.addPluginButton.clicked.connect(self.on_add_plugin_button_clicked)
        self.removePluginButton.clicked.connect(self.on_remove_plugin_button_clicked)
        self.altPluginsPathSelectButton.clicked.connect(self.on_alt_plugins_path_select_button_clicked)
        self.altPluginsPathShowButton.clicked.connect(self.on_alt_plugins_path_show_button_clicked)
        self.altPluginsPathClearButton.clicked.connect(self.on_alt_plugins_path_clear_button_clicked)

        self.pluginTableModel = ItemListTableModel() # A copy of the list of plugins
        self.pluginTableModel.append_model_columns([
            AttributeColumn(self.tr("Name"),    "name"),
            AttributeColumn(self.tr("ID"),      "id"),
            AttributeColumn(self.tr("Sources"), lambda plugin: ", ".join([source.name for source in plugin.all_sources])),
            AttributeColumn(self.tr("Outputs"), lambda plugin: ", ".join([output.name for output in plugin.all_outputs])),
            AttributeColumn(self.tr("Location"),lambda plugin: str(plugin.base_path)),
        ])
        self.pluginTableModel.set_all_columns_editable(False)
        self.pluginsTableView.setModel(self.pluginTableModel)
        self.reload_plugin_table()

    def reload_plugin_table(self):
        self.pluginTableModel.clear_items()
        self.pluginTableModel.append_items(multiscript.app().all_plugins)
        self.pluginsTableView.refresh(resize_cols=True)

    def load_config(self, config):
        '''Load the contents of config into this widget.
        '''
        if config.altPluginsPath is None:
            self.on_alt_plugins_path_clear_button_clicked()
        else:
            self.altPluginsPath = config.altPluginsPath
            self.set_alt_plugins_path(self.altPluginsPath)

    def on_add_plugin_button_clicked(self, checked=False):
        plugin_instance = multiscript.app().add_plugin()
        if plugin_instance is not None:
            self.pluginTableModel.append_item(plugin_instance)
            self.pluginsTableView.refresh(resize_cols=True)
        else:
            # On macOS, if we don't manually close the dialog prior to a restart, we get the warning:
            # 'modalSession has been exited prematurely - check for a reentrant call to endModalSession'
            if multiscript.app().restart_requested:
                self.window().accept()

    def on_remove_plugin_button_clicked(self, checked=False):
        selected_plugins = self.pluginsTableView.get_selected_items()
        if len(selected_plugins) == 0:
            # Nothing selected
            return
        for plugin in selected_plugins:
            if plugin.id != BUILTIN_PLUGIN_ID:
                multiscript.app().remove_plugin(plugin.id)

        # On macOS, if we don't manually close the dialog prior to a restart, we get the warning:
        # 'modalSession has been exited prematurely - check for a reentrant call to endModalSession'
        if multiscript.app().restart_requested:
            self.window().accept()

    def save_config(self, config):
        '''Save the contents of this widget into config.
        '''
        config.altPluginsPath = self.altPluginsPath

    def on_alt_plugins_path_select_button_clicked(self, checked=False):
        existing_path_str = str(self.altPluginsPath)
        if self.altPluginsPath is None:
            existing_path_str = str(multiscript.app().user_docs_path)
        
        new_path_str = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select Destination Folder"),
                                                                  existing_path_str)
        if len(new_path_str) > 0:
            self.altPluginsPath = Path(new_path_str)
            self.set_alt_plugins_path(new_path_str)
    
    def set_alt_plugins_path(self, path):
        path = Path(path)   # Ensure we have a Path object, and not just a string
        self.altPluginsPathLabel.setText(str(path))
        self.altPluginsPathIconLabel.setFileIconFromPath(path)

    def on_alt_plugins_path_show_button_clicked(self, checked=False):
        if self.altPluginsPath is not None and self.altPluginsPath.exists():
            launch_file(self.altPluginsPath)

    def on_alt_plugins_path_clear_button_clicked(self, checked=False):
        self.altPluginsPath = None
        self.altPluginsPathLabel.clear()
        self.altPluginsPathIconLabel.clear()
