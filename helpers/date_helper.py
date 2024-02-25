from datetime import date

def convert_date_to_yyyy_mm_dd(date_obj: date):
    if date_obj is None or type(date_obj) != date:
        raise ValueError("Input is not in date format")
    
    return date_obj.strftime("%Y-%m-%d")
