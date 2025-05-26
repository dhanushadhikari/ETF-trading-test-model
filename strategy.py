# strategy.py
import pandas as pd

def moving_average_crossover(data, short_window=20, long_window=50):
    df = data.copy()
    df['SMA_short'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_long'] = df['Close'].rolling(window=long_window).mean()
    df['Signal'] = 0
    df['Signal'][short_window:] = (
        (df['SMA_short'][short_window:] > df['SMA_long'][short_window:]).astype(int)
    )
    df['Position'] = df['Signal'].diff()
    return df
