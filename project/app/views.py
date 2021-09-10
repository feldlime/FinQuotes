from datetime import datetime

from aiohttp import hdrs, web
import attr

from project.exceptions import (
    TickerNotFoundError,
    PriceNotFoundError,
    GettingQuoteError,
)
from project.http import ok, server_error, bad_request
from project.quotes import get_quote

from .schemas import TickerSchema

__all__ = (
    'ROUTES',
)


async def ping(_: web.Request) -> web.Response:
    return ok(message='pong')


async def time(_: web.Request) -> web.Response:
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    return ok(data={'time': now_str})


async def quote(request: web.Request) -> web.Response:
    ticker = TickerSchema().load(request.match_info).pop('ticker')
    try:
        quote_ = await get_quote(ticker)
        return ok(data=attr.asdict(quote_))
    except TickerNotFoundError as e:
        return bad_request(message=f'Ticker not found: {e!r}')
    except PriceNotFoundError as e:
        return server_error(message=f'Price cannot be found: {e!r}')
    except GettingQuoteError as e:
        return server_error(message=f'Quote cannot be found: {e!r}')
    except Exception as e:
        return server_error(message=f'Some internal problems: {e!r}')


ROUTES = (
    web.route(hdrs.METH_ANY, '/api/ping', ping, name='ping'),
    web.route(hdrs.METH_ANY, '/api/time', time, name='time'),
    web.route(hdrs.METH_GET, '/api/quote/{ticker}', quote, name='quote'),
)
