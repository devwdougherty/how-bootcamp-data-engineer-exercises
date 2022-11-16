import json
import os
from abc import ABC, abstractmethod
from typing import List

import requests
import logging
import datetime
import time
import ratelimit

from schedule import repeat, every, run_pending
from backoff import on_exception, expo

# __name__ get the python file name or 'main'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)

class DataWriter():

    def __init__(self, coin: str, api: str) -> None:
        self.coin = coin
        self.api = api
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now()}.json"
        #self.filename = f"{self.api}\\{self.coin}\\{datetime.datetime.now()}.json"

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "a") as f: # 'a' append mode: add new data instead override the file 'w' -> write
            f.write(row)

    def write(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for element in data:
                self.write(element) # recursive
        else:
            raise DataTypeNotSupportedForIngestionException(data)