# -*- coding: utf-8 -*-
import os
from datetime import datetime


def dateextract(fname):
    """
    Return a datetime parsed from the filename for sorting.
    Expected CAN filename pattern: <something>_<YYYYMMDD-%H%M%S>*.asc
    If parse fails, return datetime.min so non-parsables sink to the start.
    """
    clean_name = fname
    try:
        base = os.path.basename(fname)
        # If it's a CAN .asc, strip extension and take the 2nd token after underscore
        if ("CAN" in base) and base.lower().endswith(".asc"):
            base_no_ext = base[:-4]
            parts = base_no_ext.split("_")
            if len(parts) >= 2:
                clean_name = parts[1]
        # Parse "YYYYMMDD-%H%M%S"
        return datetime.strptime(clean_name, "%Y%m%d-%H%M%S")
    except Exception:
        return datetime.min


def canlogs(path, entry_time):
    """
    Return the last CAN log whose timestamp is <= target timestamp.
    """
    dt_target = datetime.strptime(entry_time, "%Y-%m-%d %H-%M-%S")

    # List files; you can filter to .asc if needed
    names = os.listdir(path)
    # Sort by extracted datetime
    names.sort(key=dateextract)

    lower = []
    for n in names:
        # Expect timestamp as the 2nd token: *_YYYYMMDD-%H%M%S_*.asc
        name_no_ext = os.path.splitext(n)[0]
        parts = name_no_ext.split("_")
        if len(parts) >= 2:
            timestamp = parts[1]
            try:
                dt = datetime.strptime(timestamp, "%Y%m%d-%H%M%S")
            except Exception:
                continue
            # Compare datetimes (not strings)
            if dt <= dt_target:
                lower.append(n)

    if lower:
        return lower[-1]           # nearest <= target
    elif names:
        return names[0]            # fallback: earliest file
    else:
        return None                # no files


def extractcanlogs(path, entry_time):
    """
    Return up to 7 files around the anchor:
    [anchor-3, ..., anchor, ..., anchor+3]
    If anchor not found, return up to 6 from start.
    """
    names = sorted(os.listdir(path))
    anchor = canlogs(path, entry_time)
    if not anchor:
        return names[:min(6, len(names))]

    try:
        idx = names.index(anchor)
    except ValueError:
        return names[:min(6, len(names))]

    start = max(0, idx - 3)
    end = min(len(names), idx + 4)
    return names[start:end]