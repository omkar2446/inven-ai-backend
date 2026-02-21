from datetime import datetime, timedelta

def parse_date(date_str):

    if not date_str:
        return None

    try:
        return datetime.fromisoformat(date_str).date()
    except Exception as e:
        print("DATE PARSE ERROR:", e)
        return None