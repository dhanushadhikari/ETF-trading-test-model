import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

from strategy import (
    moving_average_crossover,
    rsi_strategy,
    bollinger_strategy
)
from backtest import backtest_strategy
from utils import simulate_growth

st.set_page_config(page_title="ETF Strategy App", layout="wide")
st.title("📈 ETF Profit-Maximizing Strategy (EOD)")
st.markdown("Backtest strategies and project your path to $750/month income.")

etfs = ["SPY", "QQQ", "DIA", "IWM", "XLF", "XLK", "XLE"]
selected_etf = st.selectbox("Choose an ETF", etfs)

start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("today"))

strategy = st.selectbox("Select Strategy", ["Moving Average Crossover", "RSI", "Bollinger Bands"])

if strategy == "Moving Average Crossover":
    short_window = st.slider("Short Moving Average", 5, 50, 20)
    long_window = st.slider("Long Moving Average", 10, 200, 50)
elif strategy == "RSI":
    rsi_period = st.slider("RSI Period", 5, 30, 14)
    rsi_buy = st.slider("Buy Threshold (RSI)", 10, 50, 30)
    rsi_sell = st.slider("Sell Threshold (RSI)", 50, 90, 70)
elif strategy == "Bollinger Bands":
    bb_window = st.slider("Window", 10, 50, 20)
    bb_std = st.slider("Standard Deviations", 1, 3, 2)

if st.button("Run Strategy"):
    df = yf.download(selected_etf, start=start_date, end=end_date)

    if df.empty:
        st.warning("No data found. Try a different date range.")
    else:
        if strategy == "Moving Average Crossover":
            df = moving_average_crossover(df, short_window, long_window)
        elif strategy == "RSI":
            df = rsi_strategy(df, rsi_period, rsi_buy, rsi_sell)
        elif strategy == "Bollinger Bands":
            df = bollinger_strategy(df, bb_window, bb_std)

        result, stats = backtest_strategy(df)

        st.subheader("Performance Metrics")
        st.metric("Final Portfolio Value ($)", f"{stats['Final Portfolio Value']:.2f}")
        st.metric("Total Return (%)", f"{stats['Total Return (%)']:.2f}")
        st.metric("Max Drawdown (%)", f"{stats['Max Drawdown (%)']:.2f}")

        st.subheader("Equity Curve")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(result.index, result['Portfolio_Value'], label="Strategy Portfolio")
        ax.set_title("Strategy Equity Curve")
        ax.set_ylabel("Portfolio Value")
        ax.legend()
        st.pyplot(fig)

        st.subheader("Signal Preview")
        st.dataframe(result.tail())

st.markdown("---")
st.header("📊 Simulate Compounding to Reach $750/month")
initial = st.number_input("Starting Capital ($)", value=5000)
monthly_return = st.number_input("Monthly Return (%)", value=3.0)
target_income = st.number_input("Target Monthly Income ($)", value=750.0)
months = st.slider("Months to Simulate", 6, 60, 24)

if st.button("Run Compounding Simulation"):
    growth = simulate_growth(initial, monthly_return, months)
    df_growth = pd.DataFrame({
        "Month": range(len(growth)),
        "Portfolio Value": growth,
        "Estimated Monthly Profit": [v * (monthly_return / 100) for v in growth]
    })
    st.line_chart(df_growth.set_index("Month"))

    month_hit_target = next((i for i, profit in enumerate(df_growth["Estimated Monthly Profit"]) if profit >= target_income), None)
    if month_hit_target:
        st.success(f"🎯 You can expect to reach ${target_income:.0f}/month in about {month_hit_target} months.")
    else:
        st.warning("Target not reached in simulation period.")
