# CRM_service
This is an example of a CRM Service that is composed of:
- Backend: developed in Python with the Flask framework
- Database: a MySQL 5.7 database
## Getting Started
To start developing in this project, you just have to clone the repository, meet the prerequisites and run the command shown in the Installing section.
### Prerequisites
You need to install:
- docker-compose 
- docker

Also, you need to create a .env file in the `backend` directory with some variables:
```
FLASK_APP=server:create_app('config.Dev')
FLASK_ENV=development
DATABASE_URI=YOUR_PRODUCTION_DATABASE
PYTHONUNBUFFERED=1
GOOGLE_LOGIN_CLIENT_ID=YOUR_CLIENT_ID
GOOGLE_LOGIN_CLIENT_SECRET=YOUR_CLIENT_SECRET
```
The DATABASE_URI is just for production, the config.Dev file configures by default the URI to the local database of the docker-compose
### Run the server
The server runs by default in development mode. To start it, you have to run:

`[sudo] docker-compose up`

#### Install modules
You can either install the module in the host and then rebuild the docker by running:

`[sudo] docker-compose build` 

or install it directly in the container. To do that you have to get into the container: 

`[sudo] docker exec -it $([sudo] docker ps | grep "crm_backend" | awk '{ print $1 }') bash`

and install the module:

`pipenv install MODULE-NAME [--dev]`

## Running the tests
<!-- TODO -->
## Deployment
This server is prepared to be deployed in Google App Engine Flexible, to do so, you need to configure the `app.yaml` file and the latest `requirements.txt`.
### app.yaml
In the repository there are an `app.yaml` example, in this file you have to change the environment variables for the real ones. For security, to avoid uploading credentials to the repository, you should create a copy of the file and call it `real_app.yaml` which is already in the .gitignore, put the real environment variables there and deploy it from there `gcloud app deploy real_app.yaml`.
### requirements.txt
To generate the latest `requirements.txt`, you have to get into the container:

`[sudo] docker exec -it $([sudo] docker ps | grep "crm_backend" | awk '{ print $1 }') bash`

and generate the file:

`pipenv lock -r > requirements.txt`

it is also needed the gunicorn module:

`echo "gunicorn==19.3.0" >> requirements.txt`

This file will be created inside the container and in the folder shared with the host.
### Deploy it
Once you have it, you can deploy the app by running: `gcloud app deploy [real_app.yaml]` in the `backend` directory. Beware that you have to have [initiated the cloud SDK](https://cloud.google.com/sdk/docs/initializing "Initializing Cloud SDK")
