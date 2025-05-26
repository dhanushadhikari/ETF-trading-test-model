# app.py
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from strategy import moving_average_crossover
from backtest import backtest_strategy

st.set_page_config(page_title="ETF Trading Strategy", layout="wide")

st.title("📈 ETF Profit-Maximizing Strategy (EOD)")
st.markdown("This app uses a Moving Average Crossover strategy on NYSE ETFs.")

etfs = ["SPY", "QQQ", "DIA", "IWM", "XLF", "XLK", "XLE"]
selected_etf = st.selectbox("Choose an ETF", etfs)

start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("today"))

short_window = st.slider("Short Moving Average", 5, 50, 20)
long_window = st.slider("Long Moving Average", 10, 200, 50)

if st.button("Run Strategy"):
    df = yf.download(selected_etf, start=start_date, end=end_date)
    
    if df.empty:
        st.warning("No data found. Try a different date range.")
    else:
        df = moving_average_crossover(df, short_window, long_window)
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

        st.subheader("Data Preview")
        st.dataframe(result.tail())
