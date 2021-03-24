import os
from decouple import config
from .utils import is_development


class Config:
    API_KEY = config('API_KEY')
    SECRET = config('SECRET')
    API_ENDPOINT = config('API_ENDPOINT')
    SENTRY_DSN = config('SENTRY_DSN')
    IS_DEV = config('IS_DEV')

    AUTHORIZED_ADDRESSES = ['https://www.worktravel.agency',
                            'https://worktravel.agency',
                            'https://propertydevelopment.worktravel.agency',
                            'https://property-data-t-37071.nw.r.appspot.com',
                            'https://property-data-t-37071.appspot.com'
                            ]

    IS_DEBUG = config('IS_DEBUG')

    def set_debug_cors_header(self):
        if self.IS_DEV or self.IS_DEBUG:
            self.AUTHORIZED_ADDRESSES.append('http://localhost:8080')

