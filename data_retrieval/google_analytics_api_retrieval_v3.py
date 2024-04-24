"""version 3 google api"""
import pandas as pd
from data_retrieval.google_analytics_api_retrieval import GoogleAnalyticsApiRetrieval
from dtos.google_analytics_filter_clause_dto import GoogleAnalyticsFilterClause
from dtos.google_analytics_request_config_dto import GoogleAnalyticsRequestConfig

class GoogleAnalyticsApiRetrievalV3(GoogleAnalyticsApiRetrieval):
    """google api version 3"""
    def get_sessions_by_gender(self,
                               filter_clause: GoogleAnalyticsFilterClause):
        """get session data by gender"""
        dimensions = ['customVarValue1', 'userGender']
        metrics = ["sessions"]
        data = self.get_data(request_config=GoogleAnalyticsRequestConfig(
            dimensions, metrics),
            filter_clause=filter_clause)

        # create dataframe
        data_df = pd.DataFrame(data)
        # rename columns
        data_df = data_df.rename(columns={
            'ga:customVarValue1': 'dataset_id',
            'ga:sessions': 'sessions',
            'ga:userGender': 'gender'
        })

        return self.convert_data_types(data_df)

    def get_sessions_by_landing_page(self,
                                     filter_clause: GoogleAnalyticsFilterClause):
        """get session data with landing page"""
        dimensions = ['customVarValue1', 'landingPagePath',
                      'deviceCategory', 'sourceMedium']
        metrics = ["sessions"]
        data = self.get_data(request_config=GoogleAnalyticsRequestConfig(
                             dimensions, metrics),
                             filter_clause=filter_clause)

        # create dataframe
        data_df = pd.DataFrame(data)
        # rename columns
        data_df = data_df.rename(columns={
            'ga:customVarValue1': 'dataset_id',
            'ga:landingPagePath': 'landing_page',
            'ga:deviceCategory': 'device_category',
            'ga:sourceMedium': 'source_medium',
            'ga:sessions': 'sessions'
        })

        return self.convert_data_types(data_df)

    def get_sessions_by_age(self,
                            filter_clause: GoogleAnalyticsFilterClause):
        """get sessions data by age"""
        dimensions = ['customVarValue1', 'userAgeBracket']
        metrics = ["sessions"]
        data = self.get_data(request_config=GoogleAnalyticsRequestConfig(
            dimensions, metrics),
            filter_clause=filter_clause)

        # create dataframe
        data_df = pd.DataFrame(data)
        # rename columns
        data_df = data_df.rename(columns={
            'ga:customVarValue1': 'dataset_id',
            'ga:sessions': 'sessions',
            'ga:userAgeBracket': 'age_bracket'
        })

        return self.convert_data_types(data_df)

    def get_page_views_and_sessions(self, filter_clause: GoogleAnalyticsFilterClause):
        """get page views"""
        dimensions = ['customVarValue1', 'customVarValue2', 'customVarValue3',
                      'customVarValue4', 'customVarValue5', 'landingPagePath']
        metrics = ["pageviews", "sessions"]
        data = self.get_data(request_config=GoogleAnalyticsRequestConfig(
                             dimensions, metrics),
                             filter_clause=filter_clause)

        data_df = pd.DataFrame(data)
        # rename columns
        data_df = data_df.rename(columns={
            'ga:customVarValue1': 'dataset_id',
            'ga:customVarValue2': 'post_code',
            'ga:customVarValue3': 'state',
            'ga:customVarValue4': 'subject',
            'ga:customVarValue5': 'org_type',
            'ga:sessions': 'sessions',
            'ga:landingPagePath': 'landing_page',
            'ga:pageviews': 'page_views'
        })
        return data_df
