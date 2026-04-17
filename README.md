<h1 align="center">
  <br>
  <a href="https://vantage6.ai"><img src="https://github.com/IKNL/guidelines/blob/master/resources/logos/vantage6.png?raw=true" alt="vantage6" width="400"></a>
</h1>

<h3 align="center">A privacy preserving federated learning solution</h3>

---

# v6-colnames-py

This repository contains a Vantage6 algorithm that collects the column names of
the datasets made available by all organizations in a collaboration and returns:

- the column names per organization
- the sorted intersection of column names in `common`

This version targets Vantage6 `4.14.0`.

## What changed for Vantage6 4.14.0

The algorithm was upgraded from the legacy 3.x container interface to the 4.x
algorithm-tools interface:

- the Docker image now uses `vantage6.algorithm.tools.wrap.wrap_algorithm()`
- the algorithm uses `@algorithm_client` and `@data()` decorators
- child tasks are created with `client.task.create(...)`
- results are collected with `client.wait_for_results(...)`
- the local mock test uses `MockAlgorithmClient`

## Dockerfile contract

For Vantage6 4.x, the image only needs Python plus the `wrap_algorithm`
entrypoint. This repository therefore uses a self-contained Dockerfile and does
not depend on `harbor2.vantage6.ai/algorithms/algorithm-base`:

```dockerfile
FROM python:3.10-slim

ARG PKG_NAME="v6-colnames-py"

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
        build-essential \
        gfortran \
        libopenblas-dev \
        liblapack-dev \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel && \
    pip install \
        "openpyxl>=3.0.0" \
        "pandas>=1.5.3" \
        "pyfiglet==1.0.4" \
        "pyjwt==2.12.1" \
        "SPARQLWrapper>=2.0.0" \
        "sqlalchemy==1.4.46" \
        "vantage6-common==4.14.0" \
        "vantage6-algorithm-tools==4.14.0"

COPY . /app
RUN pip install --no-deps /app

ENV PKG_NAME=${PKG_NAME}

CMD python -c "from vantage6.algorithm.tools.wrap import wrap_algorithm; wrap_algorithm()"
```

## Local test

The local test uses the 4.x mock client and in-memory pandas dataframes:

```bash
python -m pytest test.py
```

## Example researcher script

The `run.py` file contains an example of creating a task from the Python client
using the 4.14.0 API:

```bash
python run.py
```

You will need to adapt the server URL, credentials, collaboration, and image
name to your own infrastructure.

## Result shape

The master task returns a JSON-serializable object like:

```json
{
  "organization_101": {
    "organization_id": 101,
    "node_id": 11,
    "columns": ["age", "patient_id"]
  },
  "organization_202": {
    "organization_id": 202,
    "node_id": 22,
    "columns": ["age", "patient_id", "site"]
  },
  "common": ["age", "patient_id"]
}
```

## Read more

- Documentation: https://docs.vantage6.ai/
- Source code: https://github.com/vantage6/vantage6
