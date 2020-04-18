from urllib.parse import urljoin
import requests
import json
import os

from . import exceptions


def check_connection(func):
    """
    Wrapper function for checking Service connection prior to requests.
    """
    def func_wrapper(*args, **kwargs):
        host = args[0].host
        try:
            response = requests.get(host, timeout=3)
            if not response.ok:
                raise exceptions.MLPNotAvailableError()
            return func(*args, **kwargs)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            raise exceptions.ServiceNotAvailableError()
    return func_wrapper


class KWEAnalyzer:

    def __init__(self, host="http://localhost:5003"):
        self.host = host
        self.url = urljoin(host, "rest_api/extract_keywords")

    @staticmethod
    def _process_input(text):
        payload = {
            "title": text,
            "lead": text,
            "bodyText": text,
            "channelLanguage": text
        }
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


class TaggerGroupAnalyzer:

    def __init__(self):
        pass

    def process(self, text):
        pass



EMBEDDIA_ANALYZERS = {
    "KWE": KWEAnalyzer(),
    "HSD": HSDAnalyzer()
}


class EMBEDDIAAnalyzer:

    def __init__(self):
        self.embeddia_analyzers = EMBEDDIA_ANALYZERS

    def process(self, text, analyzers=EMBEDDIA_ANALYZERS.keys()):
        output = {}
        for analyzer in analyzers:
            analyzer_obj = self.embeddia_analyzers[analyzer]
            output[analyzer] = analyzer_obj.process(text)
        return output
