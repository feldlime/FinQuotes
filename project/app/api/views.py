from flask import Response, Blueprint

from project.http import ok, server_error, bad_request

bp = Blueprint('api', __name__)


@bp.route('/ping', methods=('GET',))
def ping() -> Response:
    return ok(message='pong')


@bp.route('/quote/<string:code>', methods=('GET',))
def quote(code: str) -> Response:
    if code == '':
        return server_error(message="we don't know how to process empty code")
    if code == 'FOO':
        return bad_request(message='incorrect code')
    else:
        return ok(data={'price': 111})
