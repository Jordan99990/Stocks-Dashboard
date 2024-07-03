import streamlit as st
import plotly.express as px
from tasks.stock_dict_fetcher import get_stock_symbols

from tasks.stock_data import (
    get_stock_data,
    stock_company_info,
    get_stock_info
) 

from tasks.menu import (
    menu
)

def select_stock():
    global stock_options, option
    stock_options = get_stock_symbols()
    
    option = st.selectbox("Select a stock...",
                options=list(stock_options.keys()),
                index=None,
                placeholder="Select a stock",
                label_visibility="hidden",
    )
    
    return stock_options.get(option)

# TODO : Add edge cases, in case there are no values for the indicators
def stock_intel(stock_name, selected_period):
    global stock_info
    
    def get_stock_indicator(stock_name, selected_period):
        current, percentage_value, = stock_company_info(stock_name, selected_period)
        current = round(current, 2)
        st.metric(label="__Current Price__",
              value=f'${current}',
              delta=percentage_value,
              )
        
    def get_market_cap(stock_info):
        market_cap_value = stock_info["marketCap"]
        formatted_market_cap = "{:,.0f}".format(market_cap_value)
        st.metric(label="__Market Cap__",
                value=f'${formatted_market_cap}',
                )
    
    def get_total_revenue(stock_info):
        revenue = stock_info["totalRevenue"]
        formatted_revenue = "{:,.0f}".format(revenue)
        st.metric(label="__Total Revenue__",
                value=f'${formatted_revenue}',
                )
    
    def get_trailing_pe(stock_info):
        trailing_pe = stock_info["trailingPE"]
        st.metric(label="__Trailing PE__",
                value=round(trailing_pe, 2),
                )
    
    def get_52_week_high(stock_info):
        high = stock_info["fiftyTwoWeekHigh"]
        st.metric(label="__52 Week High__",
                value=f'${high}',
                )
    
    def get_52_week_low(stock_info):
        low = stock_info["fiftyTwoWeekLow"]
        st.metric(label="__52 Week Low__",
                value=f'${low}',
                )
    
    def get_day_high(stock_info):
        high = stock_info["dayHigh"]
        st.metric(label="__Day High__",
                value=f'${high}',
                )
        
    def get_day_low(stock_info):
        low = stock_info["dayLow"]
        st.metric(label="__Day Low__",
                value=f'${low}',
                )

    def get_previous_close(stock_info):
        close = stock_info["previousClose"]
        st.metric(label="__Previous Close__",
                value=f'${close}',
                )
    
    def get_free_cash_flow(stock_info):
        free_cash_flow = stock_info["freeCashflow"]
        formatted_free_cash_flow = "{:,.0f}".format(free_cash_flow)
        st.metric(label="__Free Cash Flow__",
                value=f'${formatted_free_cash_flow}',
                )
    
    def get_earnings_growth(stock_info):
            earnings_growth = stock_info["earningsGrowth"]
            st.metric(label="__Earnings Growth Yearly__",
                    value=f'{earnings_growth}%',
                    delta=f'+{earnings_growth}%',
                    )
    
    def get_50_day_moving_avg(stock_info):
        moving_avg = stock_info["fiftyDayAverage"]
        st.metric(label="__50 Day Moving Average__",
                value=f'${moving_avg}',
                )
        
    def get_200_day_moving_avg(stock_info):
        moving_avg = stock_info["twoHundredDayAverage"]
        st.metric(label="__200 Day Moving Average__",
                value=f'${moving_avg}',
                )
    
    def get_recommendation(stock_info):
        recommendation = stock_info["recommendationKey"]
                
        st.metric(label="__Recommendation__",
                value=recommendation,
                )

    def get_bid(stock_info):
        bid = stock_info["bid"]
        st.metric(label="__Bid__",
                value=f'${bid}',
                )
    
    def get_ask(stock_info):
        ask = stock_info["ask"]
        st.metric(label="__Ask__",
                value=f'${ask}',
                )
    
    def get_target_price(stock_info):
        target_price = stock_info["targetMeanPrice"]
        st.metric(label="__Target Price__",
                value=f'${target_price}',
                )
    
    def get_currency_info(stock_info):
        currency = stock_info["currency"]
        st.metric(label="__Currency__",
                value=currency,
                )
    
    def get_symbol(stock_info):
        symbol = stock_info["symbol"]
        st.metric(label="__Symbol__",
                value=symbol,
        )
    
    
    col1, col2, col3, col4 = st.columns(4)
    
    stock_info = get_stock_info(stock_name)
    
    with col1:
        get_stock_indicator(stock_name, selected_period)
        st.write(" ")
        get_earnings_growth(stock_info)
        st.write(" ")
        get_currency_info(stock_info)
        st.write(" ")
        get_symbol(stock_info)
        
    with col2:
        get_market_cap(stock_info)
        get_total_revenue(stock_info)
        get_trailing_pe(stock_info)
        get_52_week_high(stock_info)
        get_52_week_low(stock_info)
    
    with col3:
        get_day_high(stock_info)
        get_day_low(stock_info)
        get_previous_close(stock_info)
        get_free_cash_flow(stock_info)
        get_50_day_moving_avg(stock_info)
    
    with col4:
        get_200_day_moving_avg(stock_info)
        get_recommendation(stock_info)
        get_bid(stock_info)
        get_ask(stock_info)
        get_target_price(stock_info)

def stock_price_chart(stock_name, selected_period):
    def select_chart_type():
        chart_type = st.selectbox(
            "Select chart type",
            ["Line Chart", "Candlestick Chart"],
            key='chart_type_radio',
        )
        
        return chart_type
    
    st.write(" ")
    
    _, col1, _ = st.columns(3)
    with col1: 
        select_chart_type()
    
    st.write(" ")
    _, col2 = st.columns([4, 8])
    with col2:
        st.title("Stock Price Over time")
    
    #TODO : round the values to 2 decimal places
    stock_data = get_stock_data(stock_name, selected_period)
    
    fig = px.line(stock_data, x=stock_data.index, y="Close")
    fig.update_layout(width=3*1200)
    
    fig.update_yaxes(tickprefix="$", ticksuffix="", tickformat=",.")
    
    st.plotly_chart(fig, use_container_width=True)
    
def first_page():
    menu()
    
    _, col2 = st.columns([4, 8])
    with col2:
        title_placeholder = st.empty()
    
    if 'stock' not in st.session_state:
        st.session_state.stock = None
        
    stock = select_stock()
    
    if not stock:
        return
    
    st.session_state.stock = stock
    
    title_placeholder.title(f'{list(stock_options.keys())[list(stock_options.values()).index(stock)]} ({stock})')
    
    st.write(" ")
    
    _, col2 = st.columns([4, 8])
    with col2:
        selected_period = st.radio(
            "Select period",
            ["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
            horizontal=True,
            key='selected_period_radio'
        )
        
    st.write(" ")
    
    stock_intel(stock, selected_period) 
                             
    stock_price_chart(stock, selected_period)