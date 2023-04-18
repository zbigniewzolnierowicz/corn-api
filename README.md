# Corn API 

[![CI](https://github.com/zbigniewzolnierowicz/corn-api/actions/workflows/ci.yml/badge.svg)](https://github.com/zbigniewzolnierowicz/corn-api/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/zbigniewzolnierowicz/corn-api/branch/main/graph/badge.svg?token=DB5T34KQ5R)](https://codecov.io/gh/zbigniewzolnierowicz/corn-api)

## Setup 

1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Install dependencies:

``` sh
just install
```
3. Start services:

``` sh
docker compose up -d
```

4. Start dev server:

``` sh
just dev
```

5. If you want to run tests, just run:

``` sh
just test
```

6. For linting, run:

``` sh
just lint
```

