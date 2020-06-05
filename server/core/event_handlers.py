"""
Event handlers
"""
import logging
from typing import Callable
from fastapi import FastAPI

from server.database import mongodb


__all__ = ["on_app_start", "on_app_shutdown"]


def on_app_start(app: FastAPI, logger: logging.Logger) -> Callable:
    async def startup() -> None:
        logger.info("Starting fastAPI Server")
        await mongodb.connect()
    return startup


def on_app_shutdown(app: FastAPI, logger: logging.Logger) -> Callable:
    async def shutdown() -> None:
        await mongodb.close()
        logger.info("Shutting down fastAPI Server")
    return shutdown
