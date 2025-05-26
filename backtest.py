import pandas as pd

def backtest_strategy(df, initial_cash=10000):
    df = df.copy()
    df['Signal'].fillna(0, inplace=True)
    df['Position'].fillna(0, inplace=True)

    df['Holdings'] = df['Signal'] * df['Close']
    df['Cash'] = initial_cash - (df['Position'] * df['Close']).cumsum()
    df['Portfolio_Value'] = df['Cash'] + df['Holdings']
    df['Returns'] = df['Portfolio_Value'].pct_change().fillna(0)

    final_value = df['Portfolio_Value'].iloc[-1]
    total_return = ((final_value - initial_cash) / initial_cash) * 100
    max_drawdown = ((df['Portfolio_Value'].cummax() - df['Portfolio_Value']) / df['Portfolio_Value'].cummax()).max() * 100

    stats = {
        "Final Portfolio Value": final_value,
        "Total Return (%)": total_return,
        "Max Drawdown (%)": max_drawdown
    }

    return df, stats
