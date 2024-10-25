FROM python:3.11
WORKDIR /locations

RUN pip install poetry
COPY ../pyproject.toml poetry.lock /locations/
RUN poetry config virtualenvs.create false && poetry install

COPY ./location/ /locations/


CMD [ "uvicorn", "main:app","--host","0.0.0.0", "--port", "8081"]
EXPOSE 8081