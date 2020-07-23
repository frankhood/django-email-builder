import logging

from django.conf.urls import url
from django.utils.translation import ugettext, ugettext_lazy as _

from . import views

logger = logging.getLogger(__name__)

urlpatterns = [
    url(r"^txt-email-preview/$", views.EmailPreviewTxt.as_view({"post": "get_preview"}), name="txt-email-preview"),
    url(r"^html-email-preview/$", views.EmailPreviewHtml.as_view({"post": "get_preview"}), name="html-email-preview"),
    url(
        r"^available-vars/$",
        views.EmailPreviewAvailableVariables.as_view({"get": "get_available_vars"}),
        name="available-vars",
    ),
]
