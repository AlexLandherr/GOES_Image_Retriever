from datetime import datetime, timezone

#Returns a datetime object for further use in a program. The argument is converted into a string
#in the format "Y-M-D H:M:S", where values less than 10 can be zero-padded.

def UTC_time_stamp(t):
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

#recording_start_time = str(input("Set a start time in UTC for a process, e.g. 2020-05-11 22:20:00: "))
#recording_start_date, recording_start_time_of_day = recording_start_time.split(" ")

#recording_start_year, recording_start_month, recording_start_day = recording_start_date.split('-')
#recording_start_hour, recording_start_min, recording_start_sec = recording_start_time_of_day.split(':')

#recording_stop_time = str(input("Set a stop time in UTC for a process, e.g. 2020-05-11 22:30:00: "))
#recording_stop_date, recording_stop_time_of_day = recording_stop_time.split(" ")

#recording_stop_year, recording_stop_month, recording_stop_day = recording_stop_date.split("-")
#recording_stop_hour, recording_stop_min, recording_stop_sec = recording_stop_time_of_day.split(":")

#rec_start_year = int(recording_start_year)
#rec_start_month = int(recording_start_month)
#rec_start_day = int(recording_start_day)
#rec_start_hour = int(recording_start_hour)
#rec_start_min = int(recording_start_min)
#rec_start_sec = int(recording_start_sec)

#rec_stop_year = int(recording_stop_year)
#rec_stop_month = int(recording_stop_month)
#rec_stop_day = int(recording_stop_day)
#rec_stop_hour = int(recording_stop_hour)
#rec_stop_min = int(recording_stop_min)
#rec_stop_sec = int(recording_stop_sec)

#stop = datetime(rec_stop_year, rec_stop_month, rec_stop_day, hour=rec_stop_hour, minute=rec_stop_min, second=rec_stop_sec)
#start = datetime(rec_start_year, rec_start_month, rec_start_day, hour=rec_start_hour, minute=rec_start_min, second=rec_start_sec)