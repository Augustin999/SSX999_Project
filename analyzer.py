import talib as ta
import pandas as pd
import numpy as np

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
    df_OHLC = NATR(df)
    df_OHLC = ATR(df_OHLC)
    df_OHLC = EMA_fast(df_OHLC)
    df_OHLC = EMA_slow(df_OHLC)
    df_OHLC = Heiken_Ashi(df_OHLC)
    df_OHLC = RSI(df_OHLC)
    df_OHLC = MFI(df_OHLC)
    df_OHLC = MACD(df_OHLC)
    df_OHLC = OBV(df_OHLC)
    df_OHLC = AD(df_OHLC)
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
    df['rsi'] = ta.RSI(df['close'].values, 10)
    return df

def MFI(df0):
    df = df0
    df['mfi'] = ta.MFI(df['high'].values, df['low'].values,
                    df['close'].values, df['volume'].values, 14)
    return df

def EMA_fast(df0):
    df = df0
    df['ema_fast'] = ta.EMA(df['close'].values, 14)
    return df

def EMA_slow(df0):
    df = df0
    df['ema_slow'] = ta.EMA(df['close'].values, 70)
    return df

def NATR(df0):
    df = df0
    df['natr'] = ta.NATR(
        np.array(df['high'].values),
        np.array(df['low'].values),
        np.array(df['close'].values),
        14)
    return df

def ATR(df0):
    df = df0
    df['atr'] = ta.ATR(df['high'].values, df['low'].values, df['close'].values, 14)
    return df

def MACD(df0):
    df = df0
    df['macd'], df['macd_signal'], df['macd_hist'] = ta.MACD(df['close'].values)
    return df

def OBV(df0):
    df = df0
    df['obv'] = ta.OBV(df['close'].values, df['volume'].values)
    df['d_obv'] = df['obv'].pct_change()
    return df

def AD(df0):
    df = df0
    df['ad'] = ta.AD(df['high'].values, df['low'].values,
                    df['close'].values, df['volume'].values)
    return df

def CloseStd(df0):
    df = df0
    df['close_std'] = df['close'].rolling(10).std()
    return df