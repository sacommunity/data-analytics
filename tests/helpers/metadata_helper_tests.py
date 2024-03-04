"""Tests methods for string helper methods"""
import sys
import os
import unittest
from datetime import datetime
# insert current path to system path, so that we can import python file
sys.path.insert(1, os.getcwd())
# disable wrong import position,
# because pylint asks it to position at top, but it is dependent of the sys.path
#pylint: disable=wrong-import-position
import helpers.metadata_helper as mh
import helpers.file_helper as fh
#pylint: enable=wrong-import-position

class TestMetadataHelper(unittest.TestCase):
    """Tests for String Helper methods"""
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.metadata_json_file_path = "./tmp/metadata.json"

    def tearDown(self) -> None:
        """delete the metadata.json file after each test run"""
        fh.remove_directory(self.metadata_json_file_path)
        return super().tearDown()

    def test_save_metadata_should_save_in_file(self):
        """save metadata and verify saved one"""
        data_frequency = mh.DataFrequency.DAILY
        module = mh.DataModule.AGE
        job_status = mh.JobStatus.IN_PROGRESS
        mh.save_metadata(job_config=mh.JobConfig(data_frequency, module),
                         last_date_extraction_date=datetime.now(),
                         status=job_status,
                         file_path=self.metadata_json_file_path)

        # load and verify
        metadata = mh.load_metadata(data_frequency,
                                    module=module,
                                    file_path=self.metadata_json_file_path)
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata.data_frequency.get('value'), data_frequency.value)
        self.assertEqual(metadata.module.get('value'), module.value)
        self.assertEqual(metadata.job_status.get('value'), job_status.value)


    def test_save_metadata_should_save_only_one_record_of_data_frequency_module_record(self):
        """(data_frequency, module) should be unique record. 
        So, only one record should exist for that combination"""
        data_frequency = mh.DataFrequency.DAILY
        module = mh.DataModule.AGE
        job_status = mh.JobStatus.IN_PROGRESS
        # First Save
        mh.save_metadata(job_config=mh.JobConfig(data_frequency, module),
                         last_date_extraction_date=datetime.now(),
                         status=job_status,
                         file_path=self.metadata_json_file_path)
        all_metadata = mh.load_all_metadata(file_path=self.metadata_json_file_path)
        self.assertEqual(len(all_metadata), 1)

        # Second Save
        mh.save_metadata(job_config=mh.JobConfig(data_frequency, module),
                         last_date_extraction_date=datetime.now(),
                         status=job_status,
                         file_path=self.metadata_json_file_path)
        all_metadata = mh.load_all_metadata(file_path=self.metadata_json_file_path)
        self.assertEqual(len(all_metadata), 1)

if __name__ == '__main__':
    unittest.main()
