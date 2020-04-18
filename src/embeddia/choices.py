from .analyzers.analyzers import EMBEDDIA_ANALYZERS

def get_analyzer_choices():
    return [(a, a) for a in EMBEDDIA_ANALYZERS.keys()]
