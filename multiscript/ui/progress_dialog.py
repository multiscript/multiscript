
import logging
import traceback

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt

from multiscript.plan.runner import PlanRunner, CancelError
from multiscript.plan.monitor import PlanMonitor
from multiscript.qt_custom.concurrency import call_nonblock, main_thread
from multiscript.ui.progress_dialog_generated import Ui_ProgressDialog
from multiscript.util.util import launch_file


QWIDGETSIZE_MAX = 16777215


class ProgressDialog(QtWidgets.QDialog, Ui_ProgressDialog, PlanMonitor):
    def __init__(self, parent, plan):
        super().__init__(parent)
        self.setupUi()
        self.runner = PlanRunner(plan, self)
        self.future_result = None          # FutureResult of running the runner
        self.path_to_open = None           # File path to launch if Open button clicked
        
        self.logger = logging.getLogger("multiscript")
        self.logger.setLevel(logging.INFO)
        self.log_handler = ProgressDialogLogHandler(self)
        self.logger.addHandler(self.log_handler)

        self.start()
        
    def setupUi(self):
        super().setupUi(self)
        self.last_height_with_details = None    # Last window height when details were shown

        self.showDetailsButton.clicked.connect(self.on_show_details_button_clicked)
        self.openButton.clicked.connect(self.on_open_clicked)
        self.cancelButton.clicked.connect(self.on_cancel)
        self.actionButton.clicked.connect(self.on_action_clicked)
        self.finished.connect(self.on_finished)

        self.on_show_details_button_clicked(False)
        self.set_status_text(self.tr("Running..."))
        self.actionButton.setText(self.tr("Pause"))
        self.action = self.on_pause # Holds method that will be called when actionButton clicked

    def tr(self, str):
        return QtWidgets.QApplication.translate(self.__class__.__name__, str, None, -1)

    def on_show_details_button_clicked(self, checked):
        # For some reason, these visual changes produce temporary visual artefacts, unless
        # we suspend updates until we're done.
        self.setUpdatesEnabled(False)
        if checked:
            self.detailsTextEdit.show()
            self.setMaximumHeight(QWIDGETSIZE_MAX)  # Allow vertical resizing. Must be done before calling adjustSize()
            width = self.width()                    # Save the width so we can preserve it.
            self.adjustSize()                       # Resize to new minimum size
            self.setMinimumHeight(self.height())    # Disable reducing the vertical size less than the minimum
            if self.last_height_with_details is not None:
                self.resize(width, self.last_height_with_details)   # Restore the saved width
            else:
                self.resize(width, self.height())   # Restore the saved width
        else:
            self.detailsTextEdit.hide()
            self.last_height_with_details = self.height()
            self.setMinimumHeight(0)                # Actually min height will be calculated by widget heights
            width = self.width()                    # Save the width so we can preserve it.
            self.adjustSize()                       # Resize to new minimum size
            self.resize(width, self.height())       # Restore the saved width
            self.setFixedHeight(self.height())      # Disable vertical resizing
        self.setUpdatesEnabled(True)
    
    def start(self):
        passage_count = len(self.runner.bible_ranges)
        version_count = len(self.runner.all_versions)
        self.passagesLabel.setText(str(passage_count) + " " + self.tr("passage(s):") + " " + 
                                   str(self.runner.bible_ranges))
        self.versionsLabel.setText(str(version_count) + " " + self.tr("version(s):") + " " + 
                                   ", ".join([version.abbrev for version in self.runner.all_versions]))
        self.future_result = call_nonblock(self.runner.run, callback=self.runner_finished)

    def on_action_clicked(self, checked):
        if self.action is not None:
            self.action()

    def on_pause(self):
        if self.future_result is not None:
            self.future_result.pause()
            self.set_status_text(self.tr("Pausing..."))
            self.actionButton.setText(self.tr("Resume"))
            self.action = self.on_resume
    
    def on_resume(self):
        if self.future_result is not None:
            self.future_result.resume()
            self.set_status_text(self.tr("Resuming..."))
            self.actionButton.setText(self.tr("Pause"))
            self.action = self.on_pause

    def on_continue(self):
        if self.future_result is not None:
            self.future_result.resume()
            self.set_status_text(self.tr("Continuing..."))
            self.actionButton.setText(self.tr("Pause"))
            self.action = self.on_pause
            self.path_to_open = None
            self.openButton.setEnabled(False)

    def on_cancel(self):
        if self.future_result is not None:
            self.set_status_text(self.tr("Cancelling..."))
            self.future_result.cancel()
        else:
            self.reject()
    
    def runner_finished(self, future_result):
        self.future_result = None
        if future_result.is_cancelled:
            self.reject()
        else:
            if future_result.error is None:
                self.set_status_text(self.tr("<b>Finished</b>"))
                self.set_substatus_text("")
            else:
                error = future_result.error
                self.set_status_text(self.tr("<b>An error interrupted the plan.</b>"))
                self.set_substatus_text(type(error).__name__)
                detail_text = "".join(traceback.format_exception(type(error), error, error.__traceback__))
                self.detailsTextEdit.appendPlainText(detail_text)

            self.actionButton.setText(self.tr("Done"))
            self.action = self.on_done

    def on_done(self):
        self.accept()

    def on_open_clicked(self, checked):
        if self.path_to_open is not None:
            launch_file(self.path_to_open)

    def closeEvent(self, event):
        event.ignore()      # Necessary to prevent the dialog closing immediately
        self.on_cancel()

    def on_finished(self, result):
        self.logger.removeHandler(self.log_handler)

    @main_thread
    def append_text_to_details(self, text):
        self.detailsTextEdit.appendPlainText(text)

    #
    # PlanMonitor methods.
    #
    # By default these will be called by PlanRunner.run(), and therefore be running
    # in the worker thread. When we need to update the gui, we either have to
    # use call_main_thread(), or use the @main_thread decorator to ensure the whole
    # method is called on the main thread.
    #

    @main_thread
    def set_progress_percent(self, progress):
        self.progressBar.setValue(int(progress))

    @main_thread
    def set_status_text(self, text):
        self.statusLabel.setText(text)
        # We seem to get visual glitches unless we repaint the label.
        self.statusLabel.repaint()

    @main_thread
    def set_substatus_text(self, text):
        self.substatusLabel.setText(text)
        # We seem to get visual glitches unless we repaint the label.
        self.substatusLabel.repaint()

    def allow_cancel(self):
        '''Runs in worker thread.
        '''
        if self.future_result is not None:
            if self.future_result.is_paused:
                self.set_status_text(self.tr("Paused"))
                self.future_result.wait_for_resume()
            if self.future_result.is_cancelled:
                raise CancelError()

    def request_confirmation(self, message=None, path=None):
        '''Runs in worker thread.
        '''
        if self.future_result is not None:
            self.future_result.pause()
            if message is not None:
                self.set_status_text(message)
                self.set_substatus_text("")
            if path is not None:
                self.set_path_to_open(path)
            self.actionButton.setText(self.tr("Continue"))
            self.action = self.on_continue
            self.future_result.wait_for_resume()
            if self.future_result.is_cancelled:
                raise CancelError()

    @main_thread
    def set_path_to_open(self, path=None):
        if path is not None:
            self.path_to_open = path
            self.openButton.setEnabled(True)

    #
    # End of PlanMonitor methods.
    #



class ProgressDialogLogHandler(logging.Handler):
    def __init__(self, progress_dialog):
        super().__init__()
        self.progress_dialog = progress_dialog

    def emit(self, record):
        ''' May run in main thread or worker thread.
        '''
        try:
            message = self.format(record)
            self.progress_dialog.append_text_to_details(message)
        except Exception:
            self.handleError(record)
