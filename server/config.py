"""
App Configuration
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from starlette.datastructures import CommaSeparatedStrings, Secret

__all__ = [
    "CITY_DB",
    "COUNTRY_DB",
    "Config",
    "app_logger"
]

APP_DIR = os.path.dirname(os.path.abspath('fastApiSimple'))
LOG_DIR = os.path.join(APP_DIR, 'log')
GEO_DIR = os.path.join(APP_DIR, 'server', 'geo')
CITY_DB = os.path.join(GEO_DIR, 'GeoLite2-City.mmdb')
COUNTRY_DB = os.path.join(GEO_DIR, 'GeoLite2-Country.mmdb')


class Config:

    DB_NAME = 'fastapisimple'
    USERS_DOCUMENT_NAME = 'users'
    MONGODB_URL = f'mongodb://localhost:27017/{DB_NAME}'

    DEFAULT_ROUTE_STR = "/api"
    SECRET_KEY = Secret('a nice secret key')

    ALLOWED_HOSTS = CommaSeparatedStrings("localhost, 127.0.0.1")


def app_logger(name, log_file=None):
    if not os.access(LOG_DIR, os.F_OK):
        os.makedirs(LOG_DIR)

    log_file = os.path.join(LOG_DIR, 'application.log' or log_file)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_format = logging.Formatter(
        fmt="%(asctime)s | %(levelname)8s | %(name)s : %(message)s",
        datefmt="%b %d %Y %I:%M:%S %p"
    )
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(log_format)
    file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024*1024*10, backupCount=10)
    file_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

