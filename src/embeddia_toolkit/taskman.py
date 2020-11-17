import os
from celery import Celery

from embeddia_toolkit.settings import ARTICLE_ANALYZERS, COMMENT_ANALYZERS, CELERY_TASK_QUEUE



ALL_ANALYZERS= {**ARTICLE_ANALYZERS, **COMMENT_ANALYZERS}


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'embeddia_toolkit.settings')

app = Celery('taskman')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(name="apply_single_analyzer", queue=CELERY_TASK_QUEUE)
def apply_single_analyzer(analyzer_name, text):
    # select analyzer
    analyzer = ALL_ANALYZERS[analyzer_name]
    # process with analyzer
    result = analyzer.process(text)
    return result
