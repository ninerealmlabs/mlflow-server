#!/usr/bin/env bash
docker buildx create --use --name builder;
docker buildx build \
  --tag="ninerealmlabs/mlflow-server:latest" \
  --load \
  .

  # --progress=plain \
  # --platform="linux/amd64" \

docker run \
  --rm \
  -p 5555:5555 \
  --env
  ninerealmlabs/mlflow-server:latest


docker run \
  --rm \
  -it \
  -p 5555:5000 \
  ninerealmlabs/mlflow-server:latest sh
