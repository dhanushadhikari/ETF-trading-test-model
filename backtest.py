# backtest.py
import pandas as pd

def backtest_strategy(df, initial_cash=10000):
    df = df.copy()
    df['Daily_Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Daily_Return'] * df['Signal'].shift(1)
    df['Portfolio_Value'] = (1 + df['Strategy_Return']).cumprod() * initial_cash

    stats = {
        "Final Portfolio Value": df['Portfolio_Value'].iloc[-1],
        "Total Return (%)": ((df['Portfolio_Value'].iloc[-1] / initial_cash) - 1) * 100,
        "Max Drawdown (%)": max_drawdown(df['Portfolio_Value']),
    }

    return df, stats

def max_drawdown(series):
    roll_max = series.cummax()
    drawdown = (series - roll_max) / roll_max
    return drawdown.min() * 100
