import factory, factory.django, factory.fuzzy

from email_builder.models import EmailBuilder
from email_builder.models import email_code_choices
from tests.polls.models import Question, Choice


class EmailBuilderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailBuilder

    description = factory.Faker("paragraph")
    code = factory.fuzzy.FuzzyChoice(email_code_choices)
    subject = factory.Faker("paragraph")
    content = factory.Faker("paragraph")


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    question_text = factory.Faker("paragraph")
    pub_date = factory.Faker("date_time")


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Choice

    question = factory.SubFactory(QuestionFactory)
    choice_text = factory.Faker("paragraph")
    votes = factory.Faker("pyint")


