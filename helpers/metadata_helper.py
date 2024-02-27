from datetime import datetime, date
from enum import Enum
import json
import os
from file_helper import create_directory_excluding_filename
from date_helper import convert_date_to_yyyy_mm_dd, convert_date_to_yyyy_mm_dd_hh_mm_ss

DEFAULT_METADATA_FILE_PATH = "./metadata/metadata.json"

class JobStatus(Enum):
    Default = 0
    InProgress = 1
    Success = 2
    Failed = 3

    def __str__(self) -> str:
        return str(self.value)

class DataFrequency(Enum):
    Default = 0
    Daily = 1
    Weekly = 2
    Monthly = 3
    Yearly = 4

    def __str__(self) -> str:
        return str(self.value)

class DataModule(Enum):
    Default = 0
    Age = 1
    Gender = 2
    LandingPage = 3

    def __str__(self) -> str:
        return str(self.value)

def new_metadata(data_frequency: DataFrequency,
                module: DataModule,
                last_data_extraction_date: date | datetime,
                status: JobStatus,
                failure_reason = ''):
    return {
        'data_frequency': str(data_frequency),
        'module': str(module),
        'last_data_extraction_date': convert_date_to_yyyy_mm_dd(last_data_extraction_date),
        'status': str(status),
        'failure_reason': failure_reason,
        'created_date': convert_date_to_yyyy_mm_dd_hh_mm_ss(datetime.now()),
        'created_date_utc': convert_date_to_yyyy_mm_dd_hh_mm_ss(datetime.utcnow())
    }

def load_all_metadata(file_path = DEFAULT_METADATA_FILE_PATH):
    metadata = []

    if not os.path.exists(file_path):
        return metadata

    with open(file_path, 'r') as f:
        metadata = f.read()

    if metadata is None or metadata == "":
        return []
    
    return json.loads(metadata)

def load_metadata(module, file_path = DEFAULT_METADATA_FILE_PATH):
    all_metadata = load_all_metadata(file_path)
    metadata = [m for m in all_metadata if m['module'] == module]
    if len(metadata) > 0:
        return metadata[0]
    
    return None

def save_metadata(data_frequency: DataFrequency,
                  module: DataModule,
                  last_date_extraction_date: date | datetime,
                  status : JobStatus,
                  failure_reason = '',
                  file_path = DEFAULT_METADATA_FILE_PATH):
    create_directory_excluding_filename(file_path)
    all_metadata = load_all_metadata(file_path)
    other_metadata = [m for m in all_metadata if m['module'] != module]
    metadata = new_metadata(data_frequency, module, last_date_extraction_date, status, failure_reason)
    other_metadata.append(metadata)
    new_metadatas_json = json.dumps(other_metadata)

    with open(file_path, 'w') as f:
        f.write(new_metadatas_json)
    

# save_metadata(DataFrequency.Daily, DataModule.Age, datetime.now(), JobStatus.InProgress)
# save_metadata("./metadata/metadata.json", 'gender', datetime.now(), 'Failed')
# save_metadata("./metadata/metadata.json", 'landing_page', datetime.now(), 'Success')