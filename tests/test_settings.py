# -*- coding: utf-8 -*-

from .settings import *

SOUTH_TESTS_MIGRATE = False
DATABASES["default"] = {"ENGINE": "django.db.backends.sqlite3"}
