from .analyzers.analyzers import EMBEDDIAAnalyzer

def get_analyzer_choices():
    return [(a, a) for a in EMBEDDIAAnalyzer.EMBEDDIA_ANALYZERS.keys()]
