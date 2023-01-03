
import copy

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyle
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QStyleOptionViewItem as QSOVI


class EnhancedCheckedDelegate(QtWidgets.QStyledItemDelegate):
    '''Delegate with enhanced functionality.
    
    If an item is checked and has no icon and no text, draw the indicator
    (check box or radio button) in the center of the item.
    '''
    def __init__(self, parent=None, use_radio_buttons=False):
        super().__init__(parent)
        self.use_radio_buttons = use_radio_buttons

    def paint(self, painter, option, index):
        style = QtWidgets.QApplication.style()
        self.initStyleOption(option, index)
    
        # If we're not a lone indicator (i.e. there's an icon or text), use the standard delegate.
        if not self._isLoneIndicator(option):
            super().paint(painter, option, index)
            return

        # We now follow the same procedure as QCommonStyle.drawControl() for the CE_ItemViewItem
        # element, except that we don't draw the icon or text, and we ensure the indicator (check box
        # or radio button) is centered in the middle of the item.
        # For more info see:
        # https://code.woboq.org/qt5/qtbase/src/widgets/itemviews/qstyleditemdelegate.cpp.html#379
        # https://code.woboq.org/qt5/qtbase/src/widgets/styles/qcommonstyle.cpp.html#2271
        # See https://wiki.qt.io/Technical_FAQ#How_can_I_align_the_checkboxes_in_a_view.3F

        painter.save()
        painter.setClipRect(option.rect)

        # Draw the background
        style.drawPrimitive(QStyle.PrimitiveElement.PE_PanelItemViewItem, option, painter, None)

        # Draw the indicator
        indicator_style_opt = copy.copy(option)
        indicator_style_opt.rect = self._indicatorRect(option)
        indicator_style_opt.state = indicator_style_opt.state & ~QStyle.StateFlag.State_HasFocus

        if option.checkState == Qt.CheckState.Checked:
            indicator_style_opt.state |= QStyle.StateFlag.State_On
        elif option.checkState == Qt.CheckState.PartiallyChecked:
            indicator_style_opt.state |= QStyle.StateFlag.State_NoChange
        else:
            indicator_style_opt.state |= QStyle.StateFlag.State_Off
        
        if self.use_radio_buttons:
            style.drawPrimitive(QStyle.PrimitiveElement.PE_IndicatorRadioButton,
                                indicator_style_opt, painter, None)
        else:
            # Note: I originally called style.drawPrimitive() using QStyle.PrimitiveElement.PE_IndicatorCheckBox.
            # However, the Fusion style didn't draw the check box. It seems using
            # PE_IndicatorItemViewItemCheck is more reliable
            style.drawPrimitive(QStyle.PrimitiveElement.PE_IndicatorItemViewItemCheck,
                                indicator_style_opt, painter, None)

        # Draw the focus rect. I'm not sure if this will actually be visible, but we're following
        # QCommonStyle.drawControl() to be safe.
        if (option.state & QStyle.StateFlag.State_HasFocus):
            focus_style_opt = copy.copy(option)
            focus_style_opt.rect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemFocusRect, option, None)
            focus_style_opt.state |= QStyle.StateFlag.State_KeyboardFocusChange
            focus_style_opt.state |= QStyle.StateFlag.State_Item
            color_group = QPalette.ColorGroup.Normal if (option.state & QStyle.StateFlag.State_Enabled) \
                          else QPalette.ColorGroup.Disabled
            focus_style_opt.backgroundColor = option.palette.color(color_group,
                QPalette.ColorRole.Highlight if (option.state & QStyle.StateFlag.State_Selected) \
                                             else QPalette.ColorRole.Window)
            style.drawPrimitive(QStyle.PrimitiveElement.PE_FrameFocusRect, focus_style_opt, painter, None)

        painter.restore()

    def sizeHint(self, option, index):
        self.initStyleOption(option, index)

        if self._isLoneIndicator(option):
            return self._indicatorSize(option)
        else:
            return super().sizeHint(option, index)

    def editorEvent(self, event, model, option, index):
        self.initStyleOption(option, index)
               
        if self._isLoneIndicator(option):
            # See https://wiki.qt.io/Technical_FAQ#How_can_I_align_the_checkboxes_in_a_view.3F

            flags = index.flags()
            if not (flags & Qt.ItemFlag.ItemIsUserCheckable) or not (flags & Qt.ItemFlag.ItemIsEnabled):
                return False
            
            if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
                # Clicking anywhere in the current rect is sufficient to check the indicator
                if not option.rect.contains(event.pos()):
                    return False
            elif event.type() == QtCore.QEvent.Type.KeyPress:
                if event.key() != Qt.Key.Key_Space and event.key() != Qt.Key.Key_Select:
                    return False
            else:
                return False
            
            if self.use_radio_buttons:
                newState = Qt.CheckState.Checked
            else:
                newState = Qt.CheckState.Unchecked if option.checkState == Qt.CheckState.Checked \
                                                   else Qt.CheckState.Checked
            result = model.setData(index, newState, Qt.ItemDataRole.CheckStateRole)

            # If we're using radio buttons, clear the sibling radio buttons
            if result and self.use_radio_buttons:
                sibling = index.siblingAtRow(0)
                while sibling.isValid():
                    if sibling.row() != index.row() and \
                        sibling.data(Qt.ItemDataRole.CheckStateRole) != Qt.CheckState.Unchecked:
                        model.setData(sibling, Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
                    sibling = sibling.siblingAtRow(sibling.row()+1)
            return result
        else:
            return super().editorEvent(event, model, option, index)

    def _isLoneIndicator(self, option):
        hasCheckIndicator = True if (option.features & QSOVI.ViewItemFeature.HasCheckIndicator) else False
        hasDecoration = True if (option.features & QSOVI.ViewItemFeature.HasDecoration) else False
        hasDisplay = True if (option.features & QSOVI.ViewItemFeature.HasDisplay) else False
        return (hasCheckIndicator and not hasDecoration and not hasDisplay)

    def _indicatorSize(self, option):
        style = QtWidgets.QApplication.style()
        if self.use_radio_buttons:
            indicatorWidth = style.pixelMetric(QStyle.PixelMetric.PM_ExclusiveIndicatorWidth)
            indicatorHeight = style.pixelMetric(QStyle.PixelMetric.PM_ExclusiveIndicatorHeight)
        else:
            indicatorWidth = style.pixelMetric(QStyle.PixelMetric.PM_IndicatorWidth)
            indicatorHeight = style.pixelMetric(QStyle.PixelMetric.PM_IndicatorHeight)
        return QtCore.QSize(indicatorWidth, indicatorHeight)

    def _indicatorRect(self, option):
        return QStyle.alignedRect(option.direction, Qt.AlignmentFlag.AlignCenter,
                                  self._indicatorSize(option), option.rect)


class EnhanceDataMapperDelegate(QtWidgets.QItemDelegate):
    '''
    For models that store boolean data using the Qt.ItemDataRole.CheckStateRole, and
    need this to be mapped to the checked state of QAbstractButtons
    '''
    def setModelData(self, editor_widget, model, index):
        if isinstance(editor_widget, QtWidgets.QAbstractButton):
            value = Qt.CheckState.Checked if editor_widget.isChecked() else Qt.CheckState.Unchecked
            model.setData(index, value, Qt.ItemDataRole.CheckStateRole)
        else:
            super().setModelData(editor_widget, model, index)
    
    def setEditorData(self, editor_widget, index):
        if isinstance(editor_widget, QtWidgets.QAbstractButton):
            editor_widget.setChecked(True if index.data(Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked \
                                          else False)
        else:
            super().setEditorData(editor_widget, index)
       
