import streamlit as st
import pandas as pd
from tasks.menu import menu
from tasks.stock_dict_fetcher import get_stock_symbols
from tasks.stock_data import get_stock_data
from tasks.forecasting.sarimax import forecast_stock_sarimax
from tasks.forecasting.arima import forecast_stock_arima
from tasks.forecasting.random_forest import forecast_stock_random_forest

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
    
    data = get_stock_data(stock, "1y")
    
    _, col2 = st.columns([4, 8])
    with col2:
        with st.spinner('Loading Forecasting'):
            forecast_df_sarima = forecast_stock_sarimax(data)
            forecast_df_arima = forecast_stock_arima(data)
            # forecast_df_random_forest = forecast_stock_random_forest(get_stock_data(stock, "3mo"))
            
            forecast_df_sarima.index = forecast_df_arima.index
            combined_forecast_df = pd.DataFrame({
                "SARIMA": forecast_df_sarima['Forecasted Close'],
                "ARIMA": forecast_df_arima['Forecasted Close']
                # "Random Forest": forecast_df_random_forest['Forecasted Close']
            })
    
    days_to_show = period_to_days(period_selected)
    filtered_combined_forecast_df = combined_forecast_df.head(days_to_show)

    title_placeholder.title("Sarima vs Arima vs XGboost vs PyTorch NN")
    st.line_chart(filtered_combined_forecast_df)

def forecasting_page():
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
    
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        period_selected = st.selectbox("Select forecasted period...",
                options=['3d', '1w', '2w', '2mo', '3mo'],
                index=None,
                placeholder="Select a period",
                key="period_select",
                help="Select the time period for the forecast"
        )

    st.write("")
    
    _, col2 = st.columns([2, 8])
    with col2:
        title_placeholder = st.empty()
    
    forecasting_chart(stock, period_selected, title_placeholder)
    
    st.write(" ")

forecasting_page()