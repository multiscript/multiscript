
import pathlib

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

import multiscript


class IconLabel(QtWidgets.QLabel):
    '''QLabel subclass that allows an icon to be easily set that will scale to the label's size while maintaining
    aspect ratio.

    This class is useful because QLabel's allow a pixmap to be set, but not an icon, and it takes a bit of work
    to scale an icon to a label's existing size while maintaining the icon's natural aspect ratio.
    '''
    def setIcon(self, icon):
        '''Set the label to display the icon, scaled to the label's current size while maintaining the icon's
        aspect ratio.
        '''
        self._icon = icon
        max_size = None
        if len(icon.availableSizes()) > 0:
            max_size = icon.availableSizes()[-1] # Get the largest icon available
        else:
            # It's probably an SVG icon, so we just pick a big size
            max_size = QtCore.QSize(2048, 2048)
        
        # Re high-DPI screens:
        #   * On macOS, we have multiply the required sieze by the device pixel ratio (e.g. 2)
        #   * On Windows, this scaling seems to be unnecessary.
        scale_factor = self.devicePixelRatioF() if multiscript.on_mac() else 1
        pixmap = icon.pixmap(max_size).scaled(self.size() * scale_factor,
                                              Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(pixmap)
    
    def icon(self):
        '''Return the last icon set on the label, or None if no icon has been set.
        '''
        icon = None
        try:
            icon = self._icon
        except AttributeError:
            pass
        return icon
    
    def setFileIconFromPath(self, path):
        '''Set the label to the display the file icon of the file at the given path. The file must exist.
        '''
        provider = QtWidgets.QFileIconProvider()
        info = QtCore.QFileInfo(str(path))
        icon = provider.icon(info)
        self.setIcon(icon)


class ConfigWidget(QtWidgets.QWidget):
    '''Base class for QtWidgets that provide UI for instances of the
    Config class or its subclasses, using a load/store mechanism.
    '''
    def load_config(self, config):
        '''Subclasses override this method to load the contents of config into this widget.
        '''
        pass

    def save_config(self, config):
        '''Subclasses override this method to save the contents of this widget into config.
        '''
        pass


class ConfigSubform(QtWidgets.QWidget):
    '''Base class for QtWidgets that provide UI for instances of the
    Config class or its subclasses, using a subform mechanism
    '''
    def add_mappings(self, form, *args, **kwargs):
        '''Subclasses override this method to add mappings between the widgets
        on this subform to fields in an underlying ItemListTableModel. Subclasses
        do this by calling add_model_column_and_widget() on the supplied parent form.
        The parent form will then ensure the widgets are updated as the selected item
        in the model changes.

        Extra *args and **kwargs are allowed so that subclasses can supply other useful
        objects at the time the mappings are created.
        '''
        pass


class OutputConfigSubform(ConfigSubform):
    '''ConfigSubform for config associated with a BibleOutput
    '''
    def add_mappings(self, form, bible_output, *args, **kwargs):
        '''In addition to the form, this class also supplies the associated BibleOutput.'''
        pass

