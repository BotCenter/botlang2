import calendar
import time

from datetime import datetime
from dateutil import parser

import pytz
from pytz import timezone


utc = pytz.utc


weekdays = {
    'EN': [
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
        'sunday'
    ],
    'ES': [
        'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'
    ]
}


def time_delta_seconds(init_time, delta):
    return init_time + delta


def time_delta_minutes(init_time, delta):
    return init_time + delta * 60


def time_delta_hours(init_time, delta):
    return init_time + delta * 60 * 60


def time_delta_days(init_time, delta):
    return init_time + delta * 60 * 60 * 24


def time_from_string(string):
    dt = parser.parse(string)
    return calendar.timegm(dt.utctimetuple())


def time_to_string(time_to_convert, format, tz_string='UTC'):
    return time_localize(time_to_convert, tz_string).strftime(format)


def time_localize(time_to_localize, tz_string='UTC'):
    utc_dt = datetime.fromtimestamp(time_to_localize, tz=utc)
    locale_tz = timezone(tz_string)
    return utc_dt.astimezone(locale_tz)


def time_weekday(t, tz_string='UTC'):
    return time_localize(t, tz_string).weekday()


def time_weekday_iso(t, tz_string='UTC'):
    return time_localize(t, tz_string).isoweekday()


def time_weekday_str(t, lang='ES', tz_string='UTC'):
    weekday = time_weekday(t, tz_string)
    return weekdays[lang][weekday]


def time_year(t, tz_string='UTC'):
    return time_localize(t, tz_string).year


def time_month(t, tz_string='UTC'):
    return time_localize(t, tz_string).month


def time_day(t, tz_string='UTC'):
    return time_localize(t, tz_string).day


def time_hour(t, tz_string='UTC'):
    return time_localize(t, tz_string).hour


def time_minute(t, tz_string='UTC'):
    return time_localize(t, tz_string).minute


def time_second(t, tz_string='UTC'):
    return time_localize(t, tz_string).second


DATETIME_PRIMITIVES = {
    'timestamp': time.time,
    'time-now': time.time,
    'time-delta-seconds': time_delta_seconds,
    'time-delta-minutes': time_delta_minutes,
    'time-delta-hours': time_delta_hours,
    'time-delta-days': time_delta_days,
    'time-from-string': time_from_string,
    'time-to-string': time_to_string,
    'time-weekday': time_weekday,
    'time-weekday-iso': time_weekday_iso,
    'time-weekday-str': time_weekday_str,
    'time-year': time_year,
    'time-month': time_month,
    'time-day': time_day,
    'time-hour': time_hour,
    'time-minute': time_minute,
    'time-second': time_second
}
