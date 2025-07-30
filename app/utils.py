from datetime import datetime

def validate_date(date_text: str) -> bool:
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def format_na_if_empty(value):
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return "NA"
    return value
