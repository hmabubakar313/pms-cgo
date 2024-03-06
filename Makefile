.PHONY: build
build: ## Build developer containers.
	docker compose build


.PHONY: up
up: ## Build developer containers.
	docker compose up


.PHONY: down
down: ## Build developer containers.
	docker compose down


.PHONY: silenceup
silenceup: ## Build developer containers.
	docker compose up -d

.PHONY: tests
tests: ## Build developer containers.
	docker compose run --rm web python manage.py test

.PHONY: send_emal
send_email: ## Build developer containers.
	docker compose run --rm web python manage.py send_email

.PHONY: makemigrations
makemigrations: ## Build developer containers.
	docker compose run --rm web python manage.py makemigrations


.PHONY: migrate
migrate: ## Build developer containers.
	docker compose run --rm web python manage.py migrate

.PHONY: createsuperuser
createsuperuser: ## Build developer containers.
	docker compose run --rm web python manage.py createsuperuser

