import sys
import os
import unittest
from datetime import date, datetime
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

    def test_convert_yyyy_mm_dd_to_date(self):
        date_obj = dh.convert_yyyy_mm_dd_to_date("2024-02-29")
        self.assertIsInstance(date_obj, date)
        self.assertEqual(date_obj.year, 2024)
        self.assertEqual(date_obj.month, 2)
        self.assertEqual(date_obj.day, 29)

    def test_convert_yyyy_mm_dd_hh_mm_ss_to_date(self):
        datetime_obj = dh.convert_yyyy_mm_dd_hh_mm_ss_to_date("2024-02-29-00-53-20")
        self.assertIsInstance(datetime_obj, datetime)
        self.assertEqual(datetime_obj.year, 2024)
        self.assertEqual(datetime_obj.month, 2)
        self.assertEqual(datetime_obj.day, 29)
        self.assertEqual(datetime_obj.hour, 0)
        self.assertEqual(datetime_obj.minute, 53)
        self.assertEqual(datetime_obj.second, 20)
        
if __name__ == '__main__':
    unittest.main()
