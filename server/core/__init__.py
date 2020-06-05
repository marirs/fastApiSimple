"""
fastApi Simple
"""
from .event_handlers import on_app_start, on_app_shutdown

__all__ = [
    "on_app_start",
    "on_app_shutdown",
]