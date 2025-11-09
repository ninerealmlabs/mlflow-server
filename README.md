# MLflow-server

This repo provides a MLflow container intended for robust [self-hosted deployment](https://mlflow.org/docs/latest/self-hosting/), where the MLflow container serves as the tracking server, with (optional but recommended) external Artifact and Backend Stores. This readme details the recommended configuration.

> ⚠️ Deprecation Notice: No longer updating DockerHub repository ⚠️
>
> Due to March 2023 removal of Docker's free Teams organization & history of price changes,
> images will no longer be pushed to DockerHub.
> Please use `ghcr.io/ninerealmlabs/mlflow-server:<tag>`

## Quickstart

The [`quickstart` directory](./quickstart) provides a sample docker compose deployment, demonstrating MLflow Server, MLflow AI Gateway, and using S3 and Postgres as Artifact and Backend Stores respectively.

## Experiment Tracking Server

The [MLflow Tracking Server](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/) hosts the MLflow UI and proxies connections to the Artifact and Backend Stores.

### Artifact Store

The [Artifact Store](https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/) is the storage location for the _artifacts_ created by each run (model weights, images (.jpeg, .png), and model and data files). MLflow supports a variety of object storage solutions (S3, blob, network-accessible storage, etc.)

### Backend Store

The [Backend Store](https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/) persists MLflow entities and metadata (_runs_, parameters, metrics, tags, notes, etc.) to a relational database.

### Configuration

Configuration is done by setting environmental variables. Generally, environmental variables are equivalent to [mlflow-server cli commands](https://mlflow.org/docs/latest/cli.html#mlflow-server) with "MLFLOW" prefix, all-caps, and underscores (i.e., `--serve-artifacts` would become `MLFLOW_SERVE_ARTIFACTS`).

Options for storage are specified in the [tracking server documentation](https://mlflow.org/docs/latest/tracking/artifacts-stores.html#supported-storage-types-for-the-artifact-store)

### Network security middleware

Review the [network hardening guide](https://mlflow.org/docs/latest/self-hosting/security/network/) and configure the container with explicit settings. The compose example accepts overrides via `.env`:

```yaml
MLFLOW_SERVER_ALLOWED_HOSTS=mlflow.example.com,localhost:5555 MLFLOW_SERVER_CORS_ALLOWED_ORIGINS=https://app.example.com
MLFLOW_SERVER_X_FRAME_OPTIONS=DENY
...
```

Adjust these to match the domains that should reach the tracking server. Set `MLFLOW_SERVER_X_FRAME_OPTIONS=NONE` only when the UI must be embedded cross-origin, and avoid overriding `MLFLOW_SERVER_ALLOWED_HOSTS` with `*` outside of local development.

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

This container can also be used to deploy the [MLflow AI Gateway](https://mlflow.org/docs/latest/genai/governance/ai-gateway/). The AI Gateway provides a central interface for deploying and managing multiple LLM providers, and supports the [prompt engineering UI](https://mlflow.org/docs/latest/genai/prompt-registry/prompt-engineering/).

Follow the instructions in the [AI Gateway Configuration documentation](https://mlflow.org/docs/latest/genai/governance/ai-gateway/configuration/) to create a `config.yaml` file with the specifications for the AI API services that will be routed through the AI Gateway.
