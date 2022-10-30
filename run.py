import subprocess
import sys

from dotenv import load_dotenv

load_dotenv(override=True)

# TODO Check if docker is up and running. If not exit with a verbose error message
# subprocess.run(["docker", "build", "-t", "mlflow-docker-example", "."], stderr=sys.stderr, stdout=sys.stdout)
# print("\nBuilt docker image.\nStarting mlflow run...\n")

subprocess.run(["mlflow", "run", "."], stderr=sys.stderr, stdout=sys.stdout)