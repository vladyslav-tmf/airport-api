.PHONY: install
install: ## Install dependencies
	poetry install

.PHONY: migrate
migrate:  ## Create and apply migrations
	python manage.py makemigrations
	python manage.py migrate

.PHONY: run
run: ## Run development server
	python manage.py runserver

.PHONY: superuser
superuser: ## Create superuser
	python manage.py createsuperuser

.PHONY: test
test: ## Run tests
	python manage.py test

.PHONY: load
load: ## Load initial data
	python manage.py loaddata airport_api_sample_data.json

.PHONY: setup
setup: install migrate run ## Complete project setup
