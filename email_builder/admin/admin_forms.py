from django import forms
from string import Template
import re

from django import forms
from django.core.exceptions import ValidationError
from django.template import Context, Template
from django.utils.translation import gettext_lazy as _

from ..utils import get_email_builder_handler
from ..validators import validate_template_syntax, validate_subject_syntax
from ..models import EmailBuilder
from .. import utils


class EmailBuilderForm(forms.ModelForm):
    class Meta:
        model = EmailBuilder
        fields = [
            "code",
            "description",
            "subject",
            "extends_template",
            "body_content",
            "extends_html_template",
            "body_html_content",
            "libs_loaded",
            "language",
            "html_content",
            "content",
        ]

    def clean(self):
        self.cleaned_data = super().clean()
        self.modified_data = []
        subject = self.cleaned_data.get("subject", "")
        libs_loaded = self.cleaned_data.get("libs_loaded", utils.get_default_libs_loaded())
        self.modified_data.append("libs_loaded")
        body_content = self.cleaned_data.get("body_content", "")
        if "body_html_content" not in self.fields and body_content:
            self.cleaned_data["body_html_content"] = body_content.replace("\n", "<br>")
            body_html_content = self.cleaned_data["body_html_content"]
            self.modified_data.append("body_html_content")
        else:
            body_html_content = self.cleaned_data.get("body_html_content", body_content.replace("\n", "<br>"))
            self.modified_data.append("body_html_content")
        extends_template = self.cleaned_data.get(
            "extends_template",
            get_email_builder_handler().get_base_txt_template()
        )
        extends_html_template = self.cleaned_data.get(
            "extends_html_template",
            get_email_builder_handler().get_base_html_template()
        )
        mail_content = get_email_builder_handler().get_mail_template(
            body_content,
            mail_tmpl=get_email_builder_handler().MAIL_TXT_BLOCKS,
            template=extends_template,
            libs_loaded=libs_loaded
        )
        mail_html_content = get_email_builder_handler().get_mail_template(
            body_html_content,
            subject=subject,
            mail_tmpl=get_email_builder_handler().MAIL_HTML_BLOCK,
            template=extends_html_template,
            libs_loaded=libs_loaded
        )
        try:
            validate_subject_syntax(subject)
        except ValidationError as ex:
            raise ValidationError({"subject": ex.message})
        try:
            validate_template_syntax(mail_content)
        except ValidationError as ex:
            raise ValidationError({"body_content": ex.message})

        try:
            validate_template_syntax(mail_html_content)
        except ValidationError as ex:
            raise ValidationError({"body_html_content": ex.message})

        self.cleaned_data["content"] = mail_content
        self.modified_data.append("content")
        self.cleaned_data["html_content"] = mail_html_content
        self.modified_data.append("html_content")

        return self.cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=commit)
        for field in self.modified_data:
            setattr(instance, field, self.cleaned_data.get(field, ""))
        if instance.id:
            instance.save(update_fields=self.modified_data)
        else:
            instance.save()
        return instance





