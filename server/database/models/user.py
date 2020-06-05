"""
User DB Model
"""
from datetime import datetime, timezone
from pydantic import BaseConfig, BaseModel, Field, EmailStr, validator
from typing import Optional


class RWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        }


class _DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")


class BaseUser(_DateTimeModelMixin, RWModel):
    email: EmailStr
    endpoint_acl: list = ["user"]
    is_superuser: bool = False
    enabled: bool = True


class BaseUserIn(BaseUser):
    api_key: str = ""


class BaseUserCreate(RWModel):
    email: EmailStr


class BaseUserLogin(RWModel):
    api_key: str


class BaseUserUpdate(BaseUser):
    api_key: Optional[str] = None
    enabled: Optional[bool] = None
    is_superuser: Optional[bool] = None
    endpoint_acl: Optional[list] = None


class User(BaseUser):
    api_key: str
    is_superuser: bool
    endpoint_acl = list
