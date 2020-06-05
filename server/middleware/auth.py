"""
Authorise requests
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from server.core.dependencies import get_current_user
from server.database import get_userdb
from server.consts import HTTP_FORBIDDEN, HTTP_UNAUTHORIZED


class Auth(BaseHTTPMiddleware):
    async def dispatch(self,
                       request: Request,
                       call_next: RequestResponseEndpoint):

        user_db = await get_userdb()
        api_user = await get_current_user(request, user_db)
        if not api_user:
            return HTTP_UNAUTHORIZED
        elif not api_user.enabled:
            return HTTP_FORBIDDEN

        response = await call_next(request)

        return response
