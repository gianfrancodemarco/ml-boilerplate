import subprocess
from os import system
from dotenv import load_dotenv

load_dotenv(override=True)
system("docker build -t mlflow-docker-example .")
system("mlflow run .")