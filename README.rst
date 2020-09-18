=============================
Django Email Builder
=============================

.. image:: https://badge.fury.io/py/django-email-builder.svg
    :target: https://badge.fury.io/py/django-email-builder

.. image:: https://travis-ci.org/frankhood/django-email-builder.svg?branch=master
    :target: https://travis-ci.org/frankhood/django-email-builder

.. image:: https://codecov.io/gh/frankhood/django-email-builder/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/django-email-builder

Forget the boring customization of email templates! With our package,
you will disrupt the way how to tailor email through Django Admin!

Documentation
-------------

The full documentation is at https://django-email-builder.readthedocs.io.

Quickstart
----------

Install Django Email Builder:

::

    pip install django-email-builder

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'email_builder',
        ...
    )

Run migrations:
_______________

::

    python manage.py migrate email_builder


Add Django Email Builder's URL patterns:

.. code-block:: python

    urlpatterns = [
        ...
        url(r'^', include("email_builder.api.urls")),
        ...
    ]


Add template choices into yours  `settings.py`:

.. code-block:: python

    EMAIL_BUILDER_DEFAULT_LIBS_LOADED = [
        "i18n",
        "static",
    ]

    EMAIL_BUILDER_CODE_<YOUR_TEMPLATE_NAME> = "<your_template_name>_template"

    EMAIL_BUILDER_CODE_CHOICES = [
        (EMAIL_BUILDER_CODE_<YOUR_TEMPLATE_NAME>, "<Your Template Name> Template"),
    ]

    EMAIL_BUILDER_CONTEXT_HANDLER_PATH = (
        "<your.controller.path>.ExampleMailBuilderContextHandler"
    )


Create the project handler to add your own variables overriding `MailBuilderContextHandler` in `controllers.py` :

.. code-block:: python

    class ExampleMailBuilderContextHandler(MailBuilderContextHandler):
        @classmethod
        def get_available_variables(cls, email_code=None):
            # You can use factories to fill the fake value that will rendered in mail template preview
            factory = <YourModel>Factory.stub()

            variables = {
                settings.EMAIL_BUILDER_CODE_<YOUR_TEMPLATE_NAME>: {
                    "available_variables": {
                        "<your_model_field>": {"label": "Question Pub Date", "fake_value": factory.<your_model_field>},
                    }
                },
            }
            return variables


You can change base mail template adding into yours `settings.py`:

.. code-block:: python

    # for txt rendered mail
    BASE_MAIL_TXT_PATH = "email_templates/base_mail.txt"
    # for html rendered mail
    BASE_MAIL_HTML_PATH = "email_templates/base_mail.html"


Features
--------

* Use customized and ui based django variables into your mail template
* Add your own templatetags into mail template
* See simultaneously what will be displayed in the sent email


Running Tests
-------------

Does the code actually work? discover it with our docker!
It will run your tests with python3.6, python3.7, python3.8

::

    $ docker-compose up tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt

.. include:: ../CONTRIBUTING.rst

.. include:: ../AUTHORS.rst

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
