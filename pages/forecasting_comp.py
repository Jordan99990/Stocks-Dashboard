import streamlit as st
import pandas as pd
from tasks.stock_dict_fetcher import get_stock_symbols
from tasks.stock_data import get_stock_data
from tasks.forecasting.sarimax import forecast_stock_sarimax
from tasks.forecasting.arima import forecast_stock_arima
from tasks.forecasting.random_forest import forecast_stock_random_forest
from tasks.forecasting.linear_regression import forecast_stock_linear_regression
from tasks.forecasting.svr import forecast_stock_svr
import plotly.express as px

CONFIG = {
    "period_options": ['3d', '1w', '2w', '2mo', '3mo'],
    "data_timeframes": {
        "SARIMA": "2y",
        "ARIMA": "2y",
        "Linear Regression": "1mo",
        "Random Forest": "6mo",
        "SVR": "6mo",
    },
}

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

def forecasting_chart(stock, period_selected, title_placeholder):
    def period_to_days(period):
        if period.endswith('d'):
            return int(period[0])
        elif period.endswith('w'):
            return int(period[0]) * 7
        elif period.endswith('mo'):
            return int(period[0]) * 30  

    if period_selected is None:
        st.error("Please select a period")
        return
    
    _, col2 = st.columns([4, 8])
    with col2:
        with st.spinner('Loading Forecasting'):
            combined_forecast_df = pd.DataFrame({
                "SARIMA": forecast_stock_sarimax(get_stock_data(stock, CONFIG["data_timeframes"]["SARIMA"]))['Forecasted Close'],
                "ARIMA": forecast_stock_arima(get_stock_data(stock, CONFIG["data_timeframes"]["ARIMA"]))['Forecasted Close'],
                "Linear Regression": forecast_stock_linear_regression(get_stock_data(stock, CONFIG["data_timeframes"]["Linear Regression"]))['Forecasted Close'],
                "Random Forest": forecast_stock_random_forest(get_stock_data(stock, CONFIG["data_timeframes"]["Random Forest"]))['Forecasted Close'],
                "SVR": forecast_stock_svr(get_stock_data(stock, CONFIG["data_timeframes"]["SVR"]))['Forecasted Close']
            })
    
    days_to_show = period_to_days(period_selected)
    filtered_combined_forecast_df = combined_forecast_df.head(days_to_show)

    title_placeholder.title("Stock Price Forecast")
    
    fig = px.line(filtered_combined_forecast_df)
    fig.update_layout(
        yaxis_tickprefix='$', 
        yaxis_tickformat=',.2f', 
        xaxis_title="Date", 
        yaxis_title="Price (USD)",
        legend=dict(orientation = "h", yanchor="bottom",y=-0.4,xanchor="left", x=0)
    )

    st.plotly_chart(fig, use_container_width=True)  

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

def title_placeholder():
    _, col2 = st.columns([4, 8])
    with col2:
        title_placeholder = st.empty()
    return title_placeholder

def forecasting_page():
    _, col2 = st.columns([4, 8])
    with col2:
        title_placehold = st.empty()
    
    if 'stock' not in st.session_state:
        st.session_state.stock = None
        
    stock = select_stock()
    
    if not stock:
        return
    
    st.session_state.stock = stock
    
    title_placehold.title(f'{list(stock_options.keys())[list(stock_options.values()).index(stock)]} ({stock})')
    
    st.write(" ")
    
    period_seclected = period_selection()
    
    st.write("")
    
    title_placehold = title_placeholder()
    
    forecasting_chart(stock, period_seclected, title_placehold)
    
    st.write(" ")