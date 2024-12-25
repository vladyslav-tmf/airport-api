.PHONY: install
install: ## Install dependencies
	poetry install

.PHONY: migrate
migrate:  ## Create and apply migrations
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

.PHONY: run
run: ## Run development server
	poetry run python manage.py runserver

.PHONY: superuser
superuser: ## Create superuser
	poetry run python manage.py createsuperuser

.PHONY: test
test: ## Run tests
	poetry run python manage.py test

.PHONY: setup
setup: install migrate superuser ## Complete project setup
