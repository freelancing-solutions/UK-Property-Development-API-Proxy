import os
from decouple import config
from .utils import is_development


class Config:
    API_KEY = config('API_KEY')
    SECRET = config('SECRET')
    API_ENDPOINT = config('API_ENDPOINT')
    SENTRY_DSN = config('SENTRY_DSN')
    IS_DEV = is_development()
