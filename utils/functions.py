import time
import datetime


def datetime_to_timestamp(_datetime):
    return int(time.mktime(_datetime.timetuple()))


def iso_string_to_timestamp(iso_string):
    return datetime_to_timestamp(datetime.datetime.strptime(iso_string, '%Y-%m-%dT%H:%M:%S'))


def timestamp_to_iso_string(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).isoformat()


def get_today_midnight():
    return datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
