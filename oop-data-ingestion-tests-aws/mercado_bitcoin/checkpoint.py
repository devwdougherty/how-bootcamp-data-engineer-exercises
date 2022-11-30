from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

from os import getenv

import logging
import datetime

from dotenv import load_dotenv

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

# env with AWS credentials
load_dotenv(".env")


class CheckpointModel(Model):
    class Meta:
        # credentials from env file not working here...
        # aws_access_key_id = str(getenv('AWS_ID')),
        # aws_secret_access_key = str(getenv('AWS_KEY'))
        aws_access_key_id = "AKIATUFPHB3EV3EBFMTE"
        aws_secret_access_key = "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"
        table_name = "mercado_bitcoin_ingestor_checkpoints"
        region = "us-east-1"

    report_id = UnicodeAttribute(hash_key=True)
    checkpoint_date = UnicodeAttribute()


class DynamoCheckpoints:
    def __init__(self, model: CheckpointModel, report_id: str, default_start_date: datetime.date):
        self.default_start_date = default_start_date
        self.model = model
        self.report_id = report_id
        self.create_table()

    def update_checkpoint(self, checkpoint_date):
        logger.info(f"Updating checkpoint")
        checkpoint = self.model.get(self.report_id)
        checkpoint.checkpoint_date = f"{checkpoint_date}"
        checkpoint.save()

    def create_or_update_checkpoint(self, checkpoint_date):
        logger.info(
            f"Saving/Updating checkpoint for {self.report_id}: {checkpoint_date}"
        )
        if not self.checkpoint_exist:
            self.create_checkpoint(checkpoint_date)
        else:
            self.update_checkpoint(checkpoint_date)

    def create_checkpoint(self, checkpoint_date):
        logger.info(f"Creating checkpoint")
        checkpoint = self.model(self.report_id, checkpoint_date=f"{checkpoint_date}")
        checkpoint.save()

    def get_checkpoint(self):
        if self.checkpoint_exist:
            checkpoint = list(self.model.query(self.report_id))[0].checkpoint_date
            logger.info(f"Checkpoint found for {self.report_id}: {checkpoint}")
            return datetime.datetime.strptime(checkpoint, "%Y-%m-%d").date()
        else:
            logger.info(f"Checkpoint not found for {self.report_id} using default_start_date")
            return self.default_start_date

    @property  # -> a decorator
    def checkpoint_exist(self):
        try:
            return list(self.model.query(self.report_id)) != []
        except KeyError:
            logger.warning(f"KeyError: {self.report_id}")
            return False

    def create_table(self):
        logger.info(f"Creating dynamo table")

        if not self.model.exists():
            self.model.create_table(billing_mode="PAY_PER_REQUEST", wait=True)


DynamoCheckpoints(
    model=CheckpointModel, report_id="abc", default_start_date=datetime.date(2022, 9, 1)
)
