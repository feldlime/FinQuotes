import requests

from project.exceptions import TickerNotFoundError

BASE_URL = 'https://financialmodelingprep.com/api/v3/company/profile'
PRICE_FIELD = 'price'


def make_url(ticker: str) -> str:
    return f'{BASE_URL}/{ticker}'


def fetch(ticker: str) -> dict:
    url = make_url(ticker)
    resp = requests.get(url)
    json = resp.json()
    return json


def quote(ticker: str) -> float:
    json = fetch(ticker)
    try:
        price = json[PRICE_FIELD]
    except KeyError:
        raise TickerNotFoundError()
    return price
