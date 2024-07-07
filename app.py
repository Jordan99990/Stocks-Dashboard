from pages.stock_screener import stock_page
import streamlit as st

from tasks.menu import (
    page_settings
)

page_settings()

def main():
    stock_page()

if __name__ == "__main__":
    main()