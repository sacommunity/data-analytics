"""Retrieve and save google analytics data"""
import sys
import os
sys.path.insert(1, os.getcwd())
print(os.getcwd())
import uuid
import pandas as pd
import logging
from datetime import date

from data_retrieval.google_analytics_api_retrieval import PageDto
from dtos.date_range_dto import DateRangeDto
from helpers.file_helper import create_directory_excluding_filename
from helpers.settings_helper import get_google_analytics_view_id_from_settings, get_file_storage_root_folder_from_settings
from data_retrieval.google_analytics_api_retrieval import GoogleAnalyticsApiRetrieval, GoogleAuthenticationMethod

class GoogleAnalyticsData():
    def __init__(self, oauth_credentials_filepath: str, oauth_token_filepath: str) -> None:
        self.ga_data_log = logging.getLogger(__name__)
        self.oauth_credentials_filepath = oauth_credentials_filepath
        self.oauth_token_filepath = oauth_token_filepath

    def save_df_to_csv(self, df: pd.DataFrame, root_dir: str, run_id: str, module: str):
        file_name = f'{module}.csv'
        file_path = os.path.join(root_dir, 'data', run_id, file_name)
        create_directory_excluding_filename(file_path)
        df.to_csv(file_path, index=False)

    def group_data(self, df: pd.DataFrame, select_columns: list[str], grp_columns: list[str]) -> pd.DataFrame:
        df_s = df[select_columns]
        df_grp = df_s.groupby(by=grp_columns, as_index=False).sum()
        return df_grp

    def filter_data_by_dataset_id(self, df: pd.DataFrame, data_set_id: str):
        return df[df['dataset_id'] == data_set_id]

    def save_data(self, start_date: date, end_date: date):
        view_id = get_google_analytics_view_id_from_settings()
        self.ga_data_log.info('google analytics view id ', view_id)
        root_dir = get_file_storage_root_folder_from_settings()
        self.ga_data_log.info('root_dir to store data is ', root_dir)
        run_id = str(uuid.uuid4())
        self.ga_data_log.info('Run id ', run_id)

        ga = GoogleAnalyticsApiRetrieval(google_authentication_method=GoogleAuthenticationMethod.OAUTH,
                                         oauth_credentials_filepath=self.oauth_credentials_filepath,
                                         oauth_token_filepath=self.oauth_token_filepath,
                                         view_id=view_id)

        date_range_dto = DateRangeDto(start_date, end_date)
        page_dto = PageDto(10000, None)

        # 1, 2, 3. Data for device category, source medium and landing page
        self.ga_data_log.info('Getting data for landing page')
        data_df = ga.get_sessions_by_landing_page(date_range_dto, page_dto)

        # 1 device category
        device_category_df = self.group_data(data_df, ["dataset_id", "device_category","sessions"], ["dataset_id", "device_category"])
        self.save_df_to_csv(device_category_df, root_dir, run_id, 'device_category')

        # 2 source medium
        source_medium_df = self.group_data(data_df, ["dataset_id", "source_medium","sessions"], ["dataset_id", "source_medium"])
        self.save_df_to_csv(source_medium_df, root_dir, run_id, 'source_medium')

        # 3 landing page
        landing_page_df = self.group_data(data_df, ["dataset_id", "landing_page","sessions"], ["dataset_id", "landing_page"])
        self.save_df_to_csv(landing_page_df, root_dir, run_id, 'landing_page')

        # 4 Age
        self.ga_data_log.info("Getting age data")
        age_df = ga.get_sessions_by_age(date_range_dto, page_dto)
        self.save_df_to_csv(age_df, root_dir, run_id, 'age')

        # 5 gender
        self.ga_data_log.info("Getting gender data")
        gender_df = ga.get_sessions_by_gender(date_range_dto, page_dto)
        self.save_df_to_csv(gender_df, root_dir, run_id, 'gender')

        return run_id
