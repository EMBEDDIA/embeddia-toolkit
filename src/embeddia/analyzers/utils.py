import requests
from . import exceptions


def check_connection(func):
    """
    Wrapper function for checking Service connection prior to requests.
    """
    def func_wrapper(*args, **kwargs):
        health = args[0].health
        try:
            response = requests.get(health, timeout=3)
            if not response.ok:
                raise exceptions.ServiceNotAvailableError(health)
            return func(*args, **kwargs)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            raise exceptions.ServiceNotAvailableError(health)
    return func_wrapper