""" views
    Created at 14/07/20
"""
import logging

from django.template import TemplateDoesNotExist
from django.template.loader import _engine_list
from django.template.response import SimpleTemplateResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import BaseDetailView

from email_builder.models import EmailBuilder

logger = logging.getLogger(__name__)


class TemplateContentResponse(SimpleTemplateResponse):
    rendering_attrs = SimpleTemplateResponse.rendering_attrs + ["_request"]

    def resolve_template(self, template_string):
        """
        Load and return a template for the given name.

        Raise TemplateDoesNotExist if no such template exists.
        """
        chain = []
        engines = _engine_list()
        for engine in engines:
            try:
                return engine.from_string(template_string)
            except Exception as e:
                chain.append(e)

        raise TemplateDoesNotExist(template_string, chain=chain)

    def __init__(self, request, template, context=None, content_type=None, status=None, charset=None, using=None):
        super().__init__(template, context, content_type, status, charset, using)
        self._request = request


class TemplateContentResponseMixin(TemplateResponseMixin):
    response_class = TemplateContentResponse

    def get_template_content(self):
        raise NotImplementedError()

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault("content_type", self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_content(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )


class EmailBuilderBasePreview(TemplateContentResponseMixin, BaseDetailView):
    model = EmailBuilder


class EmailBuilderHtmlPreview(EmailBuilderBasePreview):
    def get_template_content(self):
        return self.object.html_content


class EmailBuilderTxtPreview(EmailBuilderBasePreview):
    def get_template_content(self):
        return self.object.content
