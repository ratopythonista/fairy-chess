install:
	pip install -e .

build:
	docker-compose build

startup:
	docker-compose up