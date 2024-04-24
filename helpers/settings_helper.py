"""Settings helper to retrieve settings data from json file"""
import json
from helpers.string_helper import StringHelper


class SettingsHelper():
    """helper class for app_settings.json"""
    def __init__(self, file_path = './settings/app_settings.json') -> None:
        self.file_path = file_path
        self.str_helper = StringHelper()

    def get_settings(self):
        """Get all settings from settings json"""
        file_data = ''
        with open(self.file_path, 'r', encoding="UTF-8") as file_obj:
            file_data = file_obj.read()

        if file_data is None or file_data == '':
            return None

        return json.loads(file_data)

    def get_settings_for_a_module(self, module):
        """Get settings related to particular module"""
        settings = self.get_settings()
        return settings.get(module)

    def get_value_by_key(self, module: str, key: str, is_key_required: bool = True):
        """retrieve value from module for a key"""
        module_value = self.get_settings_for_a_module(module)
        if module_value is None:
            raise ValueError(f"{module} not found in app_settings")

        key_value = module_value.get(key)
        if is_key_required and isinstance(key_value, str) \
            and self.str_helper.is_null_or_whitespace(key_value):
            raise ValueError(f"{key} not found in app_settings")

        return key_value

    def get_google_analytics_view_id_v3(self):
        """Get ViewId for google analytics"""
        return self.get_value_by_key('GoogleAnalytics', 'ViewId_V3')

    def get_google_analytics_view_id_v4(self):
        """Get ViewId for google analytics"""
        return self.get_value_by_key('GoogleAnalytics', 'ViewId_V4')

    def get_google_analytics_page_size(self):
        """get page size to retrieve data"""
        return self.get_value_by_key('GoogleAnalytics', 'PageSize')

    def get_file_storage_root_folder(self):
        """Get RootDir"""
        return self.get_value_by_key('FileStorage', 'RootDir')

    def get_web_scraping_maximum_concurrent_requests(self):
        """Get value for MaximumConcurrentRequests"""
        return self.get_value_by_key('WebScraping', 'MaximumConcurrentRequests')

    def get_web_scraping_timeout_in_seconds(self):
        """Get value for DefaultTimeoutInSeconds"""
        return self.get_value_by_key("WebScraping", "DefaultTimeoutInSeconds")

    def get_sacommunity_url(self) -> str:
        """get sacommunity url from settings"""
        return self.get_settings_for_a_module('SACommunityUrl')
