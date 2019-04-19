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
DATABASE_URI=[production_database]
PYTHONUNBUFFERED=1
```
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
<!-- TODO -->