set MLFLOW_TRACKING_URI = test
set MLFLOW_TRACKING_USERNAME = nul

docker build -t mlflow-docker-example ^
 --build-arg MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI$ ^
 --build-arg MLFLOW_TRACKING_USERNAME=$MLFLOW_TRACKING_USERNAME$ ^
 .
mlflow run .