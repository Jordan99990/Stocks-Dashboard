import yfinance as yf
from tasks.limiter.rate_limiter import configure_cached_limiter_session
from tasks.limiter.smart_scraping import (
    # enable_debug_mode, 
    configure_requests_cache
)

session = configure_requests_cache("yfinance.cache", "my-program/1.0")
limiter_session = configure_cached_limiter_session(2, 5, "yfinance.cache")

def get_stock_data(stock: str):
    info = yf.Ticker(stock).history(period='1mo')
    return info