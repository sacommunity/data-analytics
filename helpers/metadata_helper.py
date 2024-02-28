from datetime import datetime, date, timedelta
from enum import Enum
import json
import os

# Comment these to run the methods from the current file as entry point
# from helpers.file_helper import create_directory_excluding_filename
# from helpers.date_helper import convert_date_to_yyyy_mm_dd, convert_date_to_yyyy_mm_dd_hh_mm_ss

# Uncomment these to run the methods from the current file as entry point
from file_helper import create_directory_excluding_filename
from date_helper import convert_date_to_yyyy_mm_dd, convert_date_to_yyyy_mm_dd_hh_mm_ss

DEFAULT_METADATA_FILE_PATH = "./metadata/metadata.json"
class JobStatus(Enum):
    Default = 0
    InProgress = 1
    Success = 2
    Failed = 3

class DataFrequency(Enum):
    Default = 0
    Daily = 1
    Weekly = 2
    Monthly = 3
    Yearly = 4

class DataModule(Enum):
    Default = 0
    Age = 1
    Gender = 2
    LandingPage = 3

# Python DTO: https://hackernoon.com/dto-in-python-an-explanation
class MetadataDto():
    def __init__(self, **kwargs) -> None:
        self.data_frequency = kwargs.get("data_frequency")
        self.data_frequency_name = kwargs.get("data_frequency_name")
        self.module = kwargs.get("module")
        self.module_name = kwargs.get("module_name")
        self.last_data_extraction_date = kwargs.get("last_data_extraction_date")
        self.status = kwargs.get("status")
        self.status_name = kwargs.get("status_name")
        self.failure_reason = kwargs.get("failure_reason")
        self.created_date = kwargs.get("created_date")
        self.created_date_utc = kwargs.get("created_date_utc")

    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, metadata_dict):
        return cls(**metadata_dict)

def new_metadata(data_frequency: DataFrequency,
                module: DataModule,
                last_data_extraction_date: date | datetime,
                status: JobStatus,
                failure_reason = ''):
    return {
        'data_frequency': data_frequency.value,
        'data_frequency_name': data_frequency.name,
        'module': module.value,
        'module_name': module.name,
        'last_data_extraction_date': convert_date_to_yyyy_mm_dd(last_data_extraction_date),
        'status': status.value,
        'status_name': status.name,
        'failure_reason': failure_reason,
        'created_date': convert_date_to_yyyy_mm_dd_hh_mm_ss(datetime.now()),
        'created_date_utc': convert_date_to_yyyy_mm_dd_hh_mm_ss(datetime.utcnow())
    }

def sort_metadatas(metadatas):
    return sorted(metadatas, key = lambda x: (x.get("data_frequency_name"), x.get("module_name")))

def load_all_metadata(file_path = DEFAULT_METADATA_FILE_PATH):
    metadata = []

    if not os.path.exists(file_path):
        return metadata

    with open(file_path, 'r') as f:
        metadata = f.read()

    if metadata is None or metadata == "":
        return []
    
    metadatas = json.loads(metadata)
    # sort
    return sort_metadatas(metadatas)
    

def load_metadata(data_frequency: DataFrequency, module: DataModule, file_path = DEFAULT_METADATA_FILE_PATH) -> MetadataDto:
    all_metadata = load_all_metadata(file_path)
    metadata = [m for m in all_metadata if m['module'] == module.value and m['data_frequency'] == data_frequency.value]
    if len(metadata) > 0:
        return MetadataDto.from_dict(metadata[0])
    
    return None

def save_metadata(data_frequency: DataFrequency,
                  module: DataModule,
                  last_date_extraction_date: date | datetime,
                  status : JobStatus,
                  failure_reason = '',
                  file_path = DEFAULT_METADATA_FILE_PATH):
    create_directory_excluding_filename(file_path)
    all_metadata = load_all_metadata(file_path)
    other_metadata = [m for m in all_metadata if not (m['module'] == module.value and m['data_frequency'] == data_frequency.value)]
    metadata = new_metadata(data_frequency, module, last_date_extraction_date, status, failure_reason)
    other_metadata.append(metadata)
    new_metadatas_json = json.dumps(sort_metadatas(other_metadata))

    with open(file_path, 'w') as f:
        f.write(new_metadatas_json)

def get_start_date(last_data_extraction_date: date | datetime, job_status: int):
    # if the last job was success, then return the next day, else return the same day to repeat the proecss
    if job_status == JobStatus.Success:
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


metadata = load_metadata(DataFrequency.Weekly, DataModule.Age)
print('date ', metadata.last_data_extraction_date)
print('date type ', type(metadata.last_data_extraction_date))
