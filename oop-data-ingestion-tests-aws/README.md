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

