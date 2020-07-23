import factory, factory.django, factory.fuzzy

from tests.polls.models import Question, Choice


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


