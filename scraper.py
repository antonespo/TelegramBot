import requests
from bs4 import BeautifulSoup
import time
from random import random
from fake_useragent import UserAgent
import re


def get_data(url):
    time.sleep(random() * 3)
    ua = UserAgent()
    headers = {"User-Agent": ua.random,
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
               "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    content = r.content
    soup = BeautifulSoup(content, 'html.parser')
    ps = soup.findAll('div', attrs={'class': 'item_total_price'})
    ns = soup.findAll('a', attrs={'class': 'item_name no_desc'})
    names = []
    prices = []
    if ps is not None and ns is not None:
        for name in ns:
            if name is not None:
                names.append(name.text.strip())
            else:
                names.append("unknown-product")
        for price in ps:
            if price is not None:
                prices.append(re.findall(r'\d+,\d+', price.text.strip())[0])
            else:
                prices.append("unknown-price")
    text = '''This is the list of the first 3 prices of %s 

    ''' % (url)
    for index, name in enumerate(names):
        text = text + '''
<b>Product name</b>: %s
<b>Total price</b>: %s €
        ''' % (names[index], prices[index] )
        if index == 2:
            break
    return text