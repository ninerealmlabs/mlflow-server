#%%
import os

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

#%%
# load the iris dataset and split it into train and test sets
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

#%%
tracking_uri = "http://localhost:5555"
mlflow.set_tracking_uri(tracking_uri)
mlflow.set_experiment("iris-test")

#%%
# ### NOTE: env vars required for scenario 4 but not for scenario 5
# os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://localhost:9000"
# os.environ['AWS_ACCESS_KEY_ID'] = "miniomlflow"
# os.environ['AWS_SECRET_ACCESS_KEY'] = "miniomlflow"
# os.environ['AWS_DEFAULT_REGION'] = "us-east"

# # check whether env vars set
# mlflow_env = {env: os.environ[env] for env in os.environ if env.startswith("MLFLOW")}
# aws_env = {env: os.environ[env] for env in os.environ if env.startswith("AWS")}
# print(mlflow_env)
# print(aws_env)


#%%
with mlflow.start_run():
    print(f"{mlflow.get_artifact_uri()=}")
    print(f"{mlflow.get_registry_uri()=}")

    n_estimators = 42
    # create a pipeline object
    pipe = make_pipeline(
        StandardScaler(),
        RandomForestClassifier(n_estimators=n_estimators),
    )
    mlflow.log_param(key="preprocess", value="StandardScaler")
    mlflow.log_param(key="n_estimators", value=n_estimators)

    # fit the whole pipeline
    pipe.fit(X_train, y_train)

    # preserve model object
    mlflow.sklearn.log_model(pipe, f"pipeline_model")

    # predict and assess
    y_predict = pipe.predict(X_test)
    accuracy = accuracy_score(y_test, y_predict)
    f1 = f1_score(y_test, y_predict, average="macro")
    mlflow.log_metrics(
        {
            "accuracy": accuracy,
            "f1": f1,
        }
    )

    # save artifact other than model
    pd.DataFrame(y_predict).to_csv("predictions.csv")
    mlflow.log_artifact("predictions.csv")
    # clean up
    os.remove("predictions.csv")

# %%
