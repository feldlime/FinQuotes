from flask import Response, Blueprint

from project.http import ok, server_error, bad_request
from project.services import (
    smart_lab_quote,
    bcs_quote,
    TickerNotFoundError,
    PriceNotFoundError,
)

bp = Blueprint('api', __name__)


@bp.route('/ping', methods=('GET',))
def ping() -> Response:
    return ok(message='pong')


@bp.route('/quote/<string:ticker>', methods=('GET',))
def quote(ticker: str) -> Response:
    try:
        # price = smart_lab_quote(code)
        price = bcs_quote(ticker)
        return ok(data={'price': price})
    except TickerNotFoundError as e:
        return bad_request(message=f'Ticker not found: {e!r}')
    except PriceNotFoundError as e:
        return server_error(message=f'Price cannot be found: {e!r}')
    except Exception as e:
        return server_error(message=f'Some problems while getting price: {e!r}')
