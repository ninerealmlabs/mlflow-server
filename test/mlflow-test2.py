import mlflow

mlflow.set_tracking_uri('http://localhost:5555')
mlflow.set_registry_uri("https://truenas.ninerealmlabs.com:9000")   # replace
expr_name = "new_experiment_2"
s3_bucket = "S3://mlflow"  # replace

mlflow.create_experiment(expr_name, s3_bucket)
mlflow.set_experiment(expr_name)

with mlflow.start_run():
    # debug
    print(f"{mlflow.get_artifact_uri()=}")
    print(f"{mlflow.get_tracking_uri()=}")
    print(f"{mlflow.get_registry_uri()=}")

    mlflow.log_param("foo", 0)
    mlflow.log_metric("bar", 1)

    with open("test.txt", "w") as f:
        f.write("test")

    mlflow.log_artifact("test.txt")