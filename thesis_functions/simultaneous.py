import numpy as np
from astropy.time import Time


def magic_times_to_unixtime(times):
    """
    Parameters
    ----------
    times: time container opened with uproot: `file['Events']['MTime_1.']`
    """
    # Get milliseconds (int), nanoseconds (int)
    ms = times[b"MTime_1.fTime.fMilliSec"].array()
    ns = times[b"MTime_1.fNanoSec"].array()

    # Calculate milliseconds (float)
    ms_f = np.array(ms + ns / 1e6)

    # Get MJD, directly converted to unixtime (-> seconds)
    mjd = Time(times[b"MTime_1.fMjd"].array(), format="mjd").unix

    # Calculate ISO timestamps from milliseconds and unixtime
    timestamps = np.array(mjd * 1e3 + ms_f, dtype="datetime64[ms]")

    # Calculate unixtime to return
    magic_unixtime = Time(timestamps.astype("<U23"), format="isot").unix

    return magic_unixtime


def get_indices_of_simultaneous_event(times0, times1, tol=1e-16):
    """Return indices of simultaneous events in a given relative tolarance.

    The first array returned are the indices of the first times parameter,
    and vice versa.
    """
    # Calculate Masks where the timings overlap
    m1 = times1 < times0[-1]
    m2 = times1 > times0[0]
    m3 = times0 < times1[-1]
    m4 = times0 > times1[0]
    n_close = np.isclose(
        times1[(m1 & m2)].reshape(1, -1), times0[(m3 & m4)].reshape(-1, 1), atol=tol
    )
    n_zero = n_close.nonzero()
    index0 = (times0[(m3 & m4)][n_zero[0]] == times0).nonzero()
    index1 = (times1[(m1 & m2)][n_zero[1]] == times1).nonzero()
    return index0, index1
