from embeddia_toolkit.settings import EMBEDDIA_ANALYZERS
from embeddia_toolkit.settings import EMBEDDIA_GENERATORS
from embeddia.analyzers import exceptions


def get_analyzer_choices():
    return [(a, a) for a in EMBEDDIA_ANALYZERS.keys()]


def get_generator_dataset_choices():
    try:
        return [(a, a) for a in EMBEDDIA_GENERATORS["UH EU Generator"].get_datasets()]
    except exceptions.ServiceNotAvailableError:
        return []


def get_generator_language_choices():
    try:
        return [(a, a) for a in EMBEDDIA_GENERATORS["UH EU Generator"].get_languages()]
    except exceptions.ServiceNotAvailableError:
        return []

def get_generator_location_choices():
    try:
        return [(a, a) for a in EMBEDDIA_GENERATORS["UH EU Generator"].get_locations()]
    except exceptions.ServiceNotAvailableError:
        return []
