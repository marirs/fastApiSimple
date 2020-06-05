"""
API User Management endpoint
- Add user & user properties
- Disable/Enable User
- Remove user
"""
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, Form
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from http import HTTPStatus

from server.core.dependencies import get_current_user
from server.consts import HTTP_NOTFOUND, HTTP_UNAUTHORIZED
from server.database.models.user import User, BaseUserCreate
from server.database.crud.user import UserDatabase
from server.database import get_userdb

user_router = APIRouter()


async def _validate(email, current_user) -> None:
    """Common validations before proceeding with the request
    """
    if not email:
        """No Email found in form"""
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="email address not provided"
        )

    if not current_user.is_superuser:
        """Current User is not a Superuser"""
        return HTTP_NOTFOUND

    if email == current_user.email:
        """Requested for Email and Current User's Email is the same"""
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="email provided for new user provision - email is your own email"
        )


@user_router.get("/")
async def list_users(current_user: User = Depends(get_current_user)):
    """List All users if Superuser or else
    Show current user information
    """
    # if current_user.is_superuser or "admin" in current_user.endpoint_access:
    #     user_list = await get_all(db)
    #     return user_list

    current_user = current_user.dict()
    projection = ['is_superuser', 'endpoint_acl', 'enabled']
    [current_user.pop(k, None) for k in projection]

    return current_user


@user_router.post('/new')
async def new_user_provision(
        email: EmailStr = Form(None),
        is_superuser: Optional[bool] = Form(None),
        endpoints_acl: Optional[str] = Form(None),
        current_user: User = Depends(get_current_user),
        user_db: UserDatabase = Depends(get_userdb)
):
    await _validate(email, current_user)
    if await user_db.get_by_email(email=email):
        """Requested for Email already exists"""
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="email provided for new user provision - already exists"
        )

    user: BaseUserCreate = BaseUserCreate(email=email)
    if endpoints_acl:
        endpoints_acl = endpoints_acl.split(",")

    if is_superuser:
        if current_user.is_superuser:
            # Only superusers can create
            # users with superuser access
            is_superuser: bool = True
        else:
            return HTTP_UNAUTHORIZED

    _user = await user_db.create_api_user(user, endpoints_acl, is_superuser)
    return JSONResponse(
        content=jsonable_encoder(dict(**_user.dict())),
        status_code=HTTPStatus.OK
    )


@user_router.post('/update')
async def update_user(
        email: EmailStr = Form(None),
        is_superuser: Optional[bool] = Form(None),
        endpoint_acl: Optional[str] = Form(None),
        current_user: User = Depends(get_current_user),
        user_db: UserDatabase = Depends(get_userdb)

):
    await _validate(email, current_user)

    api_user = await user_db.get_by_email(email=email)
    if is_superuser is not None:
        api_user.is_superuser = is_superuser

    if endpoint_acl is not None:
        api_user.endpoint_acl = endpoint_acl.split(',')

    api_user.updated_at = datetime.utcnow()

    _user = await user_db.update(api_user)
    return JSONResponse(
        content=jsonable_encoder(dict(**_user.dict())),
        status_code=HTTPStatus.OK
    )
