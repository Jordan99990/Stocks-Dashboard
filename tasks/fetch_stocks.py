from bs4 import BeautifulSoup
import requests

def fetch_html(url, headers):
    response = requests.get(url, headers=headers)
    return response.content

def parse_stocks(html):
    soup = BeautifulSoup(html, 'html.parser')
    tbody = soup.find('tbody')
    stock_symbols = {}
    
    for tr in tbody.find_all('tr'):
        key, value = None, None
        for td in tr.find_all('td'):
            a_tag = td.find('a', href=True)
            if a_tag:
                if not key:
                    key = a_tag.text
                else:
                    value = a_tag.text
                    break
        if key and value:  
            stock_symbols[key] = value
    
    return stock_symbols

def get_stock_symbols():
    url = 'https://www.slickcharts.com/sp500'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    html = fetch_html(url, headers)
    stock_symbols = parse_stocks(html)
    return stock_symbols