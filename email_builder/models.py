""" models
    Created at 09/07/20
"""
import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from string import Template
from django.utils.translation import gettext, gettext_lazy as _
from django_extensions.db.fields.json import JSONField
# from parler.models import TranslatableModel

from . import utils
from .utils import get_email_builder_handler
from .validators import validate_template_syntax

logger = logging.getLogger(__name__)

email_code_choices = [(x, _(y)) for x, y in utils.get_email_code_choices()]
language_choices = [(x, _(y)) for x, y in utils.get_email_languages()]
base_raw_template_choices = [(x, _(y)) for x, y in utils.get_base_templates()]
base_html_template_choices = [(x, _(y)) for x, y in utils.get_base_html_templates()]


"""
# TODO Next Step
class EmailTemplateBlock(models.Model):
    email_template = models.ForeignKey(EmailBuilder, related_name="blocks", on_delete=models.CASCADE)
    block_name = models.CharField(_("Block name"), help_text=_("The name of the block used in overrided template e.g. if {% block \"content\" %} -> \"content\" "))
    body_content = models.TextField(blank=True,
        verbose_name=_("Content"), validators=[validate_template_syntax])
    body_html_content = models.TextField(blank=True,
        verbose_name=_("Html Content"), validators=[validate_template_syntax])
"""


class EmailBuilder(models.Model):

    code = models.CharField(
        _("Name"),
        choices=email_code_choices,
        max_length=255,
        help_text=_(
            "Select your logic between the available ones. For each key, a different context will be available in the emails created through this template"
        ),
    )
    description = models.TextField(_("Description"), blank=True, help_text=_("Description of this template."))
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=255, verbose_name=_("Subject"), validators=[utils.validate_template_syntax])
    content = models.TextField(
        verbose_name=_("Content"), validators=[utils.validate_template_syntax], blank=True, default=""
    )
    html_content = models.TextField(
        verbose_name=_("HTML content"), validators=[utils.validate_template_syntax], blank=True, default=""
    )
    extends_template = models.CharField(max_length=255, choices=base_raw_template_choices, blank=True, default="")
    extends_html_template = models.CharField(max_length=255, choices=base_html_template_choices, blank=True, default="")
    body_content = models.TextField(verbose_name=_("Content"), blank=True, default="")
    body_html_content = models.TextField(verbose_name=_("Html Content"), blank=True, default="")
    libs_loaded = JSONField(verbose_name=_("Loaded Libs"), blank=True, default="[]")

    language = models.CharField(
        max_length=12,
        verbose_name=_("Language"),
        help_text=_("Render template in alternative language"),
        choices=language_choices,
        default=settings.LANGUAGE_CODE,
    )

    class Meta:
        unique_together = ("code", "language")
        verbose_name = _("Email Template")
        verbose_name_plural = _("Email Templates")

    def __str__(self):
        return u"%s [%s]" % (self.name, self.language)

    @property
    def name(self):
        return self.get_code_display()

    @classmethod
    def get_available_variables(cls):
        return utils.get_email_code_context()

    def get_available_context(self):
        return self.__class__.get_available_variables()[self.name]
