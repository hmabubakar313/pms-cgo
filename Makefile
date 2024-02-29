IMAGE_NAME ?= pms

.PHONY: run
run: stop 
	docker build --tag ${IMAGE_NAME} .
	docker run -d -p 8000:8000 ${IMAGE_NAME}

.PHONY: stop
stop:
    docker ps --filter "ancestor=${IMAGE_NAME}" --filter "expose=${PORT}/tcp" -q | xargs docker stop || true


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

.PHONY: makemigrations
makemigrations: ## Build developer containers.
	docker compose run --rm web python manage.py makemigrations


.PHONY: migrate
migrate: ## Build developer containers.
	docker compose run --rm web python manage.py migrate