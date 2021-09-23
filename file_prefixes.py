def file_prefixes(x):
    KiB = 1024
    MiB = 1024**2
    GiB = 1024**3
    TiB = 1024**4
    if x >= KiB and x < MiB:
        f_size = round((x/KiB), 2)
        return str(f_size) + " KiB"
    elif x >= MiB and x < GiB:
        f_size = round((x/MiB), 2)
        return str(f_size) + " MiB"
    elif x >= GiB and x < TiB:
        f_size = round((x/GiB), 2)
        return str(f_size) + " GiB"
    elif x >= TiB:
        f_size = round((x/TiB), 2)
        return str(f_size) + " TiB"
    elif x < KiB:
        f_size = x
        return str(f_size) + " B"