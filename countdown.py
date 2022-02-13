from truncate import truncate

def countdown(sec):
    '''Returns a string representing the corresponding days, hours, minutes and seconds from a given value of seconds.
    Can take a float or int.'''
    sec_in_day = 86400
    sec_in_hour = 3600
    sec_in_minute = 60
    days = int(sec // sec_in_day)
    hours = int((sec - (days * sec_in_day)) // sec_in_hour)
    minutes = int((sec - (days * sec_in_day) - (hours * sec_in_hour)) // sec_in_minute)
    seconds = truncate(((sec - (days * sec_in_day) - (hours * sec_in_hour) - (minutes * 60))), 6)
    time = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds."
    return time