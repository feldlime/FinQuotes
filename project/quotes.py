from typing import Callable, Optional

import attr

from .exceptions import GettingQuoteError
from .services import (
    moex_bound_quote,
    moex_share_quote,
    bcs_quote,
)


@attr.s(slots=True, frozen=True)
class Quote:
    price: float = attr.ib()
    source: str = attr.ib()


def get_quote_with_method(
        method: Callable[[str], float],
        source_name: str,
        ticker: str,
) -> Optional[Quote]:
    try:
        price = method(ticker)
    except GettingQuoteError:
        return None

    return Quote(price, source_name)


def get_quote(ticker: str) -> Quote:
    methods = [
        (moex_share_quote, 'moex_share'),
        (moex_bound_quote, 'moex_bound'),
        (bcs_quote, 'bcs'),
    ]

    for method in methods:
        quote = get_quote_with_method(method[0], method[1], ticker)
        if quote is not None:
            return quote

    raise GettingQuoteError('No quote was found')
