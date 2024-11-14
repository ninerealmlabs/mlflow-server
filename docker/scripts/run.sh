#!/bin/bash

cmd="mlflow server --port 5555"

# required params
backend="--backend-store-uri ${MLFLOW_BACKEND_STORE_URI:?Error - MLFLOW_BACKEND_STORE_URI must be provided}"
artifact="--default-artifact-root ${MLFLOW_DEFAULT_ARTIFACT_ROOT:?Error - MLFLOW_DEFAULT_ARTIFACT_ROOT must be provided}"

# server params
if [[ -z "$MLFLOW_HOST" ]]; then
    host=""
else
    host="--host ${MLFLOW_HOST:-0.0.0.0}"
fi

if [[ -z "$MLFLOW_WORKERS" ]]; then
    workers=""
else
    workers="--workers ${MLFLOW_WORKERS}"
fi

# optional params
if [[ -z "$MLFLOW_ARTIFACTS_DESTINATION" ]]; then
    destination=""
else
    destination="--artifacts-destination ${MLFLOW_ARTIFACTS_DESTINATION}"
fi

if [[ -z "$MLFLOW_STATIC_PREFIX" ]]; then
    prefix=""
else
    prefix="--static-prefix ${MLFLOW_STATIC_PREFIX}"
fi

if [[ -z "$MLFLOW_SERVE_ARTIFACTS" ]]; then
    serve=""
else
    serve="--serve-artifacts"
fi

if [[ -z "$MLFLOW_ARTIFACTS_ONLY" ]]; then
    only=""
else
    only="--artifacts-only"
fi

if [[ -z "$MLFLOW_GUNICORN_OPTS" ]]; then
    gopts=""
else
    gopts="--gunicorn-opts ${MLFLOW_GUNICORN_OPTS}"
fi

if [[ -z "$MLFLOW_WAITRESS_OPTS" ]]; then
    wopts=""
else
    wopts="--waitress-opts ${MLFLOW_WAITRESS_OPTS}"
fi

if [[ -z "$MLFLOW_EXPOSE_PROMETHEUS" ]]; then
    prom=""
else
    prom="--expose-prometheus ${MLFLOW_EXPOSE_PROMETHEUS}"
fi

run_cmd="$cmd \
    $host \
    $workers \
    $backend \
    $artifact \
    $destination \
    $prefix \
    $serve \
    $only \
    $gopts \
    $wopts \
    $prom"
run_cmd=$(echo "$run_cmd" | xargs)
echo "$run_cmd"
eval "$run_cmd"
