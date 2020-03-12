import re

import requests
from lxml import etree

from .exceptions import TickerNotFoundError, PriceNotFoundError

BASE_URL = 'https://bcs-express.ru/kotirovki-i-grafiki'

__all__ = (
    'quote',
)


def get_url(ticker: str) -> str:
    return f'{BASE_URL}/{ticker}'


def load_html(ticker: str) -> str:
    url = get_url(ticker)
    r = requests.get(url)

    if r.status_code >= 400:
        raise TickerNotFoundError(
            f'Cannot find ticker page, status_code = {r.status_code}'
        )

    return r.text


def extract_price(html: str) -> float:
    htmlparser = etree.HTMLParser()
    tree = etree.fromstring(html, htmlparser)
    price_xpath = '/html/body/div[1]/section/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]'
    price_elems = tree.xpath(price_xpath)

    if len(price_elems) != 1:
        raise PriceNotFoundError(f'len(price_elems) = {len(price_elems)}')

    price_elem = price_elems[0]
    price = price_elem.text
    clear_price = re.sub(r'[^0-9,]', '', price)
    return float(clear_price.replace(',', '.'))


def quote(ticker: str) -> float:
    html = load_html(ticker)
    price = extract_price(html)
    return price
