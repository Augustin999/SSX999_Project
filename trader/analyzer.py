# SSX999 Project
#
# Augustin BRISSART
# Github: @augustin999


from ta.volatility import average_true_range, bollinger_mavg, bollinger_hband, bollinger_lband
from ta.trend import ema_indicator, macd, macd_signal, macd_diff, cci
from ta.momentum import rsi
from ta.volume import money_flow_index, on_balance_volume


def strategy_CCI(features):
    """
    Analyze a given set of candle and corresponding indicators.
    Return a position (0 or 1).

    Works well on 4h timeframe

    Inputs:
        features : dictionary
            'HA_close_current' : current Heikin-Ashi close price
            'HA_open_current' : current Heikin-Ashi open price
            'ema_current' : current EMA4
            'bollinger_center_previous': previous Bollinger moving average value (window = 160)
            'bollinger_center_current' : current Bollinger moving average value (window = 160)
            'cci_previous' : previous Commodity Channel Index value (window = 160) transformed by an EMA4
            'cci_current' : current Commodity Channel Index values (window = 160) transformed by an EMA4
            'last_position' : latest Position value (0 or 1)
        
    Results :
        Next position to hold
    """

    if features['HA_close_current'] >= features['HA_open_current']:
        current_color = 'green'
    else:
        current_color = 'red'

    new_position = features['last_position']

    if features['last_position'] == 0 and current_color == 'green' and features['ema_current'] > features['bollinger_center_current']:
        # Reason to buy validated => waiting for trigger
        if features['cci_previous'] <= 100 and features['cci_current'] > 100:
            new_position = 1
        

    if features['last_position'] == 1 and features['ema_previous'] >= features['bollinger_center_previous'] and features['ema_current'] < features['bollinger_center_current']:
        new_position = 0
    
    return new_position



def compute_indicators(df):
    df_OHLC = df
    df_OHLC = EMA(df_OHLC)
    df_OHLC = Heiken_Ashi(df_OHLC)
    df_OHLC = CCI(df_OHLC)
    df_OHLC = Bollinger(df_OHLC)

    return df_OHLC


def Heiken_Ashi(df0):
    df = df0
    df['HA_open'] = round((df['open'].shift(1) + df['close'].shift(1))/2, 4)
    df['HA_close'] = round((df['open'] + df['high'] + df['low'] + df['close'])/4, 4)
    df['HA_high'] = round(df[['high', 'HA_open', 'HA_close']].max(axis=1), 4)
    df['HA_low'] = round(df[['low', 'HA_open', 'HA_close']].min(axis=1), 4)
    return df


def CCI(df0, n=160):
    df = df0
    df['cci'] = ema_indicator(cci(df['high'], df['low'], df['close'], n, 0.015, fillna=False), 4, fillna=False)
    return df


def EMA(df0, n=4):
    df = df0
    df['ema'] = ema_indicator(df['close'], n, fillna=False)
    return df


def Bollinger(df0, n=160):
    df = df0
    df['bollinger_center'] = bollinger_mavg(df['close'], n, fillna=False)
    df['bollinger_upper'] = bollinger_hband(df['close'], n, fillna=False)
    df['bollinger_lower'] = bollinger_lband(df['close'], n, fillna=False)
    return df
    

def RSI(df0):
    df = df0
    df['rsi'] = rsi(df['close'], 10, fillna=False)
    return df


def MFI(df0):
    df = df0
    df['mfi'] = money_flow_index(
        df['high'],
        df['low'],
        df['close'],
        df['volume'],
        14,
        fillna=False
    )
    return df


def ATR(df0):
    df = df0
    df['atr'] = average_true_range(
        df['high'],
        df['low'],
        df['low'],
        14,
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
