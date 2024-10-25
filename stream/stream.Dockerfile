FROM python:3.11

WORKDIR /stream
RUN pip install poetry
COPY ../pyproject.toml poetry.lock /stream/
RUN poetry config virtualenvs.create false && poetry install

COPY ./stream/ /stream/

CMD [ "python", "main.py"]

