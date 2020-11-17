import requests
from . import exceptions


def check_connection(func):
    """
    Wrapper function for checking Service connection prior to requests.
    """
    def func_wrapper(*args, **kwargs):
        health = args[0].health
        ssl_verify = args[0].ssl_verify
        error = f"URL {health} is not accessible. SSL verification is {ssl_verify}."
        try:
            response = requests.get(health, timeout=3, verify=ssl_verify)
            if not response.ok:
                raise exceptions.ServiceNotAvailableError(error)
            return func(*args, **kwargs)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            raise exceptions.ServiceNotAvailableError(error)
    return func_wrapper
