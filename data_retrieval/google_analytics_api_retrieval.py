from enum import Enum
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import date
import os
import sys
# insert current path to system path, so that we can import python file
# pwd = os.getcwd()
# root_folder = 'data-analytics'
# da_index = pwd.index(root_folder)
# root_dir = os.path.join(pwd[0:da_index], root_folder)
# sys.path.insert(1, root_dir)
sys.path.insert(1, os.getcwd())
from helpers.date_helper import convert_date_to_yyyy_mm_dd
from helpers.string_helper import is_null_or_whitespace

class GoogleAuthenticationMethod(Enum):
    NoValue = 0
    OAuth = 1
    ServiceAccount = 2


class GoogleAnalyticsApiRetrieval():
    def __init__(self, google_authentication_method: GoogleAuthenticationMethod,
                 oauth_credentials_filepath: str = '',
                 oauth_token_filepath: str = '',
                 view_id: str = '') -> None:
        self.view_id = view_id
        self.google_authentication_method = google_authentication_method
        if google_authentication_method == GoogleAuthenticationMethod.OAuth:
            if is_null_or_whitespace(oauth_credentials_filepath):
                raise Exception("oauth credentials filepath is required")
            self.oauth_credentials_filepath = oauth_credentials_filepath

            if is_null_or_whitespace(oauth_token_filepath):
                raise Exception("oauth token filepath is required")
            self.oauth_token_filepath = oauth_token_filepath

        self.scopes = ['https://www.googleapis.com/auth/analytics.readonly']
        self.creds = None

    def get_oauth_credentials(self):
        if os.path.exists(self.oauth_token_filepath):
            self.creds = Credentials.from_authorized_user_file(
                self.oauth_token_filepath, self.scopes)
            if not self.creds or not self.creds.valid:
                self.refresh_oauth_token()
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.oauth_credentials_filepath, self.scopes)
            self.creds = flow.run_local_server(port=0)
            with open(self.oauth_token_filepath, 'w') as token:
                token.write(self.creds.to_json())

    def refresh_oauth_token(self):
        if self.creds is None:
            self.get_oauth_credentials()
        elif self.creds.expired:
            self.creds.refresh(Request())
            with open(self.oauth_token_filepath, 'w') as token:
                token.write(self.creds.to_json())

    def extract_data_from_response(self, response, start_date, end_date):
        reports = response.get('reports')
        if reports is None:
            return None

        results = []
        for report in reports:
            column_header = report.get('columnHeader')
            data = report.get('data')
            totals = data.get('totals')
            total_record = totals[0]['values'][0]
            if int(total_record) == 0:
                # print('continue for loop to next item')
                continue
            dimensions = column_header.get('dimensions')
            metric_header = column_header.get('metricHeader')
            metrics = metric_header.get('metricHeaderEntries')

            rows = data.get('rows')

            for row in rows:
                row_dimensions = row.get('dimensions')
                row_metrics = row.get('metrics')

                result = {'start_date': start_date, 'end_date': end_date}
                for i in range(len(dimensions)):
                    col_dimension = dimensions[i]
                    row_dimension = row_dimensions[i]

                    result[col_dimension] = row_dimension

                for i in range(len(metrics)):
                    col_metric = metrics[i]
                    row_metric = row_metrics[i]
                    row_metric_value = row_metric.get('values')

                    result[col_metric.get('name')] = row_metric_value[0]

                results.append(result)

        return results

    def get_batch_data(self, view_id: str, dimensions: list[str], start_date: date, end_date: date, metrics: list[str] = ['sessions'],
                 page_size = 1000,
                 page_token = None):
        self.refresh_oauth_token()
        analytics = build('analyticsreporting', 'v4', credentials=self.creds)

        metrics_list = [{'expression': 'ga:' + m} for m in metrics]
        dimensions_list = [{'name': 'ga:' + d} for d in dimensions]

        request_body = {
            'reportRequests': [
                {
                    'pageSize': page_size,
                    'pageToken': page_token,
                    'viewId': view_id,
                    'dateRanges': [{'startDate': convert_date_to_yyyy_mm_dd(start_date), 'endDate': convert_date_to_yyyy_mm_dd(end_date)}],
                    'metrics': metrics_list,
                    'dimensions': dimensions_list,

                }
            ]
        }

        return analytics.reports().batchGet(body=request_body).execute()
        

    def get_data(self, view_id: str, dimensions: list[str], start_date: date, end_date: date, metrics: list[str] = ['sessions'],
                 page_size = 1000,
                 page_token = None):
        
        results = []
        
        while True:
            response = self.get_batch_data(view_id, dimensions, start_date, end_date, metrics, page_size, page_token)
            results.extend(self.extract_data_from_response(response, start_date, end_date))
            page_token = response['reports'][0].get('nextPageToken')

            if page_token is None:
                break
        
        return results

    def get_sessions_by_gender(self, start_date: date, end_date: date):
        dimensions = ['customVarValue1', 'userGender']
        return self.get_data(self.view_id, dimensions, start_date, end_date)

    def get_sessions_by_landing_page(self, start_date: date, end_date: date):
        dimensions = ['customVarValue1', 'landingPagePath',
                      'deviceCategory', 'sourceMedium']
        return self.get_data(self.view_id, dimensions, start_date, end_date)

    def get_sessions_by_age(self, start_date: date, end_date: date):
        dimensions = ['customVarValue1', 'userAgeBracket']
        return self.get_data(self.view_id, dimensions, start_date, end_date)


# Test Script, to debug
# if __name__ == '__main__':
#     CLIENT_SECRETS_FILE = './credentials/credentials.json'
#     TOKEN_FILE = './credentials/token.json'
#     view_id = "23837774"
#     ga = GoogleAnalyticsApiRetrieval(google_authentication_method = GoogleAuthenticationMethod.OAuth,
#                                     oauth_credentials_filepath= CLIENT_SECRETS_FILE,
#                                     oauth_token_filepath=TOKEN_FILE,
#                                     view_id=view_id)

    # data = ga.get_sessions_by_gender(date(2021,12,25), date(2021,12,25))
    # print('data response ', data)


    # data = ga.get_sessions_by_age(date(2021,12,25), date(2021,12,25))
    # print('data response ', data)


    # data = ga.get_sessions_by_landing_page(date(2021,12,25), date(2021,12,25))
    # print('data response ', data)
