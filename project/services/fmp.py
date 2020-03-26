import aiohttp

from project.exceptions import TickerNotFoundError

BASE_URL = 'https://financialmodelingprep.com/api/v3/company/profile'


def make_url(ticker: str) -> str:
    return f'{BASE_URL}/{ticker}'


async def fetch(session: aiohttp.ClientSession, ticker: str) -> dict:
    url = make_url(ticker)
    async with session.get(url) as resp:
        json = await resp.json()
        return json


async def quote(session: aiohttp.ClientSession, ticker: str) -> float:
    json = await fetch(session, ticker)
    try:
        price = json['profile']['price']
    except KeyError:
        raise TickerNotFoundError()
    return price
