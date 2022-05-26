
import contextlib
import sys

@contextlib.contextmanager
def catch_unhandled_exceptions(q_application = None):
    '''This function can be used as a context manager or decorator. It ensures that
    any unhandled exceptions that occur during the body of a 'with' block or decorated
    function are re-raised at the end of the block/function.

    This is especially useful when testing Qt-related code. Any exception that occurs in
    python code called by Qt (such as signals, event handlers, callbacks etc.) does
    not bubble up through the Qt C++ code. But by ensuring the original call to Qt
    is wrapped by this function, we can capture any python exceptions in the
    signal/event-handler/callback and re-raise them in the calling code. This is
    particularly necessary to ensure unit tests work correctly.

    If a QApplication instance is provided, it is passed to the UnhandledExceptionCatcher.
    Usually, this results in QApplication.exit() being called in the event of an
    unhandled exception being caught. This will result in the Qt event loop exiting.

    Usage as a context manager:
        with catch_unhandled_exceptions():
            # Do something

    Usage as a context manager with instance:
        with catch_unhandled_exceptions() as catcher:
            # catcher will be an instance of UnhandledExceptionCatcher
            # Do something
    
    Usage as a function decorator:
        @catch_unhandled_exceptions()
        def do_something():
            # Do something
    '''
    # Executed as the entry of the context manager:
    catcher = UnhandledExceptionCatcher(q_application)
    catcher.install_hook()

    # Control yielded to the caller (either the body of the context manager, or
    # the body of the function being decorated)
    yield catcher
    
    # Executed as the exit of the context manager:
    catcher.remove_hook()
    if catcher.exception is not None:
        raise catcher.exception


class UnhandledExceptionCatcher:
    def __init__(self, q_application = None):
        '''An optional QApplication instance can be provided. If so, then when an unhandled exception
        is caught, QApplication.exit() will be called. This will result in the Qt event loop exiting.
        '''
        self.previous_excepthook = None
        self.exception_type = None
        self.exception = None
        self.traceback = None
        self.q_application = q_application
    
    def install_hook(self):
        self.previous_excepthook = sys.excepthook
        sys.excepthook = self._excepthook

    def _excepthook(self, type_, value, traceback):
        self.exception_type = type_
        self.exception = value
        self.traceback = traceback
        if self.previous_excepthook is not None:
            self.previous_excepthook(type_, value, traceback)
        if self.q_application is not None:
            self.q_application.exit(1)
    
    def remove_hook(self):
        if sys.excepthook == self._excepthook:
            sys.excepthook = self.previous_excepthook
