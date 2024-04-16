"""File helpers"""
import os
import shutil
from datetime import date
import pandas as pd

from helpers.enums import DataModule
from helpers.settings_helper import get_file_storage_root_folder_from_settings

def create_directory(dir_path: str):
    """create directory"""
    os.makedirs(dir_path, exist_ok=True)

def create_directory_excluding_filename(file_path):
    """create directory excluding filename"""
    create_directory(os.path.dirname(file_path))

def save_list_to_csv(data : list, file_path):
    """save list of data as csv"""
    create_directory(os.path.dirname(file_path))
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(file_path, index=False)

def get_data_path_in_current_directory(data_frequency_name, module_name, date_obj: date):
    """get data path in current directory"""
    return get_data_path(".", data_frequency_name, module_name, date_obj)

def get_file_name_based_on_date(date_obj: date):
    """get file name based on date"""
    month_str = str(date_obj.month).zfill(2)
    day_str = str(date_obj.day).zfill(2)
    return f'{date_obj.year}_{month_str}_{day_str}'

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

def save_df_to_csv(dataframe: pd.DataFrame, file_path: str):
    """save dataframe to csv"""
    create_directory_excluding_filename(file_path)
    dataframe.to_csv(file_path, index=False)

def get_run_file_path(run_id: str, module: DataModule):
    """get run file path"""
    file_name = f'{module.name.lower()}.csv'
    root_dir = get_file_storage_root_folder_from_settings()
    return os.path.join(root_dir, 'data', run_id, file_name)

def save_run_file_to_csv(dataframe: pd.DataFrame,
                       run_id: str,
                       module: DataModule):
    """save run file dataframe to csv"""
    file_path = get_run_file_path(run_id, module)
    save_df_to_csv(dataframe, file_path)

def read_run_file(run_id: str, module: DataModule):
    """read run file"""
    file_path = get_run_file_path(run_id, module)
    return pd.read_csv(file_path)
