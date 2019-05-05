# CRM_service
This is an example of a backend CRM Service that is composed of:
- Server: developed in Python with the Flask framework
- Database: a MySQL 5.7 database
## Getting Started
To start developing in this project, you just have to clone the repository, meet the prerequisites and run the command shown in the Run the server section.
### Prerequisites
You need to have installed:
- docker-compose 
- docker

You need to create a .env file in the `backend` directory with some variables:
```
FLASK_APP=server:create_app('config.Dev')
FLASK_ENV=development
DATABASE_URI=YOUR_PRODUCTION_DATABASE 
PYTHONUNBUFFERED=1
GOOGLE_LOGIN_CLIENT_ID=YOUR_CLIENT_ID
GOOGLE_LOGIN_CLIENT_SECRET=YOUR_CLIENT_SECRET
GOOGLE_APPLICATION_CREDENTIALS=.credentials/crm-service-storage-key.json
GOOGLE_PROJECT=PROJECT_NAME
GOOGLE_BUCKET=BUCKET_NAME
```

This file is in the gitignore, so no credentials are going to be uploaded to the repository.

The `DATABASE_URI` is just for production, the config.Dev file configures by default the URI to the local database of the docker-compose, so you can leave it like it is in the example.

You have to create a `.credentials/` folder in the `backend` directory where you have to put the Google Cloud Storage bucket key and it has to be named `crm-service-storage-key.json`.


### Run the server
The server runs by default in development mode. To start it, you have to run:

`[sudo] docker-compose up`

The first time you run the server you have to create the tables and a user in the database. After you run the previous command, you can create them with the `init_database.sh` script. This script must be run with an email as argument, that is going to be the email of the admin user. At the moment, the email `must be` a gmail account for the oauth authentication.

Run the command:

`sh init_database.sh youremail@gmail.com`

## Working in the project
As this project is build in a dockerized environment, the developers have to adapt to work with it.
#### Install new modules
The modules have to be installed in the server that is inside the container, so if a developer needs to install a new module, it must be installed with the following command:

`[sudo] docker exec -t $([sudo] docker ps | grep "crm_backend" | awk '{ print $1 }') pipenv install MODULE-NAME [--dev]`

This will install the module in the container and it will be added to the Pipfile which is shared with the host and tracked in the repository.

### Running the tests
The test are run in a test database, so the first time, you have to create the tables an a user for the tests. There is a script that does this, so you can just run:

`sh init_test_database.sh`

Then you can run the tests in the container:

`[sudo] docker exec -t $([sudo] docker ps | grep "crm_backend" | awk '{ print $1 }') pipenv run python tests.py`

## Deployment
### Automated deployment
This repository is integrated within a CI/CD jenkins pipeline. This pipeline builds the environment for the tests and runs them, also, when changes are made in the master branch it deploys the code to App Engine Flexible.
### Manual deployment
This server is prepared to be deployed in Google App Engine Flexible, if you wish to deploy it manually, you need to configure the `app.yaml` file and generate the latest `requirements.txt`.
#### Configure app.yaml
In the repository there is an `app.yaml` example, in this file you have to change the environment variables for the real ones. For security, to avoid uploading credentials to the repository, you should create a copy of the file and call it `real_app.yaml` which is already in the .gitignore, put the real environment variables there and deploy it with this file.
#### Generate requirements.txt
To generate the latest `requirements.txt`, you have to get into the container:

`[sudo] docker exec -it $([sudo] docker ps | grep "crm_backend" | awk '{ print $1 }') bash`

and generate the file:

`pipenv lock -r >  requirements.txt`

it is also needed the gunicorn module:

`echo "gunicorn==19.9.0" >> requirements.txt`

we have to remove the first line created by the pipenv lock -r

`echo "$(tail -n +2 requirements.txt)" > requirements.txt`

This file will be created inside the container and in the folder shared with the host.
#### Deploy it
Once you have it, you can deploy the app by running: `gcloud app deploy real_app.yaml` in the `backend` directory. Beware that you have to have [initiated the cloud SDK](https://cloud.google.com/sdk/docs/initializing "Initializing Cloud SDK")
