import unittest

import multiscript

# Application singleton for unit tests
TEST_APP = multiscript.app()
TEST_APP.load_plugins()


class MultiscriptAppTestCase(unittest.TestCase):
    '''Test cases that need to use TEST_APP should inherit from MultiscriptAppTestCase. This allows us to add
    any necessary setup or teardown code we may need later on.
    '''
    pass

