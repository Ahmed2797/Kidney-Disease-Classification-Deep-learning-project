# Kidney-Disease-Classification-Deep-learning-project

## workflow

1. Update config.yaml
2. Update secrets.yaml [Optional]
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in project configuration
6. Update the components
7. Update the pipeline
8. Update the main.py
9. Update the dvc.yaml
10. app.py

How to run?

STEPS:

Clone the repository

    '''bash

    git clone https://github.com/Ahmed2797/Kidney-Disease-Classification-Deep-learning-project.git
    

    '''

STEP 01- Create a conda environment after opening the repository

    '''bash
    conda create -n kidney python=3.12

    conda config --set auto_activate_base false

    conda activate kidney

    conda deactivate

    deactivate  # Linux/Mac

    '''

STEP 02- install the requirements

    '''bash
    pip install -r requirements.txt

    pip install python-multipart

    '''

sudo apt  install tree

terminal >> tree -L 3

Project Structure

.
├── app.py
├── artifacts
│   └── data_ingestion
│       ├── data.zip
│       └── kidney-ct-scan-image
├── Kidney_Disease_Classification.egg-info
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── requires.txt
│   ├── SOURCES.txt
│   └── top_level.txt
├── notex.txt
├── project
│   ├── cloud
│   │   └── __init__.py
│   ├── components
│   │   ├── data_ingestion.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── configeration
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── constants
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── entity
│   │   ├── config.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── exception
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── __init__.py
│   ├── logger
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── pipeline
│   │   ├── 1_data_ingestion_pipeline.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── __pycache__
│   │   └── __init__.cpython-312.pyc
│   └── utils
│       ├── __init__.py
│       └── __pycache__
├── README.md
├── recsearch
│   ├── 0_try.ipynb
│   └── 1_data_ingestion.ipynb
├── requirements.txt
├── setup.py
├── templates.sh
└── yamlfile
    ├── config.yaml
    ├── param.yaml
    ├── __pycache__
    │   └── __init__.cpython-312.pyc
    └── secrets.yaml

## Data Url

    data_url = 'https://drive.google.com/file/d/1RhMp1TyTY4YLVjMhCzAM7SqzMlSnn-Ib/view?usp=sharing'

    file_id = data_url.split('/')[-2]

## DVC cmd

    '''bash
    dvc init

    dvc repro

    dvc dag

    '''

## MLflow

    https://mlflow.org/docs/latest/ml/

## Dagshub

    https://dagshub.com/docs/integration_guide/mlflow_tracking/

    export MLFLOW_TRACKING_URI= https://dagshub.com/Ahmed2797/Kidney-Disease-Classification-Deep-learning-project.mlflow

    export MLFLOW_TRACKING_USERNAME= Ahmed2797

    export MLFLOW_TRACKING_PASSWORD= 466cd6e40b4463c19cee521d93d34f35fb915367
    

## AWS-CICD-Deployment-with-Github-Actions

1. Login to AWS console.
2. Create IAM user for deployment

### with specific access

1. EC2 access : It is virtual machine

2. ECR: Elastic Container registry to save your docker image in aws

### Description: About the deployment

1. Build docker image of the source code

2. Push your docker image to ECR

3. Launch Your EC2

4. Pull Your image from ECR in EC2

5. Lauch your docker image in EC2

### Policy

1. AmazonEC2ContainerRegistryFullAccess

2. AmazonEC2FullAccess
