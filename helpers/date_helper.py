"""Date helpers"""
from datetime import date, datetime

YYYY_MM_DD_DEFAULT_FORMAT = "%Y-%m-%d"
YYYY_MM_DD_HH_MM_SS_DEFAULT_FORMAT = "%Y-%m-%d-%H-%M-%S"


def convert_date_to_yyyy_mm_dd(date_obj: date | datetime):
    """convert date to string in format yyyy-mm-dd"""
    if date_obj is None or (not isinstance(date_obj, date) and not isinstance(date_obj, datetime)):
        raise ValueError("Input is not in date format")

    return date_obj.strftime(YYYY_MM_DD_DEFAULT_FORMAT)


def convert_yyyy_mm_dd_to_date(date_str: str) -> date:
    """convert str of format yyyy-mm-dd date to date"""
    return datetime.strptime(date_str, YYYY_MM_DD_DEFAULT_FORMAT)


def convert_date_to_yyyy_mm_dd_hh_mm_ss(date_obj: date | datetime):
    """convert date time to string"""
    if date_obj is None or (not isinstance(date_obj, date) and not isinstance(date_obj, datetime)):
        raise ValueError("Input is not in date format")

    return date_obj.strftime(YYYY_MM_DD_HH_MM_SS_DEFAULT_FORMAT)


def convert_yyyy_mm_dd_hh_mm_ss_to_date(date_str: str) -> datetime:
    """convert datetime strting to datetime obj"""
    return datetime.strptime(date_str, YYYY_MM_DD_HH_MM_SS_DEFAULT_FORMAT)
