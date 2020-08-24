""" views
    Created at 10/07/20
"""
import logging

from django.utils.translation import ugettext, ugettext_lazy as _
from rest_framework import mixins, generics, status, viewsets, permissions
from rest_framework.response import Response

from email_builder.api.serializers import EmailBuilderTxtSerializer, EmailBuilderHtmlSerializer
from email_builder.utils import get_email_builder_handler

logger = logging.getLogger(__name__)


class EmailPreviewTxtViewSet(viewsets.GenericViewSet):
    serializer_class = EmailBuilderTxtSerializer
    permission_classes = [permissions.AllowAny]

    def get_preview(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.validated_data, status=status.HTTP_200_OK
        )


class EmailPreviewHtmlViewSet(viewsets.GenericViewSet):
    serializer_class = EmailBuilderHtmlSerializer
    permission_classes = [permissions.AllowAny]

    def get_preview(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.validated_data, status=status.HTTP_200_OK
        )


class EmailPreviewAvailableVariablesViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    def get_available_vars(self, request, *args, **kwargs):
        email_code = request.query_params.get("email_code")
        variables = {}
        if email_code:
            try:
                variables = get_email_builder_handler().get_available_variables_by_email_code(email_code=email_code)
            except Exception as ex:
                raise ex
        else:
            raise Exception("No email code passed")
        return Response(status=status.HTTP_200_OK, data=variables)
