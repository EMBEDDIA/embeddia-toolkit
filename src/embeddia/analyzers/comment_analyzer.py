from urllib.parse import urljoin
import requests
import json
import os

from .utils import check_connection
from . import exceptions


class QMULAnalyzer:

    def __init__(self, host="http://localhost:5001", ssl_verify=True):
        self.host = host
        self.health = host
        self.url = urljoin(host, "comments_api/hate_speech/")
        self.ssl_verify = ssl_verify
        self.name = "QMUL Analyzer"

    @staticmethod
    def _process_input(text):
        payload = {"text": text}
        return payload

    @staticmethod
    def _process_output(response_json):
        if response_json["label"] == "OFF":
            return [{"tag": "OFFENSIVE", "probability": response_json["confidence"]}]
        else:
            return []

    @check_connection
    def check_health(self):
        """
        A method to check if service is alive. Throws ServiceNotAvailableException if not.
        """
        return True

    @check_connection
    def process(self, text):
        payload = self._process_input(text)
        response = requests.post(self.url, json=payload, verify=self.ssl_verify)
        if response.status_code != 200:
            raise exceptions.ServiceFailedError(f"Service sent non-200 response. Please check service url and input. Exception: {response.text}")
        response_json = response.json()
        return self._process_output(response_json)


class MultiTagAnalyzer:

    def __init__(self, host="http://rest-dev.texta.ee", project=1, auth_token="", lemmatize=True, ssl_verify=True):
        self.host = host
        self.health = urljoin(host, "api/v1/health")
        self.url = urljoin(host, f"api/v1/projects/{project}/multitag_text/")
        self.headers = {"Authorization": f"Token {auth_token}"}
        self.lemmatize = lemmatize
        self.ssl_verify = ssl_verify
        self.name = "MultiTag Analyzer"

    @staticmethod
    def _process_output(response_json):
        translations = {
            "delete": "VERY OFFENSIVE",
            "moderate": "OFFENSIVE"
        }
        return [{"tag": translations[a["tag"]], "probability": a["probability"]} for a in response_json]

    @check_connection
    def check_health(self):
        """
        A method to check if service is alive. Throws ServiceNotAvailableException if not.
        """
        return True

    def _process_input(self, text):
        payload = {"text": text, "lemmatize": self.lemmatize, "hide_false": True}
        return payload

    @check_connection
    def process(self, text):
        payload = self._process_input(text)
        response = requests.post(self.url, data=payload, headers=self.headers, verify=self.ssl_verify)
        if response.status_code != 200:
            raise exceptions.ServiceFailedError(f"Service sent non-200 response. Please check service url and input. Exception: {response.text.encode()}")
        response_json = response.json()
        return self._process_output(response_json)


class CommentAnalyzer:

    def __init__(self, analyzers):
        self.analyzers = analyzers

    def process(self, text):
        tags = []
        for name, analyzer in self.analyzers.items():
            analyzer_output = analyzer.process(text)
            for t in analyzer_output:
                t["source"] = name
                tags.append(t)
        return {"tags": tags, "text": text, "analyzers": list(self.analyzers.keys()}
