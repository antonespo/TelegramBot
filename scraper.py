import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
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
    prices = soup.findAll('div', attrs={'class': 'item_total_price'})
    names = soup.findAll('a', attrs={'class': 'item_name no_desc'})
    links = soup.findAll('a', attrs={'class': "listing_item_button cta_button"})
    if prices is not None and names is not None and links is not None:
        df = pd.DataFrame({'name': names, 'price': prices, 'link': links})
        for index, product in df.iterrows():
            product['name'] = product['name'].text.strip()
            product['price'] = re.findall(r'\d+,\d+', product['price'].text.strip())[0]
            product['link'] = ("https://trovaprezzi.it" + product['link'].attrs['href'])
    return df


def print_data_ordered(df, url):
    df = df.sort_values(by=['price'])
    text = f"This is the list of the first 3 prices of {url} \n\n"
    for index, product in df.head(3).iterrows():
        text = text + f"Product name: {product['name']} \nTotal price: {product['price']} € \nLink: {product['link'] } \n\n"
        if index == 2:
            break
    return text

