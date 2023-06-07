import datetime


def timestamp_to_str(timestamp: int) -> str:
    return datetime.datetime.strftime(
        datetime.datetime.fromtimestamp(
            timestamp, datetime.timezone(datetime.timedelta(hours=8))), '%Y-%m-%d %H:%M:%S')


def str_to_datetime(raw: str, type: int) -> datetime.datetime:
    if type == 1:
        return datetime.datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")
    elif type == 2:
        return datetime.datetime.strptime(raw, "%Y-%m-%d")


def datetime_to_str(raw: datetime.datetime, type: int) -> str:
    return raw.strftime("%Y-%m-%d %H:%M:%S") if type == 1 else raw.strftime("%Y-%m-%d")


def datetime_to_ymd(raw: datetime.datetime) -> datetime:
    s = datetime_to_str(raw, 2)
    return str_to_datetime(s, 2)
