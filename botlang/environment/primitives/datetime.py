import time

def time_delta_seconds(init_time, delta):
    return init_time + delta

def time_delta_minutes(init_time, delta):
    return init_time + delta * 60

def time_delta_hours(init_time, delta):
    return init_time + delta * 60 * 60

def time_delta_days(init_time, delta):
    return init_time + delta * 60 * 60 * 24

def time_from_string(string, format):
    return time.mktime(time.strptime(string, format))

def time_to_string(time_to_convert, format):
    return time.strftime(format, time.gmtime(time_to_convert))

DATETIME_PRIMITIVES = {
    'timestamp': time.time,
    'time-now': time.time,
    'time-delta-seconds': time_delta_seconds,
    'time-delta-minutes': time_delta_minutes,
    'time-delta-hours': time_delta_hours,
    'time-delta-days': time_delta_days,
    'time-from-string': time_from_string,
    'time-to-string': time_to_string
}
