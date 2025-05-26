# strategy.py (add this)
def rsi_strategy(data, period=14, threshold_buy=30, threshold_sell=70):
    df = data.copy()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df['Signal'] = 0
    df.loc[df['RSI'] < threshold_buy, 'Signal'] = 1  # Buy
    df.loc[df['RSI'] > threshold_sell, 'Signal'] = 0  # Sell / Hold Cash
    df['Position'] = df['Signal'].diff()
    return df
