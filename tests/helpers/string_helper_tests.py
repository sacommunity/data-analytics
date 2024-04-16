"""Tests methods for string helper methods"""
import sys
import os
import unittest
# insert current path to system path, so that we can import python file
sys.path.insert(1, os.getcwd())
# disable wrong import position,
# because pylint asks it to position at top, but it is dependent of the sys.path
#pylint: disable=wrong-import-position
from helpers.string_helper import StringHelper
#pylint: enable=wrong-import-position

class TestStringHelper(unittest.TestCase):
    """Tests for String Helper methods"""
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.string_helper = StringHelper()

    def test_is_null_or_whitespace_should_return_true_for_null_input(self):
        """Null value check"""
        # Check Null
        self.assertTrue(self.string_helper.is_null_or_whitespace(None))

    def test_is_null_or_whitespace_should_return_true_for_empty_input(self):
        """Empty content check"""
        # check empty
        self.assertTrue(self.string_helper.is_null_or_whitespace(""))

    def test_is_null_or_whitespace_should_return_true_for_single_whitespace_input(self):
        """ Single white space is considered empty"""
        # check white space
        self.assertTrue(self.string_helper.is_null_or_whitespace(" "))

    def test_is_null_or_whitespace_should_return_true_for_multiple_whitespaces_input(self):
        """ Multiple white space is also considered empty """
        # check tab
        self.assertTrue(self.string_helper.is_null_or_whitespace("      "))

    def test_is_null_or_whitespace_should_return_false_for_nonempty_input(self):
        """is_null_of_whitespace should return False if the input value is not empty"""
        # check non emtpy string
        self.assertFalse(self.string_helper.is_null_or_whitespace("something"))

if __name__ == '__main__':
    unittest.main()
