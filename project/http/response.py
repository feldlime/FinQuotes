from http import HTTPStatus
from typing import Any

import ujson
from flask import Response


__all__ = (
    "create_response",
    "ok",
    "bad_request",
    "server_error",
)


def create_response(
        code: int,
        data: Any = None,
        message: str = None,
) -> Response:
    http_status = HTTPStatus(code)

    data = data or {}
    message = message or http_status.phrase

    content = {
        'status': http_status < HTTPStatus.BAD_REQUEST,
        'data': data,
        'message': message,
    }
    content_json = ujson.dumps(content)

    mimetype = 'application/json'

    response = Response(content_json, code, mimetype)
    return response


def ok(data: Any = None, message: str = None) -> Response:
    status = HTTPStatus.OK
    response = create_response(status, data, message)
    return response


def bad_request(data: Any = None, message: str = None) -> Response:
    status = HTTPStatus.BAD_REQUEST
    response = create_response(status, data, message)
    return response


def server_error(data: Any = None, message: str = None) -> Response:
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    response = create_response(status, data, message)
    return response
