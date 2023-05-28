"""
util.py

Shared utility functions.
"""
from datetime import datetime


def fmt_print_str(dtg_str: str, inp_fmt: str, clock_fmt: str = '12') -> str:
    """
    Format a DTG for output.

    Args:
        dtg_str: str
            Datetime group string to convert.
        inp_fmt: str
            Input datetime format string.
        clock_fmt: str
            Clock format, either '12' or '24'.

    Returns:
        str
    """
    dtg = datetime.strftime(dtg_str, inp_fmt)

    if clock_fmt == '12':
        rtn_str = dtg.strftime('%a %I:%M %p')
    elif clock_fmt == '24':
        rtn_str = dtg.strftime('%a %H:%M')

    return rtn_str


def sec_to_hour_min(secs: int | str) -> str:
    """
    Convert elapsed time in seconds to hours & minutes.

    Args:
        secs: str or int
            Elapsed time, in seconds.

    Returns:
        str
    """
    secs = secs if isinstance(secs, int) else int(secs)

    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)

    hours = str(hours).zfill(2)
    mins = str(mins).zfill(2)

    return f'{hours}:{mins}'


