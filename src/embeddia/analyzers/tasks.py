from celery.decorators import task


@task(name="apply_analyzer")
def apply_analyzer(analyzer, text):
    from embeddia_toolkit.settings import EMBEDDIA_ANALYZERS
    analyzer = EMBEDDIA_ANALYZERS[analyzer]
    return analyzer.process(text)
