from abc import ABC, abstractmethod
from typing import List

import logging
import datetime

from mercado_bitcoin.checkpoint import DynamoCheckpoints, CheckpointModel

from mercado_bitcoin.apis import DaySummaryApi
from mercado_bitcoin.writers import DataWriter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DataIngestor(ABC):
    def __init__(
        self, coins: List[str], default_start_date: datetime.date, writer: DataWriter
    ) -> None:
        self.coins = coins
        self.default_start_date = default_start_date
        self.writer = writer
        self._checkpoint = self._load_checkpoint()

    @property
    def _checkpoint_filename(self) -> str:
        # __name__ get the python class name or 'main'
        return f"{self.__class__.__name__}.checkpoint"

    def _write_checkpoint(self):
        with open(self._checkpoint_filename, "w") as f:
            f.write(f"{self._checkpoint}")

    def _load_checkpoint(self) -> datetime.date:
        try:
            with open(self._checkpoint_filename, "r") as f:
                return datetime.datetime.strptime(f.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return self.default_start_date

    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        else:
            return self._checkpoint

    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()

    @abstractmethod
    def ingest(self) -> None:
        pass


class DaySummaryIngestor(DataIngestor):
    def ingest(self) -> None:
        date = self._get_checkpoint()
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
                self._update_checkpoint(date + datetime.timedelta(days=1))


class AWSDataIngestor(ABC):
    def __init__(
        self, coins: List[str], default_start_date: datetime.date, writer: DataWriter
    ) -> None:
        self.dynamodb_checkpoint = DynamoCheckpoints(
            model=CheckpointModel,
            report_id=self.__class__.__name__,
            default_start_date=default_start_date,
        )
        self.coins = coins
        self.default_start_date = default_start_date
        self.writer = writer
        self._checkpoint = self._load_checkpoint()

    def _load_checkpoint(self) -> datetime.date:
        return self.dynamodb_checkpoint.get_checkpoint()

    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        else:
            return self._checkpoint

    def _update_checkpoint(self, value):
        self._checkpoint = value
        self.dynamodb_checkpoint.create_or_update_checkpoint(checkpoint_date=self._checkpoint)

    @abstractmethod
    def ingest(self) -> None:
        pass


class AWSDaySummaryIngestor(AWSDataIngestor):
    def ingest(self) -> None:
        date = self._get_checkpoint()
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
                self._update_checkpoint(date + datetime.timedelta(days=1))
