# SSX999 Project

# Augustin BRISSART
# Github: @augustin999


# utils.py

#       Data, parameters or functions useful in all files

import numpy as np
import pandas as pd
from pandas import Timestamp as ts

import config


def StoUnix(tsSeries):
    """
    Convert a series of multiple string-like timestamp into a unix timestamp.
    """
    return tsSeries.astype(np.int64)//10**9


def StoTs(unixSeries):
    """
    Convert a series of multiple unix timestamp into a string-like timestamp.
    """
    return pd.to_datetime(unixSeries, utc=True, unit='s')


def toTs(unixDate):
    """
    Convert a single unixTimestamp to UTC time.
    """
    return ts(unixDate, tz='utc', unit='s')


def toUnix(tsDate):
    """
    Convert a single UTC Time to UnixTimestamp.
    """
    return StoUnix(pd.Series([tsDate]))[0]

def set_pair(base):
        """
        Return a correct pair with any base and quote, 
        taking into consideration currencies' specificities.
        """
        pair = 'X' + base.upper() + 'Z' + config.QUOTE.upper()
        if base.upper() in config.SPECIAL_BASES:
            pair = base.upper() + config.QUOTE.upper()
        return pair
