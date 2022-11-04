import json
import os
from abc import ABC, abstractmethod
from typing import List

import requests
import logging
import datetime

# __name__ get the python file name or 'main'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

"""
ABC -> abstract base class
"""
class MercadoBitcoinApi(ABC):

    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = "https://www.mercadobitcoin.net/api"

    """
    _ in the beginning of function's name means that it's a intern method, not accessible externaly
    @abstractmethod -> transforming the method in a abstract one (not instantiable)
    Abstract method should now be implemented to be used (open-close principle)
    **kwargs -> Making the signature of this method available and open for N of arguments of key-value.
    """
    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass
        #return f"{self.base_endpoint}/{self.coin}/day-summary/2022/10/31"

    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status() # requests library -> raise_for_status verifies if it is an OK success return.
        return response.json()


class BtcApi(MercadoBitcoinApi):
    def _get_endpoint(self) -> str:
        return "a"


class DaySummaryApi(MercadoBitcoinApi):

    type = "day-summary"

    def _get_endpoint(self, date: datetime.date) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"


class TradesApi(MercadoBitcoinApi):
    type = "trades"

    def convert_date_to_unix(self, date: datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.datetime = None) -> str:
        if date_from and not date_to:
            unix_date_from = self.convert_date_to_unix(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"
        elif date_from and date_to:
            unix_date_from = self.convert_date_to_unix(date_from)
            unix_date_to = self.convert_date_to_unix(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"

        return endpoint

#print(DaySummaryApi(coin="BTC").get_data(date=datetime.date(2022, 10, 31)))
#print(TradesApi(coin="BTC").get_data())
#print(TradesApi(coin="BTC").get_data(date_from=datetime.datetime(2022, 10, 25)))
#print(TradesApi(coin="BTC").get_data(date_from=datetime.datetime(2022, 10, 25), date_to=datetime.datetime(2022, 10, 26)))


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

"""
day_summary_data = DaySummaryApi(coin="BTC").get_data(date=datetime.date(2022, 10, 30))
writer = DataWriter('day_summary.json')
writer.write(day_summary_data)

trades_data = TradesApi(coin="BTC").get_data()
writer = DataWriter('trades.json')
writer.write(trades_data)
"""

class DataIngestor(ABC):
    def __init__(self, coins: List[str], default_start_date: datetime.date, writer: DataWriter) -> None:
        self.coins = coins
        self.default_start_date = default_start_date
        self.writer = writer

    @abstractmethod
    def ingest(self) -> None:
        pass


class DaySummaryIngestor(DataIngestor):

    def ingest(self) -> None:
        date = self.default_start_date
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
                # self.writer.write(data)
                # update date


ingestor = DaySummaryIngestor(writer=DataWriter, coins=["BTC", "ETH", "LTC"], default_start_date=datetime.date(2022, 10, 31))
ingestor.ingest()