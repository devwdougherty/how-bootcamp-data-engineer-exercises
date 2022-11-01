from abc import ABC, abstractmethod

import requests
import logging

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
    """
    @abstractmethod
    def _get_endpoint(self) -> str:
        pass
        #return f"{self.base_endpoint}/{self.coin}/day-summary/2022/10/31"

    def get_data(self) -> dict:
        endpoint = self._get_endpoint()
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status() # requests library -> raise_for_status verifies if it is an OK success return.
        return response.json()

class BtcApi(MercadoBitcoinApi):
    def _get_endpoint(self) -> str:
        return "a"

BtcApi(coin="BTC")