import json
import os

from abc import ABC, abstractmethod
from tempfile import NamedTemporaryFile
from typing import List

import requests
import logging
import datetime
import time
import ratelimit
import boto3

from schedule import repeat, every, run_pending
from backoff import on_exception, expo

from os import getenv
from dotenv import load_dotenv

# __name__ get the python file name or 'main'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# env with AWS credentials
load_dotenv('.env')

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

    def _write_to_file(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for element in data:
                self.write(element) # recursive
        else:
            raise DataTypeNotSupportedForIngestionException(data)

    def write(self, data: [List, dict]):
        self._write_to_file(data=data)


class S3Writter(DataWriter):
    
    def __init__(self, coin: str, api: str) -> None:
        super().__init__(coin, api)
        self.tempfile = NamedTemporaryFile()
        self.client = boto3.client(
            "s3",
            aws_access_key_id = getenv('AWS_ID'),
            aws_secret_access_key = getenv('AWS_KEY')
        )
        self.key = f"mercado_bitcoin/{self.api}/coin={self.coin}/extracted_at={datetime.datetime.now().date()}/{self.api}_{self.coin}_{datetime.datetime.now()}.json"

    def _write_row(self, row: str) -> None:
        with open(self.tempfile.name, "a") as f: # 'a' append mode: add new data instead override the file 'w' -> write
            f.write(row)

    def write(self, data: [List, dict]):
        # write on S3
        self._write_to_file(data=data)
        self._write_file_to_s3()


    def _write_file_to_s3(self):
        self.client.put_object(
            Body=self.tempfile,
            Bucket="mercado-bitcoin-exercise-29-11",
            Key=self.key
        )
