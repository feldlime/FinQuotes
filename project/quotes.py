import asyncio
from typing import Callable, Optional

import aiohttp
import attr

from .exceptions import GettingQuoteError
from .services import (
    moex_bound_quote,
    moex_share_quote,
    bcs_quote,
    fmp_quote,
)


@attr.s(slots=True, frozen=True)
class Quote:
    price: float = attr.ib()
    source: str = attr.ib()


async def fetch(
        session: aiohttp.ClientSession,
        method: Callable[[aiohttp.ClientSession, str], float],
        source_name: str,
        ticker: str,
) -> Optional[Quote]:
    try:
        price = await method(session, ticker)
    except GettingQuoteError:
        return None

    return Quote(price, source_name)


async def get_quote(ticker: str) -> Quote:
    methods = [
        (bcs_quote, 'bcs'),
        (fmp_quote, 'fmp'),
        (moex_share_quote, 'moex_share'),
        (moex_bound_quote, 'moex_bound'),

    ]

    tasks = []
    async with aiohttp.ClientSession() as session:
        for method_desc in methods:
            method, method_name = method_desc
            coroutine = fetch(session, method, method_name, ticker)
            task = asyncio.create_task(coroutine)
            tasks.append(task)

        for future in asyncio.as_completed(tasks):
            quote = await future
            if quote is not None:
                return quote

    raise GettingQuoteError('No quote was found')
