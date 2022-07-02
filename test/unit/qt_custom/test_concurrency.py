import unittest
import time

from PySide6.QtCore import QThread
from PySide6.QtGui import QWindow

from multiscript.qt_custom.concurrency import *
from multiscript.util.exception_catcher import catch_unhandled_exceptions
from test.application import TEST_APP


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
