from mercado_bitcoin.ingestors import AWSDaySummaryIngestor
from mercado_bitcoin.writers import S3Writter

import datetime
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

'''
    lambda_handler -> name convention
    event, context -> var names convetion
'''
def lambda_handler(event, context):
    logger.info(f"{event}")
    logger.info(f"{context}")

    AWSDaySummaryIngestor(
        writer=S3Writter,
        coins=["BTC", "ETH", "LTC"],
        default_start_date=datetime.date(2022, 9, 1),
    ).ingest()
