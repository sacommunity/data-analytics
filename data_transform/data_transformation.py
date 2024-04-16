"""data transformations"""
import os
import pandas as pd
from helpers.settings_helper import SettingsHelper

# google analytics data cleanup
class GoogleAnalyticsDataProcessing():
    """data processing for google analytics data"""

    def __init__(self, council_name = "", fiscal_year = "") -> None:
        self.sacommunity_url = SettingsHelper().get_sacommunity_url()
        self.council_name = council_name
        self.fiscal_year = fiscal_year
        self.data_root_folder = './data'
        self.google_analytics_landing_page_df = None
        self.sa_community_data_gov_au_export_df = None

    def get_data_folder_path(self) -> str:
        """get data folder path"""
        return os.path.join(self.data_root_folder, self.council_name, self.fiscal_year)

    def read_google_analytics_landing_page_data(self, file_name: str) -> pd.DataFrame:
        """read google analytics landing page data"""
        full_file_name = os.path.join(self.get_data_folder_path(), file_name)
        self.google_analytics_landing_page_df = pd.read_excel(
            full_file_name, sheet_name='Dataset1')
        return self.google_analytics_landing_page_df

    def read_sacommunity_data_gov_au_export(self, file_name: str) -> pd.DataFrame:
        """read SA community data gov au export"""
        full_file_name = os.path.join(self.get_data_folder_path(), file_name)
        self.sa_community_data_gov_au_export_df = pd.read_csv(full_file_name)
        return self.sa_community_data_gov_au_export_df

    def save_processed_data(self, data_df: pd.DataFrame, file_name: str):
        """save processed data"""
        full_file_name = os.path.join(self.get_data_folder_path(), file_name)
        data_df.to_csv(full_file_name, index=False)


# test texts
# google_analytics_processing = GoogleAnalyticsDataProcessing()
# inputs = [
#     "/org/196236-Dave's_Angels_Playgroup?fbclid=IwAR05WAQ0z5mwY7v1UEVmkDITFg7sDh8pcD8taJ3o\
#         GH4336EpkNZeP81BIKc",
#     "/search?q=cache:UTs_a-1ZNgEJ:https://sacommunity.org/org/196341-Neighbourhood_Watch_-_\
#         Linden_Park_249+&cd=63&hl=en&ct=clnk&gl=bj",
#     "/org/201669-Gifted_&_Talented_Children's_Association_of_SA_Inc.?_x_tr_sl=en&_x_tr_tl\
#         =th&_x_tr_hl=th&_x_tr_pto=sc",
#     "/org/201830-Aged_Rights_Advocacy_Service_Inc.?\
#         back=https://www.google.com/search?client=safari&as_qdr=all&as_occt=any&safe=active&as_q=\
#             Age+advocate+for+South+Australia&channel=aplab&source=a-app1&hl=en",
#     "/org/201950-SA_Ambulance_Service?_x_tr_sl=en&_x_tr_tl=fr&_x_tr_hl=fr&_x_tr_pto=nui,sc"
# ]

# for input in inputs:
#     print(google_analytics_processing.clean_landing_page(input))
