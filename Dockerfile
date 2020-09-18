FROM python:3.6
RUN python3.6 -m venv venv-36_dock
FROM python:3.7
RUN python3.7 -m venv venv-37_dock
FROM python:3.8
RUN python3.8 -m venv venv-38_dock
COPY . /django-email-builder/
WORKDIR /django-email-builder/
RUN pip install tox
