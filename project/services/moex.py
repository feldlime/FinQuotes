from typing import Optional

import requests


def fetch(engine: str, market: str, code: str) -> requests.Response:
    base_url = 'https://iss.moex.com/iss'
    url = f'{base_url}/engines/{engine}/markets/{market}/securities/{code}.json'
    resp = requests.get(url)
    return resp


def quote(engine: str, market: str, code: str) -> Optional[float]:
    resp = fetch(engine, market, code)
    json = resp.json()
    data = json['marketdata']['data']
    price_data = list(filter(lambda l: l[1] in ('TQBR', 'TQTF'), data))

    if not price_data:
        return None

    price_str = price_data[0][12]
    price = float(price_str)

    return price


def share_quote(code: str) -> Optional[float]:
    return quote('stock', 'shares', code)


def bound_quote(code: str) -> Optional[float]:
    return quote('stock', 'bound', code)
