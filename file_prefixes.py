from truncate import truncate

def file_prefixes(bytes, precision=2):
    '''Returns a string representing an amount of data with binary prefixes and truncates that value to two decimal places.
    Returns 0 bytes if given a negative value.'''
    zero_bytes = 0
    KiB = 1024
    MiB = 1024**2
    GiB = 1024**3
    TiB = 1024**4
    PiB = 1024**5
    EiB = 1024**6
    ZiB = 1024**7
    YiB = 1024**8
    if bytes < 0:
        return "{0} B".format(zero_bytes)
    elif bytes < KiB:
        return "{0} B".format(bytes)
    elif KiB <= bytes < MiB:
        return "{0} KiB".format(truncate(bytes / KiB, precision))
    elif MiB <= bytes < GiB:
        return "{0} MiB".format(truncate(bytes / MiB, precision))
    elif GiB <= bytes < TiB:
        return "{0} GiB".format(truncate(bytes / GiB, precision))
    elif TiB <= bytes < PiB:
        return "{0} TiB".format(truncate(bytes / TiB, precision))
    elif PiB <= bytes < EiB:
        return "{0} PiB".format(truncate(bytes / PiB, precision))
    elif EiB <= bytes < ZiB:
        return "{0} EiB".format(truncate(bytes / EiB, precision))
    elif ZiB <= bytes < YiB:
        return "{0} ZiB".format(truncate(bytes / ZiB, precision))
    elif YiB <= bytes:
        return "{0} YiB".format(truncate(bytes / YiB, precision))