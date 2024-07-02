# smart_scraping.py
import yfinance as yf
import requests_cache

def enable_debug_mode():
    yf.enable_debug_mode()

def configure_requests_cache(cache_file, user_agent):
    session = requests_cache.CachedSession(cache_file)
    session.headers['User-agent'] = user_agent
    return session