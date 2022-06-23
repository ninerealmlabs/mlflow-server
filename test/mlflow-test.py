#%%
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

#%%
# Function just to make a bit of mock data
def make_data(data_size=100):
    X0_var1 = [np.random.randint(0,5) for x in range(0,data_size)]
    X0_var2 = [np.random.randint(0,100) for x in range(0,data_size)]
    y0 = [0 for x in range(0,data_size)]
    df0 = pd.DataFrame({'var1':X0_var1,'var2':X0_var2,'y':y0})
    X1_var1 = [np.random.randint(4,10) for x in range(0,data_size)]
    X1_var2 = [np.random.randint(80,200) for x in  range(0,data_size)]
    y1 = [1 for x in range(0,data_size)]
    df1 = pd.DataFrame({'var1':X1_var1,'var2':X1_var2,'y':y1})
    df = df0.append(df1)
    df = df.sample(frac=1)
    df = df.reset_index(drop=True)
    return df

#%%
mlflow.set_tracking_uri('http://localhost:5555')
mlflow.set_experiment("test")

df = make_data(100)
X_train, X_test, y_train, y_test = train_test_split(df[['var1','var2']], df[['y']], test_size=0.33, random_state=42)

with mlflow.start_run():
    print(f"{mlflow.get_artifact_uri()=}")
    print(f"{mlflow.get_registry_uri()=}")

    n_estimators = 200
    model = RandomForestClassifier(n_estimators=n_estimators)
    mlflow.log_param(key="n_estimators", value=n_estimators)
    model.fit(X_train,y_train)

    y_predict = model.predict(X_test)

    results_table = pd.DataFrame(
      classification_report(y_test, y_predict,output_dict=True)
    )
    weighted_avg_f1 = results_table['weighted avg'].loc['f1-score']

    mlflow.sklearn.log_model(model, f"model")
    mlflow.log_metrics({"weighted_avg_f1": weighted_avg_f1})

    pd.DataFrame(y_predict).to_csv('predictions.csv')
    mlflow.log_artifact('predictions.csv')
# %%
