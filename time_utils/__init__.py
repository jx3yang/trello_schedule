import datetime as dt

def get_date_dt(date_string: str, time_delta=0) -> dt.datetime:
    idx_to_unit = ['year', 'month', 'day', 'hour', 'minute', 'second']
    units = { unit: 0 for unit in idx_to_unit }
    for idx, t in enumerate(date_string.split(',')):
        units[idx_to_unit[idx]] = int(t)
    return dt.datetime(**units) + dt.timedelta(days=time_delta)

def get_date(date_string: str, time_delta=0) -> str:
    return get_date_dt(date_string, time_delta).isoformat()

__all__ = ['get_date', 'get_date_dt']
