import sys
import os
import unittest
# insert current path to system path, so that we can import python file
sys.path.insert(1, os.getcwd())

import helpers.string_helper as sh

class TestStringHelper(unittest.TestCase):
    def test_is_null_or_whitespace_should_return_true_for_null_input(self):
        # Check Null
        self.assertTrue(sh.is_null_or_whitespace(None))

    def test_is_null_or_whitespace_should_return_true_for_empty_input(self):
        # check empty
        self.assertTrue(sh.is_null_or_whitespace(""))
        
    def test_is_null_or_whitespace_should_return_true_for_single_whitespace_input(self):
        # check white space
        self.assertTrue(sh.is_null_or_whitespace(" "))

    def test_is_null_or_whitespace_should_return_true_for_multiple_whitespaces_input(self):
        # check tab
        self.assertTrue(sh.is_null_or_whitespace("      "))

    def test_is_null_or_whitespace_should_return_false_for_notempty_input(self):
        # check non emtpy string
        self.assertFalse(sh.is_null_or_whitespace("something"))

if __name__ == '__main__':
    unittest.main()

