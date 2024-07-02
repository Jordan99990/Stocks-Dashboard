# custom_logger.py
import logging
import yfinance as yf

def configure_logger():
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(yf.__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger