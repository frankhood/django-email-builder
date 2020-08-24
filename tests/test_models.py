#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-email-builder
------------

Tests for `django-email-builder` models module.
"""
from django.contrib.auth.models import AbstractUser, User
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from email_builder import models
from email_builder.handlers import MailBuilderContextHandler
from email_builder.models import EmailBuilder
from email_builder.utils import get_email_builder_handler
from . import email_builder_settings
from .polls.factories import EmailBuilderFactory


class TestEmailBuilder(TestCase):

    def setUp(self):
        self.api_client = APIClient()

    def test_create_mail_template_using_admin(self):
        # =======================================================================
        # ./manage.py test tests.test_models.TestEmailBuilder.test_create_mail_template_using_admin  --settings=tests.test_settings
        # =======================================================================
        user = User.objects.create(username="admin", password="admin", is_staff=True, is_superuser=True)
        self.api_client.force_login(user=user)
        response = self.api_client.get(reverse("admin:email_builder_emailbuilder_add"))
        print(response.get("form"))
