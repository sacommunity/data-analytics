import json
from helpers.string_helper import is_null_or_whitespace

DEFAULT_APP_SETTINGS_FILE_PATH = './settings/app_settings.json'

def get_settings(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    file_data = ''
    with open(file_path, 'r') as f:
        file_data = f.read()

    if file_data is None or file_data == '':
        return None
    
    return json.loads(file_data)

def get_settings_for_a_module(module, file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    settings = get_settings(file_path)
    return settings.get(module)

def get_google_analytics_settings(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    return get_settings_for_a_module('GoogleAnalytics', file_path)

def get_google_analytics_view_id_from_settings(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    google_analytics_settings = get_google_analytics_settings(file_path)
    view_id = google_analytics_settings.get('ViewId')
    if is_null_or_whitespace(view_id):
        raise ValueError("ViewId not found in app_settings.json")

    return view_id

def get_file_storage_settings(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    return get_settings_for_a_module('FileStorage', file_path)

def get_file_storage_root_folder_from_settings(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    file_storage_settings = get_file_storage_settings(file_path)
    root_dir = file_storage_settings.get('RootDir')
    if is_null_or_whitespace(root_dir):
        raise ValueError("RootDir not found in app_settings.json")

    return root_dir

# print(get_google_analytics_settings())
