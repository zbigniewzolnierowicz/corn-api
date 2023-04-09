run:
    poetry run uvicorn corn.main:app --port 8000
dev:
    poetry run uvicorn corn.main:app --port 8000 --reload
test:
    poetry run pytest --cov
