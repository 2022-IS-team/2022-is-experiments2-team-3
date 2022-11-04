.PHONY: up
up:
	docker-compose build
	docker-compose up

.PHONY: build
build:
	docker-compose build --no-cache

.PHONY: exec
exec:
	docker-compose exec dev bash

.PHONY: down
down:
	docker-compose down
