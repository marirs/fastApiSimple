"""
Endpoints Router
"""
from fastapi import APIRouter, Depends
from .endpoints.user import user_router


router = APIRouter()
router.include_router(user_router, prefix="/user")
