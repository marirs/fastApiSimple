"""
CONSTANTS
"""
from http import HTTPStatus
from starlette.responses import PlainTextResponse

__all__ = [
    "FAVICON",
    "HTTP_FORBIDDEN",
    "HTTP_UNAUTHORIZED",
    "HTTP_NOTFOUND",
    "HTTP_SERVER_ERROR",
    "HTTP_OK"
]

FAVICON = '<link rel="icon" href="data:;base64,iVBORw0KGgo=">'

HTTP_FORBIDDEN = PlainTextResponse(
    content="Forbidden",
    status_code=HTTPStatus.FORBIDDEN
)
HTTP_UNAUTHORIZED = PlainTextResponse(
    content="Unauthorized",
    status_code=HTTPStatus.UNAUTHORIZED
)
HTTP_NOTFOUND = PlainTextResponse(
    content="Nothing found here",
    status_code=HTTPStatus.NOT_FOUND
)
HTTP_OK = PlainTextResponse(
    content="",
    status_code=HTTPStatus.OK
)
HTTP_SERVER_ERROR = PlainTextResponse(
    content="Internal server error",
    status_code=HTTPStatus.INTERNAL_SERVER_ERROR
)
