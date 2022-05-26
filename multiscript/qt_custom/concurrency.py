
import functools
import threading
import sys
import time
import traceback

from PySide2.QtCore import Qt, QObject, QMetaObject, QThread, Slot
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QWindow

from multiscript.util.exception import MultiscriptException


def call_nonblock(callable, *args, callback=None, **kwargs):
    """Execute the callable without blocking, using threads.
    Returns a FutureResult, which will receive the result of the callable.
    
    If supplied, the callback is executed when the callable completes or raises
    an exception. The callback is executed on the main event loop thread, and
    receives one argument: the same FutureResult, which now contains the result
    of the callable and any error that occurred:
        def callback(future_result):
            pass

    A QApplication instance must be created before calling this function.
    """
    future_result = FutureResult()
    thread = _Call_NonBlock_Thread(callable, *args, future_result=future_result,
                                   callback=callback, **kwargs)
    thread.start()
    return future_result


class _Call_NonBlock_Thread(QThread):
    """A thread class for executing non-blocking calls.

    A QApplication instance must have been created prior to instantiating this class.
    """
    # We maintain a list of instances of this class, to ensure instances are not accidentally
    # garbage collected before the thread has finished.
    # We use a lock to protect this list. Technically the Python global interpreter lock
    # should make our lock unnecessary, but we include it anyway, just to be safe.
    instances = []
    instances_lock = threading.RLock()

    @classmethod
    def wait_for_all(cls):
        """Wait for all unfinished _Call_NonBlock_Thread to finish.
        """
        threads = []
        with _Call_NonBlock_Thread.instances_lock:
            threads = _Call_NonBlock_Thread.instances.copy()
        
        print(len(threads),"thread(s) to wait for")
        for thread in threads:
            thread.wait()

    def __init__(self, callable_obj, *args, future_result=None, callback=None, **kwargs):
        super().__init__()
        self.callable = callable_obj
        self.args = args
        self.future_result = future_result
        if self.future_result is None:
            self.future_result = FutureResult()
        self.callback = callback
        self.kwargs = kwargs
        self.setObjectName("QThread (Python id " + str(id(self)) + ")")
        
        # We use the finished signal to remove our saved instance of ourselves.
        # It's safest for this to occur on the main thread, when we have confidence
        # the QThread object is ready to be deleted. We use Qt.QueuedConnection
        # to make the finished signal be received on the main thread.
        self.finished.connect(self.on_finished, type=Qt.QueuedConnection)
        
        with _Call_NonBlock_Thread.instances_lock:
            _Call_NonBlock_Thread.instances.append(self)

    def on_finished(self):
        # Now this thread has completed, it's safe to remove our saved instance of it
        # print("on_finished thread: ", QThread.currentThread().objectName())
        with _Call_NonBlock_Thread.instances_lock:
            _Call_NonBlock_Thread.instances.remove(self)

    def run(self):

        result = None
        exception = None
        
        try:
            result = self.callable(*self.args, **self.kwargs)
        except BaseException as e:
            # Save the exception, for when e goes out of scope
            exception = e
        finally:
            self.future_result.set(result, exception)
            if self.callback is not None:
                call_main_thread(self.callback, self.future_result)
            if exception is not None:
                # We don't want to re-raise the exception (which, if caught at a global
                # level might result in termination of the program). Instead, it's up
                # to the callback to decide what to do with the exception. However,
                # we do print the exception to the console, to assist with debugging.
                print("Caught exception during non-blocking call:")
                traceback.print_exception(type(exception), exception, exception.__traceback__)


class FutureResult():
    '''A simple class to allow one thread to wait for a result from another thread.
    A result value or error can only be set once for a given FutureResult instance.
    set() is used both to set the result, or alternatively, the error.

    The class also allows a cancelled condition to be set. Note that this will not
    actually cancel the worker thread, unless it is explicitly written to check
    the is_cancelled property of this FutureResult.

    The class also allows a pause condition to be set. Note that this will not
    actually pause the worker thread, unless it is explicitly written to check
    the is_paused property or call wait_for_resume.
    
    Calling cancel() will also call resume() to wake up any thread waiting for
    the end of pausing. But calling cancel() will not call set() and not directly
    set a result or error. Instead, the worker thread needs to poll is_cancelled,
    and if it is set, it's up to the worker thread what result is returned or 
    error is raised.
    '''
    def __init__(self):
        self._result_condition = threading.Condition()
        self._value = None          # Access controlled by self._result_condition
        self._error = None          # Access controlled by self._result_condition
        self._is_set = False        # Access controlled by self._result_condition
        self._is_cancelled = False  # Access controlled by self._result_condition
        
        self._paused_condition = threading.Condition()
        self._is_paused = False # Accesss controlleb by self._paused_condition
    
    @property
    def value(self):
        """Return the current value of the result, without waiting. If a value has not been
        set, return None.
        """
        with self._result_condition:
            return self._value

    @property
    def error(self):
        """Return any error set on the result, without waiting. If an error has not been
        set, return None.
        """
        with self._result_condition:
            return self._error

    @property
    def is_set(self):
        with self._result_condition:
            return self._is_set

    def wait(self):
        """Wait for the result value to be set, then return it.
        """
        with self._result_condition:
            while not self._is_set:
                self._result_condition.wait()
        return self._value

    def set(self, value=None, error=None):
        with self._result_condition:
            if self._is_set:
                raise FutureResultError("Can't set a second value.")
            self._value = value
            self._error = error
            self._is_set = True
            self._result_condition.notify()
    
    @property
    def is_cancelled(self):
        with self._result_condition:
            return self._is_cancelled

    def cancel(self):
        '''Sets is_cancelled to True, then calls resume()
        '''
        with self._result_condition:
            self._is_cancelled = True
        self.resume()

    @property
    def is_paused(self):
        with self._paused_condition:
            return self._is_paused
    
    def pause(self):
        '''Sets is_paused to True (in a thread-safe manner).
        '''
        with self._paused_condition:
            self._is_paused = True

    def resume(self):
        '''Sets is_paused to False (in a thread-safe manner), and wakes any thread
        waiting for this resume call.
        '''
        with self._paused_condition:
            self._is_paused = False
            self._paused_condition.notify()

    def wait_for_resume(self):
        '''If is_paused is True, wait for resume to be called.
        If is_paused is False, returns immediately.
        '''
        with self._paused_condition:
            while self._is_paused:
                self._paused_condition.wait()


class FutureResultError(MultiscriptException):
    pass


def wait_for_nonblock_threads():
    """Waits for any unfinished threads associated with calls to call_nonblock().

    While Python automatically waits for its own non-daemon Python threads,
    we have to manually wait to any unfinished QThreads. It's therefore wise to
    call this method after the completion of the main thread event loop.
    """
    _Call_NonBlock_Thread.wait_for_all()

def call_main_thread(callable, *args, **kwargs):
    """Execute the callable on the main event loop thread. Returns a FutureResult
    immediately without waiting for the callable to executed.
    
    While Qt signals and slots are generally thread-safe, this method is a
    simpler way to invoke a function on the main thread without having to set up
    extra signals and slots. Internally, it relies onQMetaObject.invokeMethod().
    """
    future_call = _FutureCall(callable, *args, **kwargs)
    QMetaObject.invokeMethod(future_call, "call")
    return future_call.future_result

def wait_main_thread(callable, *args, **kwargs):
    """Execute the callable on the main event loop thread, and wait for a result
    to be received. Returns a FutureResult containing both the result value and
    any error raised.

    While Qt signals and slots are generally thread-safe, this method is a
    simpler way to invoke a function on the mainloop without having to set up
    extra signals and slots. Internally, it relies on QMetaObject.invokeMethod().
     """
    future_result = call_main_thread(callable, *args, **kwargs)
    future_result.wait()
    return future_result


class _FutureCall(QObject):
    """Represents a callable, together with its arguments, to be called on the main event loop
    on the main thread.

    Based on callafter.py by Florian Rheim at https://gist.github.com/FlorianRhiem/41a1ad9b694c14fb9ac3
    to which he attached an MIT Licence at https://gist.github.com/FlorianRhiem/871e455b672157729cb66cf9879ed7db
    """
    # We maintain a list of instances of this class, to ensure instances are not accidentally
    # garbage collected between when the _FutureCall is instantiated, and when its call()
    # slot is executed.
    # We use a lock to protect this list. Technically the Python global interpreter lock
    # should make our lock unnecessary, but we include it anyway, just to be safe.
    instances = []
    instances_lock = threading.RLock()
 
    def __init__(self, callable_obj, *args, **kwargs):
        super().__init__()
        self.callable = callable_obj
        self.args = args
        self.kwargs = kwargs
        self.future_result = FutureResult()
        
        # Ensure this QObject has affinity with the main thread, so that call() will 
        # be invoked on the main thread.
        self.moveToThread(QApplication.instance().thread())

        with _FutureCall.instances_lock:
            _FutureCall.instances.append(self)

    @Slot()
    def call(self):
        with _FutureCall.instances_lock:
            _FutureCall.instances.remove(self)
        
        # TODO: Trap any exception the callable raises, and store it in the future result.
        result = self.callable(*self.args, **self.kwargs)
        self.future_result.set(result)


def main_thread(orig_function=None, *, some_arg=None):
    """Function decorator that ensures a function executes on the main event loop thread.
    """
    # Note that writing the decorator with the signature above allows us to easily add
    # arguments to the decorator if we wish to later on
    def decorate(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            call_main_thread(function, *args, **kwargs)
        return wrapper

    if orig_function:
        # The decorator was written without arguments, and so was called with just the function
        # to be decorated.
        return decorate(orig_function)
    else:
        # The decorator was written with arguments, and so was called first with those arguments.
        # We now return a function that the system will then call with the function to be decorated.
        return decorate

