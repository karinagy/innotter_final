FROM python:3.8

ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1

RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

RUN mkdir /app
COPY . .

RUN pipenv install --system --deploy --ignore-pipfile

WORKDIR /app