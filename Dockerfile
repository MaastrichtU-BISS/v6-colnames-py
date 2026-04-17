# Self-contained Python base image so the build does not depend on the
# vantage6 Harbor registry being reachable.
FROM python:3.10-slim

# This is a placeholder that should be overloaded by invoking
# docker build with '--build-arg PKG_NAME=...'
ARG PKG_NAME="v6-colnames-py"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PKG_NAME=${PKG_NAME}

WORKDIR /app

# arm/v7 may need to build numpy/pandas from source because binary wheels are
# not always available. Install the native toolchain and BLAS/LAPACK headers
# needed for that fallback path.
RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
        build-essential \
        gfortran \
        libopenblas-dev \
        liblapack-dev \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install only the runtime pieces required by the 4.14.0 wrapper path.
# The Harbor base image normally bundles these, but the wrapper itself only
# needs Python plus the algorithm-tools stack.
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

# install federated algorithm itself without re-resolving runtime deps
COPY . /app
RUN pip install --no-deps /app

# Tell docker to execute `wrap_algorithm()` when the image is run.
CMD ["python", "-c", "from vantage6.algorithm.tools.wrap import wrap_algorithm; wrap_algorithm()"]
