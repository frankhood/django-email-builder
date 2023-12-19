import logging

from django.urls import path
from django.utils.translation import gettext, gettext_lazy as _

from . import views

logger = logging.getLogger(__name__)

urlpatterns = [
    path("txt-email-preview/", views.EmailPreviewTxtViewSet.as_view({"post": "get_preview"}), name="txt-email-preview"),
    path("html-email-preview/", views.EmailPreviewHtmlViewSet.as_view({"post": "get_preview"}), name="html-email-preview"),
    path(
        "available-vars/",
        views.EmailPreviewAvailableVariablesViewSet.as_view({"get": "get_available_vars"}),
        name="available-vars",
    ),
]
