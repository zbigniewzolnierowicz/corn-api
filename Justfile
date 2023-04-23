set dotenv-load

list:
    just -l
run:
    poetry run uvicorn corn.main:app --port 8000
dev:
    poetry run uvicorn corn.main:app --port 8000 --reload
install:
    poetry install
install-ci:
    poetry install --without=lsp
install-cd:
    poetry install --only-root
test:
    poetry run tox run-parallel
test-ci:
    poetry run tox run-parallel -o
lint:
    poetry run tox run-parallel -e type,lint
lint-ci:
    poetry run tox run-parallel -o -e type,lint
deps:
    docker compose up -d
generate-private-key:
    ssh-keygen -t rsa -b 4096 -m PEM -f private.pem -q -N ""
generate-public-key:
    openssl rsa -in private.pem -pubout -outform PEM -out public.pem
generate-keys: generate-private-key generate-public-key
