TARGET=update_sus

.PHONY: start
start:
	-@make up
	@echo "ファイルの監視を開始しました。ファイルを保存するとテストが実行され結果が表示されます。"
	@make start-test || :
	@echo "!!!後処理中 しばらくお待ちください!!!"
	-@make down

.PHONY: up
up:
	@docker-compose build
	@docker-compose up -d

.PHONY: build
build:
	docker-compose build --no-cache

.PHONY: exec-dev
exec:
	docker-compose exec dev bash

.PHONY: exec-test
exec-test:
	docker-compose exec test bash

.PHONY: start-test
start-test:
	@docker-compose exec test incrond -n

.PHONY: down
down:
	@docker-compose down

.PHONY: test
test:
	@if [ ! -f ./.logging ]; then\
		touch .logging &&\
		pytest -q tests/environment/controller/test_$(TARGET).py || : &&\
		rm .logging;\
	fi
