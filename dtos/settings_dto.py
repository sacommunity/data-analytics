"""settings dto"""

class SettingsDto():
    """settings class"""
    def __init__(self) -> None:
        self.cu_dataset_file_path = ''
        self.client_secret_file_path = ''
        self.token_file_path = ''
        self.sa_community_export_file_path = ''

    def set_cu_dataset_file_path(self, file_path: str):
        """set cu_dataset file path"""
        self.cu_dataset_file_path = file_path

    def set_client_secret_file_path(self, file_path: str):
        """set client secret file path"""
        self.client_secret_file_path = file_path

    def set_token_file_path(self, file_path: str):
        """set token file path"""
        self.token_file_path = file_path

    def set_sa_community_export_file_path(self, file_path: str):
        """set sa community export file path"""
        self.sa_community_export_file_path = file_path

    def to_dict(self):
        """returns dictionary representation of dto"""
        return self.__dict__

    @classmethod
    def from_dict(cls, dict_obj):
        """creates new instance from dictionary"""
        return cls(**dict_obj)
    