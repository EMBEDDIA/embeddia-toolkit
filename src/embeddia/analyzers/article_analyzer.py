from urllib.parse import urljoin
import requests
import json
import os

from .utils import check_connection
from . import exceptions


class NERAnalyzer:

    def __init__(self, host="http://localhost:5004", ssl_verify=True):
        self.host = host
        self.health = host
        self.url = urljoin(host, "ner/predictRawText/")
        self.ssl_verify = ssl_verify

    @staticmethod
    def _process_input(text, language):
        payload = {"text": text, "language": language}
        return payload

    @staticmethod
    def _process_output(response_json):
        return response_json

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
    def process(self, text, language):
        payload = self._process_input(text, language)
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


class ArticleAnalyzer:

    def __init__(self, mlp, analyzers):
        self.mlp = mlp
        self.analyzers = analyzers

    def process(self, text, analyzers=[]):
        # process with MLP
        mlp_analysis = self.mlp.process(text)
        # extract stuff from MLP output
        tokenized_text = mlp_analysis["text"]["text"]
        language = mlp_analysis["text"]["lang"]
        lemmas = mlp_analysis["text"]["lemmas"]
        entities = [{"entity": e["str_val"], "type": e["fact"], "source": "MLP"} for e in mlp_analysis["texta_facts"]]
        # use analyzers
        tags = []
        for name, analyzer in self.analyzers.items():
            predicted_tags = analyzer.process(lemmas)
            for tag in predicted_tags:
                tag["source"] = name
                tags.append(tag)
        # prepare output
        output = {
            "text": tokenized_text,
            "tags": tags,
            "entities": entities,
            "language": language,
            "analyzers": list(self.analyzers.keys())+["TEXTA MLP"]
        }
        return output
