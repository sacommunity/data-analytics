"""Date helpers"""
from datetime import date, datetime


class DateHelper():
    """date helper methods"""
    def __init__(self) -> None:
        self.yyyy_mm_dd_format = "%Y-%m-%d"
        self.yyyy_mm_dd_hh_mm_ss_format = "%Y-%m-%d-%H-%M-%S"

    def convert_date_to_yyyy_mm_dd(self, date_obj: date | datetime):
        """convert date to string in format yyyy-mm-dd"""
        if date_obj is None or (not isinstance(date_obj, date) \
                                and not isinstance(date_obj, datetime)):
            raise ValueError("Input is not in date format")

        return date_obj.strftime(self.yyyy_mm_dd_format)


    def convert_yyyy_mm_dd_to_date(self, date_str: str) -> date:
        """convert str of format yyyy-mm-dd date to date"""
        return datetime.strptime(date_str, self.yyyy_mm_dd_format).date()


    def convert_date_to_yyyy_mm_dd_hh_mm_ss(self, date_obj: date | datetime):
        """convert date time to string"""
        if date_obj is None or (not isinstance(date_obj, date) \
                                and not isinstance(date_obj, datetime)):
            raise ValueError("Input is not in date format")

        return date_obj.strftime(self.yyyy_mm_dd_hh_mm_ss_format)


    def convert_yyyy_mm_dd_hh_mm_ss_to_date(self, date_str: str) -> datetime:
        """convert datetime strting to datetime obj"""
        return datetime.strptime(date_str, self.yyyy_mm_dd_hh_mm_ss_format)
