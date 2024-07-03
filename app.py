import streamlit as st
from pages.stock_screener import first_page

from tasks.menu import (
    page_settings,
)

def main():
    first_page()

if __name__ == "__main__":
    page_settings()
    main()