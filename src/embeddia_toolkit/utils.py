import os


# def apply_celery_task(task_func, *args):
#    if not 'test' in sys.argv:
#        return task_func.apply_async(args=(*args,))
#    else:
#        return task_func.apply(args=(*args,))


def parse_bool(value: str):
    if not isinstance(value, str):
        raise ValueError("Environment variable must be a valid boolean string (true, false)!")
    if value == "":
        raise ValueError("Environment variable must not be empty!")
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    else:
        raise ValueError("Environment variable must be a valid boolean string (true, false)!")


def parse_list_env_headers(env_key: str, default_value: list) -> list:
    """
    Function for handling env values that need to be stored as a list.

    :param env_key: key of the env value you need to parse.
    :param default_value: in case the key is missing or false, what list value to return
    """
    data = os.getenv(env_key, None)
    if data and isinstance(data, str):
        return data.split(",")
    else:
        return default_value
