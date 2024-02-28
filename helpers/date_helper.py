from datetime import date, datetime

YYYY_MM_DD_DEFAULT_FORMAT = "%Y-%m-%d"
YYYY_MM_DD_HH_MM_SS_DEFAULT_FORMAT = "%Y-%m-%d-%H-%M-%S"

def convert_date_to_yyyy_mm_dd(date_obj: date | datetime):
    if date_obj is None or (type(date_obj) != date and type(date_obj) != datetime):
        raise ValueError("Input is not in date format")
    
    return date_obj.strftime(YYYY_MM_DD_DEFAULT_FORMAT)

def convert_yyyy_mm_dd_to_date(date_str: str) -> date:
    return datetime.strptime(date_str, YYYY_MM_DD_DEFAULT_FORMAT)

def convert_date_to_yyyy_mm_dd_hh_mm_ss(date_obj: date | datetime):
    if date_obj is None or (type(date_obj) != date and type(date_obj) != datetime):
        raise ValueError("Input is not in date format")
    
    return date_obj.strftime(YYYY_MM_DD_HH_MM_SS_DEFAULT_FORMAT)

def convert_yyyy_mm_dd_hh_mm_ss_to_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, YYYY_MM_DD_HH_MM_SS_DEFAULT_FORMAT)