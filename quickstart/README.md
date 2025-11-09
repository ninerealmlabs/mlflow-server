# Quickstart

## Deploy

```sh
cd quickstart
docker compose up
```

## Use `mlflow-server` as remote MLflow instance

From a local python runtime with at least `ipykernel`, `mlflow`, `pandas`, and `scikit-learn` installed, run [try-mlflow.py](try-mlflow.py), replacing `tracking_uri` with the address of the running `mlflow-server` instance.

```sh
uv venv
source ./venv/bin/activate
uv pip install mlflow pandas scikit-learn ipykernel
uv pip install openai # for MLflow AI Gateway
```
