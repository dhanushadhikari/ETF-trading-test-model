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

def rsi_strategy(data, period=14, threshold_buy=30, threshold_sell=70):
    df = data.copy()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['Signal'] = 0
    df.loc[df['RSI'] < threshold_buy, 'Signal'] = 1
    df.loc[df['RSI'] > threshold_sell, 'Signal'] = 0
    df['Position'] = df['Signal'].diff()
    return df

def bollinger_strategy(data, window=20, num_std=2):
    df = data.copy()
    df['MA'] = df['Close'].rolling(window=window).mean()
    df['STD'] = df['Close'].rolling(window=window).std()
    df['Upper'] = df['MA'] + (num_std * df['STD'])
    df['Lower'] = df['MA'] - (num_std * df['STD'])

    df['Signal'] = 0
    df.loc[df['Close'] < df['Lower'], 'Signal'] = 1
    df.loc[df['Close'] > df['Upper'], 'Signal'] = 0
    df['Position'] = df['Signal'].diff()
    return df
