# MLflow-server

[MLflow](https://mlflow.org) posits 6 scenarios for use:

1. MLflow on localhost
2. MLflow on localhost with SQLite
3. MLflow on localhost with Tracking Server
4. MLflow with remote Tracking Server, backend and artifact stores
5. MLflow Tracking Server enabled with proxied artifact storage access
6. MLflow Tracking Server used exclusively as proxied access host for artifact storage access

Given this creates a docker container to run an MLflow server, this repo will prioritize scenarios 4-6.
However, "local" storage in container directory `/mlruns` is possible, but will require using docker volume mounts
to configure persistence and be fraught with permissions considerations.

MLflow uses two components for storage: backend store and artifact store.
The backend store persists MLflow entities (_runs_, parameters, metrics, tags, notes, metadata, etc), and
these data can be recorded to local files, to a SQLAlchemy compatible database, or remotely to a tracking server

The artifact store persists _artifacts_ (files, models, images, in-memory objects, or model summary, etc)
to local files or a variety of remote file storage solutions.

## Quickstart

## Use `mlflow-server` as remote MLflow instance

From a local python runtime with at least `mlflow`, `pandas`, and `scikit-learn` installed,
run [try-mlflow.py](try-mlflow.py), replacing `tracking_uri` with the address of the running `mlflow-server` instance

## Configuration

Configuration is done by setting environmental variables in [docker-compose.yaml](docker-compose.yaml).

Generally, environmental variables are equivalent to [mlflow-server cli commands](https://mlflow.org/docs/latest/cli.html#mlflow-server)
with "MLFLOW" prefix, capslock, and underscores (i.e., `--serve-artifacts` would become `MLFLOW_SERVE_ARTIFACTS`).
For more, see [run.sh](docker/run.sh)

> The only `mlflow-server` cli command that cannot be configure is the port mapping,
> as that will be handled by the container runtime.
> This mlflow-server exposes port 5555.

Options for storage are as follows (or see [.env.tmpl](.env.tmpl)):

```ini
### environmental variables for docker-compose ###
### https://mlflow.org/docs/latest/tracking.html ###

### Backend Store (Database)
# In order to use model registry functionality, you must run your server using a database-backed store.
MLFLOW_BACKEND_STORE_URI="<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>"

### Artifact Store
# The artifact store is a location suitable for large data and
# is where clients log their artifact output (for example, models)

### aws/s3
MLFLOW_DEFAULT_ARTIFACT_ROOT="s3://<bucket>/<path>"

# if using custom s3 endpoint
MLFLOW_S3_ENDPOINT_URL=""
MLFLOW_S3_IGNORE_TLS=true
# MLFLOW_S3_UPLOAD_EXTRA_ARGS='{"ServerSideEncryption": "aws:kms", "SSEKMSKeyId": "1234"}'

AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_DEFAULT_REGION="us-east"

### azure
MLFLOW_DEFAULT_ARTIFACT_ROOT="wasbs://<container>@<storage-account>.blob.core.windows.net/<path>"
AZURE_STORAGE_CONNECTION_STRING=""
AZURE_STORAGE_ACCESS_KEY=""

### Google Cloud Storage
MLFLOW_DEFAULT_ARTIFACT_ROOT="gs://<bucket>/<path>"
MLFLOW_GCS_DEFAULT_TIMEOUT=""

### FTP
MLFLOW_DEFAULT_ARTIFACT_ROOT="ftp://<user>:<pass>@<host/path/to/directory>"

### SFTP
# ensure clients can log into sftp server without password over ssh (public key, identity file in ssh_config, ...)
MLFLOW_DEFAULT_ARTIFACT_ROOT="sftp://<user>@<host/path/to/directory>"

### NFS
# This path must be the same on both the server and the client –
# may need to use symlinks or remount the client in order to enforce this property.
MLFLOW_DEFAULT_ARTIFACT_ROOT="<path>"
```
