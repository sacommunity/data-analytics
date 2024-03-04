"""Date range dto"""
from datetime import date


class DateRangeDto():
    """Date range dto"""

    def __init__(self, start_date: date, end_date: date) -> None:
        self.start_date = start_date
        self.end_date = end_date

    def to_dict(self):
        """returns dictionary representation of dto"""
        return self.__dict__

    @classmethod
    def from_dict(cls, dict_obj):
        """creates new instance from dictionary"""
        return cls(**dict_obj)
