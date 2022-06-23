#!/bin/bash
mlflow server \
  --host 0.0.0.0 \
  --port 5555 \
  --gunicorn-opts '--log-level debug' \
  --backend-store-uri "$MLFLOW_BACKEND_STORE_URI" \
  --default-artifact-root "$MLFLOW_DEFAULT_ARTIFACT_ROOT"