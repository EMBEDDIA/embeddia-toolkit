from urllib.parse import urljoin
import requests
import json
import os

from .utils import check_connection
from . import exceptions

class KWEAnalyzer:

    def __init__(self, host="http://localhost:5003", ssl_verify=True):
        self.host = host
        self.health = host
        self.url = urljoin(host, "rest_api/extract_keywords/")
        self.ssl_verify = ssl_verify

    @staticmethod
    def _process_input(text):
        payload = {"text": text}
        return payload

    @staticmethod
    def _process_output(response_json):
        return [{"tag": keyword} for keyword in response_json["keywords"]]

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


class HSDAnalyzer:

    def __init__(self, host="http://localhost:5001", ssl_verify=True):
        self.host = host
        self.health = host
        self.url = urljoin(host, "comments_api/hate_speech/")
        self.ssl_verify = ssl_verify

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


class HybridTaggerAnalyzer:

    def __init__(self, host="http://rest-dev.texta.ee", project=1, tagger_group=1, auth_token="", lemmatize=True, use_ner=True, ssl_verify=True):
        self.host = host
        self.health = urljoin(host, "api/v1/health")
        self.url = urljoin(host, f"api/v1/projects/{project}/tagger_groups/{tagger_group}/tag_text/")
        self.headers = {"Authorization": f"Token {auth_token}"}
        self.lemmatize = lemmatize
        self.use_ner = use_ner
        self.ssl_verify = ssl_verify

    @staticmethod
    def _process_output(response_json):
        return [{"tag": a["tag"], "probability": a["probability"]} for a in response_json]

    def _process_input(self, text):
        payload = {"text": text, "lemmatize": self.lemmatize, "use_ner": self.use_ner}
        return payload

    @check_connection
    def check_health(self):
        """
        A method to check if service is alive. Throws ServiceNotAvailableException if not.
        """
        return True

    @check_connection
    def process(self, text):
        payload = self._process_input(text)
        response = requests.post(self.url, data=payload, headers=self.headers, verify=self.ssl_verify)
        if response.status_code != 200:
            raise exceptions.ServiceFailedError(f"Service sent non-200 response. Please check service url and input. Exception: {response.text.encode()}")
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


class EMBEDDIAAnalyzer:

    def __init__(self, embeddia_analyzers={}):
        self.embeddia_analyzers = embeddia_analyzers

    def process(self, text, analyzers=[]):
        output = {}
        if not analyzers:
            analyzers = self.embeddia_analyzers.keys()
        for analyzer in analyzers:
            analyzer_obj = self.embeddia_analyzers[analyzer]
            output[analyzer] = analyzer_obj.process(text)
        return output
