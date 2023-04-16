set dotenv-load

list:
    just -l
run:
    poetry run uvicorn corn.main:app --port 8000
dev:
    poetry run uvicorn corn.main:app --port 8000 --reload
test:
    poetry run tox run-parallel
test-ci:
    poetry run tox run-parallel -o
deps:
    docker compose up -d
