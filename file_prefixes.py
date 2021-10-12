def file_prefixes(x):
    KiB = 1024
    MiB = 1024**2
    GiB = 1024**3
    TiB = 1024**4
    PiB = 1024**5
    EiB = 1024**6
    ZiB = 1024**7
    YiB = 1024**8
    if x < KiB:
        return "{0} B".format(x)
    elif KiB <= x < MiB:
        return "{0:.2f} KiB".format(x / KiB)
    elif MiB <= x < GiB:
        return "{0:.2f} MiB".format(x / MiB)
    elif GiB <= x < TiB:
        return "{0:.2f} GiB".format(x / GiB)
    elif TiB <= x < PiB:
        return "{0:.2f} TiB".format(x / TiB)
    elif PiB <= x < EiB:
        return "{0:.2f} PiB".format(x / PiB)
    elif EiB <= x < ZiB:
        return "{0:.2f} EiB".format(x / EiB)
    elif ZiB <= x < YiB:
        return "{0:.2f} ZiB".format(x / ZiB)
    elif YiB <= x:
        return "{0:.2f} YiB".format(x / YiB)