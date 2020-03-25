import requests

from project.exceptions import GettingQuoteError


def fetch(engine: str, market: str, code: str) -> requests.Response:
    base_url = 'https://iss.moex.com/iss'
    url = f'{base_url}/engines/{engine}/markets/{market}/securities/{code}.json'
    resp = requests.get(url)
    return resp


def get_price_data(engine: str, market: str, code: str) -> dict:
    resp = fetch(engine, market, code)
    json = resp.json()
    data = json['marketdata']['data']
    return data


def share_quote(code: str) -> float:
    price_data = get_price_data('stock', 'shares', code)
    price_data = list(filter(lambda l: l[1] in ('TQBR', 'TQTF'), price_data))

    if not price_data:
        raise GettingQuoteError()

    price = price_data[0][12]
    return float(price)


def bound_quote(code: str) -> float:
    price_data = get_price_data('stock', 'bonds', code)

    if not price_data:
        raise GettingQuoteError()

    price = price_data[0][11]
    return float(price)

