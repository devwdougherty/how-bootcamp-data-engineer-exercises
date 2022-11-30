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

from ingestors import DaySummaryIngestor, AWSDaySummaryIngestor
from writers import DataWriter, S3Writter

# __name__ get the python file name or 'main'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    #day_summary_ingestor = DaySummaryIngestor(
    day_summary_ingestor = AWSDaySummaryIngestor(
        # writer=DataWriter,
        writer=S3Writter,
        coins=["BTC", "ETH", "LTC"],
        default_start_date=datetime.date(2022, 9, 1),
    )

    @repeat(every(1).seconds)
    def job():
        day_summary_ingestor.ingest()

    while True:
        run_pending()
        time.sleep(0.5)


"""
day_summary_data = DaySummaryApi(coin="BTC").get_data(date=datetime.date(2022, 10, 30))
writer = DataWriter('day_summary.json')
writer.write(day_summary_data)

trades_data = TradesApi(coin="BTC").get_data()
writer = DataWriter('trades.json')
writer.write(trades_data)
"""

# print(DaySummaryApi(coin="BTC").get_data(date=datetime.date(2022, 10, 31)))
# print(TradesApi(coin="BTC").get_data())
# print(TradesApi(coin="BTC").get_data(date_from=datetime.datetime(2022, 10, 25)))
# print(TradesApi(coin="BTC").get_data(date_from=datetime.datetime(2022, 10, 25), date_to=datetime.datetime(2022, 10, 26)))
