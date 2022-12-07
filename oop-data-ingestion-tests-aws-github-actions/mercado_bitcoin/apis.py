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

    # return f"{self.base_endpoint}/{self.coin}/day-summary/2022/10/31"

    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()  # requests library -> raise_for_status verifies if it is an OK success return.
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
        #return int(date.timestamp())
        return int((date - datetime.datetime(1970, 1, 1)).total_seconds())  # Fixing to not get the default timezone of my region, but the original timestamp.

    def _get_endpoint(
        self, date_from: datetime.datetime = None, date_to: datetime.datetime = None
    ) -> str:

        if date_from and not date_to:
            unix_date_from = self.convert_date_to_unix(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"
        elif date_from and date_to:

            if date_from > date_to:
                raise RuntimeError("date_from cannot be greater than date_to")

            unix_date_from = self.convert_date_to_unix(date_from)
            unix_date_to = self.convert_date_to_unix(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"

        return endpoint
