import json

def get_settings():
    settings_file_path = '../settings/app_settings.json'
    file_data = ''
    with open(settings_file_path, 'r') as f:
        file_data = f.read()

    if file_data is None or file_data == '':
        return None
    
    return json.loads(file_data)