# data ingestion service

## AWS 

### Services
- Kinesis Firehose
- AWS Glue (Crawler + Database)
- AWS Athena

### Setup

1. Create the S3 bucket that is going to receive the data from Delivery Stream.
2. Create the Kinesis Firehose delivery stream.
3. Create the Glue crawler along Glue database.

## Run

1. Create and activate the python virtual env.
2. Install the requirements.txt.
3. Configure the AWS local credentials for your user.

```bash
aws config
````
4. Run the main.py script.
5. Run your AWS Crawler previously created.
6. Check the table created at Glue Database.
7. Run your SQL queries on Athena on your Glue table.

## AWS Cloud Architecture

[diagram]

## References
AWS
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

Boto3
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration

Fake Web Events
https://pypi.org/project/fake-web-events/