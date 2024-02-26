import sys
import os
import unittest
from datetime import date
# insert current path to system path, so that we can import python file
sys.path.insert(1, os.getcwd())

import helpers.date_helper as dh

class TestDateHelper(unittest.TestCase):
    def test_convert_date_to_yyyy_mm_dd_should_return_response_for_valid_date(self):
        date_str = dh.convert_date_to_yyyy_mm_dd(date(2024,2,25))
        self.assertEqual("2024-02-25", date_str)

    def test_convert_date_to_yyyy_mm_dd_should_throw_error_in_empty_string_input(self):
        self.assertRaises(ValueError, dh.convert_date_to_yyyy_mm_dd, "")

    def test_convert_date_to_yyyy_mm_dd_should_throw_error_in_None_input(self):
        self.assertRaises(ValueError, dh.convert_date_to_yyyy_mm_dd, None)
  
    def test_convert_date_to_yyyy_mm_dd_should_throw_error_in_invalid_input(self):
        self.assertRaises(ValueError, dh.convert_date_to_yyyy_mm_dd, "2024-02-25")
        
if __name__ == '__main__':
    unittest.main()
