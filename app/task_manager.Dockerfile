FROM python:3.11
WORKDIR /task_manager
RUN pip install poetry
COPY ../pyproject.toml poetry.lock /task_manager/
RUN poetry config virtualenvs.create false && poetry install

COPY ./app/ /task_manager/

CMD [ "uvicorn", "main:app","--host","0.0.0.0", "--port", "8080"]
EXPOSE 8080
