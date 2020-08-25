import datetime
import logging
from django.conf import settings

from tests.polls.factories import QuestionFactory, ChoiceFactory

logger = logging.getLogger(__name__)

from email_builder.handlers import MailBuilderContextHandler


class ExampleMailBuilderContextHandler(MailBuilderContextHandler):
    @classmethod
    def get_available_variables(cls, email_code=None):
        question_factory = QuestionFactory.stub(pub_date=datetime.datetime(2018, 12, 12, 0, 0, 0))
        choice_factory = ChoiceFactory.stub()

        variables = {
            settings.EMAIL_BUILDER_CODE_QUESTION: {
                "available_variables": {
                    "question_pub_date": {"label": "Question Pub Date", "fake_value": question_factory.pub_date},
                }
            },
            settings.EMAIL_BUILDER_CODE_CHOICE: {
                "available_variables": {"choice_votes": {"label": "Choice votes", "fake_value": choice_factory.votes},}
            },
        }
        return variables
