from flask import Response, Blueprint

from project.http import ok, server_error, bad_request
from project.services import smart_lab_quote

bp = Blueprint('api', __name__)


@bp.route('/ping', methods=('GET',))
def ping() -> Response:
    return ok(message='pong')


@bp.route('/quote/<string:code>', methods=('GET',))
def quote(code: str) -> Response:
    price = smart_lab_quote(code)
    return ok(data={'price': price})
