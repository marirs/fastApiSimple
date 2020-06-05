"""
Dependencies
- User
- Threat
"""
from .user import is_user_admin, get_current_user

__all__ = [
    "is_user_admin",
    "get_current_user"
]
