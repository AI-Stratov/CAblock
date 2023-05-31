# CAblock
## Installation
### Setup project
```pip install poetry```

```poetry install```

### Prepare database
Create main PostgreSQL database and test database
* for example with psql:

```CREATE DATABASE cablock;```

```CREATE DATABASE cablock_test;```

### Setup environment variables
Look at .env.example and create .env file with your own values

### Run migrations
```poetry run alembic upgrade head```

### Run project
```poetry run python main.py```

## Testing
Change .env var ALEMBIC_TEST_CONFIG to "Test"

```poetry run pytest```

## Docker
Change .env vars DB_HOST and DB_HOST_TEST to container names

```docker-compose up --build```

You can reach the API at http://localhost:8080

