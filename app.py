import streamlit as st
from pages.stock_screener import stock_page
from pages.forecasting_comp import forecasting_page
from pages.data import data_page

def page_settings():
    st.set_page_config(
        page_title="Stock Market Analysis",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
def menu():
    st.sidebar.title("Navigation")
    pages = {
        "📈 Stock Screener": stock_page,
        "🔮 Forecasting": forecasting_page,
        "📊 Data": data_page
    }
    page = st.sidebar.selectbox("Choose a page:", list(pages.keys()))

    pages[page]()

if __name__ == "__main__":
    page_settings()
    menu()