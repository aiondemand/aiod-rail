# AIoD - RAIL Backend

_RAIL Backend_ serves as a backend application for [RAIL service](../README.md).
This backend consists of a REST API service (FastAPI) and a non-relational database (MongoDB).

## Setup

This repository contains two systems; the database and the REST API.
As a database we use a containerized MongoDB server (through Docker), the REST API can be run locally or containerized.

### Using docker compose [RECOMMENDED]

1. Create `.env` file containing relevant ENV variables required for the service defined in `.env.sample`.
    - `MONGODB_DBNAME`: Name of the database - do not change it unless you need to
    - `AIOD_API__BASE_URL`: URL of the running AIoD API
    - `MAX_PARALLEL_IMAGE_BUILDS`: Define a maximum number of Python (asyncio) tasks that build and push docker images
      in parallel
    - `MAX_PARALLEL_CONTAINERS`: Define a maximum number of Python (asyncio) tasks that run REANA workflows in parallel
    - `MAX_IMAGE_BUILDS_ATTEMPTS`: Define a maximum number of ATTEMPTS that are executed for each failing process of
      building a docker image
    - `MAX_EXPERIMENT_RUN_ATTEMPTS`: Define a maximum number of ATTEMPTS that are executed for each failing experiment
      run
    - `REANA_SERVER_URL`: Define the URL used for connecting to REANA server
    - `REANA_ACCESS_TOKEN`: Define the access token used for connecting to REANA server
    - `DOCKER_REGISTRY_URL`: Define a path to a repository that we want to use for storing docker images of individual
      ExperimentTemplates
    - `DOCKER_REGISTRY_USERNAME`: Define a username for a Docker Hub profile that has push permissions to a repository
      defined in variable `DOCKER_REGISTRY_URL`
    - `DOCKER_REGISTRY_PASSWORD`: Define a password for a Docker Hub profile that has push permissions to a repository
      defined in variable `DOCKER_REGISTRY_URL`
    - `AIOD_KEYCLOAK__*`: Variables related to authentication using Keycloak
1. Start the service using the following command: `docker compose up -d --build`

**IMPORTANT**: Make sure you check and potentially modify the host port mappings for specific components
in [docker-compose.yml](docker-compose.yml) file.

### Local installation

1. Create two arbitrarily located folders that will be used to store:
    1. MongoDB database, e.g. `./db`
    1. files corresponding to individual experiments (*throughout this documentation we tend to call this
       folder `eee-data`, however you can name this directory however you would like*)
1. Create MongoDB container using following
   command: `docker run --name eee-mongo -p 27017:27017 -d -v <PATH_TO_DB_FOLDER>:/data/db mongo`
1. [IF YOU'RE ON WINDOWS] Open specific port for Docker to listen to, so that you can communicate with it. Specifically
   use Docker Desktop application and:
    - Go to "settings"
    - Go to "general"
    - Check "Expose daemon on tcp://localhost:2375 without TLS" if its unchecked
1. Create `.env` file containing relevant ENV variables required for the service defined in `.env.sample`. The required
   variables are described in greater detail in the previous section.
1. Install Python >= 3.10 if you haven't done so already. We recommend using Python version 3.10 as this particular
   version has been tested and used for the development of this project.
1. Install dependencies by executing following command: `pip install -r requirements.txt`.
1. Create additional ENV variables (these variables can be also added to the created `.env` file):
    - `MONGODB_URI`: URL of mongodb, if you created mongodb instance using command in the previous step then use
      value `mongodb://localhost:27017` for this variable
    - `DOCKER_BASE_URL`: Use value `tcp://localhost:2375` if you're on Windows and not using WSL; otherwise
      use `unix:///var/run/docker.sock`
    - `EEE_DATA_PATH`: Not necessarily an absolute path of the so called `eee-data` folder you have created beforehand
      in the step 1.2.
1. Start the FastAPI server using the following command: `uvicorn app.main:app --reload`

### Fill some toy data into the database

Execute Python script found on the path: `dev-scripts/experiments/create_experiment_template.py` that creates one
ExperimentTemplate that will be stored in MongoDB database.

**IMPORTANT**:

- Run the script from the directory `dev-scripts/experiments`
- Don't forget to change the port in said script to the one your FastAPI server is listening on

## Folder Structure

By default, the application stores data in a named volume `eee-data` mounted folder on `/data/eee` path.

Example of a resulting folder structure after creation of one ExperimentTemplate and a successful execution of
ExperimentRun:

```bash
/data/eee/
├── experiment-templates
│   └── template-64940e38a8784c37c5f9a529
│       ├── Dockerfile
│       ├── reana.yaml
│       ├── requirements.txt
│       └── script.py
└── experiments-userdata
    └── run-64d22795090f4a38dbbf9764
        ├── .env
        ├── log.txt
        ├── reana.yaml
        ├── script.py
        └── output
            └── metrics.json
```

## Contributing

### 1. Install dependencies
```shell
pip install -r requirements-dev.txt
```
### 2. Setup pre-commit hooks
```shell
pre-commit install
```
You can also trigger the execution of pre-commit hooks on all files manually by running the following command:
   ```shell
   pre-commit run --all-files
   ```
### 3. Run unit tests
This project uses [pytest](https://docs.pytest.org/) framework for testing.

You need to run the unit tests from root directory `backend` where also the config file `pytest.ini` is located.
The execution of all tests can be then simply done by running the command:
```shell
pytest
```

#### Code coverage
The configuration makes sure that code coverage is computed by `pytest-cov` as well.
You can browse the generated coverage report in HTML format found in directory `htmlcov`.
   