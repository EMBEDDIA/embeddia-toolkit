from urllib.parse import urljoin
import requests
import json
import os

from .utils import check_connection
from . import exceptions


class NLGenerator:

    def __init__(self, host="http://localhost:5000"):
        self.host = host
        self.health = urljoin(host, "datasets")
        self.url = urljoin(host, "eunlg")

    @check_connection
    def get_datasets(self):
        response = requests.get(urljoin(self.host, "datasets"))
        return response.json()["datasets"]

    @check_connection
    def get_languages(self):
        response = requests.get(urljoin(self.host, "languages"))
        return response.json()["languages"]

    @check_connection
    def get_locations(self):
        locations = []
        for dataset in self.get_datasets():
            payload = {"dataset": dataset}
            response = requests.post(urljoin(self.host, "locations"), json=payload)
            locations = locations + response.json()["locations"]
        return locations

    @check_connection
    def process(self, dataset, language, location):
        payload = {
            "language": language,
            "dataset": dataset,
            "location": location
        }
        response = requests.post(self.url, json=payload)
        if response.status_code != 200:
            raise exceptions.ServiceFailedError(f"Service sent non-200 response. Please check service url and input. Exception: {response.text}")
        response_json = response.json()
        return response_json
