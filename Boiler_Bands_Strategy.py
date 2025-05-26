# strategy.py (add this)
def bollinger_strategy(data, window=20, num_std=2):
    df = data.copy()
    df['MA'] = df['Close'].rolling(window=window).mean()
    df['STD'] = df['Close'].rolling(window=window).std()
    df['Upper'] = df['MA'] + (num_std * df['STD'])
    df['Lower'] = df['MA'] - (num_std * df['STD'])
    
    df['Signal'] = 0
    df.loc[df['Close'] < df['Lower'], 'Signal'] = 1  # Buy
    df.loc[df['Close'] > df['Upper'], 'Signal'] = 0  # Sell
    df['Position'] = df['Signal'].diff()
    return df
