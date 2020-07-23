import logging

from django.core.exceptions import ValidationError
from django.utils.html import strip_spaces_between_tags
from string import Template
from django.utils.translation import ugettext, ugettext_lazy as _
from post_office.validators import validate_template_syntax

from . import utils

logger = logging.getLogger("email_builder")

email_code_choices = [(x, _(y)) for x, y in utils.get_email_code_choices()]
language_choices = [(x, _(y)) for x, y in utils.get_email_languages()]
base_raw_template_choices = [(x, _(y)) for x, y in utils.get_base_templates()]
base_html_template_choices = [(x, _(y)) for x, y in utils.get_base_html_templates()]


class MailBuilderContextHandler(object):
    MAIL_TXT_BLOCKS = """{% extends '$extends_tmpl' %}{% load $loaded_libs %}{% block content %}$body{% endblock %}"""
    MAIL_HTML_BLOCK = """{% extends '$extends_tmpl' %}{% load $loaded_libs %}
    {% block title %}$subject{% endblock title %}{% block content %}$body{% endblock %}"""


    @classmethod
    def get_base_txt_template(cls):
        return base_raw_template_choices[0][0]

    @classmethod
    def get_base_html_template(cls):
        return base_html_template_choices[0][0]

    @classmethod
    def get_available_variables(cls):
        """
        This method should return your mail configuration in this form:

        if you don't pass email_code you have to return the content formatte in this way

        <email_code>: {
            "available_variables": {
                <varname>: {
                    "label": (str),
                    "fake_value": (str nullable),
                },
                ...
            }
        }
        """
        # raise NotImplementedError(
        #     "Please create your handler inheriting from MailBuilderContextHandler"
        # )
        return {}

    @classmethod
    def get_context_by_email_code(cls, email_code):
        """
        This method should return your mail configuration in this form:
        {
            <varname>: (str nullable),
            ...
        }

        """
        available_variables = cls.get_available_variables().get(email_code, {}).get("available_variables", {})
        if not available_variables:
            logger.warning(f"No variables found for email_code '{email_code}'")
        return {k: v.get("fake_value", "") for k, v in available_variables.items()}

    @classmethod
    def get_available_variables_by_email_code(cls, email_code):
        """
        This method should return your mail configuration in this form:
        {
            <varname>: (str nullable),
            ...
        }

        """
        available_variables = cls.get_available_variables().get(email_code, {}).get("available_variables", {})
        if not available_variables:
            logger.warning(f"No variables found for email_code '{email_code}'")
        return {k: v.get("label", "") for k, v in available_variables.items()}

    @classmethod
    def get_mail_template(cls, content, subject=None, mail_tmpl=None, template=None, libs_loaded=None):
        return Template(mail_tmpl).substitute(
            extends_tmpl=template,
            loaded_libs=" ".join(libs_loaded),
            subject=subject,
            body=content
        )


    @classmethod
    def get_rendered_mail(cls, email_content, email_code):
        from django.template import engines
        # @TODO Change me and take the first that returns something in a for cycle (see DjangoTemplateResponseMixin)
        return strip_spaces_between_tags(
            engines.all()[0].from_string(
                email_content
            ).render(
                context=cls.get_context_by_email_code(
                    email_code
                )
            )
        )

# class BaseMail:
#     code = None
#     label = _("My Label")
#
#     def __init__(self):
#         if not
#
#     def get_available_variables(self):
#         return []
#
#
# class BaseVariable:
#     code = None
#     label = None
#
#     def get_fake_value(self):
#         return None
#
#
# class MailToEngineering(BaseMail):
#     name
#     label
#
#     def get_available_variables(self):
