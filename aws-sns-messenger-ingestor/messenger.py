import boto3
import json
import time

from datetime import datetime
from faker import Faker

client = boto3.client('sns')
faker_instance = Faker()

def get_data():
    lat, lng, region, country, timezone = faker_instance.location_on_land()
    return dict(
        created_at=f"{datetime.utcnow()}",
        updated_at=f"{datetime.utcnow()}",
        customer_id=faker_instance.uuid4(),
        name=faker_instance.name(),
        region=region,
        country=country,
        lat=lat,
        lng=lng,
        email=faker_instance.ascii_free_email(),
        phone=faker_instance.phone_number()
    )

while True:
    data = get_data()

    client.publish(
        TopicArn='arn:aws:sns:us-east-1:714363732047:created-consumer',
        Message=json.dumps(data)
    )

    print(data)
    time.sleep(1)