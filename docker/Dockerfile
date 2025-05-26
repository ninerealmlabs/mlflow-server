ARG SOURCE_IMAGE=python:3.11-slim-bullseye
# hadolint ignore=DL3006
FROM "${SOURCE_IMAGE}"

# Labels
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
ENV BUILD_DATE=${BUILD_DATE}
ENV VCS_REF=${VCS_REF}
ENV VERSION=${VERSION}
LABEL org.opencontainers.image.title="mlflow-server"
LABEL org.opencontainers.image.source="https://github.com/ninerealmlabs/mlflow-server"
LABEL org.opencontainers.image.description="A containerized mlflow tracking server"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.revision="${VCS_REF}"


SHELL ["/bin/bash", "-o", "pipefail", "-c"]
EXPOSE 5000

USER root

ENV VIRTUAL_ENV=/app/venv
RUN <<EOF
groupadd --gid 10001 mlflow
useradd --uid 10001 --gid mlflow --shell /bin/bash --create-home mlflow
mkdir -p /app/mlruns
python -m venv $VIRTUAL_ENV
chown -R mlflow:mlflow /app
EOF

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

VOLUME /app
WORKDIR /app
ENV MLFLOW_HOST=0.0.0.0
ENV MLFLOW_PORT=5000

RUN <<EOF
apt-get update -yq
apt-get upgrade -yq
apt-get install -yq \
    gcc \
    g++ \
    libpq-dev \
    libyaml-cpp-dev \
    libyaml-dev \
    nano
apt-get autoremove
apt-get clean
rm -rf /var/lib/apt/lists/*
EOF

USER mlflow
COPY --chown=mlflow requirements.txt ./
COPY --chown=mlflow scripts/ ./
RUN <<EOF
chmod +x ./*.py ./*.sh ./*.sql
python3 -m venv $VIRTUAL_ENV
./venv/bin/python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel
./venv/bin/python3 -m pip install --no-cache-dir --quiet --requirement ./requirements.txt
./venv/bin/python3 -m pip cache purge
EOF

ENTRYPOINT ["mlflow"]
CMD ["server"]
# COPY run.sh ./
# ENTRYPOINT mlflow server --host 0.0.0.0 --port 5000
# CMD ["--backend-store-uri $MLFLOW_BACKEND_STORE_URI", \
#      "--default-artifact-root $MLFLOW_DEFAULT_ARTIFACT_ROOT", \
#      "--serve-artifacts"]
# ENTRYPOINT ["/bin/bash", "run.sh"]
