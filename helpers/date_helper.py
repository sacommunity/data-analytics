from datetime import date, datetime

def convert_date_to_yyyy_mm_dd(date_obj: date | datetime):
    if date_obj is None or (type(date_obj) != date and type(date_obj) != datetime):
        raise ValueError("Input is not in date format")
    
    return date_obj.strftime("%Y-%m-%d")

def convert_date_to_yyyy_mm_dd_hh_mm_ss(date_obj: date | datetime):
    if date_obj is None or (type(date_obj) != date and type(date_obj) != datetime):
        raise ValueError("Input is not in date format")
    
    return date_obj.strftime("%Y-%m-%d-%H-%M-%S")