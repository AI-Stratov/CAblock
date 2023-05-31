#!/bin/bash

if [ "$ALEMBIC_TEST_CONFIG" = "Test" ]; then
  poetry run pytest
else
  poetry run alembic upgrade head

  poetry run uvicorn app.app:app --host 0.0.0.0 --port 80 --log-level info
fi
