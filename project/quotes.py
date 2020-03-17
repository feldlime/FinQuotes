import attr

from .services import (
    moex_bound_quote,
    moex_share_quote,
    bcs_quote,
)


@attr.s(slots=True, frozen=True)
class Quote:
    price: float = attr.ib()
    source: str = attr.ib()


def get_quote(code: str) -> Quote:
    price = moex_bound_quote(code)
    if price is not None:
        return Quote(price, 'moex_bound')

    price = moex_share_quote(code)
    if price is not None:
        return Quote(price, 'moex_share')

    price = bcs_quote(code)
    return Quote(price, 'bcs')
