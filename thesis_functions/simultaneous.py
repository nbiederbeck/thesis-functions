import numpy as np
from astropy.time import Time


def magic_times_to_unixtime(times):
    """Calculate unixtime from MAGIC root file time.

    Parameters
    ----------
    times: time container opened with uproot: `file['Events']['MTime_1.']`

    Returns
    -------
    Timestamps in unix seconds

    """
    # Get milliseconds (int), nanoseconds (int)
    ms = times[b"MTime_1.fTime.fMilliSec"].array()
    ns = times[b"MTime_1.fNanoSec"].array()

    # Calculate seconds (float)
    s_f = np.array(ms + ns / 1e6) / 1e3

    # Get MJD, directly converted to unixtime (-> seconds)
    mjd = Time(times[b"MTime_1.fMjd"].array(), format="mjd").unix

    timestamps = mjd + s_f

    return timestamps
