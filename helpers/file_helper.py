import os
import pandas as pd
import shutil

def create_directory(dir_path: str):
    """create directory"""
    os.makedirs(dir_path, exist_ok=True)

def create_directory_excluding_filename(file_path):
    """create directory excluding filename"""
    create_directory(os.path.dirname(file_path))

def save_list_to_csv(data : list, file_path):
    """save list of data as csv"""
    create_directory(os.path.dirname(file_path))
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

def get_data_path_in_current_directory(data_frequency, module, year, month, day):
    """get data path in current directory"""
    return get_data_path(".", data_frequency, module, year, month, day)

def get_data_path(root_dir, data_frequency, module, year, month, day):
    """get data path"""
    month_str = str(month).zfill(2)
    day_str = str(day).zfill(2)
    data_dir_path = os.path.join(root_dir, "data", data_frequency, module, str(year), month_str, day_str)
    file_name = f'{year}_{month_str}_{day_str}.csv'
    full_path = os.path.join(data_dir_path, file_name)
    return full_path

def remove_file(file_path):
    """removes file with directory"""
    shutil.rmtree(file_path)