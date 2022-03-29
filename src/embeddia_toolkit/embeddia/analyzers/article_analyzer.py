from urllib.parse import urljoin
import requests
import json
import os

from .utils import check_connection
from . import exceptions


class NERAnalyzer:

    def __init__(self, host="http://localhost:5004", ssl_verify=True, language="hr"):
        self.host = host
        self.health = host
        self.url = urljoin(host, f"ner/predictRawText/{language}/")
        self.ssl_verify = ssl_verify
    
    @staticmethod
    def _process_input(text):
        payload = {"text": text}
        return payload

    @staticmethod
    def _process_output(response_json):
        # This API output is HORRIBLE!
        out = []
        data = response_json["data"]["result"]["0"]
        current_tag = []
        seen_tags = []
        for i, tag in enumerate(data["tags"]):
            if tag.startswith("B-") or tag.startswith("I-"):
                current_tag.append(data["tokens"][i])
            elif current_tag:
                tag = " ".join(current_tag)
                if tag not in seen_tags:
                    seen_tags.append(tag)
                    out.append({"tag": tag})
                    current_tag = []
        return out

    @check_connection
    def get_languages(self):
        response = requests.get(urljoin(self.host, "supportedLanguages"), verify=self.ssl_verify)
        return response.json()["data"]["languages"]

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
        self.health = urljoin(host, f"api/v1/projects/{project}/tagger_groups/{tagger_group}/")
        self.url = urljoin(host, f"api/v1/projects/{project}/tagger_groups/{tagger_group}/tag_text/")
        self.headers = {"Authorization": f"Token {auth_token}"}
        self.lemmatize = lemmatize
        self.use_ner = use_ner
        self.ssl_verify = ssl_verify

    @staticmethod
    def _process_output(response_json):
        return [{"tag": a["tag"]} for a in response_json]

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
        keywords_combined = [j for sub in response_json.values() for j in sub]
        return [{"tag": keyword} for keyword in keywords_combined]

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


class SentimentAnalyzer:

    def __init__(self, host="http://localhost:5010", ssl_verify=True):
        self.host = host
        self.health = host
        self.url = urljoin(host, "rest_api/analyze_sentiment/")
        self.ssl_verify = ssl_verify

    @staticmethod
    def _process_input(text):
        payload = {"text": text}
        return payload

    @staticmethod
    def _process_output(response_json):
        keywords_combined = [j for sub in response_json.values() for j in sub]
        return [{"tag": keyword} for keyword in keywords_combined]

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
