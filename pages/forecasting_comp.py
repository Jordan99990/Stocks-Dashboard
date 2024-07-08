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

def select_stock() -> str:
    global stock_options, option
    stock_options = get_stock_symbols()
    
    option = st.selectbox("Select a stock...",
                options=list(stock_options.keys()),
                index=None,
                placeholder="Select a stock",
                label_visibility="hidden",
    )
    
    return stock_options.get(option)

def forecasting_chart(stock: str, period_selected: str, title_placeholder: str) -> None:
    def period_to_days(period: str) -> int:
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

def period_selection() -> str:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        period_selected = st.selectbox("Select forecasted period...",
                options=CONFIG["period_options"],
                index=None,
                placeholder="Select a period",
                key="period_select_",
                help="Select the time period for the forecast"
        )
    
    return period_selected

def title_placeholder() -> str:
    _, col2 = st.columns([4, 8])
    with col2:
        title_placeholder = st.empty()
    
    st.session_state['title_placeholder_'] = title_placeholder
    
    return title_placeholder

def setup() -> None:
    def title_setup() -> None:
        _, col2 = st.columns([4, 8])
        with col2:
            st.session_state['title_placeholder_'] = st.empty()
    
    def session_setup() -> None:
        if 'stock_' not in st.session_state:
            st.session_state['stock_'] = None
    
        if 'period_selected_' not in st.session_state:
            st.session_state['period_selected_'] = None
            
        if 'title_placeholder_' not in st.session_state:
            st.session_state['title_placeholder_'] = None
            
    session_setup()
    title_setup()

def forecasting_page():
    setup()
    
    st.session_state['stock_'] = select_stock()
    
    if st.session_state['stock_'] is not None:
        st.session_state['title_placeholder_'].title(f'{list(stock_options.keys())[list(stock_options.values()).index(st.session_state['stock_'])]} ({st.session_state['stock_']}) Data')
    
    st.write(" ")
    if st.session_state['stock_'] is not None:
        st.session_state['period_selected_'] = period_selection()
    
    st.write("")
    if st.session_state['stock_'] is not None:
        st.session_state['title_placeholder_'] = title_placeholder()
    
    st.write(" ")
    if st.session_state['stock_'] is not None:
        stock = st.session_state['stock_']
        period_seclected = st.session_state['period_selected_']
        title_placehold = st.session_state['title_placeholder_']   
        forecasting_chart(stock, period_seclected, title_placehold)
    
    st.write(" ")