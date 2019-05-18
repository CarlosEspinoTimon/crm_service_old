db_init:
	sudo docker exec -t crm_service_crm_backend_1 pipenv run flask db init

db_migrate:
	sudo docker exec -t crm_service_crm_backend_1 pipenv run flask db migrate

db_upgrade:
	sudo docker exec -t crm_service_crm_backend_1 pipenv run flask db upgrade

db_downgrade:
	sudo docker exec -t crm_service_crm_backend_1 pipenv run flask db downgrade

run_tests:
	sudo docker exec -t crm_service_crm_backend_1 pipenv run python tests.py

access_container:
	sudo docker exec -t crm_service_crm_backend_1 bash

# Usage install_module module='MODULE WITH WHITESPACES'
install_module:
	sudo docker exec -t crm_service_crm_backend_1 pipenv install ${module}


