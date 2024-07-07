import streamlit as st

from tasks.menu import (
    menu
)
menu()

def data_page():
    st.write("Stock Data")