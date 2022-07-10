import unittest
import time

from PySide6.QtCore import QThread
from PySide6.QtGui import QWindow

import multiscript
from multiscript.qt_custom.concurrency import *
from multiscript.util.exception_catcher import catch_unhandled_exceptions
from test.application import TEST_APP


CALL_LATER_TEST_STRING = "Expected value" # For testing call_main_thread_later


class TestConcurrency(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MAIN_THREAD_NAME = "Main thread"

    def setUp(self):
        QThread.currentThread().setObjectName(self.MAIN_THREAD_NAME)

    # We use the catch_unhandled_exceptions decorator to ensure any exceptions
    # in code called by Qt (in this case: our callbacks) are re-raised and so
    # do result in the test failing.
    @catch_unhandled_exceptions() 
    def test_call_nonblock(self):
        # Make calls on new threads
        call_nonblock(self.callable_that_succeeds, 'blue', 'green', 1, 2, a='yes', b=[3,4],
                      callback=self.callback_for_success)
        call_nonblock(self.callable_that_fails, 'blue', 'green', 1, 2, a='yes', b=[3,4],
                      callback=self.callback_for_failure)

        wait_for_nonblock_threads() # Wait for all threads to return, just so we know the event queue will
                                    # have callbacks in it

        # Process all penting events in Qt event queue, which includes callback calls.
        TEST_APP.processEvents()
        # print("Main finished")
    
    def callable_that_succeeds(self, *args, **kwargs):
        # print("Receiving thread: ", QThread.currentThread().objectName())
        # print("Received args:    ", args)
        # print("Received kwargs:  ", kwargs, "\n")
        self.assertNotEqual(QThread.currentThread().objectName(), self.MAIN_THREAD_NAME)
        self.assertEqual(args, ('blue', 'green', 1, 2))
        self.assertEqual(kwargs, {'a': 'yes', 'b': [3, 4]})
        return ('some', 'results')

    def callable_that_fails(self, *args, **kwargs):
        # print("Receiving thread: ", QThread.currentThread().objectName())
        # print("Received args:    ", args)
        # print("Received kwargs:  ", kwargs, "\n")
        self.assertNotEqual(QThread.currentThread().objectName(), self.MAIN_THREAD_NAME)
        self.assertEqual(args, ('blue', 'green', 1, 2))
        self.assertEqual(kwargs, {'a': 'yes', 'b': [3, 4]})

        # Create an exception
        a = 1/0
        return ('some', 'results') # We should never get to here

    def callback_for_success(self, future_result):
        # print("Callback thread:    ", QThread.currentThread().objectName())
        # print("Result in callback: ", future_result.value)
        # print("Error in callback:  ", future_result.error, "\n")
        self.assertEqual(QThread.currentThread().objectName(), self.MAIN_THREAD_NAME)
        self.assertEqual(future_result.value, ('some', 'results'))
        self.assertIs(future_result.error, None)

    def callback_for_failure(self, future_result):
        # print("Callback thread:    ", QThread.currentThread().objectName())
        # print("Result in callback: ", future_result.value)
        # print("Error in callback:  ", future_result.error, "\n")
        self.assertEqual(QThread.currentThread().objectName(), self.MAIN_THREAD_NAME)
        self.assertIs(future_result.value, None)
        self.assertIsInstance(future_result.error, ZeroDivisionError)

    def test_crossthread_wait(self):
        future_result = call_nonblock(self.crossthread_send)
        # print("Waiting for result\n")
        future_result.wait()
        # print("Received result is:", future_result.value)
        # print("is_set is: ", future_result.is_set)
        # print("error is:  ", future_result.error)
        self.assertEqual(future_result.value, [1,2,3,4,5])
        self.assertTrue(future_result.is_set)
        self.assertIsNone(future_result.error)

    def crossthread_send(self):
        time.sleep(1)
        # print("Returning result\n")
        return [1,2,3,4,5]
    
    def test_main_thread_calling_techniques(self):
        '''Tests our various ways of passing calls from a secondary thread to the
        main thread. 
        '''
        self.call_later_test_string = CALL_LATER_TEST_STRING
        app = multiscript.app()
        future_result = call_nonblock(self.runs_on_own_thread_and_calls_main_thread, app)
        app.exec()
        self.assertIsNone(future_result.value)
        self.assertEqual(self.call_later_test_string, CALL_LATER_TEST_STRING)

    def runs_on_own_thread_and_calls_main_thread(self, app):
        '''Should be run in its own thread by calling it with call_nonblock().
        
        Returns None if all the tests have passed, otherwise a string error message.
        (We don't use testing assertions here, because we want to return
        the result back to the method that called us.)

        Makes a series of calls to test our various ways of passing calls
        from a secondary thread to the main thread. Before returning, ends
        the app's event loop.
        '''
        try:
            # Fail if somehow we *are* on the main thread.
            if QThread.currentThread().objectName() == self.MAIN_THREAD_NAME:
                return "Didn't create a secondary thread"
            
            # Fail if should_run_on_main_thread() failed
            future_result = call_main_thread(self.should_run_on_main_thread)
            if future_result.wait() != self.MAIN_THREAD_NAME:
                return "call_main_thread didn't work!"

            # Test using wait_main_thread instead
            future_result = wait_main_thread(self.should_run_on_main_thread)
            if future_result.value != self.MAIN_THREAD_NAME:
                return "wait_main_thread didn't work!"

            # Test exceptions raised during main thread call
            future_result = wait_main_thread(self.raise_exception_during_main_thread_call)
            if future_result.value is not None or \
               not isinstance(future_result.error, ConcurrencyTestException):
                return "wait_main_thread didn't detect extension"

            # Test using main_thread decorator
            decorated_result = self.decorated_for_main_thread()
            if not isinstance(decorated_result, FutureResult):
                return "main_thread decorator seems missing!"
            if decorated_result.wait() != self.MAIN_THREAD_NAME:
                return "main_thread decorated didn't work!"

            # Test call_main_thread_later()
            change_future_result = wait_main_thread(self.change_string)
            reset_future_result = change_future_result.value
            # Make sure the event loop keeps running long enough for the reset to occur
            reset_future_result.wait()

            # By making it to this point, we're passing so far.
            return None
        except Exception as e:
            return f"Exception raised: {e}"
        finally:
            # End the event loop
            app.quit()

    def should_run_on_main_thread(self):
        '''Returns name of thread the method executes on.
        '''
        return QThread.currentThread().objectName()

    @main_thread
    def decorated_for_main_thread(self):
        '''Returns name of thread the method executes on.
        '''
        return QThread.currentThread().objectName()
    
    def change_string(self):
        '''Expected to run on main thread.'''
        # By using call_main_thread_later to call reset_string(), we expect the string
        # to actually be reset *after* the value is changed below.
        reset_future_result = call_main_thread_later(self.reset_string)
        self.call_later_test_string = "Changed value!"
        return reset_future_result

    def reset_string(self):
        self.call_later_test_string = CALL_LATER_TEST_STRING
    
    def raise_exception_during_main_thread_call(self):
        raise ConcurrencyTestException("Exception on main thread!")


class ConcurrencyTestException(Exception):
    pass
