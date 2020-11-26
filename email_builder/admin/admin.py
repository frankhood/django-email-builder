import html
import json
import logging
from functools import update_wrapper
from django import forms

import htmlentities
from django.contrib import admin
from django.utils.html import strip_spaces_between_tags, escape
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.utils.translation import ugettext, ugettext_lazy as _

from email_builder.admin.admin_forms import EmailBuilderForm
from email_builder.models import EmailBuilder, email_code_choices
from email_builder.views import EmailBuilderHtmlPreview, EmailBuilderTxtPreview
from email_builder.utils import get_email_builder_handler

from django import template
from django.template.context import Context

register = template.Library()

logger = logging.getLogger("email_builder")


@admin.register(EmailBuilder)
class EmailBuilderAdmin(admin.ModelAdmin):
    form = EmailBuilderForm
    list_display = ("code", "description_shortened", "subject", "created")
    search_fields = ("code", "description", "subject")
    change_form_template = "admin/email_builder/email_builder_change_form.html"
    save_as = True
    readonly_fields = (
        "content",
        "html_content",
        "mail_preview",
        "available_variables",
    )

    fieldsets = [
        (_("Settings"), {"fields": (("code",),("description",)),},),
        (
            "Email",
            {
                "fields": (
                    ("available_variables",),
                    ("subject",),
                    ("body_content",),
                    ("mail_preview",)
                ),
            },
        ),
    ]

    @mark_safe
    def available_variables(self, obj=None):
        if obj and obj.id:
            available_variables_link = ""
            for key, value in get_email_builder_handler().get_available_variables_by_email_code(email_code=obj.code).items():
                available_variables_link += mark_safe(
                    """ <a class="add-btn folding__hook" href="#" data-token="{slug}">{label}</a> """.format(
                        slug=key, label=value
                    )
                )
            return """<div id='available_variables_container'>{buttons}</div>""".format(
                buttons=available_variables_link
            )
        return "<div id='available_variables_container'></div>"

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            kwargs.update({
                "widget": forms.TextInput(attrs={"class": "vLargeTextField"}),
                "label": _("Mail Subject"),
            })
        if db_field.name == "content":
            kwargs.update({
                "label": _("Mail Body")
            })
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def description_shortened(self, instance):
        return Truncator(instance.description.split("\n")[0]).chars(200)

    description_shortened.short_description = _("Description")
    description_shortened.admin_order_field = "description"

    def preview_html_view(self, request, object_id):
        return EmailBuilderHtmlPreview.as_view()(request, pk=object_id)

    def preview_txt_view(self, request, object_id):
        return EmailBuilderTxtPreview.as_view()(request, pk=object_id)

    def get_urls(self):

        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            path("<path:object_id>/preview/html/", wrap(self.preview_html_view), name="%s_%s_preview_html" % info),
            path("<path:object_id>/preview/txt/", wrap(self.preview_txt_view), name="%s_%s_preview_txt" % info),
        ] + super().get_urls()
        return urlpatterns

    @mark_safe
    def mail_preview(self, obj=None):
        """
        If you want to modify me dinamically:

            $('iframe').attr('srcdoc', yourApiResponse )

        """
        if obj:
            try:
                from django.template import engines
                html_content_preview = get_email_builder_handler().get_rendered_mail(
                    obj.html_content, obj.code
                )

                help_text = '<div class="help" style="margin-left: 0px!important;">%s</div>' % (
                    _("*I dati in questa preview sono fittizzi e del tutto casuali")
                )
                return strip_spaces_between_tags(
                    """{help_text}
                    <div>
                    <iframe id="mail-preview-iframe" class="vLargeTextField" height="480px" srcdoc="{mail_message}">
                    PREVIEW
                    </iframe>
                    </div>""".format(
                        **{"help_text": help_text, "mail_message": html.escape(html_content_preview)}
                    )
                )
            except Exception as ex:
                logger.warning("Somethng went wrong")
                return "Error : {}".format(str(ex))

        return ""

    mail_preview.short_description = _("Preview")
