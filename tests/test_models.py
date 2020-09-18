#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-email-builder
------------

Tests for `django-email-builder` models module.
"""
import datetime
import importlib
import sys
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import formats
from rest_framework import status
from rest_framework.test import APIClient

from email_builder.models import EmailBuilder
from . import email_builder_settings
from .polls import factories
from .polls.controllers import ExampleMailBuilderContextHandler
from .polls.factories import EmailBuilderFactory


class TestEmailBuilder(TestCase):
    def setUp(self):
        self.api_client = APIClient()

    def test_python_version(self):
        # =======================================================================
        # python manage.py test tests.test_models.TestEmailBuilder.test_python_version  --settings=tests.test_settings
        # =======================================================================
        print("PYTHON VERSION => ", sys.version)

    def test_wysiwyg_api(self):
        # =======================================================================
        # python manage.py test tests.test_models.TestEmailBuilder.test_wysiwyg_api  --settings=tests.test_settings
        # =======================================================================
        user = User.objects.create(username="admin", password="admin", is_staff=True, is_superuser=True)
        self.api_client.force_login(user=user)
        stub_data_factory = EmailBuilderFactory.stub()
        data = {
            "email_code": email_builder_settings.EMAIL_BUILDER_CODE_QUESTION,
            "subject": stub_data_factory.subject,
            "content": "Testing Email Builder template with this tag {{ question_pub_date }}",
        }
        response = self.api_client.post(reverse("html-email-preview"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email_code"), email_builder_settings.EMAIL_BUILDER_CODE_QUESTION)
        self.assertEqual(response.data.get("content"), data.get("content"))
        self.assertEqual(response.data.get("subject"), data.get("subject"))
        self.assertEqual(
            response.data.get("rendered_content"),
            f"""<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>{data.get("subject")}</title></head><body style="text-align:left; font-family:Arial, Helvetica, Verdana, sans-serif; background-color: #FFFFFF;" bgcolor="#FFFFFF"; ><table border="0" cellpadding="0" cellspacing="0" width="100%" style="width: 100%; border: 0; margin: 0; background:#FFFFFF none;" bgcolor="#FFFFFF"><tr><td align="center"><table border="0" bgcolor="#FFFFFF" cellpadding="0" cellspacing="0" style="margin: 0; background-color: #FFFFFF; max-width: 700px; ">\n\t\t\t\t\t\t\t\t    {str(data.get('content').replace('{{ question_pub_date }}',formats.date_format(datetime.datetime(2018, 12, 12, 0, 0, 0), settings.DATETIME_FORMAT)))}\n                    \n                </table></td></tr></table></body></html>\n\n""",
        )
