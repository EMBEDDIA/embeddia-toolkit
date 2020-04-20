from embeddia_toolkit.settings import EMBEDDIA_ANALYZERS
from embeddia_toolkit.settings import EMBEDDIA_EU_GENERATOR


def get_analyzer_choices():
    return [(a, a) for a in EMBEDDIA_ANALYZERS.keys()]


def get_generator_dataset_choices():
    return [(a, a) for a in EMBEDDIA_EU_GENERATOR.get_datasets()]


def get_generator_language_choices():
    return [(a, a) for a in EMBEDDIA_EU_GENERATOR.get_languages()]


### THIS IS A TEMPORARY HACK
def get_generator_location_choices():
    return [(a, a) for a in ["EE", "FI", "LV", "LT"]]
