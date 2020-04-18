from .analyzers.analyzers import EMBEDDIAAnalyzer

def get_analyzer_choices():
    return [(a["name"], a["name"]) for a in EMBEDDIAAnalyzer.analyzers]
