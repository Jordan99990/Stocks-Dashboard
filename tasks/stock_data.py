import yfinance as yf
from tasks.limiter.rate_limiter import configure_cached_limiter_session
from tasks.limiter.smart_scraping import (
    # enable_debug_mode, 
    configure_requests_cache
)

session = configure_requests_cache("yfinance.cache", "my-program/1.0")
limiter_session = configure_cached_limiter_session(2, 5, "yfinance.cache")

def get_stock_data(stock: str, selected_period):
    info = yf.Ticker(stock).history(period=selected_period)
    return info

def get_stock_info(stock: str) -> dict:
    return yf.Ticker(stock).info

def get_current_price(stock: str):
    return yf.Ticker(stock).history(period="1d").iloc[-1]["Close"]

def stock_company_info(stock: str, selected_period: str):
    stock_data = yf.Ticker(stock).history(period=selected_period)

    current_price = stock_data.iloc[-1]["Close"]
    previous_closed = stock_data.iloc[0]["Close"] if len(stock_data) > 1 else current_price
    
    price_difference = current_price - previous_closed
    percentage_change = (price_difference / previous_closed) * 100 if previous_closed != 0 else 0
    
    price_diff_str = f'+${price_difference:.2f}' if price_difference >= 0 else f'{price_difference:.2f}'
    percentage_change_str = f'(+{percentage_change:.2f}%)' if percentage_change >= 0 else f'({percentage_change:.2f}%)'
    
    return current_price, f'{price_diff_str} {percentage_change_str}'