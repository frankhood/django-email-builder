FROM python:3.8
FROM python:3.6
FROM python:3.7

ENV PYTHONBUFFERED 1

RUN mkdir /django-email-builder/
COPY . /django-email-builder
WORKDIR /django-email-builder



