import streamlit as st

def page_settings():
    st.set_page_config(
    page_title="Stock Dashboard", 
    page_icon=":chart_with_upwards_trend", 
    layout="wide")

def menu():
    st.sidebar.title("Navigation")

    st.sidebar.page_link("app.py",
                         label = "Stock Overall",
                         icon="📈")
    
    st.sidebar.page_link("./pages/forecasting_comp.py",
                        label = "Stock Forecast",
                        icon="🔮")
    
    st.sidebar.page_link("./pages/data.py",
                        label = "Stock Data",
                        icon="📊")