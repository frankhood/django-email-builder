FROM python:3.5
FROM python:3.6
FROM python:3.7
FROM python:3.8

COPY . /python35/
COPY . /python36/
COPY . /python37/
COPY . /python38/
RUN pip install virtualenv
RUN virtualenv python35
CMD source python35/bin/activate
RUN virtualenv python36
CMD source python36/bin/activate
RUN virtualenv python37
CMD source python37/bin/activate
RUN virtualenv python38
CMD source python38/bin/activate
COPY . /django-email-builder/
CMD pip install tox
CMD python setup.py sdist
CMD tox
