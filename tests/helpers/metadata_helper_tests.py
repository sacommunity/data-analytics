"""Tests methods for string helper methods"""
import sys
import os
import unittest
from datetime import datetime, date, timedelta
# insert current path to system path, so that we can import python file
sys.path.insert(1, os.getcwd())
# disable wrong import position,
# because pylint asks it to position at top, but it is dependent of the sys.path
#pylint: disable=wrong-import-position
import helpers.metadata_helper as mh
#pylint: enable=wrong-import-position

class TestMetadataHelper(unittest.TestCase):
    """Tests for String Helper methods"""
    # def test_is_null_or_whitespace_should_return_true_for_null_input(self):
    #     """Null value check"""
    #     # Check Null
    #     self.assertTrue(sh.is_null_or_whitespace(None))

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.metadata_json_file_path = "./tmp/metadata.json"

    def setUp(self) -> None:
        print('setup called')
        return super().setUp()

    def tearDown(self) -> None:
        print("tear down called")
        return super().tearDown()
    
    def doCleanups(self) -> None:
        print("do cleanups called")
        return super().doCleanups()

    def test_save_metadata_should_save_in_file(self):
        """"""
        mh.save_metadata(data_frequency=mh.DataFrequency.DAILY,
                         module=mh.DataModule.AGE,
                         last_date_extraction_date=datetime.now(),
                         status=mh.JobStatus.IN_PROGRESS,
                         file_path="")

    # save_metadata(DataFrequency.Daily, DataModule.Age, datetime.now(), JobStatus.InProgress)

if __name__ == '__main__':
    unittest.main()
