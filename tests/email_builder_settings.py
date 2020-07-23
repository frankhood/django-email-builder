_ = lambda s: s

EMAIL_BUILDER_DEFAULT_LIBS_LOADED = [
    "i18n",
    "static",
]

EMAIL_BUILDER_CODE_QUESTION = "question_template"  # pub_date
EMAIL_BUILDER_CODE_CHOICE = "choice_template"  # votes

EMAIL_BUILDER_CODE_CHOICES = [
    (EMAIL_BUILDER_CODE_QUESTION, "Question Template"),
    (EMAIL_BUILDER_CODE_CHOICE, "Choice Template"),
]

EMAIL_BUILDER_CONTEXT_HANDLER_PATH = (
    "tests.polls.controllers.ExampleMailBuilderContextHandler"
)
