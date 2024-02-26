from datetime import datetime
import json
import os
from file_helper import create_directory_excluding_filename
from date_helper import convert_date_to_yyyy_mm_dd, convert_date_to_yyyy_mm_dd_hh_mm_ss

def new_metadata(module, last_data_extraction_date, status, failure_reason = ''):
    return {
        'module': module,
        'last_data_extraction_date': convert_date_to_yyyy_mm_dd(last_data_extraction_date),
        'status': status,
        'failure_reason': failure_reason,
        'created_date': convert_date_to_yyyy_mm_dd_hh_mm_ss(datetime.now()),
        'created_date_utc': convert_date_to_yyyy_mm_dd_hh_mm_ss(datetime.utcnow())
    }

def load_all_metadata(file_path):
    metadata = []

    if not os.path.exists(file_path):
        return metadata

    with open(file_path, 'r') as f:
        metadata = f.read()

    if metadata is None or metadata == "":
        return []
    
    return json.loads(metadata)

def load_metadata(module, file_path):
    all_metadata = load_all_metadata(file_path)
    metadata = [m for m in all_metadata if m['module'] == module]
    if len(metadata) > 0:
        return metadata[0]
    
    return None

def save_metadata(file_path, module, last_date_extraction_date, status, failure_reason = ''):
    create_directory_excluding_filename(file_path)
    all_metadata = load_all_metadata(file_path)
    other_metadata = [m for m in all_metadata if m['module'] != module]
    print('other metadata ', other_metadata)
    metadata = new_metadata(module, last_date_extraction_date, status, failure_reason)
    other_metadata.append(metadata)
    print('new metadatas ', other_metadata)
    new_metadatas_json = json.dumps(other_metadata)
    print('json ', new_metadatas_json)

    with open(file_path, 'w') as f:
        f.write(new_metadatas_json)
    

# save_metadata("./metadata/metadata.json", 'age', datetime.now(), 'Success')
# save_metadata("./metadata/metadata.json", 'gender', datetime.now(), 'Failed')
# save_metadata("./metadata/metadata.json", 'landing_page', datetime.now(), 'Success')