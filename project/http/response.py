from http import HTTPStatus
from typing import Any

import ujson
from aiohttp import hdrs, web

from project.types import Headers


__all__ = (
    "create_response",
    "ok",
    "bad_request",
    "server_error",
)

HEADERS: Headers = {
    hdrs.EXPIRES: '0',
    hdrs.PRAGMA: 'no-cache',
    hdrs.CACHE_CONTROL: 'no-cache, no-store, must-revalidate',
}


def create_response(
        code: int,
        data: Any = None,
        message: str = None,
) -> web.Response:

    # noinspection PyArgumentList
    http_status = HTTPStatus(code)

    data = data or {}
    message = message or http_status.phrase

    content = {
        'status': http_status < HTTPStatus.BAD_REQUEST,
        'data': data,
        'message': message,
    }

    response = web.json_response(content, headers=HEADERS, dumps=ujson.dumps)
    return response


def ok(data: Any = None, message: str = None) -> web.Response:
    status = HTTPStatus.OK
    response = create_response(status, data, message)
    return response


def bad_request(data: Any = None, message: str = None) -> web.Response:
    status = HTTPStatus.BAD_REQUEST
    response = create_response(status, data, message)
    return response


def server_error(data: Any = None, message: str = None) -> web.Response:
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    response = create_response(status, data, message)
    return response
