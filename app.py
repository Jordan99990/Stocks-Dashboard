import streamlit as st
from tasks.fetch_stocks import get_stock_symbols

st.set_page_config(
    page_title="Stock Dashboard", 
    page_icon=":chart_with_upwards_trend", 
    layout="wide")

stock_options = get_stock_symbols()

stock = st.selectbox("Select a stock...",
            options=list(stock_options.keys()),
            index=None,
            placeholder="Select a stock",
)

try:
    stock_symbol = stock_options[stock]
    st.write(f"Stock selected: {stock_symbol}") 
except KeyError:
    st.write("Please select a stock from the dropdown")