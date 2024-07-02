import yfinance as yf
from tasks.limiter.rate_limiter import configure_cached_limiter_session
from tasks.limiter.smart_scraping import (
    # enable_debug_mode, 
    configure_requests_cache
)

session = configure_requests_cache("yfinance.cache", "my-program/1.0")
limiter_session = configure_cached_limiter_session(2, 5, "yfinance.cache")

def get_stock_data(stock: str, period):
    info = yf.Ticker(stock).history(period=period)
    return info

def get_current_price(stock: str):
    return yf.Ticker(stock).history(period="1d").iloc[-1]["Close"]