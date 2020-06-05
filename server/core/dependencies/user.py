"""
Dependencies
"""
from typing import Optional
from fastapi import Request, Depends

from server.database import get_userdb
from server.database.crud.user import UserDatabase
from server.database.models.user import User


__all__ = [
    "is_user_admin",
    "get_current_user"
]


async def _get_key(request) -> Optional[str]:
    """Gets the API key either from header or url path
    :param request: request
    :return: key or none
    """
    path = str(request.url.path)
    key = request.headers.get('X-API-KEY', path.split('/api/')[-1].split('/', 1)[0])
    return key


async def get_current_user(
        request: Request,
        user_db: UserDatabase = Depends(get_userdb)
) -> Optional[User]:
    """Returns Current User information
    :param request: Request
    :param user_db: user's database
    :return: returns User or None
    """
    key = await _get_key(request)
    if key:
        return await user_db.get(str(key))


async def is_user_admin(
        request: Request,
        user_db: UserDatabase = Depends(get_userdb)
) -> bool:
    """Is a user admin
    :param request: Request
    :param user_db: User's database
    :return: returns True is admin else false
    """
    key = await _get_key(request)
    if key:
        user = await user_db.get(str(key))
        return user.is_superuser
