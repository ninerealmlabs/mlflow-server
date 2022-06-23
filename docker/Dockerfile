FROM python:3.9-bullseye


EXPOSE 5555

RUN mkdir -p /mnt/filestore
VOLUME /mnt/filestore

WORKDIR /
COPY . /

RUN apt-get update -yq \
 && apt-get upgrade -yq \
 && apt-get install -yq \
    libyaml-cpp-dev \
    libyaml-dev \
    nano \
 && apt-get autoremove \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
 && pip install --quiet \
   # --root-user-action=ignore \
   # -r requirements.txt  \
   mlflow==1.26.1 \
   psycopg2 \
   pg8000 \
   azure-identity \
   azure-storage-common \
   azure-storage-blob \
   azure-storage-file-share \
   boto3 \
   google-cloud-storage \
   pysftp \
 && pip cache purge

# ENTRYPOINT mlflow server --host 0.0.0.0 --port 5555
# CMD ["--backend-store-uri $MLFLOW_BACKEND_STORE_URI", \
#      "--default-artifact-root $MLFLOW_DEFAULT_ARTIFACT_ROOT", \
#      "--serve-artifacts"]
ENTRYPOINT ["/bin/bash", "run.sh"]
