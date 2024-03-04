"""File helpers"""
import os
import shutil
from datetime import date
import pandas as pd

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

def get_data_path_in_current_directory(data_frequency_name, module_name, date_obj: date):
    """get data path in current directory"""
    return get_data_path(".", data_frequency_name, module_name, date_obj)

def get_data_path(root_dir, data_frequency_name: str, module_name:str, date_obj: date):
    """get data path
    Note: cannot have DataFrequency object because of circular dependency
    """
    month_str = str(date_obj.month).zfill(2)
    day_str = str(date_obj.day).zfill(2)
    data_dir_path = os.path.join(root_dir,
                                 "data",
                                 data_frequency_name,
                                 module_name,
                                 str(date_obj.year),
                                 month_str,
                                 day_str)
    file_name = f'{date_obj.year}_{month_str}_{day_str}.csv'
    full_path = os.path.join(data_dir_path, file_name)
    return full_path

def remove_directory(file_path):
    """removes directory with file contents"""
    dir_name = os.path.dirname(file_path)
    shutil.rmtree(dir_name)
