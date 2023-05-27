FROM python:3.11

WORKDIR /code

COPY . /code

RUN pip install poetry

RUN poetry install

CMD ["poetry", "run", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "info"]
