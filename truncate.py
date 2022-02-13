def truncate(value, precision):
    '''Returns a truncated float value to a given precision/number of decimal places.'''
    return int(value * 10 ** precision) / 10 ** precision