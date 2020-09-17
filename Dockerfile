FROM python:3.5
FROM python:3.6
FROM python:3.7
FROM python:3.8

ENV PYTHONBUFFERED 1

RUN mkdir /django-email-builder/
WORKDIR /django-email-builder
COPY . /django-email-builder/
RUN pip install -r requirements_test.txt



