import aiohttp

from project.exceptions import GettingQuoteError


def make_url(engine: str, market: str, ticker: str) -> str:
    base = 'https://iss.moex.com/iss'
    return f'{base}/engines/{engine}/markets/{market}/securities/{ticker}.json'


async def fetch(
        session: aiohttp.ClientSession,
        engine: str,
        market: str,
        ticker: str,
) -> dict:
    url = make_url(engine, market, ticker)
    async with session.get(url) as resp:
        json = await resp.json()
        return json


async def share_quote(session: aiohttp.ClientSession, ticker: str) -> float:
    data = await fetch(session, 'stock', 'shares', ticker)
    price_data = data['marketdata']['data']
    price_data = list(filter(lambda l: l[1] in ('TQBR', 'TQTF'), price_data))

    if not price_data:
        raise GettingQuoteError()

    price = price_data[0][12]
    return float(price)


async def bound_quote(session: aiohttp.ClientSession, ticker: str) -> float:
    data = await fetch(session, 'stock', 'bonds', ticker)
    price_data = data['marketdata']['data']

    if not price_data:
        raise GettingQuoteError()

    price = price_data[0][11]
    return float(price)

