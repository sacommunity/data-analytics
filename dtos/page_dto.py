"""page dto"""
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
