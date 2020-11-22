from ta.volatility import average_true_range
from ta.trend import ema_indicator, macd, macd_signal, macd_diff
from ta.momentum import rsi
from ta.volume import money_flow_index, on_balance_volume


def strategy_HA_MFI(features):
    """
    Analyze a given set of candle and corresponding indicators.
    Return a position (0 or 1).

    Inputs:
        features : dictionary
            'HA_open' : current Heikin-Ashi open
            'HA_close' : current Heikin-Ashi close
            'mfi_prev' : previous MFI index value
            'mfi_curr' : current MFI index value
            'lastPosition' : latest Position value (0 or 1)
        
    Results :
        Next position to hold
    """

    # Buy case
    if features['HA_close'] >= features['HA_open'] and features['mfi_curr'] > 70 and features['mfi_prev'] <= 70:
        newPosition = 1

    # Sell case
    elif features['HA_close'] <= features['HA_open'] and features['mfi_curr'] <= 30 and features['mfi_prev'] > 30:
        newPosition = 0

    # Stay case
    else:
        newPosition = features['lastPosition']
    
    return newPosition


def compute_indicators(df):
    df_OHLC = ATR(df)
    df_OHLC = EMA_fast(df_OHLC)
    df_OHLC = EMA_slow(df_OHLC)
    df_OHLC = Heiken_Ashi(df_OHLC)
    df_OHLC = RSI(df_OHLC)
    df_OHLC = MFI(df_OHLC)
    df_OHLC = MACD(df_OHLC)
    df_OHLC = OBV(df_OHLC)
    df_OHLC = CloseStd(df_OHLC)

    return df_OHLC


def Heiken_Ashi(df0):
    df = df0
    df['HA_open'] = round((df['open'].shift(1) + df['close'].shift(1))/2, 4)
    df['HA_high'] = round(df[['high', 'open', 'close']].max(axis=1), 4)
    df['HA_low'] = round(df[['low', 'open', 'close']].min(axis=1), 4)
    df['HA_close'] = round(
        (df['open'] + df['high'] + df['low'] + df['close'])/4, 4)
    return df


def RSI(df0):
    df = df0
    df['rsi'] = rsi(df['close'], n=10, fillna=False)
    return df


def MFI(df0):
    df = df0
    df['mfi'] = money_flow_index(
        df['high'],
        df['low'],
        df['close'],
        df['volume'],
        n=14,
        fillna=False
    )
    return df


def EMA_fast(df0):
    df = df0
    df['ema_fast'] = ema_indicator(df['close'], n=14, fillna=False)
    return df


def EMA_slow(df0):
    df = df0
    df['ema_slow'] = ema_indicator(df['close'], n=70, fillna=False)
    return df


def ATR(df0):
    df = df0
    df['atr'] = average_true_range(
        df['high'],
        df['low'],
        df['low'],
        n=14,
        fillna=False
    )
    return df


def MACD(df0):
    df = df0
    df['macd'] = macd(df['close'], n_slow=26, n_fast=12, fillna=False)
    df['macd_signal'] = macd_signal(df['close'], n_slow=26, n_fast=12, n_sign=9, fillna=False)
    df['macd_hist'] = macd_diff(df['close'], n_slow=26, n_fast=12, n_sign=9, fillna=False)
    return df


def OBV(df0):
    df = df0
    df['obv'] = on_balance_volume(df['close'], df['volume'], fillna=False)
    return df


def CloseStd(df0):
    df = df0
    df['close_std'] = df['close'].rolling(10).std()
    return df
