"""Metadata helper module"""
from datetime import datetime, date, timedelta
from enum import Enum
import json
import os

# Comment these to run the methods from the current file as entry point
from helpers.file_helper import create_directory_excluding_filename
from helpers.date_helper import convert_date_to_yyyy_mm_dd, convert_date_to_yyyy_mm_dd_hh_mm_ss

# Uncomment these to run the methods from the current file as entry point
# from file_helper import create_directory_excluding_filename
# from date_helper import convert_date_to_yyyy_mm_dd, convert_date_to_yyyy_mm_dd_hh_mm_ss

DEFAULT_METADATA_FILE_PATH = "./metadata/metadata.json"


class JobStatus(Enum):
    """job status"""
    DEFAULT = 0
    IN_PROGRESS = 1
    SUCCESS = 2
    FAILED = 3


class DataFrequency(Enum):
    """data frequency in which data are transformed / aggregated"""
    DEFAULT = 0
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4


class DataModule(Enum):
    """Different data modules found in google analytics"""
    DEFAULT = 0
    AGE = 1
    GENDER = 2
    LANDING_PAGE = 3

# Python DTO: https://hackernoon.com/dto-in-python-an-explanation


class MetadataDto():
    """Data Transfer Object (DTO) for Metadata"""

    def __init__(self, **kwargs) -> None:
        self.data_frequency = kwargs.get("data_frequency")
        self.module = kwargs.get("module")
        self.last_data_extraction_date = kwargs.get(
            "last_data_extraction_date")
        self.job_status = kwargs.get("job_status")
        self.failure_reason = kwargs.get("failure_reason")
        self.created_date = kwargs.get("created_date")
        self.created_date_utc = kwargs.get("created_date_utc")

    def to_dict(self):
        """returns dictionary representation of the metadata dto"""
        return self.__dict__

    @classmethod
    def from_dict(cls, metadata_dict):
        """creates new instance of metadata dto from dictionary"""
        return cls(**metadata_dict)


def new_metadata(data_frequency: DataFrequency,
                 module: DataModule,
                 last_data_extraction_date: date | datetime,
                 status: JobStatus,
                 failure_reason=''):
    """creates new object for metadata"""
    return {
        'data_frequency': {
            "value": data_frequency.value,
            "name": data_frequency.name
        },
        "module": {
            "value": module.value,
            "name": module.name
        },
        'last_data_extraction_date': convert_date_to_yyyy_mm_dd(last_data_extraction_date),
        "job_status": {
            "value": status.value,
            "name": status.name
        },
        'failure_reason': failure_reason,
        "created_date": {
            "date_local": convert_date_to_yyyy_mm_dd_hh_mm_ss(datetime.now()),
            "date_utc": convert_date_to_yyyy_mm_dd_hh_mm_ss(datetime.utcnow())
        }
    }


def sort_metadatas(metadatas):
    """sort metadata first by data_frequency and then by module"""
    return sorted(metadatas,
                  key=lambda x: (x.get("data_frequency").get("name"),
                                 x.get("module").get("name")))


def load_all_metadata(file_path=DEFAULT_METADATA_FILE_PATH):
    """load all metadata"""
    metadata = []

    if not os.path.exists(file_path):
        return metadata

    with open(file_path, 'r', encoding='UTF-8') as f:
        metadata = f.read()

    if metadata is None or metadata == "":
        return []

    metadatas = json.loads(metadata)
    # sort
    return sort_metadatas(metadatas)


def load_metadata(data_frequency: DataFrequency,
                  module: DataModule,
                  file_path=DEFAULT_METADATA_FILE_PATH) -> MetadataDto:
    """Load metadata"""
    all_metadata = load_all_metadata(file_path)
    metadata = [m for m in all_metadata if m['module']['value'] ==
                module.value and m['data_frequency']['value'] == data_frequency.value]
    if len(metadata) > 0:
        return MetadataDto.from_dict(metadata[0])

    return None


def save_metadata(data_frequency: DataFrequency,
                  module: DataModule,
                  last_date_extraction_date: date | datetime,
                  status: JobStatus,
                  failure_reason='',
                  file_path=DEFAULT_METADATA_FILE_PATH):
    """Save metadata"""
    create_directory_excluding_filename(file_path)
    all_metadata = load_all_metadata(file_path)
    other_metadata = [m for m in all_metadata if not
                      (m['module'].get('value') == module.value and
                       m['data_frequency'].get('value') == data_frequency.value)]
    metadata = new_metadata(data_frequency,
                            module,
                            last_date_extraction_date,
                            status,
                            failure_reason)
    other_metadata.append(metadata)
    new_metadatas_json = json.dumps(sort_metadatas(other_metadata))

    with open(file_path, 'w', encoding='UTF-8') as f:
        f.write(new_metadatas_json)


def get_start_date(last_data_extraction_date: date | datetime, job_status: int):
    """if the last job was success, then return the next day, 
    else return the same day to repeat the proecss"""
    if job_status == JobStatus.SUCCESS:
        return last_data_extraction_date + timedelta(days=1)
    return last_data_extraction_date

# save_metadata(DataFrequency.Daily, DataModule.Age, datetime.now(), JobStatus.InProgress)
# save_metadata(DataFrequency.Weekly, DataModule.Age, datetime.now(), JobStatus.InProgress)
# save_metadata(DataFrequency.Monthly, DataModule.Age, datetime.now(), JobStatus.InProgress)
# save_metadata(DataFrequency.Yearly, DataModule.Age, datetime.now(), JobStatus.InProgress)

# save_metadata(DataFrequency.Daily, DataModule.Gender, datetime.now(), JobStatus.Failed)
# save_metadata(DataFrequency.Weekly, DataModule.Gender, datetime.now(), JobStatus.Success)
# save_metadata(DataFrequency.Monthly, DataModule.Gender, datetime.now(), JobStatus.InProgress)
# save_metadata(DataFrequency.Yearly, DataModule.Gender, datetime.now(), JobStatus.Failed)


# metadata = load_metadata(DataFrequency.Weekly, DataModule.Age)
# print('date ', metadata.last_data_extraction_date)
# print('date type ', type(metadata.last_data_extraction_date))
