# """version 4 of google analytics data"""
# from data_retrieval.google_analytics_api_retrieval import GoogleAnalyticsApiRetrieval
# from dtos.google_analytics_filter_clause_dto import GoogleAnalyticsFilterClause
# from dtos.google_analytics_request_config_dto import GoogleAnalyticsRequestConfig
# from helpers.enums import GoogleAuthenticationMethod


# class GoogleAnalyticsApiRetrievalV4(GoogleAnalyticsApiRetrieval):
#     """google analytics version 4"""
#     def __init__(self, google_authentication_method: GoogleAuthenticationMethod,
#                  oauth_credentials_filepath: str = '',
#                  oauth_token_filepath: str = '') -> None:
#         super().__init__(google_authentication_method,
#                          oauth_credentials_filepath,
#                          oauth_token_filepath)

#     def get_sessions_by_gender(self):
#         """get session data by gender"""
#         return None

#     def get_sessions_by_landing_page(self):
#         """get session data with landing page"""
#         return None

#     def get_sessions_by_age(self):
#         """get sessions data by age"""
#         return None

#     def get_page_views_and_sessions(self):
#         """get page views"""
#         return None
