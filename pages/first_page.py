import streamlit as st
import plotly.express as px
from tasks.stock_dict_fetcher import get_stock_symbols
from tasks.stock_data import (
    get_current_price,
    get_stock_data
) 

from tasks.menu import (
    menu
)

def select_stock():
    global stock_options
    stock_options = get_stock_symbols()

    option = st.selectbox("Select a stock...",
                options=list(stock_options.keys()),
                index=None,
                placeholder="Select a stock",
                label_visibility="hidden",
    )
    
    return stock_options.get(option)

def stock_screener(stock_name):
    def current_price(stock_name):
        current = get_current_price(stock_name)
        st.metric(label="Current Price", 
                  value=current, 
                  delta=current)
            
    current_price(stock_name)
        
def stock_price_line_chart(stock_name):
    _, col2 = st.columns([4, 8])
    with col2:
        period = st.radio(
            "Select period",
            ["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
            horizontal = True,
        )   
    stock_data = get_stock_data(stock_name, 
                                period = period)
    
    fig = px.line(stock_data, 
                  x=stock_data.index, 
                  y=stock_data["Close"]
                )
    
    st.plotly_chart(fig, use_container_width=True)
    
def first_page():
    menu()
    
    _, col2 = st.columns([4, 8])
    with col2:
        title_placeholder = st.empty()
    
    stock = select_stock()
    
    if not stock:
        return
    
    title_placeholder.title(f'{list(stock_options.keys())[list(stock_options.values()).index(stock)]} ({stock})')
    

    stock_screener(stock)
    stock_price_line_chart(stock)