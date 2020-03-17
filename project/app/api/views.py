from datetime import datetime

from flask import Response, Blueprint
import attr

from project.exceptions import (
    TickerNotFoundError,
    PriceNotFoundError,
)
from project.http import ok, server_error, bad_request
from project.quotes import get_quote


bp = Blueprint('api', __name__)


@bp.route('/ping', methods=('GET',))
def ping() -> Response:
    return ok(message='pong')


@bp.route('/quote/<string:ticker>', methods=('GET',))
def quote(ticker: str) -> Response:
    try:
        quote_ = get_quote(ticker)
        return ok(data=attr.asdict(quote_))
    except TickerNotFoundError as e:
        return bad_request(message=f'Ticker not found: {e!r}')
    except PriceNotFoundError as e:
        return server_error(message=f'Price cannot be found: {e!r}')
    except Exception as e:
        return server_error(message=f'Some problems while getting price: {e!r}')


@bp.route('/time', methods=('GET',))
def time() -> Response:
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    return ok(data={'time': now_str})
