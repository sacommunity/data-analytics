"""Settings helper to retrieve settings data from json file"""
import json
from helpers.string_helper import is_null_or_whitespace

DEFAULT_APP_SETTINGS_FILE_PATH = './settings/app_settings.json'

def get_settings(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    """Get all settings from settings json"""
    file_data = ''
    with open(file_path, 'r', encoding="UTF-8") as f:
        file_data = f.read()

    if file_data is None or file_data == '':
        return None

    return json.loads(file_data)

def get_settings_for_a_module(module, file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    """Get settings related to particular module"""
    settings = get_settings(file_path)
    return settings.get(module)

def get_google_analytics_settings(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    """Get GoogleAnalytics section"""
    return get_settings_for_a_module('GoogleAnalytics', file_path)

def get_google_analytics_view_id_from_settings(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    """Get ViewId for google analytics"""
    google_analytics_settings = get_google_analytics_settings(file_path)
    view_id = google_analytics_settings.get('ViewId')
    if is_null_or_whitespace(view_id):
        raise ValueError("ViewId not found in app_settings.json")

    return view_id

def get_file_storage_settings(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    """Get FileStorage section"""
    return get_settings_for_a_module('FileStorage', file_path)

def get_file_storage_root_folder_from_settings(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    """Get RootDir"""
    file_storage_settings = get_file_storage_settings(file_path)
    root_dir = file_storage_settings.get('RootDir')
    if is_null_or_whitespace(root_dir):
        raise ValueError("RootDir not found in app_settings.json")

    return root_dir

def get_global_configs(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    """Get GlobalConfig section"""
    return get_settings_for_a_module('GlobalConfig', file_path)

def get_maximum_concurrent_requests(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    """Get value for MaximumConcurrentRequests"""
    global_settings = get_global_configs(file_path)
    max_concurrent_requests = global_settings.get('MaximumConcurrentRequests')
    return max_concurrent_requests if max_concurrent_requests is not None else 3

def get_default_timeout_in_seconds(file_path = DEFAULT_APP_SETTINGS_FILE_PATH):
    """Get value for DefaultTimeoutInSeconds"""
    global_settings = get_global_configs(file_path)
    default_timeout_in_seconds = global_settings.get('DefaultTimeoutInSeconds')
    return default_timeout_in_seconds if default_timeout_in_seconds is not None else 300

# print(get_google_analytics_settings())
