"""
CRUD Operations for User Endpoint
"""
import secrets
from typing import Optional, List
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import EmailStr

from server.database.models.user import User, BaseUser, BaseUserCreate, BaseUserIn, BaseUserUpdate


class UserDatabase:
    _user: User
    _collection: AsyncIOMotorCollection
    _projection: dict = {"_id": False}

    def __init__(self, user: User, collection: AsyncIOMotorCollection):
        self._user = user
        self._collection = collection
        self._collection.create_index('api_key', unique=True)
        self._collection.create_index('email', unique=True)

    async def get(self, key: str, projection: dict = None) -> Optional[User]:
        user = await self._collection.find_one({'api_key': key}, projection=projection or self._projection)
        return self._user(**user) if user else None

    async def get_by_email(self, email: EmailStr, projection: dict = None) -> Optional[User]:
        user = await self._collection.find_one({'email': email}, projection=projection or self._projection)
        return self._user(**user) if user else None

    async def insert(self, user: BaseUserIn) -> User:
        await self._collection.insert_one(user.dict())
        return self._user(**user.dict())

    async def update(self, user: User) -> User:
        await self._collection.replace_one({'email': user.email}, user.dict())
        return user

    async def delete(self, user: User) -> None:
        await self._collection.delete_one({'email': user.email})

    async def create_api_user(
            self,
            api_user: BaseUserCreate,
            endpoints_acl: Optional[list] = None,
            is_superuser: Optional[bool] = False
    ) -> Optional[User]:
        api_user = BaseUserIn(**api_user.dict())
        api_user.api_key = secrets.token_hex(24)
        api_user.created_at = datetime.utcnow()
        api_user.updated_at = datetime.utcnow()

        if is_superuser:
            api_user.is_superuser = is_superuser

        if endpoints_acl:
            api_user.endpoint_acl += endpoints_acl
            api_user.endpoints_acl = list(set(api_user.endpoint_acl))

        return await self.insert(api_user)
