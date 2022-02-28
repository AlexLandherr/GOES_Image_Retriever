from datetime import datetime, timezone

def UTC_time_stamp(t):
    '''Returns a datetime object for further use in a program. The argument is converted into a string
    in the format "Y-M-D H:M:S", where values less than 10 can be zero-padded.'''
    time = str(t)
    date, time_of_day = time.split(" ")
    year, month, day = date.split('-')
    hour, minute, second = time_of_day.split(':')
    y = int(year)
    m = int(month)
    d = int(day)
    h = int(hour)
    min = int(minute)
    sec = int(second)
    return datetime(y, m, d, h, min, sec, tzinfo=timezone.utc)