"""Google Analytics API methods"""
from enum import Enum
import os
import sys
import logging
sys.path.insert(1, os.getcwd())

# pylint: disable=wrong-import-position
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pandas as pd

from helpers.string_helper import is_null_or_whitespace
from helpers.date_helper import convert_date_to_yyyy_mm_dd
from dtos.date_range_dto import DateRangeDto
# pylint: enable=wrong-import-position

ga_api_retrieval_log = logging.getLogger(__name__)


class GoogleAuthenticationMethod(Enum):
    """Authentication methods"""
    DEFAULT = 0
    OAUTH = 1
    SERVICE_ACCOUNT = 2


class PageDto():
    """request config page size and page token"""

    def __init__(self, page_size, page_token) -> None:
        self.page_size = page_size
        self.page_token = page_token

    def to_dict(self):
        """returns dictionary representation of dto"""
        return self.__dict__

    @classmethod
    def from_dict(cls, dict_obj):
        """creates new instance from dictionary"""
        return cls(**dict_obj)


class GoogleAnalyticsRequestConfig():
    """Request Config: dimensions and metrics"""

    def __init__(self, dimensions, metrics) -> None:
        self.dimensions = dimensions
        self.metrics = metrics

    def to_dict(self):
        """returns dictionary representation of dto"""
        return self.__dict__

    @classmethod
    def from_dict(cls, dict_obj):
        """creates new instance from dictionary"""
        return cls(**dict_obj)


class GoogleAnalyticsApiRetrieval():
    """Retrieve data from google analytics"""

    def __init__(self, google_authentication_method: GoogleAuthenticationMethod,
                 oauth_credentials_filepath: str = '',
                 oauth_token_filepath: str = '',
                 view_id: str = '') -> None:
        self.view_id = view_id
        self.google_authentication_method = google_authentication_method
        if google_authentication_method == GoogleAuthenticationMethod.OAUTH:
            if is_null_or_whitespace(oauth_credentials_filepath):
                raise ValueError("oauth credentials filepath is required")
            self.oauth_credentials_filepath = oauth_credentials_filepath

            if is_null_or_whitespace(oauth_token_filepath):
                raise ValueError("oauth token filepath is required")
            self.oauth_token_filepath = oauth_token_filepath

        self.scopes = ['https://www.googleapis.com/auth/analytics.readonly']
        self.creds = None

    def get_oauth_credentials(self):
        """get oauth credentials"""
        if os.path.exists(self.oauth_token_filepath):
            self.creds = Credentials.from_authorized_user_file(
                self.oauth_token_filepath, self.scopes)
            if not self.creds or not self.creds.valid:
                self.refresh_oauth_token()
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.oauth_credentials_filepath, self.scopes)
            self.creds = flow.run_local_server(port=0)
            with open(self.oauth_token_filepath, 'w', encoding='UTF-8') as token:
                token.write(self.creds.to_json())

    # REFRESH token doesnot work, need to debug it later
    def refresh_oauth_token(self):
        """refresh oauth token if expired"""
        if self.creds is None:
            self.get_oauth_credentials()
        elif self.creds.expired:
            self.creds.refresh(Request())
            with open(self.oauth_token_filepath, 'w', encoding='UTF-8') as token:
                token.write(self.creds.to_json())

    def extract_data_from_response(self, response, date_range: DateRangeDto):
        """fomat response received from google analytics"""

        results = []
        for report in response.get('reports'):
            column_header = report.get('columnHeader')
            # if total is zero, continue to another
            if int(report.get('data').get('totals')[0]['values'][0]) == 0:
                # print('continue for loop to next item')
                continue
            dimensions = column_header.get('dimensions')
            dimensions_len = len(dimensions)
            metric_header = column_header.get('metricHeader')
            metrics = metric_header.get('metricHeaderEntries')
            metrics_len = len(metrics)

            for row in report.get('data').get('rows'):
                result = {'start_date': date_range.start_date,
                          'end_date': date_range.end_date}
                for i in range(dimensions_len):
                    result[dimensions[i]] = row.get('dimensions')[i]

                for i in range(metrics_len):
                    result[metrics[i].get('name')] = row.get(
                        'metrics')[i].get('values')[0]

                results.append(result)

        return results

    def get_batch_data(self,
                       view_id: str,
                       request_config: GoogleAnalyticsRequestConfig,
                       date_range: DateRangeDto,
                       page_dto: PageDto):
        """get batch data"""
        self.refresh_oauth_token()
        analytics = build('analyticsreporting', 'v4', credentials=self.creds)

        metrics_list = [{'expression': 'ga:' + m}
                        for m in request_config.metrics]
        dimensions_list = [{'name': 'ga:' + d}
                           for d in request_config.dimensions]

        request_body = {
            'reportRequests': [
                {
                    'pageSize': page_dto.page_size,
                    'pageToken': page_dto.page_token,
                    'viewId': view_id,
                    'dateRanges': [
                        {
                            'startDate': convert_date_to_yyyy_mm_dd(date_range.start_date),
                            'endDate': convert_date_to_yyyy_mm_dd(date_range.end_date)
                        }],
                    'metrics': metrics_list,
                    'dimensions': dimensions_list,
                }
            ]
        }

        # pylint: disable=no-member
        return analytics.reports().batchGet(body=request_body).execute()
        # pylint: enable=no-member

    def get_data(self,
                 view_id: str,
                 request_config: GoogleAnalyticsRequestConfig,
                 date_range: DateRangeDto,
                 page_dto: PageDto):
        """get all data"""
        results = []
        page_token = page_dto.page_token

        while True:
            new_page_dto = PageDto(page_dto.page_size, page_token)
            response = self.get_batch_data(view_id=view_id,
                                           request_config=request_config,
                                           date_range=date_range,
                                           page_dto=new_page_dto)
            ga_api_retrieval_log.debug('request_config %s, date_range %s,\
                                        page_dto %s, response %s',
                                       request_config.to_dict(),
                                       date_range.to_dict(),
                                       page_dto.to_dict(),
                                       response)
            results.extend(self.extract_data_from_response(
                response, date_range))
            page_token = response['reports'][0].get('nextPageToken')

            total_rows = response.get('reports')[0].get('data').get('totals')[0]['values'][0]
            ga_api_retrieval_log.debug("Retrieved %s of %s ", len(results), total_rows)

            if page_token is None:
                ga_api_retrieval_log.debug("All data has been retrieved")
                break

        return results

    def get_sessions_by_gender(self, date_range: DateRangeDto, page: PageDto):
        """get session data by gender"""
        dimensions = ['customVarValue1', 'userGender']
        metrics = ["sessions"]
        data = self.get_data(view_id=self.view_id,
                             request_config=GoogleAnalyticsRequestConfig(
                                 dimensions, metrics),
                             date_range=date_range,
                             page_dto=page)
    
        # create dataframe
        data_df = pd.DataFrame(data)
        # rename columns
        data_df = data_df.rename(columns={
            'ga:customVarValue1':'dataset_id', 
            'ga:sessions': 'sessions',
            'ga:userGender': 'gender'
            })
        
        return self.convert_data_types(data_df)

    def get_sessions_by_landing_page(self, date_range: DateRangeDto, page: PageDto):
        """get session data with landing page"""
        dimensions = ['customVarValue1', 'landingPagePath',
                      'deviceCategory', 'sourceMedium']
        metrics = ["sessions"]
        data = self.get_data(view_id=self.view_id,
                             request_config=GoogleAnalyticsRequestConfig(
                                 dimensions, metrics),
                             date_range=date_range,
                             page_dto=page)
    
        # create dataframe
        data_df = pd.DataFrame(data)
        # rename columns
        data_df = data_df.rename(columns={
            'ga:customVarValue1':'dataset_id', 
            'ga:landingPagePath': 'landing_page', 
            'ga:deviceCategory': 'device_category', 
            'ga:sourceMedium':'source_medium', 
            'ga:sessions': 'sessions'
            })
        
        return self.convert_data_types(data_df)

    def get_sessions_by_age(self, date_range: DateRangeDto, page: PageDto):
        """get sessions data by age"""
        dimensions = ['customVarValue1', 'userAgeBracket']
        metrics = ["sessions"]
        data = self.get_data(view_id=self.view_id,
                             request_config=GoogleAnalyticsRequestConfig(
                                 dimensions, metrics),
                             date_range=date_range,
                             page_dto=page)
        
        # create dataframe
        data_df = pd.DataFrame(data)
        # rename columns
        data_df = data_df.rename(columns={
            'ga:customVarValue1':'dataset_id', 
            'ga:sessions': 'sessions',
            'ga:userAgeBracket': 'age_bracket'
            })
        
        return self.convert_data_types(data_df)
    
    def convert_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        # convert data types
        df['sessions'] = pd.to_numeric(df['sessions'])
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])

        return df
