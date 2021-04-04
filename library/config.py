import os
from decouple import config
from .utils import is_development


class Config:
    API_KEY: str = config('API_KEY')
    SECRET: str = config('SECRET')
    API_ENDPOINT: str = config('API_ENDPOINT')
    SENTRY_DSN: str = config('SENTRY_DSN')
    IS_DEV: bool = config('IS_DEV')
    PROJECT: str = "property-data-t-37071"
    CACHE_TTL: int = 43200
    CACHE_SIZE: int = 1024

    AUTHORIZED_ADDRESSES: list = ['https://www.worktravel.agency',
                            'https://worktravel.agency',
                            'https://propertydevelopment.worktravel.agency',
                            'https://property-data-t-37071.nw.r.appspot.com',
                            'https://property-data-t-37071.appspot.com'
                            ]

    IS_DEBUG: bool = config('IS_DEBUG')

    def set_debug_cors_header(self) -> None:
        if self.IS_DEV or self.IS_DEBUG:
            self.AUTHORIZED_ADDRESSES.append('http://localhost:8080')

