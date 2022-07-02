
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

import multiscript
import traceback


def main():
    # On Windows, the Fusion style looks better than the native style
    if multiscript.on_windows():
        QtWidgets.QApplication.setStyle("Fusion")

    app = multiscript.app()

    try:
        app.load_plugins()
        app.ui_init()
        app.exec()
    except BaseException as exception:
        detail_text = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        app.msg_box(app.tr("We're sorry, but an unexpected error has occurred and Multiscript needs to close."),
                    app.tr("Unexpected Error"),detail_text=detail_text)

    multiscript.qt_custom.concurrency.wait_for_nonblock_threads()
    if app.restart_requested:
        app.execute_restart()


if __name__ == "__main__":
    main()
