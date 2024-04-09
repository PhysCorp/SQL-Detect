<h1 align="center">
  <strong>Flask-based SQL Injection Detection API</strong>
</h1>

<div align="center">
  
  <a href="https://github.com/PhysCorp/SQL-Detect">![link to GitHub showing Stars number](https://img.shields.io/github/stars/PhysCorp/SQL-Detect?style=social)</a>
  <a href="https://github.com/PhysCorp/SQL-Detect">![link to GitHub showing Forks number](https://img.shields.io/github/forks/PhysCorp/SQL-Detect?style=social)</a>
  <a href="https://github.com/PhysCorp/SQL-Detect/LICENSE">![link to license](https://img.shields.io/github/license/PhysCorp/SQL-Detect)</a>
 
</div>

## Notes
Tested on Fedora Silverblue

## Description
This webserver is designed to detect SQL injection attempts in provided queries. It uses a trained Random Forest model to classify queries as malicious or not. The server is built with Quart, a Python ASGI web microframework, and Hypercorn, an ASGI server.

## Endpoints
### POST /detect
This endpoint accepts a JSON object with a `query` field. It returns a JSON object with a `is_malicious` field indicating whether the provided query is considered malicious.

**Request:**
```json
{
    "query": "SELECT * FROM users"
}
```

**Response:**
```json
{
    "is_malicious": false
}
```

### POST /upload_csv
This endpoint accepts a CSV file for retraining the model. The CSV file should be included in the `file` field of the form data. A `password` field should also be included in the form data for authentication. The server will return a message indicating whether the file was saved successfully and the model training has started.

**Form Data:**
- `file`: The CSV file
- `password`: The password for authentication

**Response:**
```json
{
    "message": "File saved and model training started"
}
```

### GET /healthcheck
This endpoint returns the status of the server and the training process. It returns a JSON object with a `status` field indicating the status of the server and a `training` field indicating the status of the training process.

**Response:**
```json
{
    "message": "System is operational. Please POST to /detect with 'query' to use the service.",
    "status": "ok",
    "training": "idle"
}
```

## Environment Variables
- `MODEL_URL`: Specify a URL to a model file to load. If not specified, the server will train a new model.
- `VECTORIZER_URL`: Specify a URL to a vectorizer file to load. If not specified, the server will create vectorizer when training a new model.
- `ALLOW_TRAINING`: Specify whether to allow training via the `/upload_csv` endpoint. If not specified, the default is `False`.
- `SECRET_TRAIN_PASSKEY`: Specify a password for the training endpoint. If not specified, the default password is `1234`.

## Requirements
- [X] Docker
- [X] Docker-compose
- [ ] Python 3.8
- [ ] python3-pip
- [ ] conda
- [ ] python3-virtualenv

## Docker Method (Recommended)

#### Please note, the Docker-compose file is required, and this project *cannot* be ran via `docker run` due to the need for volume mount and port mapping.

### Deploy from Docker Hub
> [!Note]
> Make sure you have [Docker](https://docs.docker.com/engine/install/) installed
1. Save the [`docker-compose.yaml`](https://raw.githubusercontent.com/PhysCorp/SQL-Detect/main/docker-compose.yaml) file from this project to your local machine.
2. Create/edit `.env` file based on the contents in the `.env.example` file.:
3. Create the container with `sudo docker-compose up`, or add `-d` to run in background.

### Building from Source
> [!Note]
> Make sure you have [Docker](https://docs.docker.com/engine/install/) installed
1. Clone the repository with `git clone https://github.com/PhysCorp/SQL-Detect.git` and navigate to the project directory with `cd SQL-Detect`.
2. Create/edit `.env` file based on the contents in the `.env.example` file.:
3. Build the Docker image with `sudo docker-compose build`.
4. Run the Docker image in foreground with `sudo docker-compose up`, or add `-d` to run in background.

## Manual Method
### Installation
1. Install python3, python3-pip and anaconda. Anaconda can be retrieved from [here](https://www.anaconda.com/products/individual). If you are on Windows, you can install anaconda with [chocolatey](https://chocolatey.org/) using `choco install anaconda3`.
2. Create a conda environment with `conda create --name SQL-Detect python=3.8`.
3. Activate the conda environment with `conda activate SQL-Detect`.
4. Install the requirements with `python3 -m pip install -r requirements.txt`.
5. (Optional): Reinstall charset-normalizer if experiencing issues with COMMON_SAFE_ASCII_CHARACTERS `python3 -m pip install --force-reinstall charset-normalizer`

### Usage
0. Download this project with `git clone https://github.com/PhysCorp/SQL-Detect.git` and navigate to the project directory with `cd SQL-Detect`.
1. Activate the conda environment with `conda activate SQL-Detect`.
2. Create/edit `.env` file based on the contents in the `.env.example` file.
3. Run `python3 main.py` to start the application.

### Alternate Instructions using virtualenv (Linux & MacOS, Windows mileage may vary)
Create a new virtualenv with `python3 -m venv .venv`.
Activate the virtualenv with `source .venv/bin/activate`.
Install the requirements with `python3 -m pip install -r requirements.txt`.

### Uninstall Conda Environment
1. Deactivate the conda environment with `conda deactivate`.
2. Remove the conda environment with `conda remove --name SQL-Detect --all`.

## License
Copyright 2024 | This project is licensed under the [MIT License](LICENSE). The full license can be found in the GitHub repository.