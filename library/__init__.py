
from functools import wraps
from flask import request
from store.store import admin_view


def generate_key(json_data):
    l_str = ""
    for _, value in enumerate(json_data):
        l_str += json_data[value]
    return l_str


def api_cache_decorator(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        key = (request.url.split("/")[-1] + generate_key(request.get_json())).replace(" ", "")
        response = admin_view.get_cache(key)
        admin_view.add_cached_request()
        admin_view.add_successful_request()
        if not response:
            response = fn(None, *args, **kwargs)
            admin_view.set_cache(key, response)
        return fn(response, *args, **kwargs)

    return decorated
