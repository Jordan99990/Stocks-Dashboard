import streamlit as st
from tasks.stock_dict_fetcher import get_stock_symbols

def page_settings():
    st.set_page_config(
    page_title="Stock Dashboard", 
    page_icon=":chart_with_upwards_trend", 
    layout="wide")

def select_stock():
    stock_options = get_stock_symbols()

    option = st.selectbox("Select a stock...",
                options=list(stock_options.keys()),
                index=None,
                placeholder="Select a stock",
                label_visibility="hidden",
    )
    
    return stock_options.get(option)
        
def main():
    page_settings()
    stock = select_stock()
    
    if not stock:
        return

    from tasks.stock_data import get_stock_data
    
    # try:
    #     stock = get_stock_data(stock)
    #     print(stock)
    #     st.vega_lite_chart(stock)
    # except Exception as e:
    #     pass
   
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Stock Symbol", value="symbol")
        # st.write("Stock Symbol")
        # st.write("symbol")
    
    with col2:
        st.write("Stock Name")
        st.write("name")
    
    with col3:
        st.write("Stock Price")
        st.write("price")

if __name__ == "__main__":
    main()