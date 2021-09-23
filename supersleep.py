import time

def supersleep(wait):
    endtime = time.time() + wait
    while time.time() < endtime:
        pass