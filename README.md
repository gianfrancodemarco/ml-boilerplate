ml-boilerplate
==============================

A Python ML boilerplate based on Cookiecutter Data Science, providing support for data versioning (DVC), experiment tracking, Model&Dataset cards, etc.

<br/>

## Table of Contents
1. [Cookiecutter](#cookiecutter)
    1. [Cookiecutter Data science Setup](#cookiecutter-data-science-setup)
    2. [Project Organization](#project-organization)
3. [DVC](#dvc)
    1. [DVC setup (Windows)](#dcv-setup-windows)
    2. [DVC usage](#dvc-usage)
    3. [Troubleshooting](#troubleshooting)
4. [MLFlow](#mlflow)

<br/>

## Cookiecutter

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) is a command-line utility that creates projects from cookiecutters (project templates), e.g. creating a Python package project from a Python package project template.

<br/>

### Cookiecutter Data science Setup

This project was created with the following steps:
1) [Installing](https://cookiecutter.readthedocs.io/en/stable/installation.html) cookiecutter on the host machine with PiP

    `python3 -m pip install --user cookiecutter`

2) [Initializing](https://drivendata.github.io/cookiecutter-data-science/) the project directly from github:

    `python -m cookiecutter https://github.com/drivendata/cookiecutter-data-science`

3) Filling in the required information
4) Creating a github repository from the Web Interface and adding it as remote:

    `
    echo "# ml-boilerplate" >> README.md
    git init
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin https://github.com/gianfrancodemarco/ml-boilerplate.git
    git push -u origin main
    `

<br/>
<br/>

### Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<br/>
<br/>

## DVC

Data Version Control is a data versioning, ML workflow automation, and experiment management tool that takes advantage of the existing software engineering toolset you're already familiar with (Git, your IDE, CI/CD, 
etc.). 

DVC will:

- upload the data files to a remote (the data files will be ignored by GIT)
- create pointers (.dvc files) to those files (the pointers will be stored in GIT)

<br/>

### DCV setup (Windows)
<br/>

1) Install DVC

    `pip install dvc`

2) Init DVC

    `dvc init`

3) Use `dvc get` to download a sample dataset (Optional) 
    
    `dvc get https://github.com/iterative/dataset-registry get-started/data.xml -o data/raw/data.xml`

4) Add a DVC remote (Google Drive)

    a) Create a folder for DVC on Google Drive
    b) Open the folder and grab the folder id from the url bar
    c) `dvc remote add -d storage gdrive://<folder_id>'

5) Push the data to the configured remote
    `dvc push`

<br/>

### DVC usage

<br/>

- Add data to DVC tracking:

    `dvc add <file_or_folder_to_track>`
    
    E.g: `dvc add data/raw`

    Then:
    
    `git add data\raw.dvc data\.gitignore`
    `git commit ...`
    `git push`
    `dvc push`

- Pull data from DVC

    `dvc pull`

- Checkout a previous DVC version
    
    1) git checkout to the desired version the .dvc file corresponding to the data we want to checkout
    2) `dvc checkout` 

<br/>


### Troubleshooting

- If pulling from gdrive fails with the error "file has been identified as malware or spam and cannot be 
downloaded dvc" run:

    `dvc remote modify <myremote> gdrive_acknowledge_abuse true`

<br/>

## MLFlow