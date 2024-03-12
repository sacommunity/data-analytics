"""data transformations"""
import pandas as pd
import os
import math

# google analytics data cleanup
class GoogleAnalyticsDataProcessing():
    def __init__(self, council_name, fiscal_year) -> None:
        self.suffixes_to_remove = ["?fbclid=", "+&", "?_x_tr_", "?back="]
        self.search_cache_identifier = "/search?q=cache:"
        self.sacommunity_url = "https://sacommunity.org"
        self.council_name = council_name
        self.fiscal_year = fiscal_year
        self.data_root_folder = './data'
        self.google_analytics_landing_page_df = None
        self.sa_community_data_gov_au_export_df = None

    def get_data_folder_path(self) -> str:
        return os.path.join(self.data_root_folder, self.council_name, self.fiscal_year)

    def read_google_analytics_landing_page_data(self, file_name: str) -> pd.DataFrame:
        full_file_name = os.path.join(self.get_data_folder_path(), file_name)
        self.google_analytics_landing_page_df = pd.read_excel(full_file_name, sheet_name='Dataset1')
        return self.google_analytics_landing_page_df

    def read_sacommunity_data_gov_au_export(self, file_name: str) -> pd.DataFrame:
        full_file_name = os.path.join(self.get_data_folder_path(), file_name)
        self.sa_community_data_gov_au_export_df = pd.read_csv(full_file_name)
        return self.sa_community_data_gov_au_export_df

    def save_processed_data(self, data_df : pd.DataFrame, file_name: str):
        full_file_name = os.path.join(self.get_data_folder_path(), file_name)
        data_df.to_csv(full_file_name, index=False)

    def clean_landing_page(self, text: str) -> str:
        if self.search_cache_identifier in text:
            text = text[text.index(self.sacommunity_url):].replace(self.sacommunity_url, "")

        for suffix_to_remove in self.suffixes_to_remove:
            if suffix_to_remove in text:
                text = text[:text.index(suffix_to_remove)]

        # remove underscore
        text = text.replace("_", " ")
        # remove /org/
        text = text.replace("/org/", "")

        return text.strip()

    def get_organization_id(self, text: str) -> str:
        if "-" in text:
            return int(text[:text.index("-")])
        else:
            return None
    
    def get_organization_name(self, text: str) -> str:
        if "-" in text:
            return text[text.index("-") + 1:]
        else:
            return None
        
    def get_sessions_by_organization(self, df_ga_orig: pd.DataFrame) -> pd.DataFrame:
        df_ga = df_ga_orig.dropna().copy()
        df_ga['organization_id_name'] = df_ga['Landing Page'].apply(self.clean_landing_page)
        df_ga['organization_id'] = df_ga['organization_id_name'].apply(self.get_organization_id)
        df_ga['organization_name'] = df_ga['organization_id_name'].apply(self.get_organization_name)
        return df_ga[["Landing Page", "organization_id_name", "organization_id", "organization_name", "Sessions"]]
    
    def group_sessions_by_organization(self, google_analytics_cleaned_df) -> pd.DataFrame:
        return google_analytics_cleaned_df.groupby(by=['organization_id']).sum("Sessions")

    def process_data(self, google_analytics_sessions_data_df, sa_community_df) -> pd.DataFrame:
        results = []
        for _, row in google_analytics_sessions_data_df.iterrows():
            org_id_str = row["organization_id"]
            if math.isnan(org_id_str):
                print('org id is invalid, so skip it ', org_id_str)
                continue
            org_id = 0
            if org_id_str is not None:
                org_id = int(org_id_str)
            
            session_count = row["Sessions"]
            
            # organization name from sa-community file
            org_names_sa_community = sa_community_df[sa_community_df['ID_19'] == org_id]["Org_name"].values
            organization_name_sa_community = ''
            is_record_available_in_sacommunity_db = False
            if len(org_names_sa_community) > 0:
                organization_name_sa_community = org_names_sa_community[0]
                is_record_available_in_sacommunity_db = True
        
            # organization name from google analytics file
            org_names_google = google_analytics_sessions_data_df[google_analytics_sessions_data_df["organization_id"] == org_id]["organization_name"].values
            # print('org_names_google ', org_names_google)
            organization_name_google = ''
            if len(org_names_google) > 0:
                organization_name_google = org_names_google[0]

            # print('org_names_google ', org_names_google)
            landing_page = self.sacommunity_url + google_analytics_sessions_data_df[google_analytics_sessions_data_df["organization_id"] == org_id]["Landing Page"].values[0]
            results.append({
                'org_id': org_id,
                'landing_page': landing_page,
                'sessions_count': session_count,
                'organization_name_sa_community': organization_name_sa_community,
                'organization_name_google': organization_name_google,
                'is_record_available_in_sacommunity_db': is_record_available_in_sacommunity_db,
            })

        return pd.DataFrame(results)

# test texts
# google_analytics_processing = GoogleAnalyticsDataProcessing()
# inputs = [
#     "/org/196236-Dave's_Angels_Playgroup?fbclid=IwAR05WAQ0z5mwY7v1UEVmkDITFg7sDh8pcD8taJ3oGH4336EpkNZeP81BIKc",
#     "/search?q=cache:UTs_a-1ZNgEJ:https://sacommunity.org/org/196341-Neighbourhood_Watch_-_Linden_Park_249+&cd=63&hl=en&ct=clnk&gl=bj",
#     "/org/201669-Gifted_&_Talented_Children's_Association_of_SA_Inc.?_x_tr_sl=en&_x_tr_tl=th&_x_tr_hl=th&_x_tr_pto=sc",
#     "/org/201830-Aged_Rights_Advocacy_Service_Inc.?back=https://www.google.com/search?client=safari&as_qdr=all&as_occt=any&safe=active&as_q=Age+advocate+for+South+Australia&channel=aplab&source=a-app1&hl=en",
#     "/org/201950-SA_Ambulance_Service?_x_tr_sl=en&_x_tr_tl=fr&_x_tr_hl=fr&_x_tr_pto=nui,sc"
# ]

# for input in inputs:
#     print(google_analytics_processing.clean_landing_page(input))

