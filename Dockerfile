FROM python:3.11

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /code

COPY run_app.sh /code/run_app.sh

RUN chmod +x /code/run_app.sh

CMD ["/code/run_app.sh"]
