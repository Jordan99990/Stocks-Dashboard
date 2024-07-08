import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from tasks.stock_dict_fetcher import get_stock_symbols

CONFIG = {
    "period_options": ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
}

from tasks.stock_data import (
    get_stock_data,
    stock_company_info,
    get_stock_info
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
            
            earnings_growth = f'+{earnings_growth}' if earnings_growth > 0 else f'{earnings_growth}'
            
            st.metric(label="__Earnings Growth Yearly__",
                    value=earnings_growth + '%',
                    delta=earnings_growth + '%',
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
        try:
            get_stock_indicator(stock_name, selected_period)
        except KeyError:
            st.error("Stock indicator not available")
        st.write(" ")
        try:
            get_earnings_growth(stock_info)
        except KeyError:
            st.error("Earnings growth not available")
        st.write(" ")
        try:
            get_currency_info(stock_info)
        except KeyError:
            st.error("Currency info not available")
        st.write(" ")
        try:
            get_symbol(stock_info)
        except KeyError:
            st.error("Symbol not available")
        
    with col2:
        try:
            get_market_cap(stock_info)
        except KeyError:
            st.error("Market cap not available")
        try:
            get_total_revenue(stock_info)
        except KeyError:
            st.error("Total revenue not available")
        try:
            get_trailing_pe(stock_info)
        except KeyError:
            st.error("Trailing PE not available")
        try:
            get_52_week_high(stock_info)
        except KeyError:
            st.error("52 week high not available")
        try:
            get_52_week_low(stock_info)
        except KeyError:
            st.error("52 week low not available")
    
    with col3:
        try:
            get_day_high(stock_info)
        except KeyError:
            st.error("Day high not available")
        try:
            get_day_low(stock_info)
        except KeyError:
            st.error("Day low not available")
        try:
            get_previous_close(stock_info)
        except KeyError:
            st.error("Previous close not available")
        try:
            get_free_cash_flow(stock_info)
        except KeyError:
            st.error("Free cash flow not available")
        try:
            get_50_day_moving_avg(stock_info)
        except KeyError:
            st.error("50 day moving average not available")
    
    with col4:
        try:
            get_200_day_moving_avg(stock_info)
        except KeyError:
            st.error("200 day moving average not available")
        try:
            get_recommendation(stock_info)
        except KeyError:
            st.error("Recommendation not available")
        try:
            get_bid(stock_info)
        except KeyError:
            st.error("Bid not available")
        try:
            get_ask(stock_info)
        except KeyError:
            st.error("Ask not available")
        try:
            get_target_price(stock_info)
        except KeyError:
            st.error("Target price not available")

def stock_price_chart(stock_name, selected_period):
    def line_chart(stock_name, selected_period):
        stock_data = get_stock_data(stock_name, selected_period)

        stock_data = stock_data["Close"].apply(lambda x: round(x, 2))

        fig = px.line(stock_data, x=stock_data.index, y="Close")
        fig.update_layout(width=3*1200)

        fig.update_yaxes(title="Stock Price", tickprefix="$", ticksuffix="", tickformat=",")

        fig.update_traces(line_color="blue", selector=dict(type="scatter", mode="lines"))

        st.plotly_chart(fig, use_container_width=True)
    
    def candlestick_chart(stock_name, selected_period):
        stock_data = get_stock_data(stock_name, selected_period)
        
        fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                             open=round(stock_data['Open'], 2),
                                             high=round(stock_data['High'], 2),
                                             low=round(stock_data['Low'], 2),
                                             close=round(stock_data['Close'], 2))])
        
        fig.update_layout(width=3*1200)
        
        fig.update_yaxes(title = "Stock Price", tickprefix="$", ticksuffix="", tickformat=",.")
        
        st.plotly_chart(fig, use_container_width=True)
    
    def ohlc_chart(stock_name, selected_period):
        stock_data = get_stock_data(stock_name, selected_period)
        
        fig = go.Figure(data=[go.Ohlc(x=stock_data.index,
                                      open=round(stock_data['Open'], 2),
                                      high=round(stock_data['High'], 2),
                                      low=round(stock_data['Low'], 2),
                                      close=round(stock_data['Close'], 2))])
        
        fig.update_layout(width=3*1200)
        
        fig.update_yaxes(title = "Stock Price", tickprefix="$", ticksuffix="", tickformat=",.")
        
        st.plotly_chart(fig, use_container_width=True)
    
    def select_chart_type():
        chart_type = st.selectbox(
            "Select chart type",
            ["Line Chart", "Candlestick Chart", "OHLC Chart"],
            key='chart_type_radio',
        )
        
        return chart_type
    
    chart_dict = {
        "Line Chart": line_chart,
        "Candlestick Chart": candlestick_chart,
        "OHLC Chart": ohlc_chart,
    }
    
    st.write(" ")
    
    _, col1, _ = st.columns(3)
    with col1: 
        chart_type = select_chart_type()
    
    st.write(" ")
    _, col2 = st.columns([4, 8])
    with col2:
        st.title("Stock Price Over time")
    
    chart_dict[chart_type](stock_name, selected_period)

def period_selection():
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        period_selected = st.selectbox("Select forecasted period...",
                options=CONFIG["period_options"],
                index=None,
                placeholder="Select a period",
                key="period_select",
                help="Select the time period for the forecast"
        )
    
    return period_selected

def stock_page():
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
    
    selected_period = period_selection()
            
    st.write(" ")
    
    stock_intel(stock, selected_period) 
                             
    stock_price_chart(stock, selected_period)