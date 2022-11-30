# OOP Data Ingestion Tests

## Pytest
Every test needs to be in /tests and each file needs to have 'test' in its filename.

### Running
To run
```bash
$ python -m pytest
```

To run with code coverage (pytest-cov package)
```bash
$ python -m pytest --cov=mercado_bitcoin tests/
``` 

## Makefile

```make init```

## Poetry

```poetry init```

```poetry config virtualenvs.create true --local```

```poetry config virtualenvs.in-project true --local```

```
poetry add requests
poetry add schedule
poetry add ratelimit
poetry add backoff
```

### Installing a 'dev' dependency in poetry
```
poetry add --dev black
```

Toml Python Env
MacOS
```
$ source .venv/bin/activate
```

## Black - code formating
```
$ black .
```

# References

## AWS

### Setup
1. Create S3 bucket
2. Check Dynamo Table doesn't exist

### APIs

#### S3

##### To handle with S3 - boto
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

#### DynamoDB

##### To handle with DynamoDB - pynamodb
https://github.com/pynamodb/PynamoDB

# TO DO

[ ] build a container for this app