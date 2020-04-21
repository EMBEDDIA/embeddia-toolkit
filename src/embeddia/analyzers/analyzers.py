from urllib.parse import urljoin
from celery import group
import requests
import json
import os

from .utils import check_connection
from . import exceptions
from .tasks import apply_analyzer
from utils import apply_celery_task

class KWEAnalyzer:

    def __init__(self, host="http://localhost:5003"):
        self.host = host
        self.health = host
        self.url = urljoin(host, "rest_api/extract_keywords/")

    @staticmethod
    def _process_input(text):
        payload = {"text": text}
        return payload

    @staticmethod
    def _process_output(response_json):
        return response_json["keywords"]

    @check_connection
    def process(self, text):
        payload = self._process_input(text)
        response = requests.post(self.url, json=payload)
        if response.status_code != 200:
            raise exceptions.ServiceFailedError(f"Service sent non-200 response. Please check service url and input. Exception: {response.text}")
        response_json = response.json()
        return self._process_output(response_json)


class HSDAnalyzer:

    def __init__(self, host="http://localhost:5001"):
        self.host = host
        self.health = host
        self.url = urljoin(host, "ml_hate_speech/ml_bert")

    @staticmethod
    def _process_input(text):
        payload = {
            "tweet": [text],
        }
        return payload

    @staticmethod
    def _process_output(response_json):
        return response_json[0]

    @check_connection
    def process(self, text):
        payload = self._process_input(text)
        response = requests.post(self.url, json=payload)
        if response.status_code != 200:
            raise exceptions.ServiceFailedError(f"Service sent non-200 response. Please check service url and input. Exception: {response.text}")
        response_json = response.json()
        return self._process_output(response_json)


class HybridTaggerAnalyzer:

    def __init__(self, host="http:/dev.texta.ee:8000", project=1, tagger_group=1, auth_token="", lemmatize=True, use_ner=True):
        self.host = host
        self.health = urljoin(host, "api/v1/health")
        self.url = urljoin(host, f"api/v1/projects/{project}/tagger_groups/{tagger_group}/tag_text/")
        self.headers = {"Authorization": f"Token {auth_token}"}
        self.lemmatize = lemmatize
        self.use_ner = use_ner

    def _process_input(self, text):
        payload = {"text": text, "lemmatize": self.lemmatize, "use_ner": self.use_ner}
        return payload

    @staticmethod
    def _process_output(response_json):
        return [{"tag": a["tag"], "probability": a["probability"]} for a in response_json]

    @check_connection
    def process(self, text):
        payload = self._process_input(text)
        response = requests.post(self.url, data=payload, headers=self.headers)
        if response.status_code != 200:
            raise exceptions.ServiceFailedError(f"Service sent non-200 response. Please check service url and input. Exception: {response.text}")
        response_json = response.json()
        return self._process_output(response_json)


class MultiTagAnalyzer:

    def __init__(self, host="http:/dev.texta.ee:8000", project=1, auth_token="", lemmatize=True, hide_false=False):
        self.host = host
        self.health = urljoin(host, "api/v1/health")
        self.url = urljoin(host, f"api/v1/projects/{project}/multitag_text/")
        self.headers = {"Authorization": f"Token {auth_token}"}
        self.lemmatize = lemmatize
        self.hide_false = hide_false

    def _process_input(self, text):
        payload = {"text": text, "hide_false": self.hide_false, "lemmatize": self.lemmatize}
        return payload

    @staticmethod
    def _process_output(response_json):
        return [{"tag": a["tag"], "probability": a["probability"], "result": a["result"]} for a in response_json]

    @check_connection
    def process(self, text):
        payload = self._process_input(text)
        response = requests.post(self.url, data=payload, headers=self.headers)
        if response.status_code != 200:
            raise exceptions.ServiceFailedError(f"Service sent non-200 response. Please check service url and input. Exception: {response.text}")
        response_json = response.json()
        return self._process_output(response_json)


class EMBEDDIAAnalyzer:

    def __init__(self, embeddia_analyzers={}):
        self.embeddia_analyzers = embeddia_analyzers

    @staticmethod
    def apply_analyzers(analyzers, text):
        group_task = group(apply_analyzer.s(analyzer, text) for analyzer in analyzers)
        print('asd')
        #group_results = apply_celery_task(group_task)
        group_results = group_task.apply()
        print('asdasd')
        # retrieve results & remove non-hits
        tags = [result for result in group_results.get() if result]
        print(tags)
        return tags

    def process(self, text, analyzers=[]):
        if not analyzers:
            analyzers = self.embeddia_analyzers.keys()
        results = self.apply_analyzers(analyzers, text)
        return results


