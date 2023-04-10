set dotenv-load

run:
    poetry run uvicorn corn.main:app --port 8000
dev:
    poetry run uvicorn corn.main:app --port 8000 --reload
test:
    poetry run tox
test-unit:
    poetry run tox -e unit
test-type:
    poetry run tox -e type
test-lint:
    poetry run tox -e lint
deps:
    docker compose up -d
