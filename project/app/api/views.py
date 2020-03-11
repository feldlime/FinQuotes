from flask import Response, Blueprint

from project.http import ok, server_error, bad_request
from project.services import smart_lab_quote
from project.services.smart_lab import SmartLabError, TickerNotFoundError

bp = Blueprint('api', __name__)


@bp.route('/ping', methods=('GET',))
def ping() -> Response:
    return ok(message='pong')


@bp.route('/quote/<string:code>', methods=('GET',))
def quote(code: str) -> Response:
    try:
        price = smart_lab_quote(code)
        return ok(data={'price': price})
    except TickerNotFoundError:
        return bad_request(message='Ticker not found')
    except SmartLabError:
        return server_error(message='Some problems while extracting price')
