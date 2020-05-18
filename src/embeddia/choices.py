from embeddia_toolkit.settings import EMBEDDIA_GENERATOR
from embeddia.analyzers import exceptions


def get_generator_dataset_choices():
    try:
        return [(a, a) for a in EMBEDDIA_GENERATOR.get_datasets()]
    except exceptions.ServiceNotAvailableError:
        return []


def get_generator_language_choices():
    try:
        return [(a, a) for a in EMBEDDIA_GENERATOR.get_languages()]
    except exceptions.ServiceNotAvailableError:
        return []

def get_generator_location_choices():
    try:
        return [(a, a) for a in EMBEDDIA_GENERATOR.get_locations()]
    except exceptions.ServiceNotAvailableError:
        return []

#def get_ner_language_choices():
#    try:
#        return [(a, a) for a in EMBEDDIA_ANALYZERS["NER"].get_languages()]
#    except exceptions.ServiceNotAvailableError:
#        return []
