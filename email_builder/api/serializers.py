""" serializers
    Created at 10/07/20
"""
import logging

import htmlentities
from django.core.exceptions import ValidationError
from django.template import engines
from django.utils.html import strip_spaces_between_tags
from django.utils.translation import ugettext, ugettext_lazy as _
from rest_framework import serializers

from email_builder import utils
from email_builder.models import EmailBuilder
from email_builder.utils import get_email_code_choices, validate_template_syntax, get_email_builder_handler

# from project.apps.notifications.mail_notifications.controllers import IrideosMailBuilderContextHandler

logger = logging.getLogger(__name__)


class EmailBuilderTxtSerializer(serializers.Serializer):
    email_code = serializers.ChoiceField(choices=get_email_code_choices())
    content = serializers.CharField(validators=[validate_template_syntax])

    class Meta:
        fields = [
            "content",
            "email_code",
            "rendered_content",
        ]

    def validate(self, attrs):
        attrs.update(
            {
                "rendered_content": get_email_builder_handler().get_rendered_txt_mail(
                    EmailBuilder(code=attrs.get("email_code", ""), body_content=attrs.get("content", ""))
                )
            }
        )
        return attrs


class EmailBuilderHtmlSerializer(serializers.Serializer):
    email_code = serializers.ChoiceField(choices=get_email_code_choices())
    content = serializers.CharField(validators=[validate_template_syntax])
    libs_loaded = serializers.JSONField(required=False)
    template = serializers.CharField(required=False)
    subject = serializers.CharField()

    class Meta:
        fields = [
            "content",
            "email_code",
            "libs_loaded",
            "template",
            "subject",
            "rendered_content",
        ]

    def validate(self, attrs):
        libs_loaded = attrs.get("libs_loaded", None) or utils.get_default_libs_loaded()
        template = attrs.get("template", None) or get_email_builder_handler().get_base_html_template()
        rendered_content = get_email_builder_handler().get_mail_template(
            attrs.get("content").replace("\n", "<br>"),
            subject=attrs.get("subject", ""),
            mail_tmpl=get_email_builder_handler().MAIL_HTML_BLOCK,
            template=template,
            libs_loaded=libs_loaded
        )
        attrs.update({
            "rendered_content": get_email_builder_handler().get_rendered_mail(
                rendered_content, attrs.get("email_code")
            )
        })
        return attrs