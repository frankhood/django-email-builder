import logging
from django.conf import settings

from tests.polls.factories import QuestionFactory, ChoiceFactory

logger = logging.getLogger(__name__)

from email_builder.handlers import MailBuilderContextHandler


class ExampleMailBuilderContextHandler(MailBuilderContextHandler):
    @classmethod
    def get_available_variables(cls, email_code=None):

        question_factory = QuestionFactory.stub()
        choice_factory = ChoiceFactory.stub()

        variables = {
            settings.EMAIL_BUILDER_CODE_QUESTION: {
                "available_variables": {
                    "question_pub_date": {"label": "Question Pub Date", "fake_value": question_factory.pub_date},
                }
            },
            settings.EMAIL_BUILDER_CODE_CHOICE: {
                "available_variables": {
                    "choice_votes": {"label": "Choice votes", "fake_value": choice_factory.votes},
                }
            },
        }
        return variables

    # @classmethod
    # def get_available_variables_by_email_code(cls, email_code):
    #     """
    #     This method should return your mail configuration in this form:
    #     {
    #         <varname>: (str nullable),
    #         ...
    #     }
    #
    #     """
    #     available_variables = cls.get_available_variables().get(email_code, {}).get("available_variables", {})
    #     if not available_variables:
    #         logger.warning(f"No variables found for email_code '{email_code}'")
    #     return {k: v.get("label", "") for k, v in available_variables.items()}


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
