# MLflow-server

> ⚠️ Deprecation Notice: No longer updating Dockerhub repository ⚠️
>
> Due to March 2023 removal of Docker's free Teams organization & history of price changes,
> images will no longer be pushed to DockerHub.
> Please use `ghcr.io/ninerealmlabs/mlflow-server:<tag>`

## Tracking Server

[MLflow](https://mlflow.org) provides for diverse [tracking server configurations](https://mlflow.org/docs/latest/tracking.html#common-setups);
among them are:

- MLflow as remote Tracking Server, providing tracking backend and proxied access to artifact stores
- MLflow as Artifact Server only, providing proxied access to artifacts but no tracking
- MLflow Tracking Server only, and requiring direct access to the artifact store.
  In this configuration, the user must manage their direct connection to the artifact store

MLflow uses two components for storage: backend store and artifact store.
The **backend store** persists MLflow entities (_runs_, parameters, metrics, tags, notes, metadata, etc), and
these data can be recorded to local files, to a SQLAlchemy compatible database, or remotely to a tracking server
The **artifact store** persists _artifacts_ (files, models, images, in-memory objects, or model summary, etc)
to local files or a variety of remote file storage solutions.

```yaml
version: 3
services:
...
  mlflow:
    image: ghcr.io/ninerealmlabs/mlflow-server:<latest>
    ...
    command:
      - "server"
      - "--host=0.0.0.0"
      - "--port=5000"
      - "--backend-store-uri=postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASS:-postgres}@postgres:5432/${DB_NAME:-mlflow}"
      - "--serve-artifacts"
      - "--artifacts-destination=s3://${BUCKET_NAME:-mlflow}"
```

### Quickstart

```sh
cd quickstart
docker compose up
```

#### Use `mlflow-server` as remote MLflow instance

From a local python runtime with at least `mlflow`, `pandas`, and `scikit-learn` installed,
run [try-mlflow.py](try-mlflow.py), replacing `tracking_uri` with the address of the running `mlflow-server` instance

### Configuration

Configuration is done by setting environmental variables in [docker-compose.yaml](docker-compose.yaml).

Generally, environmental variables are equivalent to [mlflow-server cli commands](https://mlflow.org/docs/latest/cli.html#mlflow-server)
with "MLFLOW" prefix, capslock, and underscores (i.e., `--serve-artifacts` would become `MLFLOW_SERVE_ARTIFACTS`).

Options for storage are specified in the [tracking server documentation](https://mlflow.org/docs/latest/tracking/artifacts-stores.html#supported-storage-types-for-the-artifact-store)

### Database migrations

When upgrading MLflow, it is possible that a database migration will be required.
`mlflow` provides a command for this; run it from the tracking server container.

```sh
mlflow db upgrade "$MLFLOW_BACKEND_STORE_URI"
```

### Cleaning up deleted experiments

- Run `mlflow gc` in the mlflow container to clean up deleted runs and artifacts (this retains the experiment).
  The python script `cleanup-runs.py` may also be used to clean up runs from the database (this may orphan the artifacts).
  See more: [[BUG] gc fails with postgres backend, violates foreign key constraint · Issue #13254 · mlflow/mlflow](https://github.com/mlflow/mlflow/issues/13254)
- Run the python script `cleanup-experiments.py` to fully delete experiments from the database

## Gateway Server

This container can also be used to deploy the [MLflow AI Gateway](https://mlflow.org/docs/latest/llms/deployments/index.html)
Follow the instructions in the MLflow documentation to create a `config.yaml` file
with the specifications for the AI API services that will be routed through the AI Gateway.

```yaml
version: 3
services:
...
  mlflow:
    image: ghcr.io/ninerealmlabs/mlflow-server:<latest>
    ...
    environment:
      OPENAI_API_KEY: ...
      MLFLOW_DEPLOYMENTS_CONFIG: /app/config.yaml
    volumes:
      - ${PWD}/config.yaml:/app/config.yaml
    command:
      - "gateway"
      - "--host=0.0.0.0"
      - "--port=5000"
      - "--config-path /app/config.yaml"
```
