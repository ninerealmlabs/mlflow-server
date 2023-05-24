ARG SOURCE_IMAGE=python:3.10-slim-bullseye
# hadolint ignore=DL3006
FROM "${SOURCE_IMAGE}"

# Labels
ARG BUILD_DATE
ARG GIT_COMMIT
ARG VERSION
ENV BUILD_DATE=${BUILD_DATE}
ENV GIT_COMMIT=${GIT_COMMIT}
ENV VERSION=${VERSION}
LABEL maintainer="ninerealmlabs"
# hadolint ignore=DL3053
LABEL build-date="${BUILD_DATE}"
# hadolint ignore=DL3055
LABEL git-commit="${GIT_COMMIT}"
# hadolint ignore=DL3056
LABEL version="${VERSION}"
LABEL description="MLFlow-server"

# EXPOSE 5555
EXPOSE 5000

WORKDIR /

RUN apt-get update -yq \
 && apt-get upgrade -yq \
 && apt-get install -yq \
    gcc \
    g++ \
    libpq-dev \
    libyaml-cpp-dev \
    libyaml-dev \
    nano \
 && apt-get autoremove \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir --quiet -r requirements.txt \
 && pip cache purge

COPY run.sh ./
# ENTRYPOINT mlflow server --host 0.0.0.0 --port 5555
# CMD ["--backend-store-uri $MLFLOW_BACKEND_STORE_URI", \
#      "--default-artifact-root $MLFLOW_DEFAULT_ARTIFACT_ROOT", \
#      "--serve-artifacts"]
# ENTRYPOINT ["/bin/bash", "run.sh"]
