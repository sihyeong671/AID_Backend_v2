FROM python:3.10.11

WORKDIR /aid_web

COPY ./pyproject.toml ./poetry.lock ./

RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install
