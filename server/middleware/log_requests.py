"""
Log requests middleware
"""
import time
from fastapi import Request
import geoip2.database
from geoip2.errors import AddressNotFoundError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from server.config import app_logger
from server.config import CITY_DB

logger = app_logger(__name__, 'requests.log')
geo_location = geoip2.database.Reader(CITY_DB)


class LogRequests(BaseHTTPMiddleware):
    async def dispatch(self,
                       request: Request,
                       call_next: RequestResponseEndpoint,
                       ):
        start_time = time.time()
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)

        remote = ":".join(map(str, request.client))
        x_forwarded_for = request.headers.get('x-forwarded-for', None)
        x_real_ip = request.headers.get('x-real-ip', None)
        cc = request.headers.get('cf-ipcountry', None)
        if x_forwarded_for:
            x_forwarded_for = x_forwarded_for.split(',')[0]
        if "None" in remote:
            if x_forwarded_for:
                remote = x_forwarded_for
            elif x_real_ip:
                remote = x_real_ip

        try:
            remote_country = geo_location.city(remote.rsplit(':', 1)[0])
            remote_country = remote_country.country.name
        except AddressNotFoundError:
            remote_country = 'Unknown'

        logger.info({
            "remote_ip": remote,
            "remote_country": remote_country,
            "user_agent": request.headers.get('user-agent', None),
            'method': request.method,
            "path": request.url.path,
            "completed in (ms)": formatted_process_time,
            "response code": response.status_code
        })
        response.headers["X-Process-Time"] = str(formatted_process_time)

        return response
