import logging
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template import Template as DjangoTemplate, TemplateSyntaxError, TemplateDoesNotExist
from django.utils.module_loading import import_string

from email_builder.loading import _import_module, _pick_up_class
from . import settings as app_settings

logger = logging.getLogger("email_builder")


def validate_template_syntax(source):
    """
    Basic Django Template syntax validation. This allows for robuster template
    authoring.
    """
    try:
        DjangoTemplate(source)
    except (TemplateSyntaxError, TemplateDoesNotExist) as err:
        raise ValidationError(str(err))


def get_email_code_choices():
    return getattr(settings, "EMAIL_BUILDER_CODE_CHOICES", [("base-mail", "Base Mail"),])


def get_email_code_context():
    return getattr(settings, "EMAIL_BUILDER_CODE_CONTEXT", {"base-mail": {},})


def get_email_languages():
    return getattr(settings, "EMAIL_BUILDER_LANGUAGES", settings.LANGUAGES)


def get_default_libs_loaded():
    return getattr(settings, "EMAIL_BUILDER_DEFAULT_LIBS_LOADED", ["i18n", "static"])


def get_base_templates():
    return getattr(
        settings,
        "EMAIL_BUILDER_BASE_EMAIL_TEMPLATES",
        [(app_settings.BASE_MAIL_TXT_PATH, "Default Body"),],  # "mails/base_mail.txt"
    )


def get_base_html_templates():
    return getattr(
        settings,
        "EMAIL_BUILDER_BASE_EMAIL_HTML_TEMPLATES",
        [(app_settings.BASE_MAIL_HTML_PATH, "Default Body"),],  # "mails/base_mail.html"
    )


def get_email_builder_handler():
    handler_path = getattr(
        settings, "EMAIL_BUILDER_CONTEXT_HANDLER_PATH", "email_builder.handlers.MailBuilderContextHandler"
    )
    try:
        class_name = handler_path.split(".")[-1]
        module_path = handler_path.rsplit(".", 1)[0]
        _module = _import_module(module_path, class_name)
        return _pick_up_class(_module, class_name)
    except Exception as ex:
        logger.exception(f"Problem taking Handler from {handler_path}")
        raise ex
