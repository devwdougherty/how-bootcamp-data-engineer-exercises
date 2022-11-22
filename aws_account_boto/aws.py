import logging
import boto3

from botocore import exceptions
from botocore.exceptions import ClientError

from dotenv import load_dotenv

from os import getenv

load_dotenv('.env')
getenv('AWS_ID')

s3_client = boto3.client(
    's3',
    aws_access_key_id = getenv('AWS_ID'),
    aws_secret_access_key = getenv('AWS_KEY')
)

def create_bucket(name):
    try:
        s3_client.create_bucket(Bucket=name)
    except ClientError as e:
        logging.error(e)
        
    return True

create_bucket('wdnb-s3-bucket-devwdougherty-how-bootcamp')