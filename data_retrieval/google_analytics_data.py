"""Retrieve and save google analytics data"""
import sys
import os
sys.path.insert(1, os.getcwd())
print(os.getcwd())

# pylint: disable=wrong-import-position
import uuid
import logging
import pandas as pd
from data_retrieval.google_analytics_api_retrieval import GoogleAnalyticsFilterClause,\
    GoogleAnalyticsApiRetrieval, GoogleAuthenticationMethod, PageDto
from helpers.file_helper import create_directory_excluding_filename
from helpers.settings_helper import get_google_analytics_view_id_from_settings,\
    get_file_storage_root_folder_from_settings
# pylint: enable=wrong-import-position

class GoogleAnalyticsData():
    """google analytics data"""
    def __init__(self, oauth_credentials_filepath: str, oauth_token_filepath: str) -> None:
        self.ga_data_log = logging.getLogger(__name__)
        self.oauth_credentials_filepath = oauth_credentials_filepath
        self.oauth_token_filepath = oauth_token_filepath

    def save_df_to_csv(self, dataframe: pd.DataFrame,
                       root_dir: str,
                       run_id: str,
                       module: str):
        """save dataframe to csv"""
        file_name = f'{module}.csv'
        file_path = os.path.join(root_dir, 'data', run_id, file_name)
        create_directory_excluding_filename(file_path)
        dataframe.to_csv(file_path, index=False)

    def group_data(self, dataframe: pd.DataFrame,
                   select_columns: list[str],
                   grp_columns: list[str]) -> pd.DataFrame:
        """group data"""
        df_s = dataframe[select_columns]
        df_grp = df_s.groupby(by=grp_columns, as_index=False).sum()
        return df_grp

    def filter_data_by_dataset_id(self, dataframe: pd.DataFrame, data_set_id: str):
        """filter data by dataset id"""
        return dataframe[dataframe['dataset_id'] == data_set_id]

    def save_data(self, filter_clause: GoogleAnalyticsFilterClause):
        """save data: device category, source/medium, landing page, age, gender"""
        root_dir = get_file_storage_root_folder_from_settings()
        self.ga_data_log.info('root_dir to store data is %s', root_dir)
        run_id = str(uuid.uuid4())
        self.ga_data_log.info('Run id %s', run_id)

        google_analytics_api = GoogleAnalyticsApiRetrieval(
            google_authentication_method=GoogleAuthenticationMethod.OAUTH,
            oauth_credentials_filepath=self.oauth_credentials_filepath,
            oauth_token_filepath=self.oauth_token_filepath,
            view_id=get_google_analytics_view_id_from_settings())

        # 1, 2, 3. Data for device category, source medium and landing page
        self.ga_data_log.info('Getting data for landing page')
        data_df = google_analytics_api.get_sessions_by_landing_page(filter_clause)

        # 1 device category
        device_category_df = self.group_data(data_df, ["dataset_id", "device_category","sessions"],
                                             ["dataset_id", "device_category"])
        self.save_df_to_csv(device_category_df, root_dir, run_id, 'device_category')

        # 2 source medium
        source_medium_df = self.group_data(data_df, ["dataset_id", "source_medium","sessions"],
                                           ["dataset_id", "source_medium"])
        self.save_df_to_csv(source_medium_df, root_dir, run_id, 'source_medium')

        # 3 landing page
        landing_page_df = self.group_data(data_df, ["dataset_id", "landing_page","sessions"],
                                          ["dataset_id", "landing_page"])
        self.save_df_to_csv(landing_page_df, root_dir, run_id, 'landing_page')

        # 4 Age
        self.ga_data_log.info("Getting age data")
        filter_clause.set_page_dto(PageDto(10000, None))
        age_df = google_analytics_api.get_sessions_by_age(filter_clause)
        self.save_df_to_csv(age_df, root_dir, run_id, 'age')

        # 5 gender
        self.ga_data_log.info("Getting gender data")
        filter_clause.set_page_dto(PageDto(10000, None))
        gender_df = google_analytics_api.get_sessions_by_gender(filter_clause)
        self.save_df_to_csv(gender_df, root_dir, run_id, 'gender')

        return run_id
