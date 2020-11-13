import requests
from bs4 import BeautifulSoup
import time
from random import random
from fake_useragent import UserAgent
import re
import pandas as pd


def get_data(url):
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
    lk = soup.findAll('a', attrs={'class': "listing_item_button cta_button"})
    names = []
    prices = []
    links = []
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

        for link in lk:
            if link is not None:
                links.append("https://trovaprezzi.it" + link.attrs['href'])
            else:
                prices.append("unknown-link")

    df = pd.DataFrame({'name': names, 'price': prices, 'link': links})
    return df


def print_data_ordered(df, url):
    df = df.sort_values(by=['price'])
    text = f"This is the list of the first 3 prices of {url} \n\n"
    for index, product in df.head(3).iterrows():
        text = text + f"Product name: {product['name']} \nTotal price: {product['price']} € \nLink: {product['link'] } \n\n"
        if index == 2:
            break
    return text

