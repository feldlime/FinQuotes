import bs4 as bs
from lxml import etree
import requests

from project.exceptions import TickerNotFoundError

BASE_URL = 'https://smart-lab.ru'
SEARCH_URL = f'{BASE_URL}/q/ajax-stocks-search'


__all__ = (
    'SmartLabError',
    'quote',
)


class SmartLabError(Exception):
    pass


def request_variants(ticker: str) -> list:
    url = SEARCH_URL
    data = {
        'json': '1',
        'value': ticker
    }
    resp = requests.post(url, data)
    res = resp.json()

    if res['bStateError']:
        raise SmartLabError(res)

    return res['results']


def get_url(ticker: str) -> str:
    ticker = ticker.lower()
    variants = request_variants(ticker)

    if len(variants) == 0:
        raise TickerNotFoundError('No variants for ticker')
    elif len(variants) == 1:
        res = variants[0]
    else:
        filtered = list(
            filter(
                lambda d: d['value'].lower().count(f'[{ticker}]') == 1,
                variants,
            )
        )
        if len(filtered) == 0:
            raise TickerNotFoundError('No variants after filtering')
        elif len(filtered) == 1:
            res = filtered[0]
        else:
            raise TickerNotFoundError('More than one variant after filtering')

    url_end = res['data']
    base_url = BASE_URL
    url = f'{base_url}{url_end}'
    return url


def get_price_forum(html: str) -> float:
    htmlparser = etree.HTMLParser()
    tree = etree.fromstring(html, htmlparser)

    price_xpath = '/html/body/div[2]/div[2]/div[2]/div/span/i'
    price_elems = tree.xpath(price_xpath)
    if len(price_elems) != 1:
        raise SmartLabError(f'len(price_elems) = {len(price_elems)}')
    price_elem = price_elems[0]
    full_price = price_elem.text
    pure_price = full_price.replace('$', '').replace('₽', '')
    price = float(pure_price)
    return price


def get_price_bounds(html: str) -> float:
    soup = bs.BeautifulSoup(html, 'html5lib')
    table = soup.find(
        'table',
        attrs={'class': 'simple-little-table bond'},
    )

    nominal = None
    price_to_nominal = None
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        if len(cells) != 2:
            continue

        field, value = cells
        field = field.find('abbr').text
        value = value.text

        if field == 'Номинал':
            nominal = float(value)
        elif field == 'Цена послед':
            price_to_nominal = float(value) / 100

    if price_to_nominal is None or nominal is None:
        raise SmartLabError(f'nominal: {nominal}, price_to_nominal: {price_to_nominal}')
    price = nominal * price_to_nominal
    return price


def get_price(url: str) -> float:
    resp = requests.get(url)

    if resp.status_code != 200:
        raise SmartLabError(f'resp.status_code = {resp.status_code}')

    html = resp.text
    if '/forum/' in url:
        price = get_price_forum(html)
    elif 'q/bonds/' in url:
        price = get_price_bounds(html)
    else:
        raise SmartLabError(f'Unexpected url: {url}')

    return price


def quote(ticker: str) -> float:
    link = get_url(ticker)
    price = get_price(link)
    return price
