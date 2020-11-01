# SSX999 Project

# Augustin BRISSART
# Github: @augustin999


# utils.py

#       Data, parameters or functions useful in all files

import numpy as np
from pandas import Timestamp as ts
import pandas as pd

QUOTE = 'EUR'
PERIOD = '4h'
CAPITAL = 100
UNIVERSE = ['XBT', 'ETH', 'XMR', 'QTUM', 'ADA', 'MLN', 'ZEC']
FEE_RATE = 0.16 / 100
CSV_SEP = ','
DATA_DIR = 'Historical_data\\'
WALLET_PATH = 'wallet.pickle'
PERFORMANCES_PATH = 'performances.csv'
LASTS_PATH = 'lasts.pickle'
LOG_PATH = 'logs.txt'
DATA_COLUMNS = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']


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
        pair = 'X' + base.upper() + 'Z' + QUOTE.upper()
        if base.upper() in SPECIAL_BASES:
            pair = base.upper() + QUOTE.upper()
        return pair

def log_error(message):
    with open(LOG_PATH, 'wb') as f:
        f.write('ERROR: ' + message + '\n')
    f.close()
    return

TIME_FRAMES = {
    '1mn': 1,
    '5mn': 5,
    '15mn': 15,
    '30mn': 30,
    '1h': 60,
    '4h': 240,
    '1d': 1440,
    '1w': 10080,
    '15d': 21600
}

BASES = [
    'ETC', 'XMR', 'QTUM', 'ATOM',
    'XLM', 'DAI', 'XRP', 'LINK',
    'PAXG', 'GNO', 'REP', 'XDG',
    'MLN', 'ETH', 'ADA', 'BAT',
    'LSK', 'TRX', 'DASH', 'XTZ',
    'NANO', 'XBT', 'LTC', 'SC',
    'WAVES', 'ALGO', 'EOS', 'OMG',
    'BCH', 'ICX', 'ZEC'
]

SPECIAL_BASES = [
    'QTUM', 'ATOM', 'LINK', 'PAXG',
    'GNO', 'XDG', 'ADA', 'BAT',
    'LSK', 'TRX', 'DASH', 'XTZ',
    'NANO', 'WAVES', 'SC', 'ALGO',
    'EOS', 'OMG', 'BCH', 'ICX', 'DAI'
]

API_PUBLIC = {
    'Time',
    'Assets',
    'AssetPairs',
    'Ticker',
    'OHLC',
    'Depth',
    'Trades',
    'Spread'
}

API_PRIVATE = {
    'Balance',
    'TradeBalance',
    'OpenOrders',
    'ClosedOrders',
    'QueryOrders',
    'TradesHistory',
    'QueryTrades',
    'OpenPositions',
    'Ledgers',
    'QueryLedgers',
    'RemoveExport',
    'GetWebSocketsToken'
}

API_TRADING = {'AddOrder', 'CancelOrder'}

API_FUNDING = {
    'DepositMethods',
    'DepositAddresses',
    'DepositStatus',
    'WithdrawInfo',
    'Withdraw',
    'WithdrawStatus',
    'WithdrawCancel',
    'WalletTransfer'
}