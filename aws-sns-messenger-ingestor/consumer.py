import boto3

client = boto3.client('sqs')

response = client.receive_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/714363732047/consumer-created-payment-api'
)

print(response)