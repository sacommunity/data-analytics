import os
import pandas as pd

def create_directory(dir_path: str):
    os.makedirs(dir_path, exist_ok=True)

def create_directory_excluding_filename(file_path):
    create_directory(os.path.dirname(file_path))

def save_list_to_csv(data : list, file_path):
    create_directory(os.path.dirname(file_path))
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
