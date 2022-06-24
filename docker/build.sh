#!/usr/bin/env bash
docker buildx create --use --name builder;
docker buildx build \
  --tag="ninerealmlabs/mlflow-server:latest" \
  --load \
  .
