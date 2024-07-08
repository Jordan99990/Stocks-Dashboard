import datetime
import streamlit as st
from tasks.stock_data import (
    get_stock_data
)
from tasks.stock_dict_fetcher import get_stock_symbols

type Symbol = str
type Period = str

CONFIG = {
    "data_period_options" : ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
}

today = datetime.date.today()
first_day_of_year = datetime.date(today.year, 1, 1)
ytd_days = (today - first_day_of_year).days + 1
stock_df = lambda stock, x: get_stock_data(stock, x)
period_to_days = {
    '1d': 1,
    '5d': 5,
    '1mo': 30,
    '3mo': 90,
    '6mo': 180,
    '1y': 365,
    '2y': 730,
    '5y': 1825,
    '10y': 3650,
    'ytd': ytd_days
}

def select_stock() -> Symbol | None:
    global stock_options, option
    global min_price, max_price, stock_data
    
    stock_options = get_stock_symbols()
    
    option = st.selectbox("Select a stock...",
                options=list(stock_options.keys()),
                index=None,
                placeholder="Select a stock",
                label_visibility="hidden",
                help="Select the stock",
    )
    
    try:
        stock_data = stock_df(stock_options.get(option), 'max')
        period_to_days.update({'max': len(stock_data) - 1})
        
        min_price = stock_data['Close'].tail(5).min()
        max_price = stock_data['Close'].tail(5).max()
        
        st.session_state['min_price'] = min_price
        st.session_state['max_price'] = max_price
    except:
        st.error("Select a stock!")
        
    symbol = stock_options.get(option)
    return symbol

def period_selection() -> Period:
    global min_price, max_price
        
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        period_selected = st.selectbox("Select period...",
                options=CONFIG["data_period_options"],
                index=None,
                placeholder="Select a period",
                key="period_select",
                help="Select the time period"
        )
    
    try:
        days = period_to_days.get(period_selected)
            
        min_price = stock_data['Close'].tail(days).min()
        max_price = stock_data['Close'].tail(days).max()
        
        st.session_state['min_price'] = min_price
        st.session_state['max_price'] = max_price
    except:
        pass
    
    return period_selected
    
        
def date_range_picker() -> tuple[datetime.date, datetime.date]:
    _, col2, _ = st.columns([1, 2, 1])  
    with col2:
        date_range = st.date_input(
            "Select date range",
            value = (
                datetime.date(2020, 1, 1),
                datetime.date.today()
            ),
            min_value=datetime.date(2020, 1, 1),
            max_value=datetime.date.today(),
            key='_date_range'
        )
    
    return date_range

def table_stock_info() -> None:
    days = period_to_days.get(st.session_state['period_selected'])
    
    try:
        filtered_data = stock_data.tail(days)
    except:
        filtered_data = stock_data.tail(5)
    
    try:
        price_range = st.session_state['min_price'], st.session_state['max_price']
        filtered_data = filtered_data[(filtered_data['Close'] >= price_range[0]) & (filtered_data['Close'] <= price_range[1])]
    except:
        pass
    
    try:
        date_range = st.session_state['date_range']
        filtered_data = filtered_data[(filtered_data.index.date >= date_range[0]) & (filtered_data.index.date <= date_range[1])]
    except:
        if not date_range and st.session_state['period_selected'] is not None:
            filtered_data = stock_data.tail(days)
            st.session_state['min_price'] = filtered_data['Close'].min()
            st.session_state['max_price'] = filtered_data['Close'].max() 
        pass
    
    try:
        st.session_state['table'] = st.dataframe(filtered_data, width=2800)
    except:
        st.session_state['table'] = st.dataframe(stock_data.tail(5), width=2800)

    
def setup() -> None:
    def title_setup() -> None:
        _, col2 = st.columns([4, 8])
        with col2:
            st.session_state['title_placeholder'] = st.empty()
    
    def session_setup() -> None:
        if 'stock' not in st.session_state:
            st.session_state['stock'] = None
    
        if 'period_selected' not in st.session_state:
            st.session_state['period_selected'] = None
            
        if 'title_placeholder' not in st.session_state:
            st.session_state['title_placeholder'] = None
            
        if 'min_price' not in st.session_state:
            st.session_state['min_price'] = None
        
        if 'max_price' not in st.session_state:
            st.session_state['max_price'] = None
            
        if 'data_range' not in st.session_state:
            st.session_state['date_range'] = None
            
        if 'table' not in st.session_state:
            st.session_state['table'] = None
            
    session_setup()
    title_setup()

def price_slider() -> tuple[float, float]:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        slider = st.slider("Select price range",
                  min_value= st.session_state['min_price'],
                  value=(
                      st.session_state['min_price'],
                      st.session_state['max_price']
                      ),
                  step=0.1,
                  format="%.1f",
                  key="price_range",
                  help="Select the price range"
        )
    
    st.session_state['min_price'] = slider[0]
    st.session_state['max_price'] = slider[1]


def data_page():
    setup()
    
    st.session_state['stock'] = select_stock()
    
    if st.session_state['stock'] is not None:
        st.session_state['title_placeholder'].title(f'{list(stock_options.keys())[list(stock_options.values()).index(st.session_state['stock'])]} ({st.session_state['stock']}) Data')
    
    st.write(" ")
    if st.session_state['stock'] is not None:
        st.session_state['period_selected'] = period_selection()
        
    st.write(" ")
    if st.session_state['stock'] is not None:
        price_slider()
    
    st.write(" ")
    if st.session_state['stock'] is not None:
        st.session_state['date_range'] = date_range_picker()
    
    st.write(" ")
    if st.session_state['stock'] is not None:
        table_stock_info()