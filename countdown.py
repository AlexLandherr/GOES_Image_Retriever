def countdown(x):
    sec_in_day = 86400
    sec_in_hour = 3600
    sec_in_minute = 60
    days = int(x // sec_in_day)
    hours = int((x - (days * sec_in_day)) // sec_in_hour)
    minutes = int((x - (days * sec_in_day) - (hours * sec_in_hour)) // sec_in_minute)
    seconds = round(((x - (days * sec_in_day) - (hours * sec_in_hour) - (minutes * 60))), 6)
    time = "{0} days, {1} hours, {2} minutes, {3} seconds.".format(str(days), str(hours), str(minutes), str(seconds))
    return time