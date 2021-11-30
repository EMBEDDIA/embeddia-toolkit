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
        self.name = "EMBEDDIA Multilingual Comment Model"

    @staticmethod
    def _process_input(text):
        payload = {"text": text}
        return payload

    @staticmethod
    def _process_output(response_json):
        if response_json["label"].startswith("Blocked"):
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


class BERTTaggerAnalyzer:

    def __init__(self, host="https://rest-dev.texta.ee", project=310, tagger=71, auth_token="", ssl_verify=True):
        self.host = host
        self.health = urljoin(host, f"api/v1/projects/{project}/bert_taggers/{tagger}/")
        self.url = urljoin(host, f"api/v1/projects/{project}/bert_taggers/{tagger}/tag_text/")
        self.headers = {"Authorization": f"Token {auth_token}"}
        self.ssl_verify = ssl_verify
        self.name = "TEXTA BERT Comment Model"

    @staticmethod
    def _process_output(response_json):
        if response_json["result"] == "true":
            return [{"tag": "OFFENSIVE", "probability": response_json["probability"]}]
        else:
            return []

    @check_connection
    def check_health(self):
        """
        A method to check if service is alive. Throws ServiceNotAvailableException if not.
        """
        return True

    def _process_input(self, text):
        payload = {"text": text, "persistent": True}
        return payload

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
        self.name = "Monolingual Comment Model"

    @staticmethod
    def _process_output(response_json):
        translations = {
            "delete": "VERY OFFENSIVE",
            "moderate": "OFFENSIVE"
        }
        return [{"tag": translations[a["tag"]], "probability": a["probability"]} for a in response_json if a["tag"] in translations]

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
